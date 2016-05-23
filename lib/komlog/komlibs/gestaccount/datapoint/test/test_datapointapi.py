import unittest
import uuid
import json
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komlibs.textman.api import variables as textmanvar
from komlog.komlibs.ai.decisiontree import api as dtreeapi
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

    def test_mark_positive_variable_success_one_other_datapoint_matched(self):
        ''' mark_positive_variable should succeed if other datapoint matched '''
        datasourcename='test_mark_positive_variable_success_one_other_datapoint_matched_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched'
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
        datapointname='test_mark_positive_variable_success_one_other_datapoint_matched_2'
        color='#FFDDAA'
        datapoint2=api.create_datapoint(did=did,datapointname=datapointname, color=color)
        dtp_to_update=api.mark_positive_variable(pid=datapoint2['pid'], date=date, position=position, length=length)
        self.assertEqual(sorted(dtp_to_update),sorted([datapoint2['pid'],datapoint['pid']]))

    def test_mark_missing_datapoint_failure_non_existent_datapoint(self):
        ''' mark_missing_datapoint should fail if datapoint does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        position=1
        length=1
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.mark_missing_datapoint(pid=pid, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_DNF)

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
        self.assertEqual(cm.exception.error, Errors.E_GPA_MMDP_DMNF)

    def test_generate_decision_tree_failure_invalid_pid(self):
        ''' generate_tree should fail if pid does not exists '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_decision_tree(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDT_IP)

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
        dshashes=cassapidatasource.get_datasource_hashes(did=did,fromdate=date,todate=date)
        self.assertEqual(len(dshashes),1)
        for dshash in dshashes:
            text_hash=json.loads(dshash.content)
            variables_atts=textmanvar.get_variables_atts(text_hash)
            for var in variables_atts:
                self.assertFalse(dtree.evaluate_row(var['atts'])) if var['text_pos']!=position else self.assertTrue(dtree.evaluate_row(var['atts']))

    def test_generate_inverse_decision_tree_failure_invalid_pid(self):
        ''' generate_decision_tree should fail if pid does not exists '''
        pids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_inverse_decision_tree(pid=pid)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GIDT_IP)

    def test_generate_inverse_decision_tree_failure_non_existent_datapoint(self):
        ''' generate_decision_tree should fail if pid does not exists '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.generate_inverse_decision_tree(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GIDT_DNF)

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
        self.assertEqual(cm.exception.error, Errors.E_GPA_GIDT_ETS)

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
        dshashes=cassapidatasource.get_datasource_hashes(did=did,fromdate=date,todate=date)
        self.assertEqual(len(dshashes),1)
        for dshash in dshashes:
            text_hash=json.loads(dshash.content)
            variables_atts=textmanvar.get_variables_atts(text_hash)
            for var in variables_atts:
                self.assertFalse(dtree_inv.evaluate_row(var['atts'])) if var['text_pos']==position else self.assertTrue(dtree_inv.evaluate_row(var['atts']))

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

    def test_store_datasource_values_failure_datasource_data_not_found(self):
        ''' store_datasource_values should fail if datasource data is not found '''
        datasourcename='test_store_datasource_values_failure_datasource_data_not_found'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        date=timeuuid.uuid1()
        datapointname='test_store_datasource_values_failure_dsdata_not_found'
        color='#FFDDAA'
        datapoint=api.create_datapoint(did=did, datapointname=datapointname, color=color)
        self.assertRaises(exceptions.DatasourceDataNotFoundException, api.store_datasource_values, did=did, date=date)

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
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDMSV_IP)

    def test_should_datapoint_match_any_sample_variable_failure_invalid_date(self):
        ''' should datapoint_match_any_sample_variable should fail if date is invalid '''
        dates=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_match_any_sample_variable(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDMSV_IDT)

    def test_should_datapoint_match_any_sample_variable_failure_non_existent_pid(self):
        ''' should datapoint_match_any_sample_variable should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.should_datapoint_match_any_sample_variable(pid=pid, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDMSV_DNF)

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
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDT_ETS)

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
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDMSV_DSMNF)

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
        content='content x: AA, b: 32, c: 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=new_date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=did, date=new_date))
        stats=cassapidatapoint.get_datapoint_stats(pid=datapoint['pid'])
        self.assertFalse(api.should_datapoint_match_any_sample_variable(pid=datapoint['pid'], date=new_date))

    def test_generate_datasource_text_summary_failure_invalid_did(self):
        ''' generate_datasource_text_summary should fail if did is not valid '''
        dids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_datasource_text_summary(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDTS_ID)

    def test_generate_datasource_text_summary_failure_invalid_date(self):
        ''' generate_datasource_text_summary should fail if date is not valid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),uuid.uuid4(), uuid.uuid4().hex]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.generate_datasource_text_summary(did=did, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDTS_IDT)

    def test_generate_datasource_text_summary_non_existent_datasource(self):
        ''' generate_datasource_text_summary should fail if did does not exist '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_text_summary(did=did, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDTS_DDNF)

    def test_generate_datasource_text_summary_non_existent_data_at_given_timeuuid(self):
        ''' generate_datasource_text_summary should fail if did has no sample at given timeuuid '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_generate_datasource_text_summary_non_existent_data_at_given_timeuuid'
        datasource=datasourceapi.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_text_summary(did=datasource['did'],date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDTS_DDNF)

    def test_generate_datasource_text_summary_success(self):
        ''' generate_datasource_text_summary should generate and store the summary successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='generate_datasource_text_summary content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=did, date=date, content=content))
        data=datasourceapi.get_datasource_data(did=did, date=date)
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
            self.assertEqual(cm.exception.error, Errors.E_GPA_GDNDFD_IP)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_non_existent_pid(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if pid does not exist '''
        pid=uuid.uuid4()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=pid)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDNDFD_DNF)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_non_datasource_data(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if no datasource data is found '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDNDFD_DSDNF)

    def test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found(self):
        ''' generate_datasource_novelty_detector_for_datapoint should fail if no text summary is found, raising an error when generating de novelty detector '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_failure_no_text_summaries_found_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        with self.assertRaises(exceptions.DatasourceNoveltyDetectorException) as cm:
            api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid'])
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDNDFD_NDF)

    def test_generate_datasource_novelty_detector_for_datapoint_success(self):
        ''' generate_datasource_novelty_detector_for_datapoint should succeed '''
        datasourcename='test_generate_datasource_novelty_detector_for_datapoint_success_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_generate_datasource_novelty_detector_for_datapoint_success_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        self.assertTrue(api.generate_datasource_novelty_detector_for_datapoint(pid=datapoint['pid']))
    def test_should_datapoint_appear_in_sample_failure_invalid_pid(self):
        ''' should_datapoint_appear_in_sample should fail if pid is invalid '''
        pids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for pid in pids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_appear_in_sample(pid=pid,date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDAIS_IP)

    def test_should_datapoint_appear_in_sample_failure_invalid_date(self):
        ''' should_datapoint_appear_in_sample should fail if date is invalid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'), uuid.uuid4().hex, uuid.uuid4()]
        pid=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.should_datapoint_appear_in_sample(pid=pid, date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_SDAIS_IDT)

    def test_should_datapoint_appear_in_sample_failure_non_existent_datapoint(self):
        ''' should_datapoint_appear_in_sample should fail if pid does not exist '''
        pid=uuid.uuid4()
        date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatapointNotFoundException) as cm:
            api.should_datapoint_appear_in_sample(pid=pid, date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_SDAIS_DNF)

    def test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found(self):
        ''' should_datapoint_appear_in_sample should fail if no novelty_detector is found '''
        datasourcename='test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_failure_no_novelty_detector_found_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        with self.assertRaises(exceptions.DatasourceNoveltyDetectorException) as cm:
            api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDNDFD_NDF)

    def test_should_datapoint_appear_in_sample_failure_no_text_summary_found(self):
        ''' should_datapoint_appear_in_sample should fail if no text summary is found '''
        datasourcename='test_should_datapoint_appear_in_sample_failure_no_text_summary_found_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_failure_no_text_summary_found_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_GDTS_DDNF)

    def test_should_datapoint_appear_in_sample_success_result_false(self):
        ''' should_datapoint_appear_in_sample should succeed and the result should be false '''
        datasourcename='test_should_datapoint_appear_in_sample_success_result_false_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_success_result_false_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        new_content='some content with no relation with previous other samples'
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertFalse(api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date))

    def test_should_datapoint_appear_in_sample_success_result_true(self):
        ''' should_datapoint_appear_in_sample should succeed and the result should be true '''
        datasourcename='test_should_datapoint_appear_in_sample_success_result_true_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_should_datapoint_appear_in_sample_success_result_true_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        for i in range(1,200):
            date=timeuuid.uuid1()
            content='mark_negative_variable content with ññññ and 23 32 554 and \nnew  lines\ttabs\tetc.. '+' '*int(i/2)+' something '+crypto.get_random_string(size=1)
            self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
            self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
            self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
            if i%100==0:
                #first var should be a position 45 and length 2
                position=45
                length=2
                self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
            self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_date=timeuuid.uuid1()
        new_content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.should_datapoint_appear_in_sample(pid=datapoint['pid'],date=new_date))

    def test_classify_missing_datapoints_in_sample_failure_invalid_did(self):
        ''' classify_missing_datapoints_in_sample should fail if did is invalid '''
        dids=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1(), uuid.uuid4().hex]
        date=timeuuid.uuid1()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.classify_missing_datapoints_in_sample(did=did,date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_CMDIS_ID)

    def test_classify_missing_datapoints_in_sample_failure_invalid_date(self):
        ''' classify_missing_datapoints_in_sample should fail if date is invalid '''
        dates=[None, '234234',23423,233.2324,{'a':'dict'},['a','list'],{'set'},('a','tuple'),timeuuid.uuid1().hex, uuid.uuid4()]
        did=uuid.uuid4()
        for date in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.classify_missing_datapoints_in_sample(did=did,date=date)
            self.assertEqual(cm.exception.error, Errors.E_GPA_CMDIS_IDT)

    def test_classify_missing_datapoints_in_sample_failure_dsmap_not_found(self):
        ''' classify_missing_datapoints_in_sample should fail if dsmap is not found '''
        date=timeuuid.uuid1()
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceMapNotFoundException) as cm:
            api.classify_missing_datapoints_in_sample(did=did,date=date)
        self.assertEqual(cm.exception.error, Errors.E_GPA_CMDIS_DSMNF)

    def test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_no_datapoint_left_to_classify_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        #self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[])

    def test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 45 and length 2
        position=45
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_content='some content with some variables 32 but nothing to do with previous 211 samples '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=new_date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[datapoint['pid']])

    def test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_discarded_2_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 45 and length 2
        position=48
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_content='mark_negative_variable content with ññññ and x: AA, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=new_date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['doubts'],[])
        self.assertEqual(result['discarded'],[datapoint['pid']])

    def test_classify_missing_datapoints_in_sample_success_pid_is_doubt(self):
        ''' classify_missing_datapoints_in_sample should succeed if no datapoint is left to classify, and return a dictionary with empty categories '''
        datasourcename='test_classify_missing_datapoints_in_sample_success_only_pid_is_doubt_datasource'
        datasource=datasourceapi.create_datasource(uid=self.user['uid'], aid=self.agent['aid'],datasourcename=datasourcename)
        self.assertTrue(isinstance(datasource,dict))
        datapointname='test_classify_missing_datapoints_in_sample_success_only_pid_is_doubt_datapoint'
        color='#FFDDEE'
        datapoint=api.create_datapoint(did=datasource['did'],datapointname=datapointname, color=color)
        date=timeuuid.uuid1()
        content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
        #first var should be a position 48 and length 2
        position=48
        length=2
        self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        for i in range(1,200):
            date=timeuuid.uuid1()
            content='mark_negative_variable content with ññññ and a: 23, b: 32, c: 554 and \nnew  lines\ttabs\tetc.. '+' '*int(i/2)+' something '+crypto.get_random_string(size=2)
            self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=date, content=content))
            self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=date))
            self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=date))
            if i%20==0:
                #first var should be a position 48 and length 2
                position=48
                length=2
                self.assertTrue(api.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length))
            self.assertTrue(api.store_datasource_values(did=datasource['did'],date=date))
        new_content='mark_negative_variable content with ññññ and x:30, b: 32, c: 554 and \nnew lines\ttabs\tetc.. 20 something '+crypto.get_random_string(size=10)
        new_date=timeuuid.uuid1()
        self.assertTrue(datasourceapi.store_datasource_data(did=datasource['did'], date=new_date, content=new_content))
        self.assertTrue(datasourceapi.generate_datasource_map(did=datasource['did'], date=new_date))
        self.assertTrue(api.generate_datasource_text_summary(did=datasource['did'],date=new_date))
        self.assertTrue(api.store_datasource_values(did=datasource['did'],date=new_date))
        result=api.classify_missing_datapoints_in_sample(did=datasource['did'], date=new_date)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(result['discarded'],[])
        self.assertEqual(result['doubts'],[datapoint['pid']])

