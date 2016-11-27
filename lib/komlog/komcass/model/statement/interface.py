'''
This file contains the statements to operate with interface tables
Statements range (70000-79999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    70000:'select uid,interface,content from if_user_deny where uid=?',
    70001:'select uid,interface,content from if_user_deny where uid=? and interface=?',
    70100:'select uid,interface,ts,content from if_ts_user_deny where uid=?',
    70101:'select uid,interface,ts,content from if_ts_user_deny where uid=? and interface=?',
    70102:'select uid,interface,ts,content from if_ts_user_deny where uid=? and interface=? and ts=?',
    70103:'select uid,interface,ts,content from if_ts_user_deny where uid=? and interface=? and ts>=? and ts<=?',
    75000:'insert into if_user_deny (uid,interface,content) values (?,?,?)',
    75100:'insert into if_ts_user_deny (uid,interface,ts,content) values (?,?,?,?)',
    75101:'insert into if_ts_user_deny (uid,interface,ts,content) values (?,?,?,?) if not exists',
    77000:'delete from if_user_deny where uid=? and interface=? if exists',
    77001:'delete from if_user_deny where uid=?',
    77100:'delete from if_ts_user_deny where uid=?',
    77101:'delete from if_ts_user_deny where uid=? and interface=?',
    77102:'delete from if_ts_user_deny where uid=? and interface=? and ts=? if exists',
    77103:'delete from if_ts_user_deny where uid=? and interface=? and ts>=? and ts<=?',
}

# selects (70000 - 74999)

# if_user_deny

S_A_IFUSERDENY_B_UID=70000
S_A_IFUSERDENY_B_UID_INTERFACE=70001

# if_ts_user_deny

S_A_IFTSUSERDENY_B_UID=70100
S_A_IFTSUSERDENY_B_UID_INTERFACE=70101
S_A_IFTSUSERDENY_B_UID_INTERFACE_TS=70102
S_A_IFTSUSERDENY_B_UID_INTERFACE_ITS_ETS=70103

# Inserts (75000 - 76999)

# if_user_deny

I_A_IFUSERDENY=75000

# if_ts_user_deny

I_A_IFTSUSERDENY=75100
I_A_IFTSUSERDENY_INE=75101

# Deletes (77000 - 78999)

# if_user_deny

D_I_IFUSERDENY_B_UID_IFACE_IE=77000
D_I_IFUSERDENY_B_UID=77001

# if_ts_user_deny

D_A_IFTSUSERDENY_B_UID=77100
D_A_IFTSUSERDENY_B_UID_INTERFACE=77101
D_A_IFTSUSERDENY_B_UID_INTERFACE_TS_IE=77102
D_A_IFTSUSERDENY_B_UID_INTERFACE_ITS_ETS=77103

# Updates (79000 - 79999)

# if_user_deny

# if_ts_user_deny

