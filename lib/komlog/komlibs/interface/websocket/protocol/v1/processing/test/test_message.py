import unittest
import uuid
import time
from komlog.komfig import logging, options
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.auth import authorization
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount import exceptions as gestexcept
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.graph.api import uri as graphuri
from komlog.komlibs.graph.relations import vertex
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
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDSDM_IMT.value)

    def test__process_send_ds_data_failure_user_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)

    def test__process_send_ds_data_failure_agent_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        username='test_process_send_ds_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_IURI.value)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        option_bck=options.SAMPLES_RECEIVED_PATH
        def auth_mock(request, passport):
            return True
        option_mock='anonexistentoption:intheconfigfile'
        authorization.authorize_request = auth_mock
        options.SAMPLES_RECEIVED_PATH=option_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_EUR.value)
        authorization.authorize_request = auth_req_bck
        options.SAMPLES_RECEIVED_PATH=option_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_ds_data_failure_processing_operation(self):
        ''' _process_send_ds_data should fail if processing the post operation fails '''
        username='test_process_send_ds_data_failure_processing_operation'
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
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport):
            return True
        def operation_mock(op):
            return False
        authorization.authorize_request = auth_mock
        operation.process_operation=operation_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_FUR.value)
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_EUR.value)
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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertEqual(resp.error, Errors.OK.value)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)

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
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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

    def test__process_send_dp_data_failure_invalid_message(self):
        ''' _process_send_dp_data should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'key':'a message malformed'}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPDM_IMT.value)

    def test__process_send_dp_data_failure_different_message_passed(self):
        ''' _process_send_dp_data should fail if message is not of type SEND_DP_DATA '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPDM_IA.value)

    def test__process_send_dp_data_failure_user_not_found(self):
        ''' _process_send_dp_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)

    def test__process_send_dp_data_failure_agent_not_found(self):
        ''' _process_send_dp_data should fail if agent does not exist '''
        username='test_process_send_dp_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4())
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDPD_RE.value)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_IURI.value)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, gesterrors.E_GPA_SDPSV_CVNN.value)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_dp_data_failure_processing_operation(self):
        ''' _process_send_dp_data should fail if processing the post operation fails '''
        username='test_process_send_dp_data_failure_processing_operation'
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
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'payload':{'uri':'system.dp','ts':time.time(),'content':'55'}}
        operation_bck=operation.process_operation
        def operation_mock(op):
            return False
        operation.process_operation=operation_mock
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_FPOR.value)
        operation.process_operation = operation_bck
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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.dp','ts':time.time(),'content':'-1.3e8'}}
        operation_bck=operation.process_operation
        def operation_mock(op):
            raise Exception()
        operation.process_operation=operation_mock
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.UNKNOWN.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.dp','ts':time.time(),'content':'77.5'}}
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)

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
        msg={'v':1,'action':Messages.SEND_DP_DATA,'payload':{'uri':'system.dp','ts':time.time(),'content':'-32.0'}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertIsNotNone(datapoint)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.error, Errors.OK.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['id'],datapoint['pid'])

