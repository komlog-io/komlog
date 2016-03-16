import unittest
import uuid
import time
from komfig import logger, options
from komimc import bus, routing
from komimc import api as msgapi
from komlibs.auth import exceptions as authexcept
from komlibs.auth import errors as autherrors
from komlibs.auth import authorization
from komlibs.auth.passport import Passport
from komlibs.general.crypto import crypto
from komlibs.gestaccount import exceptions as gestexcept
from komlibs.gestaccount import errors as gesterrors
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.graph.api import uri as graphuri
from komlibs.graph.relations import vertex
from komlibs.interface.imc.model import messages
from komlibs.interface.websocket.protocol.v1 import errors, exceptions, status
from komlibs.interface.websocket.protocol.v1.processing import message, operation
from komlibs.interface.websocket.protocol.v1.model import message as modmsg
from komlibs.interface.websocket.protocol.v1.model import response as modresp
from komlibs.interface.websocket.protocol.v1.model.types import Message


class InterfaceWebSocketProtocolV1ProcessingMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.processing.message tests '''

    def test__process_send_ds_data_failure_invalid_message(self):
        ''' _process_send_ds_data should fail if message is invalid '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4())
        msg={'key':'a message malformed'}
        with self.assertRaises(exceptions.MessageValidationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, errors.E_IWSPV1MM_SDDM_IMT)

    def test__process_send_ds_data_failure_user_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        psp = Passport(uid=uuid.uuid4(),aid=uuid.uuid4())
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        with self.assertRaises(authexcept.AuthorizationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, autherrors.E_ARA_ANDS_RE)

    def test__process_send_ds_data_failure_agent_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        username='test_process_send_ds_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = Passport(uid=user_reg['uid'],aid=uuid.uuid4())
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        with self.assertRaises(authexcept.AuthorizationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, autherrors.E_ARA_ANDS_RE)

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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
        with self.assertRaises(authexcept.AuthorizationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, autherrors.E_ARA_ANDS_RE)

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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        with self.assertRaises(authexcept.AuthorizationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, autherrors.E_ARA_ANDS_RE)

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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        with self.assertRaises(authexcept.AuthorizationException) as cm:
            message._process_send_ds_data(psp, msg)
        self.assertEqual(cm.exception.error, autherrors.E_ARA_ATDSD_RE)

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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.void','ts':time.time(),'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, errors.E_IWSPV1PM_PSDD_IURI)

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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'uri','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, errors.E_IWSPV1PM_PSDD_ECDS)
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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, errors.E_IWSPV1PM_PSDD_EUR)
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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA.value,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, errors.E_IWSPV1PM_PSDD_FUR)
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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, errors.E_IWSPV1PM_PSDD_EUR)
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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport):
            return True
        def operation_mock(op):
            return True
        authorization.authorize_request = auth_mock
        operation.process_operation=operation_mock
        resp=message._process_send_ds_data(psp, msg)
        self.assertTrue(isinstance(resp, modresp.Response))
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertEqual(resp.error, None)
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
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
        psp = Passport(uid=user_reg['uid'], aid=agent['aid'])
        msg={'v':1,'action':Message.SEND_DS_DATA,'payload':{'uri':'system.ds','ts':time.time(),'content':'content'}}
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
        self.assertEqual(resp.error, None)
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)

