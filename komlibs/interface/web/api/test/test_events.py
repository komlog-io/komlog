import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.interface.web.api import user as userapi
from komlibs.interface.web.api import events as eventsapi
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.interface.imc.model import messages
from komimc import bus, routing
from komimc import api as msgapi


class InterfaceWebApiEventsTest(unittest.TestCase):
    ''' komlibs.interface.web.api.events tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        username = 'test_komlibs.interface.web.api.events_user'
        userresponse=userapi.get_user_config_request(username=username)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msg_addr=routing.get_address(type=messages.NEW_USR_NOTIF_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
            msg_addr=routing.get_address(type=messages.USER_EVENT_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if msg:
                    msg_result=msgapi.process_message(msg)
                    if msg_result:
                        msgapi.process_msg_result(msg_result)
                else:
                    break
            userresponse = userapi.get_user_config_request(username=username)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
        self.userinfo=userresponse.data

    def test_get_user_events_request_failure_invalid_username(self):
        ''' get_user_events_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for username in usernames:
            response=eventsapi.get_user_events_request(username=username)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_invalid_end_date(self):
        ''' get_user_events_request should fail if end_date is invalid '''
        end_dates=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_user_events_request_failure_invalid_end_date'
        for end_date in end_dates:
            response=eventsapi.get_user_events_request(username=username, end_date=end_date)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_user_not_found(self):
        ''' get_user_events_request should fail if username is not found '''
        username='test_get_user_events_request_failure_user_not_found'
        response=eventsapi.get_user_events_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)

    def test_get_user_events_request_success(self):
        ''' get_users_circles_config_request should succeed '''
        username=self.userinfo['username']
        response=eventsapi.get_user_events_request(username=username)
        self.assertEqual(response.status, status.WEB_STATUS_OK)

