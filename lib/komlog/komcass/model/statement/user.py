'''
This file contains the statements to operate with user tables
Statements range (0-9999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    0:'select username,uid,password,email,segment,state,creation_date from mst_user where username=?',
    1:'select username,uid,password,email,segment,state,creation_date from mst_user where uid=?',
    2:'select username,uid,password,email,segment,state,creation_date from mst_user where email=?',
    3:'select uid from mst_user where username=?',
    100:'select username,email,code,inv_id,creation_date,utilization_date from mst_signup where email=?',
    101:'select username,email,code,inv_id,creation_date,utilization_date from mst_signup where username=?',
    102:'select username,email,code,inv_id,creation_date,utilization_date from mst_signup where code=?',
    200:'select inv_id,creation_date,state,count,max_count,active_from,active_until from mst_invitation where inv_id=?',
    300:'select email,date,state,inv_id from dat_invitation_request where email=?',
    301:'select email,date,state,inv_id from dat_invitation_request where state=?',
    302:'select email,date,state,inv_id from dat_invitation_request where state=? limit ?',
    400:'select code,date,state,uid from dat_forget_request where code=?',
    401:'select code,date,state,uid from dat_forget_request where state=?',
    402:'select code,date,state,uid from dat_forget_request where state=? limit ?',
    403:'select code,date,state,uid from dat_forget_request where uid=?',
    500:'select uid,uri,sid from mst_pending_hook where uid=?',
    501:'select uid,uri,sid from mst_pending_hook where uid=? and uri=?',
    502:'select uid,uri,sid from mst_pending_hook where uid=? and uri=? and sid=?',
    503:'select uid,uri,sid from mst_pending_hook where sid=?',
    600:'select uid,billing_day,last_billing from mst_user_billing_info where uid=?',
    601:'select uid,billing_day,last_billing from mst_user_billing_info where billing_day=?',
    700:'select uid,stripe_id from mst_user_stripe_info where uid=?',
    5000:'insert into mst_user (username,uid,password,email,state,segment,creation_date) values (?,?,?,?,?,?,?)',
    5001:'insert into mst_user (username,uid,password,email,state,segment,creation_date) values (?,?,?,?,?,?,?) if not exists',
    5100:'insert into mst_signup (username,email,code,inv_id,creation_date,utilization_date) values (?,?,?,?,?,?)',
    5200:'insert into mst_invitation (inv_id,creation_date,state,count,max_count,active_from,active_until) values (?,?,?,?,?,?,?)',
    5201:'insert into mst_invitation (inv_id,creation_date,state,count,max_count,active_from,active_until) values (?,?,?,?,?,?,?) if not exists',
    5300:'insert into dat_invitation_request (email,date,state,inv_id) values (?,?,?,?)',
    5301:'insert into dat_invitation_request (email,date,state,inv_id) values (?,?,?,?) if not exists',
    5400:'insert into dat_forget_request (code,date,state,uid) values (?,?,?,?)',
    5500:'insert into mst_pending_hook (uid,uri,sid) values (?,?,?)',
    5600:'insert into mst_user_billing_info (uid,billing_day,last_billing) values (?,?,?)',
    5601:'insert into mst_user_billing_info (uid,billing_day,last_billing) values (?,?,?) if not exists',
    5700:'insert into mst_user_stripe_info (uid,stripe_id) values (?,?)',
    5701:'insert into mst_user_stripe_info (uid,stripe_id) values (?,?) if not exists',
    7000:'delete from mst_user where username=?',
    7100:'delete from mst_signup where username=?',
    7200:'delete from mst_invitation where inv_id=?',
    7300:'delete from dat_invitation_request where email=?',
    7400:'delete from dat_forget_request where code=?',
    7500:'delete from mst_pending_hook where uid=?',
    7501:'delete from mst_pending_hook where uid=? and uri=?',
    7502:'delete from mst_pending_hook where uid=? and uri=? and sid=?',
    7600:'delete from mst_user_billing_info where uid=? if exists',
    7700:'delete from mst_user_stripe_info where uid=? if exists',
    9000:'update mst_user set password=? where username=? if exists',
    9001:'update mst_user set segment=? where username=? if exists',
    9002:'update mst_user set segment=? where username=? if segment = ?',
    9200:'update mst_invitation set count=? where inv_id=? if count=?',
    9201:'update mst_invitation set state=? where inv_id=? if exists',
    9300:'update dat_invitation_request set state=? where email=? if exists',
    9400:'update dat_forget_request set state=? where code=? if exists',
    9600:'update mst_user_billing_info set billing_day = ? where uid = ?',
    9601:'update mst_user_billing_info set billing_day = ? where uid = ? if billing_day=?',
    9602:'update mst_user_billing_info set last_billing=? where uid=?',
    9603:'update mst_user_billing_info set last_billing=? where uid=? if last_billing=?',
}

# selects (0 - 4999)

# mst_user

S_A_MSTUSER_B_USERNAME=0
S_A_MSTUSER_B_UID=1
S_A_MSTUSER_B_EMAIL=2
S_UID_MSTUSER_B_USERNAME=3

# mst_signup

S_A_MSTSIGNUP_B_EMAIL=100
S_A_MSTSIGNUP_B_USERNAME=101
S_A_MSTSIGNUP_B_CODE=102

# mst_invitation

S_A_MSTINVITATION_B_INVID=200

# dat_invitation_request

S_A_DATINVITATIONREQUEST_B_EMAIL=300
S_A_DATINVITATIONREQUEST_B_STATE=301
S_A_DATINVITATIONREQUEST_B_STATE_NUM=302

# dat_forget_request

S_A_DATFORGETREQUEST_B_CODE=400
S_A_DATFORGETREQUEST_B_STATE=401
S_A_DATFORGETREQUEST_B_STATE_NUM=402
S_A_DATFORGETREQUEST_B_UID=403

# mst_pending_hook

S_A_MSTPENDINGHOOK_B_UID=500
S_A_MSTPENDINGHOOK_B_UID_URI=501
S_A_MSTPENDINGHOOK_B_UID_URI_SID=502
S_A_MSTPENDINGHOOK_B_SID=503

# mst_user_billing_info

S_A_MSTUSERBILLINGINFO_B_UID            = 600
S_A_MSTUSERBILLINGINFO_B_BILLINGDAY     = 601

# mst_user_stripe_info

S_A_MSTUSERSTRIPEINFO_B_UID             = 700

# Inserts (5000 - 6999)

# mst_user

I_A_MSTUSER=5000
I_A_MSTUSER_INE=5001

# mst_signup

I_A_MSTSIGNUP=5100

# mst_invitation

I_A_MSTINVITATION=5200
I_A_MSTINVITATION_INE=5201

# dat_invitation_request

I_A_DATINVITATIONREQUEST=5300
I_A_DATINVITATIONREQUEST_INE=5301

# dat_forget_request

I_A_DATFORGETREQUEST=5400

# mst_pending_hook

I_A_MSTPENDINGHOOK=5500

# mst_user_billing_info

I_A_MSTUSERBILLINGINFO              = 5600
I_A_MSTUSERBILLINGINFO_INE          = 5601

# mst_user_stripe_info

I_A_MSTUSERSTRIPEINFO               = 5700
I_A_MSTUSERSTRIPEINFO_INE           = 5701

# Deletes (7000 - 8999)

# mst_user

D_A_MSTUSER_B_USERNAME=7000

# mst_signup

D_A_MSTSIGNUP_B_USERNAME=7100

# mst_invitation

D_A_MSTINVITATION_B_INVID=7200

# dat_invitation_request

D_A_DATINVITATIONREQUEST_B_EMAIL=7300

# dat_forget_request

D_A_DATFORGETREQUEST_B_CODE=7400

# mst_pending_hook

D_A_MSTPENDINGHOOK_B_UID=7500
D_A_MSTPENDINGHOOK_B_UID_URI=7501
D_A_MSTPENDINGHOOK_B_UID_URI_SID=7502

# mst_user_billing_info

D_A_MSTUSERBILLINGINFO_B_UID_IE        = 7600

# mst_user_stripe_info

D_A_MSTUSERSTRIPEINFO_B_UID_IE         = 7700

# Updates (9000 - 9999)

# mst_user

U_PASSWORD_MSTUSER_B_USERNAME=9000
U_SEGMENT_MSTUSER_B_USERNAME=9001
U_SEGMENT_MSTUSER_B_USERNAME_IEQ_SEGMENT=9002

# mst_signup

# mst_invitation

U_COUNT_MSTINVITATION_I_COUNT = 9200
U_STATE_MSTINVITATION_B_INVID = 9201

# dat_invitation_request

U_STATE_DATINVITATIONREQUEST_B_EMAIL=9300

# dat_forget_request

U_STATE_DATFORGETREQUEST_B_CODE=9400

# mst_user_billing_info

U_BILLINGDAY_MSTUSERBILLINGINFO_B_UID                    = 9600
U_BILLINGDAY_MSTUSERBILLINGINFO_B_UID_IEQ_BILLINGDAY     = 9601
U_LASTBILLING_MSTUSERBILLINGINFO_B_UID                   = 9602
U_LASTBILLING_MSTUSERBILLINGINFO_B_UID_IEQ_LASTBILLING   = 9603

