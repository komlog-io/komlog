'''

Gestconsole message definitions 

'''

from komlog.komfig import logging
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount.widget import types as widgettypes
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.web.model import operation
from komlog.komlibs.mail import api as mailapi


@exceptions.ExceptionHandler
def process_message_MONVAR(message):
    ''' Los pasos son los siguientes:
    - Comprobamos que la variable exista en el sample (ds en un dtdo momento)
    - Comprobamos que la variable no pertenezca a un datapoint existente
    - Registramos el nuevo datapoint, marcando la variable como muestra positiva
    - creamos el widget dp
    - solicitamos el hook al dp de los posibles hooks pendientes a esa uri
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
            webop=operation.NewDatasourceDatapointOperation(uid=datasource['uid'],aid=datasource['aid'],did=did,pid=datapoint['pid'])
            authop=webop.get_auth_operation()
            params=webop.get_params()
            response.add_message(messages.UpdateQuotesMessage(operation=authop, params=params))
            response.add_message(messages.ResourceAuthorizationUpdateMessage(operation=authop, params=params))
            response.add_message(messages.FillDatapointMessage(pid=datapoint['pid'],date=date))
            response.add_message(messages.UserEventMessage(uid=uid,event_type=eventstypes.USER_EVENT_NOTIFICATION_NEW_DATAPOINT, parameters={'pid':datapoint['pid'].hex}))
            if datapoint['previously_existed'] is False:
                response.add_message(messages.NewDPWidgetMessage(uid=uid,pid=datapoint['pid']))
                uris=[{'type':vertex.DATAPOINT, 'id':datapoint['pid'], 'uri':datapoint['datapointname']}]
                response.add_message(messages.HookNewUrisMessage(uid=uid, uris=uris, date=date))
            response.status=status.IMC_STATUS_OK
        else:
            logging.logger.error('Error registering datapoint in database. did: '+did.hex+' date: '+date.hex+' position: '+str(position)+' length: '+str(length))
            response.error=Errors.E_IIAG_MONVAR_EMV
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_MONVAR_BP
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
        datapoints=datapointapi.mark_negative_variable(pid=pid, date=date, position=position, length=length)
        if datapoints:
            for a_pid in datapoints:
                response.add_message(messages.FillDatapointMessage(pid=a_pid,date=date))
            response.status=status.IMC_STATUS_OK
        else:
            response.error=Errors.E_IIAG_NEGVAR_EMNV
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_NEGVAR_BP
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
        datapoints=datapointapi.mark_positive_variable(date=date, position=position, length=length, pid=pid)
        if datapoints:
            for a_pid in datapoints:
                response.add_message(messages.FillDatapointMessage(pid=a_pid,date=date))
            response.status=status.IMC_STATUS_OK
        else:
            response.error=Errors.E_IIAG_POSVAR_EMPV
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_POSVAR_BP
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
            logging.logger.error('Error sending new user welcome mail to: '+usermail)
            response.error=Errors.E_IIAG_NEWUSR_ESWM
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_NEWUSR_BP
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
            logging.logger.error('Error sending invitation mail to: '+email)
            response.error=Errors.E_IIAG_NEWINV_ESIM
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_NEWINV_BP
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
            logging.logger.error('Error sending forget mail to: '+email)
            response.error=Errors.E_IIAG_FORGETMAIL_ESFM
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_FORGETMAIL_BP
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
            webop=operation.NewWidgetSystemOperation(uid=widget['uid'],wid=widget['wid'])
            authop=webop.get_auth_operation()
            params=webop.get_params()
            response.add_message(messages.UpdateQuotesMessage(operation=authop, params=params))
            response.add_message(messages.ResourceAuthorizationUpdateMessage(operation=authop, params=params))
            response.status=status.IMC_STATUS_OK
        else:
            response.error=Errors.E_IIAG_NEWDSW_ECW
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_NEWDSW_BP
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
            webop=operation.NewWidgetSystemOperation(uid=widget['uid'],wid=widget['wid'])
            authop=webop.get_auth_operation()
            params=webop.get_params()
            response.add_message(messages.UpdateQuotesMessage(operation=authop, params=params))
            response.add_message(messages.ResourceAuthorizationUpdateMessage(operation=authop, params=params))
            response.status=status.IMC_STATUS_OK
        else:
            response.error=Errors.E_IIAG_NEWDPW_ECW
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
        response.error=Errors.E_IIAG_NEWDPW_BP
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELUSER(message):
    ''' this message deletes a user from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uid=message.uid
    if args.is_valid_uuid(uid):
        deleteapi.delete_user(uid=uid)
        #TODO: Enviar email de despedida
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELUSER_BP
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
        op_id=Operations.DELETE_AGENT
        op_params={'uid':agent['uid']}
        response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELAGENT_BP
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
        op_id=Operations.DELETE_DATASOURCE
        op_params={'uid':datasource['uid'],'aid':datasource['aid']}
        response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELDS_BP
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

@exceptions.ExceptionHandler
def process_message_DELDP(message):
    ''' this message deletes a datapoint from the system '''
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    pid=message.pid
    if args.is_valid_uuid(pid):
        datapoint=datapointapi.get_datapoint_config(pid=pid)
        datasource=None
        if datapoint['did'] is not None:
            datasource=datasourceapi.get_datasource_config(did=datapoint['did'])
        deleteapi.delete_datapoint(pid=pid)
        if datasource:
            op_id=Operations.DELETE_DATASOURCE_DATAPOINT
            op_params={'uid':datapoint['uid'],'aid':datasource['aid'],'did':datapoint['did']}
            response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        else:
            op_id=Operations.DELETE_USER_DATAPOINT
            op_params={'uid':datapoint['uid']}
            response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELDP_BP
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
        op_id=Operations.DELETE_WIDGET
        op_params={'uid':widget['uid']}
        response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELWIDGET_BP
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
        op_id=Operations.DELETE_DASHBOARD
        op_params={'uid':dashboard['uid']}
        response.add_message(messages.UpdateQuotesMessage(operation=op_id, params=op_params))
        response.status=status.IMC_STATUS_OK
    else:
        response.error=Errors.E_IIAG_DELDASHB_BP
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

