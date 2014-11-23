#coding: utf-8
'''

This file defines the logic associated with interface operations received

'''

from komfig import logger
from komlibs.gestaccount.user import api as usrapi
from komlibs.gestaccount.agent import api as agapi
from komlibs.gestaccount.datasource import api as dsapi
from komlibs.gestaccount.datapoint import api as dpapi
from komlibs.gestaccount.widget import api as wgapi
from komlibs.gestaccount.dashboard import api as dbapi
from komlibs.auth import authorization
from komlibs.auth import exceptions as authexcept
from komlibs.gestaccount import exceptions as gestexcept
from komimc import messages
from komimc import api as msgapi
from komlibs.ifaceops import operations


STATUS_OK=200
STATUS_RECEIVED=202
STATUS_ACCESS_DENIED=403
STATUS_BAD_PARAMETERS=400
STATUS_NOT_FOUND=404
STATUS_INTERNAL_ERROR=500

class ExceptionHandler(object):
    def __init__(self, f):
        self.f=f

    def __call__(self, **kwargs):
        try:
            return self.f(**kwargs)
        except authexcept.AuthorizationException:
            return (STATUS_ACCESS_DENIED,{'message':'Access Denied'})
        except gestexcept.BadParametersException:
            return (STATUS_BAD_PARAMETERS,{'message':'Bad Parameters'})
        except gestexcept.UserNotFoundException:
            return (STATUS_NOT_FOUND,{'message':'User not found'})
        except gestexcept.WidgetNotFoundException:
            return (STATUS_NOT_FOUND,{'message':'Widget not found'})
        except gestexcept.DashboardNotFoundException:
            return (STATUS_NOT_FOUND,{'message':'Dashboard not found'})
        except gestexcept.AgentCreationException:
            return (STATUS_INTERNAL_ERROR,{'message':'agent creation exception'})
        except gestexcept.UserConfirmationException:
            return (STATUS_INTERNAL_ERROR,{'message':'user confirmation exception'})
        except gestexcept.DatasourceNotFoundException:
            return (STATUS_NOT_FOUND,{'message':'Datasource not found'})
        except gestexcept.DatapointDataNotFoundException:
            return (STATUS_NOT_FOUND,{'message':'Datapoint not found'})
        except gestexcept.UserAlreadyExistsException:
            return (STATUS_ACCESS_DENIED,{'message':'Access Denied'})
        except Exception as e:
            logger.logger.debug('Exception detected in '+str(self.f.__name__))
            logger.logger.debug(str(e))
            return (STATUS_INTERNAL_ERROR,{'message':'Internal Error'})

@ExceptionHandler
def new_user_operation(username, password, email):
    user=usrapi.create_user(username, password, email)
    if user:
        message=messages.NewUserMessage(uid=user.uid)
        msgapi.send_message(message)
        return (STATUS_OK,str(user.uid))
    else:
        return (STATUS_INTERNAL_ERROR,{'message':'user creation exception'})

@ExceptionHandler
def confirm_user_operation(email, code):
    if usrapi.confirm_user(email, code):
        return (STATUS_OK,{'result':email+' confirmation OK'})
    else:
        return (STATUS_INTERNAL_ERROR,{'result':'confirmation error'})

@ExceptionHandler
def get_user_profile_operation(username):
    data=usrapi.get_user_profile(username)
    return (STATUS_OK,data)

@ExceptionHandler
def new_agent_operation(username, agentname, pubkey, version):
    authorization.authorize_request(request='NewAgentRequest',username=username)
    agent=agapi.create_agent(username, agentname, pubkey, version)
    if agent:
        operation=operations.NewAgentOperation(uid=agent.uid,aid=agent.aid)
        message=messages.UpdateQuotesMessage(operation=operation)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgapi.send_message(message)
        return (STATUS_OK,{'aid':str(agent.aid)})
    else:
        return (STATUS_INTERNAL_ERROR, {'message':'Internal Error'})

@ExceptionHandler
def get_agents_config_operation(username):
    data=agapi.get_agents_config(username=username, dids_flag=True)
    return (STATUS_OK, data)

@ExceptionHandler
def get_agent_config_operation(username, aid):
    authorization.authorize_request(request='GetAgentConfigRequest',username=username,aid=aid)
    data=agapi.get_agent_config(aid,dids_flag=True)
    return (STATUS_OK, data)

@ExceptionHandler
def update_agent_config_operation(username, aid, data):
    authorization.authorize_request('AgentUpdateConfigurationRequest',username, aid=aid)
    if agapi.update_agent_config(username=username, aid=aid, data=data):
        return (STATUS_OK,{'message':'Operation completed'})
    else:
        return (STATUS_INTERNAL_ERROR,{'message':'Interal Error'})

@ExceptionHandler
def get_datasource_data_operation(username, did):
    authorization.authorize_request(request='GetDatasourceDataRequest',username=username,did=did)
    data=dsapi.get_datasource_data(did)
    return (STATUS_OK, data)

