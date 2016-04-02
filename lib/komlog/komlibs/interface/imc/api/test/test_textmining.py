import unittest
import uuid
from komlog.komfig import logger
from komlog.komlibs.interface.imc.api import textmining
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.general.time import timeuuid


class InterfaceImcApiTextminingTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.textmining tests '''

    def test_process_message_GDTREE_failure_non_existent_pid(self):
        ''' process_message_GDTREE should fail if pid does not exist '''
        pid=uuid.uuid4()
        message=messages.GenerateDTreeMessage(pid=pid)
        response=textmining.process_message_GDTREE(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_MAPVARS_failure_non_existent_data(self):
        ''' process_message_MAPVARS should fail if data does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.MapVarsMessage(did=did,date=date)
        response=textmining.process_message_MAPVARS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_FILLDP_failure_non_existent_pid(self):
        ''' process_message_FILLDP should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.FillDatapointMessage(pid=pid,date=date)
        response=textmining.process_message_FILLDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_FILLDS_failure_non_existent_pid(self):
        ''' process_message_FILLDS should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.FillDatasourceMessage(did=did,date=date)
        response=textmining.process_message_FILLDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_GENTEXTSUMMARY_failure_non_existent_pid(self):
        ''' process_message_GENTEXTSUMMARY should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        message=messages.GenerateTextSummaryMessage(did=did,date=date)
        response=textmining.process_message_GENTEXTSUMMARY(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

