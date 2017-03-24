'''

Anomalies message definitions

'''

import uuid
from komlog.komfig import logging
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.events.model import types as eventstypes
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.interface.imc.model import messages, responses
from komlog.komlibs.interface.imc import status, exceptions


@exceptions.ExceptionHandler
def process_message_MISSINGDP(message):
    response=responses.ImcInterfaceResponse(status=status.IMC_STATUS_PROCESSING, message_type=message._type_, message_params=message.to_serialization())
    did=message.did
    date=message.date
    dp_classified=datapointapi.classify_missing_datapoints_in_sample(did=did, date=date)
    for pid in dp_classified['doubts']:
        parameters={'did':did.hex, 'dates':[date.hex],'pid':pid.hex}
        response.add_imc_message(messages.UserEventMessage(uid=datasource['uid'], event_type=eventstypes.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION, parameters=parameters))
    response.status=status.IMC_STATUS_OK
    return response

