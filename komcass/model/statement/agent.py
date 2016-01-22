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
            15000:'insert into mst_agent (aid,uid,agentname,pubkey,version,state,creation_date) values (?,?,?,?,?,?,?)',
            15001:'insert into mst_agent (aid,uid,agentname,pubkey,version,state,creation_date) values (?,?,?,?,?,?,?) if not exists',
            17000:'delete from mst_agent where aid=?',
           }

# selects (10000 - 14999)

# mst_agent

S_A_MSTAGENT_B_AID=10000
S_A_MSTAGENT_B_UID=10001
S_COUNT_MSTAGENT_B_UID=10002
S_AID_MSTAGENT_B_UID=10003

# Inserts (15000 - 16999)

# mst_agent

I_A_MSTAGENT=15000
I_A_MSTAGENT_INE=15001

# Deletes (17000 - 18999)

# mst_agent

D_A_MSTAGENT_B_AID=17000

# Update (19000 - 19999)

# mst_agent

