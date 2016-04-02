import unittest
import uuid
from komlog.komfig import logger
from komlog.komlibs.gestaccount.agent import api
from komlog.komlibs.gestaccount.agent.states import *
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount import exceptions, errors
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.model.orm import agent as ormagent
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.general.time import timeuuid

class GestaccountAgentApiTest(unittest.TestCase):
    ''' komlog.gestaccount.agent.api tests '''
    
    def setUp(self):
        self.username='test_gestaccount.agent.api_user'
        self.password='password'
        self.email='test_gestaccount.agent.api_user@komlog.org'
        try:
            uid=userapi.get_uid(username=self.username)
        except Exception:
            user=userapi.create_user(username=self.username, password=self.password, email=self.email)
            uid=user['uid']
        finally:
            self.user=userapi.get_user_config(uid=uid)

    def test_create_agent_non_existent_user(self):
        ''' create_agent should fail if user is not found in system '''
        uid=uuid.uuid4()
        agentname='My Agent #9'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Version X'
        self.assertRaises(exceptions.UserNotFoundException, api.create_agent,uid=uid, agentname=agentname, pubkey=pubkey, version=version) 

    def test_create_agent_success(self):
        ''' create_agent should succeed if arguments are OK, agent does not exists yet and user exists '''
        agentname='test_create_agent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        self.assertTrue(isinstance(agent['aid'], uuid.UUID))
        self.assertEqual(agent['agentname'], agentname)
        self.assertEqual(agent['pubkey'], pubkey)
        self.assertEqual(agent['version'], version)
        self.assertEqual(agent['state'], AgentStates.ACTIVE)

    def test_create_agent_already_existing_agent(self):
        ''' create_agent should fail if agent already exists '''
        agentname='test_create_agent_already_existing_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertRaises(exceptions.AgentAlreadyExistsException, api.create_agent, uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)

    def test_activate_agent_non_existent_agent(self):
        ''' activate_agent should fail if agent is not found in system '''
        aid=uuid.uuid4()
        self.assertRaises(exceptions.AgentNotFoundException, api.activate_agent,aid=aid) 

    def test_activate_agent_success(self):
        ''' activate_agent should succeed if agent exists '''
        agentname='test_activate_agent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertTrue(api.suspend_agent(aid=agent['aid']))
        data=api.get_agent_config(aid=agent['aid'])
        self.assertEqual(data['state'], AgentStates.SUSPENDED)
        self.assertTrue(api.activate_agent(aid=agent['aid']))
        data=api.get_agent_config(aid=agent['aid'])
        self.assertEqual(data['state'], AgentStates.ACTIVE)

    def test_suspend_agent_non_existent_agent(self):
        ''' suspend_agent should fail if agent is not found in system '''
        aid=uuid.uuid4()
        with self.assertRaises(exceptions.AgentNotFoundException) as cm:
            api.suspend_agent(aid=aid)
        self.assertEqual(cm.exception.error, errors.E_GAA_SPA_ANF)

    def test_suspend_agent_success(self):
        ''' suspend_agent should succeed if agent exists '''
        agentname='test_suspend_agent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        data=api.get_agent_config(aid=agent['aid'])
        self.assertEqual(data['state'], AgentStates.ACTIVE)
        self.assertTrue(api.suspend_agent(aid=agent['aid']))
        data=api.get_agent_config(aid=agent['aid'])
        self.assertEqual(data['state'], AgentStates.SUSPENDED)

    def test_get_agent_config_non_existent_agent(self):
        ''' get_agent_config should fail if agent is not found in system '''
        aid=uuid.uuid4()
        self.assertRaises(exceptions.AgentNotFoundException, api.get_agent_config,aid=aid) 

    def test_get_agent_config_success(self):
        ''' get_agent_config should succeed if agent exists in system '''
        agentname='test_get_agent_config_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        data=api.get_agent_config(aid=agent['aid'])
        self.assertIsInstance(data,dict) 
        self.assertEqual(data['aid'],agent['aid']) 
        self.assertEqual(data['agentname'],agentname) 
        self.assertEqual(data['state'], AgentStates.ACTIVE) 
        self.assertEqual(data['version'],version) 

    def test_get_agents_config_non_existent_user(self):
        ''' get_agents_config should fail if username is not found in system '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.get_agents_config,uid=uid)

    def test_get_agents_config_success(self):
        ''' get_agents_config should succeed if username exists in system '''
        uid=self.user['uid']
        data=api.get_agents_config(uid=uid)
        self.assertIsInstance(data,list) 

    def test_update_agent_config_data_with_invalid_agentname(self):
        ''' update_agent_config should fail if data has invalid agentname'''
        aid=uuid.uuid4()
        agentnames=[None, 3423423243, {'a':'dict'},['a','list'],uuid.uuid4(),2342342.23423423,0,1,'agent_with_ñññ']
        for agentname in agentnames:
            self.assertRaises(exceptions.BadParametersException, api.update_agent_config, aid=aid, agentname=agentname)

    def test_update_agent_config_non_existent_agent(self):
        ''' update_agent_config should fail if agent is not in system '''
        aid=uuid.uuid4()
        agentname='Agent Name #19'
        self.assertRaises(exceptions.AgentNotFoundException, api.update_agent_config, aid=aid, agentname=agentname)

    def test_update_agent_config_success(self):
        ''' update_agent_config should succeed if agent exists in system '''
        agentname='test_update_agent_config_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        agentname='test_update_agent_config_success_after_update'
        self.assertTrue(api.update_agent_config( aid=agent['aid'], agentname=agentname)) 

    def test_generate_auth_challenge_failure_invalid_username(self):
        ''' generate_auth_challenge should fail if username is invalid '''
        usernames=[None, 3423423243, 2.2, {'a':'dict'},['a','list'],('a','tuple'),{'set'},'with_ñññ', uuid.uuid1()]
        pubkey='whatakey'
        for username in usernames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_auth_challenge(username=username, pubkey=pubkey)
            self.assertEqual(cm.exception.error, errors.E_GAA_GAC_IU)

    def test_generate_auth_challenge_failure_invalid_pubkey(self):
        ''' generate_auth_challenge should fail if pubkey is invalid '''
        pubkeys=[None, 3423423243, 2.2, {'a':'dict'},['a','list'],uuid.uuid4(),('a','tuple'),{'set'},'with_ñññ', crypto.generate_rsa_key(), crypto.serialize_private_key(crypto.generate_rsa_key()).hex(), crypto.serialize_public_key(crypto.generate_rsa_key().public_key()).decode('utf-8')]
        username='test_generate_auth_challenge_failure_invalid_pubkey'
        for pubkey in pubkeys:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_auth_challenge(username=username, pubkey=pubkey)
            self.assertEqual(cm.exception.error, errors.E_GAA_GAC_IPK)

    def test_generate_auth_challenge_failure_non_existent_user(self):
        ''' generate_auth_challenge should fail if user does not exist '''
        username='test_generate_auth_challenge_failure_non_existent_user'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        with self.assertRaises(exceptions.ChallengeGenerationException) as cm:
            api.generate_auth_challenge(username=username, pubkey=pubkey)
        self.assertEqual(cm.exception.error, errors.E_GAA_GAC_UNF)

    def test_generate_auth_challenge_failure_non_existent_pubkey(self):
        ''' generate_auth_challenge should fail if pubkey does not exist '''
        username='test_generate_auth_challenge_failure_non_existent_pubkey'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        with self.assertRaises(exceptions.ChallengeGenerationException) as cm:
            api.generate_auth_challenge(username=username, pubkey=pubkey)
        self.assertEqual(cm.exception.error, errors.E_GAA_GAC_ANF)

    def test_generate_auth_challenge_success(self):
        ''' generate_auth_challenge should succeed '''
        username='test_generate_auth_challenge_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_generate_auth_challenge_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        challenge=api.generate_auth_challenge(username=username, pubkey=pubkey)
        self.assertIsNotNone(challenge)

    def test_validate_auth_challenge_failure_invalid_username(self):
        ''' validate_auth_challenge should fail if username is invalid '''
        usernames=[None, 3423423243, 2.2, {'a':'dict'},['a','list'],('a','tuple'),{'set'},'with_ñññ', uuid.uuid1()]
        pubkey='whatakey'
        challenge_hash='adsfasdf'
        signature='asdfasdfasdf'
        for username in usernames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
            self.assertEqual(cm.exception.error, errors.E_GAA_VAC_IU)

    def test_validate_auth_challenge_failure_invalid_pubkey(self):
        ''' validate_auth_challenge should fail if pubkey is invalid '''
        username='test_validate_auth_challenge_failure_invalid_pubkey'
        pubkeys=[None, 3423423243, 2.2, {'a':'dict'},['a','list'],uuid.uuid4(),('a','tuple'),{'set'},'with_ñññ', crypto.generate_rsa_key(), crypto.serialize_private_key(crypto.generate_rsa_key()), crypto.generate_rsa_key().public_key()]
        challenge_hash='adsfasdf'
        signature='asdfasdfasdf'
        for pubkey in pubkeys:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
            self.assertEqual(cm.exception.error, errors.E_GAA_VAC_IPK)

    def test_validate_auth_challenge_failure_invalid_challenge_hash(self):
        ''' validate_auth_challenge should fail if challenge_hash is invalid '''
        username='test_validate_auth_challenge_failure_invalid_challenge_hash'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        challenges=[None, 3423423243, 2.2, 'string',{'a':'dict'},['a','list'],uuid.uuid4(),('a','tuple'),{'set'}, crypto.generate_rsa_key(), crypto.serialize_private_key(crypto.generate_rsa_key()).hex(), crypto.generate_rsa_key().public_key()]
        signature=b'asdfasdfasdf'
        for ch in challenges:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=ch, signature=signature)
            self.assertEqual(cm.exception.error, errors.E_GAA_VAC_ICH)

    def test_validate_auth_challenge_failure_invalid_signature(self):
        ''' validate_auth_challenge should fail if signature is invalid '''
        username='test_validate_auth_challenge_failure_invalid_signature'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        signatures=[None, 3423423243, 2.2, 'string', {'a':'dict'},['a','list'],uuid.uuid4(),('a','tuple'),{'set'}, crypto.generate_rsa_key(), crypto.serialize_private_key(crypto.generate_rsa_key()).hex(), crypto.generate_rsa_key().public_key()]
        ch=b'asdfasdfasdf'
        for signature in signatures:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=ch, signature=signature)
            self.assertEqual(cm.exception.error, errors.E_GAA_VAC_ISG)

    def test_validate_auth_challenge_failure_non_existent_user(self):
        ''' validate_auth_challenge should fail if user does not exist '''
        username='test_validate_auth_challenge_failure_non_existent_user'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        challenge_hash=b'adsfasdf'
        signature=b'asdfasdfasdf'
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_UNF)

    def test_validate_auth_challenge_failure_non_existent_pubkey(self):
        ''' validate_auth_challenge should fail if pubkey does not exist '''
        username='test_validate_auth_challenge_failure_non_existent_pubkey'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        challenge_hash=b'adsfasdf'
        signature=b'asdfasdfasdf'
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_ANF)

    def test_validate_auth_challenge_failure_non_existent_challenge(self):
        ''' validate_auth_challenge should fail if challenge does not exist '''
        username='test_validate_auth_challenge_failure_non_existent_challenge'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_validate_auth_challenge_failure_non_existent_challenge'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        challenge_hash=b'adsfasdf'
        signature=b'asdfasdfasdf'
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_CHNF)

    def test_validate_auth_challenge_failure_error_verifying_signature(self):
        ''' validate_auth_challenge should fail if signature does not correspond to message '''
        username='test_validate_auth_challenge_failure_error_verifying_signature'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_generate_auth_challenge_success_agent'
        key=crypto.generate_rsa_key()
        pubkey=crypto.serialize_public_key(key.public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        enc_challenge=api.generate_auth_challenge(username=username, pubkey=pubkey)
        challenge=crypto.decrypt(key=crypto.serialize_private_key(key), ciphertext=enc_challenge)
        self.assertIsNotNone(challenge)
        challenge_hash=crypto.get_hash(challenge)
        key2=crypto.generate_rsa_key()
        signature=crypto.sign_message(key=crypto.serialize_private_key(key2), message=challenge_hash)
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_EVS)

    def test_validate_auth_challenge_success(self):
        ''' validate_auth_challenge should succeed '''
        username='test_validate_auth_challenge_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_generate_auth_challenge_success_agent'
        key=crypto.generate_rsa_key()
        pubkey=crypto.serialize_public_key(key.public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        enc_challenge=api.generate_auth_challenge(username=username, pubkey=pubkey)
        challenge=crypto.decrypt(key=crypto.serialize_private_key(key), ciphertext=enc_challenge)
        self.assertIsNotNone(challenge)
        challenge_hash=crypto.get_hash(challenge)
        signature=crypto.sign_message(key=crypto.serialize_private_key(key), message=challenge_hash)
        aid=api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(aid, agent['aid'])

    def test_validate_auth_challenge_failure_already_validated_challenge(self):
        ''' validate_auth_challenge should fail if it has been validated before '''
        username='test_validate_auth_challenge_failure_already_validated_challenge'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_generate_auth_challenge_success_agent'
        key=crypto.generate_rsa_key()
        pubkey=crypto.serialize_public_key(key.public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        enc_challenge=api.generate_auth_challenge(username=username, pubkey=pubkey)
        challenge=crypto.decrypt(key=crypto.serialize_private_key(key), ciphertext=enc_challenge)
        self.assertIsNotNone(challenge)
        challenge_hash=crypto.get_hash(challenge)
        signature=crypto.sign_message(key=crypto.serialize_private_key(key), message=challenge_hash)
        aid=api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(aid, agent['aid'])
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_CHAU)

    def test_validate_auth_challenge_failure_expired_challenge(self):
        ''' validate_auth_challenge should fail if challenge has expired '''
        username='test_validate_auth_challenge_failure_challenge_expired'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        self.assertIsNotNone(user)
        agentname='test_generate_auth_challenge_success_agent'
        key=crypto.generate_rsa_key()
        pubkey=crypto.serialize_public_key(key.public_key())
        version='Test Version'
        agent=api.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        self.assertIsNotNone(agent)
        enc_challenge=api.generate_auth_challenge(username=username, pubkey=pubkey)
        challenge=crypto.decrypt(key=crypto.serialize_private_key(key), ciphertext=enc_challenge)
        self.assertIsNotNone(challenge)
        challenge_hash=crypto.get_hash(challenge)
        agent_challenge=cassapiagent.get_agent_challenge(aid=agent['aid'],challenge=challenge_hash)
        self.assertIsNotNone(agent_challenge)
        agent_challenge.generated=timeuuid.uuid1(seconds=1)
        self.assertTrue(cassapiagent.insert_agent_challenge(agent_challenge))
        signature=crypto.sign_message(key=crypto.serialize_private_key(key), message=challenge_hash)
        with self.assertRaises(exceptions.ChallengeValidationException) as cm:
            api.validate_auth_challenge(username=username, pubkey=pubkey, challenge_hash=challenge_hash, signature=signature)
        self.assertEqual(cm.exception.error, errors.E_GAA_VAC_CHEX)

