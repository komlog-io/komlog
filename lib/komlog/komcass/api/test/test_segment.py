import unittest
from komlog.komcass.api import segment as segmentapi
from komlog.komcass.model.orm import segment as ormsegment


class KomcassApiSegmentTest(unittest.TestCase):
    ''' komlog.komcass.api.segment tests '''

    def test_get_user_segment_non_existing_sid(self):
        ''' get_user_segment should return None if sid does not exist '''
        sid=999999
        self.assertIsNone(segmentapi.get_user_segment(sid=sid))

    def test_get_user_segment_existing_segment(self):
        ''' get_user_segment should return a UserSegment object if sid exists '''
        sid=0
        name='test_get_user_segment_existing_segment'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, params)

    def test_insert_user_segment_non_existing_segment(self):
        ''' insert_user_segment should return True and insert the Segment object  '''
        sid=1
        name='test_insert_user_segment_non_existing_segment'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, params)

    def test_insert_user_segment_already_existing_segment(self):
        ''' insert_user_segment should return True and replace the Segment object  '''
        sid=2
        name='test_insert_user_segment_already_existing_segment'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        name2='test_insert_user_segment_already_existing_segment_2'
        params2={'param2':'value2', 'param4':'value4'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name2, params=params2)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name2)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, params2)

    def test_insert_user_segment_non_valid_object(self):
        ''' insert_user_segment should fail if no UserSegment object is passed '''
        segments=[None, 2342342, '234234234', {'a':'dict'},['a','list']]
        for segment in segments:
            self.assertFalse(segmentapi.insert_user_segment(segment))

    def test_set_user_segment_params_already_existing_segment(self):
        ''' set_user_segment_params should return True and replace the Segment params  '''
        sid=3
        name='test_set_user_segment_params_already_existing_segment'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        params2={'param2':'value2', 'param4':'value4'}
        self.assertTrue(segmentapi.set_user_segment_params(sid=sid, params=params2))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, params2)

    def test_set_user_segment_params_non_existing_segment(self):
        ''' set_user_segment_params should return True and insert the Segment params  '''
        sid=4
        name='test_set_user_segment_params_non_existing_segment'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        self.assertTrue(segmentapi.set_user_segment_params(sid=sid, params=params))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, None)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, params)

    def test_set_user_segment_param_already_existing_param(self):
        ''' set_user_segment_param should return True and replace the Segment params  '''
        sid=5
        name='test_set_user_segment_param_already_existing_param'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        param2='param2'
        value2='value4'
        self.assertTrue(segmentapi.set_user_segment_param(sid=sid, param=param2, value=value2))
        new_params=params
        new_params[param2]=value2
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, new_params)
        self.assertEqual(len(segment_db.params),3)

    def test_set_user_segment_param_non_existing_param(self):
        ''' set_user_segment_param should return True and insert the new segment param '''
        sid=6
        name='test_set_user_segment_param_non_existing_param'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        param2='param4'
        value2='value4'
        self.assertTrue(segmentapi.set_user_segment_param(sid=sid, param=param2, value=value2))
        new_params=params
        new_params[param2]=value2
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, new_params)
        self.assertEqual(len(segment_db.params),4)

    def test_set_user_segment_param_non_existing_segment(self):
        ''' set_user_segment_param should return True and insert the new segment and param '''
        sid=7
        param='param4'
        value='value4'
        self.assertTrue(segmentapi.set_user_segment_param(sid=sid, param=param, value=value))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, None)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, {param:value})
        self.assertEqual(len(segment_db.params),1)

    def test_delete_user_segment_param_already_existing_param(self):
        ''' delete_user_segment_param should return True and delete the Segment params  '''
        sid=8
        name='test_delete_user_segment_param_already_existing_param'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        param='param2'
        self.assertTrue(segmentapi.delete_user_segment_param(sid=sid, param=param))
        new_params=params
        new_params.pop(param,None)
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, new_params)
        self.assertEqual(len(segment_db.params),2)

    def test_delete_user_segment_param_non_existing_param(self):
        ''' delete_user_segment_param should return True and keep params the same '''
        sid=9
        name='test_delete_user_segment_param_non_existing_param'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        param2='param4'
        self.assertTrue(segmentapi.delete_user_segment_param(sid=sid, param=param2))
        new_params=params
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertTrue(isinstance(segment_db, ormsegment.UserSegment))
        self.assertEqual(segment_db.segmentname, name)
        self.assertEqual(segment_db.sid, sid)
        self.assertEqual(segment_db.params, new_params)
        self.assertEqual(len(segment_db.params),3)

    def test_delete_user_segment_param_non_existing_segment(self):
        ''' delete_user_segment_param should return True '''
        sid=10
        param='param4'
        self.assertTrue(segmentapi.delete_user_segment_param(sid=sid, param=param))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertIsNone(segment_db)

    def test_delete_user_segment_already_existing_segment(self):
        ''' delete_user_segment_params should return True and delete the Segment params '''
        sid=11
        name='test_delete_user_segment_already_existing_params'
        params={'param1':'value1', 'param2':'value2', 'param3':'value3'}
        sobj=ormsegment.UserSegment(sid=sid, segmentname=name, params=params)
        self.assertTrue(segmentapi.insert_user_segment(sobj))
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertIsNone(segment_db)

    def test_delete_user_segment_non_existing_segment(self):
        ''' delete_user_segment_params should return True '''
        sid=13
        self.assertTrue(segmentapi.delete_user_segment(sid=sid))
        segment_db=segmentapi.get_user_segment(sid=sid)
        self.assertIsNone(segment_db)

