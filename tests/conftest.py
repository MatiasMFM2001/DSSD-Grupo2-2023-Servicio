from src.core.database import database
from tests import app

def pytest_sessionstart(session):
    with app.app_context():
        database.reset_db()
        database.initializate_prod_db()

def pytest_assertrepr_compare(config, op, left, right):
    if op in ('==', '!=', 'in', 'not in'):
        return ["{0} {1} {2}".format(left, op, right)]
    