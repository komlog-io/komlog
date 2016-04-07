
'''
This library implements authorization mechanisms based on user quotas


@author: jcazor
@date: 2013/12/08
'''

from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import interface as cassapiiface
from komlog.komlibs.auth import exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.quotes import deny
from komlog.komlibs.general.validation import arguments as args


def authorize_new_agent(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_AgentCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANA_QE)

def authorize_new_datasource(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDS_IA)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatasourceCreation'])
    interfaces.append(deny.interfaces['Agent_DatasourceCreation']+aid.hex)
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDS_QE)

def authorize_new_datapoint(uid,did):
    datasource=cassapidatasource.get_datasource(did=did)
    if not datasource:
        raise exceptions.DatasourceNotFoundException(error=Errors.E_AQA_ANDP_DSNF)
    interfaces=[]
    interfaces.append(deny.interfaces['User_DatapointCreation'])
    interfaces.append(deny.interfaces['Agent_DatapointCreation']+datasource.aid.hex)
    interfaces.append(deny.interfaces['Datasource_DatapointCreation']+did.hex)
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDP_QE)

def authorize_new_widget(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_WidgetCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANW_QE)

def authorize_new_dashboard(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_DashboardCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANDB_QE)

def authorize_new_snapshot(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_SnapshotCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANS_QE)

def authorize_new_circle(uid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_CircleCreation'])
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_ANC_QE)

def authorize_add_member_to_circle(uid, cid):
    interfaces=[]
    interfaces.append(deny.interfaces['User_AddMemberToCircle']+cid.hex)
    for iface in interfaces:
        if cassapiiface.get_user_iface_deny(uid=uid, iface=iface):
            raise exceptions.AuthorizationException(error=Errors.E_AQA_AAMTC_QE)

