#coding: utf-8
'''
This file is the entry point of authorization mechanisms

@author: jcazor
@date: 2013/12/08

'''

import sys
from komlibs.auth.quotes import authorization as quoauth
from komlibs.auth.resources import authorization as resauth
from komlibs.auth.shared import authorization as sharedauth
from komlibs.auth import exceptions as authexcept
from komlibs.auth import requests, errors
from komcass.api import user as cassapiuser
from komfig import logger

func_requests={
               requests.NEW_AGENT:'authorize_new_agent_creation',
               requests.GET_AGENT_CONFIG:'authorize_get_agent_config',
               requests.UPDATE_AGENT_CONFIG:'authorize_agent_update_configuration',
               requests.DELETE_AGENT:'authorize_delete_agent',
               requests.NEW_DATASOURCE:'authorize_new_datasource_creation',
               requests.POST_DATASOURCE_DATA:'authorize_post_datasource_data',
               requests.GET_DATASOURCE_DATA:'authorize_get_datasource_data',
               requests.GET_DATASOURCE_CONFIG:'authorize_get_datasource_config',
               requests.UPDATE_DATASOURCE_CONFIG:'authorize_datasource_update_configuration',
               requests.DELETE_DATASOURCE:'authorize_delete_datasource',
               requests.NEW_DATAPOINT:'authorize_new_datapoint_creation',
               requests.GET_DATAPOINT_DATA:'authorize_get_datapoint_data',
               requests.GET_DATAPOINT_CONFIG:'authorize_get_datapoint_config',
               requests.UPDATE_DATAPOINT_CONFIG:'authorize_datapoint_update_configuration',
               requests.MARK_POSITIVE_VARIABLE:'authorize_mark_positive_variable',
               requests.MARK_NEGATIVE_VARIABLE:'authorize_mark_negative_variable',
               requests.DELETE_DATAPOINT:'authorize_delete_datapoint',
               requests.NEW_WIDGET:'authorize_new_widget_creation',
               requests.GET_WIDGET_CONFIG:'authorize_get_widget_config',
               requests.UPDATE_WIDGET_CONFIG:'authorize_widget_update_configuration',
               requests.DELETE_WIDGET:'authorize_delete_widget',
               requests.ADD_DATAPOINT_TO_WIDGET:'authorize_add_datapoint_to_widget',
               requests.DELETE_DATAPOINT_FROM_WIDGET:'authorize_delete_datapoint_from_widget',
               requests.NEW_DASHBOARD:'authorize_new_dashboard_creation',
               requests.GET_DASHBOARD_CONFIG:'authorize_get_dashboard_config',
               requests.UPDATE_DASHBOARD_CONFIG:'authorize_dashboard_update_configuration',
               requests.ADD_WIDGET_TO_DASHBOARD:'authorize_add_widget_to_dashboard',
               requests.DELETE_WIDGET_FROM_DASHBOARD:'authorize_delete_widget_from_dashboard',
               requests.DELETE_DASHBOARD:'authorize_delete_dashboard',
               requests.NEW_SNAPSHOT:'authorize_new_snapshot_creation',
               requests.GET_SNAPSHOT_DATA:'authorize_get_snapshot_data',
               requests.GET_SNAPSHOT_CONFIG:'authorize_get_snapshot_config',
               requests.DELETE_SNAPSHOT:'authorize_delete_snapshot',
               requests.NEW_CIRCLE:'authorize_new_circle_creation',
               requests.GET_CIRCLE_CONFIG:'authorize_get_circle_config',
               requests.UPDATE_CIRCLE_CONFIG:'authorize_update_circle_config',
               requests.DELETE_CIRCLE:'authorize_delete_circle',
               requests.ADD_MEMBER_TO_CIRCLE:'authorize_add_member_to_circle',
               requests.DELETE_MEMBER_FROM_CIRCLE:'authorize_delete_member_from_circle',
               }

def authorize_request(request,username,aid=None,did=None,pid=None,gid=None,wid=None,bid=None,nid=None,cid=None,ii=None,ie=None):
    user=cassapiuser.get_user(username=username)
    if not user:
        raise authexcept.UserNotFoundException(error=errors.E_AA_AR_UNF)
    params={'aid':aid,'did':did,'uid':user.uid,'pid':pid,'wid':wid,'bid':bid,'nid':nid,'cid':cid,'ii':ii,'ie':ie}
    try:
        getattr(sys.modules[__name__],func_requests[request])(params)
    except KeyError as e:
        logger.logger.error('REQUEST NOT FOUND: '+str(request))
        logger.logger.debug(str(e))
        raise authexcept.RequestNotFoundException(error=errors.E_AA_AR_RNF)

def authorize_new_agent_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_agent(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANAC_QE)
    if not resauth.authorize_new_agent(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANAC_RE)

def authorize_get_agent_config(params):
    uid=params['uid']
    aid=params['aid']
    if not quoauth.authorize_get_agent_config(uid=uid,aid=aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGAC_QE)
    if not resauth.authorize_get_agent_config(uid=uid,aid=aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGAC_RE)

