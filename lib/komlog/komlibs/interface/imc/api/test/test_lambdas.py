import unittest
import uuid
import json
from komlog.komlibs.auth import session
from komlog.komlibs.auth.resources import update as resupdate
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.errors import Errors as AuthErrors
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.web.model import operation
from komlog.komlibs.interface.imc.api import lambdas
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors as WSErrors
from komlog.komlibs.interface.websocket import session as ws_session
from komlog.komlibs.interface.websocket.protocol.v1.model import message as ws_message


class InterfaceImcApiLambdasTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.lambdas tests '''

    def test_process_message_URISUPDT_success_no_uris_updated(self):
        ''' process_message_URISUPDT should succeed if there is no uri updated '''
        uris=[]
        date=timeuuid.uuid1()
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_no_existing_uris_updated(self):
        ''' process_message_URISUPDT should succeed but ignore unexisting uris '''
        uris=[
            {'uri':'unexistent.uri1_urisupdt','type':vertex.DATASOURCE,'id':uuid.uuid4()},
            {'uri':'unexistent.uri2_urisupdt','type':vertex.DATAPOINT,'id':uuid.uuid4()},
        ]
        date=timeuuid.uuid1()
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_uris_existed_but_no_data(self):
        ''' process_message_URISUPDT should succeed but ignore existing uris without data '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_data'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=timeuuid.uuid1()
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_uris_existed_but_no_data_at_this_date(self):
        ''' process_message_URISUPDT should succeed but ignore existing uris without data '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_data_at_date'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=timeuuid.uuid1()
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_no_session_hooked(self):
        ''' process_message_URISUPDT should succeed if there is no session hooked to the elements updated '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_session_hooked'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=timeuuid.uuid1()
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_session(self):
        ''' process_message_URISUPDT should succeed but ignore non existing sessions, and request a message to clear the non existent sessions hooks '''
        username='test_process_message_urisupdt_success_uris_existed_but_session'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        non_existent_sid=uuid.uuid4()
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=non_existent_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=non_existent_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        generated_message=messages.ClearSessionHooksMessage(sid=non_existent_sid,ids=[(pid,vertex.DATAPOINT),(did,vertex.DATASOURCE)])
        response=lambdas.process_message_URISUPDT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertNotEqual(response.unrouted_messages, [])
        self.assertTrue(len(response.unrouted_messages) == 1)
        self.assertEqual(response.unrouted_messages[0].type, messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(response.unrouted_messages[0].ids), sorted(generated_message.ids))

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_session_expired(self):
        ''' process_message_URISUPDT should succeed but ignore expired sessions, and proceed to delete them '''
        username='test_process_message_urisupdt_success_uris_existed_but_session_expired'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        expired_sid=uuid.uuid4()
        expired_session=ormagent.AgentSession(
            sid=expired_sid,
            aid=None, 
            uid=None,
            imc_address=None,
            last_update=timeuuid.uuid1(seconds=1)
        )
        self.assertTrue(cassapiagent.insert_agent_session(expired_session))
        session_info=session.get_agent_session_info(sid=expired_session.sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, expired_sid)
        self.assertEqual(session_info.aid, None)
        self.assertEqual(session_info.uid, None)
        self.assertEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=expired_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=expired_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        with self.assertRaises(authexcept.SessionNotFoundException) as cm:
            session.get_agent_session_info(sid=expired_session.sid)
        self.assertEqual(cm.exception.error, AuthErrors.E_AS_GASI_SNF)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_session_unassociated_but_not_expired_yet(self):
        ''' process_message_URISUPDT should succeed but ignore unassociated sessions.
            In this case, we should not send any update because there is no session associated
            and because the session has not expired yet, we should not delete it yet.
            We cannot request the hooks clear because session exists yet '''
        username='test_process_message_urisupdt_success_uris_existed_but_session_unassociated_but_not_expired_yet'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        unassociated_sid=uuid.uuid4()
        unassociated_session=ormagent.AgentSession(
            sid=unassociated_sid,
            aid=None, 
            uid=None,
            imc_address=None,
            last_update=timeuuid.uuid1()
        )
        self.assertTrue(cassapiagent.insert_agent_session(unassociated_session))
        session_info=session.get_agent_session_info(sid=unassociated_session.sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, unassociated_sid)
        self.assertEqual(session_info.aid, None)
        self.assertEqual(session_info.uid, None)
        self.assertEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=unassociated_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=unassociated_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info=session.get_agent_session_info(sid=unassociated_session.sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_URISUPDT_failure_uris_and_data_existed_but_no_permission(self):
        ''' process_message_URISUPDT should fail if user has no permission over elements '''
        username='test_process_message_urisupdt_failure_uris_existed_but_no_permission'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid)
        self.assertEqual(session_info.uid,uid)
        self.assertNotEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        data=[
            {'uri':datasource_uri,'content':ds_content},
            {'uri':datapoint_uri,'content':dp_content},
        ]
        generated_message=messages.SendSessionDataMessage(sid=associated_sid, data=data, date=date)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_ds(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_ds'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid)
        self.assertEqual(session_info.uid,uid)
        self.assertNotEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        data=[
            {'uri':datasource_uri,'content':ds_content},
            {'uri':datapoint_uri,'content':dp_content},
        ]
        generated_message=messages.SendSessionDataMessage(sid=associated_sid, data=data, date=date)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertNotEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        self.assertTrue(session_info.imc_address in response.routed_messages)
        self.assertTrue(len(response.routed_messages[session_info.imc_address]) == 1)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].sid, associated_sid)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].date,date)
        expected_data=[
            {'uri':datasource_uri,'content':ds_content},
        ]
        recv_data=response.routed_messages[session_info.imc_address][0].data
        pairs = zip(sorted(recv_data, key=lambda x: x['uri']), sorted(expected_data, key=lambda x: x['uri']))
        self.assertFalse(any(x != y for x,y in pairs))

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_dp(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_dp'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid)
        self.assertEqual(session_info.uid,uid)
        self.assertNotEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        data=[
            {'uri':datasource_uri,'content':ds_content},
            {'uri':datapoint_uri,'content':dp_content},
        ]
        generated_message=messages.SendSessionDataMessage(sid=associated_sid, data=data, date=date)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertNotEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        self.assertTrue(session_info.imc_address in response.routed_messages)
        self.assertTrue(len(response.routed_messages[session_info.imc_address]) == 1)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].sid, associated_sid)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].date,date)
        expected_data=[
            {'uri':datapoint_uri,'content':dp_content},
        ]
        recv_data=response.routed_messages[session_info.imc_address][0].data
        pairs = zip(sorted(recv_data, key=lambda x: x['uri']), sorted(expected_data, key=lambda x: x['uri']))
        self.assertFalse(any(x != y for x,y in pairs))

    def test_process_message_URISUPDT_success_uris_and_data_existed_and_session_associated(self):
        ''' process_message_URISUPDT should succeed and generate the corresponding messages
            to notify the agent about the update.
            One SendSessionDataMessage per session will be generated with the associated info.
            '''
        username='test_process_message_urisupdt_success_uris_existed_and_session_associated'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid)
        self.assertEqual(session_info.uid,uid)
        self.assertNotEqual(session_info.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        data=[
            {'uri':datasource_uri,'content':ds_content},
            {'uri':datapoint_uri,'content':dp_content},
        ]
        generated_message=messages.SendSessionDataMessage(sid=associated_sid, data=data, date=date)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertNotEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        self.assertTrue(session_info.imc_address in response.routed_messages)
        self.assertTrue(len(response.routed_messages[session_info.imc_address]) == 1)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].sid, associated_sid)
        self.assertEqual(response.routed_messages[session_info.imc_address][0].date,date)
        recv_data=response.routed_messages[session_info.imc_address][0].data
        pairs = zip(sorted(recv_data, key=lambda x: x['uri']), sorted(data, key=lambda x: x['uri']))
        self.assertFalse(any(x != y for x,y in pairs))

    def test_process_message_URISUPDT_success_uris_and_data_existed_and_sessions_associated(self):
        ''' process_message_URISUPDT should succeed and generate the corresponding messages
            to notify the agents about the update.
            One SendSessionDataMessage per session will be generated with the associated info.
            '''
        username='test_process_message_urisupdt_success_uris_existed_and_sessions_associated'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid1=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid1, aid=aid, uid=uid))
        session_info1=session.get_agent_session_info(sid=associated_sid1)
        self.assertIsNotNone(session_info1)
        self.assertEqual(session_info1.sid, associated_sid1)
        self.assertEqual(session_info1.aid,aid)
        self.assertEqual(session_info1.uid,uid)
        self.assertNotEqual(session_info1.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid1))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid1))
        associated_sid2=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid2, aid=aid, uid=uid))
        session_info2=session.get_agent_session_info(sid=associated_sid2)
        self.assertIsNotNone(session_info2)
        self.assertEqual(session_info2.sid, associated_sid2)
        self.assertEqual(session_info2.aid,aid)
        self.assertEqual(session_info2.uid,uid)
        self.assertNotEqual(session_info2.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid2))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid2))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        session_info1=session.get_agent_session_info(sid=associated_sid1)
        self.assertIsNotNone(session_info1)
        session_info2=session.get_agent_session_info(sid=associated_sid2)
        self.assertIsNotNone(session_info2)
        data=[
            {'uri':datasource_uri,'content':ds_content},
            {'uri':datapoint_uri,'content':dp_content},
        ]
        generated_messages=[
            messages.SendSessionDataMessage(sid=associated_sid1, data=data, date=date),
            messages.SendSessionDataMessage(sid=associated_sid2, data=data, date=date)
        ]
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertNotEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        self.assertTrue(session_info1.imc_address in response.routed_messages)
        self.assertTrue(len(response.routed_messages[session_info1.imc_address]) == 2)
        self.assertEqual(response.routed_messages[session_info1.imc_address][0].type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(response.routed_messages[session_info1.imc_address][0].sid in (associated_sid1, associated_sid2))
        self.assertEqual(response.routed_messages[session_info1.imc_address][0].date,date)
        recv_data=response.routed_messages[session_info1.imc_address][0].data
        pairs = zip(sorted(recv_data, key=lambda x: x['uri']), sorted(data, key=lambda x: x['uri']))
        self.assertFalse(any(x != y for x,y in pairs))
        self.assertEqual(response.routed_messages[session_info1.imc_address][1].type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(response.routed_messages[session_info1.imc_address][1].sid in (associated_sid1, associated_sid2))
        self.assertNotEqual(response.routed_messages[session_info1.imc_address][0].sid,response.routed_messages[session_info1.imc_address][1].sid)
        self.assertEqual(response.routed_messages[session_info1.imc_address][1].date,date)
        recv_data=response.routed_messages[session_info1.imc_address][1].data
        pairs = zip(sorted(recv_data, key=lambda x: x['uri']), sorted(data, key=lambda x: x['uri']))
        self.assertFalse(any(x != y for x,y in pairs))

    def test_process_message_CLSHOOKS_success_no_items(self):
        ''' process_message_CLSHOOKS should succeed if there is no item to clear '''
        sid=uuid.uuid4()
        ids=[]
        message=messages.ClearSessionHooksMessage(sid=sid, ids=ids)
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_CLSHOOKS_success_non_existing_items(self):
        ''' process_message_CLSHOOKS should succeed if there is no item to clear '''
        sid=uuid.uuid4()
        ids=[(uuid.uuid4(), vertex.DATASOURCE),(uuid.uuid4(), vertex.DATAPOINT)]
        message=messages.ClearSessionHooksMessage(sid=sid, ids=ids)
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_CLSHOOKS_success_items_exist(self):
        ''' process_message_CLSHOOKS should succeed and delete element hooks '''
        username='test_process_message_clshooks_success_items_exist'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        associated_sid1=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid1, aid=aid, uid=uid))
        session_info1=session.get_agent_session_info(sid=associated_sid1)
        self.assertIsNotNone(session_info1)
        self.assertEqual(session_info1.sid, associated_sid1)
        self.assertEqual(session_info1.aid,aid)
        self.assertEqual(session_info1.uid,uid)
        self.assertNotEqual(session_info1.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid1))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid1))
        associated_sid2=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid2, aid=aid, uid=uid))
        session_info2=session.get_agent_session_info(sid=associated_sid2)
        self.assertIsNotNone(session_info2)
        self.assertEqual(session_info2.sid, associated_sid2)
        self.assertEqual(session_info2.aid,aid)
        self.assertEqual(session_info2.uid,uid)
        self.assertNotEqual(session_info2.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid2))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid2))
        dp_hooks=datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(sorted(dp_hooks), sorted([associated_sid1,associated_sid2]))
        ds_hooks=datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(sorted(ds_hooks), sorted([associated_sid1,associated_sid2]))
        message=messages.ClearSessionHooksMessage(sid=associated_sid1, ids=[(pid,vertex.DATAPOINT),(did,vertex.DATASOURCE)])
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        dp_hooks=datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(dp_hooks, [associated_sid2])
        ds_hooks=datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(ds_hooks, [associated_sid2])
        message=messages.ClearSessionHooksMessage(sid=associated_sid2, ids=[(pid,vertex.DATAPOINT),(did,vertex.DATASOURCE)])
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        dp_hooks=datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(dp_hooks, [])
        ds_hooks=datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(ds_hooks, [])

    def test_process_message_SSDATA_failure_non_existing_session(self):
        ''' process_message_SSDATA should fail if sid is not associated to this module '''
        sid=uuid.uuid4()
        date=uuid.uuid1()
        data=[{'uri':'uri','content':'content'},{'uri':'uri2','content':'content2'}]
        message=messages.SendSessionDataMessage(sid=sid, date=date, data=data)
        response=lambdas.process_message_SSDATA(message=message)
        self.assertEqual(response.error, Errors.E_IIATM_SSDT_SNF)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])

    def test_process_message_SSDATA_success(self):
        ''' process_message_SSDATA should succeed '''
        sid=uuid.uuid4()
        date=uuid.uuid1()
        data=[{'uri':'uri','content':'content'},{'uri':'uri2','content':'content2'}]
        message=messages.SendSessionDataMessage(sid=sid, date=date, data=data)
        class FakeWSSession:
            def __init__(self):
                self.response_json=None

            def write_message(self, msg):
                self.response_json=json.dumps(msg)
                return
        ws_session.agent_callback[message.sid]=FakeWSSession()
        response=lambdas.process_message_SSDATA(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.message_params, message.serialized_message)
        self.assertEqual(response.routed_messages, {})
        self.assertEqual(response.unrouted_messages, [])
        expected_msg=ws_message.SendMultiData(ts=timeuuid.get_unix_timestamp(date),uris=data)
        self.assertEqual(ws_session.agent_callback[message.sid].response_json, json.dumps(expected_msg.to_dict()))

