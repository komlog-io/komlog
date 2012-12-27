'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema

class Sample(object):
    def __init__(self, sid, col_fam, content=None):
        if not content:
            self.dbsample = schema.Sample(sid,col_fam)
            self.sid = self.dbsample.sid
            self.dbdict = self.dbsample.dbdict
        else:
            self.dbsample = None
            self.sid = sid
            self.content = content
            self.dbdict = None
        print "Sample: "+str(self.dbsample)
        print "sid: "+str(self.sid)
        print "dbdict: "+str(self.dbdict)
    
    def insert(self, col_fam):
        ''' Insert a sample if it doesn't exists yet'''
        if not self.dbsample:
            self.dbsample = schema.Sample(self.sid, col_fam)
            self.dbsample.insert(self.content, col_fam)         
        else:
            raise exceptions.AlreadyExistingSample()
    
    def append(self, content, col_fam):
        self.dbsample.append(content, col_fam)
    
    def get_content(self):
        if not self.content:
            self.content = ''.join(self.dbdict.values())
        return self.content
    
def get_sample(sid, col_fam):
    return Sample(sid, col_fam)

def get_sample_list(sids, col_fam):
    samples = []
    for sid in sids:
        samples.append(Sample(sid, col_fam))
    return samples

            