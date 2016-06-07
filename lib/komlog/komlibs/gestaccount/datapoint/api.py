'''
datapoint.py: library for managing datapoints operations

This file implements the logic of different datapoint operations at a service level.
At this point, authorization and autentication has been passed

creation date: 2013/07/04
author: jcazor
'''

import uuid
import json
import pickle
from komlog.komcass import exceptions as cassexcept
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.model.orm import datapoint as ormdatapoint
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komlibs.ai.decisiontree import api as dtreeapi
from komlog.komlibs.ai.svm import api as svmapi
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general import colors
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.textman.api import summary as textmansummary
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
            elif datapoint.did:
                raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_CRD_AAD)
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

def get_datapoint_config(pid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDC_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    data={}
    data['pid']=pid
    if datapoint:
        data['datapointname']=datapoint.datapointname if datapoint.datapointname else ''
        data['uid']=datapoint.uid
        data['did']=datapoint.did
        data['color']=datapoint.color if datapoint.color else ''
        if datapoint_stats:
            data['decimalseparator']=datapoint_stats.decimal_separator if datapoint_stats.decimal_separator else ''
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

def mark_negative_variable(pid, date, position, length):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Añadimos la variable a la lista de negativos del datapoint
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
        if not value==length:
            raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MNV_VLNF)
    except KeyError:
        raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MNV_VPNF)
    #en este punto hemos comprobado que la muestra y variable existen, falta añadirla al listado de negativos
    if not cassapidatapoint.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length):
        return None
    #y eliminarla de los positivos si coincidiese con la que marcamos como negativo
    positive=cassapidatapoint.get_datapoint_dtree_positives_at(pid=pid, date=date)
    if positive and positive.position==position and positive.length==length:
        if not cassapidatapoint.delete_datapoint_dtree_positive_at(pid=pid, date=date):
            return None
    #y eliminarla de los datapoints del datasourcemap si estuviese asociada a esa variable
    ds_datapoints=cassapidatasource.get_datasource_map_datapoints(did=datapoint.did, date=date)
    if ds_datapoints and pid in ds_datapoints and ds_datapoints[pid]==position:
        cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did,date=date,pid=pid)
    generate_decision_tree(pid=pid)
    generate_inverse_decision_tree(pid=pid)
    datapoints_to_update=[]
    datapoints_to_update.append(pid)
    return datapoints_to_update

def mark_positive_variable(pid, date, position, length):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Establecemos la variable como positiva
    - Marcamos la variable negativa en el resto de pids del datasource y regeneramos sus dtrees
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
    dsmap = cassapidatasource.get_datasource_map(did=datapoint.did, date=date)
    if not dsmap:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_MPV_DMNF)
    did=datapoint.did
    try:
        value=dsmap.variables[position]
        if not value==length:
            raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MPV_VLNF)
    except KeyError:
        raise exceptions.DatasourceVariableNotFoundException(error=Errors.E_GPA_MPV_VPNF)
    ''' en este punto hemos comprobado que la muestra y variable existen y 
    dtp pertenece a did indicado.
    solicitaremos que esa variable se marque como negativa en el resto de datapoints asociados
    al datasource '''
    dshash=cassapidatasource.get_datasource_hash(did=datapoint.did,date=date)
    if not dshash:
        dshash=generate_datasource_hash(did=datapoint.did, date=date)
    text_hash=json.loads(dshash.content)
    variable_atts=textmanvar.get_variable_atts(text_hash=text_hash, text_pos=position)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    pids.remove(pid)
    response={}
    datapoints_to_update=[]
    datapoints_to_update.append(pid)
    for a_pid in pids:
        mark_negative_variable(pid=a_pid, date=date, position=position, length=length)
        datapoints_to_update.append(a_pid)
    ''' establecemos la variable como positiva para este datapoint '''
    if not cassapidatapoint.set_datapoint_dtree_positive_at(pid=pid, date=date, position=position, length=length):
        return None
    if not cassapidatapoint.delete_datapoint_dtree_negative_at(pid=pid, date=date, position=position):
        return None
    cassapidatasource.add_datapoint_to_datasource_map(did=did,date=date,pid=pid,position=position)
    generate_decision_tree(pid=pid)
    generate_inverse_decision_tree(pid=pid)
    return datapoints_to_update

