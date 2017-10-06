'''
datapoint.py: library for managing datapoints operations

This file implements the logic of different datapoint operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/07/04
author: jcazor
'''

import uuid
import json
import pandas as pd
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.model.orm import datapoint as ormdatapoint
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.ai import errors as aierrors
from komlog.komlibs.ai import exceptions as aiexceptions
from komlog.komlibs.ai.decisiontree import api as dtreeapi
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general import colors
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.textman.api import features as textfeat
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.api import kin as graphkin
from komlog.komlibs.graph.relations import vertex

def get_datapoint_data(pid, fromdate=None, todate=None, count=None):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDD_IP)
    if todate and not args.is_valid_date(todate):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDD_ITD)
    if fromdate and not args.is_valid_date(fromdate):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDD_IFD)
    if count and not args.is_valid_int(count):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDD_ICNT)
    if not todate:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        todate=datapoint_stats.last_received if datapoint_stats and datapoint_stats.last_received else timeuuid.uuid1()
    if not fromdate:
        fromdate=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(todate)-43200)
    datapoint_data=cassapidatapoint.get_datapoint_data(pid=pid,fromdate=fromdate,todate=todate, count=count)
    if len(datapoint_data)==0:
        raise exceptions.DatapointDataNotFoundException(error=Errors.E_GPA_GDD_DDNF, last_date=fromdate)
    else:
        return datapoint_data

def create_user_datapoint(uid, datapoint_uri):
    '''
    Funcion utilizada para la creacion de un datapoint asociado a un usuario
    '''
    if not args.is_valid_uuid(uid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CRUD_IU)
    if not args.is_valid_uri(datapoint_uri):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CRUD_IDU)
    user=cassapiuser.get_user(uid=uid)
    if not user:
        raise exceptions.UserNotFoundException(error=Errors.E_GPA_CRUD_UNF)
    pid=uuid.uuid4()
    if not graphuri.new_datapoint_uri(uid=uid, uri=datapoint_uri, pid=pid):
        raise exceptions.DatapointCreationException(error=Errors.E_GPA_CRUD_UAE)
    color=colors.get_random_color()
    datapoint=ormdatapoint.Datapoint(pid=pid,did=None,uid=uid, datapointname=datapoint_uri,color=color, creation_date=timeuuid.uuid1())
    try:
        if cassapidatapoint.new_datapoint(datapoint):
            return {'pid':datapoint.pid, 'uid':uid, 'datapointname':datapoint.datapointname, 'color':datapoint.color}
        graphuri.dissociate_vertex(ido=pid)
        raise exceptions.DatapointCreationException(error=Errors.E_GPA_CRUD_IDE)
    except cassexcept.KomcassException:
        cassapidatapoint.delete_datapoint(pid=pid)
        graphuri.dissociate_vertex(ido=pid)
        raise

