import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.interface.web.api import user as userapi
from komlibs.interface.web.api import events as eventsapi
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions, errors
from komlibs.events import errors as eventerrors
from komlibs.events.model import types
from komlibs.events.api import user as usereventsapi
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.general.crypto import crypto
from komlibs.gestaccount import errors as gesterrors
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.interface.imc.model import messages
from komimc import bus, routing
from komimc import api as msgapi
from komlibs.general.time import timeuuid


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

    def test_get_user_events_request_failure_invalid_ets(self):
        ''' get_user_events_request should fail if ets is invalid '''
        etss=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_user_events_request_failure_invalid_end_date'
        for ets in etss:
            response=eventsapi.get_user_events_request(username=username, ets=ets)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_invalid_its(self):
        ''' get_user_events_request should fail if its is invalid '''
        itss=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_get_user_events_request_failure_invalid_end_date'
        for its in itss:
            response=eventsapi.get_user_events_request(username=username, its=its)
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
        self.assertTrue(len(response.data)>=1)
        self.assertTrue('ts' in response.data[0])
        self.assertTrue('type' in response.data[0])
        self.assertTrue('priority' in response.data[0])
        self.assertTrue('seq' in response.data[0])
        self.assertTrue('params' in response.data[0])
        self.assertTrue('html' in response.data[0])

    def test_disable_event_request_failure_invalid_username(self):
        ''' disable_event_request should fail if username is invalid'''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        seq=20*'A'
        for username in usernames:
            response=eventsapi.disable_event_request(username=username, seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_DEVR_IU)

    def test_disable_event_request_failure_invalid_sequence(self):
        ''' disable_event_request should fail if sequence is invalid'''
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_disable_event_request_failure_invalid_sequence'
        for seq in seqs:
            response=eventsapi.disable_event_request(username=username, seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_DEVR_ISEQ)

    def test_disable_event_request_failure_user_not_found(self):
        ''' disable_event_request should fail if username is not found '''
        username='test_disable_event_request_failure_username_not_found'
        seq=20*'B'
        response=eventsapi.disable_event_request(username=username, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GUA_GUID_UNF)

    def test_disable_event_request_failure_sequence_not_found(self):
        ''' disable_event_request should fail if sequence is not found '''
        username=self.userinfo['username']
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        response=eventsapi.disable_event_request(username=username, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_DISE_EVNF)

    def test_event_response_request_failure_invalid_username(self):
        ''' event_response_request should fail if username is invalid '''
        usernames=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data=dict()
        for username in usernames:
            response=eventsapi.event_response_request(username=username, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IU)

    def test_event_response_request_failure_invalid_sequence(self):
        ''' event_response_request should fail if sequence is invalid '''
        username='test_event_response_request_failure_invalid_sequence'
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        data=dict()
        for seq in seqs:
            response=eventsapi.event_response_request(username=username, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_ISEQ)

    def test_event_response_request_failure_invalid_data(self):
        ''' event_response_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame']
        username='test_event_response_request_failure_invalid_data'
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        for data in datas:
            response=eventsapi.event_response_request(username=username, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IDAT)

    def test_event_response_request_failure_user_not_found(self):
        ''' event_response_request should fail if username is not found '''
        username='test_event_response_request_failure_username_not_found'
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GUA_GUID_UNF)

    def test_event_response_request_failure_sequence_not_found(self):
        ''' event_response_request should fail if sequence is not found '''
        username=self.userinfo['username']
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_GEV_EVNF)

    def test_event_response_request_failure_no_missing_parameter_found(self):
        ''' event_response_request should fail if no missing parameter is found '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_no_missing_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSF)

    def test_event_response_request_failure_invalid_missing_parameter_type(self):
        ''' event_response_request should fail if no missing parameter is found '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_invalid_missing_parameter_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':23234}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSF)

    def test_event_response_request_failure_no_identified_parameter_found(self):
        ''' event_response_request should fail if no missing parameter is found '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_noidentified_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[]}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDF)

    def test_event_response_request_failure_invalid_identified_parameter_type(self):
        ''' event_response_request should fail if no identified parameter is found '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_invalid_identified_parameter_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[],'identified':23234}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDF)

    def test_event_response_request_failure_invalid_missing_item(self):
        ''' event_response_request should fail if missing items are invalid '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_invalid_missing_item'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[uuid.uuid4()], 'identified':[]}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSIT)

    def test_event_response_request_failure_invalid_identified_item(self):
        ''' event_response_request should fail if identified items are invalid '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_invalid_identified_item'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename='test_event_response_request_failure_invalid_identified_item'
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[],'identified':[uuid.uuid4()]}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDIT)

    def test_event_response_request_failure_non_supported_event_type(self):
        ''' event_response_request should succeed and send message '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_failure_non_supported_event_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':agent['aid'].hex}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IEVT)

    def test_event_response_request_success_message_sent(self):
        ''' event_response_request should succeed and send message '''
        username=self.userinfo['username']
        uid=uuid.UUID(self.userinfo['uid'])
        agentname='test_event_response_request_success_message_sent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=uid, aid=agent['aid'],datasourcename=datasourcename)
        self.assertIsNotNone(datasource)
        content='content'
        date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'],date=date,content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        did=datasource['did']
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        doubts=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        discarded=[uuid.uuid4().hex, uuid.uuid4().hex, ]
        parameters={'did':did.hex, 'date':date.hex, 'doubts':doubts, 'discarded':discarded}
        new_event=usereventsapi.new_event(uid=uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        missing_pid=uuid.uuid4()
        identified_entry={'pid':uuid.uuid4().hex,'p':23,'l':2}
        data={'missing':[missing_pid.hex],'identified':[identified_entry]}
        response=eventsapi.event_response_request(username=username, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.USER_EVENT_RESPONSE_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                self.assertEqual(msg.uid, uid)
                self.assertEqual(msg.date, new_event['date'])
            else:
                break

