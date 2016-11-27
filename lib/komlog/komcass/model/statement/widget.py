'''
This file contains the statements to operate with widget tables
Statements range (90000-99999)

By default we numerate queries this way:

- 50% for selects (in this case from 90000 to 94999)
- 20% for inserts
- 20% for deletes
- 10% for updates

Each table has reserved 100 consecutive numbers of each category

'''

def get_statement(num):
    try:
        return STATEMENTS[num]
    except KeyError:
        return None


STATEMENTS={
    90000:'select wid,uid,type,creation_date,widgetname from mst_widget where wid=?',
    90001:'select wid,uid,type,creation_date,widgetname from mst_widget where uid=?',
    90002:'select count(*) from mst_widget where uid=?',
    90003:'select wid from mst_widget where uid=?',
    90100:'select wid,did from mst_widget_ds where wid=?',
    90101:'select wid,did from mst_widget_ds where did=?',
    90200:'select wid,pid from mst_widget_dp where wid=?',
    90201:'select wid,pid from mst_widget_dp where pid=?',
    90300:'select wid,datapoints,colors from mst_widget_histogram where wid=?',
    90301:'select wid from mst_widget_histogram where datapoints contains ?',
    90400:'select wid,datapoints,colors from mst_widget_linegraph where wid=?',
    90401:'select wid from mst_widget_linegraph where datapoints contains ?',
    90500:'select wid,datapoints,colors from mst_widget_table where wid=?',
    90501:'select wid from mst_widget_table where datapoints contains ?',
    90600:'select wid,active_visualization,datapoints from mst_widget_multidp where wid=?',
    90601:'select wid from mst_widget_multidp where datapoints contains ?',
    95000:'insert into mst_widget (wid,uid,type,creation_date,widgetname) values (?,?,?,?,?)',
    95001:'insert into mst_widget (wid,uid,type,creation_date,widgetname) values (?,?,?,?,?) if not exists',
    95100:'insert into mst_widget_ds (wid,did) values (?,?)',
    95200:'insert into mst_widget_dp (wid,pid) values (?,?)',
    95300:'insert into mst_widget_histogram (wid,datapoints,colors) values (?,?,?)',
    95400:'insert into mst_widget_linegraph (wid,datapoints,colors) values (?,?,?)',
    95500:'insert into mst_widget_table (wid,datapoints,colors) values (?,?,?)',
    95600:'insert into mst_widget_multidp (wid,active_visualization,datapoints) values (?,?,?)',
    97000:'delete from mst_widget where wid=?',
    97100:'delete from mst_widget_ds where wid=?',
    97200:'delete from mst_widget_dp where wid=?',
    97300:'delete from mst_widget_histogram where wid=?',
    97301:'delete datapoints[?] from mst_widget_histogram where wid=?',
    97302:'delete colors[?] from mst_widget_histogram where wid=?',
    97400:'delete from mst_widget_linegraph where wid=?',
    97401:'delete datapoints[?] from mst_widget_linegraph where wid=?',
    97402:'delete colors[?] from mst_widget_linegraph where wid=?',
    97500:'delete from mst_widget_table where wid=?',
    97501:'delete datapoints[?] from mst_widget_table where wid=?',
    97502:'delete colors[?] from mst_widget_table where wid=?',
    97600:'delete from mst_widget_multidp where wid=?',
    97601:'delete datapoints[?] from mst_widget_multidp where wid=?',
    99000:'update mst_widget set widgetname=? where wid=?',
    99300:'update mst_widget_histogram set datapoints=? where wid=?',
    99301:'update mst_widget_histogram set colors[?]=? where wid=?',
    99400:'update mst_widget_linegraph set datapoints=? where wid=?',
    99401:'update mst_widget_linegraph set colors[?]=? where wid=?',
    99500:'update mst_widget_table set datapoints=? where wid=?',
    99501:'update mst_widget_table set colors[?]=? where wid=?',
    99600:'update mst_widget_multidp set datapoints=? where wid=?',
    99601:'update mst_widget_multidp set active_visualization=? where wid=?',
}

