import unittest
import uuid
import json
from komlibs.auth import operations
from komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlibs.gestaccount.datapoint import api as gestdatapointapi
from komlibs.interface.web.api import user as userapi 
from komlibs.interface.web.api import agent as agentapi 
from komlibs.interface.web.api import datasource as datasourceapi 
from komlibs.interface.web.api import datapoint as datapointapi 
from komlibs.interface.web.model import webmodel
from komlibs.interface.web import status, exceptions
from komlibs.general.validation import arguments as args
from komlibs.general.time import timeuuid
from komlibs.interface.imc.model import messages
from komlibs.interface.imc.api import rescontrol
from komimc import bus, routing
from komimc import api as msgapi
from komfig import logger


class InterfaceWebApiDatapointTest(unittest.TestCase):
    ''' komlibs.interface.web.api.datapoint tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        username = 'test_komlibs.interface.web.api.datapoint_user'
        userresponse=userapi.get_user_config_request(username=username)
        if userresponse.status==status.WEB_STATUS_NOT_FOUND:
            password = 'password'
            email = username+'@komlog.org'
            response = userapi.new_user_request(username=username, password=password, email=email)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            userresponse = userapi.get_user_config_request(username=username)
            self.assertEqual(userresponse.status, status.WEB_STATUS_OK)
            self.userinfo=userresponse.data
            agentname='test_komlibs.interface.web.api.datapoint_agent'
            pubkey='TESTKOMLIBSINTERFACEWEBAPIDATAPOINTAGENT'
            version='test library vX.XX'
            response = agentapi.new_agent_request(username=username, agentname=agentname, pubkey=pubkey, version=version)
            aid=response.data['aid']
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                self.assertIsNotNone(msg)
                if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_AGENT or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(response.data['aid'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_RESAUTH(msg)
            datasourcename='test_komlibs.interface.web.api.datapoint_datasource'
            response = datasourceapi.new_datasource_request(username=username, aid=aid, datasourcename=datasourcename)
            self.assertTrue(isinstance(response, webmodel.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                self.assertIsNotNone(msg)
                if msg.type!=messages.UPDATE_QUOTES_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])):
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_UPDQUO(msg)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                self.assertIsNotNone(msg)
                if msg.type!=messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE or not msg.operation==operations.NEW_DATASOURCE or not (msg.params['uid']==uuid.UUID(self.userinfo['uid']) and msg.params['aid']==uuid.UUID(aid) and msg.params['did']==uuid.UUID(response.data['did'])): 
                    msgapi.send_message(msg)
                    count+=1
                    if count>=1000:
                        break
                else:
                    break
            self.assertFalse(count>=1000)
            rescontrol.process_message_RESAUTH(msg)
            msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if not msg:
                    break
                if msg and msg.type==messages.UPDATE_QUOTES_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']):
                    rescontrol.process_message_UPDQUO(msg)
                else:
                    msgapi.send_message(msg)
                    count+=1
                    if count>=100:
                        break
            count=0
            while True:
                msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
                if not msg:
                    break
                if msg and msg.type==messages.RESOURCE_AUTHORIZATION_UPDATE_MESSAGE and msg.operation==operations.NEW_WIDGET_SYSTEM and msg.params['uid']==uuid.UUID(self.userinfo['uid']): 
                    rescontrol.process_message_RESAUTH(msg)
                else:
                    msgapi.send_message(msg)
                    count+=1
                    if count>=100:
                        break
            userresponse=userapi.get_user_config_request(username=username)
            did=userresponse.data['agents'][0]['dids'][0]
            content='DATAPOINT TESTS CONTENT 0 1 2 3 4 5 6 7 8'
            date=timeuuid.uuid1()
            self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(did), date=date, content=content))
            self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(did), date=date))
        self.userinfo=userresponse.data

    def test_new_datapoint_request_success(self):
        ''' new_datapoint_request should succeed if parameters exists, and user has permission '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_success'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][0]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            self.assertIsNotNone(msg)
            if msg.type!=messages.MON_VAR_MESSAGE or msg.did!=uuid.UUID(did):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        #we put the message off the queue, but we process it manually calling the gestaccount directly
        datapoint=gestdatapointapi.monitor_new_datapoint(did=msg.did, date=msg.date, position=msg.position, length=msg.length, datapointname=msg.datapointname)
        self.assertIsNotNone(datapoint)
        self.assertEqual(datapoint['datapointname'],datapointname)
        self.assertEqual(datapoint['did'],uuid.UUID(did))

    def test_new_datapoint_request_failure_invalid_username(self):
        ''' new_datapoint_request should fail if username is invalid '''
        usernames=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        variable=(0,1)
        for username in usernames:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_invalid_did(self):
        ''' new_datapoint_request should fail if did is invalid '''
        username='test_new_datapoint_request_failure'
        dids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        variable=(0,1)
        for did in dids:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_invalid_datapointname(self):
        ''' new_datapoint_request should fail if datapointname is invalid '''
        datapointnames=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'user\tName','user name\n','userñame',json.dumps('username')]
        did=self.userinfo['agents'][0]['dids'][0]
        username='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        variable=(0,1)
        for datapointname in datapointnames:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_invalid_sequence(self):
        ''' new_datapoint_request should fail if sequence is invalid '''
        username='test_new_datapoint_request_failure'
        sequences=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4(),'abcde1234567890ABCDF1','abcde1234567890ABCD']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_failure'
        variable=(0,1)
        for sequence in sequences:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_invalid_position(self):
        ''' new_datapoint_request should fail if position is invalid '''
        username='test_new_datapoint_request_failure'
        positions=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_invalid_length(self):
        ''' new_datapoint_request should fail if length is invalid '''
        username='test_new_datapoint_request_failure'
        lengths=[None, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_datapoint_request_failure_no_permission_user_does_not_exist(self):
        ''' new_datapoint_request should fail if user does not exist '''
        username='test_new_datapoint_request_failure_no_permission_user_does_not_exist'
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        position=1
        length=1
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_datapoint_request_failure_no_permission_did_does_not_exist(self):
        ''' new_datapoint_request should fail if did does not exist '''
        username=self.userinfo['username']
        did=uuid.uuid4().hex
        datapointname='test_new_datapoint_request_failure'
        sequence='23423234565432345678'
        position=1
        length=1
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_datapoint_config_request_failure_invalid_username(self):
        ''' update_datapoint_config_request should fail if username is invalid '''
        usernames=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        for username in usernames:
            response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_invalid_data(self):
        ''' update_datapoint_config_request should fail if data is invalid '''
        datas=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        username=self.userinfo['username']
        pid=uuid.uuid4().hex
        for data in datas:
            response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_invalid_pid(self):
        ''' update_datapoint_config_request should fail if pid is invalid '''
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        username=self.userinfo['username']
        data={'datapointname':'datapointname','color':'#FFAADD'}
        for pid in pids:
            response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_update_datapoint_config_request_failure_non_existent_pid(self):
        ''' update_datapoint_config_request should fail if pid does not exist '''
        username=self.userinfo['username']
        pid=uuid.uuid4().hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_datapoint_config_request_failure_non_existent_username(self):
        ''' update_datapoint_config_request should fail if user does not exist '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_update_datapoint_config_request_failure_non_existent_username'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        variable=datasourcedata.data['variables'][1]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            self.assertIsNotNone(msg)
            if msg.type!=messages.MON_VAR_MESSAGE or msg.did!=uuid.UUID(did):
                msgapi.send_message(msg)
                count+=1
                if count>=1000:
                    break
            else:
                break
        #we put the message off the queue, but we process it manually calling the gestaccount directly
        datapoint=gestdatapointapi.monitor_new_datapoint(did=msg.did, date=msg.date, position=msg.position, length=msg.length, datapointname=msg.datapointname)
        self.assertIsNotNone(datapoint)
        self.assertEqual(datapoint['datapointname'],datapointname)
        self.assertEqual(datapoint['did'],uuid.UUID(did))
        username='test_update_datapoint_config_request_failure_non_existent_username'
        pid=datapoint['pid'].hex
        data={'datapointname':'datapointname','color':'#FFAADD'}
        response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_update_datapoint_config_request_success_new_datapointname(self):
        ''' update_datapoint_config_request should succeed, updating datapointname only '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_datapointname'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][2]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception as e:
                    logger.logger.debug('EXCEPTION '+str(e)+' '+str(msg.serialized_message))
                    pass
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception:
                    pass
            else:
                break
        datasourceinfo=datasourceapi.get_datasource_data_request(username=username, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        new_datapointname='test_update_datapoint_config_request_success_new_datapointname2'
        data={'datapointname':new_datapointname}
        response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        self.assertEqual(datapointinfo.data['color'],datapointinfo2.data['color'])
        self.assertEqual(new_datapointname,datapointinfo2.data['datapointname'])

    def test_update_datapoint_config_request_success_new_color(self):
        ''' update_datapoint_config_request should succeed, updating color only '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_datapointname'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][3]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception as e:
                    logger.logger.debug('EXCEPTION '+str(e)+' '+str(msg.serialized_message))
                    pass
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception:
                    pass
            else:
                break
        datasourceinfo=datasourceapi.get_datasource_data_request(username=username, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        new_color='#AA00EE'
        data={'color':new_color}
        response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        self.assertEqual(new_color,datapointinfo2.data['color'])
        self.assertEqual(datapointinfo.data['datapointname'],datapointinfo2.data['datapointname'])

    def test_update_datapoint_config_request_success_new_color_and_datapointname(self):
        ''' update_datapoint_config_request should succeed, updating datapointname and color '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_update_datapoint_config_request_success_new_datapointname'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][4]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception as e:
                    logger.logger.debug('EXCEPTION '+str(e)+' '+str(msg.serialized_message))
                    pass
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception:
                    pass
            else:
                break
        datasourceinfo=datasourceapi.get_datasource_data_request(username=username, did=did)
        pid=None
        for datapoint in datasourceinfo.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        datapointinfo=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        new_color='#AA00EE'
        new_datapointname='test_update_datapoint_config_request_success_new_color_and_datapointname'
        data={'color':new_color, 'datapointname':new_datapointname}
        response=datapointapi.update_datapoint_config_request(username=username, pid=pid, data=data)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        datapointinfo2=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        self.assertEqual(new_color,datapointinfo2.data['color'])
        self.assertEqual(new_datapointname,datapointinfo2.data['datapointname'])

    def test_get_datapoint_config_request_success(self):
        ''' get_datapoint_config_request should succeed, returning datapoint info '''
        username=self.userinfo['username']
        did=self.userinfo['agents'][0]['dids'][0]
        datapointname='test_get_datapoint_config_request_success'
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data['seq']
        position,length=datasourcedata.data['variables'][5]
        response=datapointapi.new_datapoint_request(username=username, did=did, sequence=sequence, position=position, length=length, datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msg_addr=routing.get_address(type=messages.MON_VAR_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception as e:
                    logger.logger.debug('EXCEPTION '+str(e)+' '+str(msg.serialized_message))
                    pass
            else:
                break
        msg_addr=routing.get_address(type=messages.UPDATE_QUOTES_MESSAGE, module_id=bus.msgbus.module_id, module_instance=bus.msgbus.module_instance, running_host=bus.msgbus.running_host)
        count=0
        while True:
            msg=msgapi.retrieve_message_from(addr=msg_addr, timeout=1)
            if msg:
                try:
                    msgresult=msgapi.process_message(msg)
                    if msgresult:
                        msgapi.process_msg_result(msgresult)
                except Exception:
                    pass
            else:
                break
        datasourcedata=datasourceapi.get_datasource_data_request(username=username, did=did)
        pid=None
        for datapoint in datasourcedata.data['datapoints']:
            if datapoint['index']==position:
                pid=datapoint['pid']
        self.assertIsNotNone(pid)
        response=datapointapi.get_datapoint_config_request(username=username, pid=pid)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertEqual(datasourcedata.data['did'], response.data['did'])
        self.assertEqual(pid, response.data['pid'])
        self.assertTrue('datapointname' in response.data)
        self.assertTrue(args.is_valid_datapointname(response.data['datapointname']))

    def test_get_datapoint_config_request_failure_invalid_username(self):
        ''' get_datapoint_config_request should fail if username is invalid '''
        usernames=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        pid=uuid.uuid4().hex
        for username in usernames:
            response=datapointapi.get_datapoint_config_request(username=username, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_datapoint_config_request_failure_invalid_pid(self):
        ''' get_datapoint_config_request should fail if pid is invalid '''
        pids=[None, 233423, 2342.2342, {'a':'dict'},['a','list'],('a','tuple'),'userName','user name','userñame',json.dumps('username'), uuid.uuid4()]
        username=self.userinfo['username']
        for pid in pids:
            response=datapointapi.get_datapoint_config_request(username=username, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_username(self):
        ''' delete_datapoint_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        for username in usernames:
            response=datapointapi.delete_datapoint_request(username=username, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_datapoint_request_failure_invalid_pid(self):
        ''' delete_datapoint_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_delete_datapoint_request_failure_invalid_pid'
        for pid in pids:
            response=datapointapi.delete_datapoint_request(username=username, pid=pid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_username(self):
        ''' mark_positive_variable_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=10
        length=1
        for username in usernames:
            response=datapointapi.mark_positive_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_pid(self):
        ''' mark_positive_variable_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_positive_variable_request_failure_invalid_pid'
        sequence='23423234565432345678'
        position=10
        length=1
        for pid in pids:
            response=datapointapi.mark_positive_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_sequence(self):
        ''' mark_positive_variable_request should fail if sequence is invalid '''
        sequences=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_positive_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        position=10
        length=1
        for sequence in sequences:
            response=datapointapi.mark_positive_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_position(self):
        ''' mark_positive_variable_request should fail if position is invalid '''
        positions=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_positive_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.mark_positive_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_positive_variable_request_failure_invalid_length(self):
        ''' mark_positive_variable_request should fail if length is invalid '''
        lengths=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_positive_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.mark_positive_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_username(self):
        ''' mark_negative_variable_request should fail if username is invalid '''
        usernames=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=10
        length=1
        for username in usernames:
            response=datapointapi.mark_negative_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_pid(self):
        ''' mark_negative_variable_request should fail if pid is invalid '''
        pids=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_negative_variable_request_failure_invalid_pid'
        sequence='23423234565432345678'
        position=10
        length=1
        for pid in pids:
            response=datapointapi.mark_negative_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_sequence(self):
        ''' mark_negative_variable_request should fail if sequence is invalid '''
        sequences=['Username','userñame',None, 23234, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_negative_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        position=10
        length=1
        for sequence in sequences:
            response=datapointapi.mark_negative_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_position(self):
        ''' mark_negative_variable_request should fail if position is invalid '''
        positions=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_negative_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        length=1
        for position in positions:
            response=datapointapi.mark_negative_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_mark_negative_variable_request_failure_invalid_length(self):
        ''' mark_negative_variable_request should fail if length is invalid '''
        lengths=['Username','userñame',None, 2342.23423, {'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid1()]
        username='test_mark_negative_variable_request_failure_invalid_sequence'
        pid=uuid.uuid4().hex
        sequence='23423234565432345678'
        position=1
        for length in lengths:
            response=datapointapi.mark_negative_variable_request(username=username, pid=pid, sequence=sequence, position=position, length=length)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

