try:
    import pymysql
    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

from .base import BaseDriver
from ..grammars.mysql import MysqlGrammar


class MysqlDriver(BaseDriver):
    def __init__(self):
        self._connection = None

    def connect(self, config):
        if not HAS_PYMYSQL:
            raise ImportError(
                "MySQL driver requires pymysql. "
                "Install: pip install pymysql"
            )

        self._connection = pymysql.connect(
            host=config.get("host", "127.0.0.1"),
            port=int(config.get("port", 3306)),
            database=config.get("database"),
            user=config.get("username", "root"),
            password=config.get("password", ""),
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def query(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params or [])
        return cursor.fetchall()

    def execute(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params or [])
        self._connection.commit()
        return cursor.rowcount

    def last_insert_id(self):
        cursor = self._connection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID()")
        row = cursor.fetchone()
        return list(row.values())[0] if row else 0

    def grammar(self, query):
        return MysqlGrammar(query)

    def close(self):
        if self._connection:
            self._connection.close()
