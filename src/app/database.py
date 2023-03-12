import os

import psycopg2

from .database_utils import CRUD

class Connector(CRUD):
    def __init__(self, **kwargs):
        self._conn = psycopg2.connect(host=os.getenv('DB_HOST'),
                             user=os.getenv('DB_USER'),
                             password=os.getenv('DB_PASS', None),
                             database=os.getenv('DB_SCHEMA', None),
                             port=os.getenv('DB_PORT', 5432))
