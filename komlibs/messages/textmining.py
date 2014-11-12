#coding: utf-8
'''
Textmining message definitions

'''

import json
from datetime import datetime,timedelta
from komfig import logger
from komlibs.textman import variables
from komlibs.numeric import weight
from komlibs.ai import decisiontree
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.model.orm import datasource as ormdatasource
from komimc import messages
from komimc import codes as msgcodes

def process_message_GDTREE(message):
    '''
    Los pasos son los siguientes:
    - Obtenemos el pid del mensaje
    - Obtenemos la informacion del datapoint
    - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario)
    - por cada una de las muestras, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
    - En base a la clasificacion obtenida, creamos el arbol de decision
    - lo almacenamos en bbdd
    '''
    msgresult=messages.MessageResult(message)
    pid=message.pid
    mdate=message.date
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        msgresult.retcode=msgcodes.ERROR
        return msgresult
    did=datapoint.did
    dates_to_get=[]
    positive_samples={}
    negative_samples={}
    dtp_positives=cassapidatapoint.get_datapoint_dtree_positives(pid=pid)
    dtp_negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=pid)
    dtree_training_set=[]
    if dtp_positives:
        for dtp_positive in dtp_positives:
            positive_samples[dtp_positive.date]=(dtp_positive.position,dtp_positive.length)
            dates_to_get.append(dtp_positive.date)
    if dtp_negatives:
        for dtp_negative in dtp_negatives:
            negative_samples[dtp_negative.date]=dtp_negative.coordinates
            dates_to_get.append(dtp_positive.date)
    dates_to_get=sorted(set(dates_to_get))
    dsmaps=[]
    for date in dates_to_get:
        dsmap=cassapidatasource.get_datasource_map(did=did, date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content)
        if date in positive_samples:
            position,length=positive_samples[date]
            for var in varlist:
                if var.s==position:
                    var.h['result']=True
                else:
                    var.h['result']=False
                dtree_training_set.append(var.h)
        if date in negative_samples and date not in positive_samples:
            negative_coordinates=negative_samples[date]
            for var in varlist:
                if str(var.s) in iter(negative_coordinates.keys()):
                    var.h['result']=False
                    dtree_training_set.append(var.h)
    dtree=decisiontree.DecisionTree(rawdata=dtree_training_set)
    if cassapidatapoint.set_datapoint_dtree(pid=pid, dtree=dtree.get_jsontree()):
        newmsg=messages.FillDatapointMessage(pid=pid,date=mdate)
        msgresult.add_msg_originated(newmsg)
        msgresult.retcode=msgcodes.SUCCESS
    else:
        msgresult.retcode=msgcodes.ERROR
    return msgresult

def process_message_MAPVARS(message):
    '''
    Los pasos son los siguientes:
    - Obtenemos el datasource del mensaje
    - Obtenemos el contenido
    - extraemos las variables que contiene, con la informacion necesaria para ser identificadas univocamente
    - almacenamos esta informacion en bbdd, por un lado todo el contenido de las variables recien extraido, y por otro el listado completo de variables de cada datasource, para acelerar las busquedas
    '''
    msgresult=messages.MessageResult(message)
    did=message.did
    date=message.date
    varlist=[]
    dsdata=cassapidatasource.get_datasource_data(did=did, date=date)
    if dsdata:
        varlist = variables.get_varlist(dsdata.content)
        mapcontentlist=[]
        mapvarcontentlist={}
        for var in varlist:
            content=var.__dict__
            mapcontentlist.append(content)
            mapvarcontentlist[content['s']]=content['l']
        mapcontentjson=json.dumps(mapcontentlist)
        dsmapobj=ormdatasource.DatasourceMap(did=did,date=date,content=mapcontentjson,variables=mapvarcontentlist)
        datasource_stats=cassapidatasource.get_datasource_stats(did=did)
        try:
            if cassapidatasource.insert_datasource_map(dsmapobj=dsmapobj):
                logger.logger.debug('Map created for did: '+str(did))
            if not datasource_stats or not datasource_stats.last_mapped or datasource_stats.last_mapped<date:
                cassapidatasource.set_last_mapped(did=did, last_mapped=date)
            newmsg=messages.FillDatapointMessage(did=did,date=date)
            msgresult.add_msg_originated(newmsg)
            msgresult.retcode=msgcodes.SUCCESS
        except Exception as e:
            #rollback
            logger.logger.exception('Exception creating Map for did '+str(did)+': '+str(e))
            cassapidatasource.delete_datasource_map(did=did, date=date)
            msgresult.retcode=msgcodes.ERROR
    else:
        logger.logger.error('Datasource data not found: '+str(did)+' '+str(date))
        msgresult.retcode=msgcodes.ERROR
    return msgresult
        

