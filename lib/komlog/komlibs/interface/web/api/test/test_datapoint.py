import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlog.komcass.api import interface as cassapiiface
from komlog.komlibs.auth.model import interfaces
from komlog.komlibs.auth.model.operations import Operations
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlog.komlibs.gestaccount.datapoint import api as gestdatapointapi
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.interface.web.api import login as loginapi 
from komlog.komlibs.interface.web.api import user as userapi 
from komlog.komlibs.interface.web.api import agent as agentapi 
from komlog.komlibs.interface.web.api import datasource as datasourceapi 
from komlog.komlibs.interface.web.api import datapoint as datapointapi 
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komfig import logging


pubkey = b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')

class InterfaceWebApiDatapointTest(unittest.TestCase):
    ''' komlibs.interface.web.api.datapoint tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.datapoint_user'
        self.password = 'password'
        agentname='test_komlibs.interface.web.api.datapoint_agent'
        version='test library vX.XX'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.unrouted_messages:
                msgresponse=msgapi.process_message(msg)
            response = loginapi.login_request(username=self.username, password=self.password)
            cookie=getattr(response, 'cookie',None)
            self.passport = passport.get_user_passport(cookie)
            response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
            aid = response.data['aid']
            cookie = {'user':self.username, 'sid':uuid.uuid4().hex, 'aid':aid, 'seq':timeuuid.get_custom_sequence(timeuuid.uuid1())}
            self.agent_passport = passport.get_agent_passport(cookie)
            for msg in response.unrouted_messages:
                msgresponse=msgapi.process_message(msg)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
            datasourcename='datasource'
            response = datasourceapi.new_datasource_request(passport=self.agent_passport, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msgs=response.unrouted_messages
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.unrouted_messages:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport = passport.get_user_passport(cookie)
        response = agentapi.get_agents_config_request(passport=self.passport)
        self.agents = response.data
        did=self.agents[0]['dids'][0]
        content='DATAPOINT TESTS CONTENT 0 1 2 3 4 5 6 7 8 9 10 11 12'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))

    def test_new_datasource_datapoint_request_success(self):
        ''' new_datasource_datapoint_request should succeed if parameters exists, and user has permission '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_new_datasource_datapoint_request_success'
        datasource_config=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(datasource_config.status, status.WEB_STATUS_OK)
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        amsg=None
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.MON_VAR_MESSAGE and msg.did==uuid.UUID(did):
                amsg=msg
                break
        datapoint=gestdatapointapi.monitor_new_datapoint(did=amsg.did, date=amsg.date, position=amsg.position, length=amsg.length, datapointname=amsg.datapointname)
        self.assertIsNotNone(datapoint)
        self.assertEqual(datapoint['datapointname'],'.'.join((datasource_config.data['datasourcename'],datapointname)))
        self.assertEqual(datapoint['did'],uuid.UUID(did))

    def test_new_datasource_datapoint_request_failure_invalid_passport(self):
        ''' new_datasource_datapoint_request should fail if username is invalid '''
        passports=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=uuid.uuid4().hex
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence='23423234565432345678'
        variable=(0,1)
        for psp in passports:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_invalid_did(self):
        ''' new_datasource_datapoint_request should fail if did is invalid '''
        psp = self.passport
        dids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence='23423234565432345678'
        variable=(0,1)
        for did in dids:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_invalid_datapointname(self):
        ''' new_datasource_datapoint_request should fail if datapointname is invalid '''
        datapointnames=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'user\tName','user name\n','userñame',json.dumps('username')]
        did=uuid.uuid4().hex
        psp = self.passport
        sequence='23423234565432345678'
        variable=(0,1)
        for datapointname in datapointnames:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_invalid_sequence(self):
        ''' new_datasource_datapoint_request should fail if sequence is invalid '''
        psp = self.passport
        sequences=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4(),'abcde1234567890ABCDF1','abcde1234567890ABCD']
        did=uuid.uuid4().hex
        datapointname='test_new_datasource_datapoint_request_failure'
        variable=(0,1)
        for sequence in sequences:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_invalid_position(self):
        ''' new_datasource_datapoint_request should fail if position is invalid '''
        psp = self.passport
        positions=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=uuid.uuid4().hex
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_invalid_length(self):
        ''' new_datasource_datapoint_request should fail if length is invalid '''
        psp = self.passport
        lengths=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=uuid.uuid4().hex
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datasource_datapoint_request_failure_user_does_not_exist(self):
        ''' new_datasource_datapoint_request should fail if user does not exist '''
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        did=self.agents[0]['dids'][0]
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence=uuid.uuid1().hex
        position=1
        length=1
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ANDSDP_RE.value)

    def test_new_datasource_datapoint_request_failure_no_permission_did_does_not_exist(self):
        ''' new_datasource_datapoint_request should fail if did does not exist '''
        psp = self.passport
        did=uuid.uuid4().hex
        datapointname='test_new_datasource_datapoint_request_failure'
        sequence=uuid.uuid1().hex
        position=1
        length=1
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_AQA_ANDSDP_DSNF.value)

    def test_update_datapoint_config_request_failure_invalid_passport(self):
        ''' update_datapoint_config_request should fail if username is invalid '''
        passports=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        for psp in passports:
            response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_invalid_data(self):
        ''' update_datapoint_config_request should fail if data is invalid '''
        datas=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        pid=uuid.uuid4().hex
        for data in datas:
            response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_invalid_pid(self):
        ''' update_datapoint_config_request should fail if pid is invalid '''
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        data={'datapointname':'datapointname','color':'#FFAADD'}
        for pid in pids:
            response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_non_existent_pid(self):
        ''' update_datapoint_config_request should fail if pid does not exist '''
        psp = self.passport
        pid=uuid.uuid4().hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDPC_RE.value)

    def test_update_datapoint_config_request_failure_non_existent_username(self):
        ''' update_datapoint_config_request should fail if user does not exist '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_update_datapoint_config_request_failure_non_existent_username'
        datasource_config=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(datasource_config.status, status.WEB_STATUS_OK)
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][1]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        amsg=None
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.MON_VAR_MESSAGE and msg.did==uuid.UUID(did):
                amsg=msg
                break
        datapoint=gestdatapointapi.monitor_new_datapoint(did=amsg.did, date=amsg.date, position=amsg.position, length=amsg.length, datapointname=amsg.datapointname)
        self.assertIsNotNone(datapoint)
        self.assertEqual(datapoint['datapointname'],'.'.join((datasource_config.data['datasourcename'],datapointname)))
        self.assertEqual(datapoint['did'],uuid.UUID(did))
        psp = passport.Passport(uid=uuid.uuid4(), sid=uuid.uuid4())
        pid=datapoint['pid'].hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_APDPC_RE.value)

    def test_update_datapoint_config_request_success_new_datapointname(self):
        ''' update_datapoint_config_request should succeed, updating datapointname only '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_datapointname'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][2]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        new_datapointname='test_update_datapoint_config_request_success_new_datapointname2'
        data={'datapointname':new_datapointname}
        response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapointinfo.data['color'],datapointinfo2.data['color'])
        self.assertEqual(new_datapointname,datapointinfo2.data['datapointname'])

    def test_update_datapoint_config_request_success_new_color(self):
        ''' update_datapoint_config_request should succeed, updating color only '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_color'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][3]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        new_color='#AA00EE'
        data={'color':new_color}
        response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(new_color,datapointinfo2.data['color'])
        self.assertEqual(datapointinfo.data['datapointname'],datapointinfo2.data['datapointname'])

    def test_update_datapoint_config_request_success_new_color_and_datapointname(self):
        ''' update_datapoint_config_request should succeed, updating datapointname and color '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_color_and_datapointname'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][4]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        new_color='#AA00EE'
        new_datapointname='test_update_datapoint_config_request_success_new_color_and_datapointname'
        data={'color':new_color, 'datapointname':new_datapointname}
        response=datapointapi.update_datapoint_config_request(passport=psp, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(new_color,datapointinfo2.data['color'])
        self.assertEqual(new_datapointname,datapointinfo2.data['datapointname'])

    def test_get_datapoint_config_request_success(self):
        ''' get_datapoint_config_request should succeed, returning datapoint info '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_get_datapoint_config_request_success'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][5]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourcedata.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        response=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourcedata.data['did'], response.data['did'])
        self.assertEqual(pid, response.data['pid'])
        self.assertTrue('datapointname' in response.data)
        self.assertTrue(args.is_valid_datapointname(response.data['datapointname']))

    def test_get_datapoint_config_request_failure_invalid_passport(self):
        ''' get_datapoint_config_request should fail if passport is invalid '''
        passports=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        for psp in passports:
            response=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datapoint_config_request_failure_invalid_pid(self):
        ''' get_datapoint_config_request should fail if pid is invalid '''
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        for pid in pids:
            response=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_passport(self):
        ''' delete_datapoint_request should fail if username is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        for psp in passports:
            response=datapointapi.delete_datapoint_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_pid(self):
        ''' delete_datapoint_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        for pid in pids:
            response=datapointapi.delete_datapoint_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_passport(self):
        ''' mark_positive_variable_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=10
        length=1
        for psp in passports:
            response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_pid(self):
        ''' mark_positive_variable_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        sequence='23423234565432345678'
        position=10
        length=1
        for pid in pids:
            response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_sequence(self):
        ''' mark_positive_variable_request should fail if sequence is invalid '''
        sequences=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        position=10
        length=1
        for sequence in sequences:
            response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_position(self):
        ''' mark_positive_variable_request should fail if position is invalid '''
        positions=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_length(self):
        ''' mark_positive_variable_request should fail if length is invalid '''
        lengths=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_non_existing_datapoint(self):
        ''' mark_positive_variable_request should fail if datapoint does not exist '''
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence=uuid.uuid1().hex
        position=1
        length=1
        response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
        self.assertEqual(response.error, autherrors.E_ARA_AMPOSV_RE.value)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_mark_positive_variable_request_success(self):
        ''' mark_positive_variable_request should succeed '''
        psp = self.passport
        did=uuid.UUID(self.agents[0]['dids'][0])
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        sequence=timeuuid.get_custom_sequence(ds_date)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='positive_datapoint_x'
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did.hex, sequence=sequence, position=position, length=length, datapointname=datapoint_uri)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        pid = None
        while len(msgs)>0:
            for msg in msgs:
                if msg._type_ == messages.Messages.FILL_DATAPOINT_MESSAGE:
                    pid = msg.pid
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=datapointapi.mark_positive_variable_request(passport=psp, pid=pid.hex, sequence=sequence, position=position, length=length)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        self.assertEqual(len(msgs),1)
        self.assertEqual(msgs[0]._type_, messages.Messages.POS_VAR_MESSAGE)

    def test_mark_negative_variable_request_failure_invalid_passport(self):
        ''' mark_negative_variable_request should fail if passport is invalid '''
        passports=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=10
        length=1
        for psp in passports:
            response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_pid(self):
        ''' mark_negative_variable_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        sequence='23423234565432345678'
        position=10
        length=1
        for pid in pids:
            response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_sequence(self):
        ''' mark_negative_variable_request should fail if sequence is invalid '''
        sequences=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        position=10
        length=1
        for sequence in sequences:
            response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_position(self):
        ''' mark_negative_variable_request should fail if position is invalid '''
        positions=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_length(self):
        ''' mark_negative_variable_request should fail if length is invalid '''
        lengths=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_non_existing_datapoint(self):
        ''' mark_negative_variable_request should fail if datapoint does not exist '''
        psp = self.passport
        pid=uuid.uuid4().hex
        sequence=uuid.uuid1().hex
        position=1
        length=1
        response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid, sequence=sequence, position=position, length=length)
        self.assertEqual(response.error, autherrors.E_ARA_AMNEGV_RE.value)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_mark_negative_variable_request_success(self):
        ''' mark_negative_variable_request should succeed '''
        psp = self.passport
        did=uuid.UUID(self.agents[0]['dids'][0])
        ds_content='x: 23, y: 45'
        ds_date=timeuuid.uuid1()
        sequence=timeuuid.get_custom_sequence(ds_date)
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=did, date=ds_date, content=ds_content))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=did, date=ds_date))
        position=3
        length=2
        datapoint_uri='negative_datapoint_x'
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did.hex, sequence=sequence, position=position, length=length, datapointname=datapoint_uri)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        pid = None
        while len(msgs)>0:
            for msg in msgs:
                if msg._type_ == messages.Messages.FILL_DATAPOINT_MESSAGE:
                    pid = msg.pid
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response=datapointapi.mark_negative_variable_request(passport=psp, pid=pid.hex, sequence=sequence, position=position, length=length)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        self.assertEqual(len(msgs),1)
        self.assertEqual(msgs[0]._type_, messages.Messages.NEG_VAR_MESSAGE)

    def test_get_datapoint_data_request_failure_invalid_passport(self):
        ''' get_datapoint_data_request should fail if passport is invalid '''
        passports=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        start_date='33'
        end_date='43'
        for psp in passports:
            response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error,Errors.E_IWADP_GDPDR_IPSP.value)

    def test_get_datapoint_data_request_failure_invalid_pid(self):
        ''' get_datapoint_data_request should fail if pid is invalid '''
        psp = self.passport
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        start_date='33'
        end_date='43'
        for pid in pids:
            response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error,Errors.E_IWADP_GDPDR_IP.value)

    def test_get_datapoint_data_request_failure_invalid_start_date(self):
        ''' get_datapoint_data_request should fail if start_date is invalid '''
        start_dates=[233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        pid = uuid.uuid4().hex
        end_date='43'
        for start_date in start_dates:
            response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error,Errors.E_IWADP_GDPDR_ISD.value)

    def test_get_datapoint_data_request_failure_invalid_end_date(self):
        ''' get_datapoint_data_request should fail if end_date is invalid '''
        end_dates=[233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        pid = uuid.uuid4().hex
        start_date='43'
        for end_date in end_dates:
            response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error,Errors.E_IWADP_GDPDR_IED.value)

    def test_get_datapoint_data_request_failure_invalid_tid(self):
        ''' get_datapoint_data_request should fail if tid is invalid '''
        tids=[233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        psp = self.passport
        pid = uuid.uuid4().hex
        start_date='33'
        end_date='43'
        for tid in tids:
            response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date, tid=tid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error,Errors.E_IWADP_GDPDR_IT.value)

    def test_get_datapoint_data_request_failure_non_existent_datapoint(self):
        ''' get_datapoint_data_request should fail if pid does not exist '''
        psp = self.passport
        pid = uuid.uuid4().hex
        start_date=None
        end_date=None
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error,autherrors.E_ARA_AGDPD_RE.value)

    def test_get_datapoint_data_request_failure_datapoint_data_not_found(self):
        ''' get_datapoint_data_request should fail if there is no data found '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_get_datapoint_data_request_failure_datapoint_data_not_found'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][6]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        start_date='10'
        end_date='20'
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error,gesterrors.E_GPA_GDD_DDNF.value)

    def test_get_datapoint_data_request_success_datapoint_data_found(self):
        ''' get_datapoint_data_request should succeed and return the data found '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_get_datapoint_data_request_success_datapoint_data_found'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][7]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        start_date='1'
        end_date=None
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data),5) # 5 because monitor_datapoint tries to store 5 sampls
        self.assertEqual(response.data[0]['value'],7)

    def test_get_datapoint_data_request_failure_date_requested_before_interval_bounds_limit(self):
        ''' get_datapoint_data_request should fail if data requested interval is before
            min interval ts allowed '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_get_datapoint_data_request_failure_datapoint_data_requested_before_interval_bounds_limit'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][8]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.HIGHEST_TIME_UUID
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        start_date=None
        end_date='100'
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_ALLOWED)
        self.assertEqual(response.error, autherrors.E_AQA_AGDPD_IBE.value)
        self.assertEqual(response.data, {'error':autherrors.E_AQA_AGDPD_IBE.value})
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_get_datapoint_data_request_success_date_requested_after_interval_bounds_limit(self):
        ''' get_datapoint_data_request should succeed if data requested interval is after
            min interval ts allowed. '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_get_datapoint_data_request_success_datapoint_data_requested_after_interval_bounds_limit'
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][9]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.unrouted_messages
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.unrouted_messages:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourceinfo=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        iface=interfaces.User_DataRetrievalMinTimestamp().value
        minTs=timeuuid.uuid1(seconds=500)
        self.assertTrue(cassapiiface.insert_user_iface_deny(psp.uid, iface, minTs.hex))
        start_date='100'
        end_date=str(timeuuid.get_unix_timestamp(timeuuid.uuid1()))
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=start_date, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data),5) # 5 because monitor_datapoint tries to store 5 sampls
        self.assertEqual(response.data[0]['value'],9)
        #the same query without setting start_date
        response=datapointapi.get_datapoint_data_request(passport=psp, pid=pid, start_date=None, end_date=end_date)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(len(response.data),5)
        self.assertEqual(response.data[0]['value'],9)
        self.assertTrue(cassapiiface.delete_user_iface_deny(psp.uid, iface))

    def test_dissociate_datapoint_from_datasource_request_failure_invalid_passport(self):
        ''' dissociate_datapoint_from_datasource_request should fail if passport is invalid '''
        passports=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        for psp in passports:
            response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWADP_DDPFDS_IPSP.value)

    def test_dissociate_datapoint_from_datasource_request_failure_invalid_pid(self):
        ''' dissociate_datapoint_from_datasource_request should fail if passport is invalid '''
        psp = self.passport
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        for pid in pids:
            response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWADP_DDPFDS_IP.value)

    def test_dissociate_datapoint_from_datasource_request_failure_non_existent_pid(self):
        ''' dissociate_datapoint_from_datasource_request should fail if pid does not exist '''
        psp = self.passport
        pid = uuid.uuid4().hex
        response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADDPFDS_RE.value)

    def test_dissociate_datapoint_from_datasource_request_success_datapoint_associated(self):
        ''' dissociate_datapoint_from_datasource_request should succeed if datapoint is
            not associated already '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_dissociate_datapoint_from_datasource_request_success_datapoint_not_associated'
        datasource_config=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(datasource_config.status, status.WEB_STATUS_OK)
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][10]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        pid=None
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.MON_VAR_MESSAGE and msg.did==uuid.UUID(did):
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgs=msg_result.unrouted_messages
                    for msg in msgs:
                        if msg.type==messages.Messages.UPDATE_QUOTES_MESSAGE:
                            pid=msg.params['pid'].hex
                        msg_result=msgapi.process_message(msg)
                else:
                    msg_result=msgapi.process_message(msg)
            else:
                msgapi.process_message(msg)
        self.assertIsNotNone(pid)
        datapoint_config=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapoint_config.status, status.WEB_STATUS_OK)
        self.assertEqual(datapoint_config.data['pid'], pid)
        self.assertEqual(datapoint_config.data['did'], did)
        response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        found=False
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE and msg.params['pid'].hex == pid and msg.params['did'].hex == did:
                found=True
            msg_result=msgapi.process_message(msg)
            msgs=msg_result.unrouted_messages
            for amsg in msgs:
                msgapi.process_message(amsg)
        self.assertTrue(found)
        datapoint_config=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapoint_config.status, status.WEB_STATUS_OK)
        self.assertEqual(datapoint_config.data['pid'], pid)
        self.assertTrue('did' not in datapoint_config.data)

    def test_dissociate_datapoint_from_datasource_request_success_datapoint_not_associated(self):
        ''' dissociate_datapoint_from_datasource_request should succeed if datapoint is
            not associated already '''
        psp = self.passport
        did=self.agents[0]['dids'][0]
        datapointname='test_dissociate_datapoint_from_datasource_request_success_datapoint_not_associated'
        datasource_config=datasourceapi.get_datasource_config_request(passport=psp, did=did)
        self.assertEqual(datasource_config.status, status.WEB_STATUS_OK)
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][10]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        pid=None
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.MON_VAR_MESSAGE and msg.did==uuid.UUID(did):
                msg_result=msgapi.process_message(msg)
                if msg_result:
                    msgs=msg_result.unrouted_messages
                    for msg in msgs:
                        if msg.type==messages.Messages.UPDATE_QUOTES_MESSAGE:
                            pid=msg.params['pid'].hex
                        msg_result=msgapi.process_message(msg)
                else:
                    msg_result=msgapi.process_message(msg)
            else:
                msgapi.process_message(msg)
        self.assertIsNotNone(pid)
        datapoint_config=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapoint_config.status, status.WEB_STATUS_OK)
        self.assertEqual(datapoint_config.data['pid'], pid)
        self.assertEqual(datapoint_config.data['did'], did)
        response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        found=False
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE and msg.params['pid'].hex == pid and msg.params['did'].hex == did:
                found=True
            msg_result=msgapi.process_message(msg)
            msgs=msg_result.unrouted_messages
            for amsg in msgs:
                msgapi.process_message(amsg)
        self.assertTrue(found)
        datapoint_config=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapoint_config.status, status.WEB_STATUS_OK)
        self.assertEqual(datapoint_config.data['pid'], pid)
        self.assertTrue('did' not in datapoint_config.data)
        #launch again over the dissociated datapoint
        response=datapointapi.dissociate_datapoint_from_datasource_request(passport=psp, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        found=False
        for msg in response.unrouted_messages:
            if msg.type==messages.Messages.UPDATE_QUOTES_MESSAGE and msg.operation==Operations.DISSOCIATE_DATAPOINT_FROM_DATASOURCE and msg.params['pid'].hex == pid and msg.params['did'].hex == did:
                found=True
            msg_result=msgapi.process_message(msg)
            msgs=msg_result.unrouted_messages
            for amsg in msgs:
                msgapi.process_message(amsg)
        self.assertFalse(found)
        datapoint_config=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(datapoint_config.status, status.WEB_STATUS_OK)
        self.assertEqual(datapoint_config.data['pid'], pid)
        self.assertTrue('did' not in datapoint_config.data)

