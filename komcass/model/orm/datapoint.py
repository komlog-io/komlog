#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Datapoint:
    def __init__(self, pid, did=None, datapointname=None, color=None, creation_date=None):
        self.pid=pid
        self.did=did
        self.datapointname=datapointname
        self.color=color
        self.creation_date=creation_date

class DatapointStats:
    def __init__(self, pid, dtree=None, dtree_inv=None, decimal_separator=None, last_received=None):
        self.pid=pid
        self.dtree=dtree
        self.dtree_inv=dtree_inv
        self.decimal_separator=decimal_separator
        self.last_received=last_received

class DatapointData:
    def __init__(self, pid=None, date=None, value=None):
        self.pid=pid
        self.date=date
        self.value=value

class DatapointDtreePositives:
    def __init__(self, pid=None, date=None, position=None, length=None):
        self.pid=pid
        self.date=date
        self.position=position
        self.length=length

class DatapointDtreeNegatives:
    def __init__(self, pid=None, date=None, coordinates=None):
        self.pid=pid
        self.date=date
        self.coordinates=coordinates