def process_message_FILDTP(message):
    '''
    Los pasos son los siguientes:
    - Obtenemos el pid o el did y date
    - Si recibimos did y date:
      - Lista de variables: las de la fecha recibida
      - lista de dtrees: la de todos los datapoint asociados al datasource
      - lista de muestras: la de la fecha
    - Si recibimos el pid:
      - lista de variables: las de todas las muestras a almacenar
      - lista de dtree: el del datapoint recibido
      - lista de muestras: DE MOMENTO VAMOS A ALMACENAR DESDE UN DIA ATRAS
    - loop:
      - por cada muestra:
        - por cada variable:
          - por cada dtree:
            evalua variable
            if true:
                almacena_valor
                break
    '''
    msgresult=messages.MessageResult(message)
    pid=message.pid
    did=message.did
    date=message.date #depending on the received param, date will be the date of the did or date of the sample whose pid was monitored or modified
    dsmaps=[]
    dtps=[]
    pidonly_flag=False
    if pid:
        pidonly_flag=True
        datapoint=cassapidatapoint.get_datapoint(pid=pid)
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if not datapoint:
            logger.logger.error('Datapoint not found: '+str(pid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        did=datapoint.did
        if datapoint_stats and datapoint_stats.dtree:
            dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
        else:
            logger.logger.error('Datapoint Decision tree not found: '+str(pid))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        dtps.append((datapoint,datapoint_stats,dtree))
        datasource=cassapidatasource.get_datasource(did=did)
        if not datasource:
            logger.logger.error('Datasource not found: '+str(did))
            msgresult.retcode=msgcodes.ERROR
            return msgresult
        datasource_stats=cassapidatasource.get_datasource_stats(did=did)
        end_date=datasource_stats.last_received
        if not end_date:
            end_date=datetime.utcnow()
        if date > end_date:
            init_date=end_date-timedelta(days=1)
        else:
            init_date=date
        #obtenemos los datos
        dsmaps=cassapidatasource.get_datasource_maps(did=did, fromdate=init_date, todate=end_date)
    else:
        dsmaps.append(cassapidatasource.get_datasource_map(did=did, date=date))
        datapoints=cassapidatapoint.get_datapoints(did=did)
        if not datapoints:
            logger.logger.info('Datasource has no datapoints: '+str(did))
            msgresult.retcode=msgcodes.NOOP
            return msgresult
        for datapoint in datapoints:
            datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=datapoint.pid)
            if datapoint_stats and datapoint_stats.dtree:
                dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
                if dtree:
                    dtps.append((datapoint,datapoint_stats,dtree))
    for dsmap in dsmaps:
        varlist=variables.get_varlist(jsoncontent=dsmap.content)
        dtplist=list(dtps)
        for var in varlist:
            for dtp in dtplist:
                datapoint,datapoint_stats,dtree=dtp
                logger.logger.debug('Evaluating var: '+str(var)+' with datapoint dtree: '+str(datapoint.pid))
                if dtree.evaluate_row(var.h):
                    logger.logger.debug('dtree matched var')
                    value,separator=variables.get_numericvalueandseparator(datapoint_stats.decimal_separator,varlist,var)
                    if cassapidatapoint.insert_datapoint_data(pid=datapoint.pid, date=dsmap.date, value=value):
                        cassapidatasource.add_datapoint_to_datasource_map(did=dsmap.did,date=dsmap.date,pid=datapoint.pid,position=var.s)
                        if not datapoint_stats.decimal_separator:
                            cassapidatapoint.set_datapoint_decimal_separator(pid=datapoint.pid, decimal_separator=separator)
                        elif not datapoint_stats.decimal_separator==separator:
                            cassapidatapoint.set_datapoint_decimal_separator(pid=datapoint.pid, decimal_separator=separator)
                        if not datapoint_stats.last_received:
                            cassapidatapoint.set_datapoint_last_received(pid=datapoint.pid, last_received=dsmap.date)
                        elif datapoint_stats.last_received < dsmap.date:
                            cassapidatapoint.set_datapoint_last_received(pid=datapoint.pid, last_received=dsmap.date)
                        dtplist.remove(dtp)
                        break
                    else:
                        logger.logger.error('Error inserting datapoint data: %s_%s' %(dtpinfo.pid,dsmap.date))
                        break
    msgresult.retcode=msgcodes.SUCCESS
    return msgresult
