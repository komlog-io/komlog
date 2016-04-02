'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.auth import permissions, exceptions, errors
from komlog.komcass.api import permission as cassapiperm

def authorize_get_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGAC_RE)

def authorize_get_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGDSC_RE)

def authorize_put_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_APDSC_RE)

def authorize_get_datasource_data(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGDSD_RE)

def authorize_post_datasource_data(uid,aid,did):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=errors.E_ARA_ATDSD_ANF)
    user_datasource_perm=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    user_agent_perm=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    if (user_datasource_perm and user_agent_perm and
        user_datasource_perm.perm & permissions.CAN_EDIT and
        user_agent_perm.perm & permissions.CAN_EDIT):
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ATDSD_RE)

def authorize_new_datasource(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=errors.E_ARA_ANDS_ANF)
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ANDS_RE)

def authorize_get_datapoint_data(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGDPD_RE)

def authorize_get_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGDPC_RE)

def authorize_put_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_APDPC_RE)

def authorize_new_datapoint(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ANDP_RE)

def authorize_put_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_APAC_RE)

def authorize_get_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGWC_RE)

def authorize_put_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_APWC_RE)

def authorize_get_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGDBC_RE)

def authorize_put_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_APDBC_RE)

def authorize_mark_positive_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AMPOSV_RE)

def authorize_mark_negative_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AMNEGV_RE)

def authorize_add_widget_to_dashboard(uid,bid,wid):
    dbperm=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    wgperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if (dbperm and dbperm.perm & permissions.CAN_EDIT and
        wgperm and wgperm.perm & permissions.CAN_READ):
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AAWTDB_RE)

def authorize_delete_widget_from_dashboard(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADWFDB_RE)

def authorize_delete_agent(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if not (permission and permission.perm & permissions.CAN_DELETE):
        raise exceptions.AuthorizationException(error=errors.E_ARA_ADA_RE)

def authorize_delete_datasource(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADDS_RE)

def authorize_delete_datapoint(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADDP_RE)

def authorize_delete_widget(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADW_RE)

def authorize_delete_dashboard(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADDB_RE)

def authorize_add_datapoint_to_widget(uid, pid, wid):
    uwperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    upperm=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if (uwperm and uwperm.perm & permissions.CAN_EDIT and
        upperm and upperm.perm & permissions.CAN_READ):
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AADPTW_RE)

def authorize_delete_datapoint_from_widget(uid, wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADDPFW_RE)

def authorize_new_snapshot(uid,wid):
    ''' check that user has permission over widget '''
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_SNAPSHOT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ANS_RE)

def authorize_get_snapshot_data(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGSD_RE)

def authorize_get_snapshot_config(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGSC_RE)

def authorize_delete_snapshot(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADS_RE)

def authorize_get_circle_config(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AGCC_RE)

def authorize_delete_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADC_RE)

def authorize_update_circle_config(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AUCC_RE)

def authorize_add_member_to_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_AAMTC_RE)

def authorize_delete_member_from_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=errors.E_ARA_ADMFC_RE)

