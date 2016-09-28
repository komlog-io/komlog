'''
Created on 01/10/2014

@author: komlog crew
'''

class UserSegment:
    def __init__(self, sid, description=None):
        self.sid=sid
        self.description=description

class UserSegmentQuo:
    def __init__(self, sid, quote, value):
        self.sid=sid
        self.quote=quote
        self.value=value

class UserSegmentTransition:
    def __init__(self, uid, date, sid=None, previous_sid=None):
        self.uid = uid
        self.date = date
        self.sid = sid
        self.previous_sid = previous_sid

class UserSegmentAllowedTransition:
    def __init__(self, sid, sids=None):
        self.sid = sid
        self.sids = sids if sids else set()

class UserSegmentFare:
    def __init__(self, sid, amount, currency, frequency):
        self.sid = sid
        self.amount = amount
        self.currency = currency
        self.frequency = frequency

