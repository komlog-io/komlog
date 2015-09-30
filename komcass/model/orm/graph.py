'''
Created on 27/02/2015

@author: komlog crew
'''


class UriRelation(object):
    def __init__(self, ido, idd, type, creation_date, uri):
        self.ido=ido
        self.idd=idd
        self.type=type
        self.creation_date=creation_date
        self.uri=uri

class KinRelation(object):
    def __init__(self, ido, idd, type, creation_date, params=None):
        self.ido=ido
        self.idd=idd
        self.type=type
        self.creation_date=creation_date
        self.params=params if params else dict()

