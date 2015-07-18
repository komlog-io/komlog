'''
This file contains the statements to operate with graph tables
Statements range (130000-139999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={130000:'select * from gr_member_in where idd=?',
            130001:'select * from gr_member_out where ido=?',
            130002:'select * from gr_member_in where idd=? and ido=?',
            130003:'select * from gr_member_out where ido=? and idd=?',
            130004:'select * from gr_bounded_share_in where idd=?',
            130005:'select * from gr_bounded_share_out where ido=?',
            130006:'select * from gr_bounded_share_in where idd=? and ido=?',
            130007:'select * from gr_bounded_share_out where ido=? and idd=?',
            130008:'select ido from gr_member_in where idd=?',
            130009:'select idd from gr_member_out where ido=?',
            130010:'select ido from gr_bounded_share_in where idd=?',
            130011:'select idd from gr_bounded_share_out where ido=?',
            130012:'select * from gr_uri_in where idd=?',
            130013:'select * from gr_uri_out where ido=?',
            130014:'select * from gr_uri_in where idd=? and ido=?',
            130015:'select * from gr_uri_out where ido=? and idd=?',
            130016:'select ido from gr_uri_in where idd=?',
            130017:'select idd from gr_uri_out where ido=?',
            130018:'select * from gr_kin_in where idd=?',
            130019:'select * from gr_kin_out where ido=?',
            130020:'select * from gr_kin_in where idd=? and ido=?',
            130021:'select * from gr_kin_out where ido=? and idd=?',
            130022:'select ido from gr_kin_in where idd=?',
            130023:'select idd from gr_kin_out where ido=?',
            131000:'insert into gr_member_in (idd,ido,type,creation_date) values (?,?,?,?)',
            131001:'insert into gr_member_out (ido,idd,type,creation_date) values (?,?,?,?)',
            131002:'insert into gr_bounded_share_in (idd,ido,type,creation_date,perm,interval_init,interval_end) values (?,?,?,?,?,?,?)',
            131003:'insert into gr_bounded_share_out (ido,idd,type,creation_date,perm,interval_init,interval_end) values (?,?,?,?,?,?,?)',
            131004:'insert into gr_uri_in (idd,ido,type,creation_date,uri) values (?,?,?,?,?)',
            131005:'insert into gr_uri_out (ido,idd,type,creation_date,uri) values (?,?,?,?,?)',
            131006:'insert into gr_kin_in (idd,ido,type,creation_date,params) values (?,?,?,?,?)',
            131007:'insert into gr_kin_out (ido,idd,type,creation_date,params) values (?,?,?,?,?)',
            132000:'delete from gr_member_in where idd=? and ido=?',
            132001:'delete from gr_member_out where ido=? and idd=?',
            132002:'delete from gr_bounded_share_in where idd=? and ido=?',
            132003:'delete from gr_bounded_share_out where ido=? and idd=?',
            132004:'delete from gr_uri_in where idd=? and ido=?',
            132005:'delete from gr_uri_out where ido=? and idd=?',
            132006:'delete from gr_kin_in where idd=? and ido=?',
            132007:'delete from gr_kin_out where ido=? and idd=?',
           }

# selects

S_A_GRMEMBERIN_B_IDD=130000
S_A_GRMEMBEROUT_B_IDO=130001
S_A_GRMEMBERIN_B_IDD_IDO=130002
S_A_GRMEMBEROUT_B_IDO_IDD=130003
S_A_GRBOUNDEDSHAREIN_B_IDD=130004
S_A_GRBOUNDEDSHAREOUT_B_IDO=130005
S_A_GRBOUNDEDSHAREIN_B_IDD_IDO=130006
S_A_GRBOUNDEDSHAREOUT_B_IDO_IDD=130007
S_IDO_GRMEMBERIN_B_IDD=130008
S_IDD_GRMEMBEROUT_B_IDO=130009
S_IDO_GRBOUNDEDSHAREIN_B_IDD=130010
S_IDD_GRBOUNDEDSHAREOUT_B_IDO=130011
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

I_A_GRMEMBERIN=131000
I_A_GRMEMBEROUT=131001
I_A_GRBOUNDEDSHAREIN=131002
I_A_GRBOUNDEDSHAREOUT=131003
I_A_GRURIIN=131004
I_A_GRURIOUT=131005
I_A_GRKININ=131006
I_A_GRKINOUT=131007

# Deletes

D_A_GRMEMBERIN_B_IDD_IDO=132000
D_A_GRMEMBEROUT_B_IDO_IDD=132001
D_A_GRBOUNDEDSHAREIN_B_IDD_IDO=132002
D_A_GRBOUNDEDSHAREOUT_B_IDO_IDD=132003
D_A_GRURIIN_B_IDD_IDO=132004
D_A_GRURIOUT_B_IDO_IDD=132005
D_A_GRKININ_B_IDD_IDO=132006
D_A_GRKINOUT_B_IDO_IDD=132007

