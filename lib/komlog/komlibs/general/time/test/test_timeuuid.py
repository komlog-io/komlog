import unittest
import time
import uuid
import decimal
import pandas as pd
import datetime
from komlog.komlibs.general.time import timeuuid

class GeneralTimeTimeuuidTest(unittest.TestCase):
    ''' komlog.general.time.timeuuid tests '''

    def test_time_complete_cicle_from_isodate_to_uuid1_to_isodate(self):
        ''' time received in the system as isodate should be transformed to uuid1 for storing,
            and when retrieved, the isodate resulting should be the same as the firts one. '''
        for i in range(1,10000):
            isodate=pd.Timestamp('now').isoformat()
            u=timeuuid.get_uuid1_from_isodate(isodate)
            isodate2=timeuuid.get_isodate_from_uuid(u)
            self.assertEqual(isodate+'+00:00', isodate2)
        for i in range(1,10000):
            isodate=pd.Timestamp('now',tz='utc').isoformat()
            u=timeuuid.get_uuid1_from_isodate(isodate)
            isodate2=timeuuid.get_isodate_from_uuid(u)
            self.assertEqual(isodate, isodate2)

    def test_uuid1_with_predictable_param_always_generates_predictable_values(self):
        ''' uuid1 should generate always the same uuid1 for a specific timestamp and be
            between max and min uuid for that timestamp '''
        now = time.time()
        for i in range(1,1000000):
            t=float(now+(i/i+1))
            u1 = timeuuid.uuid1(predictable=True, seconds=t)
            u2 = timeuuid.uuid1(predictable=True, seconds=t)
            min_u = timeuuid.min_uuid_from_time(t)
            max_u = timeuuid.max_uuid_from_time(t)
            self.assertEqual(u1,u2)
            self.assertTrue(u1>min_u)
            self.assertTrue(u1<max_u)

    def test_uuid1_with_no_predictable_param_always_generates_unpredictable_values(self):
        ''' uuid1 should generate always different uuid1 for a specific timestamp '''
        now = time.time()
        for i in range(1,10000):
            t=float(now+(i/i+1))
            u1 = timeuuid.uuid1(predictable=False, seconds=t)
            u2 = timeuuid.uuid1(predictable=False, seconds=t)
            self.assertNotEqual(u1,u2)

    def test_uuid1_with_seconds_equals_0_is_valid(self):
        ''' uuid1 should generate always the same uuid1 for a specific timestamp and be
            between max and min uuid for that timestamp '''
        t = timeuuid.uuid1(seconds=0)
        self.assertEqual(timeuuid.get_unix_timestamp(t),0)

    def test_isodates_always_produce_the_same_uuids_and_viceversa_if_requested(self):
        ''' generating a uuid from an isodate should be reproducible if param predictable is True'''
        for i in range(1,10000):
            now = pd.Timestamp('now',tz='utc').isoformat()
            u1 = timeuuid.get_uuid1_from_isodate(now, predictable=True)
            isodate = timeuuid.get_isodate_from_uuid(u1)
            u2 = timeuuid.get_uuid1_from_isodate(isodate, predictable=True)
            self.assertEqual(u1,u2)
            self.assertEqual(now,isodate)

