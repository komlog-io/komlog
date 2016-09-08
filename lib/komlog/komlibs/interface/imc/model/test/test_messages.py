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

    def test_MapVarsMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' MapVarsMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.MapVarsMessage._type_.value,'1','2','3'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_ELFS)

    def test_MapVarsMessage_failure_load_from_serialization_invalid_message(self):
        ''' MapVarsMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_MINS)

    def test_MapVarsMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' MapVarsMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_IST)

    def test_MapVarsMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' MapVarsMessage creation should fail if we pass a string with invalid did '''
        msg='|'.join((messages.MapVarsMessage._type_.value,'1',timeuuid.uuid1().hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_IHDID)

    def test_MapVarsMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' MapVarsMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join((messages.MapVarsMessage._type_.value,uuid.uuid4().hex,'2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MVM_IHDATE)

    def test_MapVarsMessage_success_load_from_serialization(self):
        ''' MapVarsMessage creation should succeed calling the classmethod load_from_serialization '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MapVarsMessage._type_.value,did.hex,date.hex))
        obj=messages.MapVarsMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.MAP_VARS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MapVarsMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MapVarsMessage_success_load_from_serialization_base_class(self):
        ''' MapVarsMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MapVarsMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.MAP_VARS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MapVarsMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MapVarsMessage_to_serialization_success(self):
        ''' MapVarsMessage to_serialization should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MapVarsMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.MAP_VARS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MapVarsMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

    def test_MonitorVariableMessage_failure_invalid_uid(self):
        ''' creation of a MonitorVariableMessage object should fail if uid is invalid '''
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

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' MonitorVariableMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.MonitorVariableMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_ELFS)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_message(self):
        ''' MonitorVariableMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_MINS)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3','4','5','6'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IST)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,'1',did.hex, date.hex, str(position), str(length), datapointname))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IHUID)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with invalid did '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, 'uhh', date.hex, str(position), str(length), datapointname))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IHDID)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with invalid date '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, 'date', str(position), str(length), datapointname))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_IHDATE)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_string_position(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with invalid position'''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, date.hex, 'position', str(length), datapointname))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_ISPOS)

    def test_MonitorVariableMessage_failure_load_from_serialization_invalid_string_length(self):
        ''' MonitorVariableMessage creation should fail if we pass a string with invalid length '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, date.hex, str(position), 'str(length)', datapointname))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MONVAR_ISLEN)

    def test_MonitorVariableMessage_success_load_from_serialization(self):
        ''' MonitorVariableMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, date.hex, str(position), str(length), datapointname))
        obj=messages.MonitorVariableMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj.datapointname, datapointname)
        self.assertEqual(obj._type_, messages.Messages.MON_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MonitorVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MonitorVariableMessage_success_load_from_serialization_base_class(self):
        ''' MonitorVariableMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, date.hex, str(position), str(length), datapointname))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj.datapointname, datapointname)
        self.assertEqual(obj._type_, messages.Messages.MON_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MonitorVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MonitorVariableMessage_to_serialization_success(self):
        ''' MonitorVariableMessage.to_serialization should succeed '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=2
        datapointname='datapointname'
        msg='|'.join((messages.MonitorVariableMessage._type_.value,uid.hex, did.hex, date.hex, str(position), str(length), datapointname))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj.datapointname, datapointname)
        self.assertEqual(obj._type_, messages.Messages.MON_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MonitorVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

    def test_GenerateDTreeMessage_failure_invalid_pid(self):
        ''' GenerateDTreeMessage creation should fail if pid is invalid '''
        pids=[None, 23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1()]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.GenerateDTreeMessage(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_IPID)

    def test_GenerateDTreeMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' GenerateDTreeMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.GenerateDTreeMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateDTreeMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_ELFS)

    def test_GenerateDTreeMessage_failure_load_from_serialization_invalid_message(self):
        ''' GenerateDTreeMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateDTreeMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_MINS)

    def test_GenerateDTreeMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' GenerateDTreeMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateDTreeMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_IST)

    def test_GenerateDTreeMessage_failure_load_from_serialization_invalid_hex_pid(self):
        ''' GenerateDTreeMessage creation should fail if we pass a string with invalid pid '''
        pid=uuid.uuid4()
        msg='|'.join((messages.GenerateDTreeMessage._type_.value,'pid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateDTreeMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GDTREE_IHPID)

    def test_GenerateDTreeMessage_success_load_from_serialization(self):
        ''' GenerateDTreeMessage creation should succeed calling the classmethod load_from_serialization '''
        pid=uuid.uuid4()
        msg='|'.join((messages.GenerateDTreeMessage._type_.value,pid.hex))
        obj=messages.GenerateDTreeMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.GDTREE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateDTreeMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_GenerateDTreeMessage_success_load_from_serialization_base_class(self):
        '''  GenerateDTreeMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        pid=uuid.uuid4()
        msg='|'.join((messages.GenerateDTreeMessage._type_.value,pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.GDTREE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateDTreeMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_GenerateDTreeMessage_to_serialization_success(self):
        ''' GenerateDTreeMessage.to_serialization should succeed '''
        pid=uuid.uuid4()
        msg='|'.join((messages.GenerateDTreeMessage._type_.value, pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.GDTREE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateDTreeMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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

    def test_FillDatapointMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' FillDatapointMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.FillDatapointMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_ELFS)

    def test_FillDatapointMessage_failure_load_from_serialization_invalid_message(self):
        ''' FillDatapointMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_MINS)

    def test_FillDatapointMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' FillDatapointMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_IST)

    def test_FillDatapointMessage_failure_load_from_serialization_invalid_hex_pid(self):
        ''' FillDatapointMessage creation should fail if we pass a string with invalid pid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatapointMessage._type_.value,'pid.hex',date.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_IHPID)

    def test_FillDatapointMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' FillDatapointMessage creation should fail if we pass a string with invalid date '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatapointMessage._type_.value,pid.hex,'date.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDP_IHDATE)

    def test_FillDatapointMessage_success_load_from_serialization(self):
        ''' FillDatapointMessage creation should succeed calling the classmethod load_from_serialization '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatapointMessage._type_.value,pid.hex, date.hex))
        obj=messages.FillDatapointMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_FillDatapointMessage_success_load_from_serialization_base_class(self):
        '''  FillDatapointMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatapointMessage._type_.value,pid.hex, date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_FillDatapointMessage_to_serialization_success(self):
        '''FillDatapointMessage .to_serialization should succeed '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatapointMessage._type_.value, pid.hex, date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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

    def test_FillDatasourceMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' FillDatasourceMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.FillDatasourceMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_ELFS)

    def test_FillDatasourceMessage_failure_load_from_serialization_invalid_message(self):
        ''' FillDatasourceMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_MINS)

    def test_FillDatasourceMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' FillDatasourceMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_IST)

    def test_FillDatasourceMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' FillDatasourceMessage creation should fail if we pass a string with invalid did '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatasourceMessage._type_.value,'did.hex',date.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_IHDID)

    def test_FillDatasourceMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' FillDatasourceMessage creation should fail if we pass a string with invalid date '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatasourceMessage._type_.value,did.hex,'date.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FILLDS_IHDATE)

    def test_FillDatasourceMessage_success_load_from_serialization(self):
        ''' FillDatasourceMessage creation should succeed calling the classmethod load_from_serialization '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatasourceMessage._type_.value,did.hex, date.hex))
        obj=messages.FillDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_FillDatasourceMessage_success_load_from_serialization_base_class(self):
        '''  FillDatasourceMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatasourceMessage._type_.value,did.hex, date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_FillDatasourceMessage_to_serialization_success(self):
        '''FillDatasourceMessage .to_serialization should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.FillDatasourceMessage._type_.value, did.hex, date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.FILL_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.FillDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' NegativeVariableMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.NegativeVariableMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_ELFS)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_message(self):
        ''' NegativeVariableMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_MINS)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' NegativeVariableMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3','4'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IST)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' NegativeVariableMessage creation should fail if we pass a string with invalid did '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,'pid.hex',date.hex,str(position),str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IHPID)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' NegativeVariableMessage creation should fail if we pass a string with invalid date '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,'date.hex',str(position),str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_IHDATE)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_string_position(self):
        ''' NegativeVariableMessage creation should fail if we pass a string with invalid pos '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,date.hex,'str(position)',str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_ISPOS)

    def test_NegativeVariableMessage_failure_load_from_serialization_invalid_string_length(self):
        ''' NegativeVariableMessage creation should fail if we pass a string with invalid length'''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,date.hex,str(position),'str(length)'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEGVAR_ISLEN)

    def test_NegativeVariableMessage_success_load_from_serialization(self):
        ''' NegativeVariableMessage creation should succeed calling the classmethod load_from_serialization '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.NegativeVariableMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.NEG_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NegativeVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NegativeVariableMessage_success_load_from_serialization_base_class(self):
        '''  NegativeVariableMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.NEG_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NegativeVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NegativeVariableMessage_to_serialization_success(self):
        '''NegativeVariableMessage .to_serialization should succeed '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.NegativeVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.NEG_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NegativeVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' PositiveVariableMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.PositiveVariableMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_ELFS)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_message(self):
        ''' PositiveVariableMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_MINS)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' PositiveVariableMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3','4'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IST)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' PositiveVariableMessage creation should fail if we pass a string with invalid did '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,'pid.hex',date.hex,str(position),str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IHPID)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' PositiveVariableMessage creation should fail if we pass a string with invalid date '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,'date.hex',str(position),str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_IHDATE)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_string_position(self):
        ''' PositiveVariableMessage creation should fail if we pass a string with invalid pos '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,date.hex,'str(position)',str(length)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_ISPOS)

    def test_PositiveVariableMessage_failure_load_from_serialization_invalid_string_length(self):
        ''' PositiveVariableMessage creation should fail if we pass a string with invalid length'''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,date.hex,str(position),'str(length)'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_POSVAR_ISLEN)

    def test_PositiveVariableMessage_success_load_from_serialization(self):
        ''' PositiveVariableMessage creation should succeed calling the classmethod load_from_serialization '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.PositiveVariableMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.POS_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.PositiveVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_PositiveVariableMessage_success_load_from_serialization_base_class(self):
        '''  PositiveVariableMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.POS_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.PositiveVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_PositiveVariableMessage_to_serialization_success(self):
        '''PositiveVariableMessage .to_serialization should succeed '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        msg='|'.join((messages.PositiveVariableMessage._type_.value,pid.hex,date.hex,str(position),str(length)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.position, position)
        self.assertEqual(obj.length, length)
        self.assertEqual(obj._type_, messages.Messages.POS_VAR_MESSAGE)
        self.assertTrue(isinstance(obj, messages.PositiveVariableMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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

    def test_NewUserNotificationMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' NewUserNotificationMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.NewUserNotificationMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewUserNotificationMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWUSR_ELFS)

    def test_NewUserNotificationMessage_failure_load_from_serialization_invalid_message(self):
        ''' NewUserNotificationMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewUserNotificationMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWUSR_MINS)

    def test_NewUserNotificationMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' NewUserNotificationMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewUserNotificationMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWUSR_IST)

    def test_NewUserNotificationMessage_success_load_from_serialization(self):
        ''' NewUserNotificationMessage creation should succeed calling the classmethod load_from_serialization '''
        email='test@komlog.org'
        code='code'
        msg='|'.join((messages.NewUserNotificationMessage._type_.value,email,code))
        obj=messages.NewUserNotificationMessage.load_from_serialization(msg)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj.code, code)
        self.assertEqual(obj._type_, messages.Messages.NEW_USR_NOTIF_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewUserNotificationMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewUserNotificationMessage_success_load_from_serialization_base_class(self):
        '''  NewUserNotificationMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        email='test@komlog.org'
        code='code'
        msg='|'.join((messages.NewUserNotificationMessage._type_.value,email,code))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj.code, code)
        self.assertEqual(obj._type_, messages.Messages.NEW_USR_NOTIF_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewUserNotificationMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewUserNotificationMessage_to_serialization_success(self):
        '''NewUserNotificationMessage .to_serialization should succeed '''
        email='test@komlog.org'
        code='code'
        msg='|'.join((messages.NewUserNotificationMessage._type_.value,email,code))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj.code, code)
        self.assertEqual(obj._type_, messages.Messages.NEW_USR_NOTIF_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewUserNotificationMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

    def test_UpdateQuotesMessage_failure_invalid_params(self):
        ''' UpdateQuotesMessage creation should fail if params is invalid '''
        paramss=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        operation=Operations.NEW_AGENT
        for params in paramss:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UpdateQuotesMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IPRM)

    def test_UpdateQuotesMessage_failure_invalid_operation(self):
        ''' UpdateQuotesMessage creation should fail if params is invalid '''
        operations=[None, 1, 'nonexistentname', -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        params={'did':uuid.uuid4()}
        for operation in operations:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UpdateQuotesMessage(params=params,operation=operation)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IOP)

    def test_UpdateQuotesMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' UpdateQuotesMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_ELFS)

    def test_UpdateQuotesMessage_failure_load_from_serialization_invalid_message(self):
        ''' UpdateQuotesMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_MINS)

    def test_UpdateQuotesMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' UpdateQuotesMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IST)

    def test_UpdateQuotesMessage_failure_load_from_serialization_invalid_json_params(self):
        ''' UpdateQuotesMessage creation should fail if we pass invalid json params '''
        params='invalid json params'
        operation=Operations.NEW_DATASOURCE
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,operation.name,params))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IJSPRM)

    def test_UpdateQuotesMessage_failure_load_from_serialization_invalid_operation_name(self):
        ''' UpdateQuotesMessage creation should fail if we pass invalid operation name '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        operation_name='nonexistent_operationname'
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,operation_name,js_params))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_UPDQUO_IOPN)

    def test_UpdateQuotesMessage_success_load_from_serialization(self):
        ''' UpdateQuotesMessage creation should succeed calling the classmethod load_from_serialization '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,operation.name,js_params))
        obj=messages.UpdateQuotesMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.UPDATE_QUOTES_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UpdateQuotesMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UpdateQuotesMessage_success_load_from_serialization_base_class(self):
        '''  UpdateQuotesMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,operation.name,js_params))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.UPDATE_QUOTES_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UpdateQuotesMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UpdateQuotesMessage_to_serialization_success(self):
        '''UpdateQuotesMessage .to_serialization should succeed '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        msg='|'.join((messages.UpdateQuotesMessage._type_.value,operation.name,js_params))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.UPDATE_QUOTES_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UpdateQuotesMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2 = obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj.params, obj2.params)
        self.assertEqual(obj.operation, obj2.operation)
        self.assertEqual(obj._type_, obj2._type_)
        self.assertTrue(isinstance(obj2, messages.UpdateQuotesMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

    def test_ResourceAuthorizationUpdateMessage_failure_invalid_params(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if params is invalid '''
        paramss=[None, -23423, 2323.2342, 'User/name no ASCII ññññ',['a','list'],('a','tuple'), timeuuid.uuid1()]
        operation=Operations.NEW_DASHBOARD
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
        self.assertEqual(msg.type, messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE)
        self.assertEqual(msg.params, params)
        self.assertEqual(msg.operation, operation)

    def test_ResourceAuthorizationUpdateMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_ELFS)

    def test_ResourceAuthorizationUpdateMessage_failure_load_from_serialization_invalid_message(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_MINS)

    def test_ResourceAuthorizationUpdateMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_IST)

    def test_ResourceAuthorizationUpdateMessage_failure_load_from_serialization_invalid_json_params(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if we pass invalid json params '''
        params='invalid json params'
        operation=Operations.NEW_DATASOURCE
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,operation.name,params))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_IJSPRM)

    def test_ResourceAuthorizationUpdateMessage_failure_load_from_serialization_invalid_operation_name(self):
        ''' ResourceAuthorizationUpdateMessage creation should fail if we pass invalid operation name '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        operation_name='nonexistent_operationname'
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,operation_name,js_params))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_RESAUTH_IOPN)

    def test_ResourceAuthorizationUpdateMessage_success_load_from_serialization(self):
        ''' ResourceAuthorizationUpdateMessage creation should succeed calling the classmethod load_from_serialization '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,operation.name,js_params))
        obj=messages.ResourceAuthorizationUpdateMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ResourceAuthorizationUpdateMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ResourceAuthorizationUpdateMessage_success_load_from_serialization_base_class(self):
        '''  ResourceAuthorizationUpdateMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'did':params['did'].hex, 'uid':params['uid'].hex, 'aid':params['aid'].hex})
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,operation.name,js_params))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ResourceAuthorizationUpdateMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ResourceAuthorizationUpdateMessage_to_serialization_success(self):
        '''ResourceAuthorizationUpdateMessage .to_serialization should succeed '''
        params={'did':uuid.uuid4(),'uid':uuid.uuid4(), 'aid':uuid.uuid4()}
        operation=Operations.NEW_DATASOURCE
        js_params=json.dumps({'aid':params['aid'].hex, 'uid':params['uid'].hex, 'did':params['did'].hex})
        msg='|'.join((messages.ResourceAuthorizationUpdateMessage._type_.value,operation.name,js_params))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.params, params)
        self.assertEqual(obj.operation, operation)
        self.assertEqual(obj._type_, messages.Messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ResourceAuthorizationUpdateMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2 = obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj.params, obj2.params)
        self.assertEqual(obj.operation, obj2.operation)
        self.assertEqual(obj._type_, obj2._type_)
        self.assertTrue(isinstance(obj2, messages.ResourceAuthorizationUpdateMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

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
        self.assertEqual(msg._type_, messages.Messages.NEW_DP_WIDGET_MESSAGE)

    def test_NewDPWidgetMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' NewDPWidgetMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.NewDPWidgetMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_ELFS)

    def test_NewDPWidgetMessage_failure_load_from_serialization_invalid_message(self):
        ''' NewDPWidgetMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_MINS)

    def test_NewDPWidgetMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' NewDPWidgetMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_IST)

    def test_NewDPWidgetMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' NewDPWidgetMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg='|'.join((messages.NewDPWidgetMessage._type_.value,'uid.hex',pid.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_IHUID)

    def test_NewDPWidgetMessage_failure_load_from_serialization_invalid_hex_pid(self):
        ''' NewDPWidgetMessage creation should fail if we pass a string with invalid pid '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg='|'.join((messages.NewDPWidgetMessage._type_.value,uid.hex,'pid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDPW_IHPID)

    def test_NewDPWidgetMessage_success_load_from_serialization(self):
        ''' NewDPWidgetMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg='|'.join((messages.NewDPWidgetMessage._type_.value,uid.hex, pid.hex))
        obj=messages.NewDPWidgetMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.NEW_DP_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDPWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewDPWidgetMessage_success_load_from_serialization_base_class(self):
        '''  NewDPWidgetMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg='|'.join((messages.NewDPWidgetMessage._type_.value, uid.hex, pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.NEW_DP_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDPWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewDPWidgetMessage_to_serialization_success(self):
        '''NewDPWidgetMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        msg='|'.join((messages.NewDPWidgetMessage._type_.value, uid.hex, pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.NEW_DP_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDPWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.NEW_DS_WIDGET_MESSAGE)

    def test_NewDSWidgetMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' NewDSWidgetMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.NewDSWidgetMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_ELFS)

    def test_NewDSWidgetMessage_failure_load_from_serialization_invalid_message(self):
        ''' NewDSWidgetMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_MINS)

    def test_NewDSWidgetMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' NewDSWidgetMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_IST)

    def test_NewDSWidgetMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' NewDSWidgetMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg='|'.join((messages.NewDSWidgetMessage._type_.value,'uid.hex',did.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_IHUID)

    def test_NewDSWidgetMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' NewDSWidgetMessage creation should fail if we pass a string with invalid did '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg='|'.join((messages.NewDSWidgetMessage._type_.value,uid.hex,'did.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWDSW_IHDID)

    def test_NewDSWidgetMessage_success_load_from_serialization(self):
        ''' NewDSWidgetMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg='|'.join((messages.NewDSWidgetMessage._type_.value,uid.hex, did.hex))
        obj=messages.NewDSWidgetMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.NEW_DS_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDSWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewDSWidgetMessage_success_load_from_serialization_base_class(self):
        '''  NewDSWidgetMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg='|'.join((messages.NewDSWidgetMessage._type_.value, uid.hex, did.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.NEW_DS_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDSWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewDSWidgetMessage_to_serialization_success(self):
        '''NewDSWidgetMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        msg='|'.join((messages.NewDSWidgetMessage._type_.value, uid.hex, did.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.NEW_DS_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewDSWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_USER_MESSAGE)
        self.assertEqual(msg.uid, uid)

    def test_DeleteUserMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteUserMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteUserMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteUserMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELUSER_ELFS)

    def test_DeleteUserMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteUserMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteUserMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELUSER_MINS)

    def test_DeleteUserMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteUserMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteUserMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELUSER_IST)

    def test_DeleteUserMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' DeleteUserMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        msg='|'.join((messages.DeleteUserMessage._type_.value,'uid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteUserMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELUSER_IHUID)

    def test_DeleteUserMessage_success_load_from_serialization(self):
        ''' DeleteUserMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        msg='|'.join((messages.DeleteUserMessage._type_.value,uid.hex))
        obj=messages.DeleteUserMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_USER_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteUserMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteUserMessage_success_load_from_serialization_base_class(self):
        '''  DeleteUserMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        msg='|'.join((messages.DeleteUserMessage._type_.value, uid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_USER_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteUserMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteUserMessage_to_serialization_success(self):
        '''DeleteUserMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        msg='|'.join((messages.DeleteUserMessage._type_.value, uid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_USER_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteUserMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_AGENT_MESSAGE)

    def test_DeleteAgentMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteAgentMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteAgentMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteAgentMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELAGENT_ELFS)

    def test_DeleteAgentMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteAgentMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteAgentMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELAGENT_MINS)

    def test_DeleteAgentMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteAgentMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteAgentMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELAGENT_IST)

    def test_DeleteAgentMessage_failure_load_from_serialization_invalid_hex_aid(self):
        ''' DeleteAgentMessage creation should fail if we pass a string with invalid aid '''
        aid=uuid.uuid4()
        msg='|'.join((messages.DeleteAgentMessage._type_.value,'aid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteAgentMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELAGENT_IHAID)

    def test_DeleteAgentMessage_success_load_from_serialization(self):
        ''' DeleteAgentMessage creation should succeed calling the classmethod load_from_serialization '''
        aid=uuid.uuid4()
        msg='|'.join((messages.DeleteAgentMessage._type_.value,aid.hex))
        obj=messages.DeleteAgentMessage.load_from_serialization(msg)
        self.assertEqual(obj.aid, aid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_AGENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteAgentMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteAgentMessage_success_load_from_serialization_base_class(self):
        '''  DeleteAgentMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        aid=uuid.uuid4()
        msg='|'.join((messages.DeleteAgentMessage._type_.value, aid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.aid, aid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_AGENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteAgentMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteAgentMessage_to_serialization_success(self):
        '''DeleteAgentMessage .to_serialization should succeed '''
        aid=uuid.uuid4()
        msg='|'.join((messages.DeleteAgentMessage._type_.value, aid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.aid, aid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_AGENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteAgentMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_DATASOURCE_MESSAGE)

    def test_DeleteDatasourceMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteDatasourceMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteDatasourceMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDS_ELFS)

    def test_DeleteDatasourceMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteDatasourceMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDS_MINS)

    def test_DeleteDatasourceMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteDatasourceMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDS_IST)

    def test_DeleteDatasourceMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' DeleteDatasourceMessage creation should fail if we pass a string with invalid did '''
        did=uuid.uuid4()
        msg='|'.join((messages.DeleteDatasourceMessage._type_.value,'did.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDS_IHDID)

    def test_DeleteDatasourceMessage_success_load_from_serialization(self):
        ''' DeleteDatasourceMessage creation should succeed calling the classmethod load_from_serialization '''
        did=uuid.uuid4()
        msg='|'.join((messages.DeleteDatasourceMessage._type_.value,did.hex))
        obj=messages.DeleteDatasourceMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDatasourceMessage_success_load_from_serialization_base_class(self):
        '''  DeleteDatasourceMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        did=uuid.uuid4()
        msg='|'.join((messages.DeleteDatasourceMessage._type_.value, did.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDatasourceMessage_to_serialization_success(self):
        '''DeleteDatasourceMessage .to_serialization should succeed '''
        did=uuid.uuid4()
        msg='|'.join((messages.DeleteDatasourceMessage._type_.value, did.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATASOURCE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatasourceMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_DATAPOINT_MESSAGE)

    def test_DeleteDatapointMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteDatapointMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteDatapointMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDP_ELFS)

    def test_DeleteDatapointMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteDatapointMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDP_MINS)

    def test_DeleteDatapointMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteDatapointMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDP_IST)

    def test_DeleteDatapointMessage_failure_load_from_serialization_invalid_hex_pid(self):
        ''' DeleteDatapointMessage creation should fail if we pass a string with invalid pid '''
        pid=uuid.uuid4()
        msg='|'.join((messages.DeleteDatapointMessage._type_.value,'pid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDP_IHPID)

    def test_DeleteDatapointMessage_success_load_from_serialization(self):
        ''' DeleteDatapointMessage creation should succeed calling the classmethod load_from_serialization '''
        pid=uuid.uuid4()
        msg='|'.join((messages.DeleteDatapointMessage._type_.value,pid.hex))
        obj=messages.DeleteDatapointMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDatapointMessage_success_load_from_serialization_base_class(self):
        '''  DeleteDatapointMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        pid=uuid.uuid4()
        msg='|'.join((messages.DeleteDatapointMessage._type_.value, pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDatapointMessage_to_serialization_success(self):
        '''DeleteDatapointMessage .to_serialization should succeed '''
        pid=uuid.uuid4()
        msg='|'.join((messages.DeleteDatapointMessage._type_.value, pid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.pid, pid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_WIDGET_MESSAGE)

    def test_DeleteWidgetMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteWidgetMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteWidgetMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELWIDGET_ELFS)

    def test_DeleteWidgetMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteWidgetMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELWIDGET_MINS)

    def test_DeleteWidgetMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteWidgetMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELWIDGET_IST)

    def test_DeleteWidgetMessage_failure_load_from_serialization_invalid_hex_wid(self):
        ''' DeleteWidgetMessage creation should fail if we pass a string with invalid wid '''
        wid=uuid.uuid4()
        msg='|'.join((messages.DeleteWidgetMessage._type_.value,'wid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteWidgetMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELWIDGET_IHWID)

    def test_DeleteWidgetMessage_success_load_from_serialization(self):
        ''' DeleteWidgetMessage creation should succeed calling the classmethod load_from_serialization '''
        wid=uuid.uuid4()
        msg='|'.join((messages.DeleteWidgetMessage._type_.value,wid.hex))
        obj=messages.DeleteWidgetMessage.load_from_serialization(msg)
        self.assertEqual(obj.wid, wid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteWidgetMessage_success_load_from_serialization_base_class(self):
        '''  DeleteWidgetMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        wid=uuid.uuid4()
        msg='|'.join((messages.DeleteWidgetMessage._type_.value, wid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.wid, wid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteWidgetMessage_to_serialization_success(self):
        '''DeleteWidgetMessage .to_serialization should succeed '''
        wid=uuid.uuid4()
        msg='|'.join((messages.DeleteWidgetMessage._type_.value, wid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.wid, wid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_WIDGET_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteWidgetMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.DELETE_DASHBOARD_MESSAGE)

    def test_DeleteDashboardMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DeleteDashboardMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DeleteDashboardMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDashboardMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDASHB_ELFS)

    def test_DeleteDashboardMessage_failure_load_from_serialization_invalid_message(self):
        ''' DeleteDashboardMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDashboardMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDASHB_MINS)

    def test_DeleteDashboardMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DeleteDashboardMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDashboardMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDASHB_IST)

    def test_DeleteDashboardMessage_failure_load_from_serialization_invalid_hex_bid(self):
        ''' DeleteDashboardMessage creation should fail if we pass a string with invalid bid '''
        bid=uuid.uuid4()
        msg='|'.join((messages.DeleteDashboardMessage._type_.value,'bid.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DeleteDashboardMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DELDASHB_IHBID)

    def test_DeleteDashboardMessage_success_load_from_serialization(self):
        ''' DeleteDashboardMessage creation should succeed calling the classmethod load_from_serialization '''
        bid=uuid.uuid4()
        msg='|'.join((messages.DeleteDashboardMessage._type_.value,bid.hex))
        obj=messages.DeleteDashboardMessage.load_from_serialization(msg)
        self.assertEqual(obj.bid, bid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DASHBOARD_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDashboardMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDashboardMessage_success_load_from_serialization_base_class(self):
        '''  DeleteDashboardMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        bid=uuid.uuid4()
        msg='|'.join((messages.DeleteDashboardMessage._type_.value, bid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.bid, bid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DASHBOARD_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDashboardMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DeleteDashboardMessage_to_serialization_success(self):
        '''DeleteDashboardMessage .to_serialization should succeed '''
        bid=uuid.uuid4()
        msg='|'.join((messages.DeleteDashboardMessage._type_.value, bid.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.bid, bid)
        self.assertEqual(obj._type_, messages.Messages.DELETE_DASHBOARD_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DeleteDashboardMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.USER_EVENT_MESSAGE)

    def test_UserEventMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' UserEventMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.UserEventMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_ELFS)

    def test_UserEventMessage_failure_load_from_serialization_invalid_message(self):
        ''' UserEventMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_MINS)

    def test_UserEventMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' UserEventMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IST)

    def test_UserEventMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' UserEventMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        event_type=0
        parameters={}
        msg='|'.join((messages.UserEventMessage._type_.value,'uid.hex',str(event_type),json.dumps(parameters)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IHUID)

    def test_UserEventMessage_failure_load_from_serialization_invalid_str_event_type(self):
        ''' UserEventMessage creation should fail if we pass a string with invalid event_type '''
        uid=uuid.uuid4()
        event_type='event type'
        parameters={}
        msg='|'.join((messages.UserEventMessage._type_.value,uid.hex,str(event_type),json.dumps(parameters)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_ISET)

    def test_UserEventMessage_failure_load_from_serialization_invalid_str_parameters(self):
        ''' UserEventMessage creation should fail if we pass a string with invalid parameters '''
        uid=uuid.uuid4()
        event_type=0
        parameters='parameters invalid json'
        msg='|'.join((messages.UserEventMessage._type_.value,uid.hex,str(event_type),parameters))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREV_IJSPRM)

    def test_UserEventMessage_success_load_from_serialization(self):
        ''' UserEventMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        event_type=0
        parameters={}
        msg='|'.join((messages.UserEventMessage._type_.value,uid.hex,str(event_type),json.dumps(parameters)))
        obj=messages.UserEventMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.event_type, event_type)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UserEventMessage_success_load_from_serialization_base_class(self):
        '''  UserEventMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        event_type=0
        parameters={}
        msg='|'.join((messages.UserEventMessage._type_.value,uid.hex,str(event_type),json.dumps(parameters)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.event_type, event_type)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UserEventMessage_to_serialization_success(self):
        '''UserEventMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        event_type=0
        parameters={}
        msg='|'.join((messages.UserEventMessage._type_.value,uid.hex,str(event_type),json.dumps(parameters)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.event_type, event_type)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.USER_EVENT_RESPONSE_MESSAGE)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' UserEventResponseMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.UserEventResponseMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_ELFS)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_message(self):
        ''' UserEventResponseMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_MINS)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' UserEventResponseMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IST)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' UserEventResponseMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        msg='|'.join((messages.UserEventResponseMessage._type_.value,'uid.hex',date.hex,json.dumps(parameters)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IHUID)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' UserEventResponseMessage creation should fail if we pass a string with invalid date '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        msg='|'.join((messages.UserEventResponseMessage._type_.value,uid.hex,'date.hex',json.dumps(parameters)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IHDATE)

    def test_UserEventResponseMessage_failure_load_from_serialization_invalid_str_parameters(self):
        ''' UserEventResponseMessage creation should fail if we pass a string with invalid parameters '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters='parameters invalid json'
        msg='|'.join((messages.UserEventResponseMessage._type_.value,uid.hex,date.hex,parameters))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_USEREVR_IJSPRM)

    def test_UserEventResponseMessage_success_load_from_serialization(self):
        ''' UserEventResponseMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        msg='|'.join((messages.UserEventResponseMessage._type_.value,uid.hex,date.hex,json.dumps(parameters)))
        obj=messages.UserEventResponseMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_RESPONSE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventResponseMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UserEventResponseMessage_success_load_from_serialization_base_class(self):
        '''  UserEventResponseMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        msg='|'.join((messages.UserEventResponseMessage._type_.value,uid.hex,date.hex,json.dumps(parameters)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_RESPONSE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventResponseMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UserEventResponseMessage_to_serialization_success(self):
        '''UserEventResponseMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        parameters={}
        msg='|'.join((messages.UserEventResponseMessage._type_.value,uid.hex,date.hex,json.dumps(parameters)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid, uid)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj.parameters, parameters)
        self.assertEqual(obj._type_, messages.Messages.USER_EVENT_RESPONSE_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UserEventResponseMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE)

    def test_GenerateTextSummaryMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' GenerateTextSummaryMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_ELFS)

    def test_GenerateTextSummaryMessage_failure_load_from_serialization_invalid_message(self):
        ''' GenerateTextSummaryMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_MINS)

    def test_GenerateTextSummaryMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' GenerateTextSummaryMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_IST)

    def test_GenerateTextSummaryMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' GenerateTextSummaryMessage creation should fail if we pass a string with invalid did '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,'uid.hex',date.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_IHDID)

    def test_GenerateTextSummaryMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' GenerateTextSummaryMessage creation should fail if we pass a string with invalid date '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,did.hex,'date.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_GTXS_IHDATE)

    def test_GenerateTextSummaryMessage_success_load_from_serialization(self):
        ''' GenerateTextSummaryMessage creation should succeed calling the classmethod load_from_serialization '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,did.hex,date.hex))
        obj=messages.GenerateTextSummaryMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateTextSummaryMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_GenerateTextSummaryMessage_success_load_from_serialization_base_class(self):
        '''  GenerateTextSummaryMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj._type_, messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateTextSummaryMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_GenerateTextSummaryMessage_to_serialization_success(self):
        '''GenerateTextSummaryMessage .to_serialization should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.GenerateTextSummaryMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj._type_, messages.Messages.GENERATE_TEXT_SUMMARY_MESSAGE)
        self.assertTrue(isinstance(obj, messages.GenerateTextSummaryMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.MISSING_DATAPOINT_MESSAGE)

    def test_MissingDatapointMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' MissingDatapointMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.MissingDatapointMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_ELFS)

    def test_MissingDatapointMessage_failure_load_from_serialization_invalid_message(self):
        ''' MissingDatapointMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_MINS)

    def test_MissingDatapointMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' MissingDatapointMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_IST)

    def test_MissingDatapointMessage_failure_load_from_serialization_invalid_hex_did(self):
        ''' MissingDatapointMessage creation should fail if we pass a string with invalid did '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MissingDatapointMessage._type_.value,'uid.hex',date.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_IHDID)

    def test_MissingDatapointMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' MissingDatapointMessage creation should fail if we pass a string with invalid date '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MissingDatapointMessage._type_.value,did.hex,'date.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_MISSDP_IHDATE)

    def test_MissingDatapointMessage_success_load_from_serialization(self):
        ''' MissingDatapointMessage creation should succeed calling the classmethod load_from_serialization '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MissingDatapointMessage._type_.value,did.hex,date.hex))
        obj=messages.MissingDatapointMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date, date)
        self.assertEqual(obj._type_, messages.Messages.MISSING_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MissingDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MissingDatapointMessage_success_load_from_serialization_base_class(self):
        '''  MissingDatapointMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MissingDatapointMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj._type_, messages.Messages.MISSING_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MissingDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_MissingDatapointMessage_to_serialization_success(self):
        '''MissingDatapointMessage .to_serialization should succeed '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        msg='|'.join((messages.MissingDatapointMessage._type_.value,did.hex,date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.did, did)
        self.assertEqual(obj.date,date)
        self.assertEqual(obj._type_, messages.Messages.MISSING_DATAPOINT_MESSAGE)
        self.assertTrue(isinstance(obj, messages.MissingDatapointMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

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
        self.assertEqual(msg._type_, messages.Messages.NEW_INV_MAIL_MESSAGE)

    def test_NewInvitationMailMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' NewInvitationMailMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.NewInvitationMailMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewInvitationMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_ELFS)

    def test_NewInvitationMailMessage_failure_load_from_serialization_invalid_message(self):
        ''' NewInvitationMailMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewInvitationMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_MINS)

    def test_NewInvitationMailMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' NewInvitationMailMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewInvitationMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_IST)

    def test_NewInvitationMailMessage_failure_load_from_serialization_invalid_hex_inv_id(self):
        ''' NewInvitationMailMessage creation should fail if we pass a string with invalid inv_id '''
        inv_id=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.NewInvitationMailMessage._type_.value,email,'inv_id.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.NewInvitationMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_NEWINV_IHINV)

    def test_NewInvitationMailMessage_success_load_from_serialization(self):
        ''' NewInvitationMailMessage creation should succeed calling the classmethod load_from_serialization '''
        inv_id=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.NewInvitationMailMessage._type_.value,email,inv_id.hex))
        obj=messages.NewInvitationMailMessage.load_from_serialization(msg)
        self.assertEqual(obj.inv_id, inv_id)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.NEW_INV_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewInvitationMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewInvitationMailMessage_success_load_from_serialization_base_class(self):
        '''  NewInvitationMailMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        inv_id=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.NewInvitationMailMessage._type_.value,email,inv_id.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.inv_id, inv_id)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.NEW_INV_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewInvitationMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_NewInvitationMailMessage_to_serialization_success(self):
        '''NewInvitationMailMessage .to_serialization should succeed '''
        inv_id=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.NewInvitationMailMessage._type_.value,email,inv_id.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.inv_id, inv_id)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.NEW_INV_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.NewInvitationMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

    def test_ForgetMailMessage_failure_invalid_email(self):
        ''' ForgetMailMessage creation should fail if email is invalid '''
        emails=[None, -23423, 2323.2342, 'User/name',{'a','dict'},['a','list'],('a','tuple'),'userñame',json.dumps('username'), 'user\nname','user\tname', timeuuid.uuid1(),'CAPITAL@email.com','adfañdasdf@email.com','email@eamil@email','email@domain','email@email@domain.com','.@.com','email@.com']
        code=uuid.uuid4()
        for email in emails:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ForgetMailMessage(email=email,code=code)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_IEMAIL)

    def test_ForgetMailMessage_failure_invalid_code(self):
        ''' ForgetMailMessage creation should fail if code is invalid '''
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
        self.assertEqual(msg._type_, messages.Messages.FORGET_MAIL_MESSAGE)

    def test_ForgetMailMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' ForgetMailMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.ForgetMailMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ForgetMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_ELFS)

    def test_ForgetMailMessage_failure_load_from_serialization_invalid_message(self):
        ''' ForgetMailMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ForgetMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_MINS)

    def test_ForgetMailMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' ForgetMailMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ForgetMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_IST)

    def test_ForgetMailMessage_failure_load_from_serialization_invalid_hex_code(self):
        ''' ForgetMailMessage creation should fail if we pass a string with invalid  code '''
        code=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.ForgetMailMessage._type_.value,email,'code.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ForgetMailMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_FORGET_IHCODE)

    def test_ForgetMailMessage_success_load_from_serialization(self):
        ''' ForgetMailMessage creation should succeed calling the classmethod load_from_serialization '''
        code=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.ForgetMailMessage._type_.value,email,code.hex))
        obj=messages.ForgetMailMessage.load_from_serialization(msg)
        self.assertEqual(obj.code,code)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.FORGET_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ForgetMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ForgetMailMessage_success_load_from_serialization_base_class(self):
        '''  ForgetMailMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        code=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.ForgetMailMessage._type_.value,email,code.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.code,code)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.FORGET_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ForgetMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ForgetMailMessage_to_serialization_success(self):
        '''ForgetMailMessage .to_serialization should succeed '''
        code=uuid.uuid4()
        email='test@komlog.org'
        msg='|'.join((messages.ForgetMailMessage._type_.value,email,code.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.code,code)
        self.assertEqual(obj.email, email)
        self.assertEqual(obj._type_, messages.Messages.FORGET_MAIL_MESSAGE)
        self.assertTrue(isinstance(obj, messages.ForgetMailMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(),msg)

    def test_UrisUpdatedMessage_failure_invalid_date(self):
        ''' UrisUpdatedMessage creation should fail if date is invalid '''
        dates=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid4(), json.dumps('username'), 'user\nname','user\tname']
        uris=[{'uri':'uri','type':'type','id':uuid.uuid4()}]
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.UrisUpdatedMessage(uris=uris, date=date)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IDT)

    def test_UrisUpdatedMessage_failure_invalid_uris_not_a_list(self):
        ''' UrisUpdatedMessage creation should fail if uris is not a list '''
        date=timeuuid.uuid1()
        uris={'uri':'uri','type':'ds','id':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_not_a_dict(self):
        ''' UrisUpdatedMessage creation should fail if uris is not a list '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            'something',
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_has_no_uri(self):
        ''' UrisUpdatedMessage creation should fail if uris item has no uri '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'type':'ds','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_has_no_type(self):
        ''' UrisUpdatedMessage creation should fail if uris item has no type '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_has_no_id(self):
        ''' UrisUpdatedMessage creation should fail if uris item has no id '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_invalid_uri(self):
        ''' UrisUpdatedMessage creation should fail if uris item has invalid uri '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'invalid uri','type':'ds','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_failure_invalid_uris_item_invalid_id(self):
        ''' UrisUpdatedMessage creation should fail if uris item has invalid id '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','type':'ds','id':'werwer'},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IURIS)

    def test_UrisUpdatedMessage_success(self):
        ''' UrisUpdatedMessage creation should fail if uris item has invalid id '''
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
        ]
        msg=messages.UrisUpdatedMessage(uris=uris, date=date)
        self.assertEqual(msg.date, date)
        self.assertEqual(msg.uris, uris)
        self.assertEqual(msg._type_, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertTrue(isinstance(msg, messages.UrisUpdatedMessage))

    def test_UrisUpdatedMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' UrisUpdatedMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_ELFS)

    def test_UrisUpdatedMessage_failure_load_from_serialization_invalid_message(self):
        ''' UrisUpdatedMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_MINS)

    def test_UrisUpdatedMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' UrisUpdatedMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IST)

    def test_UrisUpdatedMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' UrisUpdatedMessage creation should fail if we pass a string with invalid date '''
        date=uuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
        ]
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,json.dumps(uris),'date.hex'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IHDATE)

    def test_UrisUpdatedMessage_failure_load_from_serialization_invalid_json_uris(self):
        ''' UrisUpdatedMessage creation should fail if we pass a string with invalid uris '''
        date=uuid.uuid1()
        uris='uris json'
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,uris,date.hex))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_URUP_IJSURIS)

    def test_UrisUpdatedMessage_success_load_from_serialization(self):
        ''' UrisUpdatedMessage creation should succeed calling the classmethod load_from_serialization '''
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,json.dumps(uris),date.hex))
        obj=messages.UrisUpdatedMessage.load_from_serialization(msg)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UrisUpdatedMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UrisUpdatedMessage_success_load_from_serialization_base_class(self):
        '''  UrisUpdatedMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,json.dumps(uris),date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UrisUpdatedMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_UrisUpdatedMessage_to_serialization_success(self):
        '''UrisUpdatedMessage .to_serialization should succeed '''
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.UrisUpdatedMessage._type_.value,json.dumps(uris),date.hex))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertTrue(isinstance(obj, messages.UrisUpdatedMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2=obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj.date, obj2.date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj2.uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.URIS_UPDATED_MESSAGE)
        self.assertTrue(isinstance(obj2, messages.UrisUpdatedMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

    def test_SendSessionDataMessage_failure_invalid_sid(self):
        ''' SendSessionDataMessage creation should fail if sid is invalid '''
        sids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        data=[{'uri':'uri','content':'content'}]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.SendSessionDataMessage(sid=sid,data=data)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_ISID)

    def test_SendSessionDataMessage_success(self):
        ''' SendSessionDataMessage creation should succeed '''
        data=[{'uri':'uri','content':'content'}]
        sid=uuid.uuid4()
        msg=messages.SendSessionDataMessage(sid=sid, data=data)
        self.assertTrue(isinstance(msg, messages.SendSessionDataMessage))
        self.assertEqual(msg._type_, messages.Messages.SEND_SESSION_DATA_MESSAGE)

    def test_SendSessionDataMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' SendSessionDataMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.SendSessionDataMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_ELFS)

    def test_SendSessionDataMessage_failure_load_from_serialization_invalid_message(self):
        ''' SendSessionDataMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_MINS)

    def test_SendSessionDataMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' SendSessionDataMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_IST)

    def test_SendSessionDataMessage_failure_load_from_serialization_invalid_hex_sid(self):
        ''' SendSessionDataMessage creation should fail if we pass a string with invalid sid '''
        sid=uuid.uuid4()
        data=[
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
        ]
        msg='|'.join((messages.SendSessionDataMessage._type_.value,'sid.hex',json.dumps(data)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_IHSID)

    def test_SendSessionDataMessage_failure_load_from_serialization_invalid_json_data(self):
        ''' SendSessionDataMessage creation should fail if we pass a string with invalid data '''
        sid=uuid.uuid4()
        data='non json data'
        msg='|'.join((messages.SendSessionDataMessage._type_.value,sid.hex,data))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_SSDT_IJSDATA)

    def test_SendSessionDataMessage_success_load_from_serialization(self):
        ''' SendSessionDataMessage creation should succeed calling the classmethod load_from_serialization '''
        sid=uuid.uuid4()
        data='some data'
        msg='|'.join((messages.SendSessionDataMessage._type_.value,sid.hex,json.dumps(data)))
        obj=messages.SendSessionDataMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj.data, data)
        self.assertEqual(obj._type_, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(isinstance(obj, messages.SendSessionDataMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_SendSessionDataMessage_success_load_from_serialization_base_class(self):
        '''  SendSessionDataMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        sid=uuid.uuid4()
        data='some data'
        msg='|'.join((messages.SendSessionDataMessage._type_.value,sid.hex,json.dumps(data)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj.data, data)
        self.assertEqual(obj._type_, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(isinstance(obj, messages.SendSessionDataMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_SendSessionDataMessage_to_serialization_success(self):
        '''SendSessionDataMessage .to_serialization should succeed '''
        sid=uuid.uuid4()
        data='some data'
        msg='|'.join((messages.SendSessionDataMessage._type_.value,sid.hex,json.dumps(data)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj.data, data)
        self.assertEqual(obj._type_, messages.Messages.SEND_SESSION_DATA_MESSAGE)
        self.assertTrue(isinstance(obj, messages.SendSessionDataMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        self.assertEqual(obj.to_serialization(), msg)

    def test_ClearSessionHooksMessage_failure_invalid_sid(self):
        ''' ClearSessionHooksMessage creation should fail if sid is invalid '''
        sids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        ids=[(uuid.uuid4(), 'd'),(uuid.uuid4(),'p')]
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.ClearSessionHooksMessage(sid=sid,ids=ids)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_ISID)

    def test_ClearSessionHooksMessage_failure_invalid_ids_not_a_list(self):
        ''' ClearSessionHooksMessage creation should fail if ids is not a list '''
        sid=uuid.uuid4()
        ids={(uuid.uuid4(), 'd'),(uuid.uuid4(),'p')}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IIDS)

    def test_ClearSessionHooksMessage_failure_invalid_ids_item_not_list_or_tuple(self):
        ''' ClearSessionHooksMessage creation should fail if ids item is not a list or tuple '''
        sid=uuid.uuid4()
        ids=[
            (uuid.uuid4(), 'd'),
            [uuid.uuid4(),'p'],
            {'a','set'},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IIDS)

    def test_ClearSessionHooksMessage_failure_invalid_ids_item_length_not_two(self):
        ''' ClearSessionHooksMessage creation should fail if ids item has not got two elements '''
        sid=uuid.uuid4()
        ids=[
            (uuid.uuid4(), 'd'),
            [uuid.uuid4(),'p'],
            [uuid.uuid4(),'p','something'],
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IIDS)

    def test_ClearSessionHooksMessage_failure_invalid_ids_item_first_elem_not_uuid(self):
        ''' ClearSessionHooksMessage creation should fail if ids item first elem is not uuid '''
        sid=uuid.uuid4()
        ids=[
            (uuid.uuid4(), 'd'),
            [uuid.uuid4().hex,'p'],
            ['something','p'],
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IIDS)

    def test_ClearSessionHooksMessage_failure_invalid_ids_item_second_elem_not_str(self):
        ''' ClearSessionHooksMessage creation should fail if ids item second elem is not str '''
        sid=uuid.uuid4()
        ids=[
            (uuid.uuid4(), 'd'),
            [uuid.uuid4().hex,'p'],
            [uuid.uuid4(), uuid.uuid4()],
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IIDS)

    def test_ClearSessionHooksMessage_success(self):
        ''' ClearSessionHooksMessage creation should succeed '''
        sid=uuid.uuid4()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        ids=[
            (id1, 'd'),
            [id2.hex,'p'],
        ]
        obj_ids=[
            (id1,'d'),
            (id2,'p'),
        ]
        msg=messages.ClearSessionHooksMessage(sid=sid,ids=ids)
        self.assertEqual(msg._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(msg.sid, sid)
        self.assertEqual(sorted(msg.ids, key=lambda x:x[0]),sorted(obj_ids, key=lambda x:x[0]))
        self.assertTrue(isinstance(msg, messages.ClearSessionHooksMessage))

    def test_ClearSessionHooksMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' ClearSessionHooksMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_ELFS)

    def test_ClearSessionHooksMessage_failure_load_from_serialization_invalid_message(self):
        ''' ClearSessionHooksMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_MINS)

    def test_ClearSessionHooksMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' ClearSessionHooksMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IST)

    def test_ClearSessionHooksMessage_failure_load_from_serialization_invalid_hex_sid(self):
        ''' ClearSessionHooksMessage creation should fail if we pass a string with invalid sid '''
        sid=uuid.uuid4()
        ids=[
            [uuid.uuid4().hex, 'd'],
            [uuid.uuid4().hex,'p'],
        ]
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,'sid.hex',json.dumps(ids)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IHSID)

    def test_ClearSessionHooksMessage_failure_load_from_serialization_invalid_json_ids(self):
        ''' ClearSessionHooksMessage creation should fail if we pass a string with invalid data '''
        sid=uuid.uuid4()
        ids='non json data'
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,sid.hex,ids))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_CSH_IJSIDS)

    def test_ClearSessionHooksMessage_success_load_from_serialization(self):
        ''' ClearSessionHooksMessage creation should succeed calling the classmethod load_from_serialization '''
        sid=uuid.uuid4()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        ids=[
            (id1.hex, 'd'),
            [id2.hex,'p'],
        ]
        obj_ids=[
            (id1,'d'),
            (id2,'p'),
        ]
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,sid.hex,json.dumps(ids)))
        obj=messages.ClearSessionHooksMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(obj.ids, key=lambda x:x[0]),sorted(obj_ids, key=lambda x:x[0]))
        self.assertTrue(isinstance(obj, messages.ClearSessionHooksMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ClearSessionHooksMessage_success_load_from_serialization_base_class(self):
        '''  ClearSessionHooksMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        sid=uuid.uuid4()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        ids=[
            (id1.hex, 'd'),
            [id2.hex,'p'],
        ]
        obj_ids=[
            (id1,'d'),
            (id2,'p'),
        ]
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,sid.hex,json.dumps(ids)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(obj.ids, key=lambda x:x[0]),sorted(obj_ids, key=lambda x:x[0]))
        self.assertTrue(isinstance(obj, messages.ClearSessionHooksMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_ClearSessionHooksMessage_to_serialization_success(self):
        '''ClearSessionHooksMessage .to_serialization should succeed '''
        sid=uuid.uuid4()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        ids=[
            (id1.hex, 'd'),
            [id2.hex,'p'],
        ]
        obj_ids=[
            (id1,'d'),
            (id2,'p'),
        ]
        msg='|'.join((messages.ClearSessionHooksMessage._type_.value,sid.hex,json.dumps(ids)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid, sid)
        self.assertEqual(obj._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(obj.ids, key=lambda x:x[0]),sorted(obj_ids, key=lambda x:x[0]))
        self.assertTrue(isinstance(obj, messages.ClearSessionHooksMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2=obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj2.sid, sid)
        self.assertEqual(obj2._type_, messages.Messages.CLEAR_SESSION_HOOKS_MESSAGE)
        self.assertEqual(sorted(obj.ids, key=lambda x:x[0]),sorted(obj2.ids, key=lambda x:x[0]))
        self.assertTrue(isinstance(obj2, messages.ClearSessionHooksMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

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

    def test_HookNewUrisMessage_failure_invalid_uris_not_a_list(self):
        ''' HookNewUrisMessage creation should fail if uris is not a list '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris={'uri':'uri','type':'ds','id':uuid.uuid4()}
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_not_a_dict(self):
        ''' HookNewUrisMessage creation should fail if uris is not a list '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            'something',
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_has_no_uri(self):
        ''' HookNewUrisMessage creation should fail if uris item has no uri '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'type':'ds','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_has_no_type(self):
        ''' HookNewUrisMessage creation should fail if uris item has no type '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_has_no_id(self):
        ''' HookNewUrisMessage creation should fail if uris item has no id '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_invalid_uri(self):
        ''' HookNewUrisMessage creation should fail if uris item has invalid uri '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'invalid uri','type':'ds','id':uuid.uuid4()},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_failure_invalid_uris_item_invalid_id(self):
        ''' HookNewUrisMessage creation should fail if uris item has invalid id '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','type':'ds','id':'werwer'},
        ]
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IURIS)

    def test_HookNewUrisMessage_success(self):
        ''' HookNewUrisMessage creation should fail if uris item has invalid id '''
        uid=uuid.uuid4()
        date=timeuuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
            {'uri':'uri','type':'ds','id':uuid.uuid4()},
        ]
        msg=messages.HookNewUrisMessage(uid=uid, uris=uris, date=date)
        self.assertEqual(msg.date, date)
        self.assertEqual(msg.uris, uris)
        self.assertEqual(msg._type_, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertTrue(isinstance(msg, messages.HookNewUrisMessage))

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' HookNewUrisMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.HookNewUrisMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_ELFS)

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_message(self):
        ''' HookNewUrisMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_MINS)

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' HookNewUrisMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IST)

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_hex_uid(self):
        ''' HookNewUrisMessage creation should fail if we pass a string with invalid uid '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
        ]
        msg='|'.join((messages.HookNewUrisMessage._type_.value,'uid.hex',date.hex,json.dumps(uris)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IHUID)

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_hex_date(self):
        ''' HookNewUrisMessage creation should fail if we pass a string with invalid date '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        uris=[
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
            {'uri':'uri','type':'ds','id':uuid.uuid4().hex},
        ]
        msg='|'.join((messages.HookNewUrisMessage._type_.value,uid.hex,'date.hex',json.dumps(uris)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IHDATE)

    def test_HookNewUrisMessage_failure_load_from_serialization_invalid_json_uris(self):
        ''' HookNewUrisMessage creation should fail if we pass a string with invalid uris '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        uris='uris json'
        msg='|'.join((messages.HookNewUrisMessage._type_.value,uid.hex,date.hex,uris))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_HNU_IJSURIS)

    def test_HookNewUrisMessage_success_load_from_serialization(self):
        ''' HookNewUrisMessage creation should succeed calling the classmethod load_from_serialization '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.HookNewUrisMessage._type_.value,uid.hex,date.hex,json.dumps(uris)))
        obj=messages.HookNewUrisMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid,uid)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.HookNewUrisMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_HookNewUrisMessage_success_load_from_serialization_base_class(self):
        '''  HookNewUrisMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.HookNewUrisMessage._type_.value,uid.hex,date.hex,json.dumps(uris)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid,uid)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.HookNewUrisMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_HookNewUrisMessage_to_serialization_success(self):
        '''HookNewUrisMessage .to_serialization should succeed '''
        uid=uuid.uuid4()
        date=uuid.uuid1()
        id1=uuid.uuid4()
        id2=uuid.uuid4()
        uris=[
            {'uri':'uri','type':'ds','id':id1.hex},
            {'uri':'uri','type':'ds','id':id2.hex},
        ]
        obj_uris=[
            {'uri':'uri','type':'ds','id':id1},
            {'uri':'uri','type':'ds','id':id2},
        ]
        msg='|'.join((messages.HookNewUrisMessage._type_.value,uid.hex,date.hex,json.dumps(uris)))
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.uid,uid)
        self.assertEqual(obj.date,date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj_uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertTrue(isinstance(obj, messages.HookNewUrisMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2=obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj.uid, obj2.uid)
        self.assertEqual(obj.date, obj2.date)
        self.assertEqual(sorted(obj.uris, key=lambda x: x['id'].hex), sorted(obj2.uris, key=lambda x: x['id'].hex))
        self.assertEqual(obj._type_, messages.Messages.HOOK_NEW_URIS_MESSAGE)
        self.assertTrue(isinstance(obj2, messages.HookNewUrisMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

    def test_DataIntervalRequestMessage_failure_invalid_sid(self):
        ''' DataIntervalRequestMessage creation should fail if sid is invalid '''
        sids=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4().hex, uuid.uuid1(), json.dumps('username'), 'user\nname','user\tname']
        uri={'uri':'valid.uri','type':'type','id':uuid.uuid4()}
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_ISID)

    def test_DataIntervalRequestMessage_failure_invalid_ii(self):
        ''' DataIntervalRequestMessage creation should fail if ii is invalid '''
        iis=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), uuid.uuid1().hex, json.dumps('username'), 'user\nname','user\tname']
        uri={'uri':'valid.uri','type':'type','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ie=timeuuid.uuid1()
        for ii in iis:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_III)

    def test_DataIntervalRequestMessage_failure_invalid_ie(self):
        ''' DataIntervalRequestMessage creation should fail if ie is invalid '''
        ies=[None, 23423, 2323.2342, 'Username',{'a','dict'},['a','list'],('a','tuple'),'userñame',uuid.uuid4(), uuid.uuid1().hex, json.dumps('username'), 'user\nname','user\tname']
        uri={'uri':'valid.uri','type':'type','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        for ie in ies:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
            self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IIE)

    def test_DataIntervalRequestMessage_failure_invalid_uri_not_a_dict(self):
        ''' DataIntervalRequestMessage creation should fail if uri is not a dict '''
        uri='uri'
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_failure_invalid_uri_has_no_uri(self):
        ''' DataIntervalRequestMessage creation should fail if uri has no uri '''
        uri={'type':'type','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_failure_invalid_uri_has_no_type(self):
        ''' DataIntervalRequestMessage creation should fail if uri has no type '''
        uri={'uri':'uri','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_failure_invalid_uri_has_no_id(self):
        ''' DataIntervalRequestMessage creation should fail if uri has no id '''
        uri={'uri':'uri','type':'type','did':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_failure_invalid_uri_has_invalid_uri(self):
        ''' DataIntervalRequestMessage creation should fail if uri has invalid uri '''
        uri={'uri':'invalid uri','type':'type','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_failure_invalid_uri_has_invalid_id(self):
        ''' DataIntervalRequestMessage creation should fail if uri has invalid id '''
        uri={'uri':'invalid uri','type':'type','id':'id'}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IURI)

    def test_DataIntervalRequestMessage_success_uri_id_is_uuid(self):
        ''' DataIntervalRequestMessage creation should succeed if uri id is an uuid object '''
        uri={'uri':'valid.uri','type':'type','id':uuid.uuid4()}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        msg=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertTrue(isinstance(msg, messages.DataIntervalRequestMessage))
        self.assertEqual(msg.sid, sid)
        self.assertEqual(msg.ii, ii)
        self.assertEqual(msg.ie, ie)
        self.assertEqual(msg.uri, uri)
        self.assertEqual(msg._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)

    def test_DataIntervalRequestMessage_success_uri_id_is_hex_uuid(self):
        ''' DataIntervalRequestMessage creation should succeed if uri id is an hex uuid object '''
        uri={'uri':'valid.uri','type':'type','id':uuid.uuid4().hex}
        obj_uri={'uri':'valid.uri','type':'type','id':uuid.UUID(uri['id'])}
        sid=uuid.uuid4()
        ii=timeuuid.uuid1()
        ie=timeuuid.uuid1()
        msg=messages.DataIntervalRequestMessage(sid=sid, uri=uri, ii=ii, ie=ie)
        self.assertTrue(isinstance(msg, messages.DataIntervalRequestMessage))
        self.assertEqual(msg._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertEqual(msg.sid, sid)
        self.assertEqual(msg.ii, ii)
        self.assertEqual(msg.ie, ie)
        self.assertEqual(msg.uri, obj_uri)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_field_number(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string without the exact number of fields '''
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_ELFS)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_message(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a non string message '''
        msg=['not a string']
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_MINS)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_serialization_type(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string with not the expected type '''
        msg='|'.join(('WHATEVER','1','2','3','4'))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IST)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_hex_sid(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string with invalid sid '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        uri={'uri':'uri','type':'ds','id':uuid.uuid4().hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,'sid.hex',ii.hex,ie.hex,json.dumps(uri)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IHSID)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_hex_ii(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string with invalid ii '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        uri={'uri':'uri','type':'ds','id':uuid.uuid4().hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,'ii.hex',ie.hex,json.dumps(uri)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IHII)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_hex_ie(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string with invalid ie '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        uri={'uri':'uri','type':'ds','id':uuid.uuid4().hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,ii.hex,'ie.hex',json.dumps(uri)))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IHIE)

    def test_DataIntervalRequestMessage_failure_load_from_serialization_invalid_json_uri(self):
        ''' DataIntervalRequestMessage creation should fail if we pass a string with invalid uri '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        uri="{'uri':'uri','type':'ds','id':uuid.uuid4().hex}"
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,ii.hex,ie.hex,uri))
        with self.assertRaises(exceptions.BadParametersException) as cm:
            messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(cm.exception.error, Errors.E_IIMM_DIRM_IJSURI)

    def test_DataIntervalRequestMessage_success_load_from_serialization(self):
        ''' DataIntervalRequestMessage creation should succeed calling the classmethod load_from_serialization '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        id1=uuid.uuid4()
        uri={'uri':'uri','type':'ds','id':id1.hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,ii.hex,ie.hex,json.dumps(uri)))
        obj_uri={'uri':'uri','type':'ds','id':id1}
        obj=messages.DataIntervalRequestMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid,sid)
        self.assertEqual(obj.ii,ii)
        self.assertEqual(obj.ie,ie)
        self.assertEqual(obj.uri,obj_uri)
        self.assertEqual(obj._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DataIntervalRequestMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DataIntervalRequestMessage_success_load_from_serialization_base_class(self):
        '''  DataIntervalRequestMessage creation should succeed calling the classmethod load_from_serialization from the base class '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        id1=uuid.uuid4()
        uri={'uri':'uri','type':'ds','id':id1.hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,ii.hex,ie.hex,json.dumps(uri)))
        obj_uri={'uri':'uri','type':'ds','id':id1}
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid,sid)
        self.assertEqual(obj.ii,ii)
        self.assertEqual(obj.ie,ie)
        self.assertEqual(obj.uri,obj_uri)
        self.assertEqual(obj._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DataIntervalRequestMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))

    def test_DataIntervalRequestMessage_to_serialization_success(self):
        '''DataIntervalRequestMessage .to_serialization should succeed '''
        sid=uuid.uuid4()
        ii=uuid.uuid1()
        ie=uuid.uuid1()
        id1=uuid.uuid4()
        uri={'uri':'uri','type':'ds','id':id1.hex}
        msg='|'.join((messages.DataIntervalRequestMessage._type_.value,sid.hex,ii.hex,ie.hex,json.dumps(uri)))
        obj_uri={'uri':'uri','type':'ds','id':id1}
        obj=messages.IMCMessage.load_from_serialization(msg)
        self.assertEqual(obj.sid,sid)
        self.assertEqual(obj.ii,ii)
        self.assertEqual(obj.ie,ie)
        self.assertEqual(obj.uri,obj_uri)
        self.assertEqual(obj._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(isinstance(obj, messages.DataIntervalRequestMessage))
        self.assertTrue(isinstance(obj, messages.IMCMessage))
        msg2=obj.to_serialization()
        obj2=messages.IMCMessage.load_from_serialization(msg2)
        self.assertEqual(obj2.sid,sid)
        self.assertEqual(obj2.ii,ii)
        self.assertEqual(obj2.ie,ie)
        self.assertEqual(obj2.uri,obj_uri)
        self.assertEqual(obj._type_, messages.Messages.DATA_INTERVAL_REQUEST_MESSAGE)
        self.assertTrue(isinstance(obj2, messages.DataIntervalRequestMessage))
        self.assertTrue(isinstance(obj2, messages.IMCMessage))