def authorize_get_datasource_data(params):
    uid=params['uid']
    did=params['did']
    ii=params['ii']
    ie=params['ie']
    if not quoauth.authorize_get_datasource_data(uid=uid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDSD_QE)
    if not resauth.authorize_get_datasource_data(uid=uid,did=did):
        if ii and ie:
            if not sharedauth.authorize_get_datasource_data(uid=uid, did=did, ii=ii, ie=ie):
                raise authexcept.AuthorizationException(error=errors.E_AA_AGDSD_SE)
        else:
            raise authexcept.AuthorizationException(error=errors.E_AA_AGDSD_RE)

def authorize_post_datasource_data(params):
    uid=params['uid']
    did=params['did']
    aid=params['aid']
    if not quoauth.authorize_post_datasource_data(uid=uid,aid=aid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_APDSD_QE)
    if not resauth.authorize_post_datasource_data(uid=uid,aid=aid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_APDSD_RE)

def authorize_get_datasource_config(params):
    uid=params['uid']
    did=params['did']
    if not quoauth.authorize_get_datasource_config(uid=uid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDSC_QE)
    if not (resauth.authorize_get_datasource_config(uid=uid,did=did)\
        or sharedauth.authorize_get_datasource_config(uid=uid, did=did)):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDSC_RE)

def authorize_datasource_update_configuration(params):
    uid=params['uid']
    did=params['did']
    if not resauth.authorize_put_datasource_config(uid=uid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADSUC_RE)

def authorize_new_datasource_creation(params):
    uid=params['uid']
    aid=params['aid']
    if not quoauth.authorize_new_datasource(uid=uid,aid=aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDSC_QE)
    if not resauth.authorize_new_datasource(uid=uid,aid=aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDSC_RE)

def authorize_get_datapoint_data(params):
    uid=params['uid']
    pid=params['pid']
    ii=params['ii']
    ie=params['ie']
    if not quoauth.authorize_get_datapoint_data(uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDPD_QE)
    if not resauth.authorize_get_datapoint_data(uid,pid=pid):
        if ii and ie:
            if not sharedauth.authorize_get_datapoint_data(uid=uid, pid=pid, ii=ii, ie=ie):
                raise authexcept.AuthorizationException(error=errors.E_AA_AGDPD_SE)
        else:
            raise authexcept.AuthorizationException(error=errors.E_AA_AGDPD_RE)

def authorize_get_datapoint_config(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_get_datapoint_config(uid=uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDPC_QE)
    if not (resauth.authorize_get_datapoint_config(uid=uid,pid=pid)\
        or sharedauth.authorize_get_datapoint_config(uid=uid, pid=pid)):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDPC_RE)

def authorize_new_datapoint_creation(params):
    uid=params['uid']
    did=params['did']
    if not quoauth.authorize_new_datapoint(uid=uid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDPC_QE)
    if not resauth.authorize_new_datapoint(uid=uid,did=did):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDPC_RE)

def authorize_datapoint_update_configuration(params):
    uid=params['uid']
    pid=params['pid']
    if not resauth.authorize_put_datapoint_config(uid=uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADPUC_RE)

def authorize_uid_update_configuration(params):
    #If uid authentication was successfull, authorization to its own uid config is granted
    pass

def authorize_uid_update_profile(params):
    #If uid authentication was successfull, authorization to its own uid profile is granted
    pass

def authorize_agent_update_configuration(params):
    uid=params['uid']
    aid=params['aid']
    if not resauth.authorize_put_agent_config(uid=uid,aid=aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AAGUC_RE)

def authorize_get_widget_config(params):
    uid=params['uid']
    wid=params['wid']
    if not quoauth.authorize_get_widget_config(uid=uid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGWC_QE)
    if not resauth.authorize_get_widget_config(uid=uid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGWC_RE)

def authorize_widget_update_configuration(params):
    uid=params['uid']
    wid=params['wid']
    if not resauth.authorize_put_widget_config(uid=uid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AWUC_RE)

def authorize_new_widget_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_widget(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANWC_QE)
    if not resauth.authorize_new_widget(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANWC_RE)

def authorize_get_dashboard_config(params):
    uid=params['uid']
    bid=params['bid']
    if not quoauth.authorize_get_dashboard_config(uid=uid,bid=bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDBC_QE)
    if not resauth.authorize_get_dashboard_config(uid=uid,bid=bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGDBC_RE)

def authorize_dashboard_update_configuration(params):
    uid=params['uid']
    bid=params['bid']
    if not resauth.authorize_put_dashboard_config(uid=uid,bid=bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADBUC_RE)

def authorize_new_dashboard_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_dashboard(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDBC_QE)
    if not resauth.authorize_new_dashboard(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANDBC_RE)

