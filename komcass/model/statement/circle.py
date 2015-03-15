'''
This file contains the statements to operate with circle tables
Statements range (140000-149999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={140000:'select * from mst_circle where cid=?',
            140001:'select * from mst_circle where uid=? and type=? allow filtering',
            140002:'select * from mst_circle where uid=?',
            140003:'select cid from mst_circle where uid=? and type=? allow filtering',
            140004:'select cid from mst_circle where uid=?',
            140005:'select count(*) from mst_circle where uid=? and type=? allow filtering',
            140006:'select count(*) from mst_circle where uid=?',
            141000:'insert into mst_circle (cid,uid,type,creation_date,circlename,members) values (?,?,?,?,?,?)',
            142000:'delete from mst_circle where cid=?',
            142001:'delete members[?] from mst_circle where cid=?',
            143000:'update mst_circle set members=? where cid=?',
           }

# selects

S_A_MSTCIRCLE_B_CID=140000
S_A_MSTCIRCLE_B_UID_TYPE=140001
S_A_MSTCIRCLE_B_UID=140002
S_CID_MSTCIRCLE_B_UID_TYPE=140003
S_CID_MSTCIRCLE_B_UID=140004
S_COUNT_MSTCIRCLE_B_UID_TYPE=140005
S_COUNT_MSTCIRCLE_B_UID=140006

# Inserts

I_A_MSTCIRCLE=141000

# Deletes

D_A_MSTCIRCLE_B_CID=142000
D_MEMBER_MSTCIRCLE_B_MEMBER_CID=142001

# Updates

U_MEMBERS_MSTCIRCLE_B_CID=143000

