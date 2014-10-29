#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''
class Agent:
    def __init__(self, aid=None, uid=None, agentname=None, pubkey=None, version=None, state=None, creation_date=None):
        self.aid=aid
        self.uid=uid
        self.agentname=agentname
        self.pubkey=pubkey
        self.version=version
        self.state=state
        self.creation_date=creation_date
