'''
Created on 25/09/2015

@author: komlog crew
'''

class Ticket(object):
    def __init__(self, tid, date, uid, expires, allowed_uids, allowed_cids, resources, permissions, interval_init, interval_end):
        self.tid=tid
        self.date=date
        self.uid=uid
        self.expires=expires
        self.allowed_uids=allowed_uids if allowed_uids else set()
        self.allowed_cids=allowed_cids if allowed_cids else set()
        self.resources=resources if resources else set()
        self.permissions=permissions if permissions else dict()
        self.interval_init=interval_init
        self.interval_end=interval_end

