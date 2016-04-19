#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Datasource:
    def __init__(self, did, aid=None, uid=None, datasourcename=None, creation_date=None):
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

class DatasourceTextSummary:
    def __init__(self, did, date, content_length, num_lines, num_words, word_frecuency):
        self.did=did
        self.date=date
        self.content_length=content_length
        self.num_lines=num_lines
        self.num_words=num_words
        self.word_frecuency=word_frecuency

class DatasourceNoveltyDetector:
    def __init__(self, did, pid, date, nd, features):
        self.did=did
        self.pid=pid
        self.date=date
        self.nd=nd
        self.features=features

