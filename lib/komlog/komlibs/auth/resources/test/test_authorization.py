import unittest
import uuid
from komlog.komlibs.auth import permissions, exceptions
from komlog.komlibs.auth.errors import Errors
from komlog.komlibs.auth.resources import authorization
from komlog.komcass.api import permission as cassapiperm
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komfig import logging

pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

class AuthResourcesAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.resources.authorization tests '''

    def setUp(self):
        username = 'test_komlibs.auth.resources.authorization_user'
        password = 'password'
        email = 'test_komlibs.auth.resources.authorization_user@komlog.org'
        try:
            uid = userapi.get_uid(username=username)
            self.user=userapi.get_user_config(uid=uid)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)


    def test_authorize_get_agent_config_success(self):
        ''' authorize_get_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_get_agent_config(uid=uid, aid=aid))

    def test_authorize_get_agent_config_failure(self):
        ''' authorize_get_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_agent_config(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGAC_RE)

    def test_authorize_get_datasource_config_success(self):
        ''' authorize_get_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_get_datasource_config(uid=uid, did=did))

    def test_authorize_get_datasource_config_shared_uri_success(self):
        ''' authorize_get_datasource_config should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datasource_config_shared_uri_success'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_get_datasource_config(uid=dest_uid, did=datasource['did']))

    def test_authorize_get_datasource_config_failure(self):
        ''' authorize_get_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_config(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSC_RE)

    def test_authorize_get_datasource_config_shared_uri_failure_not_containing_uri(self):
        ''' authorize_get_datasource_config should fail if user shared an uri not containing the ds  '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datasource_config_shared_uri_failure_not_containing_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri.datasource.some_results'
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_config(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSC_RE)

    def test_authorize_get_datasource_config_shared_uri_failure_different_user(self):
        ''' authorize_get_datasource_config should succeed if user shared a uri containing it '''
        dest_uid=uuid.uuid4()
        username = 'test_authorize_get_datasource_config_shared_uri_failure_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_config(uid=self.user['uid'], did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSC_RE)

    def test_authorize_put_datasource_config_success(self):
        ''' authorize_put_datasource_config should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_put_datasource_config(uid=uid, did=did))

    def test_authorize_put_datasource_config_failure(self):
        ''' authorize_put_datasource_config should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_datasource_config(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDSC_RE)

    def test_authorize_get_datasource_data_success(self):
        ''' authorize_get_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_get_datasource_data(uid=uid, did=did))

    def test_authorize_get_datasource_data_shared_uri_success(self):
        ''' authorize_get_datasource_data should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datasource_data_shared_uri_success'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_get_datasource_data(uid=dest_uid, did=datasource['did']))

    def test_authorize_get_datasource_data_failure(self):
        ''' authorize_get_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSD_RE)

    def test_authorize_get_datasource_data_shared_uri_failure_non_containing_uri(self):
        ''' authorize_get_datasource_data should fail if user shared a uri not containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datasource_data_shared_uri_failure_non_containing_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri.datasource.something'
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSD_RE)

    def test_authorize_get_datasource_data_shared_uri_failure_different_user(self):
        ''' authorize_get_datasource_data should fail if user shared a uri to other user '''
        dest_uid=uuid.uuid4()
        username = 'test_authorize_get_datasource_data_shared_uri_failure_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri.datasource.something'
        datasourcename='root.uri.datasource.something'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datasource_data(uid=self.user['uid'], did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDSD_RE)

    def test_authorize_post_datasource_data_success(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did))

    def test_authorize_post_datasource_data_failure(self):
        ''' authorize_post_datasource_data should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datasource_data_failure_no_user_agent_perm(self):
        ''' authorize_post_datasource_data should fail if not user_agent perm is found '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datasource_data_failure_no_user_datasource_perm(self):
        ''' authorize_post_datasource_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datasource_data(uid=uid, aid=aid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDSD_RE)

    def test_authorize_post_datapoint_data_failure_invalid_aid(self):
        ''' authorize_post_datapoint_data should fail if aid is invalid '''
        uid=uuid.uuid4()
        aids=[None, 'text',12, 222.22, {'a':'dict'}, {'set'}, ['a','list'],('tuple','yes'),{uuid.uuid4()},[uuid.uuid4(),],(uuid.uuid4(),),uuid.uuid1(), uuid.uuid4().hex]
        pid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.AuthorizationException) as cm:
                authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_ANF)

    def test_authorize_post_datapoint_data_success(self):
        ''' authorize_post_datapoint_data should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid))

    def test_authorize_post_datapoint_data_failure_no_permission_over_datapoint(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over datapoint '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_post_datapoint_data_failure_no_permission_over_agent(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over agent '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_post_datapoint_data_failure_no_permission_over_agent_nor_datapoint(self):
        ''' authorize_post_datapoint_data should fail if user has no permission over agent nor dp '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_post_datapoint_data(uid=uid, aid=aid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ATDPD_RE)

    def test_authorize_new_datasource_success(self):
        ''' authorize_new_datasource should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_new_datasource(uid=uid, aid=aid))

    def test_authorize_new_datasource_failure(self):
        ''' authorize_new_datasource should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANDS_RE)

    def test_authorize_get_datapoint_data_success(self):
        ''' authorize_get_datapoint_data should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_get_datapoint_data(uid=uid, pid=pid))

    def test_authorize_get_datapoint_data_shared_uri_success(self):
        ''' authorize_get_datapoint_data should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_data_shared_uri_success'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_get_datapoint_data(uid=dest_uid, pid=datapoint['pid']))

    def test_authorize_get_datapoint_data_failure(self):
        ''' authorize_get_datapoint_data should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPD_RE)

    def test_authorize_get_datapoint_data_shared_uri_failure_non_containing_uri(self):
        ''' authorize_get_datapoint_data should fail if user shared a uri not containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_data_shared_uri_failure_non_containing_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri.some.thing'
        datapointname='root.uri.mydatapoint'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPD_RE)

    def test_authorize_get_datapoint_data_shared_uri_failure_different_user(self):
        ''' authorize_get_datapoint_data should fail if user shared a uri to a different user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_data_shared_uri_failure_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri.some.thing'
        datapointname='root.uri.some.thing'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_data(uid=uuid.uuid4(), pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPD_RE)

    def test_authorize_get_datapoint_config_success(self):
        ''' authorize_get_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_get_datapoint_config(uid=uid, pid=pid))

    def test_authorize_get_datapoint_config_shared_uri_success(self):
        ''' authorize_get_datapoint_data should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_config_shared_uri_success'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_get_datapoint_config(uid=dest_uid, pid=datapoint['pid']))

    def test_authorize_get_datapoint_config_failure(self):
        ''' authorize_get_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_config(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPC_RE)

    def test_authorize_get_datapoint_config_shared_uri_failure_not_containing_uri(self):
        ''' authorize_get_datapoint_data should fail if user shared a uri not containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_config_shared_uri_failure_not_containing_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri.other.things'
        datapointname='root.uri.some.things'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_config(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPC_RE)

    def test_authorize_get_datapoint_config_shared_uri_failure_different_user(self):
        ''' authorize_get_datapoint_data should fail if user shared a uri to a different user'''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_datapoint_config_shared_uri_failure_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri.other.things'
        datapointname='root.uri.other.things'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_datapoint_config(uid=uuid.uuid4(), pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDPC_RE)

    def test_authorize_put_datapoint_config_success(self):
        ''' authorize_put_datapoint_config should succeed if permission is granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_put_datapoint_config(uid=uid, pid=pid))

    def test_authorize_put_datapoint_config_failure(self):
        ''' authorize_put_datapoint_config should fail if permission is not granted'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_datapoint_config(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDPC_RE)

    def test_authorize_new_datasource_datapoint_success(self):
        ''' authorize_new_datasource_datapoint should succeed if permission is granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_new_datasource_datapoint(uid=uid, did=did))

    def test_authorize_new_datasource_datapoint_failure(self):
        ''' authorize_new_datasource_datapoint should fail if permission is not granted'''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_datasource_datapoint(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANDSDP_RE)

    def test_authorize_new_user_datapoint_failure_invalid_aid(self):
        ''' authorize_new_user_datapoint should fail if aid is invalid '''
        aids=[None, 'text',12, 222.22, {'a':'dict'}, {'set'}, ['a','list'],('tuple','yes'),{uuid.uuid4()},[uuid.uuid4(),],(uuid.uuid4(),),uuid.uuid1(), uuid.uuid4().hex]
        uid=uuid.uuid4()
        for aid in aids:
            with self.assertRaises(exceptions.AuthorizationException) as cm:
                authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_ARA_ANUDP_IA)

    def test_authorize_new_user_datapoint_failure_no_permission_found(self):
        ''' authorize_new_user_datapoint should fail if no permission is found '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_user_datapoint(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANUDP_RE)

    def test_authorize_new_user_datapoint_success(self):
        ''' authorize_new_user_datapoint should succeed if user has permission over agent '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        self.assertTrue(cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm))
        self.assertIsNone(authorization.authorize_new_user_datapoint(uid=uid, aid=aid))

    def test_authorize_put_agent_config_success(self):
        ''' authorize_put_agent_config should succeed if permission is granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        self.assertIsNone(authorization.authorize_put_agent_config(uid=uid, aid=aid))

    def test_authorize_put_agent_config_failure(self):
        ''' authorize_put_agent_config should fail if permission is not granted'''
        uid=self.user['uid']
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_agent_config(uid=uid, aid=aid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APAC_RE)

    def test_authorize_get_widget_config_success(self):
        ''' authorize_get_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_get_widget_config(uid=uid, wid=wid))

    def test_authorize_get_widget_config_success_widget_datasource_shared_uri(self):
        ''' authorize_get_widget_config should succeed if widget is ds and did is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_success_widget_datasource_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        self.assertIsNone(authorization.authorize_get_widget_config(uid=dest_uid,wid=widget['wid']))

    def test_authorize_get_widget_config_success_widget_datapoint_shared_uri(self):
        ''' authorize_get_datapoint_data should succeed if widget is dp and pid is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_success_widget_datapoint_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        self.assertIsNone(authorization.authorize_get_widget_config(uid=dest_uid,wid=widget['wid']))

    def test_authorize_get_widget_config_failure(self):
        ''' authorize_get_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_get_widget_config_failure_widget_datasource_shared_uri_non_containing(self):
        ''' authorize_get_widget_config should fail if widget is ds but did is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_failure_widget_datasource_shared_uri_non_containing'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='root.other.thing.uri'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_get_widget_config_failure_widget_datasource_shared_uri_different_user(self):
        ''' authorize_get_widget_config should fail if widget is ds but did is shared to other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_failure_widget_datasource_shared_uri_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=uuid.uuid4(), wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_get_widget_config_failure_widget_datapoint_shared_uri_non_containing_uri(self):
        ''' authorize_get_datapoint_data should fail if widget is dp but pid is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_failure_widget_datapoint_shared_uri_non_containing_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='some.diff.uri'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_get_widget_config_failure_widget_datapoint_shared_uri_other_user(self):
        ''' authorize_get_datapoint_data should fail if widget is dp but pid is shared to other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_get_widget_config_failure_widget_datapoint_shared_uri_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='root.uri'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_widget_config(uid=uuid.uuid4(), wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGWC_RE)

    def test_authorize_put_widget_config_success(self):
        ''' authorize_put_widget_config should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_put_widget_config(uid=uid, wid=wid))

    def test_authorize_put_widget_config_failure(self):
        ''' authorize_put_widget_config should fail if permission is not granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_widget_config(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APWC_RE)

    def test_authorize_get_dashboard_config_success(self):
        ''' authorize_get_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_get_dashboard_config(uid=uid, bid=bid))

    def test_authorize_get_dashboard_config_failure(self):
        ''' authorize_get_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_dashboard_config(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGDBC_RE)

    def test_authorize_put_dashboard_config_success(self):
        ''' authorize_put_dashboard_config should succeed if permission is granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_put_dashboard_config(uid=uid, bid=bid))

    def test_authorize_put_dashboard_config_failure(self):
        ''' authorize_put_dashboard_config should fail if permission is not granted'''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_put_dashboard_config(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_APDBC_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_bid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_wid(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no edit permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_no_wid_read_perm(self):
        ''' authorize_add_widget_to_dashboard should fail if user has no read permission over wid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=uid, bid=bid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_success(self):
        ''' authorize_add_widget_to_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_add_widget_to_dashboard(uid=uid,bid=bid,wid=wid))

    def test_authorize_add_widget_to_dashboard_success_widget_datasource_shared_uri(self):
        ''' authorize_add_widget_to_dashboard should succeed if widget is ds and did is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_success_widget_datasource_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        self.assertIsNone(authorization.authorize_add_widget_to_dashboard(uid=dest_uid,bid=dashboard['bid'],wid=widget['wid']))

    def test_authorize_add_widget_to_dashboard_success_widget_datapoint_shared_uri(self):
        ''' authorize_add_widget_to_dashboard should succeed if widget is dp and pid is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_success_widget_datapoint_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        self.assertIsNone(authorization.authorize_add_widget_to_dashboard(uid=dest_uid,bid=dashboard['bid'],wid=widget['wid']))

    def test_authorize_add_widget_to_dashboard_failure_widget_datasource_non_shared_uri(self):
        ''' authorize_add_widget_to_dashboard should succeed if widget is ds but did is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datasource_non_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='non.shared.ds'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_widget_datasource_shared_different_user(self):
        ''' authorize_add_widget_to_dashboard should succeed if widget is ds but did is shared to a different user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datasource_shared_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_widget_datasource_shared_no_perms(self):
        ''' authorize_add_widget_to_dashboard should succeed if widget is ds but did is shared without read permission '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datasource_shared_no_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_widget_datapoint_non_shared_uri(self):
        ''' authorize_add_widget_to_dashboard should fail if widget is dp but pid is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datapoint_non_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='non.shared.uri'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_widget_datapoint_shared_to_different_user(self):
        ''' authorize_add_widget_to_dashboard should fail if widget is dp but pid is shared to a different user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datapoint_shared_to_different_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datapointname='root.uri.datapoint'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_add_widget_to_dashboard_failure_widget_datapoint_shared_no_perms(self):
        ''' authorize_add_widget_to_dashboard should fail if widget is dp but pid is shared without perms '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_widget_to_dashboard_failure_widget_datapoint_shared_no_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='root.uri.datapoint'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        dashboard = dashboardapi.create_dashboard(uid=dest_uid, dashboardname='dashboard')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=dest_uid, bid=dashboard['bid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_widget_to_dashboard(uid=dest_uid, bid=dashboard['bid'], wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAWTDB_RE)

    def test_authorize_delete_widget_from_dashboard_failure_no_bid(self):
        ''' authorize_delete_widget_from_dashboard should fail if user has no permissions over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_widget_from_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADWFDB_RE)

    def test_authorize_delete_widget_from_dashboard_failure_no_bid_edit_perm(self):
        ''' authorize_delete_widget_to_dashboard should fail if user has no edit permission over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_widget_from_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADWFDB_RE)

    def test_authorize_delete_widget_from_dashboard_success(self):
        ''' authorize_delete_widget_from_dashboard should succeed '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_widget_from_dashboard(uid=uid,bid=bid))

    def test_authorize_delete_dashboard_failure_non_existent_bid(self):
        ''' authorize_delete_dashboard should fail if no bid exists '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDB_RE)

    def test_authorize_delete_dashboard_failure_no_delete_perm(self):
        ''' authorize_delete_dashboard should fail if user has no delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_dashboard(uid=uid, bid=bid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDB_RE)

    def test_authorize_delete_dashboard_success(self):
        ''' authorize_delete_dashboard should succeed if user has delete perm over bid '''
        uid=self.user['uid']
        bid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_dashboard(uid=uid, bid=bid))

    def test_authorize_add_datapoint_to_widget_failure_non_existent_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has not the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_non_existent_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_no_read_perm_over_pid(self):
        ''' authorize_add_datapoint_to_widget should fail if user has no edit perm over the wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_success(self):
        ''' authorize_add_datapoint_to_widget should succeed if user has permissions over pid and wid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_add_datapoint_to_widget(uid=uid, wid=wid, pid=pid))

    def test_authorize_add_datapoint_to_widget_success_shared_datapoint(self):
        ''' authorize_add_datapoint_to_widget should succeed if dp is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_success_shared_datapoint'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_multidp(uid=dest_uid, widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=dest_uid, wid=widget['wid'], perm=perm)
        self.assertIsNone(authorization.authorize_add_datapoint_to_widget(uid=dest_uid,wid=widget['wid'],pid=datapoint['pid']))

    def test_authorize_add_datapoint_to_widget_failure_shared_datapoint_not_exist(self):
        ''' authorize_add_datapoint_to_widget should fail if dp does not exit '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_failure_shared_datapoint_not_exist'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_multidp(uid=dest_uid, widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=dest_uid, wid=widget['wid'], perm=perm)
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=dest_uid, wid=widget['wid'], pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_shared_datapoint_same_user_but_not_authd(self):
        ''' authorize_add_datapoint_to_widget should fail if dp is from same user but is not auth yet '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_failure_shared_datapoint_same_user_but_not_authd'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_multidp(uid=sharing_user['uid'], widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=sharing_user['uid'], wid=widget['wid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=sharing_user['uid'], wid=widget['wid'], pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_shared_datapoint_not_shared(self):
        ''' authorize_add_datapoint_to_widget should fail if dp is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_failure_shared_datapoint_not_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='some.not.shared'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_multidp(uid=dest_uid, widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=dest_uid, wid=widget['wid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=dest_uid, wid=widget['wid'], pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_shared_datapoint_shared_without_perms(self):
        ''' authorize_add_datapoint_to_widget should fail if dp is not shared with perms '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_failure_shared_datapoint_shared_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='root.uri.shared.datapoint'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_multidp(uid=dest_uid, widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=dest_uid, wid=widget['wid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=dest_uid, wid=widget['wid'], pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_add_datapoint_to_widget_failure_shared_datapoint_shared_with_others(self):
        ''' authorize_add_datapoint_to_widget should fail if dp is not shared with perms '''
        dest_uid=self.user['uid']
        username = 'test_authorize_add_datapoint_to_widget_failure_shared_datapoint_shared_with_others'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datapointname='root.uri.shared.datapoint'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_multidp(uid=dest_uid, widgetname='widgetname')
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=dest_uid, wid=widget['wid'], perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_datapoint_to_widget(uid=dest_uid, wid=widget['wid'], pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AADPTW_RE)

    def test_authorize_delete_datapoint_from_widget_failure_non_existent_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFW_RE)

    def test_authorize_delete_datapoint_from_widget_failure_no_edit_perm_over_wid(self):
        ''' authorize_delete_datapoint_from_widget should fail if user has not edit perm over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFW_RE)

    def test_authorize_delete_datapoint_from_widget_success(self):
        ''' authorize_delete_datapoint_from_widget should succeed if user has permssion over the wid '''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_datapoint_from_widget(uid=uid, wid=wid))

    def test_authorize_new_snapshot_failure_non_existent_wid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        wid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_non_existent_uid(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=uid, wid=wid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_success(self):
        ''' authorize_new_snapshot should succeed if permission is granted'''
        uid=self.user['uid']
        wid=uuid.uuid4()
        perm=permissions.CAN_SNAPSHOT
        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
        self.assertIsNone(authorization.authorize_new_snapshot(uid=uid,wid=wid))

    def test_authorize_new_snapshot_success_widget_datasource_shared_uri(self):
        ''' authorize_new_snapshot should succeed if widget is ds and did is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_success_widget_datasource_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        self.assertIsNone(authorization.authorize_new_snapshot(uid=dest_uid,wid=widget['wid']))

    def test_authorize_new_snapshot_failure_widget_datasource_not_shared_uri(self):
        ''' authorize_new_snapshot should fail if widget is ds but did is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datasource_not_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='something.not.shared'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_widget_datasource_shared_uri_to_other_user(self):
        ''' authorize_new_snapshot should fail if widget is ds and did is shared to other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datasource_shared_uri_to_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_widget_datasource_shared_uri_without_snapshot_perm(self):
        ''' authorize_new_snapshot should fail if widget is ds and did is shared without snapshot permission '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datasource_shared_uri_without_snapshot_perm'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='root.uri.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        widget = widgetapi.new_widget_datasource(uid=sharing_user['uid'],did=datasource['did'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_success_widget_datapoint_shared_uri(self):
        ''' authorize_new_snapshot should succeed if widget is dp and pid is shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_success_widget_datapoint_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        self.assertIsNone(authorization.authorize_new_snapshot(uid=dest_uid,wid=widget['wid']))

    def test_authorize_new_snapshot_failure_widget_datapoint_not_shared_uri(self):
        ''' authorize_new_snapshot should fail if widget is dp but pid is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datapoint_not_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='something'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_widget_datapoint_shared_uri_to_other_user(self):
        ''' authorize_new_snapshot should fail if widget is dp and pid is shared with other user'''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datapoint_shared_uri_to_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_new_snapshot_failure_widget_datapoint_shared_uri_without_snapshot_perm(self):
        ''' authorize_new_snapshot should fail if widget is dp and pid is shared without snapshot perm'''
        dest_uid=self.user['uid']
        username = 'test_authorize_new_snapshot_failure_widget_datapoint_shared_uri_without_snapshot_perm'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        widget = widgetapi.new_widget_datapoint(uid=sharing_user['uid'],pid=datapoint['pid'])
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_new_snapshot(uid=dest_uid, wid=widget['wid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_ANS_RE)

    def test_authorize_get_snapshot_data_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_data(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSD_RE)

    def test_authorize_get_snapshot_data_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_data should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_data(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSD_RE)

    def test_authorize_get_snapshot_data_success(self):
        ''' authorize_get_snapshot_data should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_get_snapshot_data(uid=uid,nid=nid))

    def test_authorize_get_snapshot_config_failure_non_existent_nid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSC_RE)

    def test_authorize_get_snapshot_config_failure_non_existent_uid(self):
        ''' authorize_get_snapshot_config should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_snapshot_config(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGSC_RE)

    def test_authorize_get_snapshot_config_success(self):
        ''' authorize_get_snapshot_config should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_get_snapshot_config(uid=uid,nid=nid))

    def test_authorize_delete_snapshot_failure_non_existent_uid(self):
        ''' authorize_delete_snapshot should fail if uid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_snapshot(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADS_RE)

    def test_authorize_delete_snapshot_failure_non_existent_nid(self):
        ''' authorize_delete_snapshot should fail if nid does not exist '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        nid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_snapshot(uid=uid, nid=nid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADS_RE)

    def test_authorize_delete_snapshot_success(self):
        ''' authorize_delete_snapshot should succeed '''
        uid=self.user['uid']
        nid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_snapshot_perm(uid=uid, nid=nid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_snapshot(uid=uid,nid=nid))

    def test_authorize_get_circle_config_failure_non_existent_uid(self):
        ''' authorize_get_circle_config should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGCC_RE)

    def test_authorize_get_circle_config_success(self):
        ''' authorize_get_circle_config should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_get_circle_config(uid=uid,cid=cid))

    def test_authorize_delete_circle_failure_non_existent_uid(self):
        ''' authorize_delete_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADC_RE)

    def test_authorize_delete_circle_failure_non_existent_cid(self):
        ''' authorize_delete_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADC_RE)

    def test_authorize_delete_circle_success(self):
        ''' authorize_delete_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_DELETE
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_circle(uid=uid,cid=cid))

    def test_authorize_update_circle_config_failure_non_existent_uid(self):
        ''' authorize_update_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_update_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUCC_RE)

    def test_authorize_update_circle_config_failure_non_existent_cid(self):
        ''' authorize_update_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_update_circle_config(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUCC_RE)

    def test_authorize_update_circle_config_success(self):
        ''' authorize_update_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_update_circle_config(uid=uid,cid=cid))

    def test_authorize_add_member_to_circle_failure_non_existent_uid(self):
        ''' authorize_add_member_to_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_member_to_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAMTC_RE)

    def test_authorize_add_member_to_circle_failure_non_existent_cid(self):
        ''' authorize_add_member_to_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_add_member_to_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AAMTC_RE)

    def test_authorize_add_member_to_circle_success(self):
        ''' authorize_add_member_to_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_add_member_to_circle(uid=uid,cid=cid))

    def test_authorize_delete_member_from_circle_failure_non_existent_uid(self):
        ''' authorize_delete_member_from_circle should fail if uid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        uid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_member_from_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADMFC_RE)

    def test_authorize_delete_member_from_circle_failure_non_existent_cid(self):
        ''' authorize_delete_member_from_circle should fail if cid does not exist '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        cid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_member_from_circle(uid=uid, cid=cid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADMFC_RE)

    def test_authorize_delete_member_from_circle_success(self):
        ''' authorize_delete_member_from_circle should succeed '''
        uid=self.user['uid']
        cid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        self.assertIsNone(authorization.authorize_delete_member_from_circle(uid=uid,cid=cid))

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_existent_pid(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has not the pid '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_existent_uid(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_failure_non_enought_perms(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has not the necessary permissions '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADDPFDS_RE)

    def test_authorize_dissociate_datapoint_from_datasource_success(self):
        ''' authorize_dissociate_datapoint_from_datasource should fail if user has the necessary permissions over datapoint '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_dissociate_datapoint_from_datasource(uid=uid, pid=pid))

    def test_authorize_hook_to_datapoint_failure_non_existent_uid(self):
        ''' authorize_hook_to_datapoint should fail if uid-pid relation is not found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_hook_to_datapoint_failure_non_existent_pid(self):
        ''' authorize_hook_to_datapoint should fail if uid-pid relation is not found '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_hook_to_datapoint_failure_read_permission_not_found(self):
        ''' authorize_hook_to_datapoint should fail if user has not the necessary permissions '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_hook_to_datapoint_success(self):
        ''' authorize_hook_to_datapoint should succeed if user has the necessary permissions '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_hook_to_datapoint(uid=uid, pid=pid))

    def test_authorize_hook_to_datapoint_success_shared_uri(self):
        ''' authorize_hook_to_datapoint should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datapoint_success_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        self.assertIsNone(authorization.authorize_hook_to_datapoint(uid=dest_uid, pid=datapoint['pid']))

    def test_authorize_hook_to_datapoint_failure_non_shared_uri(self):
        ''' authorize_hook_to_datapoint should fail if dp is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datapoint_failure_non_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='not.shared.uri'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_hook_to_datapoint_failure_shared_uri_to_other_user(self):
        ''' authorize_hook_to_datapoint should fail if dp is shared to other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datapoint_failure_shared_uri_to_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_hook_to_datapoint_failure_shared_uri_without_perms(self):
        ''' authorize_hook_to_datapoint should fail if dp is shared without read perm '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datapoint_failure_shared_uri_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDP_RE)

    def test_authorize_unhook_from_datapoint_failure_non_existent_uid(self):
        ''' authorize_unhook_from_datapoint should fail if uid-pid relation is not found '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_unhook_from_datapoint_failure_non_existent_pid(self):
        ''' authorize_unhook_from_datapoint should fail if uid-pid relation is not found '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_unhook_from_datapoint_failure_read_permission_not_found(self):
        ''' authorize_unhook_from_datapoint should fail if user has not the necessary permissions'''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=uid, pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_unhook_from_datapoint_success(self):
        ''' authorize_unhook_from_datapoint should succeed if user has the necessary permissions '''
        uid=self.user['uid']
        pid=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        self.assertIsNone(authorization.authorize_unhook_from_datapoint(uid=uid, pid=pid))

    def test_authorize_unhook_from_datapoint_success_shared_uri(self):
        ''' authorize_unhook_from_datapoint should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datapoint_success_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        self.assertIsNone(authorization.authorize_unhook_from_datapoint(uid=dest_uid, pid=datapoint['pid']))

    def test_authorize_unhook_from_datapoint_failure_non_shared_uri(self):
        ''' authorize_unhook_from_datapoint should fail if dp is not shared '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datapoint_failure_non_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='not.shared.uri'
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_unhook_from_datapoint_failure_shared_uri_to_other_user(self):
        ''' authorize_unhook_from_datapoint should fail if dp is shared to other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datapoint_failure_shared_uri_to_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_unhook_from_datapoint_failure_shared_uri_without_perms(self):
        ''' authorize_unhook_from_datapoint should fail if dp is shared without read perm '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datapoint_failure_shared_uri_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='root.uri'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datapointname='.'.join((shared_uri,'some','levels','before','datapoint'))
        datapoint=datapointapi.create_user_datapoint(uid=sharing_user['uid'],datapoint_uri=datapointname)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datapoint(uid=dest_uid, pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDP_RE)

    def test_authorize_hook_to_datasource_failure_non_existent_uid(self):
        ''' authorize_hook_to_datasource should fail if uid-did relation is not found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_hook_to_datasource_failure_non_existent_did(self):
        ''' authorize_hook_to_datasource should fail if uid-did relation is not found '''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_hook_to_datasource_failure_read_permission_not_found(self):
        ''' authorize_hook_to_datasource should fail if user has not the necessary permissions '''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_hook_to_datasource_success(self):
        ''' authorize_hook_to_datasource should succeed if user has the necessary permissions '''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_hook_to_datasource(uid=uid, did=did))

    def test_authorize_hook_to_datasource_success_shared_uri(self):
        ''' authorize_hook_to_datasource should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datasource_success_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_hook_to_datasource(uid=dest_uid, did=datasource['did']))

    def test_authorize_hook_to_datasource_failure_not_shared_uri(self):
        ''' authorize_hook_to_datasource should fail if user did not share a uri '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datasource_failure_not_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='not.shared.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_hook_to_datasource_failure_shared_uri_with_other_user(self):
        ''' authorize_hook_to_datasource should fail if uri is shared with other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datasource_failure_shared_uri_with_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_hook_to_datasource_failure_shared_uri_without_perms(self):
        ''' authorize_hook_to_datasource should fail if uri is shared without read permission '''
        dest_uid=self.user['uid']
        username = 'test_authorize_hook_to_datasource_failure_shared_uri_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_hook_to_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AHTDS_RE)

    def test_authorize_unhook_from_datasource_failure_non_existent_uid(self):
        ''' authorize_unhook_from_datasource should fail if uid-did relation is not found '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_unhook_from_datasource_failure_non_existent_did(self):
        ''' authorize_unhook_from_datasource should fail if uid-did relation is not found '''
        uid=self.user['uid']
        did=uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_unhook_from_datasource_failure_read_permission_not_found(self):
        ''' authorize_unhook_from_datasource should fail if user has notthe necessary permissions'''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_EDIT
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=uid, did=did)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_unhook_from_datasource_success(self):
        ''' authorize_unhook_from_datasource should succeed if user hasthe necessary permissions '''
        uid=self.user['uid']
        did=uuid.uuid4()
        perm=permissions.CAN_READ
        cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
        self.assertIsNone(authorization.authorize_unhook_from_datasource(uid=uid, did=did))

    def test_authorize_unhook_from_datasource_success_shared_uri(self):
        ''' authorize_unhook_from_datasource should succeed if user shared a uri containing it '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datasource_success_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        self.assertIsNone(authorization.authorize_unhook_from_datasource(uid=dest_uid, did=datasource['did']))

    def test_authorize_unhook_from_datasource_failure_not_shared_uri(self):
        ''' authorize_unhook_from_datasource should fail if user did not share a uri '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datasource_failure_not_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        datasourcename='not.shared.datasource'
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_unhook_from_datasource_failure_shared_uri_with_other_user(self):
        ''' authorize_unhook_from_datasource should fail if uri is shared with other user '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datasource_failure_shared_uri_with_other_user'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uuid.uuid4(),uri=shared_uri, perm=perm))
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_unhook_from_datasource_failure_shared_uri_without_perms(self):
        ''' authorize_unhook_from_datasource should fail if uri is shared without read permission '''
        dest_uid=self.user['uid']
        username = 'test_authorize_unhook_from_datasource_failure_shared_uri_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_agent'
        version='Test Version'
        agent=agentapi.create_agent(uid=sharing_user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        shared_uri='root.uri'
        datasourcename='.'.join((shared_uri,'datasource'))
        datasource=datasourceapi.create_datasource(uid=sharing_user['uid'],aid=agent['aid'],datasourcename=datasourcename)
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=dest_uid,uri=shared_uri, perm=perm))
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_unhook_from_datasource(uid=dest_uid, did=datasource['did'])
        self.assertEqual(cm.exception.error, Errors.E_ARA_AUHFDS_RE)

    def test_authorize_get_uri_failure_invalid_uri(self):
        ''' authorize_get_uri should fail if uri is not a valid one '''
        uris=[
            1,
            1.1,
            uuid.uuid4(),
            uuid.uuid1(),
            dict(),
            list(),
            set(),
            tuple(),
            'uri with spaces',
            'non valid:global:uri',
        ]
        uid = uuid.uuid4()
        for uri in uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                authorization.authorize_get_uri(uid=uid, uri=uri)
            self.assertEqual(cm.exception.error, Errors.E_ARA_AGU_IURI)

    def test_authorize_get_uri_failure_non_existent_user_in_global_uri(self):
        ''' authorize_get_uri should fail if uri is global but user does not exist '''
        uri='test_authorize_get_uri_failure_non_existent_user_in_global_uri:uri'
        uid = uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_uri(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGU_RE)

    def test_authorize_get_uri_failure_non_shared_uri(self):
        ''' authorize_get_uri should fail if uri is not shared '''
        username='test_authorize_get_uri_failure_non_shared_uri'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        uri=username+':uri'
        uid = uuid.uuid4()
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_uri(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGU_RE)

    def test_authorize_get_uri_failure_non_shared_uri_non_containing_it(self):
        ''' authorize_get_uri should fail if uri is not shared '''
        uid = uuid.uuid4()
        username='test_authorize_get_uri_failure_non_shared_uri_non_containing_it'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uid,uri=shared_uri, perm=perm))
        uri=username+':not_shared.uri'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_uri(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGU_RE)

    def test_authorize_get_uri_failure_global_uri_shared_without_perms(self):
        ''' authorize_get_uri should fail if uri is shared without perms '''
        uid = uuid.uuid4()
        username='test_authorize_get_uri_failure_global_uri_shared_without_perms'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        perm=permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uid,uri=shared_uri, perm=perm))
        uri=username+':this.uri.is_shared.datasource'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_get_uri(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_AGU_RE)

    def test_authorize_get_uri_success_global_uri_shared(self):
        ''' authorize_get_uri should success if uri is shared '''
        uid = uuid.uuid4()
        username='test_authorize_get_uri_success_global_uri_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uid,uri=shared_uri, perm=perm))
        uri=username+':this.uri.is_shared.datasource'
        self.assertIsNone(authorization.authorize_get_uri(uid=uid, uri=uri))

    def test_authorize_get_uri_success_global_uri_is_mine(self):
        ''' authorize_get_uri should success if username of global uri is me '''
        username='test_authorize_get_uri_success_global_uri_is_mine'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        #we pass capital username to check is the same as in lowercase
        uri=username.upper()+':this.uri.is_mine'
        self.assertIsNone(authorization.authorize_get_uri(uid=sharing_user['uid'], uri=uri))

    def test_authorize_get_uri_success_local_uri(self):
        ''' authorize_get_uri should success if uri is local '''
        uid = uuid.uuid4()
        uri='local.uri'
        self.assertIsNone(authorization.authorize_get_uri(uid=uid, uri=uri))

    def test_authorize_get_uri_success_uri_is_None(self):
        ''' authorize_get_uri should success if uri is None'''
        uid = uuid.uuid4()
        uri=None
        self.assertIsNone(authorization.authorize_get_uri(uid=uid, uri=uri))

    def test_authorize_register_pending_hook_failure_invalid_uri(self):
        ''' authorize_register_pending_hook should fail if uri is not valid '''
        uid=uuid.uuid4()
        uri='invalid uri'
        with self.assertRaises(exceptions.BadParametersException) as cm:
            authorization.authorize_register_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ARPH_IURI)

    def test_authorize_register_pending_hook_failure_non_existent_owner_user(self):
        ''' authorize_register_pending_hook should fail if owner user does not exist '''
        uid=uuid.uuid4()
        uri='test_authorize_register_pending_hook_failure_non_existent_owner_user:uri'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_register_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ARPH_RE)

    def test_authorize_register_pending_hook_failure_uri_not_shared(self):
        ''' authorize_register_pending_hook should fail if owner user does not exist '''
        uid = uuid.uuid4()
        username='test_authorize_register_pending_hook_failure_uri_not_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        uri=username+':this.uri.is_not_shared.datasource'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_register_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ARPH_RE)

    def test_authorize_register_pending_hook_success_global_uri_shared(self):
        ''' authorize_register_pending_hook should success if uri is shared '''
        uid = uuid.uuid4()
        username='test_authorize_register_pending_hook_success_global_uri_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uid,uri=shared_uri, perm=perm))
        uri=username+':this.uri.is_shared.datasource'
        self.assertIsNone(authorization.authorize_register_pending_hook(uid=uid, uri=uri))

    def test_authorize_register_pending_hook_success_global_uri_is_mine(self):
        ''' authorize_register_pending_hook should success if global uri is mine '''
        username='test_authorize_register_pending_hook_success_global_uri_is_mine'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        uri=username+':this.uri.is_mine'
        self.assertIsNone(authorization.authorize_register_pending_hook(uid=sharing_user['uid'], uri=uri))

    def test_authorize_register_pending_hook_success_local_uri(self):
        ''' authorize_register_pending_hook should success if uri is local '''
        uid = uuid.uuid4()
        uri='this.uri.is.local'
        self.assertIsNone(authorization.authorize_register_pending_hook(uid=uid, uri=uri))

    def test_authorize_delete_pending_hook_failure_invalid_uri(self):
        ''' authorize_delete_pending_hook should fail if uri is not valid '''
        uid=uuid.uuid4()
        uri='invalid uri'
        with self.assertRaises(exceptions.BadParametersException) as cm:
            authorization.authorize_delete_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADPH_IURI)

    def test_authorize_delete_pending_hook_failure_non_existent_owner_user(self):
        ''' authorize_delete_pending_hook should fail if owner user does not exist '''
        uid=uuid.uuid4()
        uri='test_authorize_delete_pending_hook_failure_non_existent_owner_user:uri'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADPH_RE)

    def test_authorize_delete_pending_hook_failure_uri_not_shared(self):
        ''' authorize_delete_pending_hook should fail if owner user does not exist '''
        uid = uuid.uuid4()
        username='test_authorize_delete_pending_hook_failure_uri_not_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        uri=username+':this.uri.is_not_shared.datasource'
        with self.assertRaises(exceptions.AuthorizationException) as cm:
            authorization.authorize_delete_pending_hook(uid=uid, uri=uri)
        self.assertEqual(cm.exception.error, Errors.E_ARA_ADPH_RE)

    def test_authorize_delete_pending_hook_success_global_uri_shared(self):
        ''' authorize_delete_pending_hook should success if uri is shared '''
        uid = uuid.uuid4()
        username='test_authorize_delete_pending_hook_success_global_uri_shared'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        perm=permissions.CAN_READ|permissions.CAN_SNAPSHOT
        self.assertTrue(cassapiperm.insert_user_shared_uri_perm(uid=sharing_user['uid'],dest_uid=uid,uri=shared_uri, perm=perm))
        uri=username+':this.uri.is_shared.datasource'
        self.assertIsNone(authorization.authorize_delete_pending_hook(uid=uid, uri=uri))

    def test_authorize_delete_pending_hook_success_global_uri_is_mine(self):
        ''' authorize_delete_pending_hook should success if global uri is mine '''
        username='test_authorize_delete_pending_hook_success_global_uri_is_mine'
        password = 'password'
        email = username+'@komlog.org'
        sharing_user=userapi.create_user(username=username, password=password, email=email)
        shared_uri='this.uri.is_shared'
        uri=username+':this.uri.is_mine'
        self.assertIsNone(authorization.authorize_delete_pending_hook(uid=sharing_user['uid'], uri=uri))

    def test_authorize_delete_pending_hook_success_local_uri(self):
        ''' authorize_delete_pending_hook should success if uri is local '''
        uid = uuid.uuid4()
        uri='this.uri.is.local'
        self.assertIsNone(authorization.authorize_delete_pending_hook(uid=uid, uri=uri))

