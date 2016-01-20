'''

Gestconsole message definitions 

'''

from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.events.model import types as eventstypes
from komlibs.gestaccount.common import delete as deleteapi
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.dashboard import api as dashboardapi
from komlibs.gestaccount.widget import types as widgettypes
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions
from komlibs.mail import api as mailapi
from komlibs.interface.web.operations import weboperations


@exceptions.ExceptionHandler
def process_message_MONVAR(message):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Comprobamos que la variable no pertenezca a un datapoint existente
    - Registramos el nuevo datapoint, marcando la variable como muestra positiva
    - creamos el widget dp
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uid=message.uid
    did=message.did
    date=message.date
    position=message.position
    length=message.length
    datapointname=message.datapointname
    if args.is_valid_uuid(uid) and args.is_valid_uuid(did) and args.is_valid_date(date) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_datapointname(datapointname):
        datapoint=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        if datapoint:
            datasource=datasourceapi.get_datasource_config(did=did)
            operation=weboperations.NewDatapointOperation(uid=datasource['uid'],aid=datasource['aid'],did=did,pid=datapoint['pid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
            response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
            response.add_msg_originated(messages.FillDatapointMessage(pid=datapoint['pid'],date=date))
            response.add_msg_originated(messages.NewDPWidgetMessage(uid=uid,pid=datapoint['pid']))
            response.add_msg_originated(messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATAPOINT, parameters={'pid':datapoint['pid'].hex}))
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.error('Error registering datapoint in database. did: '+did.hex+' date: '+date.hex+' position: '+str(position)+' length: '+str(length))
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_NEGVAR(message):
    ''' Los pasos son los siguientes:
    - marcamos la variable como negativa
    - si se marca correctamente, solicitamos la regeneracion del arbol de decision con el mensaje GDTREE, si no devolvemos error.
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    date=message.date
    position=message.position
    length=message.length
    pid=message.pid
    if args.is_valid_date(date) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_uuid(pid):
        if datapointapi.mark_negative_variable(pid=pid, date=date, position=position, length=length):
            #el dtrea lo genera la propia funcion, solo hay que pedir que vuelvan a almacenar los valores de la variable 
            newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
            response.add_msg_originated(newmsg)
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_POSVAR(message):
    ''' Los pasos son los siguientes:
    - marcamos la variable como positiva
    - si se ejecuta correctamente mandamos un mensaje GDTREE para que se vuelva a general el arbol de decision
    - ademas hay que mirar si algun otro datapoint matcheo esta variable, para solicitar un NEGVAR sobre ellos
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    date=message.date
    position=message.position
    length=message.length
    pid=message.pid
    if args.is_valid_date(date) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_uuid(pid):
        if datapointapi.mark_positive_variable(date=date, position=position, length=length, pid=pid):
            #el dtrea lo genera la propia funcion, solo hay que pedir que vuelvan a almacenar los valores de la variable 
            newmsg=messages.GenerateDTreeMessage(pid=pid,date=date)
            response.add_msg_originated(newmsg)
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_NEWUSR(message):
    ''' Los pasos son los siguientes:
    - Obtenemos la informacion necesaria del mensaje
    - llamamos a la api de mail para enviar el email de bienvenida
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    usermail=message.email
    code=message.code
    if args.is_valid_email(usermail) and args.is_valid_code(code):
        if mailapi.send_welcome_mail(usermail=usermail, code=code):
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.error('Error sending new user welcome mail to: '+usermail)
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            response.error=999999
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_NEWINV(message):
    ''' Los pasos son los siguientes:
    - Obtenemos la informacion necesaria del mensaje
    - llamamos a la api de mail para enviar el email con la invitacion
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    email=message.email
    inv_id=message.inv_id
    if args.is_valid_email(email) and args.is_valid_uuid(inv_id):
        if mailapi.send_invitation_mail(to=email, inv_id=inv_id):
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.error('Error sending invitation mail to: '+email)
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            response.error=999999
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_FORGETMAIL(message):
    ''' Los pasos son los siguientes:
    - Obtenemos la informacion necesaria del mensaje
    - llamamos a la api de mail para enviar el email para el restablecimiento de la password
    '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    email=message.email
    code=message.code
    if args.is_valid_email(email) and args.is_valid_uuid(code):
        if mailapi.send_forget_mail(to=email, code=code):
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.error('Error sending forget mail to: '+email)
            response.status=status.IMC_STATUS_INTERNAL_ERROR
            response.error=999999
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_NEWDSW(message):
    ''' this message creates a new DS_WIDGET associated to a did and uid '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    uid=message.uid
    if args.is_valid_uuid(did) and args.is_valid_uuid(uid):
        widget=widgetapi.new_widget_datasource(uid=uid, did=did)
        if widget:
            operation=weboperations.NewWidgetSystemOperation(uid=widget['uid'],wid=widget['wid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
            response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_NEWDPW(message):
    ''' this message creates a new DP_WIDGET associated to a pid and uid '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    uid=message.uid
    if args.is_valid_uuid(pid) and args.is_valid_uuid(uid):
        widget=widgetapi.new_widget_datapoint(uid=uid, pid=pid)
        if widget:
            operation=weboperations.NewWidgetSystemOperation(uid=widget['uid'],wid=widget['wid'])
            auth_op=operation.get_auth_operation()
            params=operation.get_params()
            response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
            response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELUSER(message):
    ''' this message deletes a user from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    username=message.username
    if args.is_valid_username(username):
        user=userapi.get_user_config(username=username)
        agents=agentapi.get_agents_config(username=username)
        deleteapi.delete_user(username=username)
        #operation=weboperations.DeleteUserOperation(uid=user['uid'],aids=[agent['aid'] for agent in agents])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELAGENT(message):
    ''' this message deletes an agent from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    aid=message.aid
    if args.is_valid_uuid(aid):
        agent=agentapi.get_agent_config(aid=aid, dids_flag=True)
        deleteapi.delete_agent(aid=agent['aid'])
        #operation=weboperations.DeleteAgentOperation(aid=aid,uid=agent['uid'])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELDS(message):
    ''' this message deletes a datasource from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    if args.is_valid_uuid(did):
        datasource=datasourceapi.get_datasource_config(did=did)
        deleteapi.delete_datasource(did=did)
        #operation=weboperations.DeleteDatasourceOperation(did=did,aid=datasource['aid'],uid=datasource['uid'],pids=datasource['pids'])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELDP(message):
    ''' this message deletes a datapoint from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    if args.is_valid_uuid(pid):
        datapoint=datapointapi.get_datapoint_config(pid=pid)
        datasource=datasourceapi.get_datasource_config(did=datapoint['did'])
        deleteapi.delete_datapoint(pid=pid)
        #operation=weboperations.DeleteDatapointOperation(pid=pid,aid=datasource['aid'],uid=datasource['uid'])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELWIDGET(message):
    ''' this message deletes a widget from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    wid=message.wid
    if args.is_valid_uuid(wid):
        widget=widgetapi.get_widget_config(wid=wid)
        deleteapi.delete_widget(wid=wid)
        #operation=weboperations.DeleteWidgetOperation(wid=wid,uid=widget['uid'])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELDASHB(message):
    ''' this message deletes a dashboard from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    bid=message.bid
    if args.is_valid_uuid(bid):
        dashboard=dashboardapi.get_dashboard_config(bid=bid)
        deleteapi.delete_dashboard(bid=bid)
        #operation=weboperations.DeleteDashboardOperation(bid=bid,uid=dashboard['uid'])
        #auth_op=operation.get_auth_operation()
        #params=operation.get_params()
        #response.add_msg_originated(messages.UpdateQuotesMessage(operation=auth_op, params=params))
        #response.add_msg_originated(messages.ResourceAuthorizationUpdateMessage(operation=auth_op, params=params))
        response.status=status.IMC_STATUS_OK
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

