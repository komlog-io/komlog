'''

Events message definitions

'''

import uuid
from komfig import logger
from komlibs.general.validation import arguments as args
from komlibs.events.api import user as usereventsapi
from komlibs.events.model import types as eventstypes
from komlibs.interface.imc.model import messages, responses
from komlibs.interface.imc import status, exceptions


@exceptions.ExceptionHandler
def process_message_USEREV(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uid=message.uid
    event_type=message.event_type
    parameters=message.parameters
    if event_type==eventstypes.NEW_USER:
        if not 'username' in parameters or not args.is_valid_username(parameters['username']):
            raise exceptions.BadParametersException()
        username=parameters['username']
        if usereventsapi.insert_new_user_event(uid=uid, username=username):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_AGENT:
        if not 'aid' in parameters or not args.is_valid_hex_uuid(parameters['aid']):
            raise exceptions.BadParametersException()
        if not 'agentname' in parameters or not args.is_valid_agentname(parameters['agentname']):
            raise exceptions.BadParametersException()
        aid=uuid.UUID(parameters['aid'])
        agentname=parameters['agentname']
        if usereventsapi.insert_new_agent_event(uid=uid, aid=aid, agentname=agentname):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_DATASOURCE:
        if not 'aid' in parameters or not args.is_valid_hex_uuid(parameters['aid']):
            raise exceptions.BadParametersException()
        if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
            raise exceptions.BadParametersException()
        if not 'datasourcename' in parameters or not args.is_valid_datasourcename(parameters['datasourcename']):
            raise exceptions.BadParametersException()
        aid=uuid.UUID(parameters['aid'])
        did=uuid.UUID(parameters['did'])
        datasourcename=parameters['datasourcename']
        if usereventsapi.insert_new_datasource_event(uid=uid, aid=aid, did=did, datasourcename=datasourcename):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_DATAPOINT:
        if not 'did' in parameters or not args.is_valid_hex_uuid(parameters['did']):
            raise exceptions.BadParametersException()
        if not 'pid' in parameters or not args.is_valid_hex_uuid(parameters['pid']):
            raise exceptions.BadParametersException()
        if not 'datasourcename' in parameters or not args.is_valid_datasourcename(parameters['datasourcename']):
            raise exceptions.BadParametersException()
        if not 'datapointname' in parameters or not args.is_valid_datapointname(parameters['datapointname']):
            raise exceptions.BadParametersException()
        did=uuid.UUID(parameters['did'])
        pid=uuid.UUID(parameters['pid'])
        datasourcename=parameters['datasourcename']
        datapointname=parameters['datapointname']
        if usereventsapi.insert_new_datapoint_event(uid=uid, did=did, pid=pid, datasourcename=datasourcename, datapointname=datapointname):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_WIDGET:
        if not 'wid' in parameters or not args.is_valid_hex_uuid(parameters['wid']):
            raise exceptions.BadParametersException()
        if not 'widgetname' in parameters or not args.is_valid_widgetname(parameters['widgetname']):
            raise exceptions.BadParametersException()
        wid=uuid.UUID(parameters['wid'])
        widgetname=parameters['widgetname']
        if usereventsapi.insert_new_widget_event(uid=uid, wid=wid, widgetname=widgetname):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_DASHBOARD:
        if not 'bid' in parameters or not args.is_valid_hex_uuid(parameters['bid']):
            raise exceptions.BadParametersException()
        if not 'dashboardname' in parameters or not args.is_valid_dashboardname(parameters['dashboardname']):
            raise exceptions.BadParametersException()
        bid=uuid.UUID(parameters['bid'])
        dashboardname=parameters['dashboardname']
        if usereventsapi.insert_new_dashboard_event(uid=uid, bid=bid, dashboardname=dashboardname):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    elif event_type==eventstypes.NEW_CIRCLE:
        if not 'cid' in parameters or not args.is_valid_hex_uuid(parameters['cid']):
            raise exceptions.BadParametersException()
        if not 'circlename' in parameters or not args.is_valid_circlename(parameters['circlename']):
            raise exceptions.BadParametersException()
        cid=uuid.UUID(parameters['cid'])
        circlename=parameters['circlename']
        if usereventsapi.insert_new_circle_event(uid=uid, cid=cid, circlename=circlename):
            response.status=status.IMC_STATUS_OK
        else:
            response.status=status.IMC_STATUS_INTERNAL_ERROR
    else:
            response.status=status.IMC_STATUS_BAD_PARAMETERS
    return response