def mark_missing_datapoint(pid, date):
    ''' Se utiliza para indicar que un dp no aparece en una muestra. Los pasos son:
    - Seleccionamos todas las variables de la muestra
    - Añadimos las variables a la lista de negativos del datapoint, eliminando cualquier positivo de esa muestra si lo hubiera.
    - Solicitamos la generacion nuevamente de los Dtree
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
    for position,length in dsmapvars.items():
        if not cassapidatapoint.add_datapoint_dtree_negative_at(pid=pid, date=date, position=position, length=length):
            return None
    #y eliminarla de los positivos si estuviese
    if not cassapidatapoint.delete_datapoint_dtree_positive_at(pid=pid, date=date):
        return None
    #y eliminarla de los datapoints del datasourcemap si estuviese
    cassapidatasource.delete_datapoint_from_datasource_map(did=datapoint.did, date=date, pid=pid)
    generate_decision_tree(pid=pid)
    generate_inverse_decision_tree(pid=pid)
    datapoints_to_update=[]
    datapoints_to_update.append(pid)
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
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDT_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_GDT_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_GDT_DSNF)
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
    dshashes=[]
    for date in dates_to_get:
        dshash=cassapidatasource.get_datasource_hash(did=did, date=date)
        if not dshash:
            dshash=generate_datasource_hash(did=did, date=date)
        text_hash=json.loads(dshash.content)
        variable_list=textmanvar.get_variables_atts(text_hash=text_hash)
        if date in positive_samples:
            position,length=positive_samples[date]
            for var in variable_list:
                if var['text_pos']==position:
                    var['atts']['result']=True
                else:
                    var['atts']['result']=False
                dtree_training_set.append(var['atts'])
        if date in negative_samples and date not in positive_samples:
            negative_coordinates=negative_samples[date]
            for var in variable_list:
                if var['text_pos'] in iter(negative_coordinates.keys()):
                    var['atts']['result']=False
                    dtree_training_set.append(var['atts'])
    if len(dtree_training_set)>0:
        dtree=dtreeapi.generate_decision_tree(training_set=dtree_training_set)
        if cassapidatapoint.set_datapoint_dtree(pid=pid, dtree=dtree.serialize()):
            return True
        else:
            return False
    else:
        raise exceptions.DatapointDTreeTrainingSetEmptyException(error=Errors.E_GPA_GDT_ETS)

def generate_inverse_decision_tree(pid):
    '''
    Los pasos son los siguientes:
    - Obtenemos la informacion del datapoint
    - creamos un listado con las muestras que contienen variables positivas o negativas (confirmadas o descartadas por el usuario), pero a diferencia con generate_decision_tree() las positivas las marcamos como negativas y las negativas como positivas
    - por cada una de las muestras, obtenemos las variables y las clasificamos segun la info obtenida del datapoint
    - En base a la clasificacion obtenida, creamos el arbol de decision
    - lo almacenamos en bbdd
    '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GIDT_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_GIDT_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_GIDT_DSNF)
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
    for date in dates_to_get:
        dshash=cassapidatasource.get_datasource_hash(did=did, date=date)
        if not dshash:
            dshash=cassapidatasource.generate_datasource_hash(did=did, date=date)
        text_hash=json.loads(dshash.content)
        variable_list=textmanvar.get_variables_atts(text_hash=text_hash)
        if date in positive_samples:
            position,length=positive_samples[date]
            for var in variable_list:
                if var['text_pos']==position:
                    var['atts']['result']=False
                else:
                    var['atts']['result']=True
                dtree_training_set.append(var['atts'])
        if date in negative_samples and date not in positive_samples:
            negative_coordinates=negative_samples[date]
            for var in variable_list:
                if var['text_pos'] in iter(negative_coordinates.keys()):
                    var['atts']['result']=True
                    dtree_training_set.append(var['atts'])
    if len(dtree_training_set)>0:
        dtree=dtreeapi.generate_decision_tree(training_set=dtree_training_set)
        return cassapidatapoint.set_datapoint_dtree_inv(pid=pid, dtree=dtree.serialize())
    else:
        raise exceptions.DatapointDTreeTrainingSetEmptyException(error=Errors.E_GPA_GIDT_ETS)

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
        datapoints_to_update=mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        if datapoints_to_update==None:
            return None
        else:
            if datapoint['previously_existed']:
                dswidget=cassapiwidget.get_widget_ds(did=did)
                dpwidget=cassapiwidget.get_widget_dp(pid=datapoint['pid'])
                if dswidget and dpwidget:
                    graphkin.kin_widgets(ido=dpwidget.wid, idd=dswidget.wid)
                    widgets_related=True
            return datapoint
    except:
        if 'pid' in datapoint and datapoint['previously_existed'] is False:
            cassapidatapoint.delete_datapoint(pid=datapoint['pid'])
            graphuri.dissociate_vertex(ido=datapoint['pid'])
        if widgets_related:
            graphkin.unkin_widgets(ido=dpwidget.wid, idd=dswidget.wid)
        raise

