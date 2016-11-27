'''
This file contains the statements to operate with circle tables
Statements range (140000-149999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    140000:'select cid,uid,type,creation_date,circlename,members from mst_circle where cid=?',
    140001:'select cid,uid,type,creation_date,circlename,members from mst_circle where uid=? and type=? allow filtering',
    140002:'select cid,uid,type,creation_date,circlename,members from mst_circle where uid=?',
    140003:'select cid from mst_circle where uid=? and type=? allow filtering',
    140004:'select cid from mst_circle where uid=?',
    140005:'select count(*) from mst_circle where uid=? and type=? allow filtering',
    140006:'select count(*) from mst_circle where uid=?',
    145000:'insert into mst_circle (cid,uid,type,creation_date,circlename,members) values (?,?,?,?,?,?)',
    145001:'insert into mst_circle (cid,uid,type,creation_date,circlename,members) values (?,?,?,?,?,?) if not exists',
    147000:'delete from mst_circle where cid=?',
    147001:'delete members[?] from mst_circle where cid=?',
    149000:'update mst_circle set members=? where cid=?',
}

# selects (140000 - 144999)

# mst_circle

S_A_MSTCIRCLE_B_CID=140000
S_A_MSTCIRCLE_B_UID_TYPE=140001
S_A_MSTCIRCLE_B_UID=140002
S_CID_MSTCIRCLE_B_UID_TYPE=140003
S_CID_MSTCIRCLE_B_UID=140004
S_COUNT_MSTCIRCLE_B_UID_TYPE=140005
S_COUNT_MSTCIRCLE_B_UID=140006

# Inserts (145000 - 146999 )

# mst_circle

I_A_MSTCIRCLE=145000
I_A_MSTCIRCLE_INE=145001

# Deletes (147000 - 148999)

# mst_circle

D_A_MSTCIRCLE_B_CID=147000
D_MEMBER_MSTCIRCLE_B_MEMBER_CID=147001

# Updates (149000 - 149999)

# mst_circle

U_MEMBERS_MSTCIRCLE_B_CID=149000

