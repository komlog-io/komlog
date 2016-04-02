import uuid
import time
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

