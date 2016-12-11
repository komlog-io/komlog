'''
This library implements authorization mechanisms to Komlog interfaces and objects


@date: 2013/11/10
@author: jcazor
'''

from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.auth import permissions, exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import permission as cassapiperm
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.model.parametrization import widget as prmwidget

def authorize_get_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGAC_RE)

def authorize_get_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datasource=cassapidatasource.get_datasource(did)
        if datasource and datasource.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
            for share in shares:
                if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGDSC_RE)

def authorize_put_datasource_config(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_APDSC_RE)

def authorize_get_datasource_data(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datasource=cassapidatasource.get_datasource(did)
        if datasource and datasource.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
            for share in shares:
                if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGDSD_RE)

def authorize_post_datasource_data(uid,aid,did):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_ARA_ATDSD_ANF)
    user_datasource_perm=cassapiperm.get_user_datasource_perm(uid=uid,did=did)
    user_agent_perm=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    if (user_datasource_perm and user_agent_perm and
        user_datasource_perm.perm & permissions.CAN_EDIT and
        user_agent_perm.perm & permissions.CAN_EDIT):
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ATDSD_RE)

def authorize_post_datapoint_data(uid,aid,pid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_ARA_ATDPD_ANF)
    user_datapoint_perm=cassapiperm.get_user_datapoint_perm(uid=uid,pid=pid)
    user_agent_perm=cassapiperm.get_user_agent_perm(uid=uid,aid=aid)
    if (user_datapoint_perm and user_agent_perm and
        user_datapoint_perm.perm & permissions.CAN_EDIT and
        user_agent_perm.perm & permissions.CAN_EDIT):
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ATDPD_RE)

def authorize_new_datasource(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_ARA_ANDS_ANF)
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ANDS_RE)

def authorize_get_datapoint_data(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datapoint=cassapidatapoint.get_datapoint(pid)
        if datapoint and datapoint.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
            for share in shares:
                if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGDPD_RE)

def authorize_get_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datapoint=cassapidatapoint.get_datapoint(pid)
        if datapoint and datapoint.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
            for share in shares:
                if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGDPC_RE)

def authorize_put_datapoint_config(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_APDPC_RE)

def authorize_new_datasource_datapoint(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ANDSDP_RE)

def authorize_new_user_datapoint(uid,aid):
    if not args.is_valid_uuid(aid):
        raise exceptions.AuthorizationException(error=Errors.E_ARA_ANUDP_IA)
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ANUDP_RE)

def authorize_put_agent_config(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_APAC_RE)

def authorize_get_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        widget = cassapiwidget.get_widget(wid)
        if widget and widget.uid != uid:
            if widget.type == prmwidget.types.DATASOURCE:
                datasource=cassapidatasource.get_datasource(widget.did)
                if datasource and datasource.uid != uid:
                    shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
                    for share in shares:
                        if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                            return
            elif widget.type == prmwidget.types.DATAPOINT:
                datapoint=cassapidatapoint.get_datapoint(widget.pid)
                if datapoint and datapoint.uid != uid:
                    shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
                    for share in shares:
                        if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                            return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGWC_RE)

def authorize_put_widget_config(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_APWC_RE)

def authorize_get_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGDBC_RE)

def authorize_put_dashboard_config(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_APDBC_RE)

def authorize_mark_positive_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AMPOSV_RE)

def authorize_mark_negative_variable(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AMNEGV_RE)

def authorize_add_widget_to_dashboard(uid,bid,wid):
    dbperm=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    wgperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if dbperm and dbperm.perm & permissions.CAN_EDIT:
        if wgperm and wgperm.perm & permissions.CAN_READ:
            return
        else:
            widget = cassapiwidget.get_widget(wid)
            if widget and widget.uid != uid:
                if widget.type == prmwidget.types.DATASOURCE:
                    datasource=cassapidatasource.get_datasource(widget.did)
                    if datasource and datasource.uid != uid:
                        shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
                        for share in shares:
                            if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                                return
                elif widget.type == prmwidget.types.DATAPOINT:
                    datapoint=cassapidatapoint.get_datapoint(widget.pid)
                    if datapoint and datapoint.uid != uid:
                        shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
                        for share in shares:
                            if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                                return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AAWTDB_RE)

def authorize_delete_widget_from_dashboard(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADWFDB_RE)

def authorize_delete_agent(uid,aid):
    permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
    if not (permission and permission.perm & permissions.CAN_DELETE):
        raise exceptions.AuthorizationException(error=Errors.E_ARA_ADA_RE)

def authorize_delete_datasource(uid,did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADDS_RE)

def authorize_delete_datapoint(uid,pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADDP_RE)

def authorize_delete_widget(uid,wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADW_RE)

def authorize_delete_dashboard(uid,bid):
    permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADDB_RE)

