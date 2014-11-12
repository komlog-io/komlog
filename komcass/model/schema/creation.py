from cassandra import AlreadyExists
from komcass.model.schema.keyspace import KEYSPACE, REPLICATION
from komcass.model.schema import user
from komcass.model.schema import agent
from komcass.model.schema import datasource
from komcass.model.schema import datapoint
from komcass.model.schema import widget
from komcass.model.schema import dashboard
from komcass.model.schema import quote
from komcass.model.schema import permission
from komcass.model.schema import interface
from komcass.model.schema import segment

from komcass import connection

def create_keyspace(session, keyspace, replication):
    try:
        session.execute('''create keyspace '''+keyspace\
        +''' WITH REPLICATION = '''+str(replication)+''';''')
    except AlreadyExists as e:
        print('Keyspace Already exists, aborting')
        return False
    else:
        return True

def create_schema(session):
    query=None
    try:
        for obj in user.OBJECTS:
            query=getattr(user,obj)
            session.execute(query)
        for obj in agent.OBJECTS:
            query=getattr(agent,obj)
            session.execute(query)
        for obj in datasource.OBJECTS:
            query=getattr(datasource,obj)
            session.execute(query)
        for obj in datapoint.OBJECTS:
            query=getattr(datapoint,obj)
            session.execute(query)
        for obj in widget.OBJECTS:
            query=getattr(widget,obj)
            session.execute(query)
        for obj in dashboard.OBJECTS:
            query=getattr(dashboard,obj)
            session.execute(query)
        for obj in quote.OBJECTS:
            query=getattr(quote,obj)
            session.execute(query)
        for obj in permission.OBJECTS:
            query=getattr(permission,obj)
            session.execute(query)
        for obj in interface.OBJECTS:
            query=getattr(interface,obj)
            session.execute(query)
        for obj in segment.OBJECTS:
            query=getattr(segment,obj)
            session.execute(query)
    except Exception as e:
        print('Error creating schema '+str(e))
        print(query)
        return False
    else:
        print('Schema created successfully')
        return True

def create_database(ip_list, keyspace=None, replication=None):
    Session=connection.Session(ip_list)
    if not keyspace:
        keyspace=KEYSPACE
    if not replication:
        replication=REPLICATION
    if create_keyspace(Session.session, keyspace, replication):
        Session=connection.Session(ip_list,keyspace)
        create_schema(Session.session)

