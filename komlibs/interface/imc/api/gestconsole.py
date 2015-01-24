#coding:utf-8
'''

Gestconsole message definitions 

'''

from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.gestaccount.datapoint import api as datapointapi
from komlibs.gestaccount.datasource import api as datasourceapi
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
    username=message.username
    did=message.did
    date=message.date
    position=message.position
    length=message.length
    datapointname=message.datapointname
    if args.is_valid_username(username) and args.is_valid_uuid(did) and args.is_valid_date(date) and args.is_valid_int(position) and args.is_valid_int(length) and args.is_valid_datapointname(datapointname):
        datapoint=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        if datapoint:
            datasource=datasourceapi.get_datasource_config(did=did)
            operation=weboperations.NewDatapointOperation(uid=datasource['uid'],aid=datasource['aid'],did=did,pid=datapoint['pid'])
            newmsg=messages.UpdateQuotesMessage(operation=operation)
            response.add_msg_originated(newmsg)
            newmsg=messages.ResourceAuthorizationUpdateMessage(operation=operation)
            response.add_msg_originated(newmsg)
            #hay que solicitar el fildtp tambien
            #newmsg=messages.NewWidgetMessage(username=username,widget_type=widgettypes.DP_WIDGET,params={'pid':datapoint['pid']})
            #response.add_msg_originated(newmsg)
            response.status=status.IMC_STATUS_OK
        else:
            logger.logger.error('Error registering datapoint in database. did: '+did.hex+' date: '+date.hex+' position: '+str(position))
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
    else:
        response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

