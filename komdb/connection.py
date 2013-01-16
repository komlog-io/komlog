from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connection(object):
    def __init__(self, db_uri):
        self.uri = db_uri
        self.engine = create_engine(self.uri)
        self._Session = sessionmaker()
        self._Session.configure(bind=self.engine)
        self.session = self._Session()
    
    def add(self, obj):
        self.session().add(obj)
    
    def commit(self):
        self.session().commit()
        