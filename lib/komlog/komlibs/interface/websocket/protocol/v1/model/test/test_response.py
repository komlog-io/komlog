import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.interface.websocket.protocol.v1 import errors, exceptions
from komlog.komlibs.interface.websocket.protocol.v1.model import response


class InterfaceWebSocketProtocolV1ModelResponseTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.model.response tests '''

    def test_new_response_success(self):
        ''' a new response object should be created '''
        status=2
        error=222
        reason=None
        resp=response.Response(status, error, reason)
        self.assertTrue(isinstance(resp,response.Response))
        self.assertEqual(resp.status, status)
        self.assertEqual(resp.error,error)
        self.assertEqual(resp.reason,reason)

    def test_new_response_failure_invalid_status(self):
        ''' the creation of a response object should fail if status is not a positive integer '''
        statuses=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}]
        for status in statuses:
            with self.assertRaises(exceptions.ResponseValidationException) as cm:
                resp=response.Response(status=status)
            self.assertEqual(cm.exception.error, errors.E_IWSPV1MR_RESP_IS)

