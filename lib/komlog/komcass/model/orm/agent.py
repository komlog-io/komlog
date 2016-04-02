#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''
class Agent:
    def __init__(self, aid, uid, agentname=None, pubkey=None, version=None, state=None, creation_date=None):
        self.aid=aid
        self.uid=uid
        self.agentname=agentname
        self.pubkey=pubkey
        self.version=version
        self.state=state
        self.creation_date=creation_date

class AgentPubkey:
    def __init__(self, uid, pubkey, aid, state):
        self.uid = uid
        self.pubkey = pubkey
        self.aid = aid
        self.state = state

class AgentChallenge:
    def __init__(self, aid, challenge, generated, validated=None):
        self.aid = aid
        self.challenge = challenge
        self.generated = generated
        self.validated = validated

