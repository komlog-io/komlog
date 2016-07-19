'''

Lambda functionality related messages

'''

from komlog.komfig import logging, defaults
from komlog.komlibs.auth import session
from komlog.komlibs.auth.resources import authorization as resauth
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.websocket import session as ws_session
from komlog.komlibs.interface.websocket.protocol.v1.model import message as ws_message
from komlog.komimc import bus as msgbus


@exceptions.ExceptionHandler
def process_message_URISUPDT(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    uris=message.uris
    date=message.date
    hooks={}
    contents={}
    for uri in uris:
        try:
            if uri['type'] == vertex.DATASOURCE:
                sids=datasourceapi.get_datasource_hooks(did=uri['id'])
                if len(sids)>0:
                    ds_data=datasourceapi.get_datasource_data(did=uri['id'], date=date)
                    contents[uri['id']]=ds_data['content']
                    for sid in sids:
                        try:
                            hooks[sid].append(uri)
                        except KeyError:
                            hooks[sid]=[uri]
            elif uri['type'] == vertex.DATAPOINT:
                sids=datapointapi.get_datapoint_hooks(pid=uri['id'])
                if len(sids)>0:
                    dp_data=datapointapi.get_datapoint_data(pid=uri['id'], fromdate=date, todate=date, count=1)
                    contents[uri['id']]=str(dp_data[0]['value'])
                    for sid in sids:
                        try:
                            hooks[sid].append(uri)
                        except KeyError:
                            hooks[sid]=[uri]
        except (
            gestexcept.DatapointNotFoundException,
            gestexcept.DatapointDataNotFoundException,
            gestexcept.DatasourceNotFoundException,
            gestexcept.DatasourceDataNotFoundException):
            pass
    for sid,uris in hooks.items():
        try:
            session_info=session.get_agent_session_info(sid=sid)
            if session_info.imc_address is None:
                if timeuuid.get_unix_timestamp(session_info.last_update)+defaults.SESSION_INACTIVITY_EXPIRATION_SECONDS < timeuuid.get_unix_timestamp(timeuuid.uuid1()):
                    result=session.delete_agent_session(sid=sid, last_update=session_info.last_update)
            else:
                data=[]
                for uri in uris:
                    try:
                        if uri['type'] == vertex.DATASOURCE:
                            resauth.authorize_get_datasource_data(uid=session_info.uid,did=uri['id'])
                        elif uri['type'] == vertex.DATAPOINT:
                            resauth.authorize_get_datapoint_data(uid=session_info.uid,pid=uri['id'])
                        data.append({'uri':uri['uri'],'type':uri['type'],'content':contents[uri['id']]})
                    except authexcept.AuthorizationException:
                        pass
                if len(data)>0:
                    message=messages.SendSessionDataMessage(sid=sid, date=date, data=data)
                    response.add_message(message,dest=session_info.imc_address)
        except authexcept.SessionNotFoundException:
            message=messages.ClearSessionHooksMessage(sid=sid, ids=[(uri['id'],uri['type']) for uri in uris])
            response.add_message(message)
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_CLSHOOKS(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    sid=message.sid
    ids=message.ids
    for item in ids:
        if item[1] == vertex.DATASOURCE:
            datasourceapi.unhook_from_datasource(did=item[0], sid=sid)
        elif item[1] == vertex.DATAPOINT:
            datapointapi.unhook_from_datapoint(pid=item[0], sid=sid)
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_SSDATA(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    ts=timeuuid.get_isodate_from_uuid(message.date)
    msg=ws_message.SendMultiData(ts=ts, uris=message.data)
    try:
        ws_session.agent_callback[message.sid](message=msg.to_dict())
    except KeyError:
        try:
            session_info=session.get_agent_session_info(sid=message.sid)
            if session_info.imc_address==msgbus.msgbus.imc_address:
                if session.unset_agent_session(sid=message.sid,last_update=message.date):
                    response.error=Errors.E_IIATM_SSDT_SUS
                else:
                    response.error=Errors.E_IIATM_SSDT_SUE
            else:
                response.error=Errors.E_IIATM_SSDT_MRE
                if session_info.imc_address is not None:
                    response.add_message(message,dest=session_info.imc_address)
        except:
            response.error=Errors.E_IIATM_SSDT_SNF
        response.status=status.IMC_STATUS_NOT_FOUND
    else:
        response.status=status.IMC_STATUS_OK
    return response

