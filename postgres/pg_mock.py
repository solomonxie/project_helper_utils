import testing.postgresql
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from unittest import TestCase

Base = declarative_base()
Fake_PG = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)


def simple_pg():
    pg = testing.postgresql.Postgresql()
    # connect to PostgreSQL
    print(pg.url())
    engine = create_engine(pg.url())
    pg.stop()
    return engine


def shared_pg():
    pg = Fake_PG()
    print(pg.url())
    engine = create_engine(pg.url())
    pg.stop()
    return engine


class User(Base):
    __tablename__ = 'tb_Person'
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, unique=True)


def get_fake_pg_session(pg_url):
    print(pg_url)
    engine = create_engine(pg_url)
    # Init DB
    User.__table__.create(engine)
    Base.metadata.create_all(bind=engine)
    # Session
    pg_session = sessionmaker(bind=engine, autoflush=True)()
    return pg_session


class TestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.Fake_PG = testing.postgresql.PostgresqlFactory(cache_initialized_db=True)

    @classmethod
    def tearDownClass(cls):
        cls.Fake_PG.clear_cache()

    def setUp(self):
        self.pg = self.Fake_PG()

    def tearDown(self):
        pass

    def test_case_name(self):
        pg_session = get_fake_pg_session(self.pg.url())
        self.assertIsNone(pg_session)


pg = Fake_PG()
print(pg.url())
engine = create_engine(pg.url())
User.__table__.create(engine)
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine, autoflush=True)()
session.add(User(id=1, username='Jason'))
session.commit()
results = session.query(User).all()
print(results[0].username)

Fake_PG.clear_cache()
print('[ OK ]')
