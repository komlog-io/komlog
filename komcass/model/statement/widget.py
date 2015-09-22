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
            90008:'select * from mst_widget_histogram where wid=?',
            90009:'select wid from mst_widget_histogram where datapoints contains ?',
            90010:'select * from mst_widget_linegraph where wid=?',
            90011:'select wid from mst_widget_linegraph where datapoints contains ?',
            90012:'select * from mst_widget_table where wid=?',
            90013:'select wid from mst_widget_table where datapoints contains ?',
            90014:'select * from mst_widget_multidp where wid=?',
            90015:'select wid from mst_widget_multidp where datapoints contains ?',
            91000:'insert into mst_widget (wid,uid,type) values (?,?,?)',
            91001:'insert into mst_widget_ds (wid,uid,widgetname,creation_date,did) values (?,?,?,?,?)',
            91002:'insert into mst_widget_dp (wid,uid,widgetname,creation_date,pid) values (?,?,?,?,?)',
            91003:'insert into mst_widget_histogram (wid,uid,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?)',
            91004:'insert into mst_widget_linegraph (wid,uid,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?)',
            91005:'insert into mst_widget_table (wid,uid,widgetname,creation_date,datapoints,colors) values (?,?,?,?,?,?)',
            91006:'insert into mst_widget_multidp (wid,uid,widgetname,creation_date,active_visualization,datapoints) values (?,?,?,?,?,?)',
            92000:'delete from mst_widget where wid=?',
            92001:'delete from mst_widget where uid=?',
            92002:'delete from mst_widget_ds where wid=?',
            92003:'delete from mst_widget_ds where uid=?',
            92004:'delete from mst_widget_dp where wid=?',
            92005:'delete from mst_widget_dp where uid=?',
            92006:'delete from mst_widget_histogram where wid=?',
            92007:'delete datapoints[?] from mst_widget_histogram where wid=?',
            92008:'delete colors[?] from mst_widget_histogram where wid=?',
            92009:'delete from mst_widget_linegraph where wid=?',
            92010:'delete datapoints[?] from mst_widget_linegraph where wid=?',
            92011:'delete colors[?] from mst_widget_linegraph where wid=?',
            92012:'delete from mst_widget_table where wid=?',
            92013:'delete datapoints[?] from mst_widget_table where wid=?',
            92014:'delete colors[?] from mst_widget_table where wid=?',
            92015:'delete from mst_widget_multidp where wid=?',
            92016:'delete datapoints[?] from mst_widget_multidp where wid=?',
            93001:'update mst_widget_histogram set datapoints=? where wid=?',
            93002:'update mst_widget_histogram set colors[?]=? where wid=?',
            93003:'update mst_widget_linegraph set datapoints=? where wid=?',
            93004:'update mst_widget_linegraph set colors[?]=? where wid=?',
            93005:'update mst_widget_table set datapoints=? where wid=?',
            93006:'update mst_widget_table set colors[?]=? where wid=?',
            93007:'update mst_widget_ds set widgetname=? where wid=?',
            93008:'update mst_widget_dp set widgetname=? where wid=?',
            93009:'update mst_widget_histogram set widgetname=? where wid=?',
            93010:'update mst_widget_linegraph set widgetname=? where wid=?',
            93011:'update mst_widget_table set widgetname=? where wid=?',
            93012:'update mst_widget_multidp set datapoints=? where wid=?',
            93013:'update mst_widget_multidp set widgetname=? where wid=?',
            93014:'update mst_widget_multidp set active_visualization=? where wid=?',
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
S_A_MSTWIDGETHISTOGRAM_B_WID=90008
S_WID_MSTWIDGETHISTOGRAM_B_PID=90009
S_A_MSTWIDGETLINEGRAPH_B_WID=90010
S_WID_MSTWIDGETLINEGRAPH_B_PID=90011
S_A_MSTWIDGETTABLE_B_WID=90012
S_WID_MSTWIDGETTABLE_B_PID=90013
S_A_MSTWIDGETMULTIDP_B_WID=90014
S_WID_MSTWIDGETMULTIDP_B_PID=90015

# Inserts

I_A_MSTWIDGET=91000
I_A_MSTWIDGETDS=91001
I_A_MSTWIDGETDP=91002
I_A_MSTWIDGETHISTOGRAM=91003
I_A_MSTWIDGETLINEGRAPH=91004
I_A_MSTWIDGETTABLE=91005
I_A_MSTWIDGETMULTIDP=91006

# Deletes

D_A_MSTWIDGET_B_WID=92000
D_A_MSTWIDGET_B_UID=92001
D_A_MSTWIDGETDS_B_WID=92002
D_A_MSTWIDGETDS_B_UID=92003
D_A_MSTWIDGETDP_B_WID=92004
D_A_MSTWIDGETDP_B_UID=92005
D_A_MSTWIDGETHISTOGRAM_B_WID=92006
D_DATAPOINT_MSTWIDGETHISTOGRAM_B_PID_WID=92007
D_COLOR_MSTWIDGETHISTOGRAM_B_PID_WID=92008
D_A_MSTWIDGETLINEGRAPH_B_WID=92009
D_DATAPOINT_MSTWIDGETLINEGRAPH_B_PID_WID=92010
D_COLOR_MSTWIDGETLINEGRAPH_B_PID_WID=92011
D_A_MSTWIDGETTABLE_B_WID=92012
D_DATAPOINT_MSTWIDGETTABLE_B_PID_WID=92013
D_COLOR_MSTWIDGETTABLE_B_PID_WID=92014
D_A_MSTWIDGETMULTIDP_B_WID=92015
D_PID_MSTWIDGETMULTIDP_B_PID_WID=92016

# Updates

U_DATAPOINTS_MSTWIDGETHISTOGRAM_B_WID=93001
U_COLOR_MSTWIDGETHISTOGRAM_B_WID=93002
U_DATAPOINTS_MSTWIDGETLINEGRAPH_B_WID=93003
U_COLOR_MSTWIDGETLINEGRAPH_B_WID=93004
U_DATAPOINTS_MSTWIDGETTABLE_B_WID=93005
U_COLOR_MSTWIDGETTABLE_B_WID=93006
U_WIDGETNAME_MSTWIDGETDATASOURCE_B_WID=93007
U_WIDGETNAME_MSTWIDGETDATAPOINT_B_WID=93008
U_WIDGETNAME_MSTWIDGETHISTOGRAM_B_WID=93009
U_WIDGETNAME_MSTWIDGETLINEGRAPH_B_WID=93010
U_WIDGETNAME_MSTWIDGETTABLE_B_WID=93011
U_PIDS_MSTWIDGETMULTIDP_B_WID=93012
U_WIDGETNAME_MSTWIDGETMULTIDP_B_WID=93013
U_ACTIVEVISUALIZATION_MSTWIDGETMULTIDP_B_WID=93014


