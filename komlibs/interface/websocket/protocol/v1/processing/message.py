'''

this file implement the processing of the different actions supported by the
protocol

'''

import uuid
import json
from komfig import logger, config, options
from komlibs.auth import authorization, requests
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.common import delete as deleteapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.user import api as userapi
from komlibs.general.validation import arguments as args
from komlibs.graph.api import uri as graphuri
from komlibs.graph.relations import vertex
from komlibs.interface.websocket.protocol.v1 import status, errors, exceptions
from komlibs.interface.websocket.protocol.v1.processing import operation
from komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlibs.interface.websocket.protocol.v1.model import operation as modop


def _process_post_datasource_data(username, aid, message):
    if not args.is_valid_username(username):
        raise exceptions.BadParametersException(error=errors.E_IWSPV1PM_PPDD_IU)
    if not args.is_valid_hex_uuid(aid):
        raise exceptions.BadParametersException(error=errors.E_IWSPV1PM_PPDD_IHAID)
    message = modmsg.PostDatasourceDataMessage(message=message)
    uid=userapi.get_uid(username=username)
    aid=uuid.UUID(aid)
    did=None
    new_datasource=False
    agent=agentapi.get_agent_config(aid=aid)
    uri_info=graphuri.get_id(ido=uid, uri=message.payload['uri'])
    if not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=requests.NEW_DATASOURCE,uid=uid,aid=aid)
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=message.payload['uri'])
        if datasource:
            new_datasource = True
            did=datasource['did']
        else:
            return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=errors.E_IWSPV1PM_PPDD_ECDS)
    elif uri_info['type']==vertex.DATASOURCE:
        did=uri_info['id']
        authorization.authorize_request(request=requests.POST_DATASOURCE_DATA,uid=uid,aid=aid,did=did)
    else:
        return modresp.Response(status=status.MESSAGE_EXECUTION_DENIED, reason='uri is not a datasource', error=errors.E_IWSPV1PM_PPDD_IURI)
    try:
        dest_dir=config.get(options.SAMPLES_RECEIVED_PATH)
        datasourceapi.upload_datasource_data(did=did, content=json.dumps({'content':message.payload['content'],'ts':message.payload['ts']}),dest_dir=dest_dir)
    except Exception:
        if new_datasource:
            deleteapi.delete_datasource(did=datasource['did'])
        return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=errors.E_IWSPV1PM_PPDD_EUR)
    else:
        if new_datasource:
            try:
                op=modop.NewDatasourceOperation(uid=uid,aid=aid,did=datasource['did'])
                op_result=operation.process_operation(op)
            except Exception:
                deleteapi.delete_datasource(did=datasource['did'])
                return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=errors.E_IWSPV1PM_PPDD_EUR)
            else:
                if op_result == False:
                    deleteapi.delete_datasource(did=datasource['did'])
                    return modresp.Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=errors.E_IWSPV1PM_PPDD_FUR)
        return modresp.Response(status=status.MESSAGE_ACCEPTED_FOR_PROCESSING)

