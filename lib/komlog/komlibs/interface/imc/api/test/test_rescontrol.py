import unittest
import uuid
import json
from komlog.komlibs.interface.web.operations import weboperations
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status


class InterfaceImcApiRescontrolTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.rescontrol tests '''

    def test_process_message_UPDQUO_fail_user_does_not_exist(self):
        ''' process_message_UPDQUO should fail if user does not exist '''
        operation=weboperations.NewAgentOperation(uid=uuid.uuid4(), aid=uuid.uuid4())
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.UpdateQuotesMessage(operation=auth_op.value, params=params)
        response=rescontrol.process_message_UPDQUO(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_INTERNAL_ERROR)

    def test_process_message_RESAUTH_success(self):
        ''' process_message_RESAUTH should succeed if operation and params are correct '''
        operation=weboperations.NewAgentOperation(uid=uuid.uuid4(), aid=uuid.uuid4())
        auth_op=operation.get_auth_operation()
        params=operation.get_params()
        message=messages.ResourceAuthorizationUpdateMessage(operation=auth_op.value, params=params)
        response=rescontrol.process_message_RESAUTH(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)

