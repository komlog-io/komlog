'''
This file contains the multiple types a user, agent or datasource can be
and params each type accepts, translations, etc

creation date: 2013/04/07
author: jcazor
'''

DS_STR2INT={'script':'0'}
DS_INT2STR={'0':'script'}


DSPARAMS_DB2WEB={DS_STR2INT['script']:[('script_name','script_name'),\
                    ('min','minute'),\
                    ('hour','hour'),\
                    ('dow','day_of_week'),\
                    ('month','month'),\
                    ('dom','day_of_month')]}

DSPARAMS_WEB2DB={DS_STR2INT['script']:[('script_name','script_name'),\
                    ('minute','min'),\
                    ('hour','hour'),\
                    ('day_of_week','dow'),\
                    ('month','month'),\
                    ('day_of_month','dom')]}


DS_WIDGET='ds'
