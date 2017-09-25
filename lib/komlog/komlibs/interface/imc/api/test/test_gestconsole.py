import unittest
import uuid
import json
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.interface.imc.api import gestconsole
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.graph.relations import vertex
from komlog.komcass.api import datapoint as cassapidatapoint


pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

class InterfaceImcApiGestconsoleTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.gestconsole tests '''

    def test_process_message_MONVAR_failure_non_existent_did(self):
        ''' process_message_MONVAR should fail if did does not exists '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_process_message_monvar_failure_invalid_uid_datapointname'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages, {'routed':{},'unrouted':[]})

    def test_process_message_MONVAR_success_datapoint_did_not_exist_previously(self):
        ''' process_message_MONVAR should succeed and generate all necesary messages if the datapoint did not exist previously'''
        username='test_process_message_monvar_success_datapoint_did_not_exist_previously'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='content: 23'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=9
        length=2
        datapoint_uri='datapoint_uri'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))

    def test_process_message_MONVAR_success_ds_had_already_others_datapoints(self):
        ''' process_message_MONVAR should succeed and generate all necesary messages if others datapoint already existed previously'''
        username='test_process_message_monvar_success_ds_had_already_others_datapoints'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        #now monitor a new datapoint associated to the same did
        position=10
        length=2
        datapoint_uri='datapoint_y'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        #the main change is that two FILLDP messages are generated
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))

    def test_process_message_MONVAR_failure_message_requested_twice(self):
        ''' process_message_MONVAR should fail if message is requested twice '''
        username='test_process_message_monvar_failure_message_requested_twice'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        # it does not have to fail, because it belongs to the same ds, we consider this message as a POSVAR
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertTrue(len(response.imc_messages['unrouted']) == 2)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
        }

    def test_process_message_NEGVAR_failure_non_existent_datapoint(self):
        ''' process_message_NEGVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.NegativeVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_NEGVAR_success(self):
        ''' process_message_NEGVAR should succeed '''
        username='test_process_message_negvar_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        pid = None
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            if msg._type_ == messages.Messages.NEW_DP_WIDGET_MESSAGE:
                pid = msg.pid
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        message=messages.NegativeVariableMessage(pid=pid, date=ds_date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.NEG_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_NEGVAR_success_requested_twice(self):
        ''' process_message_NEGVAR should succeed, and if requested twice, dont request FILLDP if no new info is added '''
        username='test_process_message_negvar_success_requested_twice'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        pid = None
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            if msg._type_ == messages.Messages.NEW_DP_WIDGET_MESSAGE:
                pid = msg.pid
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        message=messages.NegativeVariableMessage(pid=pid, date=ds_date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.NEG_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        message=messages.NegativeVariableMessage(pid=pid, date=ds_date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.NEG_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_POSVAR_failure_non_existent_datapoint(self):
        ''' process_message_POSVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.PositiveVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_POSVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_POSVAR_success_requested_twice(self):
        ''' process_message_POSVAR should succeed, and if requested twice, dont request FILLDP if no new info is added '''
        username='test_process_message_posvar_success_requested_twice'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        pid = None
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            if msg._type_ == messages.Messages.NEW_DP_WIDGET_MESSAGE:
                pid = msg.pid
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        message=messages.PositiveVariableMessage(pid=pid, date=ds_date, position=position, length=length)
        #in this case, launching posvar after monvar is the same as launching posvar twice
        response=gestconsole.process_message_POSVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.POS_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_POSVAR_error_in_positive_identification(self):
        ''' process_message_POSVAR should realize the dtree could not be generated '''
        username='test_process_message_posvar_error_in_positive_identification'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='datapoint_x'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=ds_date, position=position, length=length, datapointname=datapoint_uri)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.MON_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 5)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.name:1,
            messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE.name:1,
            messages.Messages.USER_EVENT_MESSAGE.name:1,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.name:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.name:1,
        }
        retrieved_messages={}
        pid = None
        msgs=response.imc_messages['unrouted']
        for msg in msgs:
            if msg._type_ == messages.Messages.NEW_DP_WIDGET_MESSAGE:
                pid = msg.pid
            try:
                retrieved_messages[msg._type_.name]+=1
            except KeyError:
                retrieved_messages[msg._type_.name]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        #in this case, we say x datapoint is 45, introducing an error
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=10
        length=2
        message=messages.PositiveVariableMessage(pid=pid, date=ds_date, position=position, length=length)
        response=gestconsole.process_message_POSVAR(message=message)
        pid_stats = cassapidatapoint.get_datapoint_stats(pid=pid)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.POS_VAR_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        #in the future a new message will be generated to analize the error and generate a notification for the user to be able to identify again the right variable
        self.assertEqual(len(response.imc_messages['unrouted']), 1)
        self.assertEqual(response.imc_messages['unrouted'][0]._type_, messages.Messages.USER_EVENT_MESSAGE)

    def test_process_message_NEWDSW_failure_non_existent_user(self):
        ''' process_message_NEWDSW should fail if user does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        message=messages.NewDSWidgetMessage(uid=uid, did=did)
        response=gestconsole.process_message_NEWDSW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_NEWDPW_failure_non_existent_user(self):
        ''' process_message_NEWDPW should fail if user does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        message=messages.NewDPWidgetMessage(uid=uid, pid=pid)
        response=gestconsole.process_message_NEWDPW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELUSER_failure_non_existent_user(self):
        ''' process_message_DELUSER should fail if user does not exist '''
        uid=uuid.uuid4()
        message=messages.DeleteUserMessage(uid=uid)
        response=gestconsole.process_message_DELUSER(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELAGENT_failure_non_existent_agent(self):
        ''' process_message_DELAGENT should fail if agent does not exist '''
        aid=uuid.uuid4()
        message=messages.DeleteAgentMessage(aid=aid)
        response=gestconsole.process_message_DELAGENT(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELAGENT_success(self):
        ''' process_message_DELAGENT should succeed if agent exists '''
        username='test_process_message_delagent_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delagent_success'
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        message=messages.DeleteAgentMessage(aid=aid)
        response=gestconsole.process_message_DELAGENT(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDS_failure_non_existent_datasource(self):
        ''' process_message_DELDS should fail if datasource does not exist '''
        did=uuid.uuid4()
        message=messages.DeleteDatasourceMessage(did=did)
        response=gestconsole.process_message_DELDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDS_success(self):
        ''' process_message_DELDS should succeed if datasource exists '''
        username='test_process_message_delds_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delds_success'
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename=username
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=aid,datasourcename=datasourcename)
        message=messages.DeleteDatasourceMessage(did=datasource['did'])
        response=gestconsole.process_message_DELDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDP_failure_non_existent_datapoint(self):
        ''' process_message_DELDP should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        message=messages.DeleteDatapointMessage(pid=pid)
        response=gestconsole.process_message_DELDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDP_success(self):
        ''' process_message_DELDP should succeed if datapoint exists '''
        username='test_process_message_deldp_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delds_success'
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename=username
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=aid,datasourcename=datasourcename)
        datapointname=username
        datapoint=datapointapi.create_datasource_datapoint(did=datasource['did'],datapoint_uri=datapointname)
        message=messages.DeleteDatapointMessage(pid=datapoint['pid'])
        response=gestconsole.process_message_DELDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        self.assertEqual(response.imc_messages['unrouted'][0].operation,Operations.DELETE_DATASOURCE_DATAPOINT)
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDP_success_user_datapoint(self):
        ''' process_message_DELDP should succeed if datapoint exists and is a user datapoint '''
        username='test_process_message_deldp_user_dp_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapointname='user.datapoint.delete.success'
        datapoint=datapointapi.create_user_datapoint(uid=user['uid'],datapoint_uri=datapointname)
        self.assertIsNotNone(datapoint)
        message=messages.DeleteDatapointMessage(pid=datapoint['pid'])
        response=gestconsole.process_message_DELDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        self.assertEqual(response.imc_messages['unrouted'][0].operation,Operations.DELETE_USER_DATAPOINT)
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELWIDGET_failure_non_existent_widget(self):
        ''' process_message_DELWIDGET should fail if widget does not exist '''
        wid=uuid.uuid4()
        message=messages.DeleteWidgetMessage(wid=wid)
        response=gestconsole.process_message_DELWIDGET(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELWIDGET_success(self):
        ''' process_message_DELAWIDGET should succeed if widget exists '''
        username='test_process_message_delwidget_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        widgetname=username
        widget=widgetapi.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        message=messages.DeleteWidgetMessage(wid=widget['wid'])
        response=gestconsole.process_message_DELWIDGET(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDASHB_failure_non_existent_dashboard(self):
        ''' process_message_DELDASHB should fail if dashboard does not exist '''
        bid=uuid.uuid4()
        message=messages.DeleteDashboardMessage(bid=bid)
        response=gestconsole.process_message_DELDASHB(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(response.imc_messages['routed'],{})

    def test_process_message_DELDASHB_success(self):
        ''' process_message_DELDASHB should succeed if widget exists '''
        username='test_process_message_deldashboard_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        dashboardname=username
        dashboard=dashboardapi.create_dashboard(uid=user['uid'],dashboardname=dashboardname)
        message=messages.DeleteDashboardMessage(bid=dashboard['bid'])
        response=gestconsole.process_message_DELDASHB(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['routed'],{})
        response=rescontrol.process_message_UPDQUO(response.imc_messages['unrouted'][0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

