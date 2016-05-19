import unittest
import uuid
from komlog.komlibs.gestaccount.user import api as userapi
from komlog.komlibs.gestaccount.dashboard import api as dashboardapi
from komlog.komlibs.gestaccount import exceptions

class GestaccountDashboardApiTest(unittest.TestCase):
    ''' komlog.gestaccount.dashboard.api tests '''

    def test_get_dashboard_config_failure_invalid_bid(self):
        ''' get_dashboard_config should fail if bid is not valid '''
        bids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        for bid in bids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.get_dashboard_config, bid=bid)

    def test_get_dashboard_config_non_existent_dashboard(self):
        ''' get_dashboard_config should fail if bid is not in system '''
        bid=uuid.uuid4()
        self.assertRaises(exceptions.DashboardNotFoundException, dashboardapi.get_dashboard_config, bid=bid)

    def test_get_dashboard_config_success(self):
        ''' get_dashboard_config should succeed if bid exist and return dashboard config '''
        username='test_get_dashboard_config_success'
        dashboardname='test_get_dashboard_config_success'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname)
        bid=result['bid']
        config=dashboardapi.get_dashboard_config(bid=bid)
        self.assertEqual(config, {'uid':user['uid'],'bid':bid,'dashboardname':dashboardname,'wids':[]})

    def test_get_dashboards_config_failure_invalid_username(self):
        ''' get_dashboards_config should fail if username is not valid '''
        uids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), 'userñame','Username']
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.get_dashboards_config,uid=uid)

    def test_get_dashboards_config_non_existent_username(self):
        ''' get_dashboards_config should fail if username is not in system '''
        uid=uuid.uuid4()
        self.assertRaises(exceptions.UserNotFoundException, dashboardapi.get_dashboards_config,uid=uid)

    def test_get_dashboards_config_success_no_data(self):
        ''' get_dashboards_config should succeed if username exists, but returns and empty list if there is no dashboard '''
        username='test_get_dashboards_config_success_no_data_user'
        password='password'
        email=username+'@komlog.org'
        user=userapi.create_user(username=username, password=password, email=email)
        data=dashboardapi.get_dashboards_config(uid=user['uid'])
        self.assertEqual(data, [])

    def test_get_dashboard_config_success_some_dashboards(self):
        ''' get_dashboard_config should succeed and return dashboards config '''
        username='test_get_dashboard_config_success_some_dashboards'
        dashboardname1='test_get_dashboard_config_success_some_dashboards1'
        dashboardname2='test_get_dashboard_config_success_some_dashboards2'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname1)
        bid1=result['bid']
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname2)
        bid2=result['bid']
        config=dashboardapi.get_dashboards_config(uid=user['uid'])
        counter=0
        for element in config:
            if bid1==element['bid']:
                self.assertEqual(element,{'bid':bid1,'dashboardname':dashboardname1,'wids':[]})
                counter+=1
            elif bid2==element['bid']:
                self.assertEqual(element,{'bid':bid2,'dashboardname':dashboardname2,'wids':[]})
                counter+=1
        self.assertEqual(counter,2)

    def test_create_dashboard_failure_invalid_username(self):
        ''' create_dashboard should fail if username is invalid '''
        uids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), 'userñame','Username']
        dashboardname='test_create_dashboard_failure_invalid_username'
        for uid in uids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.create_dashboard,uid=uid, dashboardname=dashboardname)

    def test_create_dashboard_failure_invalid_dashboardname(self):
        ''' create_dashboard should fail if dashboardname is invalid '''
        dashboardnames=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4(), uuid.uuid1(), 'dashboardñame']
        uid=uuid.uuid4()
        for dashboardname in dashboardnames:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.create_dashboard,uid=uid, dashboardname=dashboardname)

    def test_create_dashboard_failure_non_existing_user(self):
        ''' create_dashboard should fail if user does not exist '''
        uid=uuid.uuid4()
        dashboardname='test_create_dashboard_failure_non_existing_user'
        self.assertRaises(exceptions.UserNotFoundException, dashboardapi.create_dashboard, uid=uid, dashboardname=dashboardname)

    def test_create_dashboard_success(self):
        ''' create_dashboard should succeed if user exists and parameters are ok '''
        username='test_create_dashboard_success'
        dashboardname='test_create_dashboard_success'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(len(result),3)
        self.assertEqual(result['dashboardname'],dashboardname)
        self.assertTrue(isinstance(result['bid'],uuid.UUID))
        self.assertTrue(isinstance(result['uid'],uuid.UUID))

    def test_update_dashboard_config_failure_invalid_dashboardname(self):
        ''' update_dashboard_config should fail if dashboardname is invalid '''
        dashboardnames=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4(), uuid.uuid1(), 'dashboardñame']
        bid=uuid.uuid4()
        for dashboardname in dashboardnames:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.update_dashboard_config, bid=bid, dashboardname=dashboardname)

    def test_update_dashboard_config_failure_invalid_bid(self):
        ''' update_dashboard_config should fail if bid is invalid '''
        bids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        dashboardname='test_update_dashboard_config_failure_invalid_bid'
        for bid in bids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.update_dashboard_config, bid=bid, dashboardname=dashboardname)

    def test_update_dashboard_config_failure_nonexistent_bid(self):
        ''' update_dashboard_config should fail if bid does not exist '''
        dashboardname='test_update_dashboard_config_failure_non_existent_bid'
        bid=uuid.uuid4()
        self.assertRaises(exceptions.DashboardNotFoundException, dashboardapi.update_dashboard_config, bid=bid, dashboardname=dashboardname)

    def test_update_dashboard_config_success(self):
        ''' update_dashboard_config should succeed if bid exists and dashboardname is valid '''
        username='test_update_dashboard_config_success'
        dashboardname1='test_update_dashboard_config success 1'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname1)
        self.assertTrue(isinstance(result,dict))
        self.assertEqual(len(result),3)
        self.assertEqual(result['dashboardname'],dashboardname1)
        self.assertTrue(isinstance(result['bid'],uuid.UUID))
        self.assertTrue(isinstance(result['uid'],uuid.UUID))
        bid=result['bid']
        dashboardname2='test_update_dashboard_config success 2'
        self.assertTrue(dashboardapi.update_dashboard_config(bid=bid, dashboardname=dashboardname2))
        dashboardconfig=dashboardapi.get_dashboard_config(bid=bid)
        self.assertEqual(dashboardconfig['bid'],bid)
        self.assertEqual(dashboardconfig['dashboardname'],dashboardname2)
        self.assertEqual(dashboardconfig['wids'],[])

    def test_add_widget_to_dashboard_failure_invalid_bid(self):
        ''' add_widget_to_dashboard should fail if bid is invalid '''
        bids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        wid=uuid.uuid4()
        for bid in bids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.add_widget_to_dashboard, bid=bid, wid=wid)

    def test_add_widget_to_dashboard_failure_invalid_wid(self):
        ''' add_widget_to_dashboard should fail if wid is invalid '''
        wids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        bid=uuid.uuid4()
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.add_widget_to_dashboard, bid=bid, wid=wid)

    def test_add_widget_to_dashboard_failure_non_existent_bid(self):
        ''' add_widget_to_dashboard should fail if bid does not exist '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertRaises(exceptions.DashboardNotFoundException, dashboardapi.add_widget_to_dashboard, bid=bid, wid=wid)

    def test_add_widget_to_dashboard_failure_non_existent_wid(self):
        ''' add_widget_to_dashboard should fail if wid does not exist '''
        username='test_add_widget_to_dashboard_failure_non_existent_wid'
        dashboardname='test_add_widget_to_dashboard_failure_non_existent_wid'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname)
        bid=result['bid']
        wid=uuid.uuid4()
        self.assertRaises(exceptions.WidgetNotFoundException, dashboardapi.add_widget_to_dashboard, bid=bid, wid=wid)

    def test_delete_widget_from_dashboard_failure_invalid_bid(self):
        ''' delete_widget_from_dashboard should fail if bid is invalid '''
        bids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        wid=uuid.uuid4()
        for bid in bids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.delete_widget_from_dashboard, bid=bid, wid=wid)

    def test_delete_widget_from_dashboard_failure_invalid_wid(self):
        ''' delete_widget_from_dashboard should fail if wid is invalid '''
        wids=[None, 2342342, 2342342.23423, {'a':'dict'}, ['a','list'],('a','tuple'),{'set'}, uuid.uuid4().hex, uuid.uuid1(), uuid.uuid1().hex, 'dashboardñame']
        bid=uuid.uuid4()
        for wid in wids:
            self.assertRaises(exceptions.BadParametersException, dashboardapi.delete_widget_from_dashboard, bid=bid, wid=wid)

    def test_delete_widget_from_dashboard_failure_non_existent_bid(self):
        ''' delete_widget_from_dashboard should fail if bid does not exist '''
        bid=uuid.uuid4()
        wid=uuid.uuid4()
        self.assertRaises(exceptions.DashboardNotFoundException, dashboardapi.delete_widget_from_dashboard, bid=bid, wid=wid)

    def test_delete_widget_from_dashboard_success(self):
        ''' delete_widget_from_dashboard should succeed, even if wid does not exist  '''
        username='test_delete_widget_from_dashboard_success'
        dashboardname='test_delete_widget_from_dashboard_success'
        user=userapi.create_user(username=username,password='password',email=username+'@komlog.org')
        result=dashboardapi.create_dashboard(uid=user['uid'], dashboardname=dashboardname)
        bid=result['bid']
        wid=uuid.uuid4()
        self.assertTrue(dashboardapi.delete_widget_from_dashboard(bid=bid, wid=wid))
        config=dashboardapi.get_dashboard_config(bid=bid)
        self.assertEqual(config, {'uid':user['uid'], 'bid':bid, 'dashboardname':dashboardname,'wids':[]})

