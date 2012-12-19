'''
Created on 14/12/2012

@author: jcazor
'''

import exceptions, schema

class Sample(object):
    def __init__(self, sid, content=None):
        if not content:
            self.dbsample = schema.Sample(sid)
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
    
    def insert(self):
        ''' Insert a sample if it doesn't exists yet'''
        if not self.dbsample:
            self.dbsample = schema.Sample(self.sid)
            self.dbsample.insert(self.content)         
        else:
            raise exceptions.AlreadyExistingSample()
    
    def append(self, content):
        self.dbsample.append(content)
    
    def get_content(self):
        if not self.content:
            self.content = ''.join(self.dbdict.values())
        return self.content
    
def get_sample(sid):
    return Sample(sid)

def get_sample_list(sids):
    samples = []
    for sid in sids:
        samples.append(Sample(sid))
    return samples

            