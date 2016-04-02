import unittest
import uuid
import json
from komlog.komlibs.auth import operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth import errors as autherrors
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import events as eventsapi
from komlog.komlibs.interface.web.model import webmodel
from komlog.komlibs.interface.web import status, exceptions, errors
from komlog.komlibs.events import errors as eventerrors
from komlog.komlibs.events.model import types
from komlog.komlibs.events.api import user as usereventsapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount import errors as gesterrors
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.interface.imc.model import messages
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komlibs.general.time import timeuuid


class InterfaceWebApiEventsTest(unittest.TestCase):
    ''' komlibs.interface.web.api.events tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        self.username = 'test_komlibs.interface.web.api.events_user'
        self.password = 'password'
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
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
        response, cookie = loginapi.login_request(username=self.username, password=self.password)
        self.passport = passport.get_user_passport(cookie)

    def test_get_user_events_request_failure_invalid_passport(self):
        ''' get_user_events_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=eventsapi.get_user_events_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_invalid_ets(self):
        ''' get_user_events_request should fail if ets is invalid '''
        etss=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for ets in etss:
            response=eventsapi.get_user_events_request(passport=psp, ets=ets)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_invalid_its(self):
        ''' get_user_events_request should fail if its is invalid '''
        itss=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for its in itss:
            response=eventsapi.get_user_events_request(passport=psp, its=its)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_user_events_request_failure_user_not_found(self):
        ''' get_user_events_request should fail if username is not found '''
        psp = passport.Passport(uid=uuid.uuid4())
        response=eventsapi.get_user_events_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, [])

    def test_get_user_events_request_success(self):
        ''' get_users_circles_config_request should succeed '''
        psp = self.passport
        response=eventsapi.get_user_events_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(len(response.data)>=1)
        self.assertTrue('ts' in response.data[0])
        self.assertTrue('type' in response.data[0])
        self.assertTrue('priority' in response.data[0])
        self.assertTrue('seq' in response.data[0])
        self.assertTrue('params' in response.data[0])
        self.assertTrue('html' in response.data[0])

    def test_disable_event_request_failure_invalid_passport(self):
        ''' disable_event_request should fail if passport is invalid'''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        seq=20*'A'
        for psp in passports:
            response=eventsapi.disable_event_request(passport=psp, seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_DEVR_IPSP)

    def test_disable_event_request_failure_invalid_sequence(self):
        ''' disable_event_request should fail if sequence is invalid'''
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for seq in seqs:
            response=eventsapi.disable_event_request(passport=psp, seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_DEVR_ISEQ)

    def test_disable_event_request_failure_user_not_found(self):
        ''' disable_event_request should fail if username is not found '''
        psp = passport.Passport(uid=uuid.uuid4())
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        response=eventsapi.disable_event_request(passport=psp, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_DISE_EVNF)

    def test_disable_event_request_failure_sequence_not_found(self):
        ''' disable_event_request should fail if sequence is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        response=eventsapi.disable_event_request(passport=psp, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_DISE_EVNF)

    def test_event_response_request_failure_invalid_passport(self):
        ''' event_response_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data=dict()
        for psp in passports:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IPSP)

    def test_event_response_request_failure_invalid_sequence(self):
        ''' event_response_request should fail if sequence is invalid '''
        psp = self.passport
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        data=dict()
        for seq in seqs:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_ISEQ)

    def test_event_response_request_failure_invalid_data(self):
        ''' event_response_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        for data in datas:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IDAT)

    def test_event_response_request_failure_user_not_found(self):
        ''' event_response_request should fail if username is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_GEV_EVNF)

    def test_event_response_request_failure_sequence_not_found(self):
        ''' event_response_request should fail if sequence is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_GEV_EVNF)

    def test_event_response_request_failure_no_missing_parameter_found(self):
        ''' event_response_request should fail if no missing parameter is found '''
        psp = self.passport
        agentname='test_event_response_request_failure_no_missing_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSF)

    def test_event_response_request_failure_invalid_missing_parameter_type(self):
        ''' event_response_request should fail if no missing parameter is found '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_missing_parameter_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':23234}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSF)

    def test_event_response_request_failure_no_identified_parameter_found(self):
        ''' event_response_request should fail if no missing parameter is found '''
        psp = self.passport
        agentname='test_event_response_request_failure_noidentified_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDF)

    def test_event_response_request_failure_invalid_identified_parameter_type(self):
        ''' event_response_request should fail if no identified parameter is found '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_parameter_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[],'identified':23234}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDF)

    def test_event_response_request_failure_invalid_missing_item(self):
        ''' event_response_request should fail if missing items are invalid '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_missing_item'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[uuid.uuid4()], 'identified':[]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IMSIT)

    def test_event_response_request_failure_invalid_identified_item(self):
        ''' event_response_request should fail if identified items are invalid '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename='test_event_response_request_failure_invalid_identified_item'
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'missing':[],'identified':[uuid.uuid4()]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IIDIT)

    def test_event_response_request_failure_non_supported_event_type(self):
        ''' event_response_request should succeed and send message '''
        psp = self.passport
        agentname='test_event_response_request_failure_non_supported_event_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        event_type=types.USER_EVENT_NOTIFICATION_NEW_AGENT
        parameters={'aid':agent['aid'].hex}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, errors.E_IWAEV_EVRPR_IEVT)

    def test_event_response_request_success_message_sent(self):
        ''' event_response_request should succeed and send message '''
        psp = self.passport
        agentname='test_event_response_request_success_message_sent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        psp_agent = passport.get_agent_passport({'user':self.username,'aid':agent['aid'].hex,'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())})
        datasource=datasourceapi.create_datasource(uid=psp.uid,aid=agent['aid'],datasourcename=datasourcename)
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
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        missing_pid=uuid.uuid4()
        identified_entry={'pid':uuid.uuid4().hex,'p':23,'l':2}
        data={'missing':[missing_pid.hex],'identified':[identified_entry]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.USER_EVENT_RESPONSE_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                self.assertEqual(msg.uid, psp.uid)
                self.assertEqual(msg.date, new_event['date'])
            else:
                break

