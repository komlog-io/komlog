import unittest
import uuid
from komlog.komfig import logging
from komlog.komlibs.auth.passport import Passport
from komlog.komlibs.interface.websocket import session


class InterfaceWebSocketSessionTest(unittest.TestCase):
    ''' komlibs.interface.websocket.session tests '''

    def test_set_session_failure_invalid_passport(self):
        ''' set session should fail if passport is invalid '''
        passports=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        callback = lambda : None
        for psp in passports:
            self.assertFalse(session.set_session(passport=psp, callback=callback))

    def test_set_session_success(self):
        ''' set_session should succeed and associate the sid with the current process imc_address '''
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        sid=uuid.uuid4()
        psp = Passport(uid=uid,sid=sid,aid=aid)
        def callback(message):
            return message
        self.assertTrue(session.set_session(psp,callback))
        message='a test message to return'
        self.assertEqual(session.agent_callback[sid](message),message)

    def test_unset_session_failure_invalid_passport(self):
        ''' unset session should fail if passport is invalid '''
        passports=['\tadas',None,-2,1.1,{'set','a'},('a','tuple'),['array',0,1],{'dict':1}, uuid.uuid4()]
        for psp in passports:
            self.assertFalse(session.unset_session(passport=psp))

    def test_unset_session_success(self):
        ''' unset_session should succeed and disassociate the sid with the current process imc_address '''
        uid = uuid.uuid4()
        aid = uuid.uuid4()
        sid=uuid.uuid4()
        psp = Passport(uid=uid,sid=sid,aid=aid)
        self.assertTrue(session.unset_session(psp))

