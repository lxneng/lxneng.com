from zope.sqlalchemy import ZopeTransactionExtension
from lxneng.models import meta
from sqlalchemy import orm


def init_sqlalchemy(engine):
    """Initialise the SQLAlchemy models. This must be called before using
    using any of the SQLAlchemy managed the tables or classes in the model."""

    sm = orm.sessionmaker(bind=engine, extension=ZopeTransactionExtension())
    meta.Session = orm.scoped_session(sm)
    meta.metadata.bind = engine