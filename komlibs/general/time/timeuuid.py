import uuid
import time
import random

node=0x010000000000
str_node='010000000000'

def get_unix_timestamp(u):
    return int((u.time - 0x01B21DD213814000) / 10000000.0 * 1000)/1000.0

def get_custom_sequence(u):
    return u.hex[0:20]

def get_uuid1_from_custom_sequence(sequence):
    return uuid.UUID(sequence+str_node)

def uuid1(clock_seq=None, seconds=None):
    '''Generate a UUID from a host ID, sequence number, and time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen.
    if seconds is given, is used to generate the timestamp of the UUID object,
    otherwise, the current time is used '''
    
    global node
    if not seconds:
        seconds=time.time()
    nanoseconds=int(seconds * 1e9)
    # 0x01b21dd213814000 is the number of 100-ns intervals between the
    # UUID epoch 1582-10-15 00:00:00 and the Unix epoch 1970-01-01 00:00:00.
    timestamp = int(nanoseconds/100) + 0x01b21dd213814000
    if clock_seq is None:
        clock_seq = random.randrange(1<<14) # instead of stable storage
    time_low = timestamp & 0xffffffff
    time_mid = (timestamp >> 32) & 0xffff
    time_hi_version = (timestamp >> 48) & 0x0fff
    clock_seq_low = clock_seq & 0xff
    clock_seq_hi_variant = (clock_seq >> 8) & 0x3f
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version,
                        clock_seq_hi_variant, clock_seq_low, node), version=1)

