from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#engine = create_engine('sqlite:///:memory:',echo=True)
engine = create_engine('postgresql://komlog:temporal@be1/komlog')


Session = sessionmaker()
Session.configure(bind=engine)

class Connection(object):
    def __init__(self, db_uri):
        self.uri = db_uri
        self.engine = create_engine(self.uri)
        self.session = sessionmaker()
        self.session.configure(bind=self.engine)
    
    def add(self, obj):
        self.session.add(obj)
    
    def commit(self):
        self.session.commit()
        