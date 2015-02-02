'''
This file contains the statements to operate with widget tables
Statements range (90000-99999)
'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={90000:'select * from mst_widget where wid=?',
            90001:'select * from mst_widget where uid=?',
            90002:'select * from mst_widget_ds where wid=?',
            90003:'select * from mst_widget_dp where wid=?',
            90004:'select count(*) from mst_widget where uid=?',
            90005:'select * from mst_widget_ds where did=?',
            90006:'select * from mst_widget_dp where pid=?',
            90007:'select wid from mst_widget where uid=?',
            91000:'insert into mst_widget (wid,uid,type) values (?,?,?)',
            91001:'insert into mst_widget_ds (wid,uid,creation_date,did) values (?,?,?,?)',
            91002:'insert into mst_widget_dp (wid,uid,creation_date,pid) values (?,?,?,?)',
            92000:'delete from mst_widget where wid=?',
            92001:'delete from mst_widget where uid=?',
            92002:'delete from mst_widget_ds where wid=?',
            92003:'delete from mst_widget_ds where uid=?',
            92004:'delete from mst_widget_dp where wid=?',
            92005:'delete from mst_widget_dp where uid=?'
           }

# selects

S_A_MSTWIDGET_B_WID=90000
S_A_MSTWIDGET_B_UID=90001
S_A_MSTWIDGETDS_B_WID=90002
S_A_MSTWIDGETDP_B_WID=90003
S_COUNT_MSTWIDGET_B_UID=90004
S_A_MSTWIDGETDS_B_DID=90005
S_A_MSTWIDGETDP_B_PID=90006
S_WID_MSTWIDGET_B_UID=90007

# Inserts

I_A_MSTWIDGET=91000
I_A_MSTWIDGETDS=91001
I_A_MSTWIDGETDP=91002

# Deletes

D_A_MSTWIDGET_B_WID=92000
D_A_MSTWIDGET_B_UID=92001
D_A_MSTWIDGETDS_B_WID=92002
D_A_MSTWIDGETDS_B_UID=92003
D_A_MSTWIDGETDP_B_WID=92004
D_A_MSTWIDGETDP_B_UID=92005

