#coding: utf-8
'''
This file contains the statements to operate with interface tables
Statements range (70000-79999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={70000:'select * from if_user_deny where uid=?',
            70001:'select * from if_user_deny where uid=? and interface=?',
            71000:'insert into if_user_deny (uid,interface,perm) values (?,?,?)',
            72000:'delete from if_user_deny where uid=? and interface=?',
            72001:'delete from if_user_deny where uid=?'
           }

# selects

S_A_IFUSERDENY_B_UID=70000
S_A_IFUSERDENY_B_UID_INTERFACE=70001

# Inserts

I_A_IFUSERDENY=71000

# Deletes

D_I_IFUSERDENY_B_UID_IFACE=72000
D_I_IFUSERDENY_B_UID=72001

