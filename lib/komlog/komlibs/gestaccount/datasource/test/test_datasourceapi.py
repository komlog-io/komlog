import unittest
import uuid
import random
from komlog.komfig import logger
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api
from komlog.komlibs.gestaccount import exceptions, errors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto

class GestaccountDatasourceApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datasource.api tests '''

    def setUp(self):
        username='test_gestaccount.datasource.api_user'
        password='password'
        email='test_gestaccount.datasource.api_user@komlog.org'
        try:
            uid=userapi.get_uid(username=username)
        except Exception:
            user=userapi.create_user(username=username, password=password, email=email)
            uid=user['uid']
        finally:
            self.user=userapi.get_user_config(uid=uid)
        agentname='test_gestaccount.datasource.api_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        try:
            self.agent=agentapi.create_agent(uid=self.user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        except Exception:
            agents=agentapi.get_agents_config(uid=self.user['uid'])
            for agent in agents:
                if agent['agentname']==agentname:
                    self.agent=agent

    def test_create_datasource_non_existent_user(self):
        ''' create_datasource should fail if user is not found in system '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        datasourcename='datasource_name'
        self.assertRaises(exceptions.UserNotFoundException, api.create_datasource,uid=uid, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_non_existent_agent(self):
        ''' create_datasource should fail if agent is not found in system '''
        uid=self.user['uid']
        aid=uuid.uuid4()
        datasourcename='test_create_datasource_non_existent_agent'
        self.assertRaises(exceptions.AgentNotFoundException, api.create_datasource,uid=uid, aid=aid, datasourcename=datasourcename ) 

    def test_create_datasource_success(self):
        ''' create_datasource should succeed if user and agent exist '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_create_datasource_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertIsInstance(datasource, dict)
        self.assertEqual(datasource['aid'],aid)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)

    def test_get_last_processed_datasource_data_non_existent_datasource(self):
        ''' get_last_processed_datasource_data should fail if did is not in system '''
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.get_last_processed_datasource_data, did=did)

    def test_upload_datasource_data_non_existent_datasource(self):
        ''' upload_datasource_data should fail if did is not in system '''
        did=uuid.uuid4()
        content='sadfa'
        dest_dir=''
        self.assertRaises(exceptions.DatasourceNotFoundException, api.upload_datasource_data, did=did, content=content, dest_dir=dest_dir)

    def test_get_datasource_config_non_existent_datasource(self):
        ''' get_datasource_config should fail if did is not in system '''
        did=uuid.uuid4()
        self.assertRaises(exceptions.DatasourceNotFoundException, api.get_datasource_config, did=did)

    def test_get_datasource_config_success(self):
        ''' get_datasource_config should succeed if datasource exists '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_config_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        data=api.get_datasource_config(did=datasource['did'], pids_flag=True)
        self.assertIsInstance(data, dict)
        self.assertEqual(datasource['aid'],aid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertEqual(len(data),5)

    def test_get_datasources_config_non_existent_username(self):
        ''' get_datasource_config should fail if user is not in system '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, api.get_datasources_config,uid=uid)

    def test_get_datasources_config_success(self):
        ''' get_datasources_config should succeed if user exists '''
        username='test_get_datasources_config_success_user'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_get_datasources_config_success_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        self.agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        data=api.get_datasources_config(uid=user['uid'])
        self.assertEqual(data, [])

    def test_update_datasource_config_data_with_empty_datasourcename(self):
        ''' update_datasource_config should fail if data has empty ds_name'''
        did=uuid.uuid4()
        datasourcename=None
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_data_with_invalid_datasourcename(self):
        ''' update_datasource_config should fail if data has invalid ds_name'''
        did=uuid.uuid4()
        datasourcename=2342321434
        self.assertRaises(exceptions.BadParametersException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_non_existent_datasource(self):
        ''' update_datasource_config should fail if datasource is not in system '''
        did=uuid.uuid4()
        datasourcename='test_update_datasource_config_with_invalid_datasourcename'
        self.assertRaises(exceptions.DatasourceNotFoundException, api.update_datasource_config, did=did, datasourcename=datasourcename)

    def test_update_datasource_config_success(self):
        ''' update_datasource_config should succeed if datasource exists '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_config_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        datasourcename='test_update_datasource_config_success_after_update'
        self.assertTrue(api.update_datasource_config(did=datasource['did'], datasourcename=datasourcename))

    def test_get_datasource_data_success(self):
        ''' store_datasource_data should should store the content successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='store_datasource_data content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], did)
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)

    def test_get_datasource_data_non_existent_datasource(self):
        ''' get_datasource_data should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.get_datasource_data, did=did, date=date)

    def test_get_datasource_data_non_existent_data_at_this_date(self):
        ''' get_datasource_data should fail if there is no data '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='store_datasource_data content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.get_datasource_data, did=did, date=date)

    def test_generate_datasource_map_non_existent_datasource(self):
        ''' generate_datasource_map should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.generate_datasource_map, did=did, date=date)

    def test_generate_datasource_map_non_existent_data_at_given_time(self):
        ''' generate_datasource_map should fail if did does not exist '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_generate_datasource_map_non_existent_data_at_given_time'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.generate_datasource_map, did=datasource['did'], date=date)

    def test_generate_datasource_map_success(self):
        ''' generate_datasource_data should generate and store the map successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='generate_datasource_map content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], did)
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)
        self.assertTrue(api.generate_datasource_map(did=did, date=date))

    def test_generate_datasource_text_summary_failure_invalid_did(self):
        ''' generate_datasource_text_summary should fail if did is not valid '''
        dids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_datasource_text_summary(did=did, date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_GDTS_ID)

    def test_generate_datasource_text_summary_failure_invalid_date(self):
        ''' generate_datasource_text_summary should fail if date is not valid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid4().hex]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_datasource_text_summary(did=did, date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_GDTS_IDT)

    def test_generate_datasource_text_summary_non_existent_datasource(self):
        ''' generate_datasource_text_summary should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_text_summary(did=did, date=date)
        self.assertEqual(cm.exception.error, errors.E_GDA_GDTS_DDNF)

    def test_generate_datasource_text_summary_non_existent_data_at_given_timeuuid(self):
        ''' generate_datasource_text_summary should fail if did has no sample at given timeuuid '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_generate_datasource_text_summary_non_existent_data_at_given_timeuuid'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_text_summary(did=datasource['did'],date=date)
        self.assertEqual(cm.exception.error, errors.E_GDA_GDTS_DDNF)

    def test_generate_datasource_text_summary_success(self):
        ''' generate_datasource_text_summary should generate and store the summary successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='generate_datasource_text_summary content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, date=date)
        self.assertIsNotNone(data)
        self.assertEqual(data['did'], did)
        self.assertEqual(data['date'], date)
        self.assertEqual(data['content'], content)
        self.assertTrue(api.generate_datasource_text_summary(did=did, date=date))

    def test_generate_datasource_novelty_detector_for_datapoint_failure_invalid_pid(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if pid is invalid '''
        pids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_datasource_novelty_detector_for_datapoint(pid=pid)
            self.assertEqual(cm.exception.error, errors.E_GDA_GDNDFD_IP)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_non_existent_pid(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if pid does not exist '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=pid)
        self.assertEqual(cm.exception.error, errors.E_GDA_GDNDFD_DNF)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_non_datasource_data(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if no datasource data is found '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, errors.E_GDA_GDNDFD_DSDNF)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if no text summary is found, raising an error when generating de novelty detector '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        with self.assertRaises(exceptions.DatasourceNoveltyDetectorException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, errors.E_GDA_GDNDFD_NDF)

    def test_generate_datasource_novelty_detector_for_datapoint_success(self):
        ''' generate_datasource_novelty_detector_for_datapoint should succeed '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_success_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_success_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid']))
    def test_should_datapoint_appear_in_sample_failure_invalid_pid(self):
        ''' should_datapoint_appear_in_sample should fail if pid is invalid '''
        pids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_appear_in_sample(pid=pid,date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_SDAIS_IP)

    def test_should_datapoint_appear_in_sample_failure_invalid_date(self):
        ''' should_datapoint_appear_in_sample should fail if date is invalid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'), uuid.uuid4().hex, uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_appear_in_sample(pid=pid, date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_SDAIS_IDT)

    def test_should_datapoint_appear_in_sample_failure_non_existent_datapoint(self):
        ''' should_datapoint_appear_in_sample should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.should_datapoint_appear_in_sample(pid=pid, date=date)
        self.assertEqual(cm.exception.error, errors.E_GDA_SDAIS_DNF)

    def test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found(self):
        ''' should_datapoint_appear_in_sample should fail if no novelty_detector is found '''
        datasourcename='test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        with self.assertRaises(exceptions.DatasourceNoveltyDetectorException) as cm:
            api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=date)
        self.assertEqual(cm.exception.error, errors.E_GDA_GDNDFD_NDF)

    def test_should_datapoint_appear_in_sample_failure_no_text_summary_found(self):
        ''' should_datapoint_appear_in_sample should fail if no text summary is found '''
        datasourcename='test_should_datapoint_appear_in_sample_failure_no_text_summary_found_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_failure_no_text_summary_found_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date)
        self.assertEqual(cm.exception.error, errors.E_GDA_GDTS_DDNF)

    def test_should_datapoint_appear_in_sample_success_result_false(self):
        ''' should_datapoint_appear_in_sample should succeed and the result should be false '''
        datasourcename='test_should_datapoint_appear_in_sample_success_result_false_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_success_result_false_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        new_content='some content with no relation with previous other samples'
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertFalse(api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date))

    def test_should_datapoint_appear_in_sample_success_result_true(self):
        ''' should_datapoint_appear_in_sample should succeed and the result should be true '''
        datasourcename='test_should_datapoint_appear_in_sample_success_result_true_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_success_result_true_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        for i in range(1,200):
            date=timeuuid.uuid1()
            content='mark_negative_variable content with ññññ and 23 32 554 and \nnew  lines\ttabs\tetc.. '+' '*int(i/2)+' something '+crypto.get_random_string(size=1)
            self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
            self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
            self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
            if i%100==0:
                #first var should be a position 45 and length 2
                position=45
                length=2
                self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
            self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        new_content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date))

    def test_classify_missing_datapoints_in_sample_failure_invalid_did(self):
        ''' classify_missing_datapoints_in_sample should fail if did is invalid '''
        dids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.classify_missing_datapoints_in_sample(did=did,date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_CMDIS_ID)

    def test_classify_missing_datapoints_in_sample_failure_invalid_date(self):
        ''' classify_missing_datapoints_in_sample should fail if date is invalid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1().hex, uuid.uuid4()]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.classify_missing_datapoints_in_sample(did=did,date=date)
            self.assertEqual(cm.exception.error, errors.E_GDA_CMDIS_IDT)

    def test_classify_missing_datapoints_in_sample_failure_dsmap_not_found(self):
        ''' classify_missing_datapoints_in_sample should fail if dsmap is not found '''
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.classify_missing_datapoints_in_sample(did=did,date=date)
        self.assertEqual(cm.exception.error, errors.E_GDA_CMDIS_DSMNF)

    def test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        #self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[])

    def test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_content='some content with some variables 32 but nothing to do with previous 211 samples '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=new_date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[datapoint['pid']])

    def test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 45 and length 2
        position=48
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_content='mark_negative_variable content with ññññ and b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=new_date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[datapoint['pid']])

    def test_classify_missing_datapoints_in_sample_success_pid_is_doubt(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_doubt_datasource'
        datasource=api.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_doubt_datapoint'
        color='#FFDDEE'
        datapoint=datapointapi.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 45 and length 2
        position=48
        length=2
        self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        for i in range(1,200):
            date=timeuuid.uuid1()
            content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew  lines\ttabs\tetc.. '+' '*int(i/2)+' something '+crypto.get_random_string(size=2)
            self.assertTrue(api.store_datasource_data(did=datasource['did'], date=date, content=content))
            self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
            self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=date))
            if i%20==0:
                #first var should be a position 45 and length 2
                position=48
                length=2
                self.assertTrue(datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
            self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=date))
        new_content='mark_negative_variable content with ññññ and a: *30*  ,b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(api.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(datapointapi.store_datasource_values(did=datasource['did'],date=new_date))
        logger.logger.debug('PID del TEST: '+str(datapoint['pid']))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        logger.logger.debug('Result: '+str(result))
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['discarded'],[])
        self.assertEqual(result['doubts'],[datapoint['pid']])

