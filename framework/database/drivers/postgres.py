try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

from .base import BaseDriver
from ..grammars.postgres import PostgresGrammar


class PostgresDriver(BaseDriver):
    def __init__(self):
        self._connection = None
        self._last_id = None

    def connect(self, config):
        if not HAS_PSYCOPG2:
            raise ImportError(
                "PostgreSQL driver requires psycopg2. "
                "Install: pip install psycopg2-binary"
            )

        self._connection = psycopg2.connect(
            host=config.get("host", "127.0.0.1"),
            port=int(config.get("port", 5432)),
            dbname=config.get("database"),
            user=config.get("username", "postgres"),
            password=config.get("password", ""),
        )

    def query(self, sql, params=None):
        cursor = self._connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        )
        cursor.execute(sql, params or [])
        return [dict(row) for row in cursor.fetchall()]

    def execute(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params or [])

        if "RETURNING" in sql.upper():
            row = cursor.fetchone()
            self._last_id = row[0] if row else None
        else:
            self._last_id = None

        self._connection.commit()
        return cursor.rowcount

    def last_insert_id(self):
        return self._last_id

    def grammar(self, query):
        return PostgresGrammar(query)

    def close(self):
        if self._connection:
            self._connection.close()
