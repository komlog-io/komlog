'''
Created on 01/10/2014

@author: komlog crew
'''

class SignUp:
    def __init__(self, username, code, email, creation_date, utilization_date=None):
        self.username=username
        self.code=code
        self.email=email
        self.creation_date=creation_date
        self.utilization_date=utilization_date

class User:
    def __init__(self, username, uid, password, email, segment=None, creation_date=None, state=None):
        self.username=username
        self.uid=uid
        self.password=password
        self.email=email
        self.state=state
        self.segment=segment
        self.creation_date=creation_date

class BillingInfo:
    def __init__(self, uid, billing_day, last_billing):
        self.uid=uid
        self.billing_day=billing_day
        self.last_billing=last_billing

class StripeInfo:
    def __init__(self, uid, stripe_id):
        self.uid=uid
        self.stripe_id=stripe_id

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

class PendingHook:
    def __init__(self, uid, uri, sid):
        self.uid = uid
        self.uri = uri
        self.sid = sid

