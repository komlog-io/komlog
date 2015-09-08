import unittest
import uuid
from komfig import logger
from komlibs.interface.imc.api import anomalies
from komlibs.interface.imc.model import messages
from komlibs.interface.imc import status, exceptions
from komlibs.general.time import timeuuid
from komlibs.gestaccount import errors as gesterrors


class InterfaceImcApiAnomaliesTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.anomalies tests '''

    def test_process_message_MISSINGDP_failure_not_found(self):
        ''' process_message_MISSINGDP should fail if did does not exist '''
        did=uuid.uuid4()
        date=uuid.uuid1()
        message=messages.MissingDatapointMessage(did=did,date=date)
        response=anomalies.process_message_MISSINGDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GDA_CMDIS_DSMNF)

