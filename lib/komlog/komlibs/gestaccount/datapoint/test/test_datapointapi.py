import unittest
import uuid
import json
import decimal
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.ai.decisiontree import api as dtreeapi
from komlog.komlibs.ai import exceptions as aiexceptions
from komlog.komlibs.ai import errors as aierrors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.datasource import api as datasourceapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.datapoint import api
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komfig import logging

pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

class GestaccountDatapointApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datapoint.api tests '''

    def setUp(self):
        username='test_gestaccount.datapoint.api_user'
        password='password'
        email='test_gestaccount.datapoint.api_user@komlog.org'
        try:
            uid=userapi.get_uid(username=username)
        except Exception:
            user=userapi.create_user(username=username, password=password, email=email)
            uid=user['uid']
        finally:
            self.user=userapi.get_user_config(uid=uid)
        agentname='test_gestaccount.datapoint.api_agent'
        version='Test Version'
        try:
            self.agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        except Exception:
            agents=agentapi.get_agents_config(uid=self.user['uid'])
            for agent in agents:
                if agent['agentname']==agentname:
                    self.agent=agent
        datasourcename='test_gestaccount.datapoint.api_datasource.'+uuid.uuid1().hex
        self.datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)

    def test_create_user_datapoint_failure_invalid_uid(self):
        ''' create_user_datapoint should fail if uid is invalid '''
        uids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        datapoint_uri='test_create_user_datapoint_failure_invalid_uid'
        for uid in uids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
            self.assertEqual(cm.exception.error, Errors.E_GPA_CRUD_IU)

    def test_create_user_datapoint_failure_invalid_datapoint_uri(self):
        ''' create_user_datapoint should fail if datapoint uri is invalid '''
        uid=uuid.uuid4()
        datapoint_uris=[None,213123123,'Not Valid chars ÑÑÑÑ',{},['names','in array'],('a','tuple'), {'set'},{'a':'dict'},uuid.uuid4(), uuid.uuid1(), 23.23]
        for datapoint_uri in datapoint_uris:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
            self.assertEqual(cm.exception.error, Errors.E_GPA_CRUD_IDU)

    def test_create_user_datapoint_failure_user_not_found(self):
        ''' create_user_datapoint should fail if uid is not found '''
        uid=uuid.uuid4()
        datapoint_uri='test_create_user_datapoint_failure_user_not_found'
        with self.assertRaises(exceptions.UserNotFoundException) as cm:
            api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CRUD_UNF)

    def test_create_user_datapoint_success(self):
        ''' create_user_datapoint should succeed '''
        username='test_create_user_datapoint_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)

    def test_create_user_datapoint_failure_uri_already_exists(self):
        ''' create_user_datapoint should fail if selected uri already exists '''
        username='test_create_user_datapoint_failure_uri_already_exists'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        with self.assertRaises(exceptions.DatapointCreationException) as cm:
            api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CRUD_UAE)

    def test_create_datasource_datapoint_non_existent_datasource(self):
        ''' create_datasource_datapoint should fail if datasource is not found in system '''
        did=uuid.uuid4()
        datapointname='datapoint_name'
        self.assertRaises(exceptions.DatasourceNotFoundException,api.create_datasource_datapoint,did=did,datapoint_uri=datapointname)

    def test_create_datasource_datapoint_success(self):
        ''' create_datasource_datapoint should succeed if datasource exists '''
        did=self.datasource['did']
        datapointname='test_create_datasource_datapoint_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        self.assertIsInstance(datapoint, dict)
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],'.'.join((self.datasource['datasourcename'],datapointname)))
        self.assertFalse(datapoint['previously_existed'])

    def test_create_datasource_datapoint_success_uri_already_existed_by_user_datapoint(self):
        ''' create_datasource_datapoint should succeed if uri already existed and was a datapoint
        without associated datasource. The datapoint returned must be the already existing one
        which is now associated to the datasource too.
        '''
        username='test_create_datasource_datapoint_success_uri_already_existed_by_user_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='some_level.datasource_uri.some_level.datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        self.assertFalse('did' in datapoint)
        agentname='test_create_datasource_datapoint_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename='some_level.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        did=datasource['did']
        ds_datapoint_uri='some_level.datapoint_uri'
        ds_datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=ds_datapoint_uri)
        self.assertEqual(ds_datapoint['pid'],datapoint['pid'])
        self.assertEqual(ds_datapoint['uid'],datapoint['uid'])
        self.assertEqual(ds_datapoint['color'],datapoint['color'])
        self.assertEqual(ds_datapoint['datapointname'],datapoint['datapointname'])
        self.assertTrue(ds_datapoint['did'],did)
        self.assertTrue(ds_datapoint['previously_existed'])

    def test_create_datasource_datapoint_failure_uri_already_existed_by_something_other_than_datapoint(self):
        ''' create_datasource_datapoint should fail if uri already existed and was something other
        than a datapoint. In this case a datasource
        '''
        username='test_create_datasource_datapoint_failure_uri_already_existed_by_something_other_than_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        agentname='test_create_datasource_datapoint_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename1='some_level.datasource1_uri'
        datasource1=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename1)
        did1=datasource1['did']
        datasourcename2='some_level.datasource1_uri.some_level.datasource2_uri'
        datasource2=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename2)
        did2=datasource2['did']
        ds_datapoint_uri='some_level.datasource2_uri'
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            api.create_datasource_datapoint(did=did1,datapoint_uri=ds_datapoint_uri)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CRD_ADU)

    def test_create_datasource_datapoint_success_uri_already_existed_but_belonging_to_same_datasource(self):
        ''' create_datasource_datapoint should succeed if uri already existed and belongs to the same ds.
        In this case we return the same pid as the already existing datapoint.
        '''
        username='test_create_datasource_datapoint_success_uri_already_existed_with_same_ds'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='some_level.datasource_uri.some_level.datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        self.assertFalse('did' in datapoint)
        agentname='test_create_datasource_datapoint_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename='some_level.datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        did=datasource['did']
        ds_datapoint_uri='some_level.datapoint_uri'
        ds_datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=ds_datapoint_uri)
        self.assertEqual(ds_datapoint['pid'],datapoint['pid'])
        self.assertEqual(ds_datapoint['uid'],datapoint['uid'])
        self.assertEqual(ds_datapoint['color'],datapoint['color'])
        self.assertEqual(ds_datapoint['datapointname'],datapoint['datapointname'])
        self.assertTrue(ds_datapoint['did'],did)
        datapoint1 = api.create_datasource_datapoint(did=did,datapoint_uri=ds_datapoint_uri)
        self.assertEqual(datapoint1['pid'],datapoint['pid'])
        self.assertEqual(datapoint1['uid'],datapoint['uid'])
        self.assertEqual(datapoint1['color'],datapoint['color'])
        self.assertEqual(datapoint1['datapointname'],datapoint['datapointname'])
        self.assertTrue(datapoint1['did'],did)

    def test_create_datasource_datapoint_failure_uri_already_existed_but_belonging_to_different_datasource(self):
        ''' create_datasource_datapoint should succeed if uri already existed and belongs to the same ds.
        In this case we return the same pid as the already existing datapoint.
        '''
        username='test_create_datasource_datapoint_failure_uri_already_existed_with_diff_datasource'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        agentname='test_create_datasource_datapoint_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=uid, agentname=agentname, pubkey=pubkey, version=version)
        aid=agent['aid']
        datasourcename='datasource_uri'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        did=datasource['did']
        ds_datapoint_uri='intermediate_level.datapoint_uri'
        ds_datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=ds_datapoint_uri)
        self.assertTrue(isinstance(ds_datapoint['pid'],uuid.UUID))
        self.assertEqual(ds_datapoint['uid'],uid)
        self.assertEqual(ds_datapoint['datapointname'],'.'.join((datasourcename,ds_datapoint_uri)))
        self.assertTrue(ds_datapoint['did'],did)
        datasourcename2='datasource_uri.intermediate_level'
        datasource2=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename2)
        did2=datasource2['did']
        ds_datapoint_uri2='datapoint_uri'
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            ds_datapoint2=api.create_datasource_datapoint(did=did2,datapoint_uri=ds_datapoint_uri2)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CRD_AAD)

    def test_get_datapoint_data_invalid_pid(self):
        ''' get_datapoint_data should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        its=timeuuid.uuid1(seconds=10)
        ets=timeuuid.uuid1(seconds=20)
        count=100
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_data(pid=pid, fromdate=its, todate=ets, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDD_IP)

    def test_get_datapoint_data_invalid_todate(self):
        ''' get_datapoint_data should fail if todate is invalid '''
        todates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        fromdate=timeuuid.uuid1(seconds=10)
        count=100
        for todate in todates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_data(pid=pid, fromdate=fromdate, todate=todate, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDD_ITD)

    def test_get_datapoint_data_invalid_fromdate(self):
        ''' get_datapoint_data should fail if fromdate is invalid '''
        fromdates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        todate=timeuuid.uuid1(seconds=10)
        count=100
        for fromdate in fromdates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_data(pid=pid, fromdate=fromdate, todate=todate, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDD_IFD)

    def test_get_datapoint_data_invalid_count(self):
        ''' get_datapoint_data should fail if count is invalid '''
        counts=['asdfasd',234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        todate=timeuuid.uuid1(seconds=20)
        fromdate=timeuuid.uuid1(seconds=10)
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_data(pid=pid, fromdate=fromdate, todate=todate, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDD_ICNT)

    def test_get_datapoint_data_non_existent_datapoint(self):
        ''' get_datapoint_data should fail if pid is not in system '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=pid)

    def test_get_datapoint_data_no_data(self):
        ''' get_datapoint_data should fail if pid has no data in system '''
        did=self.datasource['did']
        datapointname='test_get_datapoint_data_no_data'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=datapoint['pid'])

    def test_get_datapoint_data_success_user_datapoint_some_data(self):
        ''' get_datapoint_data should return the data found '''
        username='test_get_datapoint_data_success_user_datapoint_some_data'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        datapoint_data=(
            (timeuuid.uuid1(seconds=1),'1'),
            (timeuuid.uuid1(seconds=2),'2'),
            (timeuuid.uuid1(seconds=3),'3'),
            (timeuuid.uuid1(seconds=4),'4'),
            (timeuuid.uuid1(seconds=5),'5'),
            (timeuuid.uuid1(seconds=6),'6'),
            (timeuuid.uuid1(seconds=7),'7'),
            (timeuuid.uuid1(seconds=8),'8'),
            (timeuuid.uuid1(seconds=9),'9'),
            (timeuuid.uuid1(seconds=10),'10')
        )
        for date, content in datapoint_data:
            self.assertTrue(api.store_user_datapoint_value(pid=datapoint['pid'],date=date, content=content))
        db_data=api.get_datapoint_data(pid=datapoint['pid'])
        self.assertEqual(len(db_data), 10)
        db_data=api.get_datapoint_data(pid=datapoint['pid'], count=1)
        self.assertEqual(len(db_data), 1)
        self.assertEqual(db_data[0]['value'], decimal.Decimal(10))
        fromdate=timeuuid.uuid1(seconds=20)
        todate=timeuuid.uuid1(seconds=30)
        with self.assertRaises(exceptions.DatapointDataNotFoundException) as cm:
            api.get_datapoint_data(pid=datapoint['pid'], fromdate=fromdate, todate=todate)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDD_DDNF)
        self.assertEqual(cm.exception.last_date, fromdate)

    def test_get_datapoint_config_failure_invalid_pid(self):
        ''' get_datapoint_config should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_config(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDC_IP)

    def test_get_datapoint_config_non_existent_datapoint(self):
        ''' get_datapoint_config should fail if pid is not in system '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.get_datapoint_config(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDC_DNF)

    def test_get_datapoint_config_success(self):
        ''' get_datapoint_config should succeed if pid exists in system '''
        did=self.datasource['did']
        datapointname='test_get_datapoint_config_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        data=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertIsInstance(data, dict)
        self.assertEqual(data['did'],did)
        self.assertEqual(data['datapointname'],'.'.join((self.datasource['datasourcename'],datapointname)))

    def test_get_datapoint_config_success_user_datapoint(self):
        ''' get_datapoint_config should return the datapoint config '''
        username='test_get_datapoint_config_success_user_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        dp_config=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(dp_config['pid'],datapoint['pid'])
        self.assertEqual(dp_config['uid'],user['uid'])
        self.assertEqual(dp_config['did'],None)
        self.assertEqual(dp_config['datapointname'],datapoint_uri)
        self.assertTrue('color' in dp_config)
        self.assertFalse('decimalseparator' in dp_config)
        self.assertFalse('wid' in dp_config)

    def test_update_datapoint_config_failure_invalid_pid(self):
        ''' update_datapoint_config should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datapoint_config(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_UDC_IP)

    def test_update_datapoint_config_failure_invalid_datapointname(self):
        ''' update_datapoint_config should fail if datapointname is invalid '''
        names=['Invalid ÑÑ chars',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4()]
        pid=uuid.uuid4()
        for datapointname in names:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datapoint_config(pid=pid, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_UDC_IDN)

    def test_update_datapoint_config_failure_invalid_color(self):
        ''' update_datapoint_config should fail if color is invalid '''
        colors=[234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4()]
        pid=uuid.uuid4()
        for color in colors:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datapoint_config(pid=pid, color=color)
            self.assertEqual(cm.exception.error, Errors.E_GPA_UDC_IC)

    def test_update_datapoint_config_failure_nothing_to_update(self):
        ''' update_datapoint_config should fail if not color nor datapointname is passed'''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.BadParametersException) as cm:
            api.update_datapoint_config(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_UDC_EMP)

    def test_update_datapoint_config_non_existent_datapoint(self):
        ''' update_datapoint_config should fail if datapoint is not in system '''
        pid=uuid.uuid4()
        datapointname='test_update_datapoint_config_with_non_existent_datapoint'
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.update_datapoint_config(pid=pid,datapointname=datapointname)
        self.assertEqual(cm.exception.error, Errors.E_GPA_UDC_DNF)

    def test_update_datapoint_config_success(self):
        ''' update_datapoint_config should succeed if pid exists in system and params are OK '''
        did=self.datasource['did']
        datapointname='test_update_datapoint_config_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        datapointname='test_update_datapoint_config_success_after_update'
        color='#FFAA88'
        self.assertTrue(api.update_datapoint_config(pid=datapoint['pid'], datapointname=datapointname, color=color))

    def test_update_datapoint_config_success_user_datapoint(self):
        ''' update_datapoint_config should succeed if pid exists in system and params are OK '''
        username='test_update_datapoint_config_success_user_datapoint'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        datapoint_config=api.get_datapoint_config(pid=datapoint['pid'])
        new_color='#DDFFCC'
        self.assertTrue(api.update_datapoint_config(pid=datapoint['pid'], color=new_color))
        datapoint_config=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint_config['color'],new_color)
        new_datapointname='new_datapoint_uri'
        self.assertTrue(api.update_datapoint_config(pid=datapoint['pid'],datapointname=new_datapointname))
        datapoint_config=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint_config['datapointname'],new_datapointname)
        new_color='#99FFCC'
        new_datapointname='new_datapoint_uri2'
        self.assertTrue(api.update_datapoint_config(pid=datapoint['pid'],color=new_color,datapointname=new_datapointname))
        datapoint_config=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertEqual(datapoint_config['color'],new_color)
        self.assertEqual(datapoint_config['datapointname'],new_datapointname)

    def test_mark_negative_variable_failure_invalid_pid(self):
        ''' mark_negative_variable should fail if pid is not valid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        position=1
        length=1
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_negative_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_IP)

    def test_mark_negative_variable_failure_invalid_date(self):
        ''' mark_negative_variable should fail if date is not valid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_negative_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_IDT)

    def test_mark_negative_variable_failure_invalid_position(self):
        ''' mark_negative_variable should fail if position is not valid '''
        positions=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        pid=uuid.uuid4()
        date=uuid.uuid1()
        length=1
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_negative_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_IPO)

    def test_mark_negative_variable_failure_invalid_length(self):
        ''' mark_negative_variable should fail if length is not valid '''
        lenghts=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        pid=uuid.uuid4()
        position=1
        for length in lenghts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_negative_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_IL)

    def test_mark_negative_variable_failure_non_existent_datapoint(self):
        ''' mark_negative_variable should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.mark_negative_variable(pid=pid, date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_DNF)

    def test_mark_negative_variable_failure_unsupported_operation(self):
        ''' mark_negative_variable should fail if the datapoint is not associated
            to any datasource '''
        username='test_mark_negative_variable_failure_unsupported_operation'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_DSNF)

    def test_mark_negative_variable_failure_no_variables_in_datasource_map(self):
        ''' mark_negative_variable should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_no_variables_in_datasource_map'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_DMNF)

    def test_mark_negative_variable_failure_invalid_variable_length(self):
        ''' mark_negative_variable should fail if variable length does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_invalid_variable_length'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=1
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_VLNF)

    def test_mark_negative_variable_failure_invalid_variable_position(self):
        ''' mark_negative_variable should fail if variable position does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_invalid_variable_position'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=46
        length=2
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MNV_VPNF)

    def test_mark_negative_variable_success_no_positive_left_dp_will_not_be_identified(self):
        ''' mark_negative_variable should succeed '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [])
        self.assertEqual(mark_result['no_positive_tr_set'], [datapointname])
        self.assertIsNotNone(mark_result['dtree'])
        #the dtree should not be generated twice if no change detected
        mark_result=api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [])
        self.assertFalse('conflicts' in mark_result)
        self.assertFalse('classified' in mark_result)
        self.assertFalse('no_positive_tr_set' in mark_result)
        self.assertFalse('dtree' in mark_result)

    def test_mark_negative_variable_success_positive_left_dp_will_be_added_to_dtree(self):
        ''' mark_negative_variable should succeed '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        date2 = timeuuid.uuid1()
        content='this var 11 is not the dp'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date2))
        position=9
        length=2
        mark_result=api.mark_negative_variable(pid=datapoint['pid'], date=date2, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint['pid'], date=date))
        self.assertEqual(cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'], date=date),[])
        self.assertIsNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint['pid'], date=date2))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_negative(pid=datapoint['pid'], date=date2, position=position))

    def test_mark_negative_variable_success_dont_update_dtree(self):
        ''' mark_negative_variable should succeed and return the pid list of modified datapoints without updating decision trees '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_success_dont_update_dtree'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length, dtree_update=False)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [did])
        self.assertFalse('conflicts' in mark_result)
        self.assertFalse('classified' in mark_result)
        self.assertFalse('no_positive_tr_set' in mark_result)
        self.assertFalse('dtree' in mark_result)
        #the dtree should not be generated twice if no change detected
        mark_result=api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [])
        self.assertFalse('conflicts' in mark_result)
        self.assertFalse('classified' in mark_result)
        self.assertFalse('no_positive_tr_set' in mark_result)
        self.assertFalse('dtree' in mark_result)

    def test_mark_positive_variable_failure_invalid_pid(self):
        ''' mark_positive_variable should fail if pid is not valid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        position=1
        length=1
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_positive_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_IP)

    def test_mark_positive_variable_failure_invalid_date(self):
        ''' mark_positive_variable should fail if date is not valid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_positive_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_IDT)

    def test_mark_positive_variable_failure_invalid_position(self):
        ''' mark_positive_variable should fail if position is not valid '''
        positions=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        pid=uuid.uuid4()
        date=uuid.uuid1()
        length=1
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_positive_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_IPO)

    def test_mark_positive_variable_failure_invalid_length(self):
        ''' mark_positive_variable should fail if length is not valid '''
        lenghts=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        pid=uuid.uuid4()
        position=1
        for length in lenghts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_positive_variable(pid=pid, date=date, position=position, length=length)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_IL)

    def test_mark_positive_variable_failure_non_existent_datapoint(self):
        ''' mark_positive_variable should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.mark_positive_variable(pid=pid, date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_DNF)

    def test_mark_positive_variable_failure_unsupported_operation(self):
        ''' mark_positive_variable should fail if the datapoint is not associated
            to any datasource '''
        username='test_mark_positive_variable_failure_unsupported_operation'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_DSNF)

    def test_mark_positive_variable_failure_no_variables_in_datasource_map(self):
        ''' mark_positive_variable should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_no_variables_in_datasource_map'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_DMNF)

    def test_mark_positive_variable_failure_invalid_variable_length(self):
        ''' mark_positive_variable should fail if variable length does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_invalid_variable_length'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_positive_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=1
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_VLNF)

    def test_mark_positive_variable_failure_invalid_variable_position(self):
        ''' mark_positive_variable should fail if variable position does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_invalid_variable_position'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=46
        length=2
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_VPNF)

    def test_mark_positive_variable_success_no_other_datapoint_matched(self):
        ''' mark_positive_variable should succeed in this case, no other datapoint matched '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_success_no_other_datapoint_matched_dp'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])

    def test_mark_positive_variable_success_one_other_datapoint_matched(self):
        ''' mark_positive_variable should succeed if other datapoint matched '''
        datasourcename='test_mark_positive_variable_success_one_other_datapoint_matched_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_positive_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        datapoints_to_update=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        dsdata=datasourceapi.get_mapped_datasource_data(did=did, fromdate=date, todate=date)
        dsdatapoints=dsdata[0]['datapoints']
        self.assertTrue(len(dsdatapoints),1)
        self.assertEqual(dsdatapoints[0]['pid'],datapoint['pid'])
        self.assertEqual(dsdatapoints[0]['position'],position)
        datapointname2='test_mark_positive_variable_success_one_other_datapoint_matched_2'
        datapoint2=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname2)
        mark_result=api.mark_positive_variable(pid=datapoint2['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname2])
        self.assertEqual(mark_result['no_positive_tr_set'], [datapointname])
        self.assertIsNotNone(mark_result['dtree'])
        self.assertIsNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint['pid'], date=date))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_negative(pid=datapoint['pid'], date=date, position=position))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint2['pid'], date=date))
        self.assertIsNone(cassapidatapoint.get_datapoint_dtree_negative(pid=datapoint2['pid'], date=date, position=position))

    def test_mark_positive_variable_success_one_other_datapoint_matched_dont_update_dtrees(self):
        ''' mark_positive_variable should succeed if other datapoint matched and return the modified datapoints without updating their dtrees '''
        datasourcename='test_mark_positive_variable_success_one_other_datapoint_matched_datasource_dont_update_dtrees'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_positive_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        datapoints_to_update=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length, dtree_update=False)
        dsdata=datasourceapi.get_mapped_datasource_data(did=did, fromdate=date, todate=date)
        dsdatapoints=dsdata[0]['datapoints']
        self.assertTrue(len(dsdatapoints),1)
        self.assertEqual(dsdatapoints[0]['pid'],datapoint['pid'])
        self.assertEqual(dsdatapoints[0]['position'],position)
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched_2'
        datapoint2=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        mark_result=api.mark_positive_variable(pid=datapoint2['pid'], date=date, position=position, length=length, dtree_update=False)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [did])
        self.assertFalse('conflicts' in mark_result)
        self.assertFalse('classified' in mark_result)
        self.assertFalse('no_positive_tr_set' in mark_result)
        self.assertFalse('dtree' in mark_result)
        self.assertIsNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint['pid'], date=date))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_negative(pid=datapoint['pid'], date=date, position=position))
        self.assertIsNotNone(cassapidatapoint.get_datapoint_dtree_positive(pid=datapoint2['pid'], date=date))
        self.assertIsNone(cassapidatapoint.get_datapoint_dtree_negative(pid=datapoint2['pid'], date=date, position=position))

    def test_mark_positive_variable_failure_generating_dtree_ambiguous_positives(self):
        ''' mark_positive_variable should fail generating dtree if ambigous information is found in positives and negatives of this datapoint '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_generating_dtree_ambiguous_positives'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='x: 1, y: 0'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first we say datapoint is x value
        position=3
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        date2=timeuuid.uuid1()
        content='x: 1, y: 0'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date2))
        #now we say datapoint is y value
        position=9
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date2, position=position, length=length)
        self.assertEqual(mark_result['conflicts'][0]['uri'], datapointname)
        self.assertEqual(mark_result['conflicts'][0]['pid'], datapoint['pid'])
        self.assertEqual(mark_result['conflicts'][0]['dates'], sorted([date,date2]))
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [did])
        self.assertEqual(mark_result['no_positive_tr_set'],[])
        self.assertEqual(mark_result['dtree'],None)

    def test_mark_positive_variable_failure_generating_dtree_ambiguous_positives_dont_update_dtrees(self):
        ''' mark_positive_variable should fail generating dtree if ambigous information is found in positives and negatives of this datapoint. This fail will not be reported in mark function if dtree_update is False. '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_generating_dtree_ambiguous_positives_dont_update_dtrees'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='x: 1, y: 0'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first we say datapoint is x value
        position=3
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        date2=timeuuid.uuid1()
        content='x: 1, y: 0'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date2))
        #now we say datapoint is y value
        position=9
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date2, position=position, length=length, dtree_update=False)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [did])
        self.assertFalse('conflicts' in mark_result)
        self.assertFalse('classified' in mark_result)
        self.assertFalse('no_positive_tr_set' in mark_result)
        self.assertFalse('dtree' in mark_result)
        dtree_info = api.generate_decision_tree(did=did)
        self.assertEqual(dtree_info['dtree'],None)
        self.assertEqual(dtree_info['conflicts'][0]['uri'], datapointname)
        self.assertEqual(dtree_info['conflicts'][0]['pid'], datapoint['pid'])
        self.assertEqual(dtree_info['conflicts'][0]['dates'], sorted([date,date2]))

    def test_mark_missing_datapoint_failure_invalid_pid(self):
        ''' mark_missing_datapoint should fail if pid is not valid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        position=1
        length=1
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_missing_datapoint(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_IP)

    def test_mark_missing_datapoint_failure_invalid_date(self):
        ''' mark_missing_datapoint should fail if date is not valid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        position=1
        length=1
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.mark_missing_datapoint(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_IDT)

    def test_mark_missing_datapoint_failure_non_existent_datapoint(self):
        ''' mark_missing_datapoint should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.mark_missing_datapoint(pid=pid, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_DNF)

    def test_mark_missing_datapoint_failure_unsupported_operation(self):
        ''' mark_missing_datapoint should fail if the datapoint is not associated
            to any datasource '''
        username='test_mark_missing_datapoint_failure_unsupported_operation'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_DSNF)

    def test_mark_missing_datapoint_failure_no_variables_in_datasource_map(self):
        ''' mark_missing_datapoint should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_missing_datapoint_failure_no_variables_in_datasource_map'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_DMNF)

    def test_mark_missing_datapoint_success_no_positive_tr_set(self):
        ''' mark_missing_datapoint should succeed. However if datapoint loses all its positive samples,
            the dtree will be generated without it, because we have no way to identify the datapoint. '''
        did=self.datasource['did']
        datapointname='test_mark_missing_datapoint_success'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_missing_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),1)
        self.assertEqual(positives[0].pid,datapoint['pid'])
        self.assertEqual(positives[0].date,date)
        self.assertEqual(positives[0].position,position)
        self.assertEqual(positives[0].length,length)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),0)
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [])
        self.assertEqual(mark_result['no_positive_tr_set'], [datapointname]) # we only have negative tr set.
        self.assertIsNotNone(mark_result['dtree'])
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),0)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),3)
        #if no info has been modified, dtree should not be recalculated
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(mark_result,{'updated':[],'pending':[]})

    def test_mark_missing_datapoint_success_positives_remaining(self):
        ''' mark_missing_datapoint should succeed. '''
        did=self.datasource['did']
        datapointname='test_mark_missing_datapoint_success_positives_remaining'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_missing_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),1)
        self.assertEqual(positives[0].pid,datapoint['pid'])
        self.assertEqual(positives[0].date,date)
        self.assertEqual(positives[0].position,position)
        self.assertEqual(positives[0].length,length)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),0)
        date2=timeuuid.uuid1()
        content='in this content, the datapoint 23 identified before, des not appear'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date2))
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date2)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),1)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),1)
        #if no info has been modified, dtree should not be recalculated
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date2)
        self.assertEqual(mark_result,{'updated':[],'pending':[]})

    def test_mark_missing_datapoint_success_dont_update_dtree(self):
        ''' mark_missing_datapoint should succeed and return the did in the pending list '''
        did=self.datasource['did']
        datapointname='test_mark_missing_datapoint_success_dont_update_dtree'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='mark_missing_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),1)
        self.assertEqual(positives[0].pid,datapoint['pid'])
        self.assertEqual(positives[0].date,date)
        self.assertEqual(positives[0].position,position)
        self.assertEqual(positives[0].length,length)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),0)
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date, dtree_update=False)
        self.assertEqual(mark_result,{'updated':[],'pending':[did]})
        positives=cassapidatapoint.get_datapoint_dtree_positives(pid=datapoint['pid'])
        self.assertEqual(len(positives),0)
        negatives=cassapidatapoint.get_datapoint_dtree_negatives(pid=datapoint['pid'])
        self.assertEqual(len(negatives),3)
        #if no info has been modified, dtree should not be recalculated
        mark_result=api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(mark_result['updated'], [])
        self.assertEqual(mark_result['pending'], [])

    def test_generate_decision_tree_failure_invalid_did(self):
        ''' generate_tree should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_decision_tree(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDT_IDID)

    def test_generate_decision_tree_failure_non_existent_datasource(self):
        ''' generate_decision_tree should fail if did does not exists '''
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.generate_decision_tree(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDT_DSNF)

    def test_generate_decision_tree_success_no_datapoint_to_generate_for(self):
        ''' generate_decision_tree should succeed, but generating nothing if ds has no datapoints '''
        datasourcename='test_generate_decision_tree_failure_no_training_set_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        result = api.generate_decision_tree(did=did)
        self.assertEqual(result['classified'],[])
        self.assertEqual(result['dtree'],None)

    def test_generate_decision_tree_failure_training_set_empty(self):
        ''' generate_decision_tree should fail if training set is empty '''
        datasourcename='test_generate_decision_tree_failure_training_set_empty'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_decision_tree_success_datapoint'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointDTreeTrainingSetEmptyException) as cm:
            result = api.generate_decision_tree(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDT_ETS)

    def test_generate_decision_tree_success(self):
        ''' generate_decision_tree should succeed if ds exists and has datapoints '''
        datasourcename='test_generate_decision_tree_success_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_decision_tree_success_datapoint'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        content='generate_decision_tree content with ññ€#@hrññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 50 and length 2
        position=50
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length,dtree_update=False)
        self.assertEqual(mark_result,{'updated':[],'pending':[did]})
        result = api.generate_decision_tree(did=did)
        self.assertEqual(result['classified'],[datapointname])
        self.assertIsNotNone(result['dtree'])
        s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=did)
        dtree = dtreeapi.load_dtree(s_dtree)
        dshashes=cassapidatasource.get_datasource_hashes(did=did, fromdate=date, todate=date)
        self.assertEqual(len(dshashes),1)
        for dshash in dshashes:
            text_hash=json.loads(dshash.content)
            variables_atts=textmanvar.get_variables_atts(text_hash)
            for var in variables_atts:
                result = dtree.classify(var['atts'])
                if var['text_pos']!=position:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result,{datapointname:1})

    def test_generate_decision_tree_failure_error_in_generation(self):
        ''' generate_decision_tree should fail if dtree generation fails '''
        datasourcename='test_generate_decision_tree_failure_error_in_generation'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_decision_tree_success_datapoint'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        content='x: 1, y: 2'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #we say datapoint is x in this sample
        position=3
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length,dtree_update=False)
        self.assertEqual(mark_result,{'updated':[],'pending':[did]})
        result = api.generate_decision_tree(did=did)
        self.assertEqual(result['classified'],[datapointname])
        date2=timeuuid.uuid1()
        content='x: 1, y: 2'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date2))
        #but now, we say datapoint is y
        position=9
        length=1
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date2, position=position, length=length, dtree_update=False)
        #error has arised already marking it positive
        #self.assertEqual(mark_result,{'conflicts':[datapointname],'updated':[],'pending':[did]})
        #generating again fails
        dtree_info = api.generate_decision_tree(did=did)
        self.assertEqual(dtree_info['dtree'],None)
        self.assertEqual(dtree_info['conflicts'][0]['uri'], datapointname)
        self.assertEqual(dtree_info['conflicts'][0]['pid'], datapoint['pid'])
        self.assertEqual(dtree_info['conflicts'][0]['dates'], sorted([date,date2]))

    def test_monitor_new_datapoint_failure_invalid_did(self):
        ''' monitor_new_datapoint should fail if did is not valid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=uuid.uuid1()
        position=1
        length=1
        datapointname = 'test_monitor_new_datapoint_failure_invalid_did'
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MND_ID)

    def test_monitor_new_datapoint_failure_invalid_date(self):
        ''' monitor_new_datapoint should fail if date is not valid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        did=uuid.uuid4()
        position=1
        length=1
        datapointname = 'datapointname'
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MND_IDT)

    def test_monitor_new_datapoint_failure_invalid_position(self):
        ''' monitor_new_datapoint should fail if position is not valid '''
        positions=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        did=uuid.uuid4()
        date =timeuuid.uuid1()
        length=1
        datapointname = 'datapointname'
        for position in positions:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MND_IPO)

    def test_monitor_new_datapoint_failure_invalid_length(self):
        ''' monitor_new_datapoint should fail if length is not valid '''
        lengths=['asdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        did=uuid.uuid4()
        date =timeuuid.uuid1()
        position=1
        datapointname = 'datapointname'
        for length in lengths:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MND_IL)

    def test_monitor_new_datapoint_failure_invalid_datapointname(self):
        ''' monitor_new_datapoint should fail if datapointname is not valid '''
        datapointnames=['aññsdfasd',-234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4()]
        did=uuid.uuid4()
        date =timeuuid.uuid1()
        position=1
        length=1
        for datapointname in datapointnames:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MND_IDN)

    def test_monitor_new_datapoint_failure_datasource_data_not_found(self):
        ''' monitor_new_datapoint should fail if datasource data does not exist '''
        datasourcename='test_monitor_new_datapoint_failure_datasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_monitor_new_datapoint_failure_variable_position'
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.monitor_new_datapoint(did, date, position, length, datapointname)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_DMNF)

    def test_monitor_new_datapoint_failure_variable_does_not_exist_invalid_length(self):
        ''' monitor_new_datapoint should fail if selected variable does not exist '''
        datasourcename='test_monitor_new_datapoint_failure_variable_does_not_exists_length_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=4
        datapointname='test_monitor_new_datapoint_failure_variable_length'
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.monitor_new_datapoint(did, date, position, length, datapointname)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_VLNF)

    def test_monitor_new_datapoint_failure_variable_does_not_exist_invalid_position(self):
        ''' monitor_new_datapoint should fail if selected variable does not exist '''
        datasourcename='test_monitor_new_datapoint_failure_variable_does_not_exists_position_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=45
        length=2
        datapointname='test_monitor_new_datapoint_failure_variable_position'
        with self.assertRaises(exceptions.DatasourceVariableNotFoundException) as cm:
            api.monitor_new_datapoint(did, date, position, length, datapointname)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MPV_VPNF)

    def test_monitor_new_datapoint_success(self):
        ''' monitor_new_datapoint should succeed if stars alineate '''
        datasourcename='test_monitor_new_datapoint_success'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=2
        datapointname='test_monitor_new_datapoint_success'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(isinstance(datapoint,dict))
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],'.'.join((datasourcename,datapointname)))
        self.assertTrue(isinstance(datapoint['pid'],uuid.UUID))
        self.assertFalse(datapoint['previously_existed'])

    def test_monitor_new_datapoint_failure_uri_already_existed_with_different_datasource(self):
        ''' monitor_new_datapoint should fail if dp is associated to a different datasource '''
        datasourcename='test_monitor_new_datapoint_failure_uri_already_existed_with_different_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=2
        datapointname='intermediate_level.test_monitor_new_datapoint_success'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(isinstance(datapoint,dict))
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],'.'.join((datasourcename,datapointname)))
        self.assertTrue(isinstance(datapoint['pid'],uuid.UUID))
        self.assertFalse(datapoint['previously_existed'])
        datasourcename='test_monitor_new_datapoint_failure_uri_already_existed_with_different_datasource.intermediate_level'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=2
        datapointname='test_monitor_new_datapoint_success'
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CRD_AAD)

    def test_monitor_new_datapoint_success_uri_already_existed_with_same_datasource(self):
        ''' monitor_new_datapoint should succeed if dp is associated to the same datasource '''
        datasourcename='tert_monitor_new_datapoint_success_uri_already_existed_with_same_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=2
        datapointname='intermediate_level.test_monitor_new_datapoint_success'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(isinstance(datapoint,dict))
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],'.'.join((datasourcename,datapointname)))
        self.assertTrue(isinstance(datapoint['pid'],uuid.UUID))
        self.assertFalse(datapoint['previously_existed'])
        datapoint2=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(isinstance(datapoint2,dict))
        self.assertEqual(datapoint2['did'],did)
        self.assertEqual(datapoint2['datapointname'],'.'.join((datasourcename,datapointname)))
        self.assertEqual(datapoint2['pid'],datapoint['pid'])
        self.assertTrue(datapoint2['previously_existed'])

    def test_monitor_new_datapoint_success_previously_existed_with_no_associated_datasource(self):
        ''' monitor_new_datapoint should succeed if we try to associate a datasource to an
            existing user datapoint not associated yet '''

        datasourcename='test_monitor_new_datapoint_success_previously_existed_with_no_associated_ds'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        datapoint_uri=datasourcename+'.test_monitor_new_datapoint_success_previously_existed_dp'
        datapoint=api.create_user_datapoint(uid=self.user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        #second var should be a position 44 and length 2
        position=47
        length=2
        datapointname='test_monitor_new_datapoint_success_previously_existed_dp'
        dsdatapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(isinstance(datapoint,dict))
        self.assertEqual(dsdatapoint['did'],did)
        self.assertEqual(dsdatapoint['datapointname'],datapoint_uri)
        self.assertTrue(isinstance(dsdatapoint['pid'],uuid.UUID))
        self.assertEqual(dsdatapoint['pid'],datapoint['pid'])
        self.assertTrue(dsdatapoint['previously_existed'])

    def test_store_user_datapoint_value_failure_invalid_pid(self):
        ''' store_user_datapoint_values should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=timeuuid.uuid1()
        content='333'
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_user_datapoint_value(pid=pid, date=date, content=content)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPSV_IP)

    def test_store_user_datapoint_value_failure_invalid_date(self):
        ''' store_user_datapoint_values should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        content='333'
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_user_datapoint_value(pid=pid, date=date, content=content)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPSV_IDT)

    def test_store_user_datapoint_value_failure_invalid_content(self):
        ''' store_user_datapoint_values should fail if content is invalid '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        contents=[{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4()]
        for content in contents:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_user_datapoint_value(pid=pid, date=date, content=content)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPSV_IC)
        contents=['NaN','Infinity','-Infinity']
        for content in contents:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_user_datapoint_value(pid=pid, date=date, content=content)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPSV_IC)

    def test_store_user_datapoint_value_failure_datapoint_not_found(self):
        ''' store_user_datapoint_values should fail if datapoint is not found '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        content='44.3'
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.store_user_datapoint_value(pid=pid, date=date, content=content)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDPSV_DNF)

    def test_store_user_datapoint_value_success(self):
        ''' store_user_datapoint_values should fail if datapoint is not found '''
        datapoint_uri='test_store_user_datapoint_value_success'
        datapoint=api.create_user_datapoint(uid=self.user['uid'], datapoint_uri=datapoint_uri)
        pid=datapoint['pid']
        contents=['22','22.2','-33.3','1e6']
        for content in contents:
            date=timeuuid.uuid1()
            self.assertTrue(api.store_user_datapoint_value(pid=pid, date=date, content=content))

    def test_store_datapoint_values_failure_invalid_pid(self):
        ''' store_datapoint_values should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_datapoint_values(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPV_IP)

    def test_store_datapoint_values_failure_invalid_date(self):
        ''' store_datapoint_values should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.store_datapoint_values(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDPV_IDT)

    def test_store_datapoint_values_failure_datapoint_not_found(self):
        ''' store_datapoint_values should fail if datapoint is not found '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatapointNotFoundException, api.store_datapoint_values, pid=pid, date=date)

    def test_store_datapoint_values_failure_unsupported_operation(self):
        ''' store_datapoint_values should fail if we try to execute the function over
            an user datapoint that is not associated to any datasource '''
        username='test_store_datapoint_values_failure_unsupported_operation'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=user['uid'], datapoint_uri=datapoint_uri)
        self.assertIsNotNone(datapoint)
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointUnsupportedOperationException) as cm:
            api.store_datapoint_values(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDPV_DSNF)

    def test_store_datapoint_values_failure_dtree_not_found(self):
        ''' store_datapoint_values should fail if datapoint dtree is not found '''
        did=self.datasource['did']
        datapointname='test_store_datapoint_values_failure_dtree_not_found_datapoint'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointDTreeNotFoundException) as cm:
            api.store_datapoint_values(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDPV_DTNF)

    def test_store_datapoint_values_success_no_data_found_in_interval(self):
        ''' store_datapoint_values should do nothing if no data is selected in the requested interval  '''
        datasourcename='test_store_datapoint_values_success_no_data_stored'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datapoint_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        position=31
        length=2
        datapointname='test_store_datapoint_values_failure_datasource_map_not_found_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datapoint_values(pid=datapoint['pid'], date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)+600)))

    def test_store_datapoint_values_success(self):
        ''' store_datapoint_values should succeed '''
        datasourcename='test_store_datapoint_values_success'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        init_date=timeuuid.uuid1()
        content='store_datapoint_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=init_date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=init_date))
        for i in range(1,60):
            date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(init_date)+i)
            self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
            self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 31 and length 2
        position=31
        length=2
        datapointname='test_store_datapoint_values_success'
        datapoint=api.monitor_new_datapoint(did=did, date=init_date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datapoint_values(pid=datapoint['pid'], date=init_date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=init_date, todate=date)
        self.assertEqual(len(data),60)

    def test_store_datasource_values_failure_datasource_not_found(self):
        ''' store_datasource_values should fail if datasource does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.store_datasource_values( did=did, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDSV_DSNF)

    def test_store_datasource_values_datasource_has_no_dtree(self):
        ''' store_datasource_values should return if it does not have a dtree '''
        datasourcename='test_store_datasource_values_datasource_has_no_dtree'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        store_info = api.store_datasource_values(did=did, date=date)
        self.assertEqual(store_info['dp_missing'],[])
        self.assertEqual(store_info['dp_found_twice'],[])
        self.assertEqual(store_info['non_dp_uris'],[])
        self.assertEqual(store_info['dp_found'],{})
        self.assertEqual(store_info['did'],did)
        self.assertEqual(store_info['uri'],datasourcename)
        self.assertEqual(store_info['has_dtree'],False)

    def test_store_datasource_values_failure_datasource_data_not_found(self):
        ''' store_datasource_values should fail if datasource data is not found '''
        datasourcename='test_store_datasource_values_failure_datasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        datapointname='test_store_datasource_values_failure_dsdata_not_found'
        datapoint=api.create_datasource_datapoint(did=did, datapoint_uri=datapointname)

    def test_store_datasource_values_failure_datasource_data_not_found(self):
        ''' store_datasource_values should succeed '''
        datasourcename='test_store_datasource_values_failure_datasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        date2 = timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.store_datasource_values(did=did, date=date2)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDH_DDNF)

    def test_store_datasource_values_success_one_datapoint(self):
        ''' store_datasource_values should succeed '''
        datasourcename='test_store_datasource_values_success'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='test_store_datasource_values_success'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_info=api.store_datasource_values(did=did, date=date)
        self.assertEqual(store_info['dp_missing'],[])
        self.assertEqual(store_info['dp_found_twice'],[])
        self.assertEqual(store_info['non_dp_uris'],[])
        self.assertEqual(store_info['dp_found'],[{'pid':datapoint['pid'],'uri':datapoint['datapointname']}])
        self.assertEqual(store_info['did'],did)
        self.assertEqual(store_info['uri'],datasourcename)
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertEqual(int(data[0]['value']),23)
        self.assertEqual(data[0]['date'], date)

    def test_hook_to_datapoint_failure_invalid_pid(self):
        ''' hook_to_datapoint should fail if pid is not valid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        sid=uuid.uuid4()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.hook_to_datapoint(pid=pid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_HTDP_IPID)

    def test_hook_to_datapoint_failure_invalid_sid(self):
        ''' hook_to_datapoint should fail if sid is not valid '''
        sids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        pid=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.hook_to_datapoint(pid=pid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_HTDP_ISID)

    def test_hook_to_datapoint_failure_datapoint_not_found(self):
        ''' hook_to_datapoint should fail if pid is not found '''
        pid=uuid.uuid4()
        sid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.hook_to_datapoint(pid=pid, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_HTDP_DPNF)

    def test_hook_to_datapoint_success(self):
        ''' hook_to_datapoint should succeed if pid exists '''
        username='test_hook_to_datapoint_success'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        sid=uuid.uuid4()
        self.assertTrue(api.hook_to_datapoint(pid=pid, sid=sid))
        pid_hooks=cassapidatapoint.get_datapoint_hooks_sids(pid=pid)
        self.assertEqual(pid_hooks,[sid])

    def test_unhook_from_datapoint_failure_invalid_pid(self):
        ''' unhook_from_datapoint should fail if pid is not valid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        sid=uuid.uuid4()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.unhook_from_datapoint(pid=pid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_UHFDP_IPID)

    def test_unhook_from_datapoint_failure_invalid_sid(self):
        ''' unhook_from_datapoint should fail if sid is not valid '''
        sids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        pid=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.unhook_from_datapoint(pid=pid, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_UHFDP_ISID)

    def test_unhook_from_datapoint_success_hook_does_not_exist(self):
        ''' unhook_from_datapoint should succeed if hook does not exist '''
        pid=uuid.uuid4()
        sid=uuid.uuid4()
        self.assertTrue(api.unhook_from_datapoint(pid=pid, sid=sid))

    def test_unhook_from_datapoint_success_hook_does_exist(self):
        ''' unhook_from_datapoint should succeed if hook exists '''
        username='test_unhook_from_datapoint_success_hook_does_exist'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        sid=uuid.uuid4()
        self.assertTrue(api.hook_to_datapoint(pid=pid, sid=sid))
        pid_hooks=cassapidatapoint.get_datapoint_hooks_sids(pid=pid)
        self.assertEqual(pid_hooks,[sid])
        self.assertTrue(api.unhook_from_datapoint(pid=pid, sid=sid))
        pid_hooks=cassapidatapoint.get_datapoint_hooks_sids(pid=pid)
        self.assertEqual(pid_hooks,[])

    def test_get_datapoint_hooks_failure_invalid_pid(self):
        ''' get_datapoint_hooks should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datapoint_hooks(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDPH_IPID)

    def test_get_datapoint_hooks_failure_datapoint_not_found(self):
        ''' get_datapoint_hooks should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.get_datapoint_hooks(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDPH_DPNF)

    def test_get_datapoint_hooks_success_some_hooks(self):
        ''' get_datapoint_hooks should return the sid list of hooks '''
        username='test_get_datapoint_hooks_success_some_hooks'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        sids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        for sid in sids:
            self.assertTrue(api.hook_to_datapoint(pid=pid, sid=sid))
        pid_hooks=api.get_datapoint_hooks(pid=pid)
        self.assertEqual(sorted(pid_hooks),sorted(sids))

    def test_get_datapoint_hooks_success_no_hooks(self):
        ''' get_datapoint_hooks should return an empty list if no hook is found '''
        username='test_get_datapoint_hooks_success_no_hooks'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        uid=user['uid']
        datapoint_uri='datapoint_uri'
        datapoint=api.create_user_datapoint(uid=uid, datapoint_uri=datapoint_uri)
        self.assertEqual(datapoint['uid'],uid)
        self.assertEqual(datapoint['datapointname'],datapoint_uri)
        self.assertTrue('pid' in datapoint)
        self.assertTrue('color' in datapoint)
        pid=datapoint['pid']
        pid_hooks=api.get_datapoint_hooks(pid=pid)
        self.assertEqual(pid_hooks,[])

    def test_monitor_identified_uris_failure_invalid_did(self):
        ''' monitor_identified_uris should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date = timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_identified_uris(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MIU_IDID)

    def test_monitor_identified_uris_failure_invalid_date(self):
        ''' monitor_identified_uris should fail if date is invalid '''
        did = uuid.uuid4()
        dates = ['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.monitor_identified_uris(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_MIU_IDATE)

    def test_monitor_identified_uris_failure_datasource_not_found(self):
        ''' monitor_identified_uris should fail if datasource does not exist '''
        did = uuid.uuid4()
        date = timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.monitor_identified_uris(did=did, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MIU_DSNF)

    def test_monitor_identified_uris_failure_dtree_not_found(self):
        ''' monitor_identified_uris should fail if dtree does not exist '''
        datasourcename='test_monitor_identified_uris_failure_dtree_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointDTreeNotFoundException) as cm:
            api.monitor_identified_uris(did=did, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MIU_DTRNF)

    def test_monitor_identified_uris_failure_dasource_data_not_found(self):
        ''' monitor_identified_uris should fail if datasource data is not found '''
        datasourcename='test_monitor_identified_uris_failure_dasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        date2 = timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.monitor_identified_uris(did=did, date=date2)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDH_DDNF)

    def test_monitor_identified_uris_no_new_uris_found(self):
        ''' monitor_identified_uris should do nothing if no new uri is found '''
        datasourcename='test_monitor_identified_uris_no_new_uris_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        # no aditional uri has been detected with this dtree
        result = api.monitor_identified_uris(did=did, date=date)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitored'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],False)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_not_allowed(self):
        ''' monitor_identified_uris should do nothing if user has forbidden monitoring '''
        datasourcename='test_monitor_identified_uris_monitoring_not_allowed'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=[]))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        # no aditional uri has been detected with this dtree
        result = api.monitor_identified_uris(did=did, date=date)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitored'],[])
        self.assertEqual(result['monitoring_allowed'],False)
        self.assertEqual(result['monitoring_bounded'],False)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_supply_allowed_already_exists(self):
        ''' monitor_identified_uris should identify pending supplies '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_supply_allowed_already_exists'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        # no aditional uri has been detected with this dtree
        result = api.monitor_identified_uris(did=did, date=date)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitored'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_supply_allowed_does_not_exist(self):
        ''' monitor_identified_uris should identify pending supplies '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_supply_allowed_does_not_exist'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_supply_allowed_does_not_exist_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint['dtree'].serialize()))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2, date=date2)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),1)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], False)
        self.assertNotEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_no_predefined_supply_monitor_everything_it_finds(self):
        ''' monitor_identified_uris should identify every classified uri '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_no_predefined_supply_monitor_everything_it_finds'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_no_predefined_supply_monitor_everything_it_finds_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        #self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint['dtree'].serialize()))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2, date=date2)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],False)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),1)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], False)
        self.assertNotEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_allowed_only(self):
        ''' monitor_identified_uris should identify only allowed and pending uris '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_allowed_only'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri1'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        position=35
        length=2
        datapointname='datapoint_uri2'
        datapoint2=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        position=38
        length=3
        datapointname='datapoint_uri3'
        datapoint3=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_allowed_only_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri2','datapoint_uri3']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint3['dtree'].serialize()))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2, date=date2)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),2)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri2')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], False)
        self.assertEqual(result['monitored'][1]['uri'], '.'.join((datasourcename2,'datapoint_uri3')))
        self.assertEqual(result['monitored'][1]['did'], did2)
        self.assertEqual(result['monitored'][1]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][1]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][1]['previously_existed'], False)
        self.assertNotEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints(self):
        ''' monitor_identified_uris should identify only allowed and pending uris '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri1'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        position=35
        length=2
        datapointname2='datapoint_uri2'
        datapoint2=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname2)
        position=38
        length=3
        datapointname3='datapoint_uri3'
        datapoint3=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname3)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri2','datapoint_uri3']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint3['dtree'].serialize()))
        # create user datapoints, not associated to any datasource
        dp2 = api.create_user_datapoint(uid=datasource2['uid'], datapoint_uri='.'.join((datasourcename2,datapointname2)))
        dp3 = api.create_user_datapoint(uid=datasource2['uid'], datapoint_uri='.'.join((datasourcename2,datapointname3)))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2, date=date2)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),2)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri2')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], True)
        self.assertEqual(result['monitored'][1]['uri'], '.'.join((datasourcename2,'datapoint_uri3')))
        self.assertEqual(result['monitored'][1]['did'], did2)
        self.assertEqual(result['monitored'][1]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][1]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][1]['previously_existed'], True)
        self.assertNotEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints_date_null(self):
        ''' monitor_identified_uris should identify only allowed and pending uris '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints_date_null'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri1'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        position=35
        length=2
        datapointname2='datapoint_uri2'
        datapoint2=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname2)
        position=38
        length=3
        datapointname3='datapoint_uri3'
        datapoint3=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname3)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_some_predefined_supply_monitor_already_existed_as_user_datapoints_date_null_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri2','datapoint_uri3']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint3['dtree'].serialize()))
        # create user datapoints, not associated to any datasource
        dp2 = api.create_user_datapoint(uid=datasource2['uid'], datapoint_uri='.'.join((datasourcename2,datapointname2)))
        dp3 = api.create_user_datapoint(uid=datasource2['uid'], datapoint_uri='.'.join((datasourcename2,datapointname3)))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2) # date will be selected from datasource stats
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),2)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri2')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], True)
        self.assertEqual(result['monitored'][1]['uri'], '.'.join((datasourcename2,'datapoint_uri3')))
        self.assertEqual(result['monitored'][1]['did'], did2)
        self.assertEqual(result['monitored'][1]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][1]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][1]['previously_existed'], True)
        self.assertNotEqual(result['dtree'],None)

    def test_monitor_identified_uris_monitoring_allowed_limit_executions_based_on_supplies_insert_rate(self):
        ''' monitor_identified_uris should identify pending supplies '''
        datasourcename='test_monitor_identified_uris_monitoring_allowed_limit_executions_based_on_supplies_insert_rat'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did, supplies=['datapoint_uri']))
        #first var should be a position 32 and length 2
        position=32
        length=2
        datapointname='datapoint_uri1'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        position=35
        length=2
        datapointname2='datapoint_uri2'
        datapoint2=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname2)
        position=38
        length=3
        datapointname3='datapoint_uri3'
        datapoint3=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname3)
        store_result = api.store_datasource_values(did=did, date=date)
        datasourcename2= 'test_monitor_identified_uris_monitoring_allowed_limit_executions_based_on_supplies_insert_rate_2'
        datasource2=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date2=timeuuid.uuid1()
        content='store_datasource_values content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date2, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date2))
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri2']))
        self.assertTrue(cassapidatasource.insert_datapoint_classifier_dtree(did2, datapoint3['dtree'].serialize()))
        # datapoint_uri should be detected and monitored
        result = api.monitor_identified_uris(did=did2) # date will be selected from datasource stats
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],True)
        self.assertEqual(result['monitoring_bounded'],True)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),1)
        self.assertEqual(result['monitored'][0]['uri'], '.'.join((datasourcename2,'datapoint_uri2')))
        self.assertEqual(result['monitored'][0]['did'], did2)
        self.assertEqual(result['monitored'][0]['aid'], datasource2['aid'])
        self.assertEqual(result['monitored'][0]['uid'], datasource2['uid'])
        self.assertEqual(result['monitored'][0]['previously_existed'], False)
        self.assertNotEqual(result['dtree'],None)
        # now we insert supplies
        self.assertTrue(datasourceapi.update_datasource_supplies(did=did2, supplies=['datapoint_uri2','datapoint_uri3']))
        # execution should be discarded because multiple supplies updates have been done very recently
        result = api.monitor_identified_uris(did=did2)
        self.assertEqual(result['pending'],[])
        self.assertEqual(result['monitoring_allowed'],False)
        self.assertEqual(result['monitoring_bounded'],False)
        self.assertEqual(result['more_than_once'],[])
        self.assertEqual(len(result['monitored']),0)
        self.assertEqual(result['creation_failed'],[])
        self.assertEqual(result['dtree'],None)

    def test_select_dtree_for_datasource_failure_invalid_did(self):
        ''' select_dtree_for_datasource should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.select_dtree_for_datasource(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDTDS_IDID)

    def test_select_dtree_for_datasource_failure_non_existent_did(self):
        ''' select_dtree_for_datasource should fail if did does not exist '''
        did = uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.select_dtree_for_datasource(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDTDS_DSNF)

    def test_select_dtree_for_datasource_success_datasource_has_no_data(self):
        ''' select_dtree_for_datasource should do nothing if ds has no data '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_select_dtree_for_datasource_success_datasource_has_no_data'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertIsInstance(datasource, dict)
        self.assertEqual(datasource['aid'],aid)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        result = api.select_dtree_for_datasource(datasource['did'])
        self.assertEqual(result['features'],[])
        self.assertEqual(result['updated'],False)
        self.assertEqual(result['dtree'],None)

    def test_select_dtree_for_datasource_success_datasource_has_one_sample(self):
        ''' select_dtree_for_datasource should try to find a matching ds if this ds has data '''
        username='test_select_dtree_for_datasource_success_datasource_has_one_sample'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_select_dtree_for_datasource_success_datasource_has_one_sample'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='thiscontentisnotanywhereIhope 25'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        result = api.select_dtree_for_datasource(did)
        self.assertNotEqual(result['features'],[])
        self.assertEqual(result['updated'],True)
        self.assertEqual(result['dtree'],None)

    def test_select_dtree_for_datasource_success_dont_exec_if_configured_interval_not_elapsed(self):
        ''' select_dtree_for_datasource should not execute if the configured interval is not elapsed yet '''
        username='test_select_dtree_for_datasource_success_dont_exec_if_configured_interval_not_elapsed'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_select_dtree_for_datasource_success_dont_exec_if_configured_interval_not_elapsed'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='Wellthisisnotherethough 25'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        result = api.select_dtree_for_datasource(did)
        self.assertNotEqual(result['features'],[])
        self.assertEqual(result['updated'],True)
        self.assertEqual(result['dtree'],None)
        result2 = api.select_dtree_for_datasource(did)
        self.assertEqual(result2['features'],result['features'])
        self.assertEqual(result2['updated'],False)
        self.assertEqual(result2['dtree'],None)

    def test_select_dtree_for_datasource_success_dtree_identified(self):
        ''' select_dtree_for_datasource should identify a matching dtree for the ds '''
        datasourcename='test_select_dtree_for_datasource_success_dtree_identified'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='datapointname'
        datapoint=api.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        content='16 hours work no play makes Juan a dull boy, and 14 and 12 and 10 too'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 50 and length 2
        position=0
        length=2
        mark_result=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length,dtree_update=False)
        self.assertEqual(mark_result,{'updated':[],'pending':[did]})
        result = api.generate_decision_tree(did=did)
        self.assertEqual(result['classified'],[datapointname])
        self.assertIsNotNone(result['dtree'])
        s_dtree = cassapidatasource.get_datapoint_classifier_dtree(did=did)
        dtree = dtreeapi.load_dtree(s_dtree)
        dshashes=cassapidatasource.get_datasource_hashes(did=did, fromdate=date, todate=date)
        self.assertEqual(len(dshashes),1)
        for dshash in dshashes:
            text_hash=json.loads(dshash.content)
            variables_atts=textmanvar.get_variables_atts(text_hash)
            for var in variables_atts:
                result = dtree.classify(var['atts'])
                if var['text_pos']!=position:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result,{datapointname:1})
        # register ds features
        result = datasourceapi.update_datasource_features(did=did)
        # now, create a new user, agent, datasource and try to match the dtree
        username='all_work_no_play_makes_juan_a_dull_boy'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_select_dtree_for_datasource_success_dont_exec_if_configured_interval_not_elapsed'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename2='datasourcename'
        datasource2=datasourceapi.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename2)
        did2=datasource2['did']
        date=timeuuid.uuid1()
        content='16 hours work no play makes Juan a dull boy, deal with it'
        self.assertTrue(datasourceapi.store_datasource_data(did=did2, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did2, date=date))
        result2 = api.select_dtree_for_datasource(did2)
        self.assertNotEqual(result2['features'],[])
        self.assertEqual(result2['updated'],True)
        self.assertNotEqual(result2['dtree'],None)
        dshashes=cassapidatasource.get_datasource_hashes(did=did2, fromdate=date, todate=date)
        self.assertEqual(len(dshashes),1)
        for dshash in dshashes:
            text_hash=json.loads(dshash.content)
            variables_atts=textmanvar.get_variables_atts(text_hash)
            for var in variables_atts:
                result = dtree.classify(var['atts'])
                if var['text_pos']!=position:
                    self.assertIsNone(result)
                else:
                    self.assertEqual(result,{datapointname:1})