def create_datasource_datapoint(did, datapoint_uri):
    '''
    Funcion utilizada para la creacion de un datapoint asociado a un datasource
    pero sin asociar a ninguna variable en particular
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CRD_ID)
    if not args.is_valid_uri(datapoint_uri):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CRD_IDU)
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GPA_CRD_DNF)
    pid=uuid.uuid4()
    if not graphuri.new_datapoint_uri(did=did, uri=datapoint_uri, pid=pid):
        existing_node=graphuri.get_id(ido=did, uri=datapoint_uri)
        if existing_node and existing_node['type']==vertex.DATAPOINT:
            datapoint=cassapidatapoint.get_datapoint(pid=existing_node['id'])
            if datapoint is None:
                raise exceptions.DatapointCreationException(error=Errors.E_GPA_CRD_INF)
            elif datapoint.did != None:
                if datapoint.did != did:
                    raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_CRD_AAD)
                else:
                    return {'pid':datapoint.pid, 'did':did, 'uid':datapoint.uid, 'datapointname':datapoint.datapointname, 'color':datapoint.color, 'previously_existed':True}
            else:
                datapoint.did=did
                try:
                    if cassapidatapoint.insert_datapoint(datapoint):
                        return {'pid':datapoint.pid, 'did':did, 'uid':datapoint.uid, 'datapointname':datapoint.datapointname, 'color':datapoint.color, 'previously_existed':True}
                    else:
                        raise exceptions.DatapointCreationException(error=Errors.E_GPA_CRD_UDE)
                except cassexcept.KomcassException:
                    datapoint.did=None
                    cassapidatapoint.insert_datapoint(datapoint)
                    raise
        else:
            raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_CRD_ADU)
    else:
        color=colors.get_random_color()
        datapointname='.'.join((datasource.datasourcename, datapoint_uri))
        datapoint=ormdatapoint.Datapoint(pid=pid,did=did,uid=datasource.uid, datapointname=datapointname,color=color, creation_date=timeuuid.uuid1())
        try:
            if cassapidatapoint.new_datapoint(datapoint):
                return {'pid':pid, 'did':did, 'uid':datasource.uid, 'datapointname':datapoint.datapointname, 'color':datapoint.color, 'previously_existed':False}
            else:
                graphuri.dissociate_vertex(ido=pid)
                raise exceptions.DatapointCreationException(error=Errors.E_GPA_CRD_IDE)
        except cassexcept.KomcassException:
            cassapidatapoint.delete_datapoint(pid)
            graphuri.dissociate_vertex(ido=pid)
            raise

def get_datapoint_config(pid, stats_flag=True, widget_flag=True):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDC_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    data={}
    if datapoint:
        data['pid']=pid
        data['datapointname']=datapoint.datapointname if datapoint.datapointname else ''
        data['uid']=datapoint.uid
        data['did']=datapoint.did
        data['color']=datapoint.color if datapoint.color else ''
        if stats_flag:
            datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
            if datapoint_stats:
                data['decimalseparator']=datapoint_stats.decimal_separator if datapoint_stats.decimal_separator else ''
        if widget_flag:
            widget=cassapiwidget.get_widget_dp(pid=pid)
            if widget:
                data['wid']=widget.wid
    else:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_GDC_DNF)
    return data

def update_datapoint_config(pid, datapointname=None, color=None):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_UDC_IP)
    if datapointname and not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException(error=Errors.E_GPA_UDC_IDN)
    if color and not args.is_valid_hexcolor(color):
        raise exceptions.BadParametersException(error=Errors.E_GPA_UDC_IC)
    if not datapointname and not color:
        raise exceptions.BadParametersException(error=Errors.E_GPA_UDC_EMP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint:
        new_datapoint=datapoint
        if datapointname:
            new_datapoint.datapointname=datapointname
        if color:
            new_datapoint.color=color
        try:
            if cassapidatapoint.insert_datapoint(new_datapoint):
                return True
            else:
                raise exceptions.DatapointUpdateException(error=Errors.E_GPA_UDC_IDE)
        except cassexcept.KomcassException:
            cassapidatapoint.insert_datapoint(datapoint)
            raise
    else:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_UDC_DNF)

def mark_negative_variable(pid, date, position, length, dtree_update=True):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Añadimos la variable a la lista de negativos del datapoint
    - Generamos el dtree del datasource si se ha actualizado la info y el parametro dtree_update = True
    '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MNV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MNV_IDT)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MNV_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MNV_IL)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_MNV_DNF)
    if not datapoint.did:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_MNV_DSNF)
    dsmapvars = cassapidatasource.get_datasource_map_variables(did=datapoint.did, date=date)
    if not dsmapvars:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_MNV_DMNF)
    try:
        value=dsmapvars[position]
        if value != length:
            raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MNV_VLNF)
    except KeyError:
        raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MNV_VPNF)
    #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
    updated = False
    if cassapidatapoint.update_datapoint_dtree_negative(pid=pid, date=date, position=position, length=length):
        updated = True
    #y eliminarla de los positivos si coincidiese con la que marcamos como negativo
    if cassapidatapoint.delete_datapoint_dtree_positive(pid=pid, date=date, position=position):
        updated = True
    #y eliminarla de los datapoints del datasourcemap si estuviese asociada a esa variable
    ds_datapoints=cassapidatasource.get_datasource_map_datapoints(did=datapoint.did, date=date)
    if ds_datapoints and pid in ds_datapoints and ds_datapoints[pid]==position:
        cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did,date=date,pid=pid)
    failed_uris = []
    done = []
    pending = []
    dtree_info = {}
    if updated and dtree_update:
        dtree_info = generate_decision_tree(did=datapoint.did)
        if dtree_info['dtree'] != None:
            done.append(datapoint.did)
        else:
            pending.append(datapoint.did)
    elif updated:
        pending.append(datapoint.did)
    return {
        'pending':pending,
        'updated':done,
        **dtree_info
    }

def mark_positive_variable(pid, date, position, length, dtree_update=True):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Establecemos la variable como positiva
    - Marcamos la variable negativa en el resto de pids del datasource
    - Generamos el dtree del datasource si dtree_update = True
    '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MPV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MPV_IDT)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MPV_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MPV_IL)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_MPV_DNF)
    if not datapoint.did:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_MPV_DSNF)
    did=datapoint.did
    dsmap = cassapidatasource.get_datasource_map(did=did, date=date)
    if not dsmap:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_MPV_DMNF)
    try:
        value=dsmap.variables[position]
        if not value==length:
            raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MPV_VLNF)
    except KeyError:
        raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MPV_VPNF)
    ''' en este punto hemos comprobado que la muestra y variable existen y dp pertenece a did indicado.
    solicitaremos que esa variable se marque como negativa en el resto de datapoints asociados
    al datasource '''
    dshash=cassapidatasource.get_datasource_hash(did=did,date=date)
    if not dshash:
        dshash=generate_datasource_hash(did=did, date=date)
    text_hash=json.loads(dshash.content)
    variable_atts=textmanvar.get_variable_atts(text_hash=text_hash, text_pos=position)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    pids.remove(pid)
    ds_datapoints=cassapidatasource.get_datasource_map_datapoints(did=did, date=date)
    response={}
    for a_pid in pids:
        cassapidatapoint.update_datapoint_dtree_negative(pid=a_pid, date=date, position=position, length=length)
        cassapidatapoint.delete_datapoint_dtree_positive(pid=a_pid, date=date, position=position)
        if ds_datapoints and a_pid in ds_datapoints and ds_datapoints[a_pid]==position:
            cassapidatasource.delete_datapoint_from_datasource_map(did=did,date=date,pid=a_pid)
    ''' establecemos la variable como positiva para este datapoint '''
    cassapidatapoint.update_datapoint_dtree_positive(pid=pid, date=date, position=position, length=length)
    cassapidatapoint.delete_datapoint_dtree_negative(pid=pid, date=date, position=position)
    cassapidatasource.add_datapoint_to_datasource_map(did=did, date=date,pid=pid,position=position)
    failed_uris = []
    done = []
    pending = []
    dtree_info = {}
    if dtree_update:
        dtree_info = generate_decision_tree(did=datapoint.did)
        if dtree_info['dtree'] != None:
            done.append(datapoint.did)
        else:
            pending.append(datapoint.did)
    else:
        pending.append(datapoint.did)
    return {
        'pending':pending,
        'updated':done,
        **dtree_info
    }

def mark_missing_datapoint(pid, date, dtree_update=True):
    ''' Se utiliza para indicar que un dp no aparece en una muestra. Los pasos son:
    - Seleccionamos todas las variables de la muestra
    - Añadimos las variables a la lista de negativos del datapoint, eliminando cualquier positivo de esa muestra si lo hubiera.
    - Solicitamos la generacion nuevamente del Dtree del datasource
    '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MMDP_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MMDP_IDT)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_MMDP_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_MMDP_DSNF)
    dsmapvars = cassapidatasource.get_datasource_map_variables(did=datapoint.did, date=date)
    if not dsmapvars:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_MMDP_DMNF)
    updated = False
    for position,length in dsmapvars.items():
        if cassapidatapoint.update_datapoint_dtree_negative(pid=pid, date=date, position=position, length=length):
            updated = True
    #y eliminarla de los positivos si estuviese
    if cassapidatapoint.delete_datapoint_dtree_positive(pid=pid, date=date):
        updated = True
    #y eliminarla de los datapoints del datasourcemap si estuviese
    cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did, date=date, pid=pid)
    failed_uris = []
    done = []
    pending = []
    dtree_info = {}
    if updated and dtree_update:
        dtree_info = generate_decision_tree(did=datapoint.did)
        if dtree_info['dtree'] != None:
            done.append(datapoint.did)
        else:
            pending.append(datapoint.did)
    elif updated:
        pending.append(datapoint.did)
    return {
        'pending':pending,
        'updated':done,
        **dtree_info
    }

