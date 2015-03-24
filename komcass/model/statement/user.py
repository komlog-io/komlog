#coding: utf-8
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
            2:'select * from mst_signup where email=?',
            3:'select * from mst_signup where username=?',
            4:'select * from mst_signup where signup_code=?',
            5:'select * from mst_user where email=?',
            6:'select uid from mst_user where username=?',
            1000:'insert into mst_user (username,uid,password,email,state,segment,creation_date) values (?,?,?,?,?,?,?)',
            1001:'insert into mst_signup (username,signup_code,email,creation_date,utilization_date) values (?,?,?,?,?)',
            2000:'delete from mst_user where username=?',
            2001:'delete from mst_signup where username=?',
           }

# selects

S_A_MSTUSER_B_USERNAME=0
S_A_MSTUSER_B_UID=1
S_A_MSTSIGNUP_B_EMAIL=2
S_A_MSTSIGNUP_B_USERNAME=3
S_A_MSTSIGNUP_B_SIGNUPCODE=4
S_A_MSTUSER_B_EMAIL=5
S_UID_MSTUSER_B_USERNAME=6

# Inserts

I_A_MSTUSER=1000
I_A_MSTSIGNUP=1001

# Deletes

D_A_MSTUSER_B_USERNAME=2000
D_A_MSTSIGNUP_B_USERNAME=2001

