from contextlib import contextmanager
from sqlalchemy.pool import NullPool
from sqlalchemy import orm, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from libutils.base.db import connection_string


class SqlAlchemyConnection:
    """SQLAlchemy database connection"""

    engine = create_engine(connection_string, echo=False,
                           pool_recycle=280, poolclass=NullPool)
    meta = MetaData(bind=engine)
    session = orm.scoped_session(orm.sessionmaker(bind=engine))
    base = declarative_base()

    @staticmethod
    @contextmanager
    def session_scope():
        """Provide a transactional scope around a series of operations."""

        session = SqlAlchemyConnection.session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class ResultSet:

    def __init__(self, result):
        self._cursor = result

    def __next__(self):
        return next(self._cursor)
