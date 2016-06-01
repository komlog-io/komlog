
'''
This library implements authorization mechanisms based on user quotas


@author: jcazor
@date: 2013/12/08
'''

import uuid
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import interface as cassapiiface
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid


def authorize_new_agent(uid):
    ifaces=[]
    ifaces.append(interfaces.User_AgentCreation().value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANA_QE)

def authorize_new_datasource(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDS_IA)
    ifaces=[]
    ifaces.append(interfaces.User_DatasourceCreation().value)
    ifaces.append(interfaces.Agent_DatasourceCreation(aid).value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDS_QE)

def authorize_new_datasource_datapoint(uid,did):
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQA_ANDSDP_DSNF)
    ifaces=[]
    ifaces.append(interfaces.User_DatapointCreation().value)
    ifaces.append(interfaces.Agent_DatapointCreation(datasource.aid).value)
    ifaces.append(interfaces.Datasource_DatapointCreation(did).value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDSDP_QE)

def authorize_new_user_datapoint(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_AQA_ANUDP_IA)
    ifaces=[]
    ifaces.append(interfaces.User_DatapointCreation().value)
    ifaces.append(interfaces.Agent_DatapointCreation(aid).value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANUDP_QE)

def authorize_new_widget(uid):
    ifaces=[]
    ifaces.append(interfaces.User_WidgetCreation().value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANW_QE)

def authorize_new_dashboard(uid):
    ifaces=[]
    ifaces.append(interfaces.User_DashboardCreation().value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDB_QE)

def authorize_new_snapshot(uid):
    ifaces=[]
    ifaces.append(interfaces.User_SnapshotCreation().value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANS_QE)

def authorize_new_circle(uid):
    ifaces=[]
    ifaces.append(interfaces.User_CircleCreation().value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANC_QE)

def authorize_add_member_to_circle(uid, cid):
    ifaces=[]
    ifaces.append(interfaces.User_AddMemberToCircle(cid).value)
    for iface in ifaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_AAMTC_QE)

def authorize_post_datasource_data(uid, did):
    ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
    ifaces=[]
    ifaces.append(interfaces.User_PostDatasourceDataDaily().value)
    ifaces.append(interfaces.User_PostDatasourceDataDaily(did).value)
    for iface in ifaces:
        if cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_APDSD_QE)

def authorize_post_datapoint_data(uid, pid):
    ts=timeuuid.get_day_timestamp(timeuuid.uuid1())
    ifaces=[]
    ifaces.append(interfaces.User_PostDatapointDataDaily().value)
    ifaces.append(interfaces.User_PostDatapointDataDaily(pid).value)
    for iface in ifaces:
        if cassapiiface.get_user_ts_iface_deny(uid=uid, iface=iface, ts=ts):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_APDPD_QE)

def authorize_get_datasource_data(did, ii, ie):
    ''' This method checks wether the DataRetrievalMinTimestamp interface is set.
        If it is set, and ii and ie are not informed, or they are less than the value set,
        then raise an exception indicating that some limitations apply in the request.
        The datasource propietary user sets the limitation, so we use the datasource uid
        instead of the request uid.
    '''
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource or not datasource.uid:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQA_AGDSD_DSNF)
    iface=interfaces.User_DataRetrievalMinTimestamp().value
    db_iface=cassapiiface.get_user_iface_deny(uid=datasource.uid, iface=iface)
    if db_iface:
        min_date=uuid.UUID(db_iface.perm)
        if ii and ie and ii.time >= min_date.time and ie.time >= min_date.time:
            pass
        else:
            raise exceptions.IntervalBoundsException(data={'date':min_date}, error=Errors.E_AQA_AGDSD_IBE)

def authorize_get_datapoint_data(pid, ii, ie):
    ''' This method checks wether the DataRetrievalMinTimestamp interface is set.
        If it is set, and ii and ie are not informed, or they are less than the value set,
        then raise an exception indicating that some limitations apply in the request.
        The datapoint propietary user sets the limitation, so we use the datapoint uid
        instead of the request uid.
    '''
    datapoint=cassapidatapoint.get_datapoint(pid=pid)
    if not datapoint:
        raise exceptions.DatapointNotFoundException(error=Errors.E_AQA_AGDPD_DPNF)
    iface=interfaces.User_DataRetrievalMinTimestamp().value
    db_iface=cassapiiface.get_user_iface_deny(uid=datapoint.uid, iface=iface)
    if db_iface:
        min_date=uuid.UUID(db_iface.perm)
        if ii and ie and ii.time >= min_date.time and ie.time >= min_date.time:
            pass
        else:
            raise exceptions.IntervalBoundsException(data={'date':min_date}, error=Errors.E_AQA_AGDPD_IBE)

