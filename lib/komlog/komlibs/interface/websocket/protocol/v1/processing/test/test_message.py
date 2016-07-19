import unittest
import uuid
import time
import decimal
import pandas as pd
from komlog.komfig import logging, options
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.relations import vertex
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.websocket.protocol.v1 import exceptions, status
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import message, operation
from komlog.komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlog.komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlog.komlibs.interface.websocket.protocol.v1.model.types import Messages


class InterfaceWebSocketProtocolV1ProcessingMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.processing.message tests '''

    def test__process_send_ds_data_failure_invalid_message(self):
        ''' _process_send_ds_data should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDSD_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_user_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_agent_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        username='test_process_send_ds_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_no_permission_for_ds_creation(self):
        ''' _process_send_ds_data should fail if user has no permission for ds creation '''
        username='test_process_send_ds_data_failure_no_permission_for_ds_creation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_no_permission_for_uri_mutation(self):
        ''' _process_send_ds_data should fail if user has no permission for uri mutation '''
        username='test_process_send_ds_data_failure_no_permission_for_uri_mutation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_no_permission_for_post_ds_data(self):
        ''' _process_send_ds_data should fail if user has no permission for posting over this ds '''
        username='test_process_send_ds_data_failure_no_permission_for_post_ds_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_incompatible_uri_type(self):
        ''' _process_send_ds_data should fail if uri exists and is not void or ds type '''
        username='test_process_send_ds_data_failure_incompatible_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_IURI.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_ds_data_failure_error_creating_ds(self):
        ''' _process_send_ds_data should fail if ds creationg fails '''
        username='test_process_send_ds_data_failure_error_creating_ds'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        ds_creation_bck=datasourceapi.create_datasource
        def auth_mock(request, passport):
            return True
        def ds_creation_mock(uid, aid, datasourcename):
            return None
        authorization.authorize_request = auth_mock
        datasourceapi.create_datasource = ds_creation_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_ECDS.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        authorization.authorize_request = auth_req_bck
        datasourceapi.create_datasource = ds_creation_bck

    def test__process_send_ds_data_failure_error_path_not_found(self):
        ''' _process_send_ds_data should fail if path to store data is not found '''
        username='test_process_send_ds_data_failure_error_path_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        option_bck=options.SAMPLES_RECEIVED_PATH
        def auth_mock(request, passport):
            return True
        option_mock='anonexistentoption:intheconfigfile'
        authorization.authorize_request = auth_mock
        options.SAMPLES_RECEIVED_PATH=option_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, gesterrors.E_GDA_UDD_IDD.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        authorization.authorize_request = auth_req_bck
        options.SAMPLES_RECEIVED_PATH=option_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_ds_data_failure_processing_operation_exception(self):
        ''' _process_send_ds_data should fail if processing the post operation exception '''
        username='test_process_send_ds_data_failure_processing_operation_exception'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport):
            return True
        def operation_mock(op):
            raise Exception()
        authorization.authorize_request = auth_mock
        operation.process_operation=operation_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_ds_data_success_ds_did_not_exist_previously(self):
        ''' _process_send_ds_data should succeed and create the ds '''
        username='test_process_send_ds_data_success_ds_did_not_exist_previously'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertNotEqual(resp.unrouted_messages,[])
        self.assertEqual(resp.routed_messages,{})
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:1,
            messages.NEW_DS_WIDGET_MESSAGE:1,
            messages.USER_EVENT_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))

    def test__process_send_ds_data_success_ds_already_existed(self):
        ''' _process_send_ds_data should succeed and create the ds '''
        username='test_process_send_ds_data_success_ds_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        self.assertTrue(datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri']))
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        def operation_mock(op):
            return True
        authorization.authorize_request = auth_mock
        operation.process_operation=operation_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertEqual(resp.error, Errors.OK.value)
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(resp.routed_messages,{})
        expected_messages={
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))

    def test__process_send_dp_data_failure_invalid_message(self):
        ''' _process_send_dp_data should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_different_message_passed(self):
        ''' _process_send_dp_data should fail if message is not of type SEND_DP_DATA '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_user_not_found(self):
        ''' _process_send_dp_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'89'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_agent_not_found(self):
        ''' _process_send_dp_data should fail if agent does not exist '''
        username='test_process_send_dp_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'79'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_no_permission_for_dp_creation(self):
        ''' _process_send_dp_data should fail if agent has no permission for dp creation '''
        username='test_process_send_dp_data_failure_no_permission_for_dp_creation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'],sid=uuid.uuid4(), aid=agent['aid'])
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'70'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_no_permission_for_uri_mutation(self):
        ''' _process_send_dp_data should fail if user has no permission for uri mutation '''
        username='test_process_send_dp_data_failure_no_permission_for_uri_mutation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_no_permission_for_post_dp_data(self):
        ''' _process_send_dp_data should fail if user has no permission for posting over this dp '''
        username='test_process_send_dp_data_failure_no_permission_for_post_dp_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDPD_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_incompatible_uri_type(self):
        ''' _process_send_dp_data should fail if uri exists and is not void or dp type '''
        username='test_process_send_dp_data_failure_incompatible_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.void','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_IURI.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_dp_data_failure_error_creating_dp(self):
        ''' _process_send_dp_data should fail if dp creationg fails '''
        username='test_process_send_dp_data_failure_error_creating_dp'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'70'}}
        res_msg=messages. ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        dp_creation_bck=datapointapi.create_user_datapoint
        def dp_creation_mock(uid, datapoint_uri):
            return None
        datapointapi.create_user_datapoint = dp_creation_mock
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_ECDP.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        datapointapi.create_user_datapoint = dp_creation_bck

    def test__process_send_dp_data_failure_error_invalid_message_numeric_content(self):
        ''' _process_send_dp_data should fail if storing datapoint value fails '''
        username='test_process_send_dp_data_failure_error_invalid_message_numeric_content'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ICNT.value)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_dp_data_failure_processing_operation_exception(self):
        ''' _process_send_dp_data should fail if processing the post operation exception '''
        username='test_process_send_dp_data_failure_processing_operation_exception'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.dp','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'-1.3e8'}}
        operation_bck=operation.process_operation
        def operation_mock(op):
            raise Exception()
        operation.process_operation=operation_mock
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.UNKNOWN.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        operation.process_operation = operation_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_dp_data_success_dp_did_not_exist_previously(self):
        ''' _process_send_dp_data should succeed and create the user dp '''
        username='test_process_send_dp_data_success_dp_did_not_exist_previously'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.dp','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'77.5'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertNotEqual(resp.unrouted_messages,[])
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:1,
            messages.NEW_DP_WIDGET_MESSAGE:1,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))

    def test__process_send_dp_data_success_dp_already_existed(self):
        ''' _process_send_dp_data should succeed using the existing datapoint '''
        username='test_process_send_dp_data_success_dp_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.dp','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'-32.0'}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertIsNotNone(datapoint)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for item in msgs:
            try:
                retrieved_messages[item.type]+=1
            except KeyError:
                retrieved_messages[item.type]=1
        self.assertEqual(sorted(expected_messages),sorted(retrieved_messages))
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['id'],datapoint['pid'])

    def test__process_send_multi_data_failure_invalid_message(self):
        ''' _process_send_multi_data should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SMTD_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_different_message_passed(self):
        ''' _process_send_multi_data should fail if message is not of type SEND_MULTI_DATA '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SMTD_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_user_not_found_new_datasource_auth_failed(self):
        ''' _process_send_multi_data should fail if user does not exist and a new ds uri has to be created '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri','type':vertex.DATASOURCE,'content':'content'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_agent_not_found_new_datasource_auth_failed(self):
        ''' _process_send_multi_data should fail if agent does not exist '''
        username='test_process_send_multi_data_failure_agent_not_found_new_ds_auth_failed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri','type':vertex.DATASOURCE,'content':'content'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_user_not_found_new_datapoint_auth_failed(self):
        ''' _process_send_multi_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_agent_not_found_new_datapoint_auth_failed(self):
        ''' _process_send_multi_data should fail if agent does not exist '''
        username='test_process_send_multi_data_failure_agent_not_found_new_dp_auth_failed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_send_multi_data should fail if uri type is not datasource nor datapoint '''
        username='test_process_send_multi_data_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.widget','type':vertex.DATAPOINT,'content':'44'}]}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_ONAOU.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_no_permission_for_post_datapoint_data(self):
        ''' _process_send_multi_data should fail if user has no permission to post datapoint data'''
        username='test_process_send_multi_data_failure_no_permission_for_post_datapoint_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ATDPD_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_failure_no_permission_for_post_datasource_data(self):
        ''' _process_send_multi_data should fail if user has no permission to post datasource data'''
        username='test_process_send_multi_data_failure_no_permission_for_post_datasource_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_success_new_datasource(self):
        ''' _process_send_multi_data should succeed and create the new datasource '''
        username='test_process_send_multi_data_success_new_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'content 5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:2,
            messages.NEW_DS_WIDGET_MESSAGE:1,
            messages.USER_EVENT_MESSAGE:1,
            messages.GENERATE_TEXT_SUMMARY_MESSAGE:1,
            messages.MAP_VARS_MESSAGE:1,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(retrieved_messages), sorted(expected_messages))
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATASOURCE)

    def test__process_send_multi_data_success_new_datapoint(self):
        ''' _process_send_multi_data should succeed and create the new datapoint '''
        username='test_process_send_multi_data_success_new_datapoint'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT,'content':'5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:1,
            messages.NEW_DP_WIDGET_MESSAGE:1,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
        self.assertEqual(sorted(retrieved_messages), sorted(expected_messages))
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATAPOINT)

    def test__process_send_multi_data_success_datasource_already_existed(self):
        ''' _process_send_multi_data should succeed and store content in already existing ds '''
        username='test_process_send_multi_data_success_datasource_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:1,
            messages.GENERATE_TEXT_SUMMARY_MESSAGE:1,
            messages.MAP_VARS_MESSAGE:1,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
 
    def test__process_send_multi_data_success_datapoint_already_existed(self):
        ''' _process_send_multi_data should and store content in datapoint '''
        username='test_process_send_multi_data_success_datapoint_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for msg in msgs:
            try:
                retrieved_messages[msg.type]+=1
            except KeyError:
                retrieved_messages[msg.type]=1
 
    def test__process_send_multi_data_failure_datapoint_already_existed_but_content_is_not_numeric(self):
        ''' _process_send_multi_data should fail if we try to store non numeric content into a datapoint '''
        username='test_process_send_multi_data_failure_datapoint_already_existed_but_content_is_not_numeric'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'payload':{'ts':pd.Timestamp('now',tz='utc').isoformat(),'uris':[{'uri':'uri.dp','type':vertex.DATASOURCE, 'content':'value: 44'}]}}
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_UCNV.value)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_send_multi_data_success_existing_and_non_existing_uris(self):
        ''' _process_send_multi_data should succeed, creating uris when they do not exist and updating the existing ones '''
        username='test_process_send_multi_data_success_existing_and_non_existing_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={
            'v':1,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'ts':pd.Timestamp('now',tz='utc').isoformat(),
                'uris':[
                    {'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'-4.4'},
                    {'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'value: 44'},
                    {'uri':'uri.new_dp','type':vertex.DATAPOINT, 'content':'44'},
                    {'uri':'uri.new_ds','type':vertex.DATASOURCE, 'content':'new value: 44'},
                    ]
            }
        }
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertNotEqual(resp.unrouted_messages,[])
        expected_messages={
            messages.UPDATE_QUOTES_MESSAGE:4,
            messages.NEW_DP_WIDGET_MESSAGE:1,
            messages.NEW_DS_WIDGET_MESSAGE:1,
            messages.USER_EVENT_MESSAGE:1,
            messages.GENERATE_TEXT_SUMMARY_MESSAGE:2,
            messages.MAP_VARS_MESSAGE:2,
            messages.URIS_UPDATED_MESSAGE:1
        }
        retrieved_messages={}
        msgs=resp.unrouted_messages
        for item in msgs:
            try:
                retrieved_messages[item.type]+=1
            except KeyError:
                retrieved_messages[item.type]=1
        self.assertEqual(sorted(retrieved_messages), sorted(expected_messages))
        did=datasource['did']
        existing_ds_stats=cassapidatasource.get_datasource_stats(did=did)
        date=existing_ds_stats.last_received
        self.assertEqual(timeuuid.get_unix_timestamp(date),timeuuid.get_unix_timestamp(timeuuid.uuid1(seconds=pd.Timestamp(msg['payload']['ts']).timestamp())))
        existing_ds_data=cassapidatasource.get_datasource_data_at(did=did, date=date)
        self.assertEqual(existing_ds_data.content, 'value: 44')
        pid=datapoint['pid']
        existing_dp_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        self.assertEqual(date, existing_dp_stats.last_received)
        existing_dp_data=cassapidatapoint.get_datapoint_data_at(pid=pid, date=date)
        self.assertEqual(existing_dp_data.value, decimal.Decimal('-4.4'))
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.new_ds')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATASOURCE)
        new_ds_stats=cassapidatasource.get_datasource_stats(did=uri_info['id'])
        self.assertEqual(new_ds_stats.last_received, date)
        new_ds_data=cassapidatasource.get_datasource_data_at(did=uri_info['id'], date=date)
        self.assertEqual(new_ds_data.content, 'new value: 44')
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.new_dp')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATAPOINT)
        new_dp_stats=cassapidatapoint.get_datapoint_stats(pid=uri_info['id'])
        self.assertEqual(new_dp_stats.last_received, date)
        new_dp_data=cassapidatapoint.get_datapoint_data_at(pid=uri_info['id'],date=date)
        self.assertEqual(new_dp_data.value, decimal.Decimal('44'))
        self.assertEqual(new_dp_data.date, date)

    def test__process_send_multi_data_failure_existing_and_non_existing_uris_dp_content_not_valid(self):
        ''' _process_send_multi_data should fail if one of the uris content is not valid '''
        username='test_process_send_multi_data_failure_existing_and_non_existing_uris_dp_content_not_valid'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={
            'v':1,
            'action':Messages.SEND_MULTI_DATA.value,
            'payload':{
                'ts':pd.Timestamp('now',tz='utc').isoformat(),
                'uris':[
                    {'uri':'uri.dp','type':vertex.DATASOURCE, 'content':'content: -4.4'},
                    {'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'value: 44'},
                    {'uri':'uri.new_dp','type':vertex.DATAPOINT, 'content':'44'},
                    {'uri':'uri.new_ds','type':vertex.DATASOURCE, 'content':'new value: 44'},
                ]
            }
        }
        resp=message._process_send_multi_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_UCNV.value)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.new_ds')
        self.assertIsNone(uri_info)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.new_dp')
        self.assertIsNone(uri_info)
        did=datasource['did']
        existing_ds_stats=cassapidatasource.get_datasource_stats(did=did)
        self.assertIsNone(existing_ds_stats)
        pid=datapoint['pid']
        existing_dp_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        self.assertIsNone(existing_dp_stats)

    def test__process_hook_to_uri_failure_invalid_message(self):
        ''' _process_hook_to_uri should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_HTU_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_failure_different_message_passed(self):
        ''' _process_hook_to_uri should fail if message is not of type HOOK_TO_URI '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':pd.Timestamp('now',tz='utc').isoformat(),'content':'content'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_HTU_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_failure_uri_not_found(self):
        ''' _process_hook_to_uri should fail if uri does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'system.ds'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PHTU_UNF.value)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_hook_to_uri should fail if uri type is not datasource nor datapoint '''
        username='test_process_hook_to_uri_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.widget'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PHTU_ONA.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_failure_no_read_permission_for_datasource(self):
        ''' _process_hook_to_uri should fail if uri type is datasource and no read perm is found'''
        username='test_process_hook_to_uri_failure_no_read_permission_for_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_AHTDS_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_success_datasource_uri(self):
        ''' _process_hook_to_uri should succeed if uri type is ds and read perm is found'''
        username='test_process_hook_to_uri_success_datasource_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp.sid])

    def test__process_hook_to_uri_success_datasource_uri_multiple_sessions(self):
        ''' _process_hook_to_uri should succeed if uri type is ds and read perm is found and register all sessions hooked to the ds '''
        username='test_process_hook_to_uri_success_datasource_uri_multiple_sessions'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp2 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp3 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        #if the same session resend the message, it has no efect over hooked sids
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))

    def test__process_hook_to_uri_failure_no_read_permission_for_datapoint(self):
        ''' _process_hook_to_uri should fail if uri is dp and we dont have read perm over it'''
        username='test_process_hook_to_uri_failure_no_read_permission_for_datapoint'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_AHTDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_hook_to_uri_success_datapoint_uri(self):
        ''' _process_hook_to_uri should succeed if uri is dp and we have read perm over it'''
        username='test_process_hook_to_uri_success_datapoint_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp.sid])

    def test__process_hook_to_uri_success_datapoint_uri_multiple_sessions(self):
        ''' _process_hook_to_uri should succeed if uri is dp and we have read perm over it and register all the sessions hooked '''
        username='test_process_hook_to_uri_success_datapoint_uri_multiple_sessions'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp2 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp3 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))

    def test__process_unhook_from_uri_failure_invalid_message(self):
        ''' _process_unhook_from_uri should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_UHFU_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_failure_different_message_passed(self):
        ''' _process_unhook_from_uri should fail if message is not of type UNHOOK_FROM_URI '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'system.ds'}}
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_UHFU_ELFD.value)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_failure_uri_not_found(self):
        ''' _process_unhook_from_uri should fail if uri does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'system.ds'}}
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PUHFU_UNF.value)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_unhook_from_uri should fail if uri type is not datasource nor datapoint '''
        username='test_process_unhook_from_uri_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri.widget'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PUHFU_ONA.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_failure_no_read_permission_for_datasource(self):
        ''' _process_unhook_from_uri should fail if uri type is datasource and no read perm is found'''
        username='test_process_unhook_from_uri_failure_no_read_permission_for_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_AUHFDS_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_success_datasource_uri(self):
        ''' _process_unhook_from_uri should succeed if uri type is ds and read perm is found'''
        username='test_process_unhook_from_uri_success_datasource_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp2 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp3 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri.ds'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[])

    def test__process_unhook_from_uri_failure_no_read_permission_for_datapoint(self):
        ''' _process_unhook_to_uri should fail if uri is dp and we dont have read perm over it'''
        username='test_process_unhook_from_uri_failure_no_read_permission_for_datapoint'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_unhook_from_uri(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, autherrors.E_ARA_AUHFDP_RE.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])

    def test__process_unhook_from_uri_success_datapoint_uri(self):
        ''' _process_unhook_from_uri should succeed if uri is dp and we have read perm over it'''
        username='test_process_unhook_from_uri_success_datapoint_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp2 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        psp3 = Passport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4())
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'payload':{'uri':'uri.dp'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.routed_messages,{})
        self.assertEqual(resp.unrouted_messages,[])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[])

