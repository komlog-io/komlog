import unittest
import uuid
from komlibs.general.time import timeuuid
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.datapoint import api
from komlibs.gestaccount import exceptions
from komcass.model.orm import datapoint as ormdatapoint

class GestaccountDatapointApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datapoint.api tests '''
    
    def setUp(self):
        username='test_gestaccount.datapoint.api_user'
        password='password'
        email='test_gestaccount.datapoint.api_user@komlog.org'
        self.user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_gestaccount.datapoint.api_agent'
        pubkey='pubkey'
        version='Test Version'
        self.agent=agentapi.create_agent(username=self.user.username, agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='test_gestaccount.datapoint.api_datasource'
        self.datasource=datasourceapi.create_datasource(username=self.user.username, aid=self.agent.aid, datasourcename=datasourcename)

    def test_create_datapoint_non_existent_datasource(self):
        ''' create_datapoint should fail if datasource is not found in system '''
        did=uuid.uuid4()
        datapointname='Datapoint Name'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceNotFoundException,api.create_datapoint,did=did,datapointname=datapointname,position=position,length=length, date=date)

    def test_create_datapoint_success(self):
        ''' create_datapoint should succeed if datasource exists '''
        did=self.datasource.did
        datapointname='test_create_datapoint_success'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        datapoint=api.create_datapoint(did=did,datapointname=datapointname,position=position,length=length, date=date)
        self.assertIsInstance(datapoint, ormdatapoint.Datapoint)

    def test_get_datapoint_data_non_existent_datapoint(self):
        ''' get_datapoint_data should fail if pid is not in system '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=pid)

    def test_get_datapoint_data_no_data(self):
        ''' get_datapoint_data should fail if pid has no data in system '''
        did=self.datasource.did
        datapointname='test_get_datapoint_data_no_data'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        datapoint=api.create_datapoint(did=did,datapointname=datapointname,position=position,length=length, date=date)
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=datapoint.pid)

    def test_get_datapoint_config_non_existent_datapoint(self):
        ''' get_datapoint_config should fail if pid is not in system '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.get_datapoint_config, pid=pid)

    def test_get_datapoint_config_success(self):
        ''' get_datapoint_config should succeed if pid exists in system '''
        did=self.datasource.did
        datapointname='test_get_datapoint_config_success'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        datapoint=api.create_datapoint(did=did,datapointname=datapointname,position=position,length=length, date=date)
        data=api.get_datapoint_config(pid=datapoint.pid)
        self.assertIsInstance(data, dict)
    
    def test_update_datapoint_config_non_existent_datapoint(self):
        ''' update_datapoint_config should fail if datapoint is not in system '''
        pid=uuid.uuid4()
        data={'name':'test_update_datapoint_config_with_non_existent_datapoint'}
        self.assertRaises(exceptions.DatapointNotFoundException, api.update_datapoint_config, pid=pid, data=data)

    def test_update_datapoint_config_with_invalid_datapointname(self):
        ''' update_datapoint_config should fail if data has invalid datapointname'''
        pid=uuid.uuid4()
        datapointnames=[None,213123123,'Not Valid chars ÑÑÑÑ',{},['names','in array']]
        for name in datapointnames:
            data={'name':name}
            self.assertRaises(exceptions.BadParametersException, api.update_datapoint_config, pid=pid, data=data)

    def test_update_datapoint_config_with_invalid_color(self):
        ''' update_datapoint_config should fail if data has invalid color code'''
        pid=uuid.uuid4()
        datapointcolors=[None,213123123,'Not Valid chars ÑÑÑÑ',{},['colors','in array']]
        for color in datapointcolors:
            data={'color':color}
            self.assertRaises(exceptions.BadParametersException, api.update_datapoint_config, pid=pid, data=data)

    def test_update_datapoint_config_success(self):
        ''' update_datapoint_config should succeed if pid exists in system and params are OK '''
        did=self.datasource.did
        datapointname='test_update_datapoint_config_success'
        position='1'
        length='1'
        date=timeuuid.uuid1()
        datapoint=api.create_datapoint(did=did,datapointname=datapointname,position=position,length=length, date=date)
        data={'name':'test_update_datapoint_config_success_after_update', 'color':'#FFAA88'}
        self.assertTrue(api.update_datapoint_config(pid=datapoint.pid, data=data))
    
