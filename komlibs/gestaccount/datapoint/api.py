#coding: utf-8
'''
datapoint.py: library for managing datapoints operations

This file implements the logic of different datapoint operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/07/04
author: jcazor
'''

import uuid
import json
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komcass.api import widget as cassapiwidget
from komcass.api import dashboard as cassapidashboard
from komcass.model.orm import datapoint as ormdatapoint
from komlibs.gestaccount import exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.textman import variables
from komlibs.ai import decisiontree
from komfig import logger

def get_datapoint_data(pid, fromdate=None, todate=None):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    if todate and not args.is_valid_date(todate):
        raise exceptions.BadParametersException()
    if fromdate and not args.is_valid_date(fromdate):
        raise exceptions.BadParametersException()
    if not todate:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        todate=datapoint_stats.last_received if datapoint_stats and datapoint_stats.last_received else timeuuid.uuid1()
    if not fromdate:
        fromdate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(todate)-43200)
    datapoint_data_list=cassapidatapoint.get_datapoint_data(pid=pid,fromdate=fromdate,todate=todate)
    data=[]
    if datapoint_data_list==[]:
        raise exceptions.DatapointDataNotFoundException(last_date=fromdate)
    else:
        for datapoint_data in datapoint_data_list:
            data.append({'date':datapoint_data.date,'value':datapoint_data.value})
    return data

def create_datapoint(did, datapointname):
    '''
    Funcion utilizada para la creacion de un datapoint sin asociar a ninguna variable en particular
    '''
    if not args.is_valid_uuid(did) or not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException()
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException()
    pid=uuid.uuid4()
    datapoint=ormdatapoint.Datapoint(pid=pid,did=did,datapointname=datapointname,creation_date=timeuuid.uuid1())
    if cassapidatapoint.new_datapoint(datapoint):
        return {'pid':datapoint.pid, 'did':datapoint.did, 'datapointname':datapoint.datapointname}
    else:
        raise exceptions.DatapointCreationException()

def get_datapoint_config(pid):
    ''' como se ha pasado por las fases de autorización y autenticación, 
    no comprobamos que el pid existe '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    data={}
    data['pid']=pid
    if datapoint:
        data['datapointname']=datapoint.datapointname if datapoint.datapointname else ''
        data['did']=datapoint.did
        data['color']=datapoint.color if datapoint.color else ''
        if datapoint_stats:
            data['decimalseparator']=datapoint_stats.decimal_separator if datapoint_stats.decimal_separator else ''
    else:
        raise exceptions.DatapointNotFoundException()
    return data

def update_datapoint_config(pid, datapointname=None, color=None):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    if datapointname and not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException()
    if color and not args.is_valid_hexcolor(color):
        raise exceptions.BadParametersException()
    if not datapointname and not color:
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint:
        if datapointname:
            datapoint.datapointname=datapointname
        if color:
            datapoint.color=color
        if cassapidatapoint.insert_datapoint(datapoint):
            return True
        else:
            raise exceptions.DatapointUpdateException()
    else:
        raise exceptions.DatapointNotFoundException()

def mark_negative_variable(pid, date, position, length):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Añadimos la variable a la lista de negativos del datapoint
    '''
    if not args.is_valid_uuid(pid) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    dsmapvars = cassapidatasource.get_datasource_map_variables(did=datapoint.did, date=date)
    if not dsmapvars: 
        raise exceptions.DatasourceMapNotFoundException()
    try:
        value=dsmapvars[position]
        if not value==length:
            logger.logger.debug('Received length doesnt match stored value: '+str(datapoint.did)+' '+str(date)+' position: '+str(position)+' length: '+str(length))
            raise exceptions.DatasourceVariableNotFoundException()
    except KeyError:
        logger.logger.debug('Variable not found: '+str(datapoint.did)+' '+str(date)+' position: '+str(position)+' length: '+str(length))
        raise exceptions.DatasourceVariableNotFoundException()
    #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
    if not cassapidatapoint.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length):
        logger.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
        return None
    #y eliminarla de los positivos si estuviese
    if not cassapidatapoint.delete_datapoint_dtree_positive_at(pid=pid, date=date):
        logger.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
        return None
    #y eliminarla de los datapoints del datasourcemap si estuviese
    if not cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did, date=date, pid=pid):
        logger.logger.error('Error deleting datapoint from datasource map')
    generate_decision_tree(pid=pid)
    datapoints_to_update=[]
    datapoints_to_update.append(pid)
    return datapoints_to_update

