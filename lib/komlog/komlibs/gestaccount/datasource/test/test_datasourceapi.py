import unittest
import uuid
import random
from komlog.komfig import logging
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.agent import api as agentapi
from komlog.komlibs.gestaccount.widget import api as widgetapi
from komlog.komlibs.gestaccount.datapoint import api as datapointapi
from komlog.komlibs.gestaccount.datasource import api
from komlog.komlibs.gestaccount import exceptions
from komlog.komlibs.gestaccount.errors import Errors
from komlog.komlibs.general.time import timeuuid
from komlog.komlibs.general.crypto import crypto
from komlog.komcass.api import datasource as cassapidatasource

pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())

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
        ''' get_datasource_data should retrieve the content successfully '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='store_datasource_data content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['date'], date)
        self.assertEqual(data[0]['content'], content)

    def test_get_datasource_data_no_data_found(self):
        ''' get_datasource_data should fail if there is no data '''
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.get_datasource_data(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GDA_GDD_DDNF)

    def test_get_datasource_data_failure_invalid_did(self):
        ''' get_datasource_data should fail if did is not valid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_data(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDD_ID)

    def test_get_datasource_data_failure_invalid_fromdate(self):
        ''' get_datasource_data should fail if fromdate is not valid '''
        did=uuid.uuid4()
        dates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for fromdate in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_data(did=did, fromdate=fromdate)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDD_IFD)

    def test_get_datasource_data_failure_invalid_todate(self):
        ''' get_datasource_data should fail if todate is not valid '''
        did=uuid.uuid4()
        dates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for todate in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_data(did=did, todate=todate)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDD_ITD)

    def test_get_datasource_data_failure_invalid_count(self):
        ''' get_datasource_data should fail if count is not valid '''
        did=uuid.uuid4()
        counts=['asdfasd',-234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_data(did=did, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDD_ICNT)

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
        data=api.get_datasource_data(did=did, fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['date'], date)
        self.assertEqual(data[0]['content'], content)
        self.assertTrue(api.generate_datasource_map(did=did, date=date))

    def test_get_mapped_datasource_data_no_data_found(self):
        ''' get_mapped_datasource_data should fail if there is no data '''
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceDataNotFoundException) as cm:
            api.get_mapped_datasource_data(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GDA_GMDD_DDNF)

    def test_get_mapped_datasource_data_failure_invalid_did(self):
        ''' get_mapped_datasource_data should fail if did is not valid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_mapped_datasource_data(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GMDD_ID)

    def test_get_mapped_datasource_data_failure_invalid_fromdate(self):
        ''' get_mapped_datasource_data should fail if fromdate is not valid '''
        did=uuid.uuid4()
        dates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for fromdate in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_mapped_datasource_data(did=did, fromdate=fromdate)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GMDD_IFD)

    def test_get_mapped_datasource_data_failure_invalid_todate(self):
        ''' get_mapped_datasource_data should fail if todate is not valid '''
        did=uuid.uuid4()
        dates=['asdfasd',234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for todate in dates:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_mapped_datasource_data(did=did, todate=todate)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GMDD_ITD)

    def test_get_mapped_datasource_data_failure_invalid_count(self):
        ''' get_mapped_datasource_data should fail if count is not valid '''
        did=uuid.uuid4()
        counts=['asdfasd',-234234,234234.234,{'a':'dict'},['a','list'],{'set'},('tupl','e'),timeuuid.uuid1().hex,uuid.uuid4()]
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_mapped_datasource_data(did=did, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GMDD_ICNT)

    def test_get_mapped_datasource_data_success(self):
        ''' get_mapped_datasource_data should return the content '''
        did=uuid.uuid4()
        date=timeuuid.uuid1()
        content='generate_datasource_map content with ññññ and 23 32 554 and \nnew lines\ttabs\tetc..'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        data=api.get_datasource_data(did=did, fromdate=date, todate=date)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['date'], date)
        self.assertEqual(data[0]['content'], content)
        self.assertTrue(api.generate_datasource_map(did=did, date=date))
        data=api.get_mapped_datasource_data(did=did)
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]['date'], date)
        self.assertEqual(data[0]['content'], content)
        self.assertEqual(len(data[0]['variables']), 3)
        self.assertEqual(len(data[0]['datapoints']), 0)

    def test_hook_to_datasource_failure_invalid_did(self):
        ''' hook_to_datasource should fail if did is not valid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        sid=uuid.uuid4()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.hook_to_datasource(did=did, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GDA_HTDS_IDID)

    def test_hook_to_datasource_failure_invalid_sid(self):
        ''' hook_to_datasource should fail if sid is not valid '''
        sids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        did=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.hook_to_datasource(did=did, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GDA_HTDS_ISID)

    def test_hook_to_datasource_failure_datasource_not_found(self):
        ''' hook_to_datasource should fail if did is not found '''
        did=uuid.uuid4()
        sid=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.hook_to_datasource(did=did, sid=sid)
        self.assertEqual(cm.exception.error, Errors.E_GDA_HTDS_DSNF)

    def test_hook_to_datasource_success(self):
        ''' hook_to_datasource should succeed if did exists '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_hook_to_datasource_success'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(api.hook_to_datasource(did=did, sid=sid))
        did_hooks=cassapidatasource.get_datasource_hooks_sids(did=did)
        self.assertEqual(did_hooks,[sid])

    def test_unhook_from_datasource_failure_invalid_did(self):
        ''' unhook_from_datasource should fail if did is not valid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        sid=uuid.uuid4()
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.unhook_from_datasource(did=did, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UHFDS_IDID)

    def test_unhook_from_datasource_failure_invalid_sid(self):
        ''' unhook_from_datasource should fail if sid is not valid '''
        sids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        did=uuid.uuid4()
        for sid in sids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.unhook_from_datasource(did=did, sid=sid)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UHFDS_ISID)

    def test_unhook_from_datasource_success_hook_does_not_exist(self):
        ''' unhook_from_datasource should succeed if hook does not exist '''
        did=uuid.uuid4()
        sid=uuid.uuid4()
        self.assertTrue(api.unhook_from_datasource(did=did, sid=sid))

    def test_unhook_from_datasource_success_hook_does_exist(self):
        ''' unhook_from_datasource should succeed if hook exists '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_unhook_from_datasource_success_hook_does_exist'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        sid=uuid.uuid4()
        self.assertTrue(api.hook_to_datasource(did=did, sid=sid))
        did_hooks=cassapidatasource.get_datasource_hooks_sids(did=did)
        self.assertEqual(did_hooks,[sid])
        self.assertTrue(api.unhook_from_datasource(did=did, sid=sid))
        did_hooks=cassapidatasource.get_datasource_hooks_sids(did=did)
        self.assertEqual(did_hooks,[])

    def test_get_datasource_hooks_failure_invalid_did(self):
        ''' get_datasource_hooks should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_hooks(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDSH_IDID)

    def test_get_datasource_hooks_failure_datasource_not_found(self):
        ''' get_datasource_hooks should fail if datasource does not exist '''
        did=uuid.uuid4()
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.get_datasource_hooks(did=did)
        self.assertEqual(cm.exception.error, Errors.E_GDA_GDSH_DSNF)

    def test_get_datasource_hooks_success_some_hooks(self):
        ''' get_datasource_hooks should return the sid list of hooks '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_hooks_success_some_hooks'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        sids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        for sid in sids:
            self.assertTrue(api.hook_to_datasource(did=did, sid=sid))
        did_hooks=api.get_datasource_hooks(did=did)
        self.assertEqual(sorted(did_hooks),sorted(sids))

    def test_get_datasource_hooks_success_no_hooks(self):
        ''' get_datasource_hooks should return an empty list if no hook is found '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_hooks_success_no_hooks'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename) 
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        did_hooks=api.get_datasource_hooks(did=did)
        self.assertEqual(did_hooks,[])

    def test_update_datasource_supplies_failure_invalid_did(self):
        ''' update_datasource_supplies should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        supplies = []
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datasource_supplies(did=did, supplies=supplies)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UDSSUP_IDID)

    def test_update_datasource_supplies_failure_invalid_supplies_type(self):
        ''' update_datasource_supplies should fail if supplies is not a list '''
        did = uuid.uuid4()
        supplies_s=['asdfasd',234234,234234.234,{'a':'dict'},None,{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for supplies in supplies_s:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datasource_supplies(did=did, supplies=supplies)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UDSSUP_ISUPT)

    def test_update_datasource_supplies_failure_invalid_supplies_item(self):
        ''' update_datasource_supplies should fail if any supplies item is not a valid local uri '''
        did = uuid.uuid4()
        items = [
            'invalid uri'
            'global:uri',
            234234,
            234234.234,
            {'a':'dict'},
            None,
            {'set'},
            ('tupl','e'),
            timeuuid.uuid1(),
            uuid.uuid4()
        ]
        for item in items:
            supplies = [item]
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datasource_supplies(did=did, supplies=supplies)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UDSSUP_ISUPI)

    def test_update_datasource_supplies_failure_datasource_not_found(self):
        ''' update_datasource_supplies should fail if datasource does not exist '''
        did = uuid.uuid4()
        supplies = ['uri','other_uri']
        with self.assertRaises(exceptions.DatasourceNotFoundException) as cm:
            api.update_datasource_supplies(did=did, supplies=supplies)
        self.assertEqual(cm.exception.error, Errors.E_GDA_UDSSUP_DSNF)

    def test_update_datasource_supplies_success_previous_supplies_did_not_exist(self):
        ''' update_datasource_supplies should succeed and insert the new info '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_supplies_success_previous_supplies_did_not_exist'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        supplies = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, supplies)

    def test_update_datasource_supplies_success_previous_supplies_was_different_now_other_items(self):
        ''' update_datasource_supplies should succeed and insert the new info '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_supplies_success_previous_supplies_was_different_now_other_items'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        supplies = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, supplies)
        new_supplies = ['uri1','uri3','uri4']
        self.assertTrue(api.update_datasource_supplies(did, new_supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, new_supplies)

    def test_update_datasource_supplies_success_previous_supplies_was_different_now_none(self):
        ''' update_datasource_supplies should succeed and insert the new info '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_supplies_success_previous_supplies_was_different_now_none'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        supplies = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, supplies)
        new_supplies = []
        self.assertTrue(api.update_datasource_supplies(did, new_supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, new_supplies)

    def test_update_datasource_supplies_failure_previous_supplies_equal(self):
        ''' update_datasource_supplies should return False if previous supplies are equal '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_update_datasource_supplies_failure_previous_supplies_equal'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        supplies = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, supplies)
        new_supplies = ['uri2','uri1']
        self.assertFalse(api.update_datasource_supplies(did, new_supplies))
        current_sups = cassapidatasource.get_last_datasource_supplies_count(did, count=1)
        self.assertEqual(current_sups[0].supplies, sorted(new_supplies))

    def test_get_datasource_supplies_failure_invalid_did(self):
        ''' get_datasource_supplies should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_supplies(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDSSUP_IDID)

    def test_get_datasource_supplies_failure_invalid_count(self):
        ''' get_datasource_supplies should fail if count is not an integer or is less than 1'''
        did = uuid.uuid4()
        counts=['asdfasd',-234234,234234.234,{'a':'dict'},None,{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for count in counts:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.get_datasource_supplies(did=did, count=count)
            self.assertEqual(cm.exception.error, Errors.E_GDA_GDSSUP_ICNT)

    def test_get_datasource_supplies_success_none_found(self):
        ''' get_datasource_supplies should succeed and return the supplies list '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_supplies_success_none_found'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        count = 1
        supplies = api.get_datasource_supplies(did, count)
        self.assertEqual(supplies, [])

    def test_get_datasource_supplies_success_some_found_no_dups(self):
        ''' get_datasource_supplies should succeed and return the supplies list '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_supplies_success_some_found_no_dups'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        count = 1
        supplies = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies))
        supplies = api.get_datasource_supplies(did, count)
        self.assertEqual(supplies, supplies)

    def test_get_datasource_supplies_success_some_found_not_previous(self):
        ''' get_datasource_supplies should succeed and return the supplies list '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_supplies_success_some_found_not_previous'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        count = 1
        supplies1 = ['uri1','uri2']
        self.assertTrue(api.update_datasource_supplies(did, supplies1))
        supplies2 = ['uri3','uri4']
        self.assertTrue(api.update_datasource_supplies(did, supplies2))
        supplies = api.get_datasource_supplies(did, count)
        self.assertEqual(supplies, supplies2)

    def test_get_datasource_supplies_success_some_found_merge_and_delete_dups(self):
        ''' get_datasource_supplies should succeed and return the supplies list '''
        uid=self.user['uid']
        aid=self.agent['aid']
        datasourcename='test_get_datasource_supplies_success_some_found_merge_and_delete_dups'
        datasource=api.create_datasource(uid=uid, aid=aid, datasourcename=datasourcename)
        self.assertEqual(datasource['uid'],uid)
        self.assertEqual(datasource['datasourcename'],datasourcename)
        self.assertTrue('did' in datasource)
        did=datasource['did']
        count = 10
        supplies1 = ['uri1','uri2','uri3']
        self.assertTrue(api.update_datasource_supplies(did, supplies1))
        supplies2 = ['uri2','uri3','uri4']
        self.assertTrue(api.update_datasource_supplies(did, supplies2))
        supplies = api.get_datasource_supplies(did, count)
        self.assertEqual(supplies, sorted(set(supplies1+supplies2)))

    def test_update_datasource_features_failure_invalid_did(self):
        ''' update_datasource_features should fail if did is invalid '''
        dids=['asdfasd',234234,234234.234,{'a':'dict'},None,['a','list'],{'set'},('tupl','e'),timeuuid.uuid1(),uuid.uuid4().hex]
        for did in dids:
            with self.assertRaises(exceptions.BadParametersException) as cm:
                api.update_datasource_features(did=did)
            self.assertEqual(cm.exception.error, Errors.E_GDA_UDDSF_IDID)

    def test_update_datasource_features_success_no_datapoint_to_update_features(self):
        ''' update_datasource_features should not insert anything if no datapoint is found for it '''
        did = uuid.uuid4()
        result = api.update_datasource_features(did)
        self.assertEqual(result['features'],[])
        self.assertEqual(result['delete_prev'],False)
        self.assertEqual(result['insert_new'],False)
        self.assertEqual(result['insert_date'],None)
        self.assertEqual(result['did'],did)

    def test_update_datasource_features_success_one_datapoint_existed_no_previous_features(self):
        ''' update_datasource_features should insert the new ds features '''
        username='test_update_datasource_features_success_one_datapoint_existed_no_previous_features'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_update_datasource_features_success_one_datapoint_existed_no_previous_features'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=api.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='datapointname'
        datapoint=datapointapi.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='datapointX: 15, datapointY: 25'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=12
        length=2
        mark_result=datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        # we have a datasource with a datapoint identified. Lets update the ds features
        result = api.update_datasource_features(did)
        self.assertNotEqual(result['features'],[])
        self.assertEqual(result['delete_prev'],False)
        self.assertEqual(result['insert_new'],True)
        self.assertNotEqual(result['insert_date'],None)
        self.assertEqual(result['did'],did)

    def test_update_datasource_features_success_one_datapoint_existed_no_previous_features_run_twice(self):
        ''' update_datasource_features should insert the new ds features '''
        username='test_update_datasource_features_success_one_datapoint_existed_no_previous_features_run_twice'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_update_datasource_features_success_one_datapoint_existed_no_previous_features_run_twice'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=api.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='datapointname'
        datapoint=datapointapi.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='datapointX: 15, datapointY: 25'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=12
        length=2
        mark_result=datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        # we have a datasource with a datapoint identified. Lets update the ds features
        result = api.update_datasource_features(did)
        self.assertNotEqual(result['features'],[])
        self.assertEqual(result['delete_prev'],False)
        self.assertEqual(result['insert_new'],True)
        self.assertNotEqual(result['insert_date'],None)
        self.assertEqual(result['did'],did)
        # 2nd run
        result2 = api.update_datasource_features(did)
        self.assertEqual(result['features'],result2['features'])
        self.assertEqual(result2['delete_prev'],False)
        self.assertEqual(result2['insert_new'],True)
        self.assertNotEqual(result2['insert_date'],None)
        self.assertEqual(result2['did'],did)

    def test_update_datasource_features_success_features_modified(self):
        ''' update_datasource_features should insert the new ds features and delete old '''
        username='test_update_datasource_features_success_features_modified'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        agentname='test_update_datasource_features_success_features_modified'
        pubkey=crypto.serialize_public_key(crypto.generate_rsa_key().public_key())
        version='Test Version'
        agent=agentapi.create_agent(uid=user['uid'], agentname=agentname, pubkey=pubkey, version=version)
        datasourcename='datasourcename'
        datasource=api.create_datasource(uid=user['uid'], aid=agent['aid'], datasourcename=datasourcename)
        did=datasource['did']
        datapointname='datapointname'
        datapoint=datapointapi.create_datasource_datapoint(did=did,datapoint_uri=datapointname)
        date=timeuuid.uuid1()
        content='datapointX: 15, datapointY: 25'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=12
        length=2
        mark_result=datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        self.assertEqual(mark_result['conflicts'], [])
        self.assertEqual(mark_result['updated'], [did])
        self.assertEqual(mark_result['pending'], [])
        self.assertEqual(mark_result['classified'], [datapointname])
        self.assertEqual(mark_result['no_positive_tr_set'], [])
        self.assertIsNotNone(mark_result['dtree'])
        date=timeuuid.uuid1()
        content='datapointW: 15, datapointZ: 25'
        self.assertTrue(api.store_datasource_data(did=did, date=date, content=content))
        self.assertTrue(api.generate_datasource_map(did=did, date=date))
        #first var should be a position 45 and length 2
        position=12
        length=2
        mark_result=datapointapi.mark_positive_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        # we have a datasource with a datapoint identified. Lets update the ds features
        result = api.update_datasource_features(did)
        self.assertNotEqual(result['features'],[])
        self.assertEqual(result['delete_prev'],False)
        self.assertEqual(result['insert_new'],True)
        self.assertNotEqual(result['insert_date'],None)
        self.assertEqual(result['did'],did)
        # mark negative var, so that we can remove some features
        mark_result=datapointapi.mark_negative_variable(pid=datapoint['pid'], date=date, position=position, length=length)
        # 2nd run
        result2 = api.update_datasource_features(did)
        self.assertNotEqual(result2['features'],[])
        self.assertEqual(result2['delete_prev'],True)
        self.assertEqual(result2['insert_new'],True)
        self.assertNotEqual(result2['insert_date'],None)
        self.assertEqual(result2['did'],did)

