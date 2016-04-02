#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class UserIfaceDeny:
    ''' This class is used to register interfaces whose access is denied to user requests'''
    def __init__(self, uid, interface=None, perm=None):
        self.uid=uid
        self.interface=interface
        self.perm=perm

