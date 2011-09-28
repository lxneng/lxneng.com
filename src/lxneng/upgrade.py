from s4u.upgrade import upgrade_context
from s4u.upgrade import upgrade_step
from sqlalchemy import create_engine
from s4u.sqlalchemy import meta
from s4u.sqlalchemy import init_sqlalchemy
import logging

log = logging.getLogger(__name__)


@upgrade_context('sql', [('--db-uri',
               {'type': str, 'required': True, 'dest': 'dburi'})])
def setup_sqlalchemy(options):
    engine = create_engine(options.dburi)
    init_sqlalchemy(engine) 
    log.info('setup_sqlalchemy')
    return {'sql-engine': engine}

@upgrade_step(require=['sql'])
def add_missing_tables(environment):
    engine = environment['sql-engine']
    log.info('add_missing_tables')
    meta.metadata.create_all(engine)
