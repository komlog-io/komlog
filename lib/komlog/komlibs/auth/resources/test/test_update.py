import unittest
import uuid
from komlog.komlibs.auth import permissions
from komlog.komlibs.auth.resources import update
from komlog.komlibs.auth.model.operations import Operations
from komlog.komcass.api import permission as cassapiperm
from komlog.komcass.api import user as cassapiuser
from komlog.komcass.api import agent as cassapiagent
from komlog.komcass.api import datasource as cassapidatasource
from komlog.komcass.api import datapoint as cassapidatapoint
from komlog.komcass.api import widget as cassapiwidget
from komlog.komcass.api import dashboard as cassapidashboard
from komlog.komcass.api import circle as cassapicircle
from komlog.komcass.model.orm import user as ormuser
from komlog.komcass.model.orm import agent as ormagent
from komlog.komcass.model.orm import datasource as ormdatasource
from komlog.komcass.model.orm import datapoint as ormdatapoint
from komlog.komcass.model.orm import widget as ormwidget
from komlog.komcass.model.orm import dashboard as ormdashboard
from komlog.komcass.model.orm import circle as ormcircle


class AuthResourcesUpdateTest(unittest.TestCase):
    ''' komlog.auth.resources.update tests '''
    
    def test_get_update_funcs_success(self):
        ''' test_update_funcs should return a list of functions '''
        operation=Operations.NEW_AGENT
        update_funcs=update.get_update_funcs(operation=operation)
        self.assertTrue(isinstance(update_funcs, tuple))

    def test_get_update_funcs_success_empty_list(self):
        '''test_update_funcs should return an empty list of functions if operation does not exist'''
        operation='234234234'
        self.assertRaises( KeyError, update.get_update_funcs, operation)

    def test_new_agent_no_uid(self):
        ''' new_agent should fail if no uid is passed'''
        params={'aid':uuid.uuid4()}
        self.assertFalse(update.new_agent(params))

    def test_new_agent_no_aid(self):
        ''' new_agent should fail if no aid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_agent(params))

    def test_new_agent_success(self):
        ''' new_agent should succeed if permissions can be set'''
        uid=uuid.uuid4()
        aid=uuid.uuid4()
        params={'uid':uid,'aid':aid}
        self.assertTrue(update.new_agent(params))
        permission=cassapiperm.get_user_agent_perm(uid=uid, aid=aid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_new_datasource_no_uid(self):
        ''' new_datasource should fail if no uid is passed'''
        params={'aid':uuid.uuid4(),'did':uuid.uuid4()}
        self.assertFalse(update.new_datasource(params))

    def test_new_datasource_no_did(self):
        ''' new_datasource should fail if no did is passed'''
        params={'uid':uuid.uuid4(),'aid':uuid.uuid4()}
        self.assertFalse(update.new_datasource(params))

    def test_new_datasource_success(self):
        ''' new_datasource should succeed if permissions can be set'''
        uid=uuid.uuid4()
        did=uuid.uuid4()
        params={'uid':uid,'did':did}
        self.assertTrue(update.new_datasource(params))
        permission=cassapiperm.get_user_datasource_perm(uid=uid, did=did)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_new_datasource_datapoint_no_uid(self):
        ''' new_datasource_datapoint should fail if no uid is passed'''
        params={'pid':uuid.uuid4()}
        self.assertFalse(update.new_datasource_datapoint(params))

    def test_new_datasource_datapoint_no_pid(self):
        ''' new_datasource_datapoint should fail if no uid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_datasource_datapoint(params))

    def test_new_datasource_datapoint_success(self):
        ''' new_datasource_datapoint should succeed if permissions can be set'''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        params={'uid':uid,'pid':pid}
        self.assertTrue(update.new_datasource_datapoint(params))
        permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_new_user_datapoint_no_uid(self):
        ''' new_user_datapoint should fail if no uid is passed'''
        params={'pid':uuid.uuid4()}
        self.assertFalse(update.new_user_datapoint(params))

    def test_new_user_datapoint_no_pid(self):
        ''' new_user_datapoint should fail if no pid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_user_datapoint(params))

    def test_new_user_datapoint_success(self):
        ''' new_user_datapoint should succeed if permissions can be set'''
        uid=uuid.uuid4()
        pid=uuid.uuid4()
        params={'uid':uid,'pid':pid}
        self.assertTrue(update.new_user_datapoint(params))
        permission=cassapiperm.get_user_datapoint_perm(uid=uid, pid=pid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_new_widget_no_uid(self):
        ''' new_widget should fail if no uid is passed'''
        params={'wid':uuid.uuid4()}
        self.assertFalse(update.new_widget(params))

    def test_new_widget_no_wid(self):
        ''' new_widget should fail if no wid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_widget(params))

    def test_new_widget_success(self):
        ''' new_widget should succeed if permissions can be set'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        params={'uid':uid,'wid':wid}
        self.assertTrue(update.new_widget(params))
        permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE | permissions.CAN_SNAPSHOT))

    def test_new_dashboard_no_uid(self):
        ''' new_dahsboard should fail if no uid is passed'''
        params={'bid':uuid.uuid4()}
        self.assertFalse(update.new_dashboard(params))

    def test_new_dashboard_no_bid(self):
        ''' new_dahsboard should fail if no bid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_dashboard(params))

    def test_new_dashboard_success(self):
        ''' new_dashboard should succeed if permissions can be set'''
        uid=uuid.uuid4()
        bid=uuid.uuid4()
        params={'uid':uid,'bid':bid}
        self.assertTrue(update.new_dashboard(params))
        permission=cassapiperm.get_user_dashboard_perm(uid=uid, bid=bid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_new_widget_system_no_uid(self):
        ''' new_widget_system should fail if no uid is passed'''
        params={'wid':uuid.uuid4()}
        self.assertFalse(update.new_widget_system(params))

    def test_new_widget_system_no_wid(self):
        ''' new_widget_system should fail if no wid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_widget_system(params))

    def test_new_widget_system_success(self):
        ''' new_widget_system should succeed if permissions can be set'''
        uid=uuid.uuid4()
        wid=uuid.uuid4()
        params={'uid':uid,'wid':wid}
        self.assertTrue(update.new_widget_system(params))
        permission=cassapiperm.get_user_widget_perm(uid=uid, wid=wid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ|permissions.CAN_SNAPSHOT))

    def test_new_snapshot_no_uid(self):
        ''' new_snapshot should fail if no uid is passed'''
        params={'nid':uuid.uuid4()}
        self.assertFalse(update.new_snapshot(params))

    def test_new_snapshot_no_nid(self):
        ''' new_widget should fail if no wid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_snapshot(params))

    def test_new_snapshot_success(self):
        ''' new_snapshot should succeed if permissions can be set'''
        uid=uuid.uuid4()
        nid=uuid.uuid4()
        params={'uid':uid,'nid':nid}
        self.assertTrue(update.new_snapshot(params))
        permission=cassapiperm.get_user_snapshot_perm(uid=uid, nid=nid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_delete_user_success(self):
        ''' delete_user should revoke all user and agents permissions '''
        uid=uuid.uuid4()
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            for i in range(0,100):
                did=uuid.uuid4()
                datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                cassapidatasource.insert_datasource(datasource)
                cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                for i in range(0,10):
                    pid=uuid.uuid4()
                    datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                    cassapidatapoint.insert_datapoint(datapoint)
                    cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,100):
            wid=uuid.uuid4()
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(update.delete_user(uid=uid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.NONE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.NONE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),3000)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.NONE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),100)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.NONE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),100)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.NONE)

    def test_delete_agent_success(self):
        ''' delete_agent should revoke permission to the agent '''
        uid=uuid.uuid4()
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        selected_aid=aids[0]
        selected_dids=[]
        selected_pids=[]
        selected_wids=[]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            if aid==selected_aid:
                for i in range(0,100):
                    did=uuid.uuid4()
                    selected_dids.append(did)
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    wid=uuid.uuid4()
                    widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=did.hex, creation_date=uuid.uuid1(), did=did)
                    cassapiwidget.insert_widget(widget)
                    selected_wids.append(wid)
                    cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        selected_pids.append(pid)
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
                        wid=uuid.uuid4()
                        widget=ormwidget.WidgetDp(wid=wid, uid=uid, widgetname=pid.hex, creation_date=uuid.uuid1(), pid=pid)
                        cassapiwidget.insert_widget(widget)
                        selected_wids.append(wid)
                        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            else:
                for i in range(0,100):
                    did=uuid.uuid4()
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,100):
            wid=uuid.uuid4()
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        aid=selected_aid
        self.assertTrue(update.delete_agent(aid=aid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            if item.aid==aid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            if item.did in selected_dids:
                # we keep the same perms to the elements "created" by the deleted agent, because they can be accessed by other agents. Datasources DO NOT belong to agents.
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),3000)
        for item in perm_list:
            if item.pid in selected_pids:
                # we keep the same perms to the elements "created" by the deleted agent, because they can be accessed by other agents. Datapoints DO NOT belong to agents.
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),1200)
        for item in perm_list:
            if item.wid in selected_wids:
                # we keep the same perms to the elements "created" by the deleted agent, because they can be accessed by other agents. Widgets DO NOT belong to agents.
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),100)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_delete_widget_success(self):
        ''' delete_widget should revoke access to the selected widget '''
        uid=uuid.uuid4()
        selected_wid=None
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            for i in range(0,10):
                did=uuid.uuid4()
                datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                cassapidatasource.insert_datasource(datasource)
                cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                for i in range(0,10):
                    pid=uuid.uuid4()
                    datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                    cassapidatapoint.insert_datapoint(datapoint)
                    cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,10):
            wid=uuid.uuid4()
            if i==0:
                selected_wid=wid
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(update.delete_widget(wid=selected_wid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),30)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            if item.wid==selected_wid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_delete_dashboard_success(self):
        ''' delete_dashboard should revoke access to the selected dashboard '''
        uid=uuid.uuid4()
        selected_bid=None
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            for i in range(0,10):
                did=uuid.uuid4()
                datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                cassapidatasource.insert_datasource(datasource)
                cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                for i in range(0,10):
                    pid=uuid.uuid4()
                    datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                    cassapidatapoint.insert_datapoint(datapoint)
                    cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,10):
            wid=uuid.uuid4()
            bid=uuid.uuid4()
            if i==0:
                selected_bid=bid
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(update.delete_dashboard(bid=selected_bid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),30)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            if item.bid==selected_bid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_delete_datasource_success(self):
        ''' delete_datasource should revoke permission to the user and agents to the datasource and its datapoints (and their associated widgetds and widgetdp '''
        uid=uuid.uuid4()
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        selected_aid=aids[0]
        selected_did=None
        selected_pids=[]
        selected_wids=[]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            if aid==selected_aid:
                for i in range(0,100):
                    did=uuid.uuid4()
                    wid=uuid.uuid4()
                    if i == 0:
                        selected_did=did
                        selected_wids.append(wid)
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=did.hex, creation_date=uuid.uuid1(), did=did)
                    cassapiwidget.insert_widget(widget)
                    cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        wid=uuid.uuid4()
                        if did == selected_did:
                            selected_pids.append(pid)
                            selected_wids.append(wid)
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
                        widget=ormwidget.WidgetDp(wid=wid, uid=uid, widgetname=pid.hex, creation_date=uuid.uuid1(), pid=pid)
                        cassapiwidget.insert_widget(widget)
                        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            else:
                for i in range(0,100):
                    did=uuid.uuid4()
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,100):
            wid=uuid.uuid4()
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        did=selected_did
        self.assertTrue(update.delete_datasource(did=did))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            if item.did == selected_did:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),3000)
        for item in perm_list:
            if item.pid in selected_pids:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),1200)
        for item in perm_list:
            if item.wid in selected_wids:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),100)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_delete_datapoint_success(self):
        ''' delete_point should revoke permission to the user and agents to the datapoint (and widgetdp) '''
        uid=uuid.uuid4()
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        selected_aid=aids[0]
        selected_did=None
        selected_pid=None
        selected_wid=None
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            if aid==selected_aid:
                for i in range(0,100):
                    did=uuid.uuid4()
                    wid=uuid.uuid4()
                    if i == 0:
                        selected_did=did
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=did.hex, creation_date=uuid.uuid1(), did=did)
                    cassapiwidget.insert_widget(widget)
                    cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        wid=uuid.uuid4()
                        if i == 0 and did == selected_did:
                            selected_pid=pid
                            selected_wid=wid
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
                        widget=ormwidget.WidgetDp(wid=wid, uid=uid, widgetname=pid.hex, creation_date=uuid.uuid1(), pid=pid)
                        cassapiwidget.insert_widget(widget)
                        cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            else:
                for i in range(0,100):
                    did=uuid.uuid4()
                    datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                    cassapidatasource.insert_datasource(datasource)
                    cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                    for i in range(0,10):
                        pid=uuid.uuid4()
                        datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                        cassapidatapoint.insert_datapoint(datapoint)
                        cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,100):
            wid=uuid.uuid4()
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        pid=selected_pid
        self.assertTrue(update.delete_datapoint(pid=pid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),3000)
        for item in perm_list:
            if item.pid == selected_pid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),1200)
        for item in perm_list:
            if item.wid == selected_wid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),100)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_delete_snapshot_success(self):
        ''' delete_snapshot should revoke access to the selected snapshot '''
        uid=uuid.uuid4()
        selected_wid=None
        aids=[uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        for aid in aids:
            agent=ormagent.Agent(aid=aid, uid=uid, agentname=aid.hex)
            cassapiagent.insert_agent(agent)
            cassapiperm.insert_user_agent_perm(uid=uid, aid=aid, perm=perm)
        for aid in aids:
            for i in range(0,10):
                did=uuid.uuid4()
                datasource=ormdatasource.Datasource(did=did, aid=aid, uid=uid, datasourcename=did.hex)
                cassapidatasource.insert_datasource(datasource)
                cassapiperm.insert_user_datasource_perm(uid=uid, did=did, perm=perm)
                for i in range(0,10):
                    pid=uuid.uuid4()
                    datapoint=ormdatapoint.Datapoint(pid=pid, did=did, uid=uid, datapointname=pid.hex)
                    cassapidatapoint.insert_datapoint(datapoint)
                    cassapiperm.insert_user_datapoint_perm(uid=uid, pid=pid, perm=perm)
        for i in range(0,10):
            wid=uuid.uuid4()
            if i==0:
                selected_wid=wid
            bid=uuid.uuid4()
            widget=ormwidget.WidgetDs(wid=wid, uid=uid, widgetname=wid.hex, creation_date=uuid.uuid1(), did=uuid.uuid4())
            cassapiwidget.insert_widget(widget)
            dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, dashboardname=bid.hex,creation_date=uuid.uuid1())
            cassapidashboard.insert_dashboard(dashboard)
            cassapiperm.insert_user_widget_perm(uid=uid, wid=wid, perm=perm)
            cassapiperm.insert_user_dashboard_perm(uid=uid, bid=bid, perm=perm)
        self.assertTrue(update.delete_widget(wid=selected_wid))
        perm_list=cassapiperm.get_user_agents_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datasources_perm(uid=uid)
        self.assertEqual(len(perm_list),30)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_datapoints_perm(uid=uid)
        self.assertEqual(len(perm_list),300)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_widgets_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            if item.wid==selected_wid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)
        perm_list=cassapiperm.get_user_dashboards_perm(uid=uid)
        self.assertEqual(len(perm_list),10)
        for item in perm_list:
            self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

    def test_new_circle_no_uid(self):
        ''' new_circle should fail if no uid is passed'''
        params={'cid':uuid.uuid4()}
        self.assertFalse(update.new_circle(params))

    def test_new_circle_no_cid(self):
        ''' new_widget should fail if no cid is passed'''
        params={'uid':uuid.uuid4()}
        self.assertFalse(update.new_circle(params))

    def test_new_circle_success(self):
        ''' new_circle should succeed if permissions can be set'''
        uid=uuid.uuid4()
        cid=uuid.uuid4()
        params={'uid':uid,'cid':cid}
        self.assertTrue(update.new_circle(params))
        permission=cassapiperm.get_user_circle_perm(uid=uid, cid=cid)
        self.assertIsNotNone(permission)
        self.assertTrue(permission.perm & (permissions.CAN_READ | permissions.CAN_EDIT| permissions.CAN_DELETE))

    def test_delete_circle_success(self):
        ''' delete_circle should revoke permission to the user to the circle '''
        uid=uuid.uuid4()
        cids=[uuid.uuid4(),uuid.uuid4(), uuid.uuid4()]
        perm=permissions.CAN_READ | permissions.CAN_EDIT | permissions.CAN_DELETE
        members=None
        type='a type for a circle'
        for cid in cids:
            creation_date=uuid.uuid1()
            circle=ormcircle.Circle(cid=cid, uid=uid, circlename=cid.hex,creation_date=creation_date,type=type,members=members)
            cassapicircle.insert_circle(circle)
            cassapiperm.insert_user_circle_perm(uid=uid, cid=cid, perm=perm)
        selected_cid=cids[0]
        self.assertTrue(update.delete_circle(cid=selected_cid))
        perm_list=cassapiperm.get_user_circles_perm(uid=uid)
        self.assertEqual(len(perm_list),3)
        for item in perm_list:
            if item.cid==selected_cid:
                self.assertEqual(item.perm, permissions.NONE)
            else:
                self.assertEqual(item.perm, permissions.CAN_READ|permissions.CAN_EDIT|permissions.CAN_DELETE)