@ExceptionHandler
def upload_datasource_data_operation(username, aid, did, content, destination):
    authorization.authorize_request(request='PostDatasourceDataRequest',username=username,aid=aid,did=did)
    destfile=dsapi.upload_content(did,content,dest_dir)
    return (STATUS_RECEIVED, {'message':'Data received'})

@ExceptionHandler
def get_datasource_config_operation(username, did):
    authorization.authorize_request(request='GetDatasourceConfigRequest',username=username,did=did)
    data=dsapi.get_datasource_config(did)
    return (STATUS_OK, data)

@ExceptionHandler
def update_datasource_config_operation(username, did, content):
    authorization.authorize_request(request='DatasourceUpdateConfigurationRequest',username=username,did=did)
    dsapi.update_datasourceconfig(did=did,data=content)
    return (STATUS_OK,{'message':'Operation completed'})

@ExceptionHandler
def new_datasource_operation(username, aid, datasourcename):
    authorization.authorize_request('NewDatasourceRequest',username,aid=aid)
    datasource=dsapi.create_datasource(username=username,aid=aid,datasourcename=datasourcename)
    if datasource:
        widget=wgapi.new_widget_ds(username=username, did=datasource.did)
        if widget:
            operation=operations.NewWidgetOperation(uid=user.uid,wid=wid)
            message=messages.UpdateQuotesMessage(operation=operation)
            msgapi.send_message(message)
            message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            msgapi.send_message(message)
        operation=operations.NewDatasourceOperation(uid=user.uid,aid=aid,did=did)
        message=messages.UpdateQuotesMessage(operation=operation)
        msgapi.send_message(message)
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        msgapi.send_message(message)
        return (STATUS_OK, {'did':str(datasource.did)})
    else:
        return (STATUS_INTERNAL_ERROR, {'message':'Internal Error'})

@ExceptionHandler
def get_datasources_config_operation(username):
    data=dsapi.get_datasources_config(username=username)
    return (STATUS_OK, data)

@ExceptionHandler
def get_datapoint_data_operation(username, pid, start_date, end_date):
    authorization.authorize_request(request='GetDatapointDataRequest',username=username,pid=pid)
    data=dpapi.get_datapoint_data(pid, end_date=end_date, start_date=start_date)
    return (STATUS_OK, data)

@ExceptionHandler
def get_datapoint_config_operation(username, pid):
    authorization.authorize_request(request='GetDatapointConfigRequest',username=username,pid=pid)
    data=dpapi.get_datapoint_config(pid)
    return (STATUS_OK, data)

@ExceptionHandler
def update_datapoint_config_operation(username, pid, data):
    authorization.authorize_request(request='DatapointUpdateConfigurationRequest',username=username,pid=pid)
    dpapi.update_datapointconfig(pid=pid,data=data)
    return (STATUS_OK,{'message':'Operation completed'})

@ExceptionHandler
def new_datapoint_operation(username, did, datasourcedate,position, length, datapointname):
    authorization.authorize_request(request='NewDatapointRequest',username=username,did=did)
    message=messages.MonitorVariableMessage(did=did,date=datasourcedate,pos=position,length=length,name=datapointname)
    msgapi.send_message(message)
    return (STATUS_RECEIVED, {'message':'Request received'})

@ExceptionHandler
def get_user_config_operation(username):
    user=usrapi.get_user(username=username)
    data=agapi.get_agents_config(username=username, dids_flag=True)
    return (STATUS_OK, data)

@ExceptionHandler
def get_widgets_config_operation(username):
    data=wgapi.get_widgets_config(username=username)
    return (STATUS_OK, data)

@ExceptionHandler
def get_widget_config_operation(username, wid):
    authorization.authorize_request(request='GetWidgetConfigRequest',username=username,wid=wid)
    data=wgapi.get_widget_config(wid=wid)
    return (STATUS_OK, data)

@ExceptionHandler
def get_dashboards_config_operation(username):
    data=dbapi.get_dashboards_config(username=username)
    return (STATUS_OK, data)

@ExceptionHandler
def get_dashboard_config_operation(username, bid):
    authorization.authorize_request(request='GetDashboardConfigRequest',username=username,bid=bid)
    data=dbapi.get_dashboard_config(bid=bid)
    return (STATUS_OK, data)

@ExceptionHandler
def update_user_config_operation(username, data):
    authorization.authorize_request('UserUpdateProfileRequest',self.user)
    if usrapi.update_user_profile(username=username, data=data):
        return (STATUS_OK,{'message':'Operation completed'})
    else:
        return (STATUS_INTERNAL_ERROR,{'message':'Interal Error'})

@ExceptionHandler
def login_operation(username, password, agentid, signature):
    if not usrapi.auth_user(username=username, password=password):
        return (STATUS_ACCESS_DENIED, {'message':'Access denied'})
    if agentid:
        if not agapi.auth_agent(agentid=agentid, signature=signature):
            return (STATUS_ACCESS_DENIED, {'message':'Access denied'})
    return (STATUS_OK,{'message':'Authentication OK'})

