'''

Lambda functionality related messages

'''

import traceback
from komlog.komfig import logging, defaults
from komlog.komlibs.auth import session, passport, authorization
from komlog.komlibs.auth.resources import authorization as resauth
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.websocket import session as ws_session
from komlog.komlibs.interface.websocket.model.message import MessagesCatalog
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komimc import bus as msgbus


@exceptions.ExceptionHandler
def process_message_URISUPDT(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    uris=message.uris
    date=message.date
    hooks={}
    contents={}
    uris_info={}
    users_info={}
    for uri in uris:
        try:
            if uri['type'] == vertex.DATASOURCE:
                sids=datasourceapi.get_datasource_hooks(did=uri['id'])
                if len(sids)>0:
                    info = datasourceapi.get_datasource_config(did=uri['id'], pids_flag=False, widget_flag=False)
                    uris_info[uri['id']]=info
                    ds_data=datasourceapi.get_datasource_data(did=uri['id'], fromdate=date, todate=date, count=1)
                    contents[uri['id']]=ds_data[0]['content']
                    for sid in sids:
                        try:
                            hooks[sid].append(uri)
                        except KeyError:
                            hooks[sid]=[uri]
            elif uri['type'] == vertex.DATAPOINT:
                sids=datapointapi.get_datapoint_hooks(pid=uri['id'])
                if len(sids)>0:
                    info = datapointapi.get_datapoint_config(pid=uri['id'], stats_flag=False, widget_flag=False)
                    uris_info[uri['id']]=info
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
                    if session.delete_agent_session(sid=sid, last_update=session_info.last_update):
                        message=messages.ClearSessionHooksMessage(sid=sid, ids=[(item['id'],item['type']) for item in uris])
                        response.add_imc_message(message)
            else:
                data=[]
                for item in uris:
                    try:
                        if item['type'] == vertex.DATASOURCE:
                            resauth.authorize_get_datasource_data(uid=session_info.uid,did=item['id'])
                        elif item['type'] == vertex.DATAPOINT:
                            resauth.authorize_get_datapoint_data(uid=session_info.uid,pid=item['id'])
                        item_uid = uris_info[item['id']]['uid']
                        if session_info.uid == item_uid:
                            uri = item['uri']
                        else:
                            if not item_uid in users_info:
                                user_info = userapi.get_user_config(uid=item_uid)
                                users_info[item_uid]=user_info
                            uri = ':'.join((users_info[item_uid]['username'],item['uri']))
                        data.append({'uri':uri,'type':item['type'],'content':contents[item['id']]})
                    except (
                        authexcept.AuthorizationException,
                        gestexcept.UserNotFoundException):
                        pass
                if len(data)>0:
                    msg=MessagesCatalog.get_message(version=session_info.pv, action=Messages.SEND_MULTI_DATA, t=date, uris=data)
                    if msg:
                        message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
                        response.add_imc_message(message,dest=session_info.imc_address)
        except authexcept.SessionNotFoundException:
            message=messages.ClearSessionHooksMessage(sid=sid, ids=[(item['id'],item['type']) for item in uris])
            response.add_imc_message(message)
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_HOOKNEW(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    uid=message.uid
    uris=message.uris
    date=message.date
    hooked=[]
    for item in uris:
        sids=userapi.get_uri_pending_hooks(uid=uid, uri=item['uri'])
        if len(sids)>0:
            try:
                if item['type'] == vertex.DATASOURCE:
                    for sid in sids:
                        datasourceapi.hook_to_datasource(did=item['id'],sid=sid)
                elif item['type'] == vertex.DATAPOINT:
                    for sid in sids:
                        datapointapi.hook_to_datapoint(pid=item['id'],sid=sid)
            except (
                gestexcept.DatapointNotFoundException,
                gestexcept.DatasourceNotFoundException):
                pass
            else:
                hooked.append(item)
                userapi.delete_uri_pending_hooks(uid=uid, uri=item['uri'])
    if len(hooked)>0:
        msg=messages.UrisUpdatedMessage(uris=hooked, date=date)
        response.add_imc_message(msg)
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_CLSHOOKS(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    sid=message.sid
    ids=message.ids
    for item in ids:
        if item[1] == vertex.DATASOURCE:
            datasourceapi.unhook_from_datasource(did=item[0], sid=sid)
        elif item[1] == vertex.DATAPOINT:
            datapointapi.unhook_from_datapoint(pid=item[0], sid=sid)
    userapi.delete_session_pending_hooks(sid=sid)
    response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_SSDATA(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    try:
        ws_session.agent_callback[message.sid](message=message.data)
    except KeyError:
        try:
            session_info=session.get_agent_session_info(sid=message.sid)
            if session_info.imc_address==msgbus.msgbus.imc_address:
                if session.unset_agent_session(sid=message.sid,last_update=session_info.last_update):
                    response.error=Errors.E_IIALD_SSDT_SUS
                else:
                    response.error=Errors.E_IIALD_SSDT_SUE
            else:
                response.error=Errors.E_IIALD_SSDT_MRE
                if session_info.imc_address is not None:
                    response.add_imc_message(message,dest=session_info.imc_address)
        except authexcept.SessionNotFoundException:
            response.error=Errors.E_IIALD_SSDT_SNF
        response.status=status.IMC_STATUS_NOT_FOUND
    except Exception:
        ex_info=traceback.format_exc().splitlines()
        for line in ex_info:
            logging.logger.error(line)
    else:
        response.status=status.IMC_STATUS_OK
    return response

@exceptions.ExceptionHandler
def process_message_DATINT(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    sid=message.sid
    session_info=session.get_agent_session_info(sid=sid)
    if session_info.imc_address is None:
        if timeuuid.get_unix_timestamp(session_info.last_update)+defaults.SESSION_INACTIVITY_EXPIRATION_SECONDS < timeuuid.get_unix_timestamp(timeuuid.uuid1()):
            result=session.delete_agent_session(sid=sid, last_update=session_info.last_update)
            response.error=Errors.E_IIALD_DATINT_SEXP
        else:
            response.error=Errors.E_IIALD_DATINT_NSA
        response.status=status.IMC_STATUS_NOT_FOUND
        return response
    psp=passport.AgentPassport(uid=session_info.uid, aid=session_info.aid, sid=session_info.sid, pv=session_info.pv)
    try:
        if message.uri['type'] == vertex.DATASOURCE:
            info = datasourceapi.get_datasource_config(did=message.uri['id'],pids_flag=False, widget_flag=False)
            if info['uid'] != session_info.uid:
                user_info = userapi.get_user_config(uid=info['uid'])
                item_uri = ':'.join((user_info['username'],message.uri['uri']))
            else:
                item_uri = message.uri['uri']
            authorization.authorize_get_datasource_data(psp, did=message.uri['id'], ii=message.ii, ie=message.ie, tid=None)
        elif message.uri['type'] == vertex.DATAPOINT:
            info = datapointapi.get_datapoint_config(pid=message.uri['id'],stats_flag=False, widget_flag=False)
            if info['uid'] != session_info.uid:
                user_info = userapi.get_user_config(uid=info['uid'])
                item_uri = ':'.join((user_info['username'],message.uri['uri']))
            else:
                item_uri = message.uri['uri']
            authorization.authorize_get_datapoint_data(psp, pid=message.uri['id'], ii=message.ii, ie=message.ie, tid=None)
    except authexcept.IntervalBoundsException as e:
        if message.ie.time<e.data['date'].time:
            uri={'uri':item_uri,'type':message.uri['type']}
            start=message.ii
            end=message.ie
            data=[]
            msg=MessagesCatalog.get_message(version=session_info.pv, action=Messages.SEND_DATA_INTERVAL, uri=uri, start=start, end=end, data=data, irt=message.irt)
            if msg:
                imc_message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
                response.add_imc_message(imc_message,dest=session_info.imc_address)
            response.status=status.IMC_STATUS_ACCESS_DENIED
        else:
            uri={'uri':item_uri,'type':message.uri['type']}
            start=message.ii
            limit=e.data['date']
            end=limit
            msg=MessagesCatalog.get_message(version=session_info.pv, action=Messages.SEND_DATA_INTERVAL, uri=uri, start=start, end=end, data=[], irt=message.irt)
            if msg:
                imc_message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
                response.add_imc_message(imc_message,dest=session_info.imc_address)
            imc_message=messages.DataIntervalRequestMessage(sid=sid, uri=message.uri, ii=limit, ie=message.ie, count=message.count, irt=message.irt)
            response.add_imc_message(imc_message)
            response.status=status.IMC_STATUS_OK
    else:
        uri={'uri':item_uri,'type':message.uri['type']}
        start=message.ii
        end=message.ie
        resp_data=[]
        try:
            if uri['type']==vertex.DATAPOINT:
                count=message.count if message.count and message.count < 1000 else 1000
                data=datapointapi.get_datapoint_data(pid=message.uri['id'],fromdate=message.ii, todate=message.ie, count=count)
                for row in data:
                    resp_data.append((row['date'].hex,str(row['value'])))
            elif uri['type']==vertex.DATASOURCE:
                count=message.count if message.count and message.count < 100 else 100
                data=datasourceapi.get_datasource_data(did=message.uri['id'],fromdate=message.ii, todate=message.ie, count=count)
                for row in data:
                    resp_data.append((row['date'].hex,str(row['content'])))
        except (gestexcept.DatapointDataNotFoundException,
            gestexcept.DatasourceDataNotFoundException):
            pass
        if len(resp_data)==count:
            new_ie=data[-1]['date']
            start=new_ie
            if message.count != count:
                new_count = message.count-count if message.count else None
                imc_message=messages.DataIntervalRequestMessage(sid=sid, uri=message.uri, ii=message.ii, ie=new_ie, count=new_count, irt=message.irt)
                response.add_imc_message(imc_message)
        msg=MessagesCatalog.get_message(version=session_info.pv, action=Messages.SEND_DATA_INTERVAL, uri=uri, start=start, end=end, data=resp_data, irt=message.irt)
        if msg:
            imc_message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
            response.add_imc_message(imc_message,dest=session_info.imc_address)
    response.status=status.IMC_STATUS_OK
    return response