def authorize_mark_positive_variable(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_mark_positive_variable(uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AMPV_QE)
    if not resauth.authorize_mark_positive_variable(uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AMPV_RE)

def authorize_mark_negative_variable(params):
    uid=params['uid']
    pid=params['pid']
    if not quoauth.authorize_mark_negative_variable(uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AMNV_QE)
    if not resauth.authorize_mark_negative_variable(uid,pid=pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AMNV_RE)

def authorize_add_widget_to_dashboard(params):
    uid=params['uid']
    bid=params['bid']
    wid=params['wid']
    if not quoauth.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AAWTDB_QE)
    if not resauth.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AAWTDB_RE)

def authorize_delete_widget_from_dashboard(params):
    uid=params['uid']
    bid=params['bid']
    if not quoauth.authorize_delete_widget_from_dashboard(uid=uid,bid=bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADWFDB_QE)
    if not resauth.authorize_delete_widget_from_dashboard(uid=uid,bid=bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADWFDB_RE)

def authorize_delete_agent(params):
    uid=params['uid']
    aid=params['aid']
    if not resauth.authorize_delete_agent(uid,aid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADAG_RE)

def authorize_delete_datasource(params):
    uid=params['uid']
    did=params['did']
    if not resauth.authorize_delete_datasource(uid,did):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADDS_RE)

def authorize_delete_datapoint(params):
    uid=params['uid']
    pid=params['pid']
    if not resauth.authorize_delete_datapoint(uid,pid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADDP_RE)

def authorize_delete_widget(params):
    uid=params['uid']
    wid=params['wid']
    if not resauth.authorize_delete_widget(uid,wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADW_RE)

def authorize_delete_dashboard(params):
    uid=params['uid']
    bid=params['bid']
    if not resauth.authorize_delete_dashboard(uid,bid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADDB_RE)

def authorize_add_datapoint_to_widget(params):
    uid=params['uid']
    pid=params['pid']
    wid=params['wid']
    if not quoauth.authorize_add_datapoint_to_widget(uid=uid, pid=pid, wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AADPTW_QE)
    if not resauth.authorize_add_datapoint_to_widget(uid=uid, pid=pid, wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AADPTW_RE)

def authorize_delete_datapoint_from_widget(params):
    uid=params['uid']
    wid=params['wid']
    if not quoauth.authorize_delete_datapoint_from_widget(uid=uid, wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADDPFW_QE)
    if not resauth.authorize_delete_datapoint_from_widget(uid=uid, wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADDPFW_RE)

def authorize_new_snapshot_creation(params):
    uid=params['uid']
    wid=params['wid']
    if not quoauth.authorize_new_snapshot(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANSCR_QE)
    if not resauth.authorize_new_snapshot(uid=uid,wid=wid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANSCR_RE)

def authorize_get_snapshot_data(params):
    uid=params['uid']
    nid=params['nid']
    if not quoauth.authorize_get_snapshot_data(uid,nid=nid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGSD_QE)
    if not resauth.authorize_get_snapshot_data(uid,nid=nid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGSD_RE)

def authorize_get_snapshot_config(params):
    uid=params['uid']
    nid=params['nid']
    if not quoauth.authorize_get_snapshot_config(uid=uid,nid=nid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGSC_QE)
    if not (resauth.authorize_get_snapshot_config(uid=uid,nid=nid)\
        or sharedauth.authorize_get_snapshot_config(uid=uid, nid=nid)):
        raise authexcept.AuthorizationException(error=errors.E_AA_AGSC_RE)

def authorize_delete_snapshot(params):
    uid=params['uid']
    nid=params['nid']
    if not resauth.authorize_delete_snapshot(uid,nid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADS_RE)

def authorize_new_circle_creation(params):
    uid=params['uid']
    if not quoauth.authorize_new_circle(uid=uid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ANCCR_QE)

def authorize_get_circle_config(params):
    uid=params['uid']
    cid=params['cid']
    if not resauth.authorize_get_circle_config(uid=uid,cid=cid):
            raise authexcept.AuthorizationException(error=errors.E_AA_AGCC_RE)

def authorize_update_circle_config(params):
    uid=params['uid']
    cid=params['cid']
    if not resauth.authorize_update_circle_config(uid=uid,cid=cid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AUCC_RE)

def authorize_delete_circle(params):
    uid=params['uid']
    cid=params['cid']
    if not resauth.authorize_delete_circle(uid,cid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADCR_RE)

def authorize_add_member_to_circle(params):
    uid=params['uid']
    cid=params['cid']
    if not quoauth.authorize_add_member_to_circle(uid=uid, cid=cid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AAMTC_QE)
    if not resauth.authorize_add_member_to_circle(uid=uid, cid=cid):
        raise authexcept.AuthorizationException(error=errors.E_AA_AAMTC_RE)

def authorize_delete_member_from_circle(params):
    uid=params['uid']
    cid=params['cid']
    if not resauth.authorize_delete_member_from_circle(uid=uid, cid=cid):
        raise authexcept.AuthorizationException(error=errors.E_AA_ADMFC_RE)

