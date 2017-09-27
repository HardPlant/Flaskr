from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///./tmp/flaskr.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
def init_db():
    #import myapp.model
    Base.metadata.create_all(bind=engine)

def test_init_db():
    engine = create_engine('sqlite:///:memory:', convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
    Base.query = db_session.query_property()

    Base.metadata.create_all(bind=engine)