def authorize_add_datapoint_to_widget(uid, pid, wid):
    uwperm=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if uwperm and uwperm.perm & permissions.CAN_EDIT:
        upperm=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
        if upperm and upperm.perm & permissions.CAN_READ:
            return
        else:
            datapoint=cassapidatapoint.get_datapoint(pid)
            if datapoint and datapoint.uid != uid:
                shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
                for share in shares:
                    if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AADPTW_RE)

def authorize_delete_datapoint_from_widget(uid, wid):
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADDPFW_RE)

def authorize_new_snapshot(uid,wid):
    ''' check that user has permission over widget '''
    permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
    if permission and permission.perm & permissions.CAN_SNAPSHOT:
        return
    else:
        widget = cassapiwidget.get_widget(wid)
        if widget and widget.uid != uid:
            if widget.type == prmwidget.types.DATASOURCE:
                datasource=cassapidatasource.get_datasource(widget.did)
                if datasource and datasource.uid != uid:
                    shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
                    for share in shares:
                        if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_SNAPSHOT:
                            return
            elif widget.type == prmwidget.types.DATAPOINT:
                datapoint=cassapidatapoint.get_datapoint(widget.pid)
                if datapoint and datapoint.uid != uid:
                    shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
                    for share in shares:
                        if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_SNAPSHOT:
                            return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ANS_RE)

def authorize_get_snapshot_data(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGSD_RE)

def authorize_get_snapshot_config(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGSC_RE)

def authorize_delete_snapshot(uid,nid):
    permission=cassapiperm.get_user_snapshot_perm(uid=uid,nid=nid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADS_RE)

def authorize_get_circle_config(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGCC_RE)

def authorize_delete_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_DELETE:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADC_RE)

def authorize_update_circle_config(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AUCC_RE)

def authorize_add_member_to_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AAMTC_RE)

def authorize_delete_member_from_circle(uid,cid):
    permission=cassapiperm.get_user_circle_perm(uid=uid,cid=cid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADMFC_RE)

def authorize_dissociate_datapoint_from_datasource(uid, pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_EDIT:
        return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADDPFDS_RE)

def authorize_hook_to_datapoint(uid, pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datapoint=cassapidatapoint.get_datapoint(pid)
        if datapoint and datapoint.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
            for share in shares:
                if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AHTDP_RE)

def authorize_hook_to_datasource(uid, did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datasource=cassapidatasource.get_datasource(did)
        if datasource and datasource.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
            for share in shares:
                if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AHTDS_RE)

def authorize_unhook_from_datapoint(uid, pid):
    permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datapoint=cassapidatapoint.get_datapoint(pid)
        if datapoint and datapoint.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datapoint.uid, dest_uid=uid)
            for share in shares:
                if (datapoint.datapointname+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AUHFDP_RE)

def authorize_unhook_from_datasource(uid, did):
    permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
    if permission and permission.perm & permissions.CAN_READ:
        return
    else:
        datasource=cassapidatasource.get_datasource(did)
        if datasource and datasource.uid != uid:
            shares = cassapiperm.get_user_shared_uris(uid=datasource.uid, dest_uid=uid)
            for share in shares:
                if (datasource.datasourcename+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AUHFDS_RE)

def authorize_get_uri(uid, uri):
    if uri is None or args.is_valid_uri(uri):
        return
    elif args.is_valid_global_uri(uri):
        owner_username,local_uri=uri.split(':')
        owner_uid = cassapiuser.get_uid(username=owner_username)
        if owner_uid:
            shares = cassapiperm.get_user_shared_uris(uid=owner_uid, dest_uid=uid)
            for share in shares:
                if (local_uri+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    else:
        raise exceptions.BadParametersException(error=Errors.E_ARA_AGU_IURI)
    raise exceptions.AuthorizationException(error=Errors.E_ARA_AGU_RE)

def authorize_register_pending_hook(uid, uri):
    if args.is_valid_uri(uri):
        return
    elif args.is_valid_global_uri(uri):
        owner_username,local_uri=uri.split(':')
        owner_uid = cassapiuser.get_uid(username=owner_username)
        if owner_uid:
            shares = cassapiperm.get_user_shared_uris(uid=owner_uid, dest_uid=uid)
            for share in shares:
                if (local_uri+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    else:
        raise exceptions.BadParametersException(error=Errors.E_ARA_ARPH_IURI)
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ARPH_RE)

def authorize_delete_pending_hook(uid, uri):
    if args.is_valid_uri(uri):
        return
    elif args.is_valid_global_uri(uri):
        owner_username,local_uri=uri.split(':')
        owner_uid = cassapiuser.get_uid(username=owner_username)
        if owner_uid:
            shares = cassapiperm.get_user_shared_uris(uid=owner_uid, dest_uid=uid)
            for share in shares:
                if (local_uri+'.').startswith(share.uri+'.') and share.perm & permissions.CAN_READ:
                    return
    else:
        raise exceptions.BadParametersException(error=Errors.E_ARA_ADPH_IURI)
    raise exceptions.AuthorizationException(error=Errors.E_ARA_ADPH_RE)

