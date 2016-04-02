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
            75000:'insert into if_user_deny (uid,interface,perm) values (?,?,?)',
            77000:'delete from if_user_deny where uid=? and interface=?',
            77001:'delete from if_user_deny where uid=?'
           }

# selects (70000 - 74999)

# if_user_deny

S_A_IFUSERDENY_B_UID=70000
S_A_IFUSERDENY_B_UID_INTERFACE=70001

# Inserts (75000 - 76999)

# if_user_deny

I_A_IFUSERDENY=75000

# Deletes (77000 - 78999)

# if_user_deny

D_I_IFUSERDENY_B_UID_IFACE=77000
D_I_IFUSERDENY_B_UID=77001

# Updates (79000 - 79999)

# if_user_deny