def store_user_datapoint_value(pid, date, content):
    ''' This function extract the numeric value of a string and stores it in the database.
        This function is used for storing values of user datapoints, those who are
        sent directly not associated to a datasource. '''
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IDT)
    if not args.is_valid_string(content):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_IC)
    value=textmanvar.get_numeric_value_from_string(content)
    if value is None:
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPSV_CVNN)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDPSV_DNF)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    last_received=datapoint_stats.last_received if datapoint_stats else None
    if cassapidatapoint.insert_datapoint_data(pid=pid, date=date, value=value):
        if last_received==None or last_received.time<date.time:
            cassapidatapoint.set_datapoint_last_received(pid=pid, last_received=date)
        return True
    else:
        raise exceptions.DatapointStoreValueException(error=Errors.E_GPA_SDPSV_IDDE)

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
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDPV_IDT)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDPV_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_SDPV_DSNF)
    if datapoint_stats is None or datapoint_stats.dtree is None:
        raise exceptions.DatapointDTreeNotFoundException(error=Errors.E_GPA_SDPV_DTNF)
    did=datapoint.did
    dtree=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree)
    datasource_stats=cassapidatasource.get_datasource_stats(did=did)
    if store_newer:
        todate=datasource_stats.last_mapped
        fromdate=date
    else:
        fromdate=date
        todate=date
    if date.time > datasource_stats.last_mapped.time:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_SDPV_DMNF)
    dsmaps=cassapidatasource.get_datasource_maps(did=did, fromdate=fromdate, todate=todate)
    for dsmap in dsmaps:
        cassapidatasource.delete_datapoint_from_datasource_map(did=did, date=dsmap.date, pid=datapoint.pid)
        cassapidatapoint.delete_datapoint_data_at(pid=datapoint.pid, date=dsmap.date)
        dshash=cassapidatasource.get_datasource_hash(did=did, date=dsmap.date)
        if not dshash:
            dshash=generate_datasource_hash(did=did, date=dsmap.date)
        text_hash=json.loads(dshash.content)
        variable_list=textmanvar.get_variables_atts(text_hash=text_hash)
        for element in text_hash['elements']:
            if 'type' in element and element['type']=='var':
                var_atts=textmanvar.get_variable_atts(text_hash=text_hash, text_pos=element['text_pos'])
                if dtree.evaluate_row(var_atts):
                    value=textmanvar.get_numeric_value(element)
                    if cassapidatapoint.insert_datapoint_data(pid=datapoint.pid, date=dsmap.date, value=value):
                        cassapidatasource.add_datapoint_to_datasource_map(did=did,date=dsmap.date,pid=datapoint.pid,position=element['text_pos'])
                        if datapoint_stats.decimal_separator!=element['decsep']:
                            cassapidatapoint.set_datapoint_decimal_separator(pid=datapoint.pid, decimal_separator=element['decsep'])
                        if datapoint_stats.last_received is None or datapoint_stats.last_received.time < dsmap.date.time:
                            cassapidatapoint.set_datapoint_last_received(pid=datapoint.pid, last_received=dshash.date)
                        break
                    else:
                        raise exceptions.DatapointStoreValueException(error=Errors.E_GPA_SDPV_IDDE)
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
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDSV_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDSV_IDT)
    dshash=cassapidatasource.get_datasource_hash(did=did, date=date)
    if dshash==None:
        dshash=generate_datasource_hash(did=did, date=date)
    pids=cassapidatapoint.get_datapoints_pids(did=did)
    if pids==[]:
        return True
    datapoints_info={}
    for pid in pids:
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if datapoint_stats and datapoint_stats.dtree:
            dtree=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree)
            if dtree:
                datapoints_info[pid]={
                    'dtree':dtree,
                    'decsep':datapoint_stats.decimal_separator,
                    'last_received':datapoint_stats.last_received
                }
        else:
            generate_decision_tree(pid=pid)
            datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
            if datapoint_stats and datapoint_stats.dtree:
                dtree=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree)
                if dtree:
                    datapoints_info[pid]={
                        'dtree':dtree,
                        'decsep':datapoint_stats.decimal_separator,
                        'last_received':datapoint_stats.last_received
                    }
    text_hash=json.loads(dshash.content)
    loop_pids=list(datapoints_info.keys())
    for element in text_hash['elements']:
        if 'type' in element and element['type']=='var':
            var_atts=textmanvar.get_variable_atts(text_hash=text_hash, text_pos=element['text_pos'])
            for pid in loop_pids:
                dtree=datapoints_info[pid]['dtree']
                decimal_separator=datapoints_info[pid]['decsep']
                last_received=datapoints_info[pid]['last_received']
                if dtree.evaluate_row(var_atts):
                    value=textmanvar.get_numeric_value(variable=element)
                    if cassapidatapoint.insert_datapoint_data(pid=pid, date=dshash.date, value=value):
                        cassapidatasource.add_datapoint_to_datasource_map(did=dshash.did,date=dshash.date,pid=pid,position=element['text_pos'])
                        if decimal_separator is None or decimal_separator!=element['decsep']:
                            cassapidatapoint.set_datapoint_decimal_separator(pid=pid, decimal_separator=element['decsep'])
                        if last_received is None or last_received.time < dshash.date.time:
                            cassapidatapoint.set_datapoint_last_received(pid=pid, last_received=dshash.date)
                        loop_pids.remove(pid)
                        break
                    else:
                        break
    return {'dp_not_found':loop_pids}