# selects 90000-94999

# mst_widget

S_A_MSTWIDGET_B_WID=90000
S_A_MSTWIDGET_B_UID=90001
S_COUNT_MSTWIDGET_B_UID=90002
S_WID_MSTWIDGET_B_UID=90003

# mst_widget_ds

S_A_MSTWIDGETDS_B_WID=90100
S_A_MSTWIDGETDS_B_DID=90101

# mst_widget_dp

S_A_MSTWIDGETDP_B_WID=90200
S_A_MSTWIDGETDP_B_PID=90201

# mst_widget_histogram

S_A_MSTWIDGETHISTOGRAM_B_WID=90300
S_WID_MSTWIDGETHISTOGRAM_B_PID=90301

# mst_widget_linegraph

S_A_MSTWIDGETLINEGRAPH_B_WID=90400
S_WID_MSTWIDGETLINEGRAPH_B_PID=90401

# mst_widget_table

S_A_MSTWIDGETTABLE_B_WID=90500
S_WID_MSTWIDGETTABLE_B_PID=90501

# mst_widget_multidp

S_A_MSTWIDGETMULTIDP_B_WID=90600
S_WID_MSTWIDGETMULTIDP_B_PID=90601

# Inserts (95000-96999)

# mst_widget

I_A_MSTWIDGET=95000
I_A_MSTWIDGET_INE=95001

# mst_widget_ds

I_A_MSTWIDGETDS=95100

# mst_widget_dp

I_A_MSTWIDGETDP=95200

# mst_widget_histogram

I_A_MSTWIDGETHISTOGRAM=95300

# mst_widget_linegraph

I_A_MSTWIDGETLINEGRAPH=95400

# mst_widget_table

I_A_MSTWIDGETTABLE=95500

# mst_widget_multidp

I_A_MSTWIDGETMULTIDP=95600


# Deletes

# mst_widget

D_A_MSTWIDGET_B_WID=97000

# mst_widget_ds

D_A_MSTWIDGETDS_B_WID=97100

# mst_widget_dp

D_A_MSTWIDGETDP_B_WID=97200

# mst_widget_histogram

D_A_MSTWIDGETHISTOGRAM_B_WID=97300
D_DATAPOINT_MSTWIDGETHISTOGRAM_B_PID_WID=97301
D_COLOR_MSTWIDGETHISTOGRAM_B_PID_WID=97302

# mst_widget_linegraph

D_A_MSTWIDGETLINEGRAPH_B_WID=97400
D_DATAPOINT_MSTWIDGETLINEGRAPH_B_PID_WID=97401
D_COLOR_MSTWIDGETLINEGRAPH_B_PID_WID=97402

# mst_widget_table

D_A_MSTWIDGETTABLE_B_WID=97500
D_DATAPOINT_MSTWIDGETTABLE_B_PID_WID=97501
D_COLOR_MSTWIDGETTABLE_B_PID_WID=97502

# mst_widget_multidp

D_A_MSTWIDGETMULTIDP_B_WID=97600
D_PID_MSTWIDGETMULTIDP_B_PID_WID=97601

# Updates

# mst_widget

U_WIDGETNAME_MSTWIDGET_B_WID=99000

# mst_widget_histogram

U_DATAPOINTS_MSTWIDGETHISTOGRAM_B_WID=99300
U_COLOR_MSTWIDGETHISTOGRAM_B_WID=99301

# mst_widget_linegraph

U_DATAPOINTS_MSTWIDGETLINEGRAPH_B_WID=99400
U_COLOR_MSTWIDGETLINEGRAPH_B_WID=99401

# mst_widget_table

U_DATAPOINTS_MSTWIDGETTABLE_B_WID=99500
U_COLOR_MSTWIDGETTABLE_B_WID=99501

# mst_widget_multidp

U_PIDS_MSTWIDGETMULTIDP_B_WID=99600
U_ACTIVEVISUALIZATION_MSTWIDGETMULTIDP_B_WID=99601


