import unittest
import uuid
import inspect
from komlibs.auth import authorization
from komlibs.auth.requests import Requests
from komlibs.auth.passport import Passport
from komlibs.auth import exceptions, permissions, errors
from komlibs.gestaccount.user import api as gestuserapi
from komlibs.general.time import timeuuid
from komfig import logger

class AuthAuthorizationTest(unittest.TestCase):
    ''' komlog.auth.authorization tests '''

    def test_authorize_request_failure_request_parameter_not_passed(self):
        ''' authorize_request should fail if request parameter is not passed '''
        passport = Passport(uid=uuid.uuid4())
        with self.assertRaises(exceptions.BadParametersException) as cm:
            authorization.authorize_request(passport=passport)
        self.assertEqual(cm.exception.error, errors.E_AA_AR_BP)

    def test_authorize_request_non_existent_request_in_kwargs(self):
        ''' authorize_request should fail if request does not exist '''
        passport = Passport(uid=uuid.uuid4())
        requests=[uuid.uuid4(),234234234,'TEST_AUTHORIZE_REQUEST_NON_EXISTENT_REQUEST']
        for request in requests:
            with self.assertRaises(exceptions.RequestNotFoundException) as cm:
                authorization.authorize_request(request=request,passport=passport)
            self.assertEqual(cm.exception.error, errors.E_AA_AR_RNF)

    def test_authorize_request_non_existent_request_in_args(self):
        ''' authorize_request should fail if request does not exist '''
        passport = Passport(uid=uuid.uuid4())
        requests=[uuid.uuid4(),234234234,'TEST_AUTHORIZE_REQUEST_NON_EXISTENT_REQUEST']
        for request in requests:
            with self.assertRaises(exceptions.RequestNotFoundException) as cm:
                authorization.authorize_request(request,passport)
            self.assertEqual(cm.exception.error, errors.E_AA_AR_RNF)

    def test_authorize_request_failure_missing_some_parameter_from_authorization_func(self):
        ''' authorize_request should fail some parameter is missing when calling the authorization function '''
        request=Requests.NEW_AGENT
        with self.assertRaises(exceptions.BadParametersException) as cm:
            authorization.authorize_request(request=request)
        self.assertEqual(cm.exception.error, errors.E_AA_AR_FBP)

    def test_requests_function_relations(self):
        ''' in this test we check that every defined request has is associated function '''
        for req in Requests:
            try:
                f = authorization.func_requests[req]
            except KeyError:
                logger.logger.debug('Request associated function not found :'+str(req))
                f = None
            finally:
                self.assertIsNotNone(f)

    def test_passport_parameter_in_authorization_funcs(self):
        ''' check that every authorization func requires a passport parameter '''
        for req, func in authorization.func_requests.items():
            try:
                pos=inspect.getargspec(func).args.index('passport')
            except Exception:
                logger.logger.debug('passport argument not found in '+str(func.__name__))
                pos=-1
            finally:
                self.assertEqual(pos,0)

