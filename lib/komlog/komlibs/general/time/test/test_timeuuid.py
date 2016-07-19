import unittest
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
