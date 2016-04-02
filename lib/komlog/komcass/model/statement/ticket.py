'''
This file contains the statements to operate with ticket tables
Statements range (160000-169999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={160000:'select * from auth_ticket where tid=?',
            160100:'select * from auth_ticket_expired where tid=?',
            165000:'insert into auth_ticket (tid,date,uid,expires,allowed_uids,allowed_cids,resources,permissions,interval_init,interval_end) values (?,?,?,?,?,?,?,?,?,?)',
            165001:'insert into auth_ticket (tid,date,uid,expires,allowed_uids,allowed_cids,resources,permissions,interval_init,interval_end) values (?,?,?,?,?,?,?,?,?,?) if not exists',
            165100:'insert into auth_ticket_expired (tid,date,uid,expires,allowed_uids,allowed_cids,resources,permissions,interval_init,interval_end) values (?,?,?,?,?,?,?,?,?,?)',
            167000:'delete from auth_ticket where tid=?',
            167100:'delete from auth_ticket_expired where tid=?',
           }

# selects (160000-164999)

# dat_auth_ticket

S_A_AUTHTICKET_B_TID=160000

# dat_auth_ticket_expired

S_A_AUTHTICKETEXPIRED_B_TID=160100

# Inserts (165000 - 166999)

# dat_auth_ticket

I_A_AUTHTICKET=165000
I_A_AUTHTICKET_INE=165001

# dat_auth_ticket_expired

I_A_AUTHTICKETEXPIRED=165100

# Deletes (167000 - 168999)

# dat_auth_ticket

D_A_AUTHTICKET_B_TID=167000

# dat_auth_ticket_expired

D_A_AUTHTICKETEXPIRED_B_TID=167100

# Updates (169000 - 169999)