def monitor_new_datapoint(did, date, position, length, datapointname):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MND_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MND_IDT)
    if not args.is_valid_int(position):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MND_IPO)
    if not args.is_valid_int(length):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MND_IL)
    if not args.is_valid_datapointname(datapointname):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MND_IDN)
    try:
        widgets_related=False
        datapoint={}
        datapoint=create_datasource_datapoint(did=did, datapoint_uri=datapointname)
        mark_result=mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length, dtree_update=False)
        #add positives from already existing datapoints as negatives to the new one.
        ds_pids = cassapidatapoint.get_datapoints_pids(did=did)
        ds_pids.remove(datapoint['pid'])
        for pid in ds_pids:
            dp_positives = cassapidatapoint.get_datapoint_dtree_positives(pid=pid)
            for positive in dp_positives:
                cassapidatapoint.add_datapoint_dtree_negative_at(datapoint['pid'],date=positive.date, position=positive.position, length=positive.length)
        if datapoint['previously_existed']:
            dswidget=cassapiwidget.get_widget_ds(did=did)
            dpwidget=cassapiwidget.get_widget_dp(pid=datapoint['pid'])
            if dswidget and dpwidget:
                graphkin.kin_widgets(ido=dpwidget.wid, idd=dswidget.wid)
                widgets_related=True
        dtree_info = generate_decision_tree(did=did)
        if datapointname in dtree_info['classified']:
            #store some previous samples so the new datapoint event can show a graph
            store_datapoint_values(pid=datapoint['pid'], date=date, store_newer=False, store_older=True, count=15)
    except:
        if 'pid' in datapoint and datapoint['previously_existed'] is False:
            cassapidatapoint.delete_datapoint(pid=datapoint['pid'])
            cassapidatapoint.delete_datapoint_data(pid=datapoint['pid'])
            graphuri.dissociate_vertex(ido=datapoint['pid'])
        if widgets_related:
            graphkin.unkin_widgets(ido=dpwidget.wid, idd=dswidget.wid)
        raise
    else:
        return {
            **datapoint,
            **dtree_info
        }