def mark_positive_variable(pid, date, position, length, replace=True):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Establecemos la variable como positiva
    - Si algun otro datapoint valida la variable marcada, solicitamos la regeneracion del DTREE de dicho datapoint 
    y mandamos un NEGVAR sobre esa variable y ese dtp
    '''
    if not args.is_valid_uuid(pid) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    dsmap = cassapidatasource.get_datasource_map(did=datapoint.did, date=date)
    if not dsmap:
        logger.logger.debug('DSMAP NOT FOUND EXCEPTION: date: '+date.hex+' did: '+datapoint.did.hex)
        raise exceptions.DatasourceMapNotFoundException()
    did=datapoint.did
    try:
        value=dsmap.variables[position]
        if not value==length:
            raise exceptions.DatasourceVariableNotFoundException()
    except KeyError:
        raise exceptions.DatasourceVariableNotFoundException()
    ''' en este punto hemos comprobado que la muestra y variable existen y dtp pertenece a did indicado.
    Comprobamos que no haya otros datapoints que validen esa variable, en caso contrario
    solicitaremos que esa variable se marque como negativa en ellos '''
    varlist=variables.get_varlist(jsoncontent=dsmap.content,onlyvar=str(position))
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    response={}
    datapoints_to_update=[]
    datapoints_to_update.append(pid)
    for a_pid in pids:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=a_pid)
        if not a_pid == pid:
            if datapoint_stats==None or datapoint_stats.dtree==None:
                generate_decision_tree(pid=a_pid)
                datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=a_pid)
            dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
            if dtree.evaluate_row(varlist[0].h):
                if replace:
                    datapoints_to_update.append(a_pid)
                    mark_negative_variable(pid=a_pid, date=date, position=position, length=length)
                else:
                    raise exceptions.VariableMatchesExistingDatapointException()
    ''' establecemos la variable como positiva para este datapoint '''
    if not cassapidatapoint.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length):
        logger.logger.error('Error updating DTree Positives: '+str(pid)+' '+str(date))
        return None
    if not cassapidatapoint.delete_datapoint_dtree_negative_at(pid=pid, date=date, position=position):
        logger.logger.error('Error updating DTree Negatives: '+str(pid)+' '+str(date))
        return None
    if not cassapidatasource.add_datapoint_to_datasource_map(did=did, date=date, pid=pid, position=position):
        logger.logger.error('Error updating datasource map ')
    generate_decision_tree(pid=pid)
    return datapoints_to_update

def generate_decision_tree(pid):
    '''
    Los pasos son los siguientes:
    - Obtenemos la informacion del datapoint
    - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario)
    - por cada una de las muestras, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
    - En base a la clasificacion obtenida, creamos el arbol de decision
    - lo almacenamos en bbdd
    '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
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
            dates_to_get.append(dtp_negative.date)
    dates_to_get=sorted(set(dates_to_get))
    dsmaps=[]
    logger.logger.debug('Vamos a obtener los siguientes dsmaps: '+str(dates_to_get))
    for date in dates_to_get:
        logger.logger.debug('Estamos en: '+str(date))
        dsmap=cassapidatasource.get_datasource_map(did=did, date=date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content)
        logger.logger.debug('sus variables: '+str(varlist))
        if date in positive_samples:
            logger.logger.debug('Esta fecha esta dentro de los positivos')
            position,length=positive_samples[date]
            logger.logger.debug('buscando la variable...')
            for var in varlist:
                if var.s==position:
                    logger.logger.debug('Encontrada, marcando como positiva: '+str(var))
                    var.h['result']=True
                else:
                    logger.logger.debug('NO Encontrada, marcando como negativa: '+str(var))
                    var.h['result']=False
                dtree_training_set.append(var.h)
        if date in negative_samples and date not in positive_samples:
            negative_coordinates=negative_samples[date]
            for var in varlist:
                if var.s in iter(negative_coordinates.keys()):
                    var.h['result']=False
                    dtree_training_set.append(var.h)
    if len(dtree_training_set)>0:
        dtree=decisiontree.DecisionTree(rawdata=dtree_training_set)
        if cassapidatapoint.set_datapoint_dtree(pid=pid, dtree=dtree.get_jsontree()):
            return True
        else:
            return False
    else:
        raise exceptions.DatapointDTreeTrainingSetEmptyException()

