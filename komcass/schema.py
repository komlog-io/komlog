'''
Created on 14/12/2012

@author: jcazor
'''

from pycassa.cassandra.ttypes import NotFoundException

        
class Sample(object):
    def __init__(self, sid, col_fam):
        print "Obteniendo: "+str(sid)
        try:
            self.sid, self.dbdict = col_fam.get(str(sid))
        except NotFoundException:
            self.sid = sid
            self.dbdict = None
    
    def insert(self, string, col_fam):
        self.dbdict = {}
        col_prefix = 'char'
        index = 0
        for char in str(string):
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char
            index+=1
        col_fam.insert(self.sid, self.dbdict)
    
    def append(self, string, col_fam):
        col_prefix = 'char'
        index = len(self.dbdict)
        for char in string:
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char
            index+=1
        col_fam.insert(self.sid, self.dbdict)     
        
        
        
            