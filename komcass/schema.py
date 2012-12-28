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
    
    def insert(self, ucontent, col_fam):
        self.dbdict = {}
        col_prefix = 'du'
        index = 0
        for char in ucontent:
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char.encode('utf8')
            index+=1
        col_fam.insert(self.sid, self.dbdict)
    
    def append(self, ucontent, col_fam):
        col_prefix = 'du'
        index = len(self.dbdict)
        for char in ucontent:
            col_name = col_prefix+str(str(index).zfill(9))
            self.dbdict[col_name]=char.encode('utf8')
            index+=1
        col_fam.insert(self.sid, self.dbdict)     
        
        
        
            