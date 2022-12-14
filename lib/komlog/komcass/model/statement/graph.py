'''
This file contains the statements to operate with graph tables
Statements range (130000-139999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    130012:'select idd,ido,type,creation_date,uri from gr_uri_in where idd=?',
    130013:'select ido,idd,type,creation_date,uri from gr_uri_out where ido=?',
    130014:'select idd,ido,type,creation_date,uri from gr_uri_in where idd=? and ido=?',
    130015:'select ido,idd,type,creation_date,uri from gr_uri_out where ido=? and idd=?',
    130016:'select ido from gr_uri_in where idd=?',
    130017:'select idd from gr_uri_out where ido=?',
    130018:'select idd,ido,type,creation_date,params from gr_kin_in where idd=?',
    130019:'select ido,idd,type,creation_date,params from gr_kin_out where ido=?',
    130020:'select idd,ido,type,creation_date,params from gr_kin_in where idd=? and ido=?',
    130021:'select ido,idd,type,creation_date,params from gr_kin_out where ido=? and idd=?',
    130022:'select ido from gr_kin_in where idd=?',
    130023:'select idd from gr_kin_out where ido=?',
    131004:'insert into gr_uri_in (idd,ido,type,creation_date,uri) values (?,?,?,?,?)',
    131005:'insert into gr_uri_out (ido,idd,type,creation_date,uri) values (?,?,?,?,?)',
    131006:'insert into gr_kin_in (idd,ido,type,creation_date,params) values (?,?,?,?,?)',
    131007:'insert into gr_kin_out (ido,idd,type,creation_date,params) values (?,?,?,?,?)',
    132004:'delete from gr_uri_in where idd=? and ido=?',
    132005:'delete from gr_uri_out where ido=? and idd=?',
    132006:'delete from gr_kin_in where idd=? and ido=?',
    132007:'delete from gr_kin_out where ido=? and idd=?',
}

# selects

S_A_GRURIIN_B_IDD=130012
S_A_GRURIOUT_B_IDO=130013
S_A_GRURIIN_B_IDD_IDO=130014
S_A_GRURIOUT_B_IDO_IDD=130015
S_IDO_GRURIIN_B_IDD=130016
S_IDD_GRURIOUT_B_IDO=130017
S_A_GRKININ_B_IDD=130018
S_A_GRKINOUT_B_IDO=130019
S_A_GRKININ_B_IDD_IDO=130020
S_A_GRKINOUT_B_IDO_IDD=130021
S_IDO_GRKININ_B_IDD=130022
S_IDD_GRKINOUT_B_IDO=130023

# Inserts

I_A_GRURIIN=131004
I_A_GRURIOUT=131005
I_A_GRKININ=131006
I_A_GRKINOUT=131007

# Deletes

D_A_GRURIIN_B_IDD_IDO=132004
D_A_GRURIOUT_B_IDO_IDD=132005
D_A_GRKININ_B_IDD_IDO=132006
D_A_GRKINOUT_B_IDO_IDD=132007

