'''

 This file contains the statements to execute to populate segment tables

 '''

STATEMENTS=[
# Segment Quote Population

# Free PLAN
    
    "insert into mst_user_segment (sid,description) values (0,'Free plan')",

    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_daily_datasource_occupation',100000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_daily_user_datasources_occupation',100000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_daily_user_data_post_counter',5000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_agent_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_agent_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_circle_total_members',256)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_datasource_total_datapoints',1000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_agents',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_circles',64)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_dashboards',1024)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_snapshots',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_widgets',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (0,'quo_user_total_occupation',100000000)",

# PERSONAL PLAN

    "insert into mst_user_segment (sid,description) values (1,'Personal plan')",

    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_daily_datasource_occupation',1000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_daily_user_datasources_occupation',1000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_daily_user_data_post_counter',50000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_agent_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_agent_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_circle_total_members',256)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_datasource_total_datapoints',1000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_agents',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_circles',64)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_dashboards',1024)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_snapshots',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_widgets',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (1,'quo_user_total_occupation',1000000000)",

# STARTUP PLAN

    "insert into mst_user_segment (sid,description) values (2,'Startup plan')",

    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_daily_datasource_occupation',10000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_daily_user_datasources_occupation',10000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_daily_user_data_post_counter',600000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_agent_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_agent_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_circle_total_members',256)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_datasource_total_datapoints',1000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_agents',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_circles',64)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_dashboards',1024)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_snapshots',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_widgets',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (2,'quo_user_total_occupation',10000000000)",

# BUSINESS PLAN

    "insert into mst_user_segment (sid,description) values (3,'Business plan')",

    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_daily_datasource_occupation',100000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_daily_user_datasources_occupation',100000000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_daily_user_data_post_counter',10000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_agent_total_datapoints',10000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_agent_total_datasources',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_circle_total_members',256)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_datasource_total_datapoints',1000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_agents',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_circles',64)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_dashboards',1024)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_datapoints',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_datasources',100000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_snapshots',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_widgets',1000000)",
    "insert into prm_user_segment_quo (sid,quote,value) values (3,'quo_user_total_occupation',100000000000)",


# ALLOWED SEGMENT TRANSITIONS

    "insert into prm_user_segment_allowed_transitions (sid,sids) values (0,{1,2,3});",
    "insert into prm_user_segment_allowed_transitions (sid,sids) values (1,{2,3,0});",
    "insert into prm_user_segment_allowed_transitions (sid,sids) values (2,{3,0,1});",
    "insert into prm_user_segment_allowed_transitions (sid,sids) values (3,{0,1,2});",

# SEGMENT FARES

    "insert into prm_user_segment_fare (sid, amount, currency, frequency) values (0,0,null,null);",
    "insert into prm_user_segment_fare (sid, amount, currency, frequency) values (1,10,'USD','m');",
    "insert into prm_user_segment_fare (sid, amount, currency, frequency) values (2,99,'USD','m');",
    "insert into prm_user_segment_fare (sid, amount, currency, frequency) values (3,995,'USD','m');",

]