def should_datapoint_match_any_sample_variable(pid, date):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDMSV_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDMSV_IDT)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDMSV_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_SDMSV_DSNF)
    datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    if not datapoint_stats or not datapoint_stats.dtree:
        generate_decision_tree(pid=pid)
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    if not datapoint_stats or not datapoint_stats.dtree_inv:
        generate_inverse_decision_tree(pid=pid)
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
    if not datapoint_stats or not datapoint_stats.dtree or not datapoint_stats.dtree_inv:
        raise exceptions.DatapointDTreeNotFoundException(error=Errors.E_GPA_SDMSV_DPDTNF)
    #obtenemos el map de la muestra, con las variables y datapoints detectados en ella
    dsmap=cassapidatasource.get_datasource_map(did=datapoint.did, date=date)
    if not dsmap:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_SDMSV_DSMNF)
    #si el datapoint ya esta detectado devolvemos true
    if pid in dsmap.datapoints.keys():
        return True
    #evaluamos el DTREE sobre las variables (en teoria todas evaluaran a false, pero si alguna evalua a true devolvemos true). Después evaluamos el DTREE INVERSO sobre ellas (si hay alguna que no da FALSE entonces devolvemos un TRUE, indicando que hay candidatas a que sean matchs)
    dtree=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree)
    dtree_inv=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree_inv)
    dshash=cassapidatasource.get_datasource_hash(did=datapoint.did, date=date)
    if not dshash:
        dshash=generate_datasource_hash(did=datapoint.did, date=date)
    text_hash=json.loads(dshash.content)
    variable_list=textmanvar.get_variables_atts(text_hash=text_hash)
    for var in variable_list:
        if not var['text_pos'] in dsmap.datapoints.values() and (dtree.evaluate_row(var['atts']) or not dtree_inv.evaluate_row(var['atts'])):
            return True
    return False

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

