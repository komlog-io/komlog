import unittest
import uuid
import time
import decimal
from komlog.komfig import logging, options
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import interface as cassapiiface
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.auth import exceptions as authexcept
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.auth import authorization, permissions
from komlog.komlibs.auth.passport import AgentPassport
from komlog.komlibs.auth.resources import update as resupdate
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth.model import interfaces
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
from komlog.komlibs.interface.websocket import exceptions, status
from komlog.komlibs.interface.websocket.model import response
from komlog.komlibs.interface.websocket.model.types import Messages
from komlog.komlibs.interface.websocket.protocol.v1.errors import Errors
from komlog.komlibs.interface.websocket.protocol.v1.processing import message, operation
from komlog.komlibs.interface.websocket.protocol.v1.model import message as v1msg


pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

class InterfaceWebSocketProtocolV1ProcessingMessageTest(unittest.TestCase):
    ''' komlibs.interface.websocket.protocol.v1.processing.message tests '''

    def test__process_send_ds_data_failure_invalid_message(self):
        ''' _process_send_ds_data should fail if message is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDSD_ELFD)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, None)

    def test__process_send_ds_data_failure_user_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_data_failure_agent_not_found(self):
        ''' _process_send_ds_data should fail if user does not exist '''
        username='test_process_send_ds_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = AgentPassport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris_of_non_existent_users(self):
        ''' _process_send_ds_data should fail if user tries send data for a foreign global uri '''
        username_owner='test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris_of_non_existent_users_non_existent'
        username='test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris_of_non_existent_users'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri=username_owner+':some_uri'
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':uri,'t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris(self):
        ''' _process_send_ds_data should fail if user tries send data for a foreign global uri '''
        username_owner='test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_send_ds_data_failure_no_permission_to_modify_foreign_global_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri=username_owner+':some_uri'
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':uri,'t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_EUGURI)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_data_failure_no_permission_for_ds_creation(self):
        ''' _process_send_ds_data should fail if user has no permission for ds creation '''
        username='test_process_send_ds_data_failure_no_permission_for_ds_creation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_data_failure_no_permission_for_uri_mutation(self):
        ''' _process_send_ds_data should fail if user has no permission for uri mutation '''
        username='test_process_send_ds_data_failure_no_permission_for_uri_mutation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_data_failure_no_permission_for_post_ds_data(self):
        ''' _process_send_ds_data should fail if user has no permission for posting over this ds '''
        username='test_process_send_ds_data_failure_no_permission_for_post_ds_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_data_failure_incompatible_uri_type(self):
        ''' _process_send_ds_data should fail if uri exists and is not void or ds type '''
        username='test_process_send_ds_data_failure_incompatible_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'content'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_IURI)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_data_failure_error_creating_ds(self):
        ''' _process_send_ds_data should fail if ds creationg fails '''
        username='test_process_send_ds_data_failure_error_creating_ds'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'content'}}
        auth_req_bck=authorization.authorize_request
        ds_creation_bck=datasourceapi.create_datasource
        def auth_mock(request, passport):
            return True
        def ds_creation_mock(uid, aid, datasourcename):
            return None
        authorization.authorize_request = auth_mock
        datasourceapi.create_datasource = ds_creation_mock
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSD_ECDS)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        authorization.authorize_request = auth_req_bck
        datasourceapi.create_datasource = ds_creation_bck

    def test__process_send_ds_data_failure_processing_operation_exception(self):
        ''' _process_send_ds_data should fail if processing the post operation exception '''
        username='test_process_send_ds_data_failure_processing_operation_exception'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport):
            return True
        def operation_mock(op):
            raise Exception()
        authorization.authorize_request = auth_mock
        operation.process_operation=operation_mock
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error.value, Errors.UNKNOWN.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        authorization.authorize_request = auth_req_bck
        operation.process_operation = operation_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNone(uri_info)

    def test__process_send_ds_data_failure_storing_data(self):
        ''' _process_send_ds_data should fail if an error occurs while storing data '''
        username='test_process_send_ds_data_failure_storing_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        auth_req_bck=authorization.authorize_request
        storing_bck=datasourceapi.store_datasource_data
        def auth_mock(request, passport):
            return True
        def storing_mock(op):
            uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
            self.assertIsNotNone(uri_info)
            raise Exception()
        authorization.authorize_request = auth_mock
        datasourceapi.store_datasource_data=storing_mock
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error.value, Errors.UNKNOWN.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        authorization.authorize_request = auth_req_bck
        datasourceapi.store_datasource_data=storing_bck
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_ds_data_success_ds_did_not_exist_previously_with_global_uri(self):
        ''' _process_send_ds_data should succeed and create the ds '''
        username='test_process_send_ds_data_success_ds_did_not_exist_previously_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='system.ds')
        self.assertIsNotNone(uri_info)
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_ds_data_success_ds_already_existed(self):
        ''' _process_send_ds_data should succeed and create the ds '''
        username='test_process_send_ds_data_success_ds_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        self.assertTrue(datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri']))
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        authorization.authorize_request = auth_req_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_ds_data_success_ds_already_existed_with_global_uri(self):
        ''' _process_send_ds_data should succeed and create the ds '''
        username='test_process_send_ds_data_success_ds_already_existed_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        self.assertTrue(datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='system.ds'))
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        authorization.authorize_request = auth_req_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='system.ds')
        self.assertIsNotNone(uri_info)
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_ds_info_failure_invalid_message(self):
        ''' _process_send_ds_info should fail if message is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDSI_ELFD)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, None)

    def test__process_send_ds_info_failure_user_not_found(self):
        ''' _process_send_ds_info should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','supplies':None}}
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSI_UNF)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_info_failure_user_not_found_in_global_uri(self):
        ''' _process_send_ds_info should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'process_send_ds_info_failure_user_not_found_in_global_uri:uri','supplies':None}}
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSI_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_info_failure_no_permission_to_modify_foreign_global_uris(self):
        ''' _process_send_ds_info should fail if user tries send info for a foreign global uri '''
        username_owner='test__process_send_ds_info_failure_no_permission_to_modify_foreign_global_uris_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_send_ds_info_failure_no_permission_to_modify_foreign_global_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri=username_owner+':some_uri'
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':uri,'supplies':['some.uri','other.uri']}}
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSI_EUGURI)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_info_failure_ds_not_found(self):
        ''' _process_send_ds_info should fail if ds does not exist '''
        username='test__process_send_ds_info_failure_ds_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','supplies':None}}
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSI_UNF)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_info_failure_uri_type_is_not_datasource(self):
        ''' _process_send_ds_info should fail if uri exists and is not a ds type '''
        username='test_process_send_ds_info_failure_uri_type_is_not_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','supplies':['uri']}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDSI_IURI)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_ds_info_failure_no_permission_for_post_ds_info(self):
        ''' _process_send_ds_info should fail if user has no permission for posting over this ds '''
        username='test_process_send_ds_info_failure_no_permission_for_post_ds_info'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':None}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.ds',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_ds_info_success_msg_supplies_none(self):
        ''' _process_send_ds_info should succeed. if no supplies are sent, no action is done. '''
        username='test__process_send_ds_info_success_msg_supplies_none'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':None}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(cassapidatasource.get_last_datasource_supplies_count(did=ds['did']),[])
        authorization.authorize_request = auth_req_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))

    def test__process_send_ds_info_success_msg_supplies_none_with_global_uri(self):
        ''' _process_send_ds_info should succeed. if no supplies are sent, no action is done. '''
        username='test__process_send_ds_info_success_msg_supplies_none_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':system.ds','supplies':None}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='system.ds')
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(cassapidatasource.get_last_datasource_supplies_count(did=ds['did']),[])
        authorization.authorize_request = auth_req_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='system.ds')
        self.assertIsNotNone(uri_info)
        self.assertEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))

    def test__process_send_ds_info_success_msg_supplies_some_uris(self):
        ''' _process_send_ds_info should succeed and set ds supplies for first time. '''
        username='test__process_send_ds_info_success_msg_supplies_some_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1','uri.2','uri.3']}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg['payload']['supplies'])
        authorization.authorize_request = auth_req_bck
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(isinstance(resp.imc_messages['unrouted'][0], messages.MonitorIdentifiedUrisMessage))
        self.assertEqual(resp.imc_messages['unrouted'][0].did, ds['did'])

    def test__process_send_ds_info_success_msg_supplies_some_uris_ds_has_the_same_uris_already(self):
        ''' _process_send_ds_info should succeed, but if ds already has the same supplies, dont set them again '''
        username='test__process_send_ds_info_success_msg_supplies_some_uris_ds_has_the_same_uris_already'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1','uri.2','uri.3']}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(isinstance(resp.imc_messages['unrouted'][0], messages.MonitorIdentifiedUrisMessage))
        self.assertEqual(resp.imc_messages['unrouted'][0].did, ds['did'])
        msg2={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1','uri.2','uri.3']}}
        resp=message._process_send_ds_info(passport=psp, message=msg2)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg2['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg2['seq']))
        self.assertEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        authorization.authorize_request = auth_req_bck

    def test__process_send_ds_info_success_msg_supplies_some_uris_ds_has_different_uris(self):
        ''' _process_send_ds_info should succeed, and update supplies if ds has a different set '''
        username='test__process_send_ds_info_success_msg_supplies_some_uris_ds_has_different_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1','uri.2','uri.3']}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(isinstance(resp.imc_messages['unrouted'][0], messages.MonitorIdentifiedUrisMessage))
        self.assertEqual(resp.imc_messages['unrouted'][0].did, ds['did'])
        msg2={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1']}}
        resp=message._process_send_ds_info(passport=psp, message=msg2)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),2)
        self.assertEqual(ds_supplies_list[0].supplies, msg2['payload']['supplies'])
        self.assertEqual(ds_supplies_list[1].supplies, msg['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg2['seq']))
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(isinstance(resp.imc_messages['unrouted'][0], messages.MonitorIdentifiedUrisMessage))
        self.assertEqual(resp.imc_messages['unrouted'][0].did, ds['did'])
        authorization.authorize_request = auth_req_bck

    def test__process_send_ds_info_success_msg_supplies_none_ds_has_some_uris_already(self):
        ''' _process_send_ds_info should succeed, but if msg has no supplies, no update should be made '''
        username='test__process_send_ds_info_success_msg_supplies_none_ds_has_some_uris_already'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':['uri.1','uri.2','uri.3']}}
        ds = datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        auth_req_bck=authorization.authorize_request
        operation_bck=operation.process_operation
        def auth_mock(request, passport, did):
            return True
        authorization.authorize_request = auth_mock
        resp=message._process_send_ds_info(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg['seq']))
        self.assertNotEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertTrue(isinstance(resp.imc_messages['unrouted'][0], messages.MonitorIdentifiedUrisMessage))
        self.assertEqual(resp.imc_messages['unrouted'][0].did, ds['did'])
        msg2={'v':1,'action':Messages.SEND_DS_INFO.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','supplies':None}}
        resp=message._process_send_ds_info(passport=psp, message=msg2)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        ds_supplies_list = cassapidatasource.get_last_datasource_supplies_count(did=ds['did'], count=10)
        self.assertTrue(len(ds_supplies_list),1)
        self.assertEqual(ds_supplies_list[0].supplies, msg['payload']['supplies'])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, uuid.UUID(msg2['seq']))
        self.assertEqual(resp.imc_messages['unrouted'],[])
        self.assertEqual(resp.imc_messages['routed'],{})
        authorization.authorize_request = auth_req_bck

    def test__process_send_dp_data_failure_invalid_message(self):
        ''' _process_send_dp_data should fail if message is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ELFD)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_different_message_passed(self):
        ''' _process_send_dp_data should fail if message is not of type SEND_DP_DATA '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ELFD)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_user_not_found(self):
        ''' _process_send_dp_data should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'89'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_agent_not_found(self):
        ''' _process_send_dp_data should fail if agent does not exist '''
        username='test_process_send_dp_data_failure_agent_not_found'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = AgentPassport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'79'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_no_permission_for_modifying_global_uri_of_non_existent_user(self):
        ''' _process_send_dp_data should fail if uri is global from other user '''
        username_owner='test__process_send_dp_data_failure_no_permission_for_modifying_global_uri_of_non_existent_user_non_existent'
        username='test__process_send_dp_data_failure_no_permission_for_modifying_global_uri_of_non_existent_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'],sid=uuid.uuid4(), aid=agent['aid'],pv=1)
        uri=username_owner+':uri'
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':uri,'t':timeuuid.uuid1().hex,'content':'70'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_dp_data_failure_no_permission_for_modifying_foreign_uri_of_existing_user(self):
        ''' _process_send_dp_data should fail if uri is global from other user '''
        username_owner='test__process_send_dp_data_failure_no_permission_for_modifying_foreign_uri_of_existing_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_reg=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_reg)
        username='test__process_send_dp_data_failure_no_permission_for_modifying_foreign_uri_of_existing_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'],sid=uuid.uuid4(), aid=agent['aid'],pv=1)
        uri=username_owner+':uri'
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':uri,'t':timeuuid.uuid1().hex,'content':'70'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_dp_data_failure_no_permission_for_dp_creation(self):
        ''' _process_send_dp_data should fail if agent has no permission for dp creation '''
        username='test_process_send_dp_data_failure_no_permission_for_dp_creation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'],sid=uuid.uuid4(), aid=agent['aid'],pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'70'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_no_permission_for_uri_mutation(self):
        ''' _process_send_dp_data should fail if user has no permission for uri mutation '''
        username='test_process_send_dp_data_failure_no_permission_for_uri_mutation'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_VOID_RELATION))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_no_permission_for_post_dp_data(self):
        ''' _process_send_dp_data should fail if user has no permission for posting over this dp '''
        username='test_process_send_dp_data_failure_no_permission_for_post_dp_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATAPOINT_RELATION))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ATDPD_RE)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_dp_data_failure_incompatible_uri_type(self):
        ''' _process_send_dp_data should fail if uri exists and is not void or dp type '''
        username='test_process_send_dp_data_failure_incompatible_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.void','t':timeuuid.uuid1().hex,'content':'70'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='system.void',type=vertex.USER_DATASOURCE_RELATION))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_IURI)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_dp_data_failure_error_creating_dp(self):
        ''' _process_send_dp_data should fail if dp creationg fails '''
        username='test_process_send_dp_data_failure_error_creating_dp'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'70'}}
        res_msg=messages. ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        dp_creation_bck=datapointapi.create_user_datapoint
        def dp_creation_mock(uid, datapoint_uri):
            return None
        datapointapi.create_user_datapoint = dp_creation_mock
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSDPD_ECDP)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri','t':timeuuid.uuid1().hex,'content':'content'}}
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SDPD_ICNT)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.dp','t':timeuuid.uuid1().hex,'content':'-1.3e8'}}
        operation_bck=operation.process_operation
        def operation_mock(op):
            raise Exception()
        operation.process_operation=operation_mock
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error.value, Errors.UNKNOWN.value)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_ERROR)
        self.assertEqual(resp.imc_messages,{'routed':{},'unrouted':[]})
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.dp','t':timeuuid.uuid1().hex,'content':'77.5'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_dp_data_success_dp_did_not_exist_previously_with_global_uri(self):
        ''' _process_send_dp_data should succeed and create the user dp '''
        username='test__process_send_dp_data_success_dp_did_not_exist_previously_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri='system.dp'
        global_uri=username+':'+uri
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':global_uri,'t':timeuuid.uuid1().hex,'content':'77.5'}}
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=uri)
        self.assertIsNotNone(uri_info)
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)

    def test__process_send_dp_data_success_dp_already_existed(self):
        ''' _process_send_dp_data should succeed using the existing datapoint '''
        username='test_process_send_dp_data_success_dp_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.dp','t':timeuuid.uuid1().hex,'content':'-32.0'}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertIsNotNone(datapoint)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for item in msgs:
            try:
                retrieved_messages[item._type_.value]+=1
            except KeyError:
                retrieved_messages[item._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=msg['payload']['uri'])
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['id'],datapoint['pid'])

    def test__process_send_dp_data_success_dp_already_existed_with_global_uri(self):
        ''' _process_send_dp_data should succeed using the existing datapoint '''
        username='test__process_send_dp_data_success_dp_already_existed_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri='system.dp'
        global_uri=username+':'+uri
        msg={'v':1,'action':Messages.SEND_DP_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':global_uri,'t':timeuuid.uuid1().hex,'content':'-32.0'}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=uri)
        self.assertIsNotNone(datapoint)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        resp=message._process_send_dp_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for item in msgs:
            try:
                retrieved_messages[item._type_.value]+=1
            except KeyError:
                retrieved_messages[item._type_.value]=1
        self.assertEqual(expected_messages,retrieved_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=uri)
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['id'],datapoint['pid'])

    def test__process_send_multi_data_failure_invalid_message(self):
        ''' _process_send_multi_data should fail if message is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SMTD_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)

    def test__process_send_multi_data_failure_different_message_passed(self):
        ''' _process_send_multi_data should fail if message is not of type SEND_MULTI_DATA '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_SMTD_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_user_not_found_new_datasource_auth_failed(self):
        ''' _process_send_multi_data should fail if user does not exist and a new ds uri has to be created '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri','type':vertex.DATASOURCE,'content':'content'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_agent_not_found_new_datasource_auth_failed(self):
        ''' _process_send_multi_data should fail if agent does not exist '''
        username='test_process_send_multi_data_failure_agent_not_found_new_ds_auth_failed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = AgentPassport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri','type':vertex.DATASOURCE,'content':'content'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_user_not_found_new_datapoint_auth_failed(self):
        ''' _process_send_multi_data should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_agent_not_found_new_datapoint_auth_failed(self):
        ''' _process_send_multi_data should fail if agent does not exist '''
        username='test_process_send_multi_data_failure_agent_not_found_new_dp_auth_failed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        psp = AgentPassport(uid=user_reg['uid'],aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri','type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ANUDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_global_uri_of_non_existent_user(self):
        ''' _process_send_multi_data should fail if uri is a global uri from a non existent user '''
        username_owner='test__process_send_multi_data_failure_global_uri_of_non_existent_user_non_existent'
        username='test__process_send_multi_data_failure_global_uri_of_non_existent_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri=username_owner+':uri'
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':uri,'type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_global_uri_of_foreign_existent_user(self):
        ''' _process_send_multi_data should fail if uri is a global uri from a foreign existent user '''
        username_owner='test__process_send_multi_data_failure_global_uri_of_foreign_existent_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_send_multi_data_failure_global_uri_of_foreign_existent_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        uri=username_owner+':uri'
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':uri,'type':vertex.DATAPOINT,'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_EUGURI)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_send_multi_data should fail if uri type is not datasource nor datapoint '''
        username='test_process_send_multi_data_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.widget','type':vertex.DATAPOINT,'content':'44'}]}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_ONAOU)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_no_permission_for_post_datapoint_data(self):
        ''' _process_send_multi_data should fail if user has no permission to post datapoint data'''
        username='test_process_send_multi_data_failure_no_permission_for_post_datapoint_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ATDPD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_failure_no_permission_for_post_datasource_data(self):
        ''' _process_send_multi_data should fail if user has no permission to post datasource data'''
        username='test_process_send_multi_data_failure_no_permission_for_post_datasource_data'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ATDSD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_success_new_datasource(self):
        ''' _process_send_multi_data should succeed and create the new datasource '''
        username='test_process_send_multi_data_success_new_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'content 5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(retrieved_messages,expected_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATASOURCE)

    def test__process_send_multi_data_success_new_datasource_with_global_uri(self):
        ''' _process_send_multi_data should succeed and create the new datasource '''
        username='test_process_send_multi_data_success_new_datasource_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        local_uri='uri.ds'
        global_uri=':'.join((username,local_uri))
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':global_uri,'type':vertex.DATASOURCE, 'content':'content 5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(retrieved_messages,expected_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT,'content':'5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(retrieved_messages, expected_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        self.assertEqual(uri_info['type'],vertex.DATAPOINT)

    def test__process_send_multi_data_success_new_datapoint_with_global_uri(self):
        ''' _process_send_multi_data should succeed and create the new datapoint '''
        username='test__process_send_multi_data_success_new_datapoint_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        local_uri='uri.dp'
        global_uri=':'.join((username,local_uri))
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':global_uri,'type':vertex.DATAPOINT,'content':'5'}]}}
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
        self.assertIsNone(uri_info)
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:2,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
        self.assertEqual(retrieved_messages, expected_messages)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1

    def test__process_send_multi_data_success_datasource_already_existed_with_global_uri(self):
        ''' _process_send_multi_data should succeed and store content in already existing ds '''
        username='test_process_send_multi_data_success_datasource_already_existed_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        local_uri='uri.ds'
        global_uri=':'.join((username,local_uri))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=local_uri)
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':global_uri,'type':vertex.DATASOURCE, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:1,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
 
    def test__process_send_multi_data_success_datapoint_already_existed(self):
        ''' _process_send_multi_data should and store content in datapoint '''
        username='test_process_send_multi_data_success_datapoint_already_existed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.URIS_UPDATED_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
 
    def test__process_send_multi_data_failure_datapoint_already_existed_but_content_is_not_numeric(self):
        ''' _process_send_multi_data should fail if we try to store non numeric content into a datapoint '''
        username='test_process_send_multi_data_failure_datapoint_already_existed_but_content_is_not_numeric'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':'uri.dp','type':vertex.DATASOURCE, 'content':'value: 44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_UCNV)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_send_multi_data_success_datapoint_already_existed_with_global_uri(self):
        ''' _process_send_multi_data should and store content in datapoint '''
        username='test_process_send_multi_data_success_datapoint_already_existed_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        local_uri='uri.dp'
        global_uri=':'.join((username,local_uri))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=local_uri)
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri=local_uri)
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_MULTI_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'t':timeuuid.uuid1().hex,'uris':[{'uri':global_uri,'type':vertex.DATAPOINT, 'content':'44'}]}}
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.URIS_UPDATED_MESSAGE.value:1
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for msg in msgs:
            try:
                retrieved_messages[msg._type_.value]+=1
            except KeyError:
                retrieved_messages[msg._type_.value]=1
 
    def test__process_send_multi_data_success_existing_and_non_existing_uris(self):
        ''' _process_send_multi_data should succeed, creating uris when they do not exist and updating the existing ones '''
        username='test_process_send_multi_data_success_existing_and_non_existing_uris'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={
            'v':1,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':timeuuid.TimeUUID().hex,
            'irt':None,
            'payload':{
                't':timeuuid.uuid1().hex,
                'uris':[
                    {'uri':'uri.dp','type':vertex.DATAPOINT, 'content':'-4.4'},
                    {'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'value: 44'},
                    {'uri':'uri.new_dp','type':vertex.DATAPOINT, 'content':'44'},
                    {'uri':'uri.new_ds','type':vertex.DATASOURCE, 'content':'new value: 44'},
                    ]
            }
        }
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:6,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:2,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for item in msgs:
            try:
                retrieved_messages[item._type_.value]+=1
            except KeyError:
                retrieved_messages[item._type_.value]=1
        for item in msgs:
            if item._type_ == messages.Messages.HOOK_NEW_URIS_MESSAGE:
                self.assertEqual(len(item.uris),2)
                self.assertTrue(any(reg['uri'] == 'uri.new_ds' for reg in item.uris))
                self.assertTrue(any(reg['uri'] == 'uri.new_dp' for reg in item.uris))
            elif item._type_ == messages.Messages.URIS_UPDATED_MESSAGE:
                self.assertEqual(len(item.uris),2)
                self.assertTrue(any(reg['uri'] == 'uri.ds' for reg in item.uris))
                self.assertTrue(any(reg['uri'] == 'uri.dp' for reg in item.uris))
        self.assertEqual(retrieved_messages, expected_messages)
        did=datasource['did']
        existing_ds_stats=cassapidatasource.get_datasource_stats(did=did)
        date=existing_ds_stats.last_received
        self.assertEqual(date,uuid.UUID(msg['payload']['t']))
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

    def test__process_send_multi_data_success_existing_and_non_existing_uris_with_global_uri(self):
        ''' _process_send_multi_data should succeed, creating uris when they do not exist and updating the existing ones '''
        username='test_process_send_multi_data_success_existing_and_non_existing_uris_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={
            'v':1,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':timeuuid.TimeUUID().hex,
            'irt':None,
            'payload':{
                't':timeuuid.uuid1().hex,
                'uris':[
                    {'uri':username+':uri.dp','type':vertex.DATAPOINT, 'content':'-4.4'},
                    {'uri':username+':uri.ds','type':vertex.DATASOURCE, 'content':'value: 44'},
                    {'uri':username+':uri.new_dp','type':vertex.DATAPOINT, 'content':'44'},
                    {'uri':username+':uri.new_ds','type':vertex.DATASOURCE, 'content':'new value: 44'},
                    ]
            }
        }
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertNotEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        expected_messages={
            messages.Messages.UPDATE_QUOTES_MESSAGE.value:6,
            messages.Messages.NEW_DP_WIDGET_MESSAGE.value:1,
            messages.Messages.NEW_DS_WIDGET_MESSAGE.value:1,
            messages.Messages.USER_EVENT_MESSAGE.value:1,
            messages.Messages.MAP_VARS_MESSAGE.value:2,
            messages.Messages.URIS_UPDATED_MESSAGE.value:1,
            messages.Messages.HOOK_NEW_URIS_MESSAGE.value:1,
        }
        retrieved_messages={}
        msgs=resp.imc_messages['unrouted']
        for item in msgs:
            try:
                retrieved_messages[item._type_.value]+=1
            except KeyError:
                retrieved_messages[item._type_.value]=1
        for item in msgs:
            if item._type_ == messages.Messages.HOOK_NEW_URIS_MESSAGE:
                self.assertEqual(len(item.uris),2)
                self.assertTrue(any(reg['uri'] == 'uri.new_ds' for reg in item.uris))
                self.assertTrue(any(reg['uri'] == 'uri.new_dp' for reg in item.uris))
            elif item._type_ == messages.Messages.URIS_UPDATED_MESSAGE:
                self.assertEqual(len(item.uris),2)
                self.assertTrue(any(reg['uri'] == 'uri.ds' for reg in item.uris))
                self.assertTrue(any(reg['uri'] == 'uri.dp' for reg in item.uris))
        self.assertEqual(retrieved_messages, expected_messages)
        did=datasource['did']
        existing_ds_stats=cassapidatasource.get_datasource_stats(did=did)
        date=existing_ds_stats.last_received
        self.assertEqual(date,uuid.UUID(msg['payload']['t']))
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
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={
            'v':1,
            'action':Messages.SEND_MULTI_DATA.value,
            'seq':timeuuid.TimeUUID().hex,
            'irt':None,
            'payload':{
                't':timeuuid.uuid1().hex,
                'uris':[
                    {'uri':'uri.dp','type':vertex.DATASOURCE, 'content':'content: -4.4'},
                    {'uri':'uri.ds','type':vertex.DATASOURCE, 'content':'value: 44'},
                    {'uri':'uri.new_dp','type':vertex.DATAPOINT, 'content':'44'},
                    {'uri':'uri.new_ds','type':vertex.DATASOURCE, 'content':'new value: 44'},
                ]
            }
        }
        resp=message._process_send_multi_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PSMTD_UCNV)
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
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
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_HTU_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'protocol error')
        self.assertEqual(resp.ws_messages[0].irt, None)

    def test__process_hook_to_uri_failure_different_message_passed(self):
        ''' _process_hook_to_uri should fail if message is not of type HOOK_TO_URI '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.SEND_DS_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','t':timeuuid.uuid1().hex,'content':'content'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_HTU_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_failure_user_not_found(self):
        ''' _process_hook_to_uri should fail if user does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, gesterrors.E_GUA_RPH_UNF)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_failure_global_uri_owner_does_not_exist(self):
        ''' _process_hook_to_uri should fail if uri is global and owner does not exist '''
        username_owner='test__process_hook_to_uri_failure_global_uri_owner_does_not_exist_owner'
        username='test__process_hook_to_uri_failure_global_uri_owner_does_not_exist'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        local_uri='system.ds'
        global_uri=':'.join((username_owner,local_uri))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':global_uri}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error,Errors.E_IWSPV1PM_PHTU_OUNF)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_success_uri_does_not_exist(self):
        ''' _process_hook_to_uri should register a pending hook for the unexistent uri '''
        username='test_process_hook_to_uri_success_uri_does_not_exist'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error.value, Errors.E_IWSPV1PM_PHTU_UNF.value)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Operation registered, but uri does not exist yet')

    def test__process_hook_to_uri_failure_global_uri_not_shared(self):
        ''' _process_hook_to_uri should fail if global uri is not shared '''
        username_owner='test__process_hook_to_uri_failure_global_uri_not_shared_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_hook_to_uri_failure_global_uri_not_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ARPH_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_success_uri_does_not_exist_global_uri_shared(self):
        ''' _process_hook_to_uri should register a pending hook for the unexistent uri '''
        username_owner='test__process_hook_to_uri_success_uri_does_not_exist_global_uri_shared_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_hook_to_uri_success_uri_does_not_exist_global_uri_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='system',perm=permissions.CAN_READ))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error.value, Errors.E_IWSPV1PM_PHTU_UNF.value)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'Operation registered, but uri does not exist yet')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_hook_to_uri should fail if uri type is not datasource nor datapoint '''
        username='test_process_hook_to_uri_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.widget'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PHTU_ONA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_failure_no_read_permission_for_datasource(self):
        ''' _process_hook_to_uri should fail if uri type is datasource and no read perm is found'''
        username='test_process_hook_to_uri_failure_no_read_permission_for_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AHTDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_success_datasource_uri(self):
        ''' _process_hook_to_uri should succeed if uri type is ds and read perm is found'''
        username='test_process_hook_to_uri_success_datasource_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp.sid])

    def test__process_hook_to_uri_success_datasource_uri_with_global_uri(self):
        ''' _process_hook_to_uri should succeed if uri type is ds and read perm is found'''
        username='test__process_hook_to_uri_success_datasource_uri_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp.sid])

    def test__process_hook_to_uri_success_datasource_uri_with_global_uri_from_other_user(self):
        ''' _process_hook_to_uri should succeed if uri type is ds and read perm is found'''
        username_owner='test__process_hook_to_uri_success_datasource_uri_with_global_uri_from_other_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        agentname=username_owner+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_owner['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_owner['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_owner['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_owner['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_owner['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        username='test__process_hook_to_uri_success_datasource_uri_with_global_uri_from_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='uri',perm=permissions.CAN_READ))
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.ds'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        #if the same session resend the message, it has no efect over hooked sids
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AHTDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_hook_to_uri_success_datapoint_uri(self):
        ''' _process_hook_to_uri should succeed if uri is dp and we have read perm over it'''
        username='test_process_hook_to_uri_success_datapoint_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp.sid])

    def test__process_hook_to_uri_success_datapoint_uri_with_global_uri(self):
        ''' _process_hook_to_uri should succeed if uri is dp and we have read perm over it'''
        username='test__process_hook_to_uri_success_datapoint_uri_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp.sid])

    def test__process_hook_to_uri_success_datapoint_uri_global_uri_from_other_user(self):
        ''' _process_hook_to_uri should succeed if uri is dp and we have read perm over it'''
        username_owner='test__process_hook_to_uri_success_datapoint_uri_global_uri_from_other_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        agentname=username_owner+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_owner['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_owner['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_owner['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_owner['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_owner['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_owner['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        username='test__process_hook_to_uri_success_datapoint_uri_global_uri_from_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='uri.dp',perm=permissions.CAN_READ))
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.dp'}}
        resp=message._process_hook_to_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))

    def test__process_unhook_from_uri_failure_invalid_message(self):
        ''' _process_unhook_from_uri should fail if message is invalid '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'key':'a message malformed'}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_UHFU_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt, None)

    def test__process_unhook_from_uri_failure_different_message_passed(self):
        ''' _process_unhook_from_uri should fail if message is not of type UNHOOK_FROM_URI '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.PROTOCOL_ERROR)
        self.assertEqual(resp.error, Errors.E_IWSPV1MM_UHFU_ELFD)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_success_uri_does_not_exist(self):
        ''' _process_unhook_from_uri should succeed even if uri does not exist '''
        psp = AgentPassport(uid=uuid.uuid4(),aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_failure_global_uri_owner_does_not_exist(self):
        ''' _process_unhook_from_uri should fail if uri is global and owner does not exist '''
        username_owner='test__process_unhook_from_uri_failure_global_uri_owner_does_not_exist_owner'
        username='test__process_unhook_from_uri_failure_global_uri_owner_does_not_exist'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PUHFU_OUNF)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_failure_global_uri_not_shared(self):
        ''' _process_unhook_from_uri should fail if uri is global and is not shared '''
        username_owner='test__process_unhook_from_uri_failure_global_uri_not_shared_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        username='test__process_unhook_from_uri_failure_global_uri_not_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_ADPH_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_success_global_uri_does_not_exist_but_shared(self):
        ''' _process_unhook_from_uri should succeed if global uri does not exist but is shared '''
        username_owner='test__process_unhook_from_uri_success_global_uri_does_not_exist_but_shared_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        username='test__process_unhook_from_uri_success_global_uri_does_not_exist_but_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='system',perm=permissions.CAN_READ))
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'Unhooked')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_unhook_from_uri should fail if uri type is not datasource nor datapoint '''
        username='test_process_unhook_from_uri_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.widget'}}
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PUHFU_ONA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_failure_no_read_permission_for_datasource(self):
        ''' _process_unhook_from_uri should fail if uri type is datasource and no read perm is found'''
        username='test_process_unhook_from_uri_failure_no_read_permission_for_datasource'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AUHFDS_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_success_datasource_uri(self):
        ''' _process_unhook_from_uri should succeed if uri type is ds and read perm is found'''
        username='test_process_unhook_from_uri_success_datasource_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[])

    def test__process_unhook_from_uri_success_datasource_uri_with_global_uri(self):
        ''' _process_unhook_from_uri should succeed if uri type is ds and read perm is found'''
        username='test_process_unhook_from_uri_success_datasource_uri_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_DATASOURCE, params={'uid':user_reg['uid'],'aid':agent['aid'],'did':datasource['did']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[])

    def test__process_unhook_from_uri_success_datasource_uri_with_global_uri_from_other_user(self):
        ''' _process_unhook_from_uri should succeed if uri type is ds and read perm is found'''
        username_owner='test_process_unhook_from_uri_success_datasource_uri_with_global_uri_from_other_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        agentname=username_owner+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_owner['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_owner['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        datasource=datasourceapi.create_datasource(uid=user_owner['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertIsNotNone(datasource)
        uri_info=graphuri.get_id(ido=user_owner['uid'], uri='uri.ds')
        self.assertIsNotNone(uri_info)
        username='test_process_unhook_from_uri_success_datasource_uri_with_global_uri_from_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='uri.ds',perm=permissions.CAN_READ))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.ds'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.ds'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatasource.get_datasource_hooks_sids(did=datasource['did']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
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
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        #res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        #self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_unhook_from_uri(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AUHFDP_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_unhook_from_uri_success_datapoint_uri(self):
        ''' _process_unhook_from_uri should succeed if uri is dp and we have read perm over it'''
        username='test_process_unhook_from_uri_success_datapoint_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[])

    def test__process_unhook_from_uri_success_datapoint_uri_with_global_uri(self):
        ''' _process_unhook_from_uri should succeed if uri is dp and we have read perm over it'''
        username='test_process_unhook_from_uri_success_datapoint_uri_with_global_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_reg['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_reg['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_USER_DATAPOINT, params={'uid':user_reg['uid'],'pid':datapoint['pid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[])

    def test__process_unhook_from_uri_success_datapoint_uri_with_global_uri_from_other_user(self):
        ''' _process_unhook_from_uri should succeed if uri is dp and we have read perm over it'''
        username_owner='test__process_unhook_from_uri_success_datapoint_uri_with_global_uri_from_other_user_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        self.assertTrue(userapi.confirm_user(email=email, code=user_owner['code']))
        agentname=username_owner+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_owner['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_owner['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        res_msg=messages.ResourceAuthorizationUpdateMessage(operation=Operations.NEW_AGENT, params={'uid':user_owner['uid'],'aid':agent['aid']})
        self.assertIsNotNone(msgapi.process_message(res_msg))
        datapoint=datapointapi.create_user_datapoint(uid=user_owner['uid'], datapoint_uri='uri.dp')
        self.assertIsNotNone(datapoint)
        uri_info=graphuri.get_id(ido=user_owner['uid'], uri='uri.dp')
        self.assertIsNotNone(uri_info)
        username='test_process_unhook_from_uri_success_datapoint_uri_with_global_uri_from_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        self.assertTrue(userapi.confirm_user(email=email, code=user_reg['code']))
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_owner['uid'],dest_uid=user_reg['uid'],uri='uri',perm=permissions.CAN_READ))
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp1 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp2 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        psp3 = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.HOOK_TO_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.dp'}}
        resp=message._process_hook_to_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp1.sid])
        resp=message._process_hook_to_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid]))
        resp=message._process_hook_to_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp1.sid,psp2.sid,psp3.sid]))
        msg={'v':1,'action':Messages.UNHOOK_FROM_URI.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':uri.dp'}}
        resp=message._process_unhook_from_uri(psp1, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),sorted([psp3.sid,psp2.sid]))
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        # if we receive the same unhook, no problem
        resp=message._process_unhook_from_uri(psp2, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[psp3.sid])
        resp=message._process_unhook_from_uri(psp3, msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_OK)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(cassapidatapoint.get_datapoint_hooks_sids(pid=datapoint['pid']),[])

    def test__process_request_data_failure_uri_does_not_exist(self):
        ''' _process_request_data should fail if uri does not exist '''
        username='test_process_request_data_failure_uri_does_not_exist'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'system.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_UNF)
        self.assertEqual(resp.status, status.RESOURCE_NOT_FOUND)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'uri system.ds does not exist')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_global_uri_owner_does_not_exist(self):
        ''' _process_request_data should fail if uri owner does not exist '''
        username_owner='test__process_request_data_failure_global_uri_owner_does_not_exist_owner'
        username='test__process_request_data_failure_global_uri_owner_does_not_exist'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_OUNF)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_global_uri_is_not_shared(self):
        ''' _process_request_data should fail if uri owner does not exist '''
        username_owner='test__process_request_data_failure_global_uri_is_not_shared_owner'
        password='password_for_the_user'
        email=username_owner+'@komlog.org'
        user_owner=userapi.create_user(username=username_owner, password=password, email=email)
        self.assertIsNotNone(user_owner)
        username='test__process_request_data_failure_global_uri_is_not_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username_owner+':system.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGU_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_operation_not_allowed_for_uri_type(self):
        ''' _process_request_data should fail if uri type is not valid '''
        username='test_process_request_data_failure_operation_not_allowed_for_uri_type'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.widget','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ONA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'operation not allowed on this uri: uri.widget')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_operation_not_allowed_for_uri_type_global_uri_from_other_user_shared(self):
        ''' _process_request_data should fail if uri type is not valid '''
        username='test__process_request_data_failure_operation_not_allowed_for_uri_type_global_uri_from_other_user_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        username_req=username+'_request'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'],dest_uid=user_req['uid'],uri='uri',perm=permissions.CAN_READ))
        agentname=username_req+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_req['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_req['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.widget','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ONA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_operation_not_allowed_for_uri_type_global_uri_from_other_user_not_shared(self):
        ''' _process_request_data should fail if uri type is not valid '''
        username='test__process_request_data_failure_operation_not_allowed_for_uri_type_global_uri_from_other_user_not_shared'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.widget',type=vertex.USER_WIDGET_RELATION))
        username_req=username+'_request'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        agentname=username_req+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_req['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_req['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.widget','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGU_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_ds_uri(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test_process_request_data_failure_access_denied_to_ds_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.ds',type=vertex.USER_DATASOURCE_RELATION))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDSD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'msg exec denied')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_ds_uri_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test__process_request_data_failure_access_denied_to_ds_uri_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.ds',type=vertex.USER_DATASOURCE_RELATION))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDSD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'msg exec denied')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_ds_uri_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test__process_request_data_failure_access_denied_to_ds_uri_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        username_req='test__process_request_data_failure_access_denied_to_ds_uri_with_global_uri_other_user_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDSD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_dp_uri(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test_process_request_data_failure_access_denied_to_dp_uri'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.dp',type=vertex.USER_DATAPOINT_RELATION))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDPD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'msg exec denied')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_dp_uri_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test_process_request_data_failure_access_denied_to_dp_uri_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        self.assertTrue(graphuri.new_uri(ido=user_reg['uid'], idd=uuid.uuid4(), uri='uri.dp',type=vertex.USER_DATAPOINT_RELATION))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDPD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'msg exec denied')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_denied_to_dp_uri_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user has no access to uri'''
        username='test_process_request_data_failure_access_denied_to_dp_uri_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':timeuuid.uuid1().hex,'end':timeuuid.uuid1().hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, autherrors.E_ARA_AGDPD_RE)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertEqual(resp.imc_messages['routed'], {})
        self.assertEqual(resp.imc_messages['unrouted'], [])
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], response.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'msg exec denied')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])

    def test__process_request_data_failure_access_to_data_range_not_allowed_ds(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_ds'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri uri.ds is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_not_allowed_ds_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_ds_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri '+username+':uri.ds is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_not_allowed_ds_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_ds_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+2*86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'],dest_uid=user_req['uid'],uri='uri.ds',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_reg['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri '+username+':uri.ds is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_not_allowed_dp(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_dp'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+2*86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri uri.dp is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_not_allowed_dp_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_dp_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+2*86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri '+username+':uri.dp is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_not_allowed_dp_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user wants to access a non reachable data range because of limitations '''
        username='test_process_request_data_failure_access_to_data_range_not_allowed_dp_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1(seconds=time.time()+2*86400)
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'],dest_uid=user_req['uid'],uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ANA)
        self.assertEqual(resp.status, status.MESSAGE_EXECUTION_DENIED)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.ws_messages[0].reason, 'Your interval requested for uri '+username+':uri.dp is wider than the limit allowed: '+timeuuid.get_isodate_from_uuid(min_ts)+'. Access to data is not allowed before that date.')
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_ds(self):
        ''' _process_request_data should fail if user wants to access a data range that has limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_ds_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user wants to access a data range that has limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_ds_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user wants to access a data range that has limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri.ds',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_ds_no_interval_received(self):
        ''' _process_request_data should limit interval if user has interval bounds and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds_no_interval_received'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        count=100
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':None,'end':None,'count':count}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_failure_access_to_data_range_limited_ds_no_interval_received_with_global_uri_same_user(self):
        ''' _process_request_data should limit interval if user has interval bounds and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds_no_interval_received_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        count=100
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':None,'end':None,'count':count}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_failure_access_to_data_range_limited_ds_no_interval_received_with_global_uri_other_user(self):
        ''' _process_request_data should limit interval if user has interval bounds and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_ds_no_interval_received_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri.ds',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        count=100
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':None,'end':None,'count':count}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_failure_access_to_data_range_limited_dp(self):
        ''' _process_request_data should fail if user wants to access a data range with limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_dp_with_global_uri_same_user(self):
        ''' _process_request_data should fail if user wants to access a data range with limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_dp_with_global_uri_other_user(self):
        ''' _process_request_data should fail if user wants to access a data range with limitations within it '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)

    def test__process_request_data_failure_access_to_data_range_limited_dp_no_interval_received(self):
        ''' _process_request_data should return a limited range if user has interval bounds limits, and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp_no_interval_received'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=200
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':start,'end':end,'count':count}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_failure_access_to_data_range_limited_dp_no_interval_received_with_global_uri_same_user(self):
        ''' _process_request_data should return a limited range if user has interval bounds limits, and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp_no_interval_received_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=200
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start,'end':end,'count':count}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_failure_access_to_data_range_limited_dp_no_interval_received_with_global_uri_other_user(self):
        ''' _process_request_data should return a limited range if user has interval bounds limits, and no interval was received in request, only count '''
        username='test_process_request_data_failure_access_to_data_range_limited_dp_no_interval_received_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        #se the date limit for data retrieval
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        uid=user_reg['uid']
        min_ts=timeuuid.uuid1()
        self.assertTrue(cassapiiface.insert_user_iface_deny(uid=uid, iface=iface, content=min_ts.hex))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=200
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start,'end':end,'count':count}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.E_IWSPV1PM_PRDI_ALP)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_success_no_limitations_ds(self):
        ''' _process_request_data should succeed if user want a data range than can access '''
        username='test_process_request_data_success_no_limitations_ds'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_ds_with_global_uri_same_user(self):
        ''' _process_request_data should succeed if user want a data range than can access '''
        username='test_process_request_data_success_no_limitations_ds_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_ds_with_global_uri_other_user(self):
        ''' _process_request_data should succeed if user want a data range than can access '''
        username='test_process_request_data_success_no_limitations_ds_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_ds_count_passed(self):
        ''' _process_request_data should succeed if user want some rows '''
        username='test_process_request_data_success_no_limitations_ds_count_passed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=400
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.ds','start':start,'end':end,'count':count}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename=msg['payload']['uri'])
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)

    def test__process_request_data_success_no_limitations_ds_count_passed_with_global_uri_same_user(self):
        ''' _process_request_data should succeed if user want some rows '''
        username='test_process_request_data_success_no_limitations_ds_count_passed_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=400
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start,'end':end,'count':count}}
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_ds_count_passed_with_global_uri_other_user(self):
        ''' _process_request_data should succeed if user want some rows '''
        username='test_process_request_data_success_no_limitations_ds_count_passed_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datasource=datasourceapi.create_datasource(uid=user_reg['uid'], aid=agent['aid'], datasourcename='uri.ds')
        self.assertTrue(resupdate.new_datasource({'uid':datasource['uid'],'did':datasource['did']}))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=400
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.ds','start':start,'end':end,'count':count}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.ds','type':vertex.DATASOURCE,'id':datasource['did']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp(self):
        ''' _process_request_data should success if user wants a data range without access limitations '''
        username='test_process_request_data_success_no_limitations_dp'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp_with_global_uri_same_user(self):
        ''' _process_request_data should success if user wants a data range without access limitations '''
        username='test_process_request_data_success_no_limitations_dp_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp_with_global_uri_other_user(self):
        ''' _process_request_data should success if user wants a data range without access limitations '''
        username='test_process_request_data_success_no_limitations_dp_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=timeuuid.uuid1(seconds=time.time()-86400)
        end=timeuuid.uuid1(seconds=time.time()+86400)
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start.hex,'end':end.hex,'count':None}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, start)
        self.assertEqual(resp.imc_messages['unrouted'][0].ie, end)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp_count_passed(self):
        ''' _process_request_data should success if user wants some rows '''
        username='test_process_request_data_success_no_limitations_dp_count_passed'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=2332
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':'uri.dp','start':start,'end':end,'count':count}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri=msg['payload']['uri'])
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp_count_passed_with_global_uri_same_user(self):
        ''' _process_request_data should success if user wants some rows '''
        username='test_process_request_data_success_no_limitations_dp_count_passed_with_global_uri_same_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        psp = AgentPassport(uid=user_reg['uid'], aid=agent['aid'],sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=2332
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start,'end':end,'count':count}}
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

    def test__process_request_data_success_no_limitations_dp_count_passed_with_global_uri_other_user(self):
        ''' _process_request_data should success if user wants some rows '''
        username='test_process_request_data_success_no_limitations_dp_count_passed_with_global_uri_other_user'
        password='password_for_the_user'
        email=username+'@komlog.org'
        user_reg=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user_reg)
        agentname=username+'_agent'
        version='agent_version'
        agent=agentapi.create_agent(uid=user_reg['uid'],agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(agentapi.activate_agent(aid=agent['aid']))
        datapoint=datapointapi.create_user_datapoint(uid=user_reg['uid'], datapoint_uri='uri.dp')
        self.assertTrue(resupdate.new_user_datapoint({'uid':datapoint['uid'],'pid':datapoint['pid']}))
        username_req=username+'_req'
        password='password_for_the_user'
        email=username_req+'@komlog.org'
        user_req=userapi.create_user(username=username_req, password=password, email=email)
        self.assertIsNotNone(user_req)
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=user_reg['uid'], dest_uid=user_req['uid'], uri='uri',perm=permissions.CAN_READ))
        psp = AgentPassport(uid=user_req['uid'], aid=uuid.uuid4(),sid=uuid.uuid4(),pv=1)
        start=None
        end=None
        count=2332
        msg={'v':1,'action':Messages.REQUEST_DATA.value,'seq':timeuuid.TimeUUID().hex, 'irt':None, 'payload':{'uri':username+':uri.dp','start':start,'end':end,'count':count}}
        resp=message._process_request_data(passport=psp, message=msg)
        self.assertTrue(isinstance(resp, response.WSocketIfaceResponse))
        self.assertEqual(resp.error, Errors.OK)
        self.assertEqual(resp.status, status.MESSAGE_ACCEPTED_FOR_PROCESSING)
        self.assertTrue(len(resp.ws_messages),1)
        self.assertTrue(isinstance(resp.ws_messages[0], v1msg.GenericResponse))
        self.assertEqual(resp.ws_messages[0].status,resp.status)
        self.assertEqual(resp.ws_messages[0].error, resp.error)
        self.assertEqual(resp.ws_messages[0].irt.hex, msg['seq'])
        self.assertEqual(resp.imc_messages['routed'],{})
        self.assertEqual(len(resp.imc_messages['unrouted']),1)
        self.assertEqual(resp.imc_messages['unrouted'][0].type, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(resp.imc_messages['unrouted'][0].sid, psp.sid)
        self.assertEqual(resp.imc_messages['unrouted'][0].uri, {'uri':'uri.dp','type':vertex.DATAPOINT,'id':datapoint['pid']})
        self.assertEqual(resp.imc_messages['unrouted'][0].ii, timeuuid.LOWEST_TIME_UUID)
        self.assertNotEqual(resp.imc_messages['unrouted'][0].ie, timeuuid.LOWEST_TIME_UUID)
        self.assertEqual(resp.imc_messages['unrouted'][0].irt.hex, msg['seq'])

