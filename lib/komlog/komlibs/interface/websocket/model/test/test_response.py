import unittest
import time
import uuid
import json
from komlog.komfig import logging
from komlog.komlibs.interface.websocket import exceptions
from komlog.komlibs.interface.websocket.errors import Errors
from komlog.komlibs.interface.websocket.model import response


class InterfaceWebSocketModelResponseTest(unittest.TestCase):
    ''' komlibs.interface.websocket.model.response tests '''

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
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test_new_response_failure_invalid_status(self):
        ''' the creation of a response object should fail if status is not a positive integer '''
        statuses=['adas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}]
        for status in statuses:
            with self.assertRaises(exceptions.ResponseValidationException) as cm:
                resp=response.Response(status=status)
            self.assertEqual(cm.exception.error, Errors.E_IWSMR_RESP_IS)

    def test_Response_error_setting_routed_messages(self):
        ''' Response.routed_messages should not be modified manually, always call add_message() '''
        resp=response.Response(status=1)
        with self.assertRaises(TypeError) as cm:
            resp.routed_messages={'route':['message']}

    def test_Response_error_setting_unrouted_messages(self):
        ''' Response.unrouted_messages should not be modified manually, always call add_message()'''
        resp=response.Response(status=1)
        with self.assertRaises(TypeError) as cm:
            resp.unrouted_messages=['message']

    def test_Response_messages_right_routing(self):
        ''' when adding a msg to a Response, the message should be added successfully to the routed/unrouted attributes '''
        dest='host'
        routed_messages=['message1','message2','message3','message4']
        unrouted_messages=['msg1','msg2','msg3','msg4']
        resp=response.Response(status=1)
        for msg in unrouted_messages:
            self.assertTrue(resp.add_message(msg))
        for msg in routed_messages:
            self.assertTrue(resp.add_message(msg, dest=dest))
        self.assertEqual(resp.routed_messages,{dest:routed_messages})
        self.assertEqual(resp.unrouted_messages,unrouted_messages)

