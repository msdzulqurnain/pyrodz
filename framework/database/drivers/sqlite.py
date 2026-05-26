import sqlite3

from .base import BaseDriver
from ..grammars.sqlite import SqliteGrammar


class SqliteDriver(BaseDriver):
    def __init__(self):
        self._connection = None

    def connect(self, config):
        database = config.get("database")
        if not database or "/" not in database:
            database = "storage/database.sqlite"
        self._connection = sqlite3.connect(database)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA foreign_keys=ON")

    def query(self, sql, params=None):
        cursor = self._connection.execute(sql, params or [])
        return [dict(row) for row in cursor.fetchall()]

    def execute(self, sql, params=None):
        cursor = self._connection.execute(sql, params or [])
        self._connection.commit()
        return cursor.rowcount

    def last_insert_id(self):
        return self._connection.execute(
            "SELECT last_insert_rowid()"
        ).fetchone()[0]

    def grammar(self, query):
        return SqliteGrammar(query)

    def close(self):
        if self._connection:
            self._connection.close()
