from komfig import logger
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
from komcass.model.schema import snapshot

from komcass import connection

def create_keyspace(session, keyspace, replication):
    logger.logger.debug('Creating keyspace: '+str(keyspace)+' with replication: '+str(replication))
    try:
        session.execute('''create keyspace '''+keyspace\
        +''' WITH REPLICATION = '''+str(replication)+''';''')
    except AlreadyExists as e:
        logger.logger.debug('Keyspace Already exists, aborting')
        return False
    else:
        logger.logger.debug('keyspace created successfully')
        return True

def create_schema(session):
    logger.logger.debug('Creating database schema')
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
        for obj in snapshot.OBJECTS:
            query=getattr(snapshot,obj)
            session.execute(query)
    except Exception as e:
        logger.logger.debug('Error creating schema '+str(e))
        logger.logger.debug(query)
        return False
    else:
        logger.logger.debug('Schema created successfully')
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
        return True
    else:
        return False

def drop_database(ip_list, keyspace):
    Session=connection.Session(ip_list)
    logger.logger.debug('dropping  keyspace: '+str(keyspace))
    try:
        Session.session.execute('''drop keyspace '''+keyspace)
    except Exception as e:
        logger.logger.debug('Exception in drop keyspace: '+str(e))
        return False
    else:
        logger.logger.debug('keyspace deleted successfully')
        return True

