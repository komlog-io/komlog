#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Datapoint:

    def __init__(self, pid, did, uid, datapointname=None, color=None, creation_date=None):
        self.pid = pid
        self.did = did
        self.uid = uid
        self.datapointname = datapointname
        self.color = color
        self.creation_date = creation_date

class DatapointStats:

    def __init__(self, pid, decimal_separator=None, last_received=None):
        self.pid = pid
        self.decimal_separator = decimal_separator
        self.last_received = last_received

class DatapointData:

    def __init__(self, pid=None, date=None, value=None):
        self.pid = pid
        self.date = date
        self.value = value

class DatapointDtreePositives:

    def __init__(self, pid, date, position, length):
        self.pid = pid
        self.date = date
        self.position = position
        self.length = length

class DatapointDtreeNegatives:

    def __init__(self, pid, date, position, length):
        self.pid = pid
        self.date = date
        self.position = position
        self.length = length

