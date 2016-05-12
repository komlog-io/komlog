import uuid
import time
from datetime import datetime, timezone
from cassandra import util

node=0x010000000000
str_node='010000000000'

HIGHEST_TIME_UUID=util.HIGHEST_TIME_UUID
LOWEST_TIME_UUID=util.LOWEST_TIME_UUID

def get_unix_timestamp(u):
    return util.unix_time_from_uuid1(u)

def get_custom_sequence(u):
    return u.hex[0:20]

def get_uuid1_from_custom_sequence(sequence):
    try:
        value=uuid.UUID(sequence+str_node)
    except ValueError:
        return None
    else:
        return value


def uuid1(clock_seq=None, seconds=None):
    global node
    if not seconds:
        seconds=time.time()
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
    date=datetime.fromtimestamp(ts)
    date=date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    timestamp=date.timestamp()
    return int(timestamp)

def get_hour_timestamp(u):
    ''' this function extracts the hour from the date passed as argument (uuid1)
        and returns the truncated timestamp at 00min:00s in seconds.
        Because the date milliseconds is set to 0, the returned value
        is of type int '''
    ts=get_unix_timestamp(u)
    date=datetime.fromtimestamp(ts)
    date=date.replace(minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    timestamp=date.timestamp()
    return int(timestamp)