def generate_datasource_text_summary(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDTS_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDTS_IDT)
    dsdata=cassapidatasource.get_datasource_data_at(did=did, date=date)
    if dsdata:
        summary=textmansummary.get_summary_from_text(text=dsdata.content)
        obj=ormdatasource.DatasourceTextSummary(did=did,date=date,content_length=summary.content_length, num_lines=summary.num_lines, num_words=summary.num_words, word_frecuency=summary.word_frecuency)
        if cassapidatasource.insert_datasource_text_summary(dstextsummaryobj=obj):
            return True
        return False
    else:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GPA_GDTS_DDNF)

def generate_datasource_novelty_detector_for_datapoint(pid):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_GDNDFD_IP)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_GDNDFD_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_GDNDFD_DSNF)
    inline_dates=[]
    for sample in cassapidatapoint.get_datapoint_dtree_positives(pid=pid):
        inline_dates.append(sample.date)
    init_date=timeuuid.uuid1(seconds=1)
    end_date=timeuuid.uuid1()
    count=1000
    for reg in cassapidatapoint.get_datapoint_data(pid=pid, fromdate=init_date, todate=end_date, count=count):
        inline_dates.append(reg['date'])
    inline_dates=sorted(list(set(inline_dates)))
    if len(inline_dates)==0:
        raise exceptions.DatasourceDataNotFoundException(error=Errors.E_GPA_GDNDFD_DSDNF)
    samples=[]
    for date in inline_dates:
        textsumm=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
        if textsumm:
            samples.append(textsumm.word_frecuency)
    nd=svmapi.generate_novelty_detector_for_datasource(samples=samples)
    if not nd:
        raise exceptions.DatasourceNoveltyDetectorException(error=Errors.E_GPA_GDNDFD_NDF)
    datasource_novelty_detector=ormdatasource.DatasourceNoveltyDetector(did=datapoint.did, pid=pid, date=timeuuid.uuid1(), nd=pickle.dumps(nd.novelty_detector), features=nd.features)
    return cassapidatasource.insert_datasource_novelty_detector_for_datapoint(obj=datasource_novelty_detector)