def store_user_datapoint_value(pid, date, content):
    ''' This function extract the numeric value of a string and stores it in the database.
        This function is used for storing values of user datapoints, those who are
        sent directly not associated to a datasource. '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IDT)
    if not args.is_valid_datapoint_content(content):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IC)
    value = textmanvar.get_numeric_value_from_string(content)
    if value is None:
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_CVNN)
    datapoint = cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDPSV_DNF)
    datapoint_stats = cassapidatapoint.get_datapoint_stats(pid=pid)
    last_received = datapoint_stats.last_received if datapoint_stats else None
    if cassapidatapoint.insert_datapoint_data(pid=pid, date=date, value=value):
        if last_received == None or last_received.time < date.time:
            cassapidatapoint.set_datapoint_last_received(pid=pid, last_received=date)
        return True
    else:
        raise exceptions.DatapointStoreValueException(error=Errors.E_GPA_SDPSV_IDDE)

def store_datapoint_values(pid, date, store_newer=True, store_older=False, count=None):
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
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPV_IDT)
    datapoint = cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDPV_DNF)
    did = datapoint.did
    if did == None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_SDPV_DSNF)
    datasource = cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GPA_SDPV_DSNF)
    try:
        uri = datapoint.datapointname.split(datasource.datasourcename+'.')[1]
    except KeyError:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_SDPV_URI)
    s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=did)
    if s_dtree == None:
        raise exceptions.DatapointDTreeNotFoundException(error=Errors.E_GPA_SDPV_DTNF)
    dtree = dtreeapi.load_dtree(s_dtree)
    datapoint_stats = cassapidatapoint.get_datapoint_stats(pid=pid)
    decimal_separator = datapoint_stats.decimal_separator if datapoint_stats else None
    last_received = datapoint_stats.last_received if datapoint_stats else None
    datasource_stats = cassapidatasource.get_datasource_stats(did=did)
    if store_newer:
        todate = datasource_stats.last_mapped if datasource_stats and datasource_stats.last_mapped else date
    else:
        todate = date
    if store_older:
        fromdate = timeuuid.LOWEST_TIME_UUID
    else:
        fromdate = date
    dsmaps_dates = cassapidatasource.get_datasource_map_dates(did=did, fromdate=fromdate, todate=todate, count=count)
    for ds_date in dsmaps_dates:
        cassapidatasource.delete_datapoint_from_datasource_map(did=did, date=ds_date, pid=datapoint.pid)
        cassapidatapoint.delete_datapoint_data_at(pid=datapoint.pid, date=ds_date)
        dshash = cassapidatasource.get_datasource_hash(did=did, date=ds_date)
        if not dshash:
            dshash = generate_datasource_hash(did=did, date=ds_date)
        text_hash = json.loads(dshash.content)
        variable_list = textmanvar.get_variables_atts(text_hash=text_hash)
        for element in text_hash['elements']:
            if 'type' in element and element['type']=='var':
                var_atts = textmanvar.get_variable_atts(text_hash=text_hash, text_pos=element['text_pos'])
                var = dtree.classify(var_atts)
                if var and uri in var and var[uri] == 1:
                    value=textmanvar.get_numeric_value(element)
                    if cassapidatapoint.insert_datapoint_data(pid=datapoint.pid, date=ds_date, value=value):
                        cassapidatasource.add_datapoint_to_datasource_map(did=did,date=ds_date,pid=datapoint.pid,position=element['text_pos'])
                        if decimal_separator!=element['decsep']:
                            cassapidatapoint.set_datapoint_decimal_separator(pid=datapoint.pid, decimal_separator=element['decsep'])
                        if last_received is None or last_received.time < ds_date.time:
                            last_received = ds_date
                            cassapidatapoint.set_datapoint_last_received(pid=datapoint.pid, last_received=last_received)
                        break
                    else:
                        raise exceptions.DatapointStoreValueException(error=Errors.E_GPA_SDPV_IDDE)
    return True

def store_datasource_values(did, date):
    '''
    Esta funcion se suele llamar, sobre todo, cada vez que un datasource llega al sistema y se ha realizado la generacion de su dsmap.
    Los pasos son los siguientes:
    - obtenemos el dtree del datasource
    - obtenemos el dsmap y generamos la lista de variables identificadas
    - obtenemos el listado de datapoints, con sus uris asociadas
    - por cada variable:
        - evalua variable
            - si valida se almacena su valor y pasamos a la siguiente variable, marcando el pid como identificado.
            - añadimos esa uri a la lista de ya identificadas, y en caso de detectar una validación doble, informamos.
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDSV_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDSV_IDT)
    datasource = cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GPA_SDSV_DSNF)
    response = {
        'did':datasource.did,
        'uri':datasource.datasourcename,
        'has_dtree':False,
        'dp_found': {},
        'dp_missing': [],
        'dp_found_twice': [],
        'non_dp_uris': [],
    }
    s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=did)
    if s_dtree == None:
        return response
    else:
        response['has_dtree'] = True
    datapoints = cassapidatapoint.get_datapoints(did=did)
    if not datapoints:
        return response
    dshash = cassapidatasource.get_datasource_hash(did=did, date=date)
    if dshash == None:
        dshash = generate_datasource_hash(did=did, date=date)
    dtree = dtreeapi.load_dtree(s_dtree)
    datapoints_info={}
    pids = []
    for dp in datapoints:
        pids.append(dp.pid)
        uri = dp.datapointname.split(datasource.datasourcename+'.')[1]
        datapoint_stats = cassapidatapoint.get_datapoint_stats(pid=dp.pid)
        datapoints_info[uri]={
            'pid':dp.pid,
            'datapointname':dp.datapointname,
            'decsep':datapoint_stats.decimal_separator if datapoint_stats else None,
            'last_received':datapoint_stats.last_received if datapoint_stats else None
        }
    text_hash = json.loads(dshash.content)
    found_twice = set()
    non_dp_uris = set()
    dp_found = []
    dp_found_info = []
    variables = (element for element in text_hash['elements'] if 'type' in element and element['type'] == 'var')
    for var in variables:
        var_atts = textmanvar.get_variable_atts(text_hash=text_hash, text_pos=var['text_pos'])
        classified = dtree.classify(var_atts)
        if classified:
            for uri,score in classified.items():
                if score == 1:
                    if not uri in datapoints_info:
                        non_dp_uris.add(uri)
                        continue
                    pid = datapoints_info[uri]['pid']
                    datapointname = datapoints_info[uri]['datapointname']
                    if pid in dp_found:
                        found_twice.add(pid)
                        continue
                    dp_found.append(pid)
                    dp_found_info.append({'pid':pid, 'uri':datapointname})
                    pids.remove(pid)
                    value = textmanvar.get_numeric_value(variable=var)
                    decimal_separator = datapoints_info[uri]['decsep']
                    last_received = datapoints_info[uri]['last_received']
                    cassapidatapoint.insert_datapoint_data(pid=pid, date=dshash.date, value=value)
                    cassapidatasource.add_datapoint_to_datasource_map(did=did, date=date, pid=pid, position=var['text_pos'])
                    if decimal_separator is None or decimal_separator!=var['decsep']:
                        cassapidatapoint.set_datapoint_decimal_separator(pid=pid, decimal_separator=var['decsep'])
                    if last_received is None or last_received.time < date.time:
                        cassapidatapoint.set_datapoint_last_received(pid=pid, last_received=date)
    response['dp_found'] = dp_found_info
    response['dp_missing'] = pids
    response['dp_found_twice'] = list(found_twice)
    response['non_dp_uris'] = list(non_dp_uris)
    return response

