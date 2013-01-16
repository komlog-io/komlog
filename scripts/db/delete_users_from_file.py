#!/usr/bin/env python

import sys
from komdb import api as dbapi
from komdb import connection as dbcon
from komdb import exceptions

sql_uri=sys.argv[1]
file=sys.argv[2]


connection = dbcon.Connection(sql_uri)
fd = open(file)
for line in fd:
    user = line.split('\n')[0]
    try:
        dbapi.delete_user(username=user,session=connection.session)
        print 'user '+line+' deleted'
    except exceptions.NotFoundUserError:
        print 'user not found: '+user
        user

fd.close
connection = None

