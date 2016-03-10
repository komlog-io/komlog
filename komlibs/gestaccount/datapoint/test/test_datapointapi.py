import unittest
import uuid
from komcass.api import datasource as cassapidatasource
from komcass.api import datapoint as cassapidatapoint
from komlibs.textman.api import variables as textmanvar
from komlibs.ai.decisiontree import api as dtreeapi
from komlibs.general.time import timeuuid
from komlibs.general.crypto import crypto
from komlibs.gestaccount.user import api as userapi
from komlibs.gestaccount.agent import api as agentapi
from komlibs.gestaccount.datasource import api as datasourceapi
from komlibs.gestaccount.widget import api as widgetapi
from komlibs.gestaccount.datapoint import api
from komlibs.gestaccount import exceptions, errors
from komfig import logger

class GestaccountDatapointApiTest(unittest.TestCase):
    ''' komlog.gestaccount.datapoint.api tests '''
    
    def setUp(self):
        username='test_gestaccount.datapoint.api_user'
        password='password'
        email='test_gestaccount.datapoint.api_user@komlog.org'
        try:
            self.user=userapi.get_user_config(username=username)
        except Exception:
            self.user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_gestaccount.datapoint.api_agent'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
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

    def test_create_datapoint_non_existent_datasource(self):
        ''' create_datapoint should fail if datasource is not found in system '''
        did=uuid.uuid4()
        datapointname='datapoint_name'
        color='#FFDDAA'
        self.assertRaises(exceptions.DatasourceNotFoundException,api.create_datapoint,did=did,datapointname=datapointname, color=color)

    def test_create_datapoint_success(self):
        ''' create_datapoint should succeed if datasource exists '''
        did=self.datasource['did']
        datapointname='test_create_datapoint_success'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        self.assertIsInstance(datapoint, dict)
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],datapointname)

    def test_get_datapoint_data_non_existent_datapoint(self):
        ''' get_datapoint_data should fail if pid is not in system '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=pid)

    def test_get_datapoint_data_no_data(self):
        ''' get_datapoint_data should fail if pid has no data in system '''
        did=self.datasource['did']
        datapointname='test_get_datapoint_data_no_data'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        self.assertRaises(exceptions.DatapointDataNotFoundException, api.get_datapoint_data, pid=datapoint['pid'])

    def test_get_datapoint_config_non_existent_datapoint(self):
        ''' get_datapoint_config should fail if pid is not in system '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.get_datapoint_config, pid=pid)

    def test_get_datapoint_config_success(self):
        ''' get_datapoint_config should succeed if pid exists in system '''
        did=self.datasource['did']
        datapointname='test_get_datapoint_config_success'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        data=api.get_datapoint_config(pid=datapoint['pid'])
        self.assertIsInstance(data, dict)
        self.assertEqual(data['did'],did)
        self.assertEqual(data['datapointname'],datapointname)
    
    def test_update_datapoint_config_non_existent_datapoint(self):
        ''' update_datapoint_config should fail if datapoint is not in system '''
        pid=uuid.uuid4()
        datapointname='test_update_datapoint_config_with_non_existent_datapoint'
        self.assertRaises(exceptions.DatapointNotFoundException, api.update_datapoint_config, pid=pid, datapointname=datapointname)

    def test_update_datapoint_config_with_invalid_datapointname(self):
        ''' update_datapoint_config should fail if data has invalid datapointname'''
        pid=uuid.uuid4()
        datapointnames=[None,213123123,'Not Valid chars ÑÑÑÑ',{},['names','in array']]
        for datapointname in datapointnames:
            self.assertRaises(exceptions.BadParametersException, api.update_datapoint_config, pid=pid, datapointname=datapointname)

    def test_update_datapoint_config_with_invalid_color(self):
        ''' update_datapoint_config should fail if data has invalid color code'''
        pid=uuid.uuid4()
        datapointcolors=[None,213123123,'Not Valid chars ÑÑÑÑ',{},['colors','in array']]
        for color in datapointcolors:
            self.assertRaises(exceptions.BadParametersException, api.update_datapoint_config, pid=pid, color=color)

    def test_update_datapoint_config_failure_no_parameters(self):
        ''' update_datapoint_config should fail if datapoint nor color is passed'''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.BadParametersException, api.update_datapoint_config, pid=pid)

    def test_update_datapoint_config_success(self):
        ''' update_datapoint_config should succeed if pid exists in system and params are OK '''
        did=self.datasource['did']
        datapointname='test_update_datapoint_config_success'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname,color=color)
        datapointname='test_update_datapoint_config_success_after_update'
        color='#FFAA88'
        self.assertTrue(api.update_datapoint_config(pid=datapoint['pid'], datapointname=datapointname, color=color))

    def test_mark_negative_variable_failure_non_existent_datapoint(self):
        ''' mark_negative_variable should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        self.assertRaises(exceptions.DatapointNotFoundException, api.mark_negative_variable, pid=pid, date=date, position=position, length=length)

    def test_mark_negative_variable_failure_no_variables_in_datasource_map(self):
        ''' mark_negative_variable should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_no_variables_in_datasource_map'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        position=1
        length=1
        self.assertRaises(exceptions.DatasourceMapNotFoundException, api.mark_negative_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_negative_variable_failure_invalid_variable_length(self):
        ''' mark_negative_variable should fail if variable length does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_invalid_variable_length'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=1
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.mark_negative_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_negative_variable_failure_invalid_variable_position(self):
        ''' mark_negative_variable should fail if variable position does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_failure_invalid_variable_position'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=46
        length=2
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.mark_negative_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_negative_variable_success(self):
        ''' mark_negative_variable should succeed '''
        did=self.datasource['did']
        datapointname='test_mark_negative_variable_success'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        datapoints_to_update=api.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(datapoints_to_update, [datapoint['pid'],])

    def test_mark_positive_variable_failure_non_existent_datapoint(self):
        ''' mark_positive_variable should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        self.assertRaises(exceptions.DatapointNotFoundException, api.mark_positive_variable, pid=pid, date=date, position=position, length=length)

    def test_mark_positive_variable_failure_no_variables_in_datasource_map(self):
        ''' mark_positive_variable should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_no_variables_in_datasource_map'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        position=1
        length=1
        self.assertRaises(exceptions.DatasourceMapNotFoundException, api.mark_positive_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_positive_variable_failure_invalid_variable_length(self):
        ''' mark_positive_variable should fail if variable length does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_invalid_variable_length'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_positive_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=1
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.mark_positive_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_positive_variable_failure_invalid_variable_position(self):
        ''' mark_positive_variable should fail if variable position does not match with the value in db'''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_failure_invalid_variable_position'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=46
        length=2
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.mark_positive_variable, pid=datapoint['pid'], date=date, position=position, length=length)

    def test_mark_positive_variable_success_no_other_datapoint_matched(self):
        ''' mark_positive_variable should succeed in this case, no other datapoint matched '''
        did=self.datasource['did']
        datapointname='test_mark_positive_variable_success_no_other_datapoint_matched_dp'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))

    def test_mark_positive_variable_failure_one_other_datapoint_matched_dont_replace(self):
        ''' mark_positive_variable should fail if other datapoint matched and dont want to replace '''
        datasourcename='test_mark_positive_variable_failure_one_other_datapoint_matched_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_mark_positive_variable_failure_one_other_datapoint_matched'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_positive_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        datapoints_to_update=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        dsdata=datasourceapi.get_datasource_data(did=did, date=date)
        dsdatapoints=dsdata['datapoints']
        self.assertTrue(len(dsdatapoints),1)
        self.assertEqual(dsdatapoints[0]['pid'],datapoint['pid'])
        self.assertEqual(dsdatapoints[0]['position'],position)
        datapointname='test_mark_positive_variable_failure_one_other_datapoint_matched_2'
        color='#FFDDAA'
        datapoint2=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        self.assertRaises(exceptions.VariableMatchesExistingDatapointException, api.mark_positive_variable, pid=datapoint2['pid'], date=date, position=position, length=length, replace=False)

    def test_mark_positive_variable_success_one_other_datapoint_matched_but_replace(self):
        ''' mark_positive_variable should succeed in this case other datapoint matched '''
        datasourcename='test_mark_positive_variable_success_one_other_datapoint_matched_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        datapoints_to_update=api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        dsdata=datasourceapi.get_datasource_data(did=did, date=date)
        dsdatapoints=dsdata['datapoints']
        self.assertTrue(len(dsdatapoints),1)
        self.assertEqual(dsdatapoints[0]['pid'],datapoint['pid'])
        self.assertEqual(dsdatapoints[0]['position'],position)
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched_2'
        color='#FFDDAA'
        datapoint2=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        datapoints_to_update=api.mark_positive_variable(pid=datapoint2['pid'], date=date, position=position, length=length)
        dsdata=datasourceapi.get_datasource_data(did=did, date=date)
        dsdatapoints=dsdata['datapoints']
        self.assertTrue(len(dsdatapoints),1)
        self.assertEqual(dsdatapoints[0]['pid'],datapoint2['pid'])
        self.assertEqual(dsdatapoints[0]['position'],position)

    def test_mark_missing_datapoint_failure_non_existent_datapoint(self):
        ''' mark_missing_datapoint should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.mark_missing_datapoint(pid=pid, date=date)
        self.assertEqual(cm.exception.error, errors.E_GPA_MMDP_DNF)

    def test_mark_missing_datapoint_failure_no_variables_in_datasource_map(self):
        ''' mark_missing_datapoint should fail if datasource map has no variables '''
        did=self.datasource['did']
        datapointname='test_mark_missing_datapoint_failure_no_variables_in_datasource_map'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.mark_missing_datapoint(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, errors.E_GPA_MMDP_DMNF)

    def test_generate_decision_tree_failure_invalid_pid(self):
        ''' generate_tree should fail if pid does not exists '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_decision_tree(pid=pid)
            self.assertEqual(cm.exception.error, errors.E_GPA_GDT_IP)

    def test_generate_decision_tree_failure_non_existent_datapoint(self):
        ''' generate_decision_tree should fail if pid does not exists '''
        pid=uuid.uuid4()
        self.assertRaises(exceptions.DatapointNotFoundException, api.generate_decision_tree, pid=pid)

    def test_generate_decision_tree_failure_no_training_set_found(self):
        ''' generate_decision_tree should fail if pid does not have a training set of positive and/or negative samples '''
        datasourcename='test_generate_decision_tree_failure_no_training_set_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_decision_tree_failure_no_training_set_found_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        pid=datapoint['pid']
        self.assertRaises(exceptions.DatapointDTreeTrainingSetEmptyException, api.generate_decision_tree, pid=pid)

    def test_generate_decision_tree_success(self):
        ''' generate_decision_tree should succeed if pid exists and has training set '''
        datasourcename='test_generate_decision_tree_success_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_decision_tree_success_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        content='generate_decision_tree content with ññ€#@hrññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 50 and length 2
        position=50
        length=2
        self.assertEqual(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length), [pid,])
        self.assertTrue(api.generate_decision_tree(pid=pid))
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        dtree=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree)
        dsmaps=cassapidatasource.get_datasource_maps(did=did,fromdate=date,todate=date)
        self.assertEqual(len(dsmaps),1)
        for dsmap in dsmaps:
            variable_list=textmanvar.get_variables_from_serialized_list(serialization=dsmap.content)
            for var in variable_list:
                self.assertFalse(dtree.evaluate_row(var.hash_sequence)) if var.position!=position else self.assertTrue(dtree.evaluate_row(var.hash_sequence))

    def test_generate_inverse_decision_tree_failure_invalid_pid(self):
        ''' generate_decision_tree should fail if pid does not exists '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_inverse_decision_tree(pid=pid)
            self.assertEqual(cm.exception.error, errors.E_GPA_GIDT_IP)

    def test_generate_inverse_decision_tree_failure_non_existent_datapoint(self):
        ''' generate_decision_tree should fail if pid does not exists '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.generate_inverse_decision_tree(pid=pid)
        self.assertEqual(cm.exception.error, errors.E_GPA_GIDT_DNF)

    def test_generate_inverse_decision_tree_failure_no_training_set_found(self):
        ''' generate_inverse_decision_tree should fail if pid does not have a training set of positive and/or negative samples '''
        datasourcename='test_generate_inverse_decision_tree_failure_no_training_set_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_inverse_decision_tree_failure_no_training_set_found_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        pid=datapoint['pid']
        with self.assertRaises(exceptions.DatapointDTreeTrainingSetEmptyException) as cm:
            api.generate_inverse_decision_tree(pid=pid)
        self.assertEqual(cm.exception.error, errors.E_GPA_GIDT_ETS)

    def test_generate_inverse_decision_tree_success(self):
        ''' generate_decision_tree should succeed if pid exists and has training set '''
        datasourcename='test_generate_inverse_decision_tree_success_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_generate_inverse_decision_tree_success_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        pid=datapoint['pid']
        date=timeuuid.uuid1()
        content='generate_decision_tree content with ññ€#@hrññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 50 and length 2
        position=50
        length=2
        self.assertEqual(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length), [pid,])
        self.assertTrue(api.generate_inverse_decision_tree(pid=pid))
        datapoint_stats=cassapidatapoint.get_datapoint_stats(pid=pid)
        dtree_inv=dtreeapi.get_decision_tree_from_serialized_data(serialization=datapoint_stats.dtree_inv)
        dsmaps=cassapidatasource.get_datasource_maps(did=did,fromdate=date,todate=date)
        self.assertEqual(len(dsmaps),1)
        for dsmap in dsmaps:
            variable_list=textmanvar.get_variables_from_serialized_list(serialization=dsmap.content)
            for var in variable_list:
                self.assertFalse(dtree_inv.evaluate_row(var.hash_sequence)) if var.position==position else self.assertTrue(dtree_inv.evaluate_row(var.hash_sequence))

    def test_monitor_new_datapoint_failure_other_datapoint_matched_variable(self):
        ''' monitor_new_datapoint should fail if there is other datapoint that matches the selected variable '''
        datasourcename='test_monitor_new_datapoint_failure_other_datapoint_matched_variable_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='monitor_new_datapoint content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 44 and length 2
        position=44
        length=2
        datapointname='test_monitor_new_datapoint_failure_other_datapoint_matched_variable_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(len(datapoint),1)
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],datapointname)
        datapointname2='test_monitor_new_datapoint_failure_other_datapoint_matched_variable_datapoint2'
        self.assertRaises(exceptions.VariableMatchesExistingDatapointException, api.monitor_new_datapoint, did=did, date=date, position=position, length=length, datapointname=datapointname2)

    def test_monitor_new_datapoint_failure_datasource_data_not_found(self):
        ''' monitor_new_datapoint should fail if datasource data does not exist '''
        datasourcename='test_monitor_new_datapoint_failure_datasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        position=1
        length=1
        datapointname='test_monitor_new_datapoint_failure_variable_position'
        self.assertRaises(exceptions.DatasourceMapNotFoundException, api.monitor_new_datapoint, did=did, date=date, position=position, length=length, datapointname=datapointname)

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
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.monitor_new_datapoint, did=did, date=date, position=position, length=length, datapointname=datapointname)

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
        self.assertRaises(exceptions.DatasourceVariableNotFoundException, api.monitor_new_datapoint, did=did, date=date, position=position, length=length, datapointname=datapointname)

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
        self.assertEqual(datapoint['datapointname'],datapointname)
        self.assertTrue(isinstance(datapoint['pid'],uuid.UUID))

    def test_store_datapoint_values_failure_datapoint_not_found(self):
        ''' store_datapoint_values should fail if datapoint is not found '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatapointNotFoundException, api.store_datapoint_values, pid=pid, date=date)

    def test_store_datapoint_values_failure_dtree_not_found(self):
        ''' store_datapoint_values should fail if datapoint dtree is not found '''
        did=self.datasource['did']
        datapointname='test_store_datapoint_values_failure_dtree_not_found_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        self.assertRaises(exceptions.DatapointDTreeNotFoundException, api.store_datapoint_values, pid=datapoint['pid'], date=date)

    def test_store_datapoint_values_failure_datasource_map_not_found(self):
        ''' store_datapoint_values should fail if datasource map is not found  '''
        datasourcename='test_store_datapoint_values_failure_datasource_map_not_found'
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
        self.assertRaises(exceptions.DatasourceMapNotFoundException, api.store_datapoint_values, pid=datapoint['pid'], date=timeuuid.uuid1(seconds=timeuuid.get_unix_timestamp(date)+600))

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

    def test_store_datasource_values_failure_datasource_map_not_found(self):
        ''' store_datasource_values should fail if datasource map is not found '''
        datasourcename='test_store_datasource_values_failure_datasource_map_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        datapointname='test_store_datasource_values_success'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did, datapointname=datapointname, color=color)
        self.assertRaises(exceptions.DatasourceMapNotFoundException, api.store_datasource_values, did=did, date=date)

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
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)

    def test_should_datapoint_match_any_sample_variable_failure_invalid_pid(self):
        ''' should datapoint_match_any_sample_variable should fail if pid is invalid '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_match_any_sample_variable(pid=pid, date=date)
            self.assertEqual(cm.exception.error, errors.E_GPA_SDMSV_IP)

    def test_should_datapoint_match_any_sample_variable_failure_invalid_date(self):
        ''' should datapoint_match_any_sample_variable should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_match_any_sample_variable(pid=pid, date=date)
            self.assertEqual(cm.exception.error, errors.E_GPA_SDMSV_IDT)

    def test_should_datapoint_match_any_sample_variable_failure_non_existent_pid(self):
        ''' should datapoint_match_any_sample_variable should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.should_datapoint_match_any_sample_variable(pid=pid, date=date)
        self.assertEqual(cm.exception.error, errors.E_GPA_SDMSV_DNF)

    def test_should_datapoint_match_any_sample_variable_failure_no_datapoint_data(self):
        ''' should_datapoint_match_any_sample_variable should fail if datapoint has no data '''
        did=self.datasource['did']
        datapointname='test_should_datapoint_match_any_sample_variable_failure_no_datapoint_data_datapoint'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        self.assertIsInstance(datapoint, dict)
        self.assertEqual(datapoint['did'],did)
        self.assertEqual(datapoint['datapointname'],datapointname)
        with self.assertRaises(exceptions.DatapointDTreeTrainingSetEmptyException) as cm:
            api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=date)
        self.assertEqual(cm.exception.error, errors.E_GPA_GDT_ETS)

    def test_should_datapoint_match_any_sample_variable_failure_datasource_map_not_found(self):
        ''' should_datapoint_match_any_sample_variable should fail if datasource map does not exist '''
        datasourcename='test_should_datapoint_match_any_sample_variable_failure_datasource_map_not_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_should_datapoint_match_any_sample_variable_failure_datasource_map_not_found_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        new_date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=new_date)
        self.assertEqual(cm.exception.error, errors.E_GPA_SDMSV_DSMNF)

    def test_should_datapoint_match_any_sample_variable_success_already_detected_pid(self):
        ''' should_datapoint_match_any_sample_variable should succeed if pid already was detected in sample '''
        datasourcename='test_should_datapoint_match_any_sample_variable_success_already_detected_pid_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_should_datapoint_match_any_sample_variable_success_already_detected_pid_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertTrue(api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=date))

    def test_should_datapoint_match_any_sample_variable_success_pid_is_on_sample(self):
        ''' should_datapoint_match_any_sample_variable should succeed if pid is on sample '''
        datasourcename='test_should_datapoint_match_any_sample_variable_success_pid_is_on_sample_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_should_datapoint_match_any_sample_variable_success_pid_is_on_sample_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        new_date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=new_date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=new_date))
        self.assertTrue(api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=new_date))

    def test_should_datapoint_match_any_sample_variable_success_pid_maybe_is_on_sample(self):
        ''' should_datapoint_match_any_sample_variable should succeed if pid maybe is on sample '''
        datasourcename='test_should_datapoint_match_any_sample_variable_success_pid_maybe_is_on_sample_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=8
        length=2
        datapointname='test_should_datapoint_match_any_sample_variable_success_pid_maybe_is_on_sample_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        new_date=timeuuid.uuid1()
        content='content not related *23*, with the previous sample 231-(23).'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=new_date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=new_date))
        self.assertTrue(api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=new_date))

    def test_should_datapoint_match_any_sample_variable_success_pid_is_not_on_sample(self):
        ''' should_datapoint_match_any_sample_variable should succeed if pid is not on sample '''
        datasourcename='test_should_datapoint_match_any_sample_variable_success_pid_is_not_on_sample_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        content='content a: 23, b: 32, c: 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=date))
        #first var should be a position 8 and length 2
        position=11
        length=2
        datapointname='test_should_datapoint_match_any_sample_variable_success_pid_is_not_on_sample_datapoint'
        datapoint=api.monitor_new_datapoint(did=did, date=date, position=position, length=length, datapointname=datapointname)
        self.assertTrue(api.store_datasource_values(did=did, date=date))
        data=api.get_datapoint_data(pid=datapoint['pid'], fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        new_date=timeuuid.uuid1()
        content='content b: 32, c: 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=new_date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=new_date))
        self.assertFalse(api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=new_date))

