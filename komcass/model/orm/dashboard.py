#coding: utf-8
'''
Created on 01/10/2014

@author: komlog crew
'''

class Dashboard:
    def __init__(self,bid,uid,dashboardname,creation_date,widgets=None):
        self.bid=bid
        self.uid=uid
        self.dashboardname=dashboardname
        self.creation_date=creation_date
        self.widgets=widgets if widgets else set()


