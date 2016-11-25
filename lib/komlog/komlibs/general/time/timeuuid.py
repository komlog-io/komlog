import uuid
import random
import time
import pandas as pd
from cassandra import util

HIGHEST_TIME_UUID=util.HIGHEST_TIME_UUID
LOWEST_TIME_UUID=util.LOWEST_TIME_UUID

def get_unix_timestamp(u):
    return util.unix_time_from_uuid1(u)

def get_custom_sequence(u):
    return u.hex

def get_uuid1_from_custom_sequence(sequence):
    try:
        value=uuid.UUID(sequence)
    except ValueError:
        return None
    else:
        return value

def get_uuid1_from_isodate(isodate, predictable=False):
    date=pd.Timestamp(isodate)
    if date.tz is None:
        date=pd.Timestamp(isodate,tz='utc')
    return uuid1(seconds=date.timestamp(), predictable=predictable)

def get_datetime_from_uuid1(u):
    return util.datetime_from_uuid1(u)

def get_isodate_from_uuid(u):
    ts=util.unix_time_from_uuid1(u)
    date=pd.Timestamp(int(ts*10**6), unit='us',tz='utc')
    return date.isoformat()

def uuid1(seconds=None, predictable=False):
    if not seconds:
        seconds=time.time()
    if predictable:
        clock_seq = (int(seconds)|129)&2047
        node = (int(seconds*1e6)^(2**48-1))&(2**48-1)
    else:
        r = random.SystemRandom()
        clock_seq = r.getrandbits(14)
        node = r.getrandbits(48)
    return util.uuid_from_time(time_arg=seconds, node=node, clock_seq=clock_seq)

def max_uuid_from_time(timestamp):
    return util.max_uuid_from_time(timestamp)

def min_uuid_from_time(timestamp):
    return util.min_uuid_from_time(timestamp)

def get_day_timestamp(u):
    ''' this function extracts the day from the date passed as argument (uuid1)
        and returns the truncated timestamp at 00:00:00h in seconds.
        Because the date milliseconds is set to 0, the returned value
        is of type int '''
    ts=get_unix_timestamp(u)
    date=pd.Timestamp(ts, unit='s', tz='utc')
    date=date.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp=date.timestamp()
    return int(timestamp)

def get_hour_timestamp(u):
    ''' this function extracts the hour from the date passed as argument (uuid1)
        and returns the truncated timestamp at 00min:00s in seconds.
        Because the date milliseconds is set to 0, the returned value
        is of type int '''
    ts=get_unix_timestamp(u)
    date=pd.Timestamp(ts, unit='s', tz='utc')
    date=date.replace(minute=0, second=0, microsecond=0)
    timestamp=date.timestamp()
    return int(timestamp)

