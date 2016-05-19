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
            10100:'select * from mst_agent_pubkey where uid=?',
            10101:'select * from mst_agent_pubkey where uid=? and pubkey=?',
            10200:'select * from mst_agent_challenge where aid=? and challenge=?',
            15000:'insert into mst_agent (aid,uid,agentname,pubkey,version,state,creation_date) values (?,?,?,?,?,?,?)',
            15001:'insert into mst_agent (aid,uid,agentname,pubkey,version,state,creation_date) values (?,?,?,?,?,?,?) if not exists',
            15100:'insert into mst_agent_pubkey (uid,pubkey,aid,state) values (?,?,?,?)',
            15101:'insert into mst_agent_pubkey (uid,pubkey,aid,state) values (?,?,?,?) if not exists',
            15200:'insert into mst_agent_challenge (aid,challenge,generated,validated) values (?,?,?,?)',
            17000:'delete from mst_agent where aid=?',
            17100:'delete from mst_agent_pubkey where uid=? and pubkey=?',
            17200:'delete from mst_agent_challenge where aid=? and challenge=?',
            17201:'delete from mst_agent_challenge where aid=?',
           }

# selects (10000 - 14999)

# mst_agent

S_A_MSTAGENT_B_AID=10000
S_A_MSTAGENT_B_UID=10001
S_COUNT_MSTAGENT_B_UID=10002
S_AID_MSTAGENT_B_UID=10003

# mst_agent_pubkey

S_A_MSTAGENTPUBKEY_B_UID=10100
S_A_MSTAGENTPUBKEY_B_UID_PUBKEY=10101

# mst_agent_challenge

S_A_MSTAGENTCHALLENGE_B_AID_CH=10200

# Inserts (15000 - 16999)

# mst_agent

I_A_MSTAGENT=15000
I_A_MSTAGENT_INE=15001

# mst_agent_pubkey

I_A_MSTAGENTPUBKEY=15100
I_A_MSTAGENTPUBKEY_INE=15101

# mst_agent_challenge

I_A_MSTAGENTCHALLENGE=15200

# Deletes (17000 - 18999)

# mst_agent

D_A_MSTAGENT_B_AID=17000

# mst_agent_pubkey

D_A_MSTAGENTPUBKEY=17100

# mst_agent_challenge

D_A_MSTAGENTCHALLENGE_B_AID_CHALLENGE=17200
D_A_MSTAGENTCHALLENGE_B_AID=17201

# Update (19000 - 19999)

# mst_agent

