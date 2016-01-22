'''
This file contains the statements to operate with user tables
Statements range (0-9999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={0:'select * from mst_user where username=?',
            1:'select * from mst_user where uid=?',
            2:'select * from mst_user where email=?',
            3:'select uid from mst_user where username=?',
            100:'select * from mst_signup where email=?',
            101:'select * from mst_signup where username=?',
            102:'select * from mst_signup where signup_code=?',
            200:'select * from dat_invitation where inv_id=? order by date desc;',
            300:'select * from dat_invitation_request where email=?',
            301:'select * from dat_invitation_request where state=?',
            302:'select * from dat_invitation_request where state=? limit ?',
            400:'select * from dat_forget_request where code=?',
            401:'select * from dat_forget_request where state=?',
            402:'select * from dat_forget_request where state=? limit ?',
            5000:'insert into mst_user (username,uid,password,email,state,segment,creation_date) values (?,?,?,?,?,?,?)',
            5001:'insert into mst_user (username,uid,password,email,state,segment,creation_date) values (?,?,?,?,?,?,?) if not exists',
            5100:'insert into mst_signup (username,signup_code,email,creation_date,utilization_date) values (?,?,?,?,?)',
            5200:'insert into dat_invitation (inv_id,date,state,tran_id) values (?,?,?,?)',
            5300:'insert into dat_invitation_request (email,date,state,inv_id) values (?,?,?,?)',
            5400:'insert into dat_forget_request (code,date,state,uid) values (?,?,?,?)',
            7000:'delete from mst_user where username=?',
            7100:'delete from mst_signup where username=?',
            7200:'delete from dat_invitation where inv_id=? and date=?',
            7300:'delete from dat_invitation_request where email=?',
            7400:'delete from dat_forget_request where code=?',
            9000:'update mst_user set password=? where username=? if exists',
            9300:'update dat_invitation_request set state=? where email=? if exists',
            9400:'update dat_forget_request set state=? where code=? if exists',
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
S_A_MSTSIGNUP_B_SIGNUPCODE=102

# dat_invitation

S_A_DATINVITATION_B_INVID=200

# dat_invitation_request

S_A_DATINVITATIONREQUEST_B_EMAIL=300
S_A_DATINVITATIONREQUEST_B_STATE=301
S_A_DATINVITATIONREQUEST_B_STATE_NUM=302

# dat_forget_request

S_A_DATFORGETREQUEST_B_CODE=400
S_A_DATFORGETREQUEST_B_STATE=401
S_A_DATFORGETREQUEST_B_STATE_NUM=402

# Inserts (5000 - 6999)

# mst_user

I_A_MSTUSER=5000
I_A_MSTUSER_INE=5001

# mst_signup

I_A_MSTSIGNUP=5100

# dat_invitation

I_A_DATINVITATION=5200

# dat_invitation_request

I_A_DATINVITATIONREQUEST=5300

# dat_forget_request

I_A_DATFORGETREQUEST=5400

# Deletes (7000 - 8999)

# mst_user

D_A_MSTUSER_B_USERNAME=7000

# mst_signup

D_A_MSTSIGNUP_B_USERNAME=7100

# dat_invitation

D_A_DATINVITATION_B_INVID_DATE=7200

# dat_invitation_request

D_A_DATINVITATIONREQUEST_B_EMAIL=7300

# dat_forget_request

D_A_DATFORGETREQUEST_B_CODE=7400

# Updates (9000 - 9999)

# mst_user

U_PASSWORD_MSTUSER_B_USERNAME=9000

# mst_signup

# dat_invitation

# dat_invitation_request

U_STATE_DATINVITATIONREQUEST_B_EMAIL=9300

# dat_forget_request

U_STATE_DATFORGETREQUEST_B_CODE=9400

