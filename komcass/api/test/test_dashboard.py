import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import dashboard as dashboardapi
from komcass.model.orm import dashboard as ormdashboard


class KomcassApiDashboardTest(unittest.TestCase):
    ''' komlog.komcass.api.dashboard tests '''

    def setUp(self):
        bid1=uuid.uuid4()
        bid2=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        name1='test_komlog.komcass.api.dashboard_dashboard1'
        name2='test_komlog.komcass.api.dashboard_dashboard2'
        self.dashboard1=ormdashboard.Dashboard(bid=bid1, uid=uid, creation_date=creation_date, dashboardname=name1)
        self.dashboard2=ormdashboard.Dashboard(bid=bid2, uid=uid, creation_date=creation_date, dashboardname=name2)
        dashboardapi.insert_dashboard(self.dashboard1)
        dashboardapi.insert_dashboard(self.dashboard2)
        dashboardapi.add_widget_to_dashboard(wid=uuid.uuid4(),bid=bid2)
        dashboardapi.add_widget_to_dashboard(wid=uuid.uuid4(),bid=bid2)

    def test_get_dashboard_existing_bid(self):
        ''' get_dashboard should succeed if we pass an existing bid '''
        bid=self.dashboard1.bid
        dashboard=dashboardapi.get_dashboard(bid=bid)
        self.assertEqual(dashboard.bid, self.dashboard1.bid)
        self.assertEqual(dashboard.uid, self.dashboard1.uid)
        self.assertEqual(dashboard.dashboardname, self.dashboard1.dashboardname)

    def test_get_dashboard_non_existing_bid(self):
        ''' get_dashboard should return None if we pass a non existing bid '''
        bid=uuid.uuid4()
        self.assertIsNone(dashboardapi.get_dashboard(bid=bid))

    def test_get_dashboards_existing_uid(self):
        ''' get_dashboards should succeed if we pass an existing uid '''
        uid=self.dashboard1.uid
        dashboards=dashboardapi.get_dashboards(uid=uid)
        self.assertEqual(len(dashboards),2)
        for dashboard in dashboards:
            self.assertTrue(isinstance(dashboard, ormdashboard.Dashboard))

    def test_get_dashboards_non_existing_uid(self):
        ''' get_dashboards should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        dashboards=dashboardapi.get_dashboards(uid=uid)
        self.assertTrue(isinstance(dashboards,list))
        self.assertEqual(len(dashboards),0)

    def test_get_number_of_dashboards_by_uid_non_existent_uid(self):
        ''' get_number_of_dashboards by uid should return 0 if uid does not exist '''
        uid=uuid.uuid4()
        num_dashboards=dashboardapi.get_number_of_dashboards_by_uid(uid)
        self.assertEqual(num_dashboards, 0)

    def test_get_number_of_dashboards_by_uid_success(self):
        ''' get_number_of_dashboards by uid should return the number of dashboards belonging to a uid '''
        uid=self.dashboard1.uid
        num_dashboards=dashboardapi.get_number_of_dashboards_by_uid(uid)
        self.assertEqual(num_dashboards, 2)

    def test_get_number_of_dashboards_by_uid_no_dashboards(self):
        ''' get_number_of_dashboards by uid should return the number of dashboards belonging to a uid '''
        uid=uuid.uuid4()
        num_dashboards=dashboardapi.get_number_of_dashboards_by_uid(uid)
        self.assertEqual(num_dashboards, 0)

    def test_get_dashboard_widgets_non_existing_dashboard(self):
        ''' get_dashboard_widgets should return an empty list if no existing bid is passed '''
        bid=uuid.uuid4()
        self.assertEqual(dashboardapi.get_dashboard_widgets(bid),[])

    def test_get_dashboard_widgets_no_widgets(self):
        ''' get_dashboard_widgets should return None if dashboard has no widgets '''
        bid=self.dashboard1.bid
        widgets=dashboardapi.get_dashboard_widgets(bid=bid)
        self.assertEqual(widgets,[])

    def test_get_dashboard_widgets_some_widgets(self):
        ''' get_dashboard_widgets should return a list with dasbhoard's widgets '''
        bid=self.dashboard2.bid
        widgets=dashboardapi.get_dashboard_widgets(bid)
        self.assertTrue(widgets,list)
        self.assertEqual(len(widgets),2)

    def test_delete_dashboard_non_existent_dashboard(self):
        ''' delete_dashboard should return True even if we try to delete a non existent dashboard '''
        bid=uuid.uuid4()
        self.assertIsNone(dashboardapi.get_dashboard(bid))
        self.assertTrue(dashboardapi.delete_dashboard(bid))

    def test_delete_dashboard_existent_dashboard(self):
        ''' delete_dashboard should return True when a dashboard is deleted successfully '''
        bid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_delete_dashboard_existent_dashboard_dashboard'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        dashboardapi.new_dashboard(dashboard)
        self.assertIsNotNone(dashboardapi.get_dashboard(bid))
        self.assertTrue(dashboardapi.delete_dashboard(bid))
        self.assertIsNone(dashboardapi.get_dashboard(bid))

    def test_new_dashboard_no_dashboard_obj(self):
        ''' new_dashboard should fail if we pass no dashboard object as argument '''
        dashboards=[None, 'qrqerqwerqw234234', 234234234, {'a':'dict'}, ['a','list']]
        for dashboard in dashboards:
            self.assertFalse(dashboardapi.new_dashboard(dashboard))

    def test_new_dashboard_dashboard_obj(self):
        ''' new_dashboard should return True when a dashboard is created successfully '''
        bid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_new_dashboard_dashboard_obj'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))

    def test_insert_dashboard_no_dashboard_obj(self):
        ''' insert_dashboard should fail if we pass no dashboard object as argument '''
        dashboards=[None, 'qrqerqwerqw234234', 234234234, {'a':'dict'}, ['a','list']]
        for dashboard in dashboards:
            self.assertFalse(dashboardapi.insert_dashboard(dashboard))

    def test_insert_dashboard_dashboard_obj(self):
        ''' insert_dashboard should return True when a dashboard is updated successfully '''
        bid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_insert_dashboard_dashboard_obj'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))
        self.assertTrue(dashboardapi.insert_dashboard(dashboard))

    def test_add_widget_to_dashboard(self):
        ''' add_widget_to_dashboard should fail if dashboard does not exist '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertFalse(dashboardapi.add_widget_to_dashboard(wid=wid, bid=bid))

    def test_add_widget_to_dashboard_no_previous_widgets(self):
        ''' add_widget_to_dashboard should succeed if dashboard exists and has no widgets yet'''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_insert_dashboard_dashboard_obj'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))
        self.assertTrue(dashboardapi.add_widget_to_dashboard(wid=wid, bid=bid))
        self.assertTrue(wid in dashboardapi.get_dashboard_widgets(bid=bid))

    def test_add_widget_to_dashboard_already_has_widgets(self):
        ''' add_widget_to_dashboard should succeed if dashboard exists and has already widgets '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_insert_dashboard_dashboard_obj'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))
        self.assertTrue(dashboardapi.add_widget_to_dashboard(wid=uuid.uuid4(), bid=bid))
        self.assertTrue(dashboardapi.add_widget_to_dashboard(wid=wid, bid=bid))
        self.assertTrue(wid in dashboardapi.get_dashboard_widgets(bid=bid))

    def test_delete_widget_from_dashboard(self):
        ''' delete_widget_from_dashboard should return True even if dashboard does not exist '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertTrue(dashboardapi.delete_widget_from_dashboard(wid=wid, bid=bid))

    def test_delete_widget_from_dashboard_no_previous_widgets(self):
        ''' delete_widget_from_dashboard should return True if dashboard exists and has no widgets yet'''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_delete_widget_from_dashboard_no_previous_widgets_dashboard'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))
        self.assertIsNotNone(dashboardapi.get_dashboard(bid=bid))
        self.assertTrue(wid not in dashboardapi.get_dashboard_widgets(bid=bid))
        self.assertTrue(dashboardapi.delete_widget_from_dashboard(wid=wid, bid=bid))
        self.assertTrue(wid not in dashboardapi.get_dashboard_widgets(bid=bid))

    def test_delete_widget_from_dashboard_has_the_widget(self):
        ''' delete_widget_from_dashboard should return True if dashboard exists and has the widget we want to delete '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        dashboardname='test_delete_widget_from_dashboard_has_the_widget_dashboard'
        dashboard=ormdashboard.Dashboard(bid=bid, uid=uid, creation_date=creation_date, dashboardname=dashboardname)
        self.assertTrue(dashboardapi.new_dashboard(dashboard))
        self.assertTrue(dashboardapi.add_widget_to_dashboard(wid=uuid.uuid4(), bid=bid))
        self.assertTrue(dashboardapi.add_widget_to_dashboard(wid=wid, bid=bid))
        self.assertTrue(wid in dashboardapi.get_dashboard_widgets(bid=bid))
        self.assertTrue(dashboardapi.delete_widget_from_dashboard(wid=wid, bid=bid))
        self.assertTrue(wid not in dashboardapi.get_dashboard_widgets(bid=bid))

