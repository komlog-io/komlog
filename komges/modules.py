#coding: utf-8

import sections, options
import re
import json
import uuid
from komcass import api as cassapi
from komcass import connection as casscon
from komapp import modules
from komfig import komlogger
from komimc import bus,messages
from komimc import codes as msgcodes
from komlibs.textman import variables
from komlibs.ai import decisiontree
from komlibs.general import stringops
from komlibs.mail import connection as mailcon
from komlibs.mail import types as mailtypes
from komlibs.mail import messages as mailmessages
from komlibs.ifaceops import operations

class Gestconsole(modules.Module):
    def __init__(self, config, instance_number):
        super(Gestconsole,self).__init__(config, self.__class__.__name__, instance_number)
        self.params={}
        self.params['cass_keyspace'] = self.config.safe_get(sections.GESTCONSOLE,options.CASS_KEYSPACE)
        self.params['cass_servlist'] = self.config.safe_get(sections.GESTCONSOLE,options.CASS_SERVLIST).split(',')
        try:
            self.params['cass_poolsize'] = int(self.config.safe_get(sections.GESTCONSOLE,options.CASS_POOLSIZE))
        except Exception:
            self.logger.error('Invalid '+options.CASS_POOLSIZE+'value: setting default (5)')
            self.params['cass_poolsize'] = 5
        self.params['broker'] = self.config.safe_get(sections.GESTCONSOLE, options.MESSAGE_BROKER)
        if not self.params['broker']:
            self.params['broker'] = self.config.safe_get(sections.MAIN, options.MESSAGE_BROKER)
        self.params['mail_server'] = self.config.safe_get(sections.MAIN,options.MAIL_SERVER)
        self.params['mail_user'] = self.config.safe_get(sections.MAIN,options.MAIL_USER)
        self.params['mail_password'] = self.config.safe_get(sections.MAIN,options.MAIL_PASSWORD)
        self.params['mail_domain'] = self.config.safe_get(sections.MAIN,options.MAIL_DOMAIN)

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Gestconsole module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        elif not self.params['mail_server'] or not self.params['mail_user'] or not self.params['mail_password']:
            self.logger.error('Mail configuration parameter not found either server, user or password')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.mailer = mailcon.Mailer(self.params['mail_server'])
            self.mailer.login(self.params['mail_user'],self.params['mail_password'])
            self.__loop()
        self.logger.info('Gestconsole module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            try:
                msgresult=getattr(self,'process_msg_'+mtype)(message)
                messages.process_msg_result(msgresult,self.message_bus,self.logger)
            except AttributeError:
                self.logger.exception('Exception processing message: '+mtype)
            except Exception as e:
                self.logger.exception('Exception processing message: '+str(e))

    def process_msg_MONVAR(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Comprobamos que la variable no pertenezca a un datapoint existente
        - Registramos el nuevo datapoint, marcando la variable como muestra positiva
        '''
        msgresult=messages.MessageResult(message)
        did=message.did
        date=message.date
        pos=message.pos
        length=message.length
        name=message.name
        dsinfo=cassapi.get_dsinfo(did,{},self.cf)
        if not dsinfo:
            self.logger.error('Datasource not found: '+str(did))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            self.logger.error('Datasource MapVar not found: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            self.logger.exception('ValueError Loading content: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        except Exception as e:
            self.logger.exception('Loading content exception '+str(e)+': '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=pos)
        dsdtprelation=cassapi.get_dsdtprelation(did,self.cf)
        if dsdtprelation:
            for pid in dsdtprelation.dtps:
                dtpinfo=cassapi.get_dtpinfo(pid,{'dtree':u''},self.cf)
                if not dtpinfo:
                    ''' Encontramos dtp sin DTREE. Solicitamos GDTREE y MONVAR nuevamente. Todos los dtp deben
                    tener DTREE para saber si la variable solicitada ya está siendo monitorizada '''
                    newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
                    msgresult.add_msg_originated(newmsg)
                    newmsg=message
                    msgresult.add_msg_originated(newmsg)
                    msgresult.retcode=msgcodes.ERROR
                    return msgresult
                try:
                    stored_dtree=dtpinfo.dbcols['dtree']
                    dtree=decisiontree.DecisionTree(jsontree=json.dumps(stored_dtree))
                    if dtree.evaluate_row(varlist[0].h):
                        self.logger.error('Datapoint Already monitored: '+str(pid))
                        msgresult.retcode=msgcodes.ERROR
                        return msgresult
                except KeyError:
                    pass
        else:
            dsdtprelation=cassapi.DsDtpRelation(did=did)
        pid=uuid.uuid4()
        newdtp=cassapi.DatapointInfo(pid,name=name,did=did)
        newdtpdtreepositives=cassapi.DatapointDtreePositives(pid)
        newdtpdtreepositives.set_positive(date,[pos,length])
        if cassapi.register_dtp(newdtp,dsdtprelation,self.cf) and cassapi.update_dtp_dtree_positives(newdtpdtreepositives,self.cf):
            aginfo=cassapi.get_agentinfo(dsinfo.aid,{},self.cf)
            operation=operations.NewDatapointOperation(uid=aginfo.uid,aid=dsinfo.aid,did=did,pid=pid)
            newmsg=messages.UpdateQuotesMessage(operation=operation)
            msgresult.add_msg_originated(newmsg)
            newmsg=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgresult.add_msg_originated(newmsg)
            newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
            msgresult.add_msg_originated(newmsg)
            msgcodes.retcode=msgcodes.SUCCESS
            return msgresult
        else:
            self.logger.error('Error registering datapoint in database. did: '+str(did)+' date: '+str(date)+' pos: '+str(pos))
            msgresult.retcode=msgcodes.ERROR
            return msgresult

    def process_msg_NEGVAR(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Añadimos la variable a la lista de negativos del datapoint
        '''
        msgresult=messages.MessageResult(message)
        date=message.date
        pos=message.pos
        length=message.length
        pid=message.pid
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        if not dtpinfo:
            self.logger.error('Datapoint not found: '+str(pid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        did=dtpinfo.did
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            self.logger.error('Datasource MapVar not found')
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            self.logger.exception('ValueError loading content: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        except Exception:
            self.logger.exception('Exception loading content: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
        dtpdtreeneg=cassapi.get_dtp_dtree_negatives(pid=pid,date=date,session=self.cf)
        if not dtpdtreeneg:
            dtpdtreeneg=cassapi.DatapointDtreeNegatives(pid=pid)
        dtpdtreeneg.add_negative(date,[pos,length])
        if not cassapi.update_dtp_dtree_negatives(dtpdtreeneg,self.cf):
            self.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        #y eliminarla de los positivos si estuviese
        dtpdtreepos=cassapi.get_dtp_dtree_positives(pid=pid,date=date,session=self.cf)
        if not dtpdtreepos:
            dtpdtreepos=cassapi.DatapointDtreePositives(pid=pid)
        dtpdtreepos.del_positive(date,[pos,length])
        if not cassapi.update_dtp_dtree_positives(dtpdtreepos,self.cf):
            self.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
        msgresult.add_msg_originated(newmsg)
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

    def process_msg_POSVAR(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Establecemos la variable como positiva
        - Si algun otro datapoint valida la variable marcada, solicitamos la regeneracion del DTREE de dicho datapoint 
        y mandamos un NEGVAR sobre esa variable y ese dtp
        '''
        msgresult=messages.MessageResult(message)
        date=message.date
        pos=message.pos
        length=message.length
        did=message.did
        pid=message.pid
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        if not dtpinfo:
            self.logger.error('Datapoint not found: '+str(pid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        if not dtpinfo.did or not did == dtpinfo.did:
            self.logger.error('Datapoint DID not matchs Message DID: dtp_did: '+str(dtpinfo.did)+' msg_did: '+str(did))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            self.logger.error('Datasource MapVar not found: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            self.logger.exception('ValueError loading content: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        except Exception:
            self.logger.exception('ValueError loading content: '+str(did)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        ''' en este punto hemos comprobado que la muestra y variable existen y dtp pertenece a did indicado.
        Comprobamos que no haya otros datapoints que validen esa variable, en caso contrario
        solicitaremos que esa variable se marque como negativa en ellos '''
        dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=pos)
        dsdtprelation=cassapi.get_dsdtprelation(did,self.cf)
        if dsdtprelation:
            pids=dsdtprelation.dtps
            pids.pop(pid)
            for apid in pids:
                dtpinfo=cassapi.get_dtpinfo(apid,{'dtree':u''},self.cf)
                if dtpinfo:
                    stored_dtree=dtpinfo.dbcols['dtree']
                    dtree=decisiontree.DecisionTree(jsontree=json.dumps(stored_dtree))
                    if dtree.evaluate_row(varlist[0].h):
                        self.logger.debug('Variable matched other datapoint. Requesting NEGVAR on it: '+str(apid))
                        newmsg=messages.NegativeVariableMessage(did=did,pid=apid,date=date,pos=pos,length=length)
                        msgresult.add_msg_originated(newmsg)
        ''' establecemos la variable como positiva para este datapoint '''
        dtpdtreepos=cassapi.get_dtp_dtree_positives(pid=pid,date=date,session=self.cf)
        if not dtpdtreepos:
            dtpdtreepos=cassapi.DatapointDtreePositives(pid=pid)
        dtpdtreepos.set_positive(date,[pos,length])
        if not cassapi.update_dtp_dtree_positives(dtpdtreepos,self.cf):
            self.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        #y eliminarla de los negativos si estuviese
        dtpdtreeneg=cassapi.get_dtp_dtree_negatives(pid=pid,date=date,session=self.cf)
        if not dtpdtreeneg:
            dtpdtreeneg=cassapi.DatapointDtreeNegatives(pid=pid)
        dtpdtreeneg.del_negative(date,[pos,length])
        if not cassapi.update_dtp_dtree_negatives(dtpdtreeneg,self.cf):
            self.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
        msgresult.add_msg_originated(newmsg)
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

    def process_msg_NEWUSR(self, message):
        ''' Los pasos son los siguientes:
        - Obtenemos la informacion del usuario
        - generamos codigo y mandamos un mail al usuario con el enlace para su activacion
        '''
        msgresult=messages.MessageResult(message)
        uid=message.uid
        userinfo=cassapi.get_userinfo(uid,{},self.cf)
        if not userinfo:
            self.logger.error('User not found: '+str(uid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        email=userinfo.email
        if not email:
            self.logger.error('User email not found: '+str(uid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        new_code=stringops.get_randomstring(size=32)
        usercoder=cassapi.UserCodeRelation(email,new_code)
        if not cassapi.insert_usercoderelation(usercoder,self.cf):
            self.logger.error('Error inserting new user code, uid: '+str(uid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        mailargs={'to_address':email,'code':new_code,'domain':self.params['mail_domain']}
        mailmessage=mailmessages.get_message(mailtypes.NEW_USER,mailargs)
        if not self.mailer.send(mailmessage):
            self.logger.error('Error sending mail, uid: '+str(uid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        msgresult.retcode=msgcodes.SUCCESS
        return msgresult

