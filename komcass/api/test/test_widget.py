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
        self.widgetds=ormwidget.WidgetDs(wid=widds, widgetname='widgetds', uid=uid, creation_date=creation_date, did=did)
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, widgetname='widgetdp', uid=uid, creation_date=creation_date, pid=pid)
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
        self.widgetds=ormwidget.WidgetDs(wid=widds, widgetname='widgetds', uid=uid, creation_date=creation_date, did=did)
        widgetapi.new_widget(self.widgetds)
        self.assertTrue(widgetapi.delete_widget(widds))
        self.assertIsNone(widgetapi.get_widget(widds))

    def test_delete_widget_existent_widget_dp(self):
        ''' delete_widget should return True when a widget DP is deleted successfully '''
        widdp=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, widgetname='widgetdp', uid=uid, creation_date=creation_date, pid=pid)
        widgetapi.new_widget(self.widgetdp)
        self.assertTrue(widgetapi.delete_widget(widdp))
        self.assertIsNone(widgetapi.get_widget(widdp))

    def test_delete_widget_existent_widget_histogram(self):
        ''' delete_widget should return True when a widget HISTOGRAM is deleted successfully '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, widgetname='widgethg', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        widgetapi.new_widget(widgethg)
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertTrue(widgetapi.delete_widget(widhg))
        self.assertIsNone(widgetapi.get_widget(widhg))

    def test_delete_widget_existent_widget_linegraph(self):
        ''' delete_widget should return True when a widget linegraph is deleted successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid, widgetname='widget linegraph', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        widgetapi.new_widget(widget)
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget linegraph')
        self.assertTrue(widgetapi.delete_widget(wid))
        self.assertIsNone(widgetapi.get_widget(wid))

    def test_delete_widget_existent_widget_table(self):
        ''' delete_widget should return True when a widget table is deleted successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid, widgetname='widget table', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        widgetapi.new_widget(widget)
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget table')
        self.assertTrue(widgetapi.delete_widget(wid))
        self.assertIsNone(widgetapi.get_widget(wid))

    def test_delete_widget_existent_widget_multidp(self):
        ''' delete_widget should return True when a widget multidp is deleted successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pids={uuid.uuid4(),uuid.uuid4()}
        widget=ormwidget.WidgetMultidp(wid=wid, widgetname='widget multidp', uid=uid,datapoints=pids, creation_date=creation_date, active_visualization=0)
        widgetapi.new_widget(widget)
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints,pids)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget multidp')
        self.assertEqual(widget.active_visualization,0)
        self.assertTrue(widgetapi.delete_widget(wid))
        self.assertIsNone(widgetapi.get_widget(wid))

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
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, widgetname='widgetdp', uid=uid, creation_date=creation_date, pid=pid)
        self.assertTrue(widgetapi.new_widget(self.widgetdp))

    def test_new_widget_widget_ds(self):
        ''' new_widget should return True when a widget DS is created successfully '''
        widds=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, widgetname='widgetds', uid=uid, creation_date=creation_date, did=did)
        self.assertTrue(widgetapi.new_widget(self.widgetds))

    def test_new_widget_widget_histogram(self):
        ''' new_widget should return True when a widget HISTOGRAM is created successfully '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, widgetname='widgethg', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_new_widget_widget_linegraph(self):
        ''' new_widget should return True when a widget linegraph is created successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid, widgetname='widget linegraph', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_new_widget_widget_table(self):
        ''' new_widget should return True when a widget table is created successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid, widgetname='widget table', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_new_widget_widget_multidp(self):
        ''' new_widget should return True when a widget multidp is created successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pids={uuid.uuid4(),uuid.uuid4()}
        widget=ormwidget.WidgetMultidp(wid=wid, widgetname='widget multidp', uid=uid,datapoints=pids, creation_date=creation_date, active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints,pids)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget multidp')
        self.assertEqual(widget.active_visualization,0)

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
        self.widgetdp=ormwidget.WidgetDp(wid=widdp, widgetname='widgetdp', uid=uid, creation_date=creation_date, pid=pid)
        self.assertTrue(widgetapi.new_widget(self.widgetdp))
        self.assertTrue(widgetapi.insert_widget(self.widgetdp))

    def test_insert_widget_widget_ds(self):
        ''' insert_widget should return True when a widget DS is updated successfully '''
        widds=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        self.widgetds=ormwidget.WidgetDs(wid=widds, widgetname='widgetds', uid=uid, creation_date=creation_date, did=did)
        self.assertTrue(widgetapi.new_widget(self.widgetds))
        self.assertTrue(widgetapi.insert_widget(self.widgetds))

    def test_insert_widget_widget_histogram(self):
        ''' insert_widget should return True when a widget HISTOGRAM is updated successfully '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, widgetname='widgethg', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        datapoints2={uuid.uuid4(), uuid.uuid4()}
        widget.datapoints=datapoints2
        self.assertTrue(widgetapi.insert_widget(widget))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints2)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_insert_widget_widget_linegraph(self):
        ''' insert_widget should return True when a widget linegraph is updated successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid, widgetname='widget linegraph', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        datapoints2={uuid.uuid4(), uuid.uuid4()}
        widget.datapoints=datapoints2
        self.assertTrue(widgetapi.insert_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints2)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_insert_widget_widget_table(self):
        ''' insert_widget should return True when a widget table is updated successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid, widgetname='widget table', uid=uid, datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)
        datapoints2={uuid.uuid4(), uuid.uuid4()}
        widget.datapoints=datapoints2
        self.assertTrue(widgetapi.insert_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints, datapoints2)
        self.assertEqual(widget.colors, colors)
        self.assertEqual(widget.creation_date, creation_date)

    def test_insert_widget_widget_multidp(self):
        ''' new_widget should return True when a widget multidp is created successfully '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pids={uuid.uuid4(),uuid.uuid4()}
        widget=ormwidget.WidgetMultidp(wid=wid, widgetname='widget multidp', uid=uid,datapoints=pids, creation_date=creation_date, active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.datapoints,pids)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget multidp')
        self.assertEqual(widget.active_visualization,0)
        new_pids={uuid.uuid4(), uuid.uuid4(), uuid.uuid4()}
        widget.datapoints=new_pids
        widget.active_visualization=1
        self.assertTrue(widgetapi.insert_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(len(widget.datapoints),len(new_pids))
        self.assertEqual(widget.datapoints,set(sorted(new_pids)))
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, 'widget multidp')
        self.assertEqual(widget.active_visualization,1)

    def test_insert_widget_widgetname_non_existent_widget(self):
        ''' insert_widget_widgetname should return False if widget does not exist '''
        wid=uuid.uuid4()
        widgetname='test_insert_widget_widgetname_non_existent_widget'
        self.assertFalse(widgetapi.insert_widget_widgetname(wid=wid, widgetname=widgetname))

    def test_insert_widget_widgetname_success_widget_datasource(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        did=uuid.uuid4()
        widgetname='test_insert_widget_widgetname_success_widget_datasource'
        widget=ormwidget.WidgetDs(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date, did=did)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_ds(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.did, did)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_datasource_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_ds(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.did, did)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_widgetname_success_widget_datapoint(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        widgetname='test_insert_widget_widgetname_success_widget_datapoint'
        widget=ormwidget.WidgetDp(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date, pid=pid)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_dp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.pid, pid)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_datapoint_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_dp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.pid, pid)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_widgetname_success_widget_histogram(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgetname='test_insert_widget_widgetname_success_widget_histogram'
        widget=ormwidget.WidgetHistogram(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_histogram(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_histogram_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_histogram(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_widgetname_success_widget_linegraph(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgetname='test_insert_widget_widgetname_success_widget_linegraph'
        widget=ormwidget.WidgetLinegraph(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_linegraph_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_widgetname_success_widget_table(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgetname='test_insert_widget_widgetname_success_widget_table'
        widget=ormwidget.WidgetTable(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_table_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_widgetname_success_widget_multidp(self):
        ''' insert_widget_widgetname should return True and update the widgetname field '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgetname='test_insert_widget_widgetname_success_widget_multidp'
        active_visualization=0
        widget=ormwidget.WidgetMultidp(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date, active_visualization=active_visualization)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        new_widgetname='test_insert_widget_widgetname_success_widget_multidp_2'
        self.assertTrue(widgetapi.insert_widget_widgetname(wid=wid, widgetname=new_widgetname))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, new_widgetname)

    def test_insert_widget_multidp_active_visualization_non_existent_widget(self):
        ''' insert_widget_multidp_active_visualization should return False if widget does not exist '''
        wid=uuid.uuid4()
        active_visualization=12
        self.assertFalse(widgetapi.insert_widget_multidp_active_visualization(wid=wid,active_visualization=active_visualization))

    def test_insert_widget_multidp_active_visualization_success(self):
        ''' insert_widget_multidp_active_visualization should return True '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgetname='test_insert_widget_multidp_active_visualization_success'
        pids={uuid.uuid4()}
        active_visualization=0
        widget=ormwidget.WidgetMultidp(wid=wid, widgetname=widgetname, uid=uid, creation_date=creation_date, active_visualization=active_visualization,datapoints=pids)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.datapoints,pids)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        self.assertEqual(widget.active_visualization, active_visualization)
        self.assertTrue(widgetapi.insert_widget_multidp_active_visualization(wid=wid, active_visualization=99 ))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.datapoints,pids)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.widgetname, widgetname)
        self.assertEqual(widget.active_visualization,99)

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

    def test_get_widget_histogram_different_type_widget(self):
        ''' get_widget_histogram should return None if wid does not exist (because is of different type) '''
        wid=self.widgetdp.wid
        self.assertIsNone(widgetapi.get_widget_histogram(wid=wid))
        
    def test_get_widget_histogram_success_by_wid(self):
        ''' get_widget_histogram should return the widget histogram object '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, uid=uid, widgetname='widgethg', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        self.assertTrue(isinstance(widgetapi.get_widget_histogram(wid=widhg), ormwidget.WidgetHistogram))

    def test_get_widget_histogram_inexistent_widget(self):
        ''' get_widget_histogram should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_histogram(wid=wid))

    def test_get_wids_histograms_with_pid_success_no_pid(self):
        ''' get_wids_histograms_with_pid should return None if the wid does not has the pid '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=wid, uid=uid, widgetname='widgethg', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        wids=widgetapi.get_wids_histograms_with_pid(pid=uuid.uuid4())
        self.assertEqual(wids,None)

    def test_get_wids_histograms_with_pid_success_by_pid(self):
        ''' get_wids_histograms_with_pid should return the wid list of histograms that have the pid '''
        wid1=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid1=uuid.uuid4()
        datapoints={uuid.uuid4(),pid1}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=wid1, uid=uid, widgetname='widgethg', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        wid2=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid2=uuid.uuid4()
        datapoints={uuid.uuid4(),pid2}
        colors={uuid.uuid4():'AE23EF'}
        widgethg=ormwidget.WidgetHistogram(wid=wid2, uid=uid, widgetname='widgethg', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        wids=widgetapi.get_wids_histograms_with_pid(pid=pid1)
        self.assertEqual(wids,[wid1])
        wids=widgetapi.get_wids_histograms_with_pid(pid=pid2)
        self.assertEqual(wids,[wid2])

    def test_add_datapoint_to_histogram_non_existent_widget(self):
        ''' add_datapoint_to_histogram should return False if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertFalse(widgetapi.add_datapoint_to_histogram(wid=wid, pid=pid, color=color))
        self.assertIsNone(widgetapi.get_widget_histogram(wid=wid))

    def test_add_datapoint_to_histogram_success_one_datapoint(self):
        ''' add_datapoint_to_histogram should succeed if datapoint is the first one '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgethg=ormwidget.WidgetHistogram(wid=widhg, uid=uid, widgetname='widgethg', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_histogram(wid=widhg, pid=pid, color=color))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})

    def test_add_datapoint_to_histogram_success_some_datapoints(self):
        ''' add_datapoint_to_histogram should succeed if datapoint is not the first one '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, uid=uid, widgetname='widgethg', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_histogram(wid=widhg, pid=pid2, color=color2))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})

    def test_delete_datapoint_from_histogram_non_existent_widget(self):
        ''' delete_datapoint_from_histogram should return True even if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.delete_datapoint_from_histogram(wid=wid, pid=pid))
        self.assertIsNone(widgetapi.get_widget_histogram(wid=wid))

    def test_delete_datapoint_from_histogram_success_no_datapoint_left(self):
        ''' delete_datapoint_from_histogram should succeed and return an empty set if no more datapoints exist '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widgethg=ormwidget.WidgetHistogram(wid=widhg, uid=uid, widgetname='widgethg', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_histogram(wid=widhg, pid=pid, color=color))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        self.assertTrue(widgetapi.delete_datapoint_from_histogram(wid=widhg, pid=pid))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, set())
        self.assertEqual(widget.colors, {})

    def test_delete_datapoint_from_histogram_success_some_datapoints_left(self):
        ''' add_datapoint_to_histogram should succeed if datapoint is not the first one '''
        widhg=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widgethg=ormwidget.WidgetHistogram(wid=widhg, uid=uid, widgetname='widgethg', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widgethg))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid,widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_histogram(wid=widhg, pid=pid2, color=color2))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})
        self.assertTrue(widgetapi.delete_datapoint_from_histogram(wid=widhg, pid=pid))
        widget=widgetapi.get_widget_histogram(wid=widhg)
        self.assertEqual(widget.wid, widhg)
        self.assertEqual(widget.widgetname,'widgethg')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid2})
        self.assertEqual(widget.colors, {pid2:color2})

    def test_get_widget_linegraph_different_type_widget(self):
        ''' get_widget_linegraph should return None if wid does not exist (because is of different type) '''
        wid=self.widgetdp.wid
        self.assertIsNone(widgetapi.get_widget_linegraph(wid=wid))
        
    def test_get_widget_linegraph_success_by_wid(self):
        ''' get_widget_linegraph should return the widget linegraph object '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        self.assertTrue(isinstance(widgetapi.get_widget_linegraph(wid=wid), ormwidget.WidgetLinegraph))

    def test_get_widget_linegraph_inexistent_widget(self):
        ''' get_widget_linegraph should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_linegraph(wid=wid))

    def test_get_wids_linegraphs_with_pid_success_no_pid(self):
        ''' get_wids_linegraphs_with_pid should return None if the wid does not has the pid '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_linegraphs_with_pid(pid=uuid.uuid4())
        self.assertEqual(wids,None)

    def test_get_wids_linegraphs_with_pid_success_by_pid(self):
        ''' get_wids_linegraphs_with_pid should return the wid list of linegraphs that have the pid '''
        wid1=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid1=uuid.uuid4()
        datapoints={uuid.uuid4(),pid1}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid1, uid=uid, widgetname='widget linegraph', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wid2=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid2=uuid.uuid4()
        datapoints={uuid.uuid4(),pid2,pid1}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetLinegraph(wid=wid2, uid=uid, widgetname='widget linegraph', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_linegraphs_with_pid(pid=pid1)
        self.assertEqual(sorted(wids),sorted([wid1,wid2]))
        wids=widgetapi.get_wids_linegraphs_with_pid(pid=pid2)
        self.assertEqual(wids,[wid2])

    def test_add_datapoint_to_linegraph_non_existent_widget(self):
        ''' add_datapoint_to_linegraph should return False if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertFalse(widgetapi.add_datapoint_to_linegraph(wid=wid, pid=pid, color=color))
        self.assertIsNone(widgetapi.get_widget_linegraph(wid=wid))

    def test_add_datapoint_to_linegraph_success_one_datapoint(self):
        ''' add_datapoint_to_linegraph should succeed if datapoint is the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_linegraph(wid=wid, pid=pid, color=color))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})

    def test_add_datapoint_to_linegraph_success_some_datapoints(self):
        ''' add_datapoint_to_linegraph should succeed if datapoint is not the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_linegraph(wid=wid, pid=pid2, color=color2))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})

    def test_delete_datapoint_from_linegraph_non_existent_widget(self):
        ''' delete_datapoint_from_linegraph should return True even if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.delete_datapoint_from_linegraph(wid=wid, pid=pid))
        self.assertIsNone(widgetapi.get_widget_linegraph(wid=wid))

    def test_delete_datapoint_from_linegraph_success_no_datapoint_left(self):
        ''' delete_datapoint_from_linegraph should succeed and return an empty set if no more datapoints exist '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_linegraph(wid=wid, pid=pid, color=color))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        self.assertTrue(widgetapi.delete_datapoint_from_linegraph(wid=wid, pid=pid))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, set())
        self.assertEqual(widget.colors, {})

    def test_delete_datapoint_from_linegraph_success_some_datapoints_left(self):
        ''' add_datapoint_to_linegraph should succeed if datapoint is not the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widget=ormwidget.WidgetLinegraph(wid=wid, uid=uid, widgetname='widget linegraph', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_linegraph(wid=wid, pid=pid2, color=color2))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})
        self.assertTrue(widgetapi.delete_datapoint_from_linegraph(wid=wid, pid=pid))
        widget=widgetapi.get_widget_linegraph(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget linegraph')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid2})
        self.assertEqual(widget.colors, {pid2:color2})

    def test_get_widget_table_different_type_widget(self):
        ''' get_widget_table should return None if wid does not exist (because is of different type) '''
        wid=self.widgetdp.wid
        self.assertIsNone(widgetapi.get_widget_table(wid=wid))
        
    def test_get_widget_table_success_by_wid(self):
        ''' get_widget_table should return the widget table object '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        self.assertTrue(isinstance(widgetapi.get_widget_table(wid=wid), ormwidget.WidgetTable))

    def test_get_widget_table_inexistent_widget(self):
        ''' get_widget_table should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_table(wid=wid))

    def test_get_wids_tables_with_pid_success_no_pid(self):
        ''' get_wids_tables_with_pid should return None if the wid does not has the pid '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        datapoints={uuid.uuid4(),uuid.uuid4()}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_tables_with_pid(pid=uuid.uuid4())
        self.assertEqual(wids,None)

    def test_get_wids_tables_with_pid_success_by_pid(self):
        ''' get_wids_tables_with_pid should return the wid list of tables that have the pid '''
        wid1=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid1=uuid.uuid4()
        datapoints={uuid.uuid4(),pid1}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid1, uid=uid, widgetname='widget table', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wid2=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid2=uuid.uuid4()
        datapoints={uuid.uuid4(),pid2,pid1}
        colors={uuid.uuid4():'AE23EF'}
        widget=ormwidget.WidgetTable(wid=wid2, uid=uid, widgetname='widget table', datapoints=datapoints, colors=colors, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_tables_with_pid(pid=pid1)
        self.assertEqual(sorted(wids),sorted([wid1,wid2]))
        wids=widgetapi.get_wids_tables_with_pid(pid=pid2)
        self.assertEqual(wids,[wid2])

    def test_add_datapoint_to_table_non_existent_widget(self):
        ''' add_datapoint_to_table should return False if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertFalse(widgetapi.add_datapoint_to_table(wid=wid, pid=pid, color=color))
        self.assertIsNone(widgetapi.get_widget_table(wid=wid))

    def test_add_datapoint_to_table_success_one_datapoint(self):
        ''' add_datapoint_to_table should succeed if datapoint is the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_table(wid=wid, pid=pid, color=color))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})

    def test_add_datapoint_to_table_success_some_datapoints(self):
        ''' add_datapoint_to_table should succeed if datapoint is not the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_table(wid=wid, pid=pid2, color=color2))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})

    def test_delete_datapoint_from_table_non_existent_widget(self):
        ''' delete_datapoint_from_table should return True even if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.delete_datapoint_from_table(wid=wid, pid=pid))
        self.assertIsNone(widgetapi.get_widget_table(wid=wid))

    def test_delete_datapoint_from_table_success_no_datapoint_left(self):
        ''' delete_datapoint_from_table should succeed and return an empty set if no more datapoints exist '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        pid=uuid.uuid4()
        color='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_table(wid=wid, pid=pid, color=color))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        self.assertTrue(widgetapi.delete_datapoint_from_table(wid=wid, pid=pid))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, set())
        self.assertEqual(widget.colors, {})

    def test_delete_datapoint_from_table_success_some_datapoints_left(self):
        ''' add_datapoint_to_table should succeed if datapoint is not the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        color='AEEEAB'
        datapoints={pid}
        colors={pid:color}
        widget=ormwidget.WidgetTable(wid=wid, uid=uid, widgetname='widget table', creation_date=creation_date, datapoints=datapoints, colors=colors)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.colors, {pid:color})
        pid2=uuid.uuid4()
        color2='AEEEAA'
        self.assertTrue(widgetapi.add_datapoint_to_table(wid=wid, pid=pid2, color=color2))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.colors, {pid:color,pid2:color2})
        self.assertTrue(widgetapi.delete_datapoint_from_table(wid=wid, pid=pid))
        widget=widgetapi.get_widget_table(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget table')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid2})
        self.assertEqual(widget.colors, {pid2:color2})

    def test_get_widget_multidp_different_type_widget(self):
        ''' get_widget_table should return None if wid does not exist (because is of different type) '''
        wid=self.widgetdp.wid
        self.assertIsNone(widgetapi.get_widget_multidp(wid=wid))
        
    def test_get_widget_multidp_success_by_wid(self):
        ''' get_widget_multidp should return the widget multidp object '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pids={uuid.uuid4(),uuid.uuid4()}
        active_visualization=0
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp',datapoints=pids, active_visualization=active_visualization, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        self.assertTrue(isinstance(widgetapi.get_widget_multidp(wid=wid), ormwidget.WidgetMultidp))

    def test_get_widget_multidp_inexistent_widget(self):
        ''' get_widget_multidp should return None if wid does not exist '''
        wid=uuid.uuid4()
        self.assertIsNone(widgetapi.get_widget_multidp(wid=wid))

    def test_get_wids_multidp_with_pid_success_no_pid(self):
        ''' get_wids_multidp_with_pid should return None if the wid does not has the pid '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pids={uuid.uuid4(),uuid.uuid4()}
        active_visualization=0
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp',datapoints=pids,active_visualization=active_visualization, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_multidp_with_pid(pid=uuid.uuid4())
        self.assertEqual(wids,None)

    def test_get_wids_multidp_with_pid_success_by_pid(self):
        ''' get_wids_multidp_with_pid should return the wid list of multidp that have the pid '''
        wid1=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid1=uuid.uuid4()
        pids={uuid.uuid4(),pid1}
        widget=ormwidget.WidgetMultidp(wid=wid1, uid=uid, widgetname='widget multidp',datapoints=pids,active_visualization=0, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wid2=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid2=uuid.uuid4()
        pids={uuid.uuid4(),pid2,pid1}
        widget=ormwidget.WidgetMultidp(wid=wid2, uid=uid, widgetname='widget multidp',datapoints=pids,active_visualization=1, creation_date=creation_date)
        self.assertTrue(widgetapi.new_widget(widget))
        wids=widgetapi.get_wids_multidp_with_pid(pid=pid1)
        self.assertEqual(sorted(wids),sorted([wid1,wid2]))
        wids=widgetapi.get_wids_multidp_with_pid(pid=pid2)
        self.assertEqual(wids,[wid2])

    def test_add_datapoint_to_multidp_non_existent_widget(self):
        ''' add_datapoint_to_multidp should return False if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertFalse(widgetapi.add_datapoint_to_multidp(wid=wid, pid=pid))
        self.assertIsNone(widgetapi.get_widget_multidp(wid=wid))

    def test_add_datapoint_to_multidp_success_one_datapoint(self):
        ''' add_datapoint_to_multidp should succeed if datapoint is the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp', creation_date=creation_date, active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.active_visualization,0)
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.add_datapoint_to_multidp(wid=wid, pid=pid))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.active_visualization,0)

    def test_add_datapoint_to_multidp_success_some_datapoints(self):
        ''' add_datapoint_to_multidp should succeed if datapoint is not the first one '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        pids={pid}
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp', creation_date=creation_date,datapoints=pids,active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.active_visualization,0)
        pid2=uuid.uuid4()
        self.assertTrue(widgetapi.add_datapoint_to_multidp(wid=wid, pid=pid2))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.active_visualization,0)
        self.assertEqual(widget.datapoints, {pid,pid2})

    def test_delete_datapoint_from_multidp_non_existent_widget(self):
        ''' delete_datapoint_from_multidp should return True even if widget does not exist '''
        wid=uuid.uuid4()
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.delete_datapoint_from_multidp(wid=wid, pid=pid))
        self.assertIsNone(widgetapi.get_widget_multidp(wid=wid))

    def test_delete_datapoint_from_multidp_success_no_datapoint_left(self):
        ''' delete_datapoint_from_multidp should succeed and return an empty set if no more datapoints exist '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp', creation_date=creation_date, active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.active_visualization,0)
        pid=uuid.uuid4()
        self.assertTrue(widgetapi.add_datapoint_to_multidp(wid=wid, pid=pid))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.active_visualization,0)
        self.assertTrue(widgetapi.delete_datapoint_from_multidp(wid=wid, pid=pid))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, set())
        self.assertEqual(widget.active_visualization,0)

    def test_delete_datapoint_from_multidp_success_some_datapoints_left(self):
        ''' delete_datapoint_to_multidp should succeed and remove from the datapoints set '''
        wid=uuid.uuid4()
        uid=uuid.uuid4()
        creation_date=timeuuid.uuid1()
        pid=uuid.uuid4()
        pids={pid}
        widget=ormwidget.WidgetMultidp(wid=wid, uid=uid, widgetname='widget multidp', creation_date=creation_date,datapoints=pids,active_visualization=0)
        self.assertTrue(widgetapi.new_widget(widget))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid,wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid})
        self.assertEqual(widget.active_visualization,0)
        pid2=uuid.uuid4()
        self.assertTrue(widgetapi.add_datapoint_to_multidp(wid=wid, pid=pid2))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid,pid2})
        self.assertEqual(widget.active_visualization,0)
        self.assertTrue(widgetapi.delete_datapoint_from_multidp(wid=wid, pid=pid))
        widget=widgetapi.get_widget_multidp(wid=wid)
        self.assertEqual(widget.wid, wid)
        self.assertEqual(widget.widgetname,'widget multidp')
        self.assertEqual(widget.uid, uid)
        self.assertEqual(widget.creation_date, creation_date)
        self.assertEqual(widget.datapoints, {pid2})
        self.assertEqual(widget.active_visualization,0)

