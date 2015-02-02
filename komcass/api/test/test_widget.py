import unittest
import uuid
from komlibs.general.time import timeuuid
from komcass.api import widget as widgetapi
from komcass.model.orm import widget as ormwidget


class KomcassApiWidgetTest(unittest.TestCase):
    ''' komlog.komcass.api.widget tests '''

    def setUp(self):
        widds=uuid.uuid4()
        widdp=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        pid=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, uid=uid, creation_date=creation_date, did=did)
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, uid=uid, creation_date=creation_date, pid=pid)
        widgetapi.insert_widget(self.widgetds)
        widgetapi.insert_widget(self.widgetdp)

    def test_get_widget_existing_wid(self):
        ''' get_widget should succeed if we pass an existing wid '''
        wid=self.widgetds.wid
        widget=widgetapi.get_widget(wid=wid)
        self.assertEqual(widget.type, self.widgetds.type)
        self.assertEqual(widget.wid, self.widgetds.wid)
        self.assertEqual(widget.uid, self.widgetds.uid)

    def test_get_widget_non_existing_wid(self):
        ''' get_widget should return None if we pass a non existing wid '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget(wid=wid))

    def test_get_widgets_existing_uid(self):
        ''' get_widgets should succeed if we pass an existing uid '''
        uid=self.widgetds.uid
        widgets=widgetapi.get_widgets(uid=uid)
        self.assertEqual(len(widgets),2)
        for widget in widgets:
            self.assertTrue(isinstance(widget, ormwidget.Widget))

    def test_get_widgets_non_existing_uid(self):
        ''' get_widgets should return an empty array if we pass a non existing uid '''
        uid=uuid.uuid4()
        widgets=widgetapi.get_widgets(uid=uid)
        self.assertTrue(isinstance(widgets,list))
        self.assertEqual(len(widgets),0)

    def test_get_number_of_widgets_by_uid_success(self):
        ''' get_number_of_widgets by uid should return the number of widgets belonging to a uid '''
        uid=self.widgetds.uid
        num_widgets=widgetapi.get_number_of_widgets_by_uid(uid)
        self.assertEqual(num_widgets, 2)

    def test_get_number_of_widgets_by_uid_no_widgets(self):
        ''' get_number_of_widgets by uid should return the number of widgets belonging to a uid '''
        uid=uuid.uuid4()
        num_widgets=widgetapi.get_number_of_widgets_by_uid(uid)
        self.assertEqual(num_widgets, 0)

    def test_delete_widget_non_existent_widget(self):
        ''' delete_widget should return True even if we try to delete a non existent widget '''
        wid=uuid.uuid4()
        self.assertTrue(widgetapi.delete_widget(wid))

    def test_delete_widget_existent_widget_ds(self):
        ''' delete_widget should return True when a widget DS is deleted successfully '''
        widds=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, uid=uid, creation_date=creation_date, did=did)
        widgetapi.new_widget(self.widgetds)
        self.assertTrue(widgetapi.delete_widget(widds))
        self.assertIsNone(widgetapi.get_widget(widds))

    def test_delete_widget_existent_widget_dp(self):
        ''' delete_widget should return True when a widget DP is deleted successfully '''
        widdp=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, uid=uid, creation_date=creation_date, pid=pid)
        widgetapi.new_widget(self.widgetdp)
        self.assertTrue(widgetapi.delete_widget(widdp))
        self.assertIsNone(widgetapi.get_widget(widdp))

    def test_new_widget_no_widget_obj(self):
        ''' new_widget should fail if we pass no widget object as argument '''
        widgets=[None, 'qrqerqwerqw234234', 234234234, {'a':'dict'}, ['a','list']]
        for widget in widgets:
            self.assertFalse(widgetapi.new_widget(widget))

    def test_new_widget_widget_dp(self):
        ''' new_widget should return True when a widget DP is created successfully '''
        widdp=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, uid=uid, creation_date=creation_date, pid=pid)
        self.assertTrue(widgetapi.new_widget(self.widgetdp))

    def test_new_widget_widget_ds(self):
        ''' new_widget should return True when a widget DS is created successfully '''
        widds=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, uid=uid, creation_date=creation_date, did=did)
        self.assertTrue(widgetapi.new_widget(self.widgetds))

    def test_insert_widget_no_widget_obj(self):
        ''' insert_widget should fail if we pass no widget object as argument '''
        widgets=[None, 'qrqerqwerqw234234', 234234234, {'a':'dict'}, ['a','list']]
        for widget in widgets:
            self.assertFalse(widgetapi.insert_widget(widget))

    def test_insert_widget_widget_dp(self):
        ''' insert_widget should return True when a widget DP is updated successfully '''
        widdp=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, uid=uid, creation_date=creation_date, pid=pid)
        self.assertTrue(widgetapi.new_widget(self.widgetdp))
        self.assertTrue(widgetapi.insert_widget(self.widgetdp))

    def test_insert_widget_widget_ds(self):
        ''' insert_widget should return True when a widget DS is updated successfully '''
        widds=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, uid=uid, creation_date=creation_date, did=did)
        self.assertTrue(widgetapi.new_widget(self.widgetds))
        self.assertTrue(widgetapi.insert_widget(self.widgetds))

    def test_get_widget_ds_inexistent_widget(self):
        ''' get_widget_ds should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_ds(wid=wid))

    def test_get_widget_ds_different_type_widget(self):
        ''' get_widget_ds should return None if wid does not exist (because is of different type) '''
        wid=self.widgetdp.wid
        self.assertIsNone(widgetapi.get_widget_ds(wid=wid))
        
    def test_get_widget_ds_success_by_wid(self):
        ''' get_widget_ds should return the widget ds object '''
        wid=self.widgetds.wid
        self.assertTrue(isinstance(widgetapi.get_widget_ds(wid=wid), ormwidget.WidgetDs))

    def test_get_widget_ds_success_by_did(self):
        ''' get_widget_ds should return the widget ds object '''
        did=self.widgetds.did
        self.assertTrue(isinstance(widgetapi.get_widget_ds(did=did), ormwidget.WidgetDs))

    def test_get_widget_dp_inexistent_widget(self):
        ''' get_widget_dp should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_dp(wid=wid))

    def test_get_widget_dp_different_type_widget(self):
        ''' get_widget_dp should return None if wid does not exist (because is of different type) '''
        wid=self.widgetds.wid
        self.assertIsNone(widgetapi.get_widget_dp(wid=wid))
        
    def test_get_widget_dp_success_by_wid(self):
        ''' get_widget_dp should return the widget dp object '''
        wid=self.widgetdp.wid
        self.assertTrue(isinstance(widgetapi.get_widget_dp(wid=wid), ormwidget.WidgetDp))

    def test_get_widget_dp_success_by_pid(self):
        ''' get_widget_dp should return the widget dp object '''
        pid=self.widgetdp.pid
        self.assertTrue(isinstance(widgetapi.get_widget_dp(pid=pid), ormwidget.WidgetDp))

