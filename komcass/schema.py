'''
Created on 14/12/2012

@author: jcazor
'''

import connection
from pycassa.cassandra.ttypes import NotFoundException

        
class Sample(object):
    def __init__(self, sid):
        print "Obteniendo: "+str(sid)
        try:
            self.sid, self.dbdict = connection.samples_cf.get(str(sid))
        except NotFoundException:
            self.sid = sid
            self.dbdict = None
    
    def insert(self, string):
        self.dbdict = {}
        col_prefix = 'char'
        index = 0
        for char in str(string):
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char
            index+=1
        connection.samples_cf.insert(self.sid, self.dbdict)
    
    def append(self, string):
        col_prefix = 'char'
        index = len(self.dbdict)
        for char in string:
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char
            index+=1
        connection.samples_cf.insert(self.sid, self.dbdict)     
        
        
        
            