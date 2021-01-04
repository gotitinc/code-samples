import logging
import os
import sys

import pytest
from alembic.command import upgrade
from alembic.config import Config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

_app = Flask(__name__)
db = SQLAlchemy(app=_app)

if os.getenv('ENVIRONMENT') != 'test':
    print('Tests should be run with "ENVIRONMENT=test"')
    sys.exit(1)

ALEMBIC_CONFIG = '/path/to/file/alembic.ini'


def pytest_addoption(parser):
    parser.addoption(
        '--log', action='store', default='WARNING', help='set logging level'
    )


def recreate_database():
    """ Run the alembic migrations """
    db.reflect()
    db.drop_all()
    config = Config(ALEMBIC_CONFIG)
    upgrade(config, 'heads')


def configure_logging():
    # loglevel = pytest.config.getoption("--log")
    loglevel = 'WARNING'
    numeric_level = getattr(
        logging,
        loglevel.upper(),
        None
    )
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logging.getLogger().setLevel(numeric_level)


@pytest.fixture(scope='session', autouse=True)
def app(request):
    ctx = _app.test_request_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='session', autouse=True)
def database(request, app):
    Migrate(_app, db)
    recreate_database()


@pytest.fixture(scope='function', autouse=True)
def session(request, monkeypatch):
    """ Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    monkeypatch.setattr(db, 'get_engine', lambda *args: connection)

    db.session = session

    def teardown():
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    return session
