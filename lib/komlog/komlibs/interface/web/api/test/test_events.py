import unittest
import uuid
import json
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import events as eventsapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.events.errors import Errors as eventerrors
from komlog.komlibs.events.model import types
from komlog.komlibs.events.api import user as usereventsapi
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komlibs.general.time import timeuuid


class InterfaceWebApiEventsTest(unittest.TestCase):
    ''' komlibs.interface.web.api.events tests '''

    def setUp(self):
        ''' In this module, we need a user '''
        self.username = 'test_komlibs.interface.web.api.events_user'
        self.password = 'password'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
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
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
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
            self.assertEqual(response.error, Errors.E_IWAEV_DEVR_IPSP.value)

    def test_disable_event_request_failure_invalid_sequence(self):
        ''' disable_event_request should fail if sequence is invalid'''
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        for seq in seqs:
            response=eventsapi.disable_event_request(passport=psp, seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAEV_DEVR_ISEQ.value)

    def test_disable_event_request_failure_user_not_found(self):
        ''' disable_event_request should fail if username is not found '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        response=eventsapi.disable_event_request(passport=psp, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_DISE_EVNF.value)

    def test_disable_event_request_failure_sequence_not_found(self):
        ''' disable_event_request should fail if sequence is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        response=eventsapi.disable_event_request(passport=psp, seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_DISE_EVNF.value)

    def test_event_response_request_failure_invalid_passport(self):
        ''' event_response_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data=dict()
        for psp in passports:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IPSP.value)

    def test_event_response_request_failure_invalid_sequence(self):
        ''' event_response_request should fail if sequence is invalid '''
        psp = self.passport
        seqs=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        data=dict()
        for seq in seqs:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_ISEQ.value)

    def test_event_response_request_failure_invalid_data(self):
        ''' event_response_request should fail if data is invalid '''
        datas=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame']
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        for data in datas:
            response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IDAT.value)

    def test_event_response_request_failure_user_not_found(self):
        ''' event_response_request should fail if username is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_GEV_EVNF.value)

    def test_event_response_request_failure_sequence_not_found(self):
        ''' event_response_request should fail if sequence is not found '''
        psp = self.passport
        seq=timeuuid.get_custom_sequence(uuid.uuid1())
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, eventerrors.E_EAU_GEV_EVNF.value)

    def test_event_response_request_failure_invalid_event_type(self):
        ''' event_response_request should fail if event type responses are not supported '''
        psp = self.passport
        event_type=types.USER_EVENT_NOTIFICATION_NEW_USER
        parameters = {}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IEVT.value)

    def test_event_response_request_failure_no_identified_parameter_found(self):
        ''' event_response_request should fail if no identified parameter is found '''
        psp = self.passport
        agentname='test_event_response_request_failure_noidentified_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'no_identified':[]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDF.value)

    def test_event_response_request_failure_invalid_identified_parameter_found(self):
        ''' event_response_request should fail if identified parameter type is invalid '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_parameter_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':{}}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDF.value)

    def test_event_response_request_failure_invalid_identified_item_type(self):
        ''' event_response_request should fail if identified parameter item type is invalid '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_type'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[1]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_p_not_found(self):
        ''' event_response_request should fail if identified parameter item has no p param '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_p_not_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'ap':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_p_invalid(self):
        ''' event_response_request should fail if identified parameter item has no p param '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_p_invalid'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'ap':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_l_not_found(self):
        ''' event_response_request should fail if identified parameter item has no p param '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_l_not_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'ap':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_l_invalid(self):
        ''' event_response_request should fail if identified parameter item has invalid l '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_l_invalid'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'ap':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_s_not_found(self):
        ''' event_response_request should fail if identified parameter item has no s param '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_s_not_found'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'ap':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_failure_invalid_identified_item_s_invalid(self):
        ''' event_response_request should fail if identified parameter item has invalid s param '''
        psp = self.passport
        agentname='test_event_response_request_failure_invalid_identified_item_s_invalid'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':date,'l':1,'p':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAEV_EVRPR_IIDIT.value)

    def test_event_response_request_success_message_generated(self):
        ''' event_response_request should succeed and generate the imc message '''
        psp = self.passport
        agentname='test_event_response_request_success_message_generated'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='version'
        agent=agentapi.create_agent(uid=psp.uid, agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        datasourcename=agentname
        datasource=datasourceapi.create_datasource(uid=psp.uid, aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='x = 1'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=4
        length=1
        datapointname='x'
        datapoint1=datapointapi.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(datapointapi.store_datapoint_values(pid=datapoint1['pid'], date=date))
        pid = datapoint1['pid']
        dates=[date.hex]
        event_type=types.USER_EVENT_INTERVENTION_DATAPOINT_IDENTIFICATION
        parameters={'did':did.hex, 'pid':pid.hex, 'dates':dates}
        new_event=usereventsapi.new_event(uid=psp.uid, event_type=event_type, parameters=parameters)
        self.assertIsNotNone(new_event)
        seq=timeuuid.get_custom_sequence(new_event['date'])
        data={'identified':[{'s':timeuuid.get_custom_sequence(date),'l':1,'p':4}]}
        response=eventsapi.event_response_request(passport=psp, seq=seq, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        self.assertEqual(response.error, Errors.OK.value)
        self.assertEqual(len(response.unrouted_messages),1)
        self.assertEqual(response.unrouted_messages[0]._type_,messages.Messages.USER_EVENT_RESPONSE_MESSAGE)
        self.assertEqual(response.unrouted_messages[0].parameters,{'identified':data['identified']})
        msgresponse=msgapi.process_message(response.unrouted_messages[0])
        self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)

