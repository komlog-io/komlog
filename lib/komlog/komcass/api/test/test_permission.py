import unittest
import uuid
from komlog.komcass.api import permission as permissionapi
from komlog.komcass.model.orm import permission as ormpermission


class KomcassApiPermissionTest(unittest.TestCase):
    ''' komlog.komcass.api.permission tests '''

    def test_get_user_agent_perm_non_existing_aid(self):
        ''' get_user_agent_perm should return None if aid does not exist '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_agent_perm(uid=uid, aid=aid2))

    def test_get_user_agent_perm_non_existing_uid(self):
        ''' get_user_agent_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_agent_perm(uid=uid, aid=aid))

    def test_get_user_agent_perm_success(self):
        ''' get_user_agent_perm should return a UserAgentPerm object if perm exists '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid2, perm=perm))
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid2, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid1, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_agents_perm_non_existing_uid(self):
        ''' get_user_agents_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_agents_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_agents_perm_success(self):
        ''' get_user_agents_perm should return a UserAgentPerm objects list if uid has agents associated '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid2, perm=perm))
        perms=permissionapi.get_user_agents_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserAgentPerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserAgentPerm))

    def test_insert_user_agent_perm_success(self):
        ''' insert_user_agent_perm should return True '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid2, perm=perm))
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid1, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid2, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_agent_perm_success(self):
        ''' delete_user_agent_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid2, perm=perm))
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid1, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_agent_perm(uid=uid, aid=aid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserAgentPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(aid2, perm_db.aid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_agent_perm(uid=uid, aid=aid1))
        self.assertIsNone(permissionapi.get_user_agent_perm(uid=uid, aid=aid1))
        self.assertTrue(permissionapi.delete_user_agent_perm(uid=uid, aid=aid2))
        self.assertIsNone(permissionapi.get_user_agent_perm(uid=uid, aid=aid2))

    def test_delete_user_agents_perm_success(self):
        ''' delete_user_agents_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        aid1=uuid.uuid4()
        aid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_agent_perm(uid=uid, aid=aid2, perm=perm))
        perms=permissionapi.get_user_agents_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_agents_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_agents_perm(uid=uid), [])

    def test_get_user_datasource_perm_non_existing_did(self):
        ''' get_user_datasource_perm should return None if did does not exist '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertIsNone(permissionapi.get_user_datasource_perm(uid=uid, did=did2))

    def test_get_user_datasource_perm_non_existing_uid(self):
        ''' get_user_datasource_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_datasource_perm(uid=uid, did=did))

    def test_get_user_datasource_perm_success(self):
        ''' get_user_datasource_perm should return a UserDatasourcePerm object if perm exists '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did2, perm=perm))
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did2, perm_db.did)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did1, perm_db.did)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_datasources_perm_non_existing_uid(self):
        ''' get_user_datasources_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_datasources_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_datasources_perm_success(self):
        ''' get_user_datasources_perm should return a UserDatasourcePerm objects list if uid has datasources associated '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did2, perm=perm))
        perms=permissionapi.get_user_datasources_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserDatasourcePerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserDatasourcePerm))

    def test_insert_user_datasource_perm_success(self):
        ''' insert_user_datasource_perm should return True '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did2, perm=perm))
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did1, perm_db.did)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did2, perm_db.did)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_datasource_perm_success(self):
        ''' delete_user_datasource_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did2, perm=perm))
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did1, perm_db.did)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datasource_perm(uid=uid, did=did2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatasourcePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(did2, perm_db.did)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_datasource_perm(uid=uid, did=did1))
        self.assertIsNone(permissionapi.get_user_datasource_perm(uid=uid, did=did1))
        self.assertTrue(permissionapi.delete_user_datasource_perm(uid=uid, did=did2))
        self.assertIsNone(permissionapi.get_user_datasource_perm(uid=uid, did=did2))

    def test_delete_user_datasources_perm_success(self):
        ''' delete_user_datasources_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        did1=uuid.uuid4()
        did2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datasource_perm(uid=uid, did=did2, perm=perm))
        perms=permissionapi.get_user_datasources_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_datasources_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_datasources_perm(uid=uid), [])

    def test_get_user_datapoint_perm_non_existing_pid(self):
        ''' get_user_datapoint_perm should return None if pid does not exist '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_datapoint_perm(uid=uid, pid=pid2))

    def test_get_user_datapoint_perm_non_existing_uid(self):
        ''' get_user_datapoint_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_datapoint_perm(uid=uid, pid=pid))

    def test_get_user_datapoint_perm_success(self):
        ''' get_user_datapoint_perm should return a UserDatapointPerm object if perm exists '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid2, perm=perm))
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid2, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid1, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_datapoints_perm_non_existing_uid(self):
        ''' get_user_datapoints_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_datapoints_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_datapoints_perm_success(self):
        ''' get_user_datapoints_perm should return a UserDatapointPerm objects list if uid has datapoints associated '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid2, perm=perm))
        perms=permissionapi.get_user_datapoints_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserDatapointPerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserDatapointPerm))

    def test_insert_user_datapoint_perm_success(self):
        ''' insert_user_datapoint_perm should return True '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid2, perm=perm))
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid1, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid2, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_datapoint_perm_success(self):
        ''' delete_user_datapoint_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid2, perm=perm))
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid1, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_datapoint_perm(uid=uid, pid=pid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDatapointPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(pid2, perm_db.pid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_datapoint_perm(uid=uid, pid=pid1))
        self.assertIsNone(permissionapi.get_user_datapoint_perm(uid=uid, pid=pid1))
        self.assertTrue(permissionapi.delete_user_datapoint_perm(uid=uid, pid=pid2))
        self.assertIsNone(permissionapi.get_user_datapoint_perm(uid=uid, pid=pid2))

    def test_delete_user_datapoints_perm_success(self):
        ''' delete_user_datapoints_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        pid1=uuid.uuid4()
        pid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_datapoint_perm(uid=uid, pid=pid2, perm=perm))
        perms=permissionapi.get_user_datapoints_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_datapoints_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_datapoints_perm(uid=uid), [])

    def test_get_user_widget_perm_non_existing_wid(self):
        ''' get_user_widget_perm should return None if wid does not exist '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_widget_perm(uid=uid, wid=wid2))

    def test_get_user_widget_perm_non_existing_uid(self):
        ''' get_user_widget_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_widget_perm(uid=uid, wid=wid))

    def test_get_user_widget_perm_success(self):
        ''' get_user_widget_perm should return a UserWidgetPerm object if perm exists '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid2, perm=perm))
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid2, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid1, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_widgets_perm_non_existing_uid(self):
        ''' get_user_widgets_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_widgets_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_widgets_perm_success(self):
        ''' get_user_widgets_perm should return a UserWidgetPerm objects list if uid has widgets associated '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid2, perm=perm))
        perms=permissionapi.get_user_widgets_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserWidgetPerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserWidgetPerm))

    def test_insert_user_widget_perm_success(self):
        ''' insert_user_widget_perm should return True '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid2, perm=perm))
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid1, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid2, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_widget_perm_success(self):
        ''' delete_user_widget_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid2, perm=perm))
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid1, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_widget_perm(uid=uid, wid=wid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserWidgetPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(wid2, perm_db.wid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_widget_perm(uid=uid, wid=wid1))
        self.assertIsNone(permissionapi.get_user_widget_perm(uid=uid, wid=wid1))
        self.assertTrue(permissionapi.delete_user_widget_perm(uid=uid, wid=wid2))
        self.assertIsNone(permissionapi.get_user_widget_perm(uid=uid, wid=wid2))

    def test_delete_user_widgets_perm_success(self):
        ''' delete_user_widgets_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        wid1=uuid.uuid4()
        wid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_widget_perm(uid=uid, wid=wid2, perm=perm))
        perms=permissionapi.get_user_widgets_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_widgets_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_widgets_perm(uid=uid), [])

    def test_get_user_dashboard_perm_non_existing_bid(self):
        ''' get_user_dashboard_perm should return None if bid does not exist '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_dashboard_perm(uid=uid, bid=bid2))

    def test_get_user_dashboard_perm_non_existing_uid(self):
        ''' get_user_dashboard_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_dashboard_perm(uid=uid, bid=bid))

    def test_get_user_dashboard_perm_success(self):
        ''' get_user_dashboard_perm should return a UserDashboardPerm object if perm exists '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid2, perm=perm))
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid2, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid1, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_dashboards_perm_non_existing_uid(self):
        ''' get_user_dashboards_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_dashboards_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_dashboards_perm_success(self):
        ''' get_user_dashboards_perm should return a UserDashboardPerm objects list if uid has dashboards associated '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid2, perm=perm))
        perms=permissionapi.get_user_dashboards_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserDashboardPerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserDashboardPerm))

    def test_insert_user_dashboard_perm_success(self):
        ''' insert_user_dashboard_perm should return True '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid2, perm=perm))
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid1, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid2, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_dashboard_perm_success(self):
        ''' delete_user_dashboard_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid2, perm=perm))
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid1, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_dashboard_perm(uid=uid, bid=bid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserDashboardPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(bid2, perm_db.bid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_dashboard_perm(uid=uid, bid=bid1))
        self.assertIsNone(permissionapi.get_user_dashboard_perm(uid=uid, bid=bid1))
        self.assertTrue(permissionapi.delete_user_dashboard_perm(uid=uid, bid=bid2))
        self.assertIsNone(permissionapi.get_user_dashboard_perm(uid=uid, bid=bid2))

    def test_delete_user_dashboards_perm_success(self):
        ''' delete_user_dashboards_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_dashboard_perm(uid=uid, bid=bid2, perm=perm))
        perms=permissionapi.get_user_dashboards_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_dashboards_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_dashboards_perm(uid=uid), [])

    def test_get_user_snapshot_perm_non_existing_nid(self):
        ''' get_user_snapshot_perm should return None if nid does not exist '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_snapshot_perm(uid=uid, nid=nid2))

    def test_get_user_snapshot_perm_non_existing_uid(self):
        ''' get_user_snapshot_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_snapshot_perm(uid=uid, nid=nid))

    def test_get_user_snapshot_perm_success(self):
        ''' get_user_snapshot_perm should return a UserSnapshotPerm object if perm exists '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid2, perm=perm))
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid2, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid1, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_snapshots_perm_non_existing_uid(self):
        ''' get_user_snapshots_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_snapshots_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_snapshots_perm_success(self):
        ''' get_user_snapshots_perm should return a UserSnapshotPerm objects list if uid has snapshots associated '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid2, perm=perm))
        perms=permissionapi.get_user_snapshots_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserSnapshotPerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserSnapshotPerm))

    def test_insert_user_snapshot_perm_success(self):
        ''' insert_user_snapshot_perm should return True '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid2, perm=perm))
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid1, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid2, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_snapshot_perm_success(self):
        ''' delete_user_snapshot_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid2, perm=perm))
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid1, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_snapshot_perm(uid=uid, nid=nid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserSnapshotPerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(nid2, perm_db.nid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_snapshot_perm(uid=uid, nid=nid1))
        self.assertIsNone(permissionapi.get_user_snapshot_perm(uid=uid, nid=nid1))
        self.assertTrue(permissionapi.delete_user_snapshot_perm(uid=uid, nid=nid2))
        self.assertIsNone(permissionapi.get_user_snapshot_perm(uid=uid, nid=nid2))

    def test_delete_user_snapshots_perm_success(self):
        ''' delete_user_snapshots_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        nid1=uuid.uuid4()
        nid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_snapshot_perm(uid=uid, nid=nid2, perm=perm))
        perms=permissionapi.get_user_snapshots_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_snapshots_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_snapshots_perm(uid=uid), [])

    def test_get_user_circle_perm_non_existing_cid(self):
        ''' get_user_circle_perm should return None if cid does not exist '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertIsNone(permissionapi.get_user_circle_perm(uid=uid, cid=cid2))

    def test_get_user_circle_perm_non_existing_uid(self):
        ''' get_user_circle_perm should return None if uid does not exist '''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        self.assertIsNone(permissionapi.get_user_circle_perm(uid=uid, cid=cid))

    def test_get_user_circle_perm_success(self):
        ''' get_user_circle_perm should return a UserCirclePerm object if perm exists '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid2, perm=perm))
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid2, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid1, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)

    def test_get_user_circles_perm_non_existing_uid(self):
        ''' get_user_circles_perm should return an empty list if uid does not exist '''
        uid=uuid.uuid4()
        perms=permissionapi.get_user_circles_perm(uid=uid)
        self.assertEqual(perms, [])

    def test_get_user_circles_perm_success(self):
        ''' get_user_circles_perm should return a UserCirclePerm objects list if uid has circles associated '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid2, perm=perm))
        perms=permissionapi.get_user_circles_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(isinstance(perms[0], ormpermission.UserCirclePerm))
        self.assertTrue(isinstance(perms[1], ormpermission.UserCirclePerm))

    def test_insert_user_circle_perm_success(self):
        ''' insert_user_circle_perm should return True '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid2, perm=perm))
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid1, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid2, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)

    def test_delete_user_circle_perm_success(self):
        ''' delete_user_circle_perm should return True and delete perm successfully '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid2, perm=perm))
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid1)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid1, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)
        perm_db=permissionapi.get_user_circle_perm(uid=uid, cid=cid2)
        self.assertTrue(isinstance(perm_db, ormpermission.UserCirclePerm))
        self.assertEqual(uid, perm_db.uid)
        self.assertEqual(cid2, perm_db.cid)
        self.assertEqual(perm, perm_db.perm)
        self.assertTrue(permissionapi.delete_user_circle_perm(uid=uid, cid=cid1))
        self.assertIsNone(permissionapi.get_user_circle_perm(uid=uid, cid=cid1))
        self.assertTrue(permissionapi.delete_user_circle_perm(uid=uid, cid=cid2))
        self.assertIsNone(permissionapi.get_user_circle_perm(uid=uid, cid=cid2))

    def test_delete_user_circles_perm_success(self):
        ''' delete_user_circles_perm should return True and delete perms successfully '''
        uid=uuid.uuid4()
        cid1=uuid.uuid4()
        cid2=uuid.uuid4()
        perm=1
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid1, perm=perm))
        self.assertTrue(permissionapi.insert_user_circle_perm(uid=uid, cid=cid2, perm=perm))
        perms=permissionapi.get_user_circles_perm(uid=uid)
        self.assertTrue(isinstance(perms, list))
        self.assertEqual(len(perms), 2)
        self.assertTrue(permissionapi.delete_user_circles_perm(uid=uid))
        self.assertEqual(permissionapi.get_user_circles_perm(uid=uid), [])

