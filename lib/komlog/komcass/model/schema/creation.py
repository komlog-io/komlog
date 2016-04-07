from komlog.komfig import logging
from cassandra import AlreadyExists
from komlog.komcass.model.schema.keyspace import KEYSPACE, REPLICATION
from komlog.komcass.model.schema import user
from komlog.komcass.model.schema import agent
from komlog.komcass.model.schema import datasource
from komlog.komcass.model.schema import datapoint
from komlog.komcass.model.schema import widget
from komlog.komcass.model.schema import dashboard
from komlog.komcass.model.schema import quote
from komlog.komcass.model.schema import permission
from komlog.komcass.model.schema import interface
from komlog.komcass.model.schema import segment
from komlog.komcass.model.schema import snapshot
from komlog.komcass.model.schema import graph
from komlog.komcass.model.schema import circle
from komlog.komcass.model.schema import events
from komlog.komcass.model.schema import ticket

from komlog.komcass import connection

def create_keyspace(session, keyspace, replication):
    logging.logger.debug('Creating keyspace: '+str(keyspace)+' with replication: '+str(replication))
    try:
        session.execute('''create keyspace '''+keyspace\
        +''' WITH REPLICATION = '''+str(replication)+''';''')
    except AlreadyExists as e:
        logging.logger.debug('Keyspace Already exists, aborting')
        return False
    else:
        logging.logger.debug('keyspace created successfully')
        return True

def create_schema(session):
    logging.logger.debug('Creating database schema')
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
        for obj in graph.OBJECTS:
            query=getattr(graph,obj)
            session.execute(query)
        for obj in circle.OBJECTS:
            query=getattr(circle,obj)
            session.execute(query)
        for obj in events.OBJECTS:
            query=getattr(events,obj)
            session.execute(query)
        for obj in ticket.OBJECTS:
            query=getattr(ticket,obj)
            session.execute(query)
    except Exception as e:
        logging.logger.debug('Error creating schema '+str(e))
        logging.logger.debug(query)
        return False
    else:
        logging.logger.debug('Schema created successfully')
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
    logging.logger.debug('dropping keyspace: '+str(keyspace))
    try:
        Session.session.execute('drop keyspace '+keyspace, timeout=None)
    except Exception as e:
        logging.logger.debug('Exception dropping keyspace')
        logging.logger.debug(str(e))
        logging.logger.debug(str(type(e)))
        return False
    else:
        logging.logger.debug('keyspace deleted successfully')
        return True

