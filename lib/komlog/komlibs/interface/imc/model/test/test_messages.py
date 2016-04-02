import unittest
import uuid
import json
from komlog.komlibs.interface.imc.api import gestconsole
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.general.time import timeuuid


class InterfaceImcModelMessagesTest(unittest.TestCase):
    ''' komlibs.interface.imc.model.messages tests '''

    def test_MonitorVariableMessage_failure_invalid_username(self):
        ''' creation of a MonitorVariableMessage object should fail if username is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure_invalid_username_datapointname'
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage, uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_MonitorVariableMessage_failure_invalid_datapointname(self):
        ''' creation of a MonitorVariableMessage object should fail if datapointname is invalid '''
        uid=uuid.uuid4()
        datapointnames=[None, 23423, 2323.2342, {'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        for datapointname in datapointnames:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage, uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_MonitorVariableMessage_failure_invalid_did(self):
        ''' creation of a MonitorVariableMessage object should fail if did is invalid '''
        uid=uuid.uuid4()
        dids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for did in dids:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage,uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_MonitorVariableMessage_failure_invalid_date(self):
        ''' creation of a MonitorVariableMessage object should fail if date is invalid '''
        uid=uuid.uuid4()
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for date in dates:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage,uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_MonitorVariableMessage_failure_invalid_position(self):
        ''' creation of a MonitorVariableMessage object should fail if position is invalid '''
        uid=uuid.uuid4()
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for position in positions:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage,uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_MonitorVariableMessage_failure_invalid_length(self):
        ''' creation of a MonitorVariableMessage object should fail if length is invalid '''
        uid=uuid.uuid4()
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        datapointname='test_MonitorVariableMessage_failure'
        for length in lengths:
            self.assertRaises(exceptions.BadParametersException, messages.MonitorVariableMessage,uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)

    def test_NegativeVariableMessage_failure_invalid_pid(self):
        ''' creation of a NegativeVariableMessage object should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        for pid in pids:
            self.assertRaises(exceptions.BadParametersException, messages.NegativeVariableMessage, date=date, position=position, length=length)

    def test_NegativeVariableMessage_failure_invalid_date(self):
        ''' creation of a NegativeVariableMessage object should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            self.assertRaises(exceptions.BadParametersException, messages.NegativeVariableMessage, date=date, position=position, length=length)

    def test_NegativeVariableMessage_failure_invalid_position(self):
        ''' creation of a NegativeVariableMessage object should fail if position is invalid '''
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        for position in positions:
            self.assertRaises(exceptions.BadParametersException, messages.NegativeVariableMessage, date=date, position=position, length=length)

    def test_NegativeVariableMessage_failure_invalid_length(self):
        ''' creation of a NegativeVariableMessage object should fail if length is invalid '''
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        for length in lengths:
            self.assertRaises(exceptions.BadParametersException, messages.NegativeVariableMessage, date=date, position=position, length=length)

    def test_PositiveVariableMessage_failure_invalid_pid(self):
        ''' creation of a PositiveVariableMessage object should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        for pid in pids:
            self.assertRaises(exceptions.BadParametersException, messages.PositiveVariableMessage, date=date, position=position, length=length)

    def test_PositiveVariableMessage_failure_invalid_date(self):
        ''' creation of a PositiveVariableMessage object should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            self.assertRaises(exceptions.BadParametersException, messages.PositiveVariableMessage, date=date, position=position, length=length)

    def test_PositiveVariableMessage_failure_invalid_position(self):
        ''' creation of a PositiveVariableMessage object should fail if position is invalid '''
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        for position in positions:
            self.assertRaises(exceptions.BadParametersException, messages.PositiveVariableMessage, date=date, position=position, length=length)

    def test_PositiveVariableMessage_failure_invalid_length(self):
        ''' creation of a PositiveVariableMessage object should fail if length is invalid '''
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        for length in lengths:
            self.assertRaises(exceptions.BadParametersException, messages.PositiveVariableMessage, date=date, position=position, length=length)

    def test_NewUserNotificationMessage_failure_invalid_email(self):
        ''' creation of a NewUserNotivicationMessage should fail if email is invalid '''
        emails=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        code='AADDVVDDFSFDFSDFccsfdSDEEF'
        for email in emails:
            self.assertRaises(exceptions.BadParametersException, messages.NewUserNotificationMessage, email=email, code=code)

    def test_NewUserNotificationMessage_failure_invalid_code(self):
        ''' creation of a NewUserNotivicationMessage should fail if email is invalid '''
        codes=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',{'a','dict'},['a','list'],('a','tuple'), timeuuid.uuid1()]
        email='test_newusernotificationmessage@komlog.org'
        for code in codes:
            self.assertRaises(exceptions.BadParametersException, messages.NewUserNotificationMessage, email=email, code=code)

