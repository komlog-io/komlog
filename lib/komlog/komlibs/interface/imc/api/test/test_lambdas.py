import unittest
import uuid
import json
from komlog.komlibs.auth import session
from komlog.komlibs.auth.resources import update as resupdate
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth import permissions
from komlog.komlibs.auth.errors import Errors as AuthErrors
from komlog.komlibs.auth.model import interfaces
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import permission as cassapiperm
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.common import delete as deleteapi
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.web.model import operation
from komlog.komlibs.interface.imc.api import lambdas
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.interface.websocket import session as ws_session
from komlog.komlibs.interface.websocket.protocol.v1.model import message as wsmsgv1


pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_success_uris_existed_but_no_data(self):
        ''' process_message_URISUPDT should succeed but ignore existing uris without data '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_data'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_success_uris_existed_but_no_data_at_this_date(self):
        ''' process_message_URISUPDT should succeed but ignore existing uris without data '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_data_at_date'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_no_session_hooked(self):
        ''' process_message_URISUPDT should succeed if there is no session hooked to the elements updated '''
        username='test_process_message_urisupdt_success_uris_existed_but_no_session_hooked'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_session(self):
        ''' process_message_URISUPDT should succeed but ignore non existing sessions, and request a message to clear the non existent sessions hooks '''
        username='test_process_message_urisupdt_success_uris_existed_but_session'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(len(response.imc_messages['unrouted']) == 1)
        self.assertEqual(response.imc_messages['unrouted'][0].type, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(response.imc_messages['unrouted'][0].ids), sorted(generated_message.ids))

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_session_expired(self):
        ''' process_message_URISUPDT should succeed but ignore expired sessions, and proceed to delete them '''
        username='test_process_message_urisupdt_success_uris_existed_but_session_expired'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
            pv=None,
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(len(response.imc_messages['unrouted']), 1)
        self.assertEqual(response.imc_messages['unrouted'][0]._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid, expired_session.sid)
        self.assertEqual(sorted(response.imc_messages['unrouted'][0].ids),sorted([(pid,vertex.DATAPOINT),(did,vertex.DATASOURCE)]))


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
            pv=None,
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
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_failure_uris_and_data_existed_but_no_permission(self):
        ''' process_message_URISUPDT should not generate any SSDATA message if user
            has no permission over uris to retrieve their data '''
        username='test_process_message_urisupdt_failure_uris_existed_but_no_permission'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid,pv=1))
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_failure_uris_and_data_existed_but_no_permission_foreign_uris(self):
        ''' process_message_URISUPDT should not generate any SSDATA message if user
            has no permission over uris to retrieve their data '''
        username='test_process_message_urisupdt_failure_uris_existed_but_no_permission_foreign_uris'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        #self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid,aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid_req)
        self.assertEqual(session_info.uid,uid_req)
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_ds(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_ds'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid,pv=1))
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        expected_data=wsmsgv1.SendMultiData(t=date, uris=[
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'content':ds_content},
        ]).to_dict()
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        expected_data.pop('seq')
        recv_data.pop('seq')
        self.assertEqual(expected_data, recv_data)

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_ds_foreign_uris(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_ds_foreign_uris'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        datasource_uri='uris.datasource'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris.datasource',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid,aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid_req)
        self.assertEqual(session_info.uid,uid_req)
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        expected_data=wsmsgv1.SendMultiData(t=date, uris=[
            {'uri':':'.join((username,datasource_uri)),'type':vertex.DATASOURCE,'content':ds_content},
        ]).to_dict()
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        expected_data.pop('seq')
        recv_data.pop('seq')
        self.assertEqual(expected_data, recv_data)

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_dp(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_dp'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid,pv=1))
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        expected_data=wsmsgv1.SendMultiData(t=date, uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'content':dp_content},
        ]).to_dict()
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        expected_data.pop('seq')
        recv_data.pop('seq')
        self.assertEqual(expected_data, recv_data)

    def test_process_message_URISUPDT_success_uris_and_data_existed_but_permission_only_over_dp_foreign_uris(self):
        ''' process_message_URISUPDT should succeed and generate messages only over elements with permissions '''
        username='test_process_message_urisupdt_success_uris_existed_but_permission_only_over_dp_foreign_uris'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri) 
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        dp_content='23'
        dp_date=timeuuid.uuid1()
        ds_content='content: 23'
        ds_date=dp_date
        self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris.datapoint_uri',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid,aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid_req)
        self.assertEqual(session_info.uid,uid_req)
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
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        expected_data=wsmsgv1.SendMultiData(t=date, uris=[
            {'uri':':'.join((username,datapoint_uri)),'type':vertex.DATAPOINT,'content':dp_content},
        ]).to_dict()
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        expected_data.pop('seq')
        recv_data.pop('seq')
        self.assertEqual(expected_data, recv_data)

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
        self.assertTrue(session.set_agent_session(sid=associated_sid, aid=aid, uid=uid,pv=1))
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
            {'uri':datasource_uri,'type':vertex.DATASOURCE, 'content':ds_content},
            {'uri':datapoint_uri,'type':vertex.DATAPOINT, 'content':dp_content},
        ]
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        self.assertTrue(recv_data['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertTrue(recv_data['payload']['t'],date)
        self.assertEqual(sorted(recv_data['payload']['uris'], key=lambda x: x['uri']),sorted(data, key=lambda x: x['uri']))
        valid_message=wsmsgv1.SendMultiData.load_from_dict(recv_data)

    def test_process_message_URISUPDT_success_uris_and_data_existed_and_session_associated_foreign_uris(self):
        ''' process_message_URISUPDT should succeed and generate the corresponding messages
            to notify the agent about the update.
            One SendSessionDataMessage per session will be generated with the associated info.
            '''
        username='test_process_message_urisupdt_success_uris_existed_and_session_associated_foreign_uris'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='uris.datasource_uri'
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
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        associated_sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid,aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=associated_sid)
        self.assertIsNotNone(session_info)
        self.assertEqual(session_info.sid, associated_sid)
        self.assertEqual(session_info.aid,aid_req)
        self.assertEqual(session_info.uid,uid_req)
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
            {'uri':':'.join((username,datasource_uri)),'type':vertex.DATASOURCE, 'content':ds_content},
            {'uri':':'.join((username,datapoint_uri)),'type':vertex.DATAPOINT, 'content':dp_content},
        ]
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, associated_sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        self.assertTrue(recv_data['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertTrue(recv_data['payload']['t'],date)
        self.assertEqual(sorted(recv_data['payload']['uris'], key=lambda x: x['uri']),sorted(data, key=lambda x: x['uri']))
        valid_message=wsmsgv1.SendMultiData.load_from_dict(recv_data)

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
        self.assertTrue(session.set_agent_session(sid=associated_sid1, aid=aid, uid=uid,pv=1))
        session_info1=session.get_agent_session_info(sid=associated_sid1)
        self.assertIsNotNone(session_info1)
        self.assertEqual(session_info1.sid, associated_sid1)
        self.assertEqual(session_info1.aid,aid)
        self.assertEqual(session_info1.uid,uid)
        self.assertNotEqual(session_info1.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid1))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid1))
        associated_sid2=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid2, aid=aid, uid=uid,pv=1))
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
            {'uri':datasource_uri,'type':vertex.DATASOURCE, 'content':ds_content},
            {'uri':datapoint_uri,'type':vertex.DATAPOINT, 'content':dp_content},
        ]
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info1.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info1.imc_address]) == 2)
        self.assertEqual(response.imc_messages['routed'][session_info1.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info1.imc_address][1].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(response.imc_messages['routed'][session_info1.imc_address][0].sid in (associated_sid1, associated_sid2))
        self.assertTrue(response.imc_messages['routed'][session_info1.imc_address][1].sid in (associated_sid1, associated_sid2))
        self.assertNotEqual(response.imc_messages['routed'][session_info1.imc_address][0].sid,response.imc_messages['routed'][session_info1.imc_address][1].sid)
        msg1=response.imc_messages['routed'][session_info1.imc_address][0].data
        msg2=response.imc_messages['routed'][session_info1.imc_address][1].data
        self.assertEqual(msg1['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertEqual(msg2['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertEqual(msg1['payload']['t'],date.hex)
        self.assertEqual(msg2['payload']['t'],date.hex)
        self.assertEqual(sorted(msg1['payload']['uris'], key=lambda x: x['uri']),sorted(data, key=lambda x: x['uri']))
        self.assertEqual(sorted(msg2['payload']['uris'], key=lambda x: x['uri']),sorted(data, key=lambda x: x['uri']))
        valid_message=wsmsgv1.SendMultiData.load_from_dict(msg1)
        valid_message=wsmsgv1.SendMultiData.load_from_dict(msg2)

    def test_process_message_URISUPDT_success_uris_and_data_existed_and_sessions_associated_foreign_and_own_uris(self):
        ''' process_message_URISUPDT should succeed and generate the corresponding messages
            to notify the agents about the update.
            One SendSessionDataMessage per session will be generated with the associated info.
            '''
        username='test_process_message_urisupdt_success_uris_existed_and_sessions_associated_foreign_and_own_uris'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        datasource_uri='uris.datasource_uri'
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
        username2=username+'_2'
        password='password'
        email=username2+'@komlog.org'
        user2=userapi.create_user(username=username2, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user2['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username2+'_agent'
        version='v'
        agent2=agentapi.create_agent(uid=user2['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid1=user['uid']
        aid1=agent['aid']
        sid_own=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid_own,aid=aid1, uid=uid1,pv=1))
        session_own=session.get_agent_session_info(sid=sid_own)
        self.assertIsNotNone(session_own)
        uid2=user2['uid']
        aid2=agent2['aid']
        sid_foreign=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid_foreign,aid=aid2, uid=uid2,pv=1))
        session_foreign=session.get_agent_session_info(sid=sid_foreign)
        self.assertIsNotNone(session_foreign)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=sid_own))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=sid_own))
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=sid_foreign))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=sid_foreign))
        uris=[
            {'uri':datapoint_uri,'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource_uri,'type':vertex.DATASOURCE,'id':did},
        ]
        date=dp_date
        message=messages.UrisUpdatedMessage(uris=uris, date=date)
        response=lambdas.process_message_URISUPDT(message=message)
        data_own=[
            {'uri':datasource_uri,'type':vertex.DATASOURCE, 'content':ds_content},
            {'uri':datapoint_uri,'type':vertex.DATAPOINT, 'content':dp_content},
        ]
        data_foreign=[
            {'uri':':'.join((username,datasource_uri)),'type':vertex.DATASOURCE,'content':ds_content},
            {'uri':':'.join((username,datapoint_uri)),'type':vertex.DATAPOINT,'content':dp_content},
        ]
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_own.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_own.imc_address]) == 2)
        self.assertEqual(response.imc_messages['routed'][session_own.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_own.imc_address][1].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(response.imc_messages['routed'][session_own.imc_address][0].sid in (sid_own,sid_foreign))
        self.assertTrue(response.imc_messages['routed'][session_own.imc_address][1].sid in (sid_own,sid_foreign))
        self.assertNotEqual(response.imc_messages['routed'][session_own.imc_address][0].sid,response.imc_messages['routed'][session_own.imc_address][1].sid)
        msg_own=response.imc_messages['routed'][session_own.imc_address][0].data if response.imc_messages['routed'][session_own.imc_address][0].sid == sid_own else response.imc_messages['routed'][session_own.imc_address][1].data
        msg_foreign=response.imc_messages['routed'][session_own.imc_address][0].data if response.imc_messages['routed'][session_own.imc_address][0].sid == sid_foreign else response.imc_messages['routed'][session_own.imc_address][1].data
        self.assertEqual(msg_own['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertEqual(msg_foreign['action'],wsmsgv1.SendMultiData._action_.value)
        self.assertEqual(msg_own['payload']['t'],date.hex)
        self.assertEqual(msg_foreign['payload']['t'],date.hex)
        self.assertEqual(sorted(msg_own['payload']['uris'], key=lambda x: x['uri']),sorted(data_own, key=lambda x: x['uri']))
        self.assertEqual(sorted(msg_foreign['payload']['uris'], key=lambda x: x['uri']),sorted(data_foreign, key=lambda x: x['uri']))
        valid_message=wsmsgv1.SendMultiData.load_from_dict(msg_own)
        valid_message=wsmsgv1.SendMultiData.load_from_dict(msg_foreign)

    def test_process_message_HOOKNEW_success_no_new_uris(self):
        ''' process_message_HOOKNEW should succeed if there is no new uri '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_HOOKNEW_success_non_existent_user(self):
        ''' process_message_HOOKNEW should succeed if user does not exist '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'datapoint.uri','type':vertex.DATAPOINT,'id':uuid.uuid4()},
            {'uri':'datasource.uri','type':vertex.DATASOURCE,'id':uuid.uuid4()},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_HOOKNEW_success_uri_exist_but_no_pending_hooks_registered(self):
        ''' process_message_HOOKNEW should succeed if uri exist and no pending hooks existed,
            but no action is requested '''
        username='test_process_message_hooknew_success_uri_exist_but_no_pending_hooks_registered'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasource_uri)
        did=datasource['did']
        date=timeuuid.uuid1()
        uris=[
            {'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_HOOKNEW_success_uri_exist_and_pending_hooks_registered(self):
        ''' process_message_HOOKNEW should succeed if uri exist and pending hooks existed,
            sending a UrisUpdatedMessage for the hooks '''
        username='test_process_message_hooknew_success_uri_exist_and_pending_hooks_registered'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasource_uri)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datapoint['datapointname'],sid=sid))
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datasource['datasourcename'],sid=sid))
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[])
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[])
        date=timeuuid.uuid1()
        uris=[
            {'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(len(response.imc_messages['unrouted']), 1)
        self.assertEqual(response.imc_messages['unrouted'][0].type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(sorted(response.imc_messages['unrouted'][0].uris, key=lambda x: x['uri']), sorted(uris, key=lambda x:x['uri']))
        self.assertEqual(response.imc_messages['unrouted'][0].date, date)
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[])
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[sid])
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[sid])

    def test_process_message_HOOKNEW_success_some_uris_does_not_exist_and_have_pending_hooks(self):
        ''' process_message_HOOKNEW should detect non existent uris with pending hooks,
            by not requesting any accion over them. Every uri in a HookNewUris message should
            exist, but some race conditions could happen that make this situation to consider '''
        username='test_process_message_hooknew_success_some_uri_does_not_exist_and_have_pending_hooks'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasource_uri)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datapoint['datapointname'],sid=sid))
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datasource['datasourcename'],sid=sid))
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[])
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[])
        self.assertTrue(deleteapi.delete_datapoint(pid=pid))
        date=timeuuid.uuid1()
        uris=[
            {'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(len(response.imc_messages['unrouted']), 1)
        self.assertEqual(response.imc_messages['unrouted'][0].type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].uris,[{'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did}])
        self.assertEqual(response.imc_messages['unrouted'][0].date, date)
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[])
        with self.assertRaises(gestexcept.DatapointNotFoundException) as cm:
            datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(cm.exception.error, gesterrors.E_GPA_GDPH_DPNF)
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[sid])

    def test_process_message_HOOKNEW_success_some_uris_does_not_exist_and_have_pending_hooks_ds(self):
        ''' process_message_HOOKNEW should detect non existent uris with pending hooks,
            by not requesting any accion over them. Every uri in a HookNewUris message should
            exist, but some race conditions could happen that make this situation to consider '''
        username='test_process_message_hooknew_success_some_uri_does_not_exist_and_have_pending_hooks_ds'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasource_uri)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datapoint['datapointname'],sid=sid))
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datasource['datasourcename'],sid=sid))
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[])
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[])
        self.assertTrue(deleteapi.delete_datasource(did=did))
        date=timeuuid.uuid1()
        uris=[
            {'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(len(response.imc_messages['unrouted']), 1)
        self.assertEqual(response.imc_messages['unrouted'][0].type, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].uris,[{'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid}])
        self.assertEqual(response.imc_messages['unrouted'][0].date, date)
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        with self.assertRaises(gestexcept.DatasourceNotFoundException) as cm:
            datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(cm.exception.error, gesterrors.E_GDA_GDSH_DSNF)
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[sid])

    def test_process_message_HOOKNEW_success_uris_do_not_exist_and_have_pending_hooks(self):
        ''' process_message_HOOKNEW should detect non existent uris with pending hooks,
            by not requesting any accion over them. Every uri in a HookNewUris message should
            exist, but some race conditions could happen that make this situation to consider '''
        username='test_process_message_hooknew_success_uris_do_not_exist_and_have_pending_hooks'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        datasource=datasourceapi.create_datasource(uid=uid,aid=aid,datasourcename=datasource_uri)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datapoint['datapointname'],sid=sid))
        self.assertTrue(userapi.register_pending_hook(uid=uid, uri=datasource['datasourcename'],sid=sid))
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        self.assertEqual(datapointapi.get_datapoint_hooks(pid=pid),[])
        self.assertEqual(datasourceapi.get_datasource_hooks(did=did),[])
        self.assertTrue(deleteapi.delete_datasource(did=did))
        self.assertTrue(deleteapi.delete_datapoint(pid=pid))
        date=timeuuid.uuid1()
        uris=[
            {'uri':datapoint['datapointname'],'type':vertex.DATAPOINT,'id':pid},
            {'uri':datasource['datasourcename'],'type':vertex.DATASOURCE,'id':did},
        ]
        message=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        response=lambdas.process_message_HOOKNEW(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'],[])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datapoint['datapointname']),[sid])
        self.assertEqual(userapi.get_uri_pending_hooks(uid=uid,uri=datasource['datasourcename']),[sid])
        with self.assertRaises(gestexcept.DatasourceNotFoundException) as cm:
            datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(cm.exception.error, gesterrors.E_GDA_GDSH_DSNF)
        with self.assertRaises(gestexcept.DatapointNotFoundException) as cm:
            datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(cm.exception.error, gesterrors.E_GPA_GDPH_DPNF)

    def test_process_message_CLSHOOKS_success_no_items(self):
        ''' process_message_CLSHOOKS should succeed if there is no item to clear '''
        sid=uuid.uuid4()
        ids=[]
        message=messages.ClearSessionHooksMessage(sid=sid, ids=ids)
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_CLSHOOKS_success_non_existing_items(self):
        ''' process_message_CLSHOOKS should succeed if there is no item to clear '''
        sid=uuid.uuid4()
        ids=[(uuid.uuid4(), vertex.DATASOURCE),(uuid.uuid4(), vertex.DATAPOINT)]
        message=messages.ClearSessionHooksMessage(sid=sid, ids=ids)
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_CLSHOOKS_success_items_exist(self):
        ''' process_message_CLSHOOKS should succeed and delete element hooks '''
        username='test_process_message_clshooks_success_items_exist'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        self.assertTrue(session.set_agent_session(sid=associated_sid1, aid=aid, uid=uid,pv=1))
        session_info1=session.get_agent_session_info(sid=associated_sid1)
        self.assertIsNotNone(session_info1)
        self.assertEqual(session_info1.sid, associated_sid1)
        self.assertEqual(session_info1.aid,aid)
        self.assertEqual(session_info1.uid,uid)
        self.assertNotEqual(session_info1.imc_address, None)
        self.assertTrue(datasourceapi.hook_to_datasource(did=did, sid=associated_sid1))
        self.assertTrue(datapointapi.hook_to_datapoint(pid=pid, sid=associated_sid1))
        associated_sid2=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=associated_sid2, aid=aid, uid=uid,pv=1))
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
        self.assertEqual(response.message_type, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        dp_hooks=datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(dp_hooks, [associated_sid2])
        ds_hooks=datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(ds_hooks, [associated_sid2])
        message=messages.ClearSessionHooksMessage(sid=associated_sid2, ids=[(pid,vertex.DATAPOINT),(did,vertex.DATASOURCE)])
        response=lambdas.process_message_CLSHOOKS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.message_type, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        dp_hooks=datapointapi.get_datapoint_hooks(pid=pid)
        self.assertEqual(dp_hooks, [])
        ds_hooks=datasourceapi.get_datasource_hooks(did=did)
        self.assertEqual(ds_hooks, [])

    def test_process_message_SSDATA_failure_non_existing_session(self):
        ''' process_message_SSDATA should fail if sid is not associated to this module '''
        sid=uuid.uuid4()
        t=timeuuid.uuid1()
        data=[
            {'uri':'uri','type':vertex.DATASOURCE,'content':'content'},
            {'uri':'uri2','type':vertex.DATAPOINT, 'content':'2323.434'}
        ]
        msg=wsmsgv1.SendMultiData(t=t, uris=data)
        message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
        response=lambdas.process_message_SSDATA(message=message)
        self.assertEqual(response.error, Errors.E_IIALD_SSDT_SNF)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_SSDATA_success(self):
        ''' process_message_SSDATA should succeed '''
        sid=uuid.uuid4()
        t=timeuuid.uuid1()
        data=[
            {'uri':'uri','type':vertex.DATASOURCE,'content':'content'},
            {'uri':'uri2','type':vertex.DATAPOINT, 'content':'333'}
        ]
        msg=wsmsgv1.SendMultiData(t=t, uris=data)
        message=messages.SendSessionDataMessage(sid=sid, data=msg.to_dict())
        class FakeWSSession:
            def __init__(self):
                self.response_json=None

            def write_message(self,message):
                self.response_json=json.dumps(message)
                return
        fake_callback=FakeWSSession()
        ws_session.agent_callback[message.sid]=fake_callback.write_message
        response=lambdas.process_message_SSDATA(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        expected_msg=msg
        self.assertEqual(fake_callback.response_json, json.dumps(expected_msg.to_dict()))

    def test_process_message_DATINT_failure_session_not_found_exception(self):
        ''' process_message_DATINT should fail if session is not found '''
        sid=uuid.uuid4()
        uri={'uri':'valid.uri','type':vertex.DATASOURCE, 'id':uuid.uuid4()}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, AuthErrors.E_AS_GASI_SNF)
        self.assertEqual(response.status, status.IMC_STATUS_ACCESS_DENIED)
        self.assertEqual(response.message_type, None)
        self.assertEqual(response.message_params, None)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_failure_orphaned_session(self):
        ''' process_message_DATINT should fail if session has no imc address '''
        sid=uuid.uuid4()
        self.assertTrue(session.unset_agent_session(sid=sid))
        uri={'uri':'valid.uri','type':vertex.DATASOURCE, 'id':uuid.uuid4()}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.E_IIALD_DATINT_NSA)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_failure_expired_session(self):
        ''' process_message_DATINT should fail if session has no imc address and has expired '''
        sid=uuid.uuid4()
        expired_session=ormagent.AgentSession(
            sid=sid,
            aid=None, 
            pv=None,
            uid=None,
            imc_address=None,
            last_update=timeuuid.uuid1(seconds=1)
        )
        self.assertTrue(cassapiagent.insert_agent_session(expired_session))
        uri={'uri':'valid.uri','type':vertex.DATASOURCE, 'id':uuid.uuid4()}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.E_IIALD_DATINT_SEXP)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        with self.assertRaises(authexcept.SessionNotFoundException) as cm:
            session.get_agent_session_info(sid=sid)
        self.assertEqual(cm.exception.error, AuthErrors.E_AS_GASI_SNF)

    def test_process_message_DATINT_failure_datasource_not_found(self):
        ''' process_message_DATINT should fail if datasource does not exist '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        uri={'uri':'valid.uri','type':vertex.DATASOURCE, 'id':uuid.uuid4()}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, gesterrors.E_GDA_GDC_DNF)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, None)
        self.assertEqual(response.message_params, None)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_failure_access_denied_to_datasource_data(self):
        ''' process_message_DATINT should fail if session has no access to datasource data '''
        username='test_process_message_datint_failure_access_denied_to_datasource_data'
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
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        uri={'uri':'valid.uri','type':vertex.DATASOURCE, 'id':datasource['did']}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, AuthErrors.E_ARA_AGDSD_RE)
        self.assertEqual(response.status, status.IMC_STATUS_ACCESS_DENIED)
        self.assertEqual(response.message_type, None)
        self.assertEqual(response.message_params, None)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_failure_datapoint_not_found(self):
        ''' process_message_DATINT should fail if datapoint does not exist '''
        sid=uuid.uuid4()
        aid=uuid.uuid4()
        uid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        uri={'uri':'valid.uri','type':vertex.DATAPOINT, 'id':uuid.uuid4()}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, gesterrors.E_GPA_GDC_DNF)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)
        self.assertEqual(response.message_type, None)
        self.assertEqual(response.message_params, None)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_failure_access_denied_to_datapoint_data(self):
        ''' process_message_DATINT should fail if session has no access to datapoint data '''
        username='test_process_message_datint_failure_access_denied_to_datapoint_data'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        uri={'uri':'valid.uri','type':vertex.DATAPOINT, 'id':datapoint['pid']}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, AuthErrors.E_ARA_AGDPD_RE)
        self.assertEqual(response.status, status.IMC_STATUS_ACCESS_DENIED)
        self.assertEqual(response.message_type, None)
        self.assertEqual(response.message_params, None)
        self.assertEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datapoint(self):
        ''' process_message_DATINT should succeed, but if no data is found, send an empty list '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datapoint_with_irt(self):
        ''' process_message_DATINT should succeed, but if no data is found, send an empty list with irt '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datapoint_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_datapoint(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages '''
        username='test_process_message_datint_success_all_interval_access_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 498)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 498)

    def test_process_message_DATINT_success_all_interval_access_datapoint_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages '''
        username='test_process_message_datint_success_all_interval_access_datapoint_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid} #uri arrives as local uri
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 498)

    def test_process_message_DATINT_success_all_interval_access_datapoint_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid} #uri arrives as local uri
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 498)

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datasource(self):
        ''' process_message_DATINT should succeed, and send an empty list if no data is found '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datasource'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datasource_with_irt(self):
        ''' process_message_DATINT should succeed, and send an empty list if no data is found with associated irt '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datasource_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datasource_foreign_uri(self):
        ''' process_message_DATINT should succeed, and send an empty list if no data is found '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datasource_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_no_data_in_datasource_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, and send an empty list if no data is found with associated irt '''
        username='test_process_message_datint_success_all_interval_access_no_data_in_datasource_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_success_all_interval_access_datasource(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages '''
        username='test_process_message_datint_success_all_interval_access_datasource'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages with irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages '''
        username='test_process_message_datint_success_all_interval_access_datasource_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve the data and generate the corresponding messages with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datapoint(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datapoint_with_irt(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datapoint_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datapoint_foreign_uri(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datapoint_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datapoint_foreign_uri_with_irt(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datapoint_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(session_data_msg.data, [])

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datasource(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datasource'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 0)

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datasource_with_irt(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datasource_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 0)

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datasource_foreign_uri(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datasource_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 0)

    def test_process_message_DATINT_failure_interval_bound_exception_to_all_interval_datasource_foreign_uri_with_irt(self):
        ''' process_message_DATINT should return an empty list if no access to the interval because of bound limitations with irt '''
        username='test_process_message_datint_failure_interval_bound_to_all_interval_datasource_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=1001)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 0)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datapoint(self):
        ''' process_message_DATINT should return only the data with allowed access '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        new_ii=timeuuid.min_uuid_from_time(450)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datapoint_with_irt(self):
        ''' process_message_DATINT should return only the data with allowed access with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datapoint_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt,irt)
        new_ii=timeuuid.min_uuid_from_time(450)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt,irt)
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datapoint_foreign_uri(self):
        ''' process_message_DATINT should return only the data with allowed access '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datapoint_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        new_ii=timeuuid.min_uuid_from_time(450)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datapoint_foreign_uri_with_irt(self):
        ''' process_message_DATINT should return only the data with allowed access with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datapoint_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt,irt)
        new_ii=timeuuid.min_uuid_from_time(450)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datasource(self):
        ''' process_message_DATINT should return only the data with allowed access '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datasource'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        new_ii=timeuuid.min_uuid_from_time(450)
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datasource_with_irt(self):
        ''' process_message_DATINT should return only the data with allowed access with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datasource_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        new_ii=timeuuid.min_uuid_from_time(450)
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datasource_foreign_uri(self):
        ''' process_message_DATINT should return only the data with allowed access '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datasource_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        new_ii=timeuuid.min_uuid_from_time(450)
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_failure_interval_bound_exception_to_partial_interval_datasource_foreign_uri_with_irt(self):
        ''' process_message_DATINT should return only the data with allowed access with associated irt '''
        username='test_process_message_datint_failure_interval_bound_to_partial_interval_datasource_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.min_uuid_from_time(450)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid, iface, minTs.hex))
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        new_ii=timeuuid.min_uuid_from_time(450)
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt,irt)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(session_data_msg.start, ii)
        self.assertEqual(session_data_msg.end, new_ii)
        self.assertEqual(len(session_data_msg.data), 0)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,new_ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie,ie)
        new_message=response.imc_messages['unrouted'][0]
        response=lambdas.process_message_DATINT(message=new_message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, new_message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(session_data_msg.start, new_ii)
        self.assertEqual(session_data_msg.end, ie)
        self.assertEqual(len(session_data_msg.data),50)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 200)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 200)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 200)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 200)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_not_enough_rows(self):
        ''' process_message_DATINT should succeed, retrieving less rows than requested if there are no more rows '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_not_enough_rows'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,50):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 48)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_not_enough_rows_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving less rows than requested if there are no more rows with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_not_enough_rows_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,50):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 48)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_not_enough_rows_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieving less rows than requested if there are no more rows '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_not_enough_rows_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,50):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 48)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_not_enough_rows_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving less rows than requested if there are no more rows with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_not_enough_rows_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,50):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count = 200
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 48)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_and_pagination(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval and paginate if interval count and msg count is greater than 1000 '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_with_pagination'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,1500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=5000)
        count = 2000
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(response.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(response.imc_messages['unrouted'][0].sid, sid)
        self.assertTrue(response.imc_messages['unrouted'][0].uri, uri)
        self.assertTrue(response.imc_messages['unrouted'][0].count, count-1000)
        self.assertTrue(response.imc_messages['unrouted'][0].ii, ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 1000)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_and_pagination_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval and paginate if interval count and msg count is greater than 1000 with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_with_pagination_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
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
        for i in range(2,1500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=5000)
        irt = timeuuid.TimeUUID()
        count = 2000
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(response.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(response.imc_messages['unrouted'][0].sid, sid)
        self.assertTrue(response.imc_messages['unrouted'][0].uri, uri)
        self.assertTrue(response.imc_messages['unrouted'][0].irt, irt)
        self.assertTrue(response.imc_messages['unrouted'][0].count, count-1000)
        self.assertTrue(response.imc_messages['unrouted'][0].ii, ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datapoint_uri, 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 1000)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_and_pagination_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval and paginate if interval count and msg count is greater than 1000 '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_with_pagination_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,1500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=5000)
        count = 2000
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(response.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(response.imc_messages['unrouted'][0].sid, sid)
        self.assertTrue(response.imc_messages['unrouted'][0].uri, uri)
        self.assertTrue(response.imc_messages['unrouted'][0].count, count-1000)
        self.assertTrue(response.imc_messages['unrouted'][0].ii, ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(len(session_data_msg.data), 1000)

    def test_process_message_DATINT_success_all_interval_access_datapoint_with_count_param_and_pagination_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieving as many rows as the count param says in the interval and paginate if interval count and msg count is greater than 1000 with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datapoint_with_count_param_with_pagination_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datapoint_uri='uris.datapoint_uri'
        datapoint=datapointapi.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        self.assertTrue(isinstance(pid,uuid.UUID))
        self.assertTrue(resupdate.new_user_datapoint(params={'uid':uid,'pid':pid}))
        for i in range(2,1500):
            dp_content=str(i)
            dp_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datapointapi.store_user_datapoint_value(pid=pid, date=dp_date, content=dp_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datapoint_uri,'type':vertex.DATAPOINT, 'id':pid}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=5000)
        irt = timeuuid.TimeUUID()
        count = 2000
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(response.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(response.imc_messages['unrouted'][0].sid, sid)
        self.assertTrue(response.imc_messages['unrouted'][0].uri, uri)
        self.assertTrue(response.imc_messages['unrouted'][0].irt, irt)
        self.assertTrue(response.imc_messages['unrouted'][0].count, count-1000)
        self.assertTrue(response.imc_messages['unrouted'][0].ii, ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datapoint_uri)), 'type':vertex.DATAPOINT})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 1000)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 50)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 50)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 50)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 50)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_not_enough_rows(self):
        ''' process_message_DATINT should succeed, retrieve less rows than requested if there are no more rows '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_not_enough'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,5):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 3)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_not_enough_rows_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve less rows than requested if there are no more rows with associated irt'''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_not_enough_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,5):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 3)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_not_enough_rows_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieve less rows than requested if there are no more rows '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_not_enough_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,5):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 3)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_not_enough_rows_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve less rows than requested if there are no more rows with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_not_enough_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,5):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count=50
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 3)

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_and_pagination(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param and paginate results if count and rows are greater than 100 '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_and_pagination'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=500
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].count,count-100)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_and_pagination_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param and paginate results if count and rows are greater than 100 with associated irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_and_pagination_with_irt'
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
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid, uid=uid,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        irt = timeuuid.TimeUUID()
        count=500
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':datasource_uri, 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].count,count-100)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_and_pagination_foreign_uri(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param and paginate results if count and rows are greater than 100 '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_and_pagination_foreign_uri'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=500
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].count,count-100)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

    def test_process_message_DATINT_success_all_interval_access_datasource_with_count_param_and_pagination_foreign_uri_with_irt(self):
        ''' process_message_DATINT should succeed, retrieve as much rows as requested by count param and paginate results if count and rows are greater than 100. All data messages generated should be associated to original irt '''
        username='test_process_message_datint_success_all_interval_access_datasource_with_count_param_and_pagination_foreign_uri_with_irt'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='v'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid=user['uid']
        aid=agent['aid']
        datasource_uri='uris.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasource_uri)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasource_uri)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        self.assertTrue(isinstance(did,uuid.UUID))
        self.assertTrue(resupdate.new_datasource(params={'uid':uid,'did':did}))
        for i in range(2,500):
            ds_content='data: '+str(i)
            ds_date=timeuuid.uuid1(seconds=i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        username_req=username+'_req'
        password='password'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user['uid'], dest_uid=user_req['uid'],uri='uris',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='v'
        agent_req=agentapi.create_agent(uid=user_req['uid'], agentname=agentname, pubkey=pubkey, version=version)
        uid_req=user_req['uid']
        aid_req=agent_req['aid']
        sid=uuid.uuid4()
        self.assertTrue(session.set_agent_session(sid=sid, aid=aid_req, uid=uid_req,pv=1))
        session_info=session.get_agent_session_info(sid=sid)
        uri={'uri':datasource_uri,'type':vertex.DATASOURCE, 'id':did}
        ii=timeuuid.uuid1(seconds=1)
        ie=timeuuid.uuid1(seconds=1000)
        count=500
        irt = timeuuid.TimeUUID()
        message=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie, count=count, irt=irt)
        response=lambdas.process_message_DATINT(message=message)
        self.assertEqual(response.error, Errors.OK)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(response.message_type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.message_params, message.to_serialization())
        self.assertNotEqual(response.imc_messages['routed'], {})
        self.assertNotEqual(response.imc_messages['unrouted'], [])
        self.assertTrue(session_info.imc_address in response.imc_messages['routed'])
        self.assertTrue(len(response.imc_messages['routed'][session_info.imc_address]) == 1)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].type, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertEqual(response.imc_messages['routed'][session_info.imc_address][0].sid, sid)
        recv_data=response.imc_messages['routed'][session_info.imc_address][0].data
        session_data_msg=wsmsgv1.SendDataInterval.load_from_dict(recv_data)
        self.assertEqual(session_data_msg.uri, {'uri':':'.join((username,datasource_uri)), 'type':vertex.DATASOURCE})
        self.assertEqual(session_data_msg.irt, irt)
        self.assertEqual(len(session_data_msg.data), 100)
        self.assertEqual(len(response.imc_messages['unrouted']),1)
        self.assertEqual(response.imc_messages['unrouted'][0].type,messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(response.imc_messages['unrouted'][0].sid,sid)
        self.assertEqual(response.imc_messages['unrouted'][0].uri,uri)
        self.assertEqual(response.imc_messages['unrouted'][0].count,count-100)
        self.assertEqual(response.imc_messages['unrouted'][0].ii,ii)
        self.assertEqual(response.imc_messages['unrouted'][0].irt,irt)
        self.assertEqual(response.imc_messages['unrouted'][0].ie.hex, response.imc_messages['routed'][session_info.imc_address][0].data['payload']['start'])