def monitor_new_datapoint(did, date, position, length, datapointname):
    if not args.is_valid_uuid(did) or not args.is_valid_date(date) or not args.is_valid_int(position) or not args.is_valid_int(length) or not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException()
    try:
        datapoint={}
        datapoint=create_datapoint(did=did, datapointname=datapointname)
        datapoints_to_update=mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length, replace=False)
        if datapoints_to_update==None:
            return None
        else:
            return datapoint
    except Exception as e:
        if 'pid' in datapoint:
            cassapidatapoint.delete_datapoint(pid=datapoint['pid'])
        logger.logger.debug('Exception monitoring new datapoint: '+str(e))
        raise e

def store_datapoint_values(pid, date, store_newer=True):
    '''
    Esta funcion suele llamarse, sobre todo, cuando un dtree de un datapoint se actualiza,
    debido a que el usuario ha aportado nueva informacion al conjunto de datos de entrenamiento.
    Los pasos son los siguientes:
        - obtenemos pid, dtree y dsmaps desde la fecha pasada hasta el last_mapped (si store_newer=True)
        - por cada dsmap:
            - eliminamos el pid de los datapoints asociados al dsmap de esa fecha.
            - eliminamos el registro de esa fecha asociado al pid en la dat_datapoint.
            - Los dos puntos anteriores lo hacemos porque al modificar un dtree puede haber cambiado el criterio de si se almacena o no, y para evitar estar haciendo comprobaciones, cortamos por lo sano.
            - Posteriormente obtenemos las variables del dsmap y comprobamos una por una si valida el dtree
            - en caso afirmativo se almacena y pasamos al siguiente dsmap. En caso negativo, comprobadas todas las variables, pasariamos al siguiente dsmap tambien.
    '''
    if not args.is_valid_uuid(pid) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    if datapoint==None:
        raise exceptions.DatapointNotFoundException()
    if datapoint_stats==None or datapoint_stats.dtree==None:
        raise exceptions.DatapointDTreeNotFoundException()
    did=datapoint.did
    dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if store_newer:
        todate=datasource_stats.last_mapped
        fromdate=date
    else:
        fromdate=date
        todate=date
    if timeuuid.get_unix_timestamp(date) > timeuuid.get_unix_timestamp(datasource_stats.last_mapped):
        raise exceptions.DatasourceMapNotFoundException()
    dsmaps=cassapidatasource.get_datasource_maps(did=did, fromdate=fromdate, todate=todate)
    for dsmap in dsmaps:
        cassapidatasource.delete_datapoint_from_datasource_map(did=did, date=dsmap.date, pid=datapoint.pid)
        cassapidatapoint.delete_datapoint_data_at(pid=datapoint.pid, date=dsmap.date)
        varlist=variables.get_varlist(jsoncontent=dsmap.content)
        for var in varlist:
            if dtree.evaluate_row(var.h):
                value,separator=variables.get_numericvalueandseparator(datapoint_stats.decimal_separator,varlist,var)
                if cassapidatapoint.insert_datapoint_data(pid=datapoint.pid, date=dsmap.date, value=value):
                    cassapidatasource.add_datapoint_to_datasource_map(did=did,date=dsmap.date,pid=datapoint.pid,position=var.s)
                    if datapoint_stats.decimal_separator!=separator:
                        cassapidatapoint.set_datapoint_decimal_separator(pid=datapoint.pid, decimal_separator=separator)
                    if datapoint_stats.last_received==None or timeuuid.get_unix_timestamp(datapoint_stats.last_received) < timeuuid.get_unix_timestamp(dsmap.date):
                        cassapidatapoint.set_datapoint_last_received(pid=datapoint.pid, last_received=dsmap.date)
                    break
                else:
                    raise exceptions.DatapointStoreValueException()
    return True

