'''
Created on 10/03/2015

@author: komlog crew
'''

from komcass.model.parametrization.widget import types

class Circle(object):
    def __init__(self,cid,uid,type,creation_date,circlename,members):
        self.cid=cid
        self.uid=uid
        self.type=type
        self.creation_date=creation_date
        self.circlename=circlename
        self.members=members if members else set()

