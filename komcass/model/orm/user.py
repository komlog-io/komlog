'''
Created on 01/10/2014

@author: komlog crew
'''

class SignUp:
    def __init__(self, username=None, signup_code=None, email=None, creation_date=None, utilization_date=None):
        self.username=username
        self.signup_code=signup_code
        self.email=email
        self.creation_date=creation_date
        self.utilization_date=utilization_date


class User:
    def __init__(self, username=None, uid=None, password=None, email=None, segment=None, creation_date=None, state=None):
        self.username=username
        self.uid=uid
        self.password=password
        self.email=email
        self.state=state
        self.segment=segment
        self.creation_date=creation_date

class Invitation:
    def __init__(self, inv_id, date, state, tran_id=None):
        self.inv_id=inv_id
        self.date=date
        self.state=state
        self.tran_id=tran_id

class InvitationRequest:
    def __init__(self, email, date, state, inv_id=None):
        self.email=email
        self.date=date
        self.state=state
        self.inv_id=inv_id

class ForgetRequest:
    def __init__(self, code, date, state, uid=None):
        self.code=code
        self.date=date
        self.state=state
        self.uid=uid

