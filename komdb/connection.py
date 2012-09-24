from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#engine = create_engine('sqlite:///:memory:',echo=True)
engine = create_engine('postgresql://komlog:temporal@be1/komlog')


Session = sessionmaker()
Session.configure(bind=engine)

