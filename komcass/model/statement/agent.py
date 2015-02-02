#coding: utf-8
'''
This file contains the statements to operate with agent tables
Statements range (10000-19999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={10000:'select * from mst_agent where aid=?',
            10001:'select * from mst_agent where uid=?',
            10002:'select count(*) from mst_agent where uid=?',
            10003:'select aid from mst_agent where uid=?',
            11000:'insert into mst_agent (aid,uid,agentname,pubkey,version,state,creation_date) values (?,?,?,?,?,?,?)',
            12000:'delete from mst_agent where aid=?',
           }

# selects

S_A_MSTAGENT_B_AID=10000
S_A_MSTAGENT_B_UID=10001
S_COUNT_MSTAGENT_B_UID=10002
S_AID_MSTAGENT_B_UID=10003

# Inserts

I_A_MSTAGENT=11000

# Deletes

D_A_MSTAGENT_B_AID=12000

