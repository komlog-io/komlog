#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Datasource:
    def __init__(self, did, aid, uid, datasourcename, creation_date):
        self.did=did
        self.aid=aid
        self.uid=uid
        self.datasourcename=datasourcename
        self.creation_date=creation_date

class DatasourceStats:
    def __init__(self, did, last_received=None, last_mapped=None):
        self.did=did
        self.last_received=last_received
        self.last_mapped=last_mapped

class DatasourceData:
    def __init__(self, did, date, content):
        self.did=did
        self.date=date
        self.content=content

    def get_sequence(self):
        return self.date.clock_seq

class DatasourceMap:
    def __init__(self, did, date, variables, datapoints=None):
        self.did=did
        self.date=date
        self.variables=variables if variables else dict()
        self.datapoints=datapoints if datapoints else dict()

class DatasourceHash:
    def __init__(self, did, date, content):
        self.did=did
        self.date=date
        self.content=content

class DatasourceMetadata:
    def __init__(self, did, date, size):
        self.did=did
        self.date=date
        self.size=size

class DatasourceSupplies:

    def __init__(self, did, date, supplies):
        self.did = did
        self.date = date
        self.supplies = list(supplies) if supplies != None else []

class DatapointClassifierDtree:

    def __init__(self, did, dtree):
        self.did = did
        self.dtree = dtree

class DatasourceFeatures:

    def __init__(self, did, date, features):
        self.did = did
        self.date = date
        self.features = list(features) if features != None else []

class DatasourceByFeature:

    def __init__(self, feature, did, weight):
        self.feature = feature
        self.did = did
        self.weight = weight

