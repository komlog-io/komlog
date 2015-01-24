import unittest
import uuid
import json
from komlibs.interface.imc.api import gestconsole
from komlibs.interface.imc.model import messages
from komlibs.interface.imc import status
from komlibs.general.time import timeuuid


class InterfaceImcApiGestconsoleTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.gestconsole tests '''

    def test_process_message_MONVAR_failure_non_existent_did(self):
        ''' process_message_MONVAR should fail if did does not exists '''
        username='test_process_message_monvar_failure'
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_process_message_MONVAR_failure_invalid_username_datapointname'
        message=messages.MonitorVariableMessage(username=username, did=did, date=date, position=position, length=length, datapointname=datapointname)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_NEGVAR_failure_non_existent_datapoint(self):
        ''' process_message_NEGVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.NegativeVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_POSVAR_failure_non_existent_datapoint(self):
        ''' process_message_POSVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.PositiveVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_POSVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

