'''

this file implement the processing of the different actions supported by the
protocol

'''

import uuid
import json
from komlog.komfig import logging, config, options
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.requests import Requests
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.websocket.protocol.v1 import status, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import operation
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import operation as modop
from komlog.komlibs.interface.websocket.protocol.v1.model.response import Response



def _process_send_ds_data(passport, message):
    message = modmsg.SendDsDataMessage(message=message)
    did=None
    new_datasource=False
    uri_info=graphuri.get_id(ido=passport.uid, uri=message.payload['uri'])
    if not uri_info or uri_info['type']==vertex.VOID:
        authorization.authorize_request(request=Requests.NEW_DATASOURCE,passport=passport)
        datasource=datasourceapi.create_datasource(uid=passport.uid, aid=passport.aid, datasourcename=message.payload['uri'])
        if datasource:
            new_datasource = True
            did=datasource['did']
        else:
            return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDD_ECDS)
    elif uri_info['type']==vertex.DATASOURCE:
        did=uri_info['id']
        authorization.authorize_request(request=Requests.POST_DATASOURCE_DATA,passport=passport,did=did)
    else:
        return Response(status=status.MESSAGE_EXECUTION_DENIED, reason='uri is not a datasource', error=Errors.E_IWSPV1PM_PSDD_IURI)
    try:
        dest_dir=config.get(options.SAMPLES_RECEIVED_PATH)
        datasourceapi.upload_datasource_data(did=did, content=json.dumps({'content':message.payload['content'],'ts':message.payload['ts']}),dest_dir=dest_dir)
    except Exception:
        if new_datasource:
            deleteapi.delete_datasource(did=datasource['did'])
        return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDD_EUR)
    else:
        if new_datasource:
            try:
                op=modop.NewDatasourceOperation(uid=passport.uid,aid=passport.aid,did=datasource['did'])
                op_result=operation.process_operation(op)
            except Exception as e:
                deleteapi.delete_datasource(did=datasource['did'])
                return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDD_EUR)
            else:
                if op_result == False:
                    deleteapi.delete_datasource(did=datasource['did'])
                    return Response(status=status.MESSAGE_EXECUTION_ERROR, reason='internal error', error=Errors.E_IWSPV1PM_PSDD_FUR)
        return Response(status=status.MESSAGE_ACCEPTED_FOR_PROCESSING)

