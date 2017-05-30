import unittest
import uuid
import json
from base64 import b64encode, b64decode
from komlog.komlibs.auth import passport
from komlog.komlibs.auth.errors import Errors as autherrors
from komlog.komlibs.gestaccount.errors import Errors as gesterrors
from komlog.komlibs.gestaccount.widget import types
from komlog.komlibs.gestaccount.datasource import api as gestdatasourceapi
from komlog.komlibs.interface.web.api import login as loginapi
from komlog.komlibs.interface.web.api import user as userapi
from komlog.komlibs.interface.web.api import agent as agentapi
from komlog.komlibs.interface.web.api import datasource as datasourceapi
from komlog.komlibs.interface.web.api import datapoint as datapointapi
from komlog.komlibs.interface.web.api import widget as widgetapi
from komlog.komlibs.interface.web.api import snapshot as snapshotapi
from komlog.komlibs.interface.web.api import circle as circleapi
from komlog.komlibs.interface.web.model import response as webresp
from komlog.komlibs.interface.web import status, exceptions
from komlog.komlibs.interface.web.errors import Errors
from komlog.komlibs.general.validation import arguments as args
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.interface.imc import status as imcstatus
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc.api import rescontrol, gestconsole
from komlog.komimc import bus, routing
from komlog.komimc import api as msgapi
from komlog.komfig import logging


