'''

Anomalies message definitions

'''

import uuid
from komlog.komfig import logging
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions


@exceptions.ExceptionHandler
def process_message_MISSINGDP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message.type, message_params=message.serialized_message)
    did=message.did
    date=message.date
    dp_classified=datasourceapi.classify_missing_datapoints_in_sample(did=did, date=date)
    if len(dp_classified['doubts'])>0:
        datasource=datasourceapi.get_datasource_config(did=did)
        response.add_msg_originated(messages.UserEventMessage(uid=datasource['uid'], event_type=eventstypes.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, parameters={'did':did.hex,'date':date.hex,'doubts':[pid.hex for pid in dp_classified['doubts']],'discarded':[pid.hex for pid in dp_classified['discarded']]}))
    response.status=status.IMC_STATUS_OK
    return response

