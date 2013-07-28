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
from komlibs.textman import variables
from komlibs.ai import decisiontree


NOTFOUND=1
ALREADYMONITORED=2
DBERROR=3
PENDINGDTREEGENERATION=4
PROCESSERROR=5

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

    def start(self):
        self.logger = komlogger.getLogger(self.config.conf_file, self.name)
        self.logger.info('Gestconsole module started')
        if not self.params['cass_keyspace'] or not self.params['cass_poolsize'] or not self.params['cass_servlist']:
            self.logger.error('Cassandra connection configuration keys not found')
        elif not self.params['broker']:
            self.logger.error('Key '+options.MESSAGE_BROKER+' not found')
        else:
            self.cass_pool = casscon.Pool(keyspace=self.params['cass_keyspace'], server_list=self.params['cass_servlist'], pool_size=self.params['cass_poolsize'])
            self.cf = casscon.CF(self.cass_pool)
            self.message_bus = bus.MessageBus(self.params['broker'], self.name, self.instance_number, self.hostname, self.logger)
            self.__loop()
        self.logger.info('Gestconsole module exiting')
    
    def __loop(self):
        while True:
            message = self.message_bus.retrieveMessage(from_modaddr=True)
            self.message_bus.ackMessage()
            mtype=message.type
            if mtype==messages.MON_VAR_MESSAGE:
                result,pid,date=self.process_MON_VAR_MESSAGE(message)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.GenerateDTreeMessage(pid=pid,date=date))
                else:
                    self.logger.error('Error processing message: '+mtype+' Error: '+str(pid))
                    #self.message_bus.sendMessage(message)
            elif mtype==messages.NEG_VAR_MESSAGE:
                result,pid,date=self.process_NEG_VAR_MESSAGE(message)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.GenerateDTreeMessage(pid=pid,date=date))
                else:
                    self.logger.error('Error processing message: '+mtype+' Error: '+str(pid))
            elif mtype==messages.POS_VAR_MESSAGE:
                result,pid,date=self.process_POS_VAR_MESSAGE(message)
                if result:
                    self.logger.debug('Message completed successfully: '+mtype)
                    self.message_bus.sendMessage(messages.GenerateDTreeMessage(pid=pid,date=date))
                else:
                    self.logger.error('Error processing message: '+mtype+' Error: '+str(pid))
            else:
                self.logger.error('Message Type not supported: '+mtype)
                self.message_bus.sendMessage(message)
    
    def process_MON_VAR_MESSAGE(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Comprobamos que la variable no pertenezca a un datapoint existente
        - Registramos el nuevo datapoint, marcando la variable como muestra positiva
        '''
        did=message.did
        date=message.date
        pos=message.pos
        length=message.length
        name=message.name
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            return False,NOTFOUND,date
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            return False,NOTFOUND,date
        except Exception:
            return False,PROCESSERROR,date
        dsmap=cassapi.get_datasourcemap(did=did,session=self.cf,date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=pos)
        dsdtprelation=cassapi.get_dsdtprelation(did,self.cf)
        if dsdtprelation:
            for pid in dsdtprelation.dtps:
                dtpinfo=cassapi.get_dtpinfo(pid,{'dtree':u''},self.cf)
                if not dtpinfo:
                    return False,PENDINGDTREEGENERATION,date
                try:
                    stored_dtree=dtpinfo.dbcols['dtree']
                    dtree=decisiontree.DecisionTree(jsontree=json.dumps(stored_dtree))
                    if dtree.evaluate_row(varlist[0].h):
                        return False,ALREADYMONITORED,date
                except KeyError:
                    pass
        else:
            dsdtprelation=cassapi.DsDtpRelation(did=did)
        pid=uuid.uuid4()
        print pid
        newdtp=cassapi.DatapointInfo(pid,name=name,did=did)
        newdtpdtreepositives=cassapi.DatapointDtreePositives(pid)
        newdtpdtreepositives.set_positive(date,[pos,length])
        if cassapi.register_dtp(newdtp,dsdtprelation,self.cf) and cassapi.update_dtp_dtree_positives(newdtpdtreepositives,self.cf):
            return True,newdtp.pid,date
        else:
            return False,DBERROR,date

    def process_NEG_VAR_MESSAGE(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Añadimos la variable a la lista de negativos del datapoint
        '''
        date=message.date
        pos=message.pos
        length=message.length
        pid=message.pid
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        if not dtpinfo:
            return False,NOTFOUND,date
        did=dtpinfo.did
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            return False,NOTFOUND,date
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            return False,NOTFOUND,date
        except Exception:
            return False,PROCESSERROR,date
        #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
        dtpdtreeneg=cassapi.get_dtp_dtree_negatives(pid=pid,date=date,session=self.cf)
        if not dtpdtreeneg:
            dtpdtreeneg=cassapi.DatapointDtreeNegatives(pid=pid)
        dtpdtreeneg.add_negative(date,[pos,length])
        if not cassapi.update_dtp_dtree_negatives(dtpdtreeneg,self.cf):
            return False,PROCESSERROR,date
        #y eliminarla de los positivos si estuviese
        dtpdtreepos=cassapi.get_dtp_dtree_positives(pid=pid,date=date,session=self.cf)
        if not dtpdtreepos:
            dtpdtreepos=cassapi.DatapointDtreePositives(pid=pid)
        dtpdtreepos.del_positive(date,[pos,length])
        if not cassapi.update_dtp_dtree_positives(dtpdtreepos,self.cf):
            return False,PROCESSERROR,date
        return True,pid,date

    def process_POS_VAR_MESSAGE(self, message):
        ''' Los pasos son los siguientes:
        - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
        - Establecemos la variable como positiva
        '''
        date=message.date
        pos=message.pos
        length=message.length
        pid=message.pid
        dtpinfo=cassapi.get_dtpinfo(pid,{},self.cf)
        if not dtpinfo:
            return False,NOTFOUND,date
        did=dtpinfo.did
        dsmapvar = cassapi.get_datasourcemapvars(did=did,session=self.cf,date=date)
        if not dsmapvar: 
            return False,NOTFOUND,date
        try:
            content=json.loads(dsmapvar.content)
            index=content.index([int(pos),int(length)])
        except ValueError:
            return False,NOTFOUND,date
        except Exception:
            return False,PROCESSERROR,date
        #en este punto hemos comprobado que la muestra y variable existen
        #falta establecerla como positivo
        dtpdtreepos=cassapi.get_dtp_dtree_positives(pid=pid,date=date,session=self.cf)
        if not dtpdtreepos:
            dtpdtreepos=cassapi.DatapointDtreePositives(pid=pid)
        dtpdtreepos.set_positive(date,[pos,length])
        if not cassapi.update_dtp_dtree_positives(dtpdtreepos,self.cf):
            return False,PROCESSERROR,date
        #y eliminarla de los negativos si estuviese
        dtpdtreeneg=cassapi.get_dtp_dtree_negatives(pid=pid,date=date,session=self.cf)
        if not dtpdtreeneg:
            dtpdtreeneg=cassapi.DatapointDtreeNegatives(pid=pid)
        dtpdtreeneg.del_negative(date,[pos,length])
        if not cassapi.update_dtp_dtree_negatives(dtpdtreeneg,self.cf):
            return False,PROCESSERROR,date
        return True,pid,date