def generate_datasource_hash(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDH_IDID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDH_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if not dsdata:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GPA_GDH_DDNF)
    text_hash = textmanvar.get_hashed_text(text=dsdata.content)
    if text_hash:
        hashobj = ormdatasource.DatasourceHash(did=did,date=date,content=json.dumps(text_hash))
        if cassapidatasource.insert_datasource_hash(obj=hashobj):
            return hashobj
        else:
            raise exceptions.DatasourceHashGenerationException(error=Errors.E_GPA_GDH_EIDB)
    else:
        raise exceptions.DatasourceHashGenerationException(error=Errors.E_GPA_GDH_NHO)

def hook_to_datapoint(pid, sid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_HTDP_IPID)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_HTDP_ISID)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_HTDP_DPNF)
    return cassapidatapoint.insert_datapoint_hook(pid=pid, sid=sid)

def unhook_from_datapoint(pid, sid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_UHFDP_IPID)
    if not args.is_valid_uuid(sid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_UHFDP_ISID)
    return cassapidatapoint.delete_datapoint_hook(pid=pid, sid=sid)

def get_datapoint_hooks(pid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDPH_IPID)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_GDPH_DPNF)
    return cassapidatapoint.get_datapoint_hooks_sids(pid=pid)

def generate_decision_tree(did):
    '''
    Los pasos son los siguientes:
    - Obtenemos la informacion del datasource
    - Obtenemos la informacion de los datapoints del datasource
    - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario)
    - por cada una de las muestras de todos los datapoints del datasource, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
    - En base a la clasificacion obtenida, creamos el arbol de decision
    - lo almacenamos en bbdd
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDT_IDID)
    ds = cassapidatasource.get_datasource(did=did)
    if not ds:
        raise exceptions.DatasourceNotFoundException(error = Errors.E_GPA_GDT_DSNF)
    result = {'classified':[], 'conflicts':[], 'no_positive_tr_set':[], 'dtree':None}
    datapoints = cassapidatapoint.get_datapoints(did=did)
    if not datapoints:
        return result
    pids_uris = {}
    pos_hashes = {}
    neg_hashes = {}
    for dp in datapoints:
        try:
            dp_uri = dp.datapointname.split(ds.datasourcename+'.')[1]
        except IndexError:
            continue
        pids_uris[dp_uri] = dp.pid
        dp_positives = cassapidatapoint.get_datapoint_dtree_positives(pid=dp.pid)
        for positive in dp_positives:
            pos_hashes.setdefault(positive.date,[]).append({'uri':dp_uri,'p':positive.position})
        dp_negatives = cassapidatapoint.get_datapoint_dtree_negatives(pid=dp.pid)
        for negative in dp_negatives:
            neg_hashes.setdefault(negative.date,[]).append({'uri':dp_uri,'p':negative.position})
    tr_set = []
    labels = set()
    hash_data = {}
    for date in pos_hashes.keys():
        hash_data[date] = cassapidatasource.get_datasource_hash(did=did, date=date)
        if not hash_data[date]:
            hash_data[date] = generate_datasource_hash(did=did, date=date)
        var_list = textmanvar.get_variables_atts(text_hash=json.loads(hash_data[date].content))
        for item in pos_hashes[date]:
            for var in var_list:
                p_var = var['atts'].copy()
                p_var['date'] = date
                if var['text_pos'] == item['p']:
                    labels.add(item['uri'])
                    p_var['label'] = item['uri']
                else:
                    p_var['label'] = '!'+item['uri']
                tr_set.append(p_var)
    for date in neg_hashes.keys():
        if not date in hash_data:
            hash_data[date] = cassapidatasource.get_datasource_hash(did=did, date=date)
            if not hash_data[date]:
                hash_data[date] = generate_datasource_hash(did=did, date=date)
        var_list = textmanvar.get_variables_atts(text_hash=json.loads(hash_data[date].content))
        for item in neg_hashes[date]:
            for var in var_list:
                if var['text_pos'] == item['p']:
                    p_var = var['atts'].copy()
                    p_var['date'] = date
                    p_var['label'] = '!'+item['uri']
                    tr_set.append(p_var)
    if len(tr_set) == 0:
        raise exceptions.DatapointDTreeTrainingSetEmptyException(error=Errors.E_GPA_GDT_ETS)
    data = pd.DataFrame(tr_set)
    missing = set(pids_uris.keys()) - labels
    labels = list(labels)
    conflicts = pd.DataFrame(index=labels, columns=labels+['!'+label for label in labels])
    rows = set(labels)
    for row in labels:
        conflicts.loc[row, row] = 0
        conflicts.loc[row, '!'+row] = 1
        for col in rows-{row}:
            conflicts.loc[row, col] = 1
            conflicts.loc[row, '!'+col] = 0
    try:
        dtree = dtreeapi.get_dtree_classifier(data=data, labels=labels, conflicts=conflicts, ignore_features=['date'])
    except aiexceptions.DTreeGenerationException as e:
        if e.error == aierrors.Errors.E_ADA_TMCL_UCFL:
            c_data = e.extra['conflicts']
            c_labels = c_data.label.unique()
            c_dates = c_data.date.unique()
            req_labels = [label for label in labels if label in c_labels]
            conflict_labels = set()
            for label in req_labels:
                if conflicts.loc[conflicts.index == label, c_labels].sum(axis=1).item() > 0:
                    conflict_labels.add(label)
            for label in conflict_labels:
                pid = pids_uris[label]
                result['conflicts'].append({'uri':label,'pid':pid,'dates':sorted(c_dates)})
    else:
        if cassapidatasource.insert_datapoint_classifier_dtree(did, dtree.serialize()):
            result['dtree'] = dtree
    result['classified'] = labels
    result['no_positive_tr_set'] = list(missing)
    return result

def select_dtree_for_datasource(did):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDTDS_IDID)
    datasource = cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GPA_SDTDS_DSNF)
    result = {
        'features':[],
        'updated':False,
        'dtree':None,
    }
    yesterday = timeuuid.get_unix_timestamp(timeuuid.uuid1()) - 86400
    feats = cassapidatasource.get_datasource_features(did=did)
    if feats and timeuuid.get_unix_timestamp(feats.date) > yesterday:
        result['features'] = feats.features
        return result
    samples = []
    ds_dates = cassapidatasource.get_datasource_map_dates(did=did, count=100)
    for ds_date in ds_dates:
        dshash = cassapidatasource.get_datasource_hash(did=did, date=ds_date)
        if not dshash:
            dshash = generate_datasource_hash(did=did, date=ds_date)
        content = json.loads(dshash.content)
        items = [el['hash'] for el in content['elements'] if not 'type' in el or el['type'] != 'var']
        samples.append(items)
    ds_vector = textfeat.get_document_vector(samples)
    features = list(ds_vector.keys())
    if features and cassapidatasource.insert_datasource_features(did, date=timeuuid.uuid1(), features=features):
        result['features'] = features
        result['updated'] = True
    docs = {}
    for feat in features:
        feat_docs = cassapidatasource.get_datasources_by_feature(feature=feat, count=1000)
        for item in feat_docs:
            try:
                docs[item.did][feat] = item.weight
            except KeyError:
                docs[item.did] = {feat:item.weight}
    matching_docs = textfeat.get_matching_documents(query=ds_vector, docs=docs, threshold=0.5, count=1)
    if matching_docs:
        s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=matching_docs[0])
        if s_dtree and cassapidatasource.insert_datapoint_classifier_dtree(did=did, dtree=s_dtree):
            result['dtree'] = dtreeapi.load_dtree(s_dtree)
    return result

def monitor_identified_uris(did, date=None):
    ''' This function will register new datapoints for the uris detected by the ds dtree.

        User can control the dps to register through his supplies.
    '''
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MIU_IDID)
    if date and not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_MIU_IDATE)
    datasource = cassapidatasource.get_datasource(did=did)
    if datasource == None:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_GPA_MIU_DSNF)
    s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=did)
    if s_dtree == None:
        raise exceptions.DatapointDTreeNotFoundException(error=Errors.E_GPA_MIU_DTRNF)
    if date == None:
        ds_stats = cassapidatasource.get_datasource_stats(did=did)
        if ds_stats and ds_stats.last_mapped:
            date = ds_stats.last_mapped
        else:
            raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GPA_MIU_DSDNF)
    dshash = cassapidatasource.get_datasource_hash(did=did, date=date)
    if dshash == None:
        dshash = generate_datasource_hash(did=did, date=date)
    response = {
        'pending':[],
        'monitored':[],
        'monitoring_allowed':False,
        'monitoring_bounded':False,
        'more_than_once':[],
        'creation_failed':[],
        'dtree_info':None,
        'sample_date':date,
    }
    # obtenemos los supplies, para determinar si el usuario quiere que monitoricemos alguna uri en especial o no
    supplies = cassapidatasource.get_last_datasource_supplies_count(did,count=10)
    supply_uris = set()
    if supplies:
        now = timeuuid.get_unix_timestamp(timeuuid.uuid1())
        if len(supplies)>1 and now - timeuuid.get_unix_timestamp(supplies[1].date) < 300:
            # a rudimentary mechanism to limit execution rate
            return response
        if supplies[0].supplies:
            # el usuario ha indicado explicitamente las uris que podemos registrar automáticamente
            response['monitoring_bounded'] = True
            for sup in supplies:
                for uri in sup.supplies:
                    supply_uris.add(uri)
        else:
            # el usuario ha indicado explicitamente que no monitoricemos automaticamente datapoints
            return response
    response['monitoring_allowed'] = True
    datapoint_uris = set()
    datapoints = cassapidatapoint.get_datapoints(did=did)
    for dp in datapoints:
        uri = dp.datapointname.split(datasource.datasourcename+'.')[1]
        datapoint_uris.add(uri)
    if response['monitoring_bounded']:
        pending_uris = supply_uris - datapoint_uris
        if not pending_uris:
            return response
    dtree = dtreeapi.load_dtree(s_dtree)
    text_hash = json.loads(dshash.content)
    candidates = {}
    variables = (element for element in text_hash['elements'] if 'type' in element and element['type'] == 'var')
    for var in variables:
        var_atts = textmanvar.get_variable_atts(text_hash=text_hash, text_pos=var['text_pos'])
        classified = dtree.classify(var_atts)
        if classified:
            for uri,score in classified.items():
                if score == 1:
                    if response['monitoring_bounded'] and uri in pending_uris:
                        candidates.setdefault(uri,[]).append(var)
                    elif not response['monitoring_bounded'] and not uri in datapoint_uris:
                        candidates.setdefault(uri,[]).append(var)
    for uri, variables in candidates.items():
        if len(variables) > 1:
            response['more_than_once'].append(uri)
        else:
            try:
                new_datapoint = create_datasource_datapoint(did, datapoint_uri=uri)
                if new_datapoint['pid']:
                    mark_result = mark_positive_variable(pid=new_datapoint['pid'],date=date,position=variables[0]['text_pos'],length=variables[0]['length'], dtree_update=False)
                    response['monitored'].append({
                        'uri':new_datapoint['datapointname'],
                        'pid':new_datapoint['pid'],
                        'did':did,
                        'aid':datasource.aid,
                        'uid':datasource.uid,
                        'previously_existed':new_datapoint['previously_existed']
                    })
            except exceptions.GestaccountException as e:
                response['creation_failed'].append({'uri':uri, 'error':e.error.value})
    if response['monitored']:
        dtree = generate_decision_tree(did)
        response['dtree_info'] = dtree
        store_datasource_values(did=did, date=date)
    return response