class InterfaceWebApiSnapshotTest(unittest.TestCase):
    ''' komlibs.interface.web.api.snapshot tests '''

    def setUp(self):
        ''' In this module, we need a user and agent '''
        self.username = 'test_komlibs.interface.web.api.snapshot_user'
        self.password = 'password'
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username+'@komlog.org'
            response = userapi.new_user_request(username=self.username, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.imc_messages['unrouted']:
                if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                    code = msg.code
                    userapi.confirm_user_request(email=email, code=code)
            msgs=response.imc_messages['unrouted']
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.imc_messages['unrouted']:
                        msgs.append(msg2)
        response = loginapi.login_request(username=self.username, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport = passport.get_user_passport(cookie)
        agentname='test_komlibs.interface.web.api.snapshot_agent'
        pubkey=b64encode(crypto.serialize_public_key(crypto.generate_rsa_key().public_key())).decode('utf-8')
        version='test library vX.XX'
        response = agentapi.new_agent_request(passport=self.passport, agentname=agentname, pubkey=pubkey, version=version)
        if response.status==status.WEB_STATUS_OK:
            msgs=response.imc_messages['unrouted']
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.imc_messages['unrouted']:
                        msgs.append(msg2)
                    self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        agents_info=agentapi.get_agents_config_request(passport=self.passport)
        self.agents=agents_info.data
        aid = response.data['aid']
        cookie = passport.AgentCookie(aid=uuid.UUID(aid),pv=1,sid=uuid.uuid4(),seq=timeuuid.get_custom_sequence(uuid.uuid1())).to_dict()
        self.agent_passport = passport.get_agent_passport(cookie)
        self.username_to_share='test_komlibs.interface.web.api.snapshot_user_to_share'
        response = loginapi.login_request(username=self.username_to_share, password=self.password)
        cookie=getattr(response, 'cookie',None)
        if response.status==status.WEB_STATUS_NOT_FOUND:
            email = self.username_to_share+'@komlog.org'
            response = userapi.new_user_request(username=self.username_to_share, password=self.password, email=email)
            self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
            self.assertEqual(response.status, status.WEB_STATUS_OK)
            for msg in response.imc_messages['unrouted']:
                if msg.type == messages.Messages.NEW_USR_NOTIF_MESSAGE:
                    code = msg.code
                    userapi.confirm_user_request(email=email, code=code)
            msgs=response.imc_messages['unrouted']
            while len(msgs)>0:
                for msg in msgs:
                    msgs.remove(msg)
                    msgresponse=msgapi.process_message(msg)
                    for msg2 in msgresponse.imc_messages['unrouted']:
                        msgs.append(msg2)
        response = loginapi.login_request(username=self.username_to_share, password=self.password)
        cookie=getattr(response, 'cookie',None)
        self.passport_share = passport.get_user_passport(cookie)

    def test_get_snapshots_config_request_failure_invalid_passport(self):
        ''' get_snapshots_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        for psp in passports:
            response=snapshotapi.get_snapshots_config_request(passport=psp)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_get_snapshots_config_request_failure_non_existent_username(self):
        ''' get_snapshots_config_request should fail if username does not exist '''
        psp = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response=snapshotapi.get_snapshots_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_NOT_FOUND)
        self.assertEqual(response.error, gesterrors.E_GSA_GSSC_UNF.value)

    def test_get_snapshots_config_request_success_no_matter_how_much_snapshots(self):
        ''' get_snapshots_config_request should succeed and return a list '''
        psp = self.passport
        response=snapshotapi.get_snapshots_config_request(passport=psp)
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(response.data,list))

    def test_get_snapshot_config_request_failure_invalid_passport(self):
        ''' get_snapshot_config_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        nid=uuid.uuid4().hex
        for psp in passports:
            response=snapshotapi.get_snapshot_config_request(passport=psp,nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWASN_GSNCR_IPSP.value)

    def test_get_snapshot_config_request_failure_invalid_nid(self):
        ''' get_snapshot_config_request should fail if nid is invalid '''
        nids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(), uuid.uuid4(), uuid.uuid1().hex]
        psp = self.passport
        for nid in nids:
            response=snapshotapi.get_snapshot_config_request(passport=psp,nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWASN_GSNCR_IN.value)

    def test_get_snapshot_config_request_failure_invalid_ticket(self):
        ''' get_snapshot_config_request should fail if username is invalid '''
        tickets=[32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid4(), uuid.uuid1().hex,uuid.uuid1()]
        nid=uuid.uuid4().hex
        psp = self.passport
        for ticket in tickets:
            response=snapshotapi.get_snapshot_config_request(passport=psp,nid=nid, tid=ticket)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)
            self.assertEqual(response.error, Errors.E_IWASN_GSNCR_IT.value)

    def test_get_snapshot_config_request_failure_non_existent_nid(self):
        ''' get_snapshot_config_request should fail if nid does not exist '''
        nid=uuid.uuid4().hex
        psp = self.passport
        response=snapshotapi.get_snapshot_config_request(passport=psp,nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_snapshot_config_request_success_snapshot_linegraph(self):
        ''' get_snapshot_config_request should succeed  '''
        psp = self.passport
        widgetname='test_get_snapshot_config_request_success_snapshot_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_linegraph_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_linegraph_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        psp = self.passport
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_histogram(self):
        ''' get_snapshot_config_request should succeed '''
        psp = self.passport
        widgetname='test_get_snapshot_config_request_success_snapshot_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        datasourcename='test_get_snapshot_config_request_success_snapshot_histogram_ds'
        psp = self.agent_passport
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_histogram_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_table(self):
        ''' get_snapshot_config_request should succeed '''
        psp = self.passport
        widgetname='test_get_snapshot_config_request_success_snapshot_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_table_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_table_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])

    def test_get_snapshot_config_request_success_snapshot_multidp(self):
        ''' get_snapshot_config_request should succeed '''
        psp = self.passport
        widgetname='test_get_snapshot_config_request_success_snapshot_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_multidp_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_multidp_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        datapoint_color=response4.data['color']
        datapoint_name=response4.data['datapointname']
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'],[pid])
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.MULTIDP)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'datapointname':datapoint_name,'color':datapoint_color}])

    def test_get_snapshot_config_request_success_snapshot_datasource(self):
        ''' get_snapshot_config_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_datasource'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data[0]['seq']
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['seq'],sequence)
        self.assertEqual(response7.data['datasource'],{'did':did,'datasourcename':datasourcename})
        self.assertEqual(response7.data['datapoints'],[])

    def test_get_snapshot_config_request_success_snapshot_datasource_shared_to_circle(self):
        ''' new_snapshot_request should succeed and accesses from circle members granted '''
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_datasource_shared_to_circle'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data[0]['seq']
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        #we create a circle with the member username_to_share
        username_to_share=self.username_to_share
        circlename='test_get_snapshot_config_request_success_snapshot_datasource_shared_with_circle'
        circle_response=circleapi.new_users_circle_request(passport=psp,circlename=circlename,members_list=[username_to_share])
        self.assertEqual(circle_response.status, status.WEB_STATUS_OK)
        cid=circle_response.data['cid']
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,cid_list=[cid],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['its'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['ets'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['datasource'],{'did':did,'datasourcename':datasourcename})
        self.assertEqual(response7.data['datapoints'],[])
        response8=datasourceapi.get_datasource_config_request(passport=psp_to_share, did=did)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did, seq=response7.data['seq'],tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_OK)
        self.assertEqual(response9.data[0]['content'],datasourcecontent)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did, seq=response7.data['seq'])
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did,tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did)
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datasourceapi.get_datasource_config_request(passport=psp_to_deny, did=did)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_get_snapshot_config_request_success_snapshot_datapoint(self):
        ''' get_snapshot_config_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_get_snapshot_config_request_success_snapshot_datapoint'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_get_snapshot_config_request_success_snapshot_datapoint'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        color=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(passport=psp,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']=='.'.join((datasourcename,datapointname)):
                    wid=widget['wid']
                    pid=widget['pid']
                    color=datapointconfig.data['color']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoint'],{'pid':pid,'datapointname':'.'.join((datasourcename,datapointname)), 'color':color})
        psp_to_share = self.passport_share
        response7 = snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoint'],{'pid':pid,'datapointname':'.'.join((datasourcename,datapointname)), 'color':color})
        response7 = snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_delete_snapshot_request_failure_invalid_passport(self):
        ''' delete_snapshot_request should fail if passport is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame', uuid.uuid4(), uuid.uuid1()]
        nid=uuid.uuid4().hex
        for psp in passports:
            response=snapshotapi.delete_snapshot_request(passport=psp, nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_snapshot_request_failure_invalid_nid(self):
        ''' delete_snapshot_request should fail if nid is invalid '''
        nids=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        for nid in nids:
            response=snapshotapi.delete_snapshot_request(passport=psp, nid=nid)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_delete_snapshot_request_failure_non_existent_username(self):
        ''' delete_snapshot_request should fail if username does not exist '''
        psp = self.passport
        nid=uuid.uuid4().hex
        response=snapshotapi.delete_snapshot_request(passport=psp, nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADS_RE.value)

    def test_delete_snapshot_request_failure_non_existent_nid(self):
        ''' delete_snapshot_request should fail if username does not exist '''
        psp = self.passport
        nid=uuid.uuid4().hex
        response=snapshotapi.delete_snapshot_request(passport=psp, nid=nid)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)
        self.assertEqual(response.error, autherrors.E_ARA_ADS_RE.value)

    def test_delete_snapshot_request_success_snapshot_linegraph(self):
        ''' delete_snapshot_request should succeed and delete the snapshot '''
        psp = self.passport
        widgetname='test_delete_snapshot_request_success_snapshot_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_linegraph_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_linegraph_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_histogram(self):
        ''' delete_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_delete_snapshot_request_success_snapshot_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_histogram_datasource'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_histogram_datapoint'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_table(self):
        ''' delete_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_delete_snapshot_request_success_snapshot_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_table_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_table_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,its=its,user_list=[username_to_share],ets=ets,wid=wid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_multidp(self):
        ''' delete_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_delete_snapshot_request_success_snapshot_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_multidp_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_multidp_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                num_widgets+=1
                pid=widget['pid']
        self.assertTrue(num_widgets>=1)
        response4=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        datapoint_color=response4.data['color']
        datapoint_name=response4.data['datapointname']
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'],[pid])
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,its=its,user_list=[username_to_share],ets=ets,wid=wid)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        psp_to_share = self.passport_share
        response7 = snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.MULTIDP)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'datapointname':datapoint_name,'color':datapoint_color}])
        response8 = snapshotapi.delete_snapshot_request(passport=psp_to_share, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_datasource(self):
        ''' delete_snapshot_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_datasource'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data[0]['seq']
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['seq'],sequence)
        self.assertEqual(response7.data['datasource'],{'did':did, 'datasourcename':datasourcename})
        self.assertEqual(response7.data['datapoints'],[])
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_delete_snapshot_request_success_snapshot_datapoint(self):
        ''' delete_snapshot_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_delete_snapshot_request_success_snapshot_datapoint_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_delete_snapshot_request_success_snapshot_datapoint_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        color=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(passport=psp,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']=='.'.join((datasourcename,datapointname)):
                    wid=widget['wid']
                    pid=widget['pid']
                    color=datapointconfig.data['color']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response7 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoint'],{'pid':pid, 'datapointname':'.'.join((datasourcename,datapointname)),'color':color})
        response8 = snapshotapi.delete_snapshot_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response8.status, status.WEB_STATUS_OK)
        response9 = snapshotapi.get_snapshot_config_request(passport=psp, nid=response6.data['nid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)

    def test_new_snapshot_request_failure_invalid_passport(self):
        ''' new_snapshot_request should fail if username is invalid '''
        passports=[None, 32423, 023423.23423, {'a':'dict'},['a','list'],('a','tuple'),'Username','user name','userñame']
        wid=uuid.uuid4().hex
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        username_to_share=self.username_to_share
        for psp in passports:
            response=snapshotapi.new_snapshot_request(passport=psp, wid=wid,user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_invalid_wid(self):
        ''' new_snapshot_request should fail if data is invalid '''
        wids=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid4(), uuid.uuid1(), uuid.uuid1().hex]
        psp = self.passport
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        username_to_share=self.username_to_share
        for wid in wids:
            response=snapshotapi.new_snapshot_request(passport=psp, wid=wid, user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_no_sequence(self):
        ''' new_snapshot_request should fail if no sequence is passed or is invalid '''
        psp = self.passport
        wid=uuid.uuid4().hex
        seqs=[None, 32423, 023423.23423, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(),uuid.uuid4().hex,uuid.uuid4(),'abcde']
        username_to_share=self.username_to_share
        for seq in seqs:
            response=snapshotapi.new_snapshot_request(passport=psp, wid=wid, user_list=[username_to_share],seq=seq)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_no_timestamps(self):
        ''' new_snapshot_request should fail if no timestamps are passed or are invalid  '''
        psp = self.passport
        wid=uuid.uuid4().hex
        tss=[None, ['a','list'],('a','tuple'),'Username','user name','userñame',uuid.uuid1(),uuid.uuid4().hex,uuid.uuid1().hex]
        username_to_share=self.username_to_share
        for ts in tss:
            its=ts
            ets=ts
            response=snapshotapi.new_snapshot_request(passport=psp, wid=wid,user_list=[username_to_share],its=its,ets=ets)
            self.assertEqual(response.status, status.WEB_STATUS_BAD_PARAMETERS)

    def test_new_snapshot_request_failure_non_existent_widget(self):
        ''' new_snapshot_request should fail if widget does not exist '''
        psp = self.passport
        wid=uuid.uuid4().hex
        username_to_share=self.username_to_share
        seq=timeuuid.get_custom_sequence(timeuuid.uuid1())
        response=snapshotapi.new_snapshot_request(passport=psp, wid=wid,user_list=[username_to_share],seq=seq)
        self.assertEqual(response.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_linegraph_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the linegraph widget has no datapoints '''
        psp = self.passport
        widgetname='test_new_snapshot_request_failure_widget_linegraph_has_no_datapoints'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=3
        username_to_share=self.username_to_share
        new_snapshot_resp = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_linegraph(self):
        ''' new_snapshot_request should succeed  '''
        psp = self.passport
        widgetname='test_new_snapshot_request_success_widget_linegraph'
        data={'type':types.LINEGRAPH, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.LINEGRAPH)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_linegraph_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_linegraph_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.LINEGRAPH)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.LINEGRAPH)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(passport=psp_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2',tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(passport=psp_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_histogram_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the histogram widget has no datapoints '''
        psp = self.passport
        widgetname='test_new_snapshot_request_failure_widget_histogram_has_no_datapoints'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        new_snapshot_resp = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_histogram(self):
        ''' new_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_new_snapshot_request_success_widget_histogram'
        data={'type':types.HISTOGRAM, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.HISTOGRAM)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_histogram_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_histogram_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.HISTOGRAM)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.HISTOGRAM)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(passport=psp_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2',tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(passport=psp_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_table_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the table widget has no datapoints '''
        psp = self.passport
        widgetname='test_new_snapshot_request_failure_widget_table_has_no_datapoints'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        new_snapshot_resp = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_table(self):
        ''' new_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_new_snapshot_request_success_widget_table'
        data={'type':types.TABLE, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.TABLE)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_table_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_table_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.TABLE)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'][0]['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],ets=ets,its=its)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        self.assertTrue(isinstance(uuid.UUID(response6.data['tid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.TABLE)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'color':response5.data['datapoints'][0]['color']}])
        response8=datapointapi.get_datapoint_config_request(passport=psp_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2',tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(passport=psp_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_failure_widget_multidp_has_no_datapoints(self):
        ''' new_snapshot_request should fail if the multidp widget has no datapoints '''
        psp = self.passport
        widgetname='test_new_snapshot_request_failure_widget_multidp_has_no_datapoints'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        new_snapshot_resp = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],its=its,ets=ets)
        self.assertEqual(new_snapshot_resp.status, status.WEB_STATUS_NOT_ALLOWED)

    def test_new_snapshot_request_success_widget_multidp(self):
        ''' new_snapshot_request should succeed '''
        psp = self.passport
        widgetname='test_new_snapshot_request_success_widget_multidp'
        data={'type':types.MULTIDP, 'widgetname':widgetname}
        response = widgetapi.new_widget_request(passport=psp, data=data)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['wid']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        wid=response.data['wid']
        response3 = widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response3.status, status.WEB_STATUS_OK)
        self.assertEqual(response3.data['type'],types.MULTIDP)
        self.assertEqual(response3.data['widgetname'],widgetname)
        self.assertEqual(response3.data['datapoints'],[])
        self.assertEqual(response3.data['wid'],wid)
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_multidp_ds'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_multidp_dp'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        pid=None
        num_widgets=0
        for widget in response2.data:
            if widget['type']==types.DATAPOINT and widget['widgetname']=='.'.join((datasourcename,datapointname)):
                num_widgets+=1
                pid=widget['pid']
        self.assertEqual(num_widgets,1)
        response4=datapointapi.get_datapoint_config_request(passport=psp, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        datapoint_color=response4.data['color']
        datapoint_name=response4.data['datapointname']
        response4=widgetapi.add_datapoint_request(passport=psp, wid=wid, pid=pid)
        self.assertEqual(response4.status, status.WEB_STATUS_OK)
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.MULTIDP)
        self.assertEqual(response5.data['widgetname'],widgetname)
        self.assertEqual(len(response5.data['datapoints']),1)
        self.assertEqual(response5.data['datapoints'],[pid])
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],ets=ets,its=its)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.MULTIDP)
        self.assertEqual(response7.data['widgetname'],widgetname)
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoints'],[{'pid':pid,'datapointname':datapoint_name,'color':datapoint_color}])
        response8=datapointapi.get_datapoint_config_request(passport=psp_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2',tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny=passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(passport=psp_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_success_widget_datasource(self):
        ''' new_snapshot_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_datasource'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        did=response.data['did']
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        sequence=datasourcedata.data[0]['seq']
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        for widget in response2.data:
            if widget['type']==types.DATASOURCE and widget['did']==did:
                wid=widget['wid']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATASOURCE)
        self.assertEqual(response5.data['widgetname'],datasourcename)
        self.assertEqual(response5.data['wid'],wid)
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],seq=sequence)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATASOURCE)
        self.assertEqual(response7.data['widgetname'],datasourcename)
        self.assertEqual(response7.data['its'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['ets'],timeuuid.get_unix_timestamp(date))
        self.assertEqual(response7.data['datasource'],{'did':did,'datasourcename':datasourcename})
        self.assertEqual(response7.data['datapoints'],[])
        response8=datasourceapi.get_datasource_config_request(passport=psp_to_share, did=did)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did, seq=response7.data['seq'],tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_OK)
        self.assertEqual(response9.data[0]['content'],datasourcecontent)
        response9=datasourceapi.get_datasource_data_request(passport=psp_to_share, did=did)
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datasourceapi.get_datasource_config_request(passport=psp_to_deny, did=did)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

    def test_new_snapshot_request_success_widget_datapoint(self):
        ''' new_snapshot_request should succeed '''
        psp = self.agent_passport
        datasourcename='test_new_snapshot_request_success_widget_datapoint'
        response = datasourceapi.new_datasource_request(passport=psp,  datasourcename=datasourcename)
        self.assertTrue(isinstance(response, webresp.WebInterfaceResponse))
        self.assertEqual(response.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response.data['did']), uuid.UUID))
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        datasourcecontent='DATASOURCE CONTENT 1 2 3'
        date=timeuuid.uuid1()
        self.assertTrue(gestdatasourceapi.store_datasource_data(did=uuid.UUID(response.data['did']), date=date, content=datasourcecontent))
        self.assertTrue(gestdatasourceapi.generate_datasource_map(did=uuid.UUID(response.data['did']), date=date))
        psp = self.passport
        datasourcedata=datasourceapi.get_datasource_data_request(passport=psp, did=response.data['did'])
        self.assertEqual(datasourcedata.status, status.WEB_STATUS_OK)
        datapointname='test_new_snapshot_request_success_widget_datapoint'
        sequence=datasourcedata.data[0]['seq']
        variable=datasourcedata.data[0]['variables'][0]
        response=datapointapi.new_datasource_datapoint_request(passport=psp, did=response.data['did'], sequence=sequence, position=variable[0], length=variable[1], datapointname=datapointname)
        self.assertEqual(response.status, status.WEB_STATUS_RECEIVED)
        msgs=response.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        response2 = widgetapi.get_widgets_config_request(passport=psp)
        self.assertEqual(response2.status, status.WEB_STATUS_OK)
        wid=None
        pid=None
        color=None
        for widget in response2.data:
            if widget['type']==types.DATAPOINT:
                datapointconfig=datapointapi.get_datapoint_config_request(passport=psp,pid=widget['pid'])
                self.assertEqual(datapointconfig.status,status.WEB_STATUS_OK)
                if datapointconfig.data['datapointname']=='.'.join((datasourcename,datapointname)):
                    wid=widget['wid']
                    pid=widget['pid']
                    color=datapointconfig.data['color']
        response5=widgetapi.get_widget_config_request(passport=psp, wid=wid)
        self.assertEqual(response5.status, status.WEB_STATUS_OK)
        self.assertEqual(response5.data['type'],types.DATAPOINT)
        self.assertEqual(response5.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response5.data['pid'],pid)
        self.assertEqual(response5.data['wid'],wid)
        its=1
        ets=2
        username_to_share=self.username_to_share
        response6 = snapshotapi.new_snapshot_request(passport=psp,wid=wid,user_list=[username_to_share],ets=ets,its=its)
        self.assertEqual(response6.status, status.WEB_STATUS_OK)
        self.assertTrue(isinstance(uuid.UUID(response6.data['nid']),uuid.UUID))
        msgs=response6.imc_messages['unrouted']
        while len(msgs)>0:
            for msg in msgs:
                msgs.remove(msg)
                msgresponse=msgapi.process_message(msg)
                for msg2 in msgresponse.imc_messages['unrouted']:
                    msgs.append(msg2)
                self.assertEqual(msgresponse.status, imcstatus.IMC_STATUS_OK)
        #username_to_share should have access to the snapshot and datapoints
        psp_to_share = self.passport_share
        response7=snapshotapi.get_snapshot_config_request(passport=psp_to_share, nid=response6.data['nid'],tid=response6.data['tid'])
        self.assertEqual(response7.status, status.WEB_STATUS_OK)
        self.assertEqual(response7.data['nid'],response6.data['nid'])
        self.assertEqual(response7.data['type'],types.DATAPOINT)
        self.assertEqual(response7.data['widgetname'], '.'.join((datasourcename,datapointname)))
        self.assertEqual(response7.data['its'],1)
        self.assertEqual(response7.data['ets'],2)
        self.assertEqual(response7.data['datapoint'],{'pid':pid,'datapointname':'.'.join((datasourcename,datapointname)),'color':color})
        response8=datapointapi.get_datapoint_config_request(passport=psp_to_share, pid=pid)
        self.assertEqual(response8.status, status.WEB_STATUS_ACCESS_DENIED)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1',end_date='2',tid=response6.data['tid'])
        self.assertEqual(response9.status, status.WEB_STATUS_NOT_FOUND)
        response9=datapointapi.get_datapoint_data_request(passport=psp_to_share, pid=pid, start_date='1', end_date='2')
        self.assertEqual(response9.status, status.WEB_STATUS_ACCESS_DENIED)
        #request from other users should be denied
        psp_to_deny = passport.UserPassport(uid=uuid.uuid4(), sid=uuid.uuid4())
        response10=snapshotapi.get_snapshot_config_request(passport=psp_to_deny, nid=response6.data['nid'])
        self.assertEqual(response10.status, status.WEB_STATUS_ACCESS_DENIED)
        response11=datapointapi.get_datapoint_config_request(passport=psp_to_deny, pid=pid)
        self.assertEqual(response11.status, status.WEB_STATUS_ACCESS_DENIED)

