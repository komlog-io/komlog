#coding:utf-8
'''

Gestconsole message definitions 

'''

import uuid
from datetime import datetime
from komfig import config, logger, options
from komcass.api import user as cassapiuser
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.model.orm import user as ormuser
from komcass.model.orm import datapoint as ormdatapoint
from komimc import messages
from komimc import codes as msgcodes
from komlibs.textman import variables
from komlibs.ai import decisiontree
from komlibs.general import stringops
from komlibs.mail import types as mailtypes
from komlibs.mail import messages as mailmessages
from komlibs.ifaceops import operations


def process_message_MONVAR(message):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Comprobamos que la variable no pertenezca a un datapoint existente
    - Registramos el nuevo datapoint, marcando la variable como muestra positiva
    - creamos el widget dp
    '''
    msgresult=messages.MessageResult(message)
    did=message.did
    date=message.date
    pos=message.pos
    length=message.length
    name=message.name
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        logger.logger.error('Datasource not found: '+str(did))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    dsmap = cassapidatasource.get_datasource_map(did=did, date=date)
    if not dsmap: 
        logger.logger.error('DatasourceMap not found: '+str(did)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    try:
        value=dsmap.variables[int(pos)]
        if not value==int(length):
            logger.logger.error('Variable length doesnt match stored value'+str(did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
    except KeyError:
        logger.logger.exception('Variable not found: '+str(did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    except Exception as e:
        logger.logger.exception('DatasourceMap exception '+str(e)+': '+str(did)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=pos)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    for pid in pids:
        dtp_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if not dtp_stats.dtree:
            ''' Encontramos dtp sin DTREE. Solicitamos GDTREE y MONVAR nuevamente. Todos los dtp deben
            tener DTREE para saber si la variable solicitada ya está siendo monitorizada '''
            newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
            msgresult.add_msg_originated(newmsg)
            newmsg=message
            msgresult.add_msg_originated(newmsg)
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        try:
            dtree=decisiontree.DecisionTree(jsontree=dtp_stats.dtree)
            if dtree.evaluate_row(varlist[0].h):
                logger.logger.error('Datapoint Already monitored: '+str(datapoint.pid))
                msgresult.retcode=msgcodes.ERROR
                return msgresult
        except KeyError:
            pass
    pid=uuid.uuid4()
    datapoint=ormdatapoint.Datapoint(pid=pid,did=did,datapointname=name,creation_date=datetime.utcnow())
    if cassapidatapoint.new_datapoint(datapoint) and cassapidatapoint.set_datapoint_dtree_positive_at(pid=pid, date=date, position=int(pos), length=int(length)):
        #TODO Creation of widget dp
        operation=operations.NewDatapointOperation(uid=datasource.uid,aid=datasource.aid,did=did,pid=pid)
        newmsg=messages.UpdateQuotesMessage(operation=operation)
        msgresult.add_msg_originated(newmsg)
        newmsg=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgresult.add_msg_originated(newmsg)
        newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
        msgresult.add_msg_originated(newmsg)
        msgcodes.retcode=msgcodes.SUCCESS
        return msgresult
    else:
        logger.logger.error('Error registering datapoint in database. did: '+str(did)+' date: '+str(date)+' pos: '+str(pos))
        msgresult.retcode=msgcodes.ERROR
        return msgresult

def process_message_NEGVAR(message):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Añadimos la variable a la lista de negativos del datapoint
    '''
    msgresult=messages.MessageResult(message)
    date=message.date
    pos=message.pos
    length=message.length
    pid=message.pid
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        logger.logger.error('Datapoint not found: '+str(pid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    dsmapvars = cassapidatasource.get_datasource_map_variables(did=datapoint.did, date=date)
    if not dsmapvars: 
        logger.logger.error('Datasource MapVar not found')
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    try:
        value=dsmapvars[pos]
        if not value==int(length):
            logger.logger.exception('Received length doesnt match stored value: '+str(datapoint.did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
    except KeyError:
        logger.logger.exception('Variable not found: '+str(datapoint.did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
    if not cassapidatapoint.add_datapoint_dtree_negative_at(pid=pid, date=date, position=pos, length=length):
        logger.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    #y eliminarla de los positivos si estuviese
    if not cassapidatapoint.delete_datapoint_dtree_positive_at(pid=pid, date=date, position=pos):
        logger.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
    msgresult.add_msg_originated(newmsg)
    msgresult.retcode=msgcodes.SUCCESS
    return msgresult

def process_message_POSVAR(message):
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
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        logger.logger.error('Datapoint not found: '+str(pid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    if not datapoint.did or not did == datapoint.did:
        logger.logger.error('Datapoint DID does not match Message DID: datapoint.did: '+str(datapoint.did)+' message.did: '+str(did))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    dsmapvars = cassapidatasource.get_datasource_map_variables(did=did, date=date)
    if not dsmapvars: 
        logger.logger.error('Datasource MapVar not found: '+str(did)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    try:
        value=dsmapvars[int(pos)]
        if not value==int(length):
            logger.logger.exception('Received length doesnt match stored value: '+str(did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
    except KeyError:
        logger.logger.exception('Variable not found: '+str(did)+' '+str(date)+' position: '+str(pos)+' length: '+str(length))
        logger.logger.debug(str(dsmapvars))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    ''' en este punto hemos comprobado que la muestra y variable existen y dtp pertenece a did indicado.
    Comprobamos que no haya otros datapoints que validen esa variable, en caso contrario
    solicitaremos que esa variable se marque como negativa en ellos '''
    dsmap=cassapidatasource.get_datasource_map(did=did, date=date)
    varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=str(pos))
    logger.logger.debug('Datasource Varlist: '+str(varlist))
    datapoints=cassapidatapoint.get_datapoints(did=did)
    if datapoints:
        for datapoint in datapoints:
            datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=datapoint.pid)
            if not datapoint.pid == pid and datapoint_stats and datapoint_stats.dtree:
                dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
                if dtree.evaluate_row(varlist[0].h):
                    logger.logger.debug('Variable matched other datapoint. Requesting NEGVAR on it: '+str(datapoint.pid))
                    newmsg=messages.NegativeVariableMessage(did=did,pid=datapoint.pid,date=date,pos=pos,length=length)
                    msgresult.add_msg_originated(newmsg)
    ''' establecemos la variable como positiva para este datapoint '''
    if not cassapidatapoint.set_datapoint_dtree_positive_at(pid=pid, date=date, position=pos, length=length):
        logger.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    #y eliminarla de los negativos si estuviese
    if not cassapidatapoint.delete_datapoint_dtree_negative_at(pid=pid, date=date, position=pos):
        logger.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
    msgresult.add_msg_originated(newmsg)
    msgresult.retcode=msgcodes.SUCCESS
    return msgresult

def process_message_NEWUSR(message):
    ''' Los pasos son los siguientes:
    - Obtenemos la informacion del usuario
    - generamos codigo y mandamos un mail al usuario con el enlace para su activacion
    '''
    msgresult=messages.MessageResult(message)
    uid=message.uid
    user=cassapiuser.get_user(uid=uid)
    if not user:
        logger.logger.error('User not found: '+str(uid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    email=user.email
    if not email:
        logger.logger.error('User email not found: '+str(uid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    signup_code=stringops.get_randomstring(size=32)
    signup_info=ormuser.SignUp(username=user.username, signup_code=signup_code, email=email, creation_date=datetime.utcnow())
    if not cassapiuser.insert_signup_info(signup_info=signup_info):
        logger.logger.error('Error inserting new user code, uid: '+str(uid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    mailargs={'to_address':email,'code':signup_code,'domain':config.get(options.MAIL_DOMAIN)}
    mailmessage=mailmessages.get_message(mailtypes.NEW_USER,mailargs)
    if not self.mailer.send(mailmessage):
        logger.logger.error('Error sending mail, uid: '+str(uid))
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    msgresult.retcode=msgcodes.SUCCESS
    return msgresult

