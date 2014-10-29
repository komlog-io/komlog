#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Datasource:
    def __init__(self, did, aid=None, uid=None, datasourcename=None, state=None, creation_date=None):
        self.did=did
        self.aid=aid
        self.uid=uid
        self.datasourcename=datasourcename
        self.state=state
        self.creation_date=creation_date

class DatasourceStats:
    def __init__(self, did, last_received=None, last_mapped=None):
        self.did=did
        self.last_received=last_received
        self.last_mapped=last_mapped

class DatasourceData:
    def __init__(self, did, date=None, content=None):
        self.did=did
        self.date=date
        self.content=content

class DatasourceMap:
    def __init__(self, did, date=None, content=None, variables=None, datapoints=None):
        self.did=did
        self.date=date
        self.content=content
        self.variables=variables
        self.datapoints=datapoints

