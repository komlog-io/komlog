import unittest
import uuid
import json
from komlog.komlibs.interface.imc.api import gestconsole
from komlog.komlibs.interface.imc.api import rescontrol
from komlog.komlibs.interface.imc.model import messages
from komlog.komlibs.interface.imc import status
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi


class InterfaceImcApiGestconsoleTest(unittest.TestCase):
    ''' komlibs.interface.imc.api.gestconsole tests '''

    def test_process_message_MONVAR_failure_non_existent_did(self):
        ''' process_message_MONVAR should fail if did does not exists '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_process_message_monvar_failure_invalid_uid_datapointname'
        message=messages.MonitorVariableMessage(uid=uid, did=did, date=date, position=position, length=length, datapointname=datapointname)
        response=gestconsole.process_message_MONVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_NEGVAR_failure_non_existent_datapoint(self):
        ''' process_message_NEGVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.NegativeVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_NEGVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_POSVAR_failure_non_existent_datapoint(self):
        ''' process_message_POSVAR should fail if datapoint does not exists '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        message=messages.PositiveVariableMessage(pid=pid, date=date, position=position, length=length)
        response=gestconsole.process_message_POSVAR(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_NEWDSW_failure_non_existent_user(self):
        ''' process_message_NEWDSW should fail if user does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        message=messages.NewDSWidgetMessage(uid=uid, did=did)
        response=gestconsole.process_message_NEWDSW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_NEWDPW_failure_non_existent_user(self):
        ''' process_message_NEWDPW should fail if user does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        message=messages.NewDPWidgetMessage(uid=uid, pid=pid)
        response=gestconsole.process_message_NEWDPW(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELUSER_failure_non_existent_user(self):
        ''' process_message_DELUSER should fail if user does not exist '''
        uid=uuid.uuid4()
        message=messages.DeleteUserMessage(uid=uid)
        response=gestconsole.process_message_DELUSER(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELAGENT_failure_non_existent_agent(self):
        ''' process_message_DELAGENT should fail if agent does not exist '''
        aid=uuid.uuid4()
        message=messages.DeleteAgentMessage(aid=aid)
        response=gestconsole.process_message_DELAGENT(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELAGENT_success(self):
        ''' process_message_DELAGENT should succeed if agent exists '''
        username='test_process_message_delagent_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delagent_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        message=messages.DeleteAgentMessage(aid=aid)
        response=gestconsole.process_message_DELAGENT(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),1)
        response=rescontrol.process_message_UPDQUO(response.get_msg_originated()[0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

    def test_process_message_DELDS_failure_non_existent_datasource(self):
        ''' process_message_DELDS should fail if datasource does not exist '''
        did=uuid.uuid4()
        message=messages.DeleteDatasourceMessage(did=did)
        response=gestconsole.process_message_DELDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELDS_success(self):
        ''' process_message_DELDS should succeed if datasource exists '''
        username='test_process_message_delds_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delds_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename=username
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=aid,datasourcename=datasourcename)
        message=messages.DeleteDatasourceMessage(did=datasource['did'])
        response=gestconsole.process_message_DELDS(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),1)
        response=rescontrol.process_message_UPDQUO(response.get_msg_originated()[0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

    def test_process_message_DELDP_failure_non_existent_datasource(self):
        ''' process_message_DELDP should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        message=messages.DeleteDatapointMessage(pid=pid)
        response=gestconsole.process_message_DELDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELDP_success(self):
        ''' process_message_DELDP should succeed if datapoint exists '''
        username='test_process_message_deldp_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_process_message_delds_success'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename=username
        datasource=datasourceapi.create_datasource(uid=user['uid'],aid=aid,datasourcename=datasourcename)
        datapointname=username
        color='#AAAAAA'
        datapoint=datapointapi.create_datapoint(did=datasource['did'], datapointname=datapointname, color=color)
        message=messages.DeleteDatapointMessage(pid=datapoint['pid'])
        response=gestconsole.process_message_DELDP(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),1)
        response=rescontrol.process_message_UPDQUO(response.get_msg_originated()[0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

    def test_process_message_DELWIDGET_failure_non_existent_widget(self):
        ''' process_message_DELWIDGET should fail if widget does not exist '''
        wid=uuid.uuid4()
        message=messages.DeleteWidgetMessage(wid=wid)
        response=gestconsole.process_message_DELWIDGET(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELWIDGET_success(self):
        ''' process_message_DELAWIDGET should succeed if widget exists '''
        username='test_process_message_delwidget_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        widgetname=username
        widget=widgetapi.new_widget_multidp(uid=user['uid'], widgetname=widgetname)
        message=messages.DeleteWidgetMessage(wid=widget['wid'])
        response=gestconsole.process_message_DELWIDGET(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),1)
        response=rescontrol.process_message_UPDQUO(response.get_msg_originated()[0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

    def test_process_message_DELDASHB_failure_non_existent_dashboard(self):
        ''' process_message_DELDASHB should fail if dashboard does not exist '''
        bid=uuid.uuid4()
        message=messages.DeleteDashboardMessage(bid=bid)
        response=gestconsole.process_message_DELDASHB(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_NOT_FOUND)

    def test_process_message_DELDASHB_success(self):
        ''' process_message_DELDASHB should succeed if widget exists '''
        username='test_process_message_deldashboard_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        dashboardname=username
        dashboard=dashboardapi.create_dashboard(uid=user['uid'],dashboardname=dashboardname)
        message=messages.DeleteDashboardMessage(bid=dashboard['bid'])
        response=gestconsole.process_message_DELDASHB(message=message)
        self.assertEqual(response.status, status.IMC_STATUS_OK)
        self.assertEqual(len(response.get_msg_originated()),1)
        response=rescontrol.process_message_UPDQUO(response.get_msg_originated()[0])
        self.assertEqual(response.status, status.IMC_STATUS_OK)

