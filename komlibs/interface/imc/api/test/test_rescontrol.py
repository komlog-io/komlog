import unittest
import uuid
import json
from komlibs.interface.web.operations import weboperations
from komlibs.interface.imc.api import rescontrol
from komlibs.interface.imc.model import messages
from komlibs.interface.imc import status


class InterfaceImcApiRescontrolTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.rescontrol tests '''

    def test_process_message_UPDQUO_success(self):
        ''' process_message_UPDQUO should succeed because this message does not check if uid or aid exist '''
        operation=weboperations.NewAgentOperation(uid=uuid.uuid4(), aid=uuid.uuid4())
        message=messages.UpdateQuotesMessage(operation=operation)
        response=rescontrol.process_message_UPDQUO(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)

    def test_process_message_RESAUTH_failure(self):
        ''' process_message_RESAUTH should fail because this message check if uid or aid exist '''
        operation=weboperations.NewAgentOperation(uid=uuid.uuid4(), aid=uuid.uuid4())
        message=messages.ResourceAuthorizationUpdateMessage(operation=operation)
        response=rescontrol.process_message_RESAUTH(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)