def should_datapoint_appear_in_sample(pid, date):
    if not args.is_valid_uuid(pid):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDAIS_IP)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_SDAIS_IDT)
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if datapoint is None:
        raise exceptions.DatapointNotFoundException(error=Errors.E_GPA_SDAIS_DNF)
    if datapoint.did is None:
        raise exceptions.DatapointUnsupportedOperationException(error=Errors.E_GPA_SDAIS_DSNF)
    #obtenemos las caracteristicas de los datasources en los que aparece el datapoint, si no lo calculamos
    ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
    if not ds_nd:
        generate_datasource_novelty_detector_for_datapoint(pid=pid)
        ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=datapoint.did,pid=pid)
        if not ds_nd:
            raise exceptions.DatasourceNoveltyDetectorException(error=Errors.E_GPA_SDAIS_DSNDNF)
    #una vez obtenido, obtenemos el summary de la muestra en cuestion, si no existe la calculamos
    ds_summary=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
    if not ds_summary:
        generate_datasource_text_summary(did=datapoint.did, date=date)
        ds_summary=cassapidatasource.get_datasource_text_summary(did=datapoint.did, date=date)
        if not ds_summary:
            raise exceptions.DatasourceTextSummaryException(error=Errors.E_GPA_SDAIS_DSTSNF)
    #una vez obtenidos ambos, los comparamos y si el resultado es muy diferente devolvemos false. Si el resultado es similar, devolvemos True
    nd=pickle.loads(ds_nd.nd)
    sample_values=[]
    for feature in ds_nd.features:
        sample_values.append(ds_summary.word_frecuency[feature]) if feature in ds_summary.word_frecuency else sample_values.append(0)
    result=svmapi.is_row_novel(novelty_detector=nd, row=sample_values)
    return True if result is not None and result[0]>0 else False

def classify_missing_datapoints_in_sample(did, date):
    if not args.is_valid_uuid(did):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CMDIS_ID)
    if not args.is_valid_date(date):
        raise exceptions.BadParametersException(error=Errors.E_GPA_CMDIS_IDT)
    dsmap=cassapidatasource.get_datasource_map(did=did, date=date)
    if not dsmap:
        raise exceptions.DatasourceMapNotFoundException(error=Errors.E_GPA_CMDIS_DSMNF)
    dshash=cassapidatasource.get_datasource_hash(did=did, date=dsmap.date)
    if not dshash:
        dshash=generate_datasource_hash(did=did, date=dsmap.date)
    text_hash=json.loads(dshash.content)
    variable_list=textmanvar.get_variables_atts(text_hash=text_hash)
    ds_summary=cassapidatasource.get_datasource_text_summary(did=did, date=date)
    if not ds_summary:
        generate_datasource_text_summary(did=did, date=date)
        ds_summary=cassapidatasource.get_datasource_text_summary(did=did, date=date)
        if not ds_summary:
            raise exceptions.DatasourceTextSummaryException(error=Errors.E_GPA_CMDIS_DSTSNF)
    ds_pids=cassapidatapoint.get_datapoints_pids(did=did)
    pids_to_classify=set(ds_pids)-set(dsmap.datapoints.keys())
    response={'doubts':[],'discarded':[]}
    for pid in pids_to_classify:
        ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=did,pid=pid)
        if not ds_nd:
            generate_datasource_novelty_detector_for_datapoint(pid=pid)
            ds_nd=cassapidatasource.get_last_datasource_novelty_detector_for_datapoint(did=did,pid=pid)
            if not ds_nd:
                response['doubts'].append(pid)
                continue
        nd=pickle.loads(ds_nd.nd)
        sample_values=[]
        for feature in ds_nd.features:
            sample_values.append(ds_summary.word_frecuency[feature]) if feature in ds_summary.word_frecuency else sample_values.append(0)
        result=svmapi.is_row_novel(novelty_detector=nd, row=sample_values)
        if result is None or result[0]<0:
            response['discarded'].append(pid)
            continue
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        if not datapoint_stats or not datapoint_stats.dtree_inv:
            response['doubts'].append(pid)
            continue
        dtree_inv=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree_inv)
        doubt=False
        for element in text_hash['elements']:
            if 'type' in element and element['type']=='var' and not element['text_pos'] in dsmap.datapoints.values():
                var_atts=textmanvar.get_variable_atts(text_hash=text_hash, text_pos=element['text_pos'])
                if not dtree_inv.evaluate_row(var_atts):
                    doubt=True
                    break
        response['doubts'].append(pid) if doubt else response['discarded'].append(pid)
    return response

