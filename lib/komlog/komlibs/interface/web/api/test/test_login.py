import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlog.komfig import logging
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto 
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komcass.api import agent as cassapiagent
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, errors
from komlog.komlibs.interface.web.errors import Errors


class InterfaceWebApiLoginTest(unittest.TestCase):
    ''' komlibs.interface.web.api.login tests '''

    def test_login_request_failure_no_password_nor_pubkey_passed(self):
        ''' login_request should fail if password and pubkey are None '''
        username = 'username'
        response = loginapi.login_request(username)
        self.assertEqual(getattr(response,'cookie',None), None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
        self.assertEqual(response.error, Errors.E_IWAL_LR_IPRM.value)

    def test_user_login_request_failure_invalid_username(self):
        ''' user_login_request should fail if username is invalid '''
        usernames = ['username\n', 1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        password = 'password'
        for username in usernames:
            response = loginapi.login_request(username, password=password)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ULR_IU.value)

    def test_user_login_request_failure_invalid_password(self):
        ''' user_login_request should fail if password is invalid '''
        passwords= ['short', 1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'}]
        username = 'username'
        for password in passwords:
            response = loginapi.login_request(username, password=password)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ULR_IPWD.value)

    def test_user_login_request_failure_non_existent_username(self):
        ''' user_login_request should fail if username does not exist '''
        username = 'test_user_login_request_failure_non_existent_username'
        password = 'password'
        response = loginapi.login_request(username, password=password)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GUA_AUU_UNF.value)

    def test_user_login_request_failure_wrong_password(self):
        ''' user_login_request should fail if password is wrong '''
        username = 'test_user_login_request_failure_wrong_password'
        password = 'password'
        email = username + '@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        password = 'wrong_password'
        response = loginapi.login_request(username, password=password)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, Errors.E_IWAL_ULR_AUTHERR.value)

    def test_user_login_request_success(self):
        ''' user_login_request should succeed '''
        username = 'test_user_login_request_success'
        password = 'password'
        email = username + '@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        response = loginapi.login_request(username, password=password)
        cookie=response.cookie
        self.assertEqual(cookie['user'], username)
        self.assertEqual(cookie['aid'],None)
        self.assertEqual(cookie['pv'],None)
        self.assertTrue(args.is_valid_sequence(cookie['seq']))
        self.assertTrue(args.is_valid_hex_uuid(cookie['sid']))
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.data, {'redirect':'/home'})
        self.assertEqual(response.error, Errors.OK.value)

    def test_agent_login_generate_challenge_request_failure_invalid_username(self):
        ''' agent_login_generate_challenge_request should fail if username is invalid '''
        usernames = ['username\n', 1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        pubkey = 'pubkey'
        for username in usernames:
            response = loginapi.login_request(username, pubkey=pubkey)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALGCR_IU.value)

    def test_agent_login_generate_challenge_request_failure_invalid_pubkey(self):
        ''' agent_login_generate_challenge_request should fail if pubkey is invalid '''
        pubkeys = [1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'}, crypto.generate_rsa_key().public_key(), crypto.serialize_public_key(crypto.generate_rsa_key().public_key())]
        username = 'username'
        for pubkey in pubkeys:
            response = loginapi.login_request(username, pubkey=pubkey)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALGCR_IPK.value)

    def test_agent_login_generate_challenge_request_failure_invalid_pv(self):
        ''' agent_login_generate_challenge_request should fail if pv is invalid '''
        pvs = [0,-1,1, 1.1, None, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'}, crypto.generate_rsa_key().public_key(), crypto.serialize_public_key(crypto.generate_rsa_key().public_key())]
        username = 'username'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        for pv in pvs:
            response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALGCR_IPV.value)

    def test_agent_login_generate_challenge_request_failure_non_existent_username(self):
        ''' agent_login_generate_challenge_request should fail if username does not exist '''
        username = 'test_agent_login_generate_challenge_request_failure_non_existent_username'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        pv = '1'
        response = loginapi.login_request(username, pubkey=pubkey,pv=pv)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_GAC_UNF.value)

    def test_agent_login_generate_challenge_request_failure_non_existent_agent(self):
        ''' agent_login_generate_challenge_request should fail if agent does not exist '''
        username = 'test_agent_login_generate_challenge_request_failure_non_existent_agent'
        password = 'password'
        email = username + '@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        pv = '1'
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_GAC_ANF.value)

    def test_agent_login_generate_challenge_request_success(self):
        ''' agent_login_generate_challenge_request should succeed '''
        username = 'test_agent_login_generate_challenge_request_succeed'
        password = 'password'
        email = username + '@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname = 'test_agent_login_generate_challenge_request_succeed_agentname'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        pv = '1'
        agent = agentapi.create_agent(uid=user['uid'],agentname=agentname,pubkey=pubkey,version='v')
        pubkey = b64encode(pubkey).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey,pv=pv)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue('challenge' in response.data)
        self.assertTrue(isinstance(response.data['challenge'],str))
        self.assertEqual(response.error, Errors.OK.value)

    def test_agent_login_validate_challenge_request_failure_invalid_username(self):
        ''' agent_login_validate_challenge_request should fail if username is invalid '''
        usernames = ['username\n', 1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        pubkey = 'pubkey'
        challenge = 'challenge'
        signature = 'signature'
        for username in usernames:
            response = loginapi.login_request(username, pubkey=pubkey, challenge=challenge, signature=signature)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALVCR_IU.value)

    def test_agent_login_validate_challenge_request_failure_invalid_pubkey(self):
        ''' agent_login_validate_challenge_request should fail if username is invalid '''
        pubkeys = [1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'}, crypto.generate_rsa_key().public_key(), crypto.serialize_public_key(crypto.generate_rsa_key().public_key())]
        username = 'username'
        challenge = 'challenge'
        signature = 'signature'
        for pubkey in pubkeys:
            response = loginapi.login_request(username, pubkey=pubkey, challenge=challenge, signature=signature)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALVCR_IPK.value)

    def test_agent_login_validate_challenge_request_failure_invalid_pv(self):
        ''' agent_login_validate_challenge_request should fail if pv is invalid '''
        pvs = [None,-1,0,1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        username = 'username'
        signature = 'signature'
        challenge='challenge'
        for pv in pvs:
            response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALVCR_IPV.value)

    def test_agent_login_validate_challenge_request_failure_invalid_challenge(self):
        ''' agent_login_validate_challenge_request should fail if challenge is invalid '''
        challenges = [1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        pubkey = 'pubkey'
        username = 'username'
        signature = 'signature'
        pv = '1'
        for challenge in challenges:
            response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALVCR_ICH.value)

    def test_agent_login_validate_challenge_request_failure_invalid_signature(self):
        ''' agent_login_validate_challenge_request should fail if signature is invalid '''
        signatures = [1, 1.1, uuid.uuid4(), timeuuid.uuid1(), ('a','tuple'),['a','list'], {'set'}, {'a':'dict'},None]
        pubkey = 'pubkey'
        pv = '1'
        username = 'username'
        challenge = 'signature'
        for signature in signatures:
            response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
            self.assertEqual(getattr(response,'cookie', None),None)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWAL_ALVCR_ISG.value)

    def test_agent_login_validate_challenge_request_failure_non_existent_username(self):
        ''' agent_login_validate_challenge_request should fail if username does not exist '''
        username = 'test_agent_login_validate_challenge_request_failure_non_existent_username'
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        pv = '1'
        challenge=b64encode(b'challenge').decode('utf-8')
        signature=b64encode(b'signature').decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_UNF.value)

    def test_agent_login_validate_challenge_request_failure_non_existent_agent(self):
        ''' agent_login_validate_challenge_request should fail if agent does not exist '''
        username = 'test_agent_login_validate_challenge_request_failure_non_existent_agent'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        pv = '1'
        challenge=b64encode(b'challenge').decode('utf-8')
        signature=b64encode(b'signature').decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_ANF.value)

    def test_agent_login_validate_challenge_request_failure_non_existent_challenge(self):
        ''' agent_login_validate_challenge_request should fail if challenge does not exist '''
        username = 'test_agent_login_validate_challenge_request_failure_non_existent_challenge'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='version'
        pubkey = crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        pv = '1'
        agent = agentapi.create_agent(user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        pubkey = b64encode(pubkey).decode('utf-8')
        challenge=b64encode(b'challenge').decode('utf-8')
        signature=b64encode(b'signature').decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=challenge, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_CHNF.value)

    def test_agent_login_validate_challenge_request_failure_wrong_signature(self):
        ''' agent_login_validate_challenge_request should fail if signature is wrong '''
        username = 'test_agent_login_validate_challenge_request_failure_wrong_signature'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='version'
        key = crypto.generate_rsa_key()
        pubkey = crypto.serialize_public_key(key.public_key())
        pv = '1'
        agent = agentapi.create_agent(user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        pubkey = b64encode(pubkey).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        serialized_priv_key=crypto.serialize_private_key(key)
        ch_plain = crypto.decrypt(serialized_priv_key, b64decode(response.data['challenge'].encode('utf-8')))
        ch_hash = crypto.get_hash(ch_plain)
        ch_resp = b64encode(ch_hash).decode('utf-8')
        signature=b64encode(b'signature').decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=ch_resp, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_EVS.value)

    def test_agent_login_validate_challenge_request_success(self):
        ''' agent_login_validate_challenge_request should succeed '''
        username = 'test_agent_login_validate_challenge_request_success'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='version'
        key = crypto.generate_rsa_key()
        pubkey = crypto.serialize_public_key(key.public_key())
        pv = '1'
        agent = agentapi.create_agent(user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        pubkey = b64encode(pubkey).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        serialized_priv_key=crypto.serialize_private_key(key)
        ch_plain = crypto.decrypt(serialized_priv_key, b64decode(response.data['challenge'].encode('utf-8')))
        ch_hash = crypto.get_hash(ch_plain)
        ch_resp = b64encode(ch_hash).decode('utf-8')
        signature=b64encode(crypto.sign_message(serialized_priv_key, ch_hash)).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=ch_resp, signature=signature)
        cookie=response.cookie
        self.assertEqual(cookie['user'], username)
        self.assertEqual(cookie['aid'],agent['aid'].hex)
        self.assertEqual(cookie['pv'],int(pv))
        self.assertTrue(args.is_valid_sequence(cookie['seq']))
        self.assertTrue(args.is_valid_hex_uuid(cookie['sid']))
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.error, Errors.OK.value)

    def test_agent_login_validate_challenge_request_failure_already_validated_challenge(self):
        ''' agent_login_validate_challenge_request should fail if challenge has been validated before'''
        username = 'test_agent_login_validate_challenge_request_failure_already_validated_challenge'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='version'
        key = crypto.generate_rsa_key()
        pubkey = crypto.serialize_public_key(key.public_key())
        pv = '1'
        agent = agentapi.create_agent(user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        pubkey = b64encode(pubkey).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        serialized_priv_key=crypto.serialize_private_key(key)
        ch_plain = crypto.decrypt(serialized_priv_key, b64decode(response.data['challenge'].encode('utf-8')))
        ch_hash = crypto.get_hash(ch_plain)
        ch_resp = b64encode(ch_hash).decode('utf-8')
        signature=b64encode(crypto.sign_message(serialized_priv_key, ch_hash)).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=ch_resp, signature=signature)
        cookie=response.cookie
        self.assertEqual(cookie['user'], username)
        self.assertEqual(cookie['aid'],agent['aid'].hex)
        self.assertEqual(cookie['pv'],int(pv))
        self.assertTrue(args.is_valid_sequence(cookie['seq']))
        self.assertTrue(args.is_valid_hex_uuid(cookie['sid']))
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(response.error, Errors.OK.value)
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=ch_resp, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_CHAU.value)

    def test_agent_login_validate_challenge_request_failure_challenge_expired(self):
        ''' agent_login_validate_challenge_request should fail if challenge has expired '''
        username = 'test_agent_login_validate_challenge_request_failure_challenge_expired'
        password = 'password'
        email = username+'@komlog.org'
        user = userapi.create_user(username=username, password=password, email=email)
        agentname=username+'_agent'
        version='version'
        key = crypto.generate_rsa_key()
        pubkey = crypto.serialize_public_key(key.public_key())
        pv = '1'
        agent = agentapi.create_agent(user['uid'],agentname=agentname,pubkey=pubkey,version=version)
        pubkey = b64encode(pubkey).decode('utf-8')
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        serialized_priv_key=crypto.serialize_private_key(key)
        ch_plain = crypto.decrypt(serialized_priv_key, b64decode(response.data['challenge'].encode('utf-8')))
        ch_hash = crypto.get_hash(ch_plain)
        ch_resp = b64encode(ch_hash).decode('utf-8')
        signature=b64encode(crypto.sign_message(serialized_priv_key, ch_hash)).decode('utf-8')
        agent_challenge=cassapiagent.get_agent_challenge(aid=agent['aid'], challenge=ch_hash)
        self.assertIsNotNone(agent_challenge)
        agent_challenge.generated = timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(agent_challenge.generated)-61)
        self.assertTrue(cassapiagent.insert_agent_challenge(agent_challenge))
        response = loginapi.login_request(username, pubkey=pubkey, pv=pv, challenge=ch_resp, signature=signature)
        self.assertEqual(getattr(response,'cookie', None),None)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, gesterrors.E_GAA_VAC_CHEX.value)

