import unittest
import uuid
import json
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.interface.imc.api import gestconsole
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status, exceptions
from komlog.komlibs.interface.imc.errors import Errors
from komlog.komlibs.general.time import timeuuid


class InterfaceImcModelMessagesTest(unittest.TestCase):
    ''' komlibs.interface.imc.model.messages tests '''

    def test_StoreSampleMessage_failure_invalid_sample_file(self):
        ''' creation os a StoreSampleMessage object should fail if sample_file is invalid '''
        sfs=[None, 23423, 2323.2342, {'a','dict'},['a','list'],('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        for sf in sfs:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.StoreSampleMessage(sample_file=sf)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_SSM_ISF)

    def test_MapVarsMessage_failure_invalid_did(self):
        ''' MapVarsMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MapVarsMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_IDID)

    def test_MapVarsMessage_failure_invalid_date(self):
        ''' MapVarsMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1().hex, uuid.uuid4()]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MapVarsMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_IDT)

    def test_MonitorVariableMessage_failure_invalid_username(self):
        ''' creation of a MonitorVariableMessage object should fail if username is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure_invalid_username_datapointname'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IUID)

    def test_MonitorVariableMessage_failure_invalid_datapointname(self):
        ''' creation of a MonitorVariableMessage object should fail if datapointname is invalid '''
        uid=uuid.uuid4()
        datapointnames=[None, 23423, 2323.2342, {'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        for datapointname in datapointnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IDPN)

    def test_MonitorVariableMessage_failure_invalid_did(self):
        ''' creation of a MonitorVariableMessage object should fail if did is invalid '''
        uid=uuid.uuid4()
        dids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IDID)

    def test_MonitorVariableMessage_failure_invalid_date(self):
        ''' creation of a MonitorVariableMessage object should fail if date is invalid '''
        uid=uuid.uuid4()
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        position=1
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IDT)

    def test_MonitorVariableMessage_failure_invalid_position(self):
        ''' creation of a MonitorVariableMessage object should fail if position is invalid '''
        uid=uuid.uuid4()
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        datapointname='test_MonitorVariableMessage_failure'
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IPOS)

    def test_MonitorVariableMessage_failure_invalid_length(self):
        ''' creation of a MonitorVariableMessage object should fail if length is invalid '''
        uid=uuid.uuid4()
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        datapointname='test_MonitorVariableMessage_failure'
        for length in lengths:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_ILEN)

    def test_GenerateDTreeMessage_failure_invalid_pid(self):
        ''' GenerateDTreeMessage creation should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.GenerateDTreeMessage(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_IPID)

    def test_FillDatapointMessage_failure_invalid_pid(self):
        ''' FillDatapointMessage creation should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.FillDatapointMessage(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_IPID)

    def test_FillDatapointMessage_failure_invalid_date(self):
        ''' FillDatapointMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1().hex, uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.FillDatapointMessage(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_IDT)

    def test_FillDatasourceMessage_failure_invalid_did(self):
        ''' FillDatasourceMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.FillDatasourceMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_IDID)

    def test_FillDatasourceMessage_failure_invalid_date(self):
        ''' FillDatasourceMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1().hex, uuid.uuid4()]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.FillDatasourceMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_IDT)

    def test_NegativeVariableMessage_failure_invalid_pid(self):
        ''' creation of a NegativeVariableMessage object should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NegativeVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IPID)

    def test_NegativeVariableMessage_failure_invalid_date(self):
        ''' creation of a NegativeVariableMessage object should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NegativeVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IDT)

    def test_NegativeVariableMessage_failure_invalid_position(self):
        ''' creation of a NegativeVariableMessage object should fail if position is invalid '''
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NegativeVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IPOS)

    def test_NegativeVariableMessage_failure_invalid_length(self):
        ''' creation of a NegativeVariableMessage object should fail if length is invalid '''
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        for length in lengths:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NegativeVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_ILEN)

    def test_PositiveVariableMessage_failure_invalid_pid(self):
        ''' creation of a PositiveVariableMessage object should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        date=timeuuid.uuid1()
        position=1
        length=1
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.PositiveVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IPID)

    def test_PositiveVariableMessage_failure_invalid_date(self):
        ''' creation of a PositiveVariableMessage object should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.PositiveVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IDT)

    def test_PositiveVariableMessage_failure_invalid_position(self):
        ''' creation of a PositiveVariableMessage object should fail if position is invalid '''
        positions=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        length=1
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.PositiveVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IPOS)

    def test_PositiveVariableMessage_failure_invalid_length(self):
        ''' creation of a PositiveVariableMessage object should fail if length is invalid '''
        lengths=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        for length in lengths:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.PositiveVariableMessage(pid=pid, date=date,position=position,length=length)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_ILEN)

    def test_NewUserNotificationMessage_failure_invalid_email(self):
        ''' creation of a NewUserNotivicationMessage should fail if email is invalid '''
        emails=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        code='AADDVVDDFSFDFSDFccsfdSDEEF'
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewUserNotificationMessage(email=email, code=code)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWUSR_IEMAIL)

    def test_NewUserNotificationMessage_failure_invalid_code(self):
        ''' creation of a NewUserNotivicationMessage should fail if email is invalid '''
        codes=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',{'a','dict'},['a','list'],('a','tuple'), timeuuid.uuid1()]
        email='test_newusernotificationmessage@komlog.org'
        for code in codes:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewUserNotificationMessage(email=email, code=code)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWUSR_ICODE)

    def test_UpdateQuotesMessage_failure_invalid_params(self):
        ''' UpdateQuotesMessage creation should fail if params is invalid '''
        paramss=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        operation=1
        for params in paramss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UpdateQuotesMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IPRM)

    def test_UpdateQuotesMessage_failure_invalid_operation(self):
        ''' UpdateQuotesMessage creation should fail if params is invalid '''
        operations=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        params={'did':uuid.uuid4()}
        for operation in operations:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UpdateQuotesMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IOP)

    def test_UpdateQuotesMessage_success(self):
        ''' UpdateQuotesMessage creation should succeed '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        msg=messages.UpdateQuotesMessage(params=params,operation=operation)
        self.assertTrue(isinstance(msg, messages.UpdateQuotesMessage))
        self.assertEqual(msg.type, messages.UPDATE_QUOTES_MESSAGE)

    def test_ResourceAuthorizationUpdateMessage_failure_invalid_params(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if params is invalid '''
        paramss=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        operation=1
        for params in paramss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ResourceAuthorizationUpdateMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_IPRM)

    def test_ResourceAuthorizationUpdateMessage_failure_invalid_operation(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if params is invalid '''
        operations=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        params={'did':uuid.uuid4()}
        for operation in operations:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ResourceAuthorizationUpdateMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_IOP)

    def test_ResourceAuthorizationUpdateMessage_success(self):
        ''' ResourceAuthorizationUpdateMessage creation should succeed '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        msg=messages.ResourceAuthorizationUpdateMessage(params=params,operation=operation)
        self.assertTrue(isinstance(msg, messages.ResourceAuthorizationUpdateMessage))
        self.assertEqual(msg.type, messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE)

    def test_NewDPWidgetMessage_failure_invalid_uid(self):
        ''' NewDPWidgetMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        pid=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewDPWidgetMessage(uid=uid,pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_IUID)

    def test_NewDPWidgetMessage_failure_invalid_pid(self):
        ''' NewDPWidgetMessage creation should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewDPWidgetMessage(uid=uid,pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_IPID)

    def test_NewDPWidgetMessage_success(self):
        ''' NewDPWidgetMessage creation should succeed '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg=messages.NewDPWidgetMessage(uid=uid,pid=pid)
        self.assertTrue(isinstance(msg, messages.NewDPWidgetMessage))
        self.assertEqual(msg.type, messages.NEW_DP_WIDGET_MESSAGE)

    def test_NewDSWidgetMessage_failure_invalid_uid(self):
        ''' NewDSWidgetMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewDSWidgetMessage(uid=uid,did=did)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_IUID)

    def test_NewDPWidgetMessage_failure_invalid_did(self):
        ''' NewDPWidgetMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewDSWidgetMessage(uid=uid,did=did)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_IDID)

    def test_NewDSWidgetMessage_success(self):
        ''' NewDSWidgetMessage creation should succeed '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg=messages.NewDSWidgetMessage(uid=uid,did=did)
        self.assertTrue(isinstance(msg, messages.NewDSWidgetMessage))
        self.assertEqual(msg.type, messages.NEW_DS_WIDGET_MESSAGE)

    def test_DeleteUserMessage_failure_invalid_uid(self):
        ''' DeleteUserMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteUserMessage(uid=uid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELUSER_IUID)

    def test_DeleteUserMessage_success(self):
        ''' DeleteUserMessage creation should succeed '''
        uid=uuid.uuid4()
        msg=messages.DeleteUserMessage(uid=uid)
        self.assertTrue(isinstance(msg, messages.DeleteUserMessage))
        self.assertEqual(msg.type, messages.DELETE_USER_MESSAGE)

    def test_DeleteAgentMessage_failure_invalid_aid(self):
        ''' DeleteAgentMessage creation should fail if aid is invalid '''
        aids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for aid in aids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteAgentMessage(aid=aid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELAGENT_IAID)

    def test_DeleteAgentMessage_success(self):
        ''' DeleteAgentMessage creation should succeed '''
        aid=uuid.uuid4()
        msg=messages.DeleteAgentMessage(aid=aid)
        self.assertTrue(isinstance(msg, messages.DeleteAgentMessage))
        self.assertEqual(msg.type, messages.DELETE_AGENT_MESSAGE)

    def test_DeleteDatasourceMessage_failure_invalid_did(self):
        ''' DeleteDatasourceMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteDatasourceMessage(did=did)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDS_IDID)

    def test_DeleteDatasourceMessage_success(self):
        ''' DeleteDatasourceMessage creation should succeed '''
        did=uuid.uuid4()
        msg=messages.DeleteDatasourceMessage(did=did)
        self.assertTrue(isinstance(msg, messages.DeleteDatasourceMessage))
        self.assertEqual(msg.type, messages.DELETE_DATASOURCE_MESSAGE)

    def test_DeleteDatapointMessage_failure_invalid_pid(self):
        ''' DeleteDatapointMessage creation should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteDatapointMessage(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDP_IPID)

    def test_DeleteDatapointMessage_success(self):
        ''' DeleteDatapointMessage creation should succeed '''
        pid=uuid.uuid4()
        msg=messages.DeleteDatapointMessage(pid=pid)
        self.assertTrue(isinstance(msg, messages.DeleteDatapointMessage))
        self.assertEqual(msg.type, messages.DELETE_DATAPOINT_MESSAGE)

    def test_DeleteWidgetMessage_failure_invalid_wid(self):
        ''' DeleteWidgetMessage creation should fail if wid is invalid '''
        wids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for wid in wids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteWidgetMessage(wid=wid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELWIDGET_IWID)

    def test_DeleteWidgetMessage_success(self):
        ''' DeleteWidgetMessage creation should succeed '''
        wid=uuid.uuid4()
        msg=messages.DeleteWidgetMessage(wid=wid)
        self.assertTrue(isinstance(msg, messages.DeleteWidgetMessage))
        self.assertEqual(msg.type, messages.DELETE_WIDGET_MESSAGE)

    def test_DeleteDashboardMessage_failure_invalid_bid(self):
        ''' DeleteDashboardMessage creation should fail if bid is invalid '''
        bids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        for bid in bids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DeleteDashboardMessage(bid=bid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDASHB_IBID)

    def test_DeleteDashboardMessage_success(self):
        ''' DeleteDashboardMessage creation should succeed '''
        bid=uuid.uuid4()
        msg=messages.DeleteDashboardMessage(bid=bid)
        self.assertTrue(isinstance(msg, messages.DeleteDashboardMessage))
        self.assertEqual(msg.type, messages.DELETE_DASHBOARD_MESSAGE)

    def test_UserEventMessage_failure_invalid_uid(self):
        ''' UserEventMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        event_type=0
        parameters={'params':'a'}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IUID)

    def test_UserEventMessage_failure_invalid_event_type(self):
        ''' UserEventMessage creation should fail if event type is invalid '''
        event_types=[None, -1,2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        parameters={'params':'a'}
        for event_type in event_types:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IET)

    def test_UserEventMessage_failure_invalid_parameters(self):
        ''' UserEventMessage creation should fail if parameters is invalid '''
        parameterss=[-1,2323.2342, 'Username',['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        event_type=0
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IPRM)

    def test_UserEventMessage_success(self):
        ''' UserEventMessage creation should succeed '''
        uid=uuid.uuid4()
        event_type=0
        parameters={'a':'dict'}
        msg=messages.UserEventMessage(uid=uid, event_type=event_type, parameters=parameters)
        self.assertTrue(isinstance(msg, messages.UserEventMessage))
        self.assertEqual(msg.type, messages.USER_EVENT_MESSAGE)

    def test_UserEventResponseMessage_failure_invalid_uid(self):
        ''' UserEventResponseMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        date=timeuuid.uuid1()
        parameters={'params':'a'}
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IUID)

    def test_UserEventResponseMessage_failure_invalid_date(self):
        ''' UserEventResponseMessage creation should fail if event type is invalid '''
        dates=[None, -1,2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        parameters={'params':'a'}
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IDT)

    def test_UserEventResponseMessage_failure_invalid_parameters(self):
        ''' UserEventResponseMessage creation should fail if parameters is invalid '''
        parameterss=[-1,2323.2342, 'Username',['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        for parameters in parameterss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IPRM)

    def test_UserEventResponseMessage_success(self):
        ''' UserEventResponseMessage creation should succeed '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={'a':'dict'}
        msg=messages.UserEventResponseMessage(uid=uid, date=date, parameters=parameters)
        self.assertTrue(isinstance(msg, messages.UserEventResponseMessage))
        self.assertEqual(msg.type, messages.USER_EVENT_RESPONSE_MESSAGE)

    def test_GenerateTextSummaryMessage_failure_invalid_did(self):
        ''' GenerateTextSummaryMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.GenerateTextSummaryMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_IDID)

    def test_GenerateTextSummaryMessage_failure_invalid_date(self):
        ''' GenerateTextSummaryMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.GenerateTextSummaryMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_IDT)

    def test_GenerateTextSummaryMessage_success(self):
        ''' GenerateTextSummaryMessage creation should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg=messages.GenerateTextSummaryMessage(did=did, date=date)
        self.assertTrue(isinstance(msg, messages.GenerateTextSummaryMessage))
        self.assertEqual(msg.type, messages.GENERATE_TEXT_SUMMARY_MESSAGE)

    def test_MissingDatapointMessage_failure_invalid_did(self):
        ''' MissingDatapointMessage creation should fail if did is invalid '''
        dids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MissingDatapointMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_IDID)

    def test_MissingDatapointMessage_failure_invalid_date(self):
        ''' MissingDatapointMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.MissingDatapointMessage(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_IDT)

    def test_MissingDatapointMessage_success(self):
        ''' MissingDatapointMessage creation should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg=messages.MissingDatapointMessage(did=did, date=date)
        self.assertTrue(isinstance(msg, messages.MissingDatapointMessage))
        self.assertEqual(msg.type, messages.MISSING_DATAPOINT_MESSAGE)

    def test_NewInvitationMailMessage_failure_invalid_email(self):
        ''' NewInvitationMailMessage creation should fail if email is invalid '''
        emails=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        inv_id=uuid.uuid4()
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewInvitationMailMessage(email=email, inv_id=inv_id)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_IEMAIL)

    def test_NewInvitationMailMessage_failure_invalid_invitation_id(self):
        ''' NewInvitationMailMessage creation should fail if email is invalid '''
        inv_ids=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        email='test_newinvitationmailmessage_failure_invalid_invitation_id@komlog.org'
        for inv_id in inv_ids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.NewInvitationMailMessage(email=email, inv_id=inv_id)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_IINV)

    def test_NewInvitationMailMessage_success(self):
        ''' NewInvitationMailMessage creation should succeed '''
        email='test_newinvitationmailmessage_success@komlog.org'
        inv_id=uuid.uuid4()
        msg=messages.NewInvitationMailMessage(email=email, inv_id=inv_id)
        self.assertTrue(isinstance(msg, messages.NewInvitationMailMessage))
        self.assertEqual(msg.type, messages.NEW_INV_MAIL_MESSAGE)

    def test_ForgetMailMessage_failure_invalid_email(self):
        ''' ForgetMailMessage creation should fail if email is invalid '''
        emails=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        code=uuid.uuid4()
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ForgetMailMessage(email=email,code=code)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_IEMAIL)

    def test_ForgetMailMessage_failure_invalid_invitation_id(self):
        ''' ForgetMailMessage creation should fail if email is invalid '''
        codes=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        email='test_newinvitationmailmessage_failure_invalid_invitation_id@komlog.org'
        for code in codes:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ForgetMailMessage(email=email, code=code)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_ICODE)

    def test_ForgetMailMessage_success(self):
        ''' ForgetMailMessage creation should succeed '''
        email='test_newinvitationmailmessage_success@komlog.org'
        code=uuid.uuid4()
        msg=messages.ForgetMailMessage(email=email, code=code)
        self.assertTrue(isinstance(msg, messages.ForgetMailMessage))
        self.assertEqual(msg.type, messages.FORGET_MAIL_MESSAGE)

    def test_UrisUpdatedMessage_failure_invalid_date(self):
        ''' UrisUpdatedMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        uris=[{'uri':'uri','type':'type','id':uuid.uuid4()}]
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UrisUpdatedMessage(uris=uris, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IDT)

    def test_UrisUpdatedMessage_success(self):
        ''' UrisUpdatedMessage creation should succeed '''
        uris=[{'uri':'uri','type':'type','id':uuid.uuid4()}]
        date=uuid.uuid1()
        msg=messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertTrue(isinstance(msg, messages.UrisUpdatedMessage))
        self.assertEqual(msg.type, messages.URIS_UPDATED_MESSAGE)

    def test_SendSessionDataMessage_failure_invalid_date(self):
        ''' SendSessionDataMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        data=[{'uri':'uri','content':'content'}]
        sid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.SendSessionDataMessage(sid=sid,data=data, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_IDT)

    def test_SendSessionDataMessage_failure_invalid_sid(self):
        ''' SendSessionDataMessage creation should fail if sid is invalid '''
        sids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        data=[{'uri':'uri','content':'content'}]
        date=uuid.uuid1()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.SendSessionDataMessage(sid=sid,data=data, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_ISID)

    def test_SendSessionDataMessage_success(self):
        ''' SendSessionDataMessage creation should succeed '''
        data=[{'uri':'uri','content':'content'}]
        sid=uuid.uuid4()
        date=uuid.uuid1()
        msg=messages.SendSessionDataMessage(sid=sid, data=data, date=date)
        self.assertTrue(isinstance(msg, messages.SendSessionDataMessage))
        self.assertEqual(msg.type, messages.SEND_SESSION_DATA_MESSAGE)

    def test_ClearSessionHooksMessage_failure_invalid_sid(self):
        ''' ClearSessionHooksMessage creation should fail if sid is invalid '''
        sids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        ids=[(uuid.uuid4(), 'd'),(uuid.uuid4(),'p')]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ClearSessionHooksMessage(sid=sid,ids=ids)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_ISID)

    def test_ClearSessionHooksMessage_success(self):
        ''' ClearSessionHooksMessage creation should succeed '''
        sid=uuid.uuid4()
        ids=[(uuid.uuid4(), 'd'),(uuid.uuid4(),'p')]
        msg=messages.ClearSessionHooksMessage(sid=sid, ids=ids)
        self.assertTrue(isinstance(msg, messages.ClearSessionHooksMessage))
        self.assertEqual(msg.type, messages.CLEAR_SESSION_HOOKS_MESSAGE)

    def test_HookNewUrisMessage_failure_invalid_uid(self):
        ''' HookNewUrisMessage creation should fail if uid is invalid '''
        uids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uris=[]
        date=timeuuid.uuid1()
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.HookNewUrisMessage(uid=uid,uris=uris, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IUID)

    def test_HookNewUrisMessage_failure_invalid_date(self):
        ''' HookNewUrisMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), uuid.uuid1().hex, json.dumps('username'), 'user\nname','user\tname']
        uris=[]
        uid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.HookNewUrisMessage(uid=uid,uris=uris, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IDT)

    def test_HookNewUrisMessage_success(self):
        ''' HookNewUrisMessage creation should succeed '''
        uid=uuid.uuid4()
        uris=[{'uri':'uri','type':'type','id':uuid.uuid4()}]
        date=uuid.uuid1()
        msg=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertTrue(isinstance(msg, messages.HookNewUrisMessage))
        self.assertEqual(msg.type, messages.HOOK_NEW_URIS_MESSAGE)

