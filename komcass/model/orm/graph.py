'''
Created on 27/02/2015

@author: komlog crew
'''


class MemberRelation(object):
    def __init__(self, ido, idd, type, creation_date):
        self.ido=ido
        self.idd=idd
        self.type=type
        self.creation_date=creation_date

class BoundedShareRelation(object):
    def __init__(self, ido, idd, type, creation_date, perm, interval_init, interval_end):
        self.ido=ido
        self.idd=idd
        self.type=type
        self.creation_date=creation_date
        self.perm=perm
        self.interval_init=interval_init
        self.interval_end=interval_end