def store_datasource_values(did, date):
    '''
    Esta funcion se suele llamar, sobre todo, cada vez que un datasource llega al sistema y se ha realizado la generacion de su dsmap.
    Los pasos son los siguientes:
    - obtenemos todos los datapoints asociados al did, y sus dtrees
    - Obtenemos el dsmap de la fecha recibida y su lista de variables
    - por cada variable:
      - por cada dtree:
        - evalua variable
            - si valida se almacena su valor y pasamos a la siguiente variable.
            - si no valida pasamos al siguiente dtree y volvemos a probar la validacion
    '''
    if not args.is_valid_uuid(did) or not args.is_valid_date(date):
        raise exceptions.BadParametersException()
    dsmap=cassapidatasource.get_datasource_map(did=did, date=date)
    if dsmap==None:
        raise exceptions.DatasourceMapNotFoundException()
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    if pids==[]:
        return True
    datapoints_info={}
    for pid in pids:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if datapoint_stats and datapoint_stats.dtree:
            dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
            if dtree:
                datapoints_info[pid]={'dtree':dtree,
                                      'decimal_separator':datapoint_stats.decimal_separator,
                                      'last_received':datapoint_stats.last_received}
        else:
            generate_decision_tree(pid=pid)
            datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
            if datapoint_stats and datapoint_stats.dtree:
                dtree=decisiontree.DecisionTree(jsontree=datapoint_stats.dtree)
                if dtree:
                    datapoints_info[pid]={'dtree':dtree,
                                          'decimal_separator':datapoint_stats.decimal_separator,
                                          'last_received':datapoint_stats.last_received}
    varlist=variables.get_varlist(jsoncontent=dsmap.content)
    loop_pids=list(datapoints_info.keys())
    for var in varlist:
        for pid in loop_pids:
            dtree=datapoints_info[pid]['dtree']
            decimal_separator=datapoints_info[pid]['decimal_separator']
            last_received=datapoints_info[pid]['last_received']
            if dtree.evaluate_row(var.h):
                value,separator=variables.get_numericvalueandseparator(decimal_separator,varlist,var)
                if cassapidatapoint.insert_datapoint_data(pid=pid, date=dsmap.date, value=value):
                    cassapidatasource.add_datapoint_to_datasource_map(did=dsmap.did,date=dsmap.date,pid=pid,position=var.s)
                    if decimal_separator==None or decimal_separator!=separator:
                        cassapidatapoint.set_datapoint_decimal_separator(pid=pid, decimal_separator=separator)
                    if last_received==None or timeuuid.get_unix_timestamp(last_received)< timeuuid.get_unix_timestamp(dsmap.date):
                        cassapidatapoint.set_datapoint_last_received(pid=pid, last_received=dsmap.date)
                    loop_pids.remove(pid)
                    break
                else:
                    logger.logger.error('Error inserting datapoint data. pid: %s, dsmap.date: %s.' %(pid.hex,date.hex))
                    break
    return True

def delete_datapoint(pid):
    ''' Delete all datapoint info. '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException()
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException()
    datasource=cassapidatasource.get_datasource(did=datapoint.did)
    bids=cassapidashboard.get_dashboards_bids(uid=datasource.uid) if datasource else []
    widget=cassapiwidget.get_widget_dp(pid=pid)
    if widget:
        cassapiwidget.delete_widget(wid=widget.wid)
        for bid in bids:
            cassapidashboard.delete_widget_from_dashboard(wid=widget.wid, bid=bid)
    fromdate=datasource.creation_date if datasource and datasource.creation_date else timeuuid.uuid1(seconds=1)
    dsmap_dates=cassapidatasource.get_datasource_map_dates(did=datapoint.did, fromdate=fromdate, todate=timeuuid.uuid1())
    for date in dsmap_dates:
        cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did, date=date, pid=pid)
    cassapidatapoint.delete_datapoint(pid=pid)
    cassapidatapoint.delete_datapoint_stats(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_positives(pid=pid)
    cassapidatapoint.delete_datapoint_dtree_negatives(pid=pid)
    cassapidatapoint.delete_datapoint_data(pid=pid)
    return True

