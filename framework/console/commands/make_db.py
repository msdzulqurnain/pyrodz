import os

from dotenv import load_dotenv

from framework.console.style import Style

load_dotenv()


class MakeDb:
    def handle(self, *args):
        connection = os.getenv("DB_CONNECTION", "sqlite")
        database = os.getenv("DB_DATABASE")

        print()
        print(Style.info(f"Driver: {connection}"))

        handlers = {
            "sqlite": self._init_sqlite,
            "mysql": self._init_mysql,
            "pgsql": self._init_pgsql,
        }

        handler = handlers.get(connection)
        if not handler:
            print(Style.error(f"Unknown driver: {connection}"))
            return

        handler(database)

    def _init_sqlite(self, database):
        if not database or "/" not in database:
            database = "storage/database.sqlite"

        if os.path.exists(database):
            print(Style.warn("Database file already exists, skipping creation."))
            return

        os.makedirs(os.path.dirname(database), exist_ok=True)

        try:
            import sqlite3
            conn = sqlite3.connect(database)
            conn.close()
            print(Style.success(f"Database created: {database}"))
        except Exception as e:
            print(Style.error(f"Failed to create database: {e}"))

    def _init_mysql(self, database):
        try:
            import pymysql
        except ImportError:
            print(Style.error("MySQL driver requires pymysql. Install: pip install pymysql"))
            return

        host = os.getenv("DB_HOST", "127.0.0.1")
        port = int(os.getenv("DB_PORT", "3306"))
        user = os.getenv("DB_USERNAME", "root")
        password = os.getenv("DB_PASSWORD", "")

        if not database:
            print(Style.error("DB_DATABASE is not set."))
            return

        try:
            conn = pymysql.connect(
                host=host, port=port, user=user, password=password,
            )
            with conn.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{database}` "
                    f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
            conn.close()
            print(Style.success(f"Database '{database}' created (or already exists)."))
        except Exception as e:
            print(Style.error(f"Failed to create MySQL database: {e}"))

    def _init_pgsql(self, database):
        try:
            import psycopg2
        except ImportError:
            print(Style.error("PostgreSQL driver requires psycopg2. Install: pip install psycopg2-binary"))
            return

        host = os.getenv("DB_HOST", "127.0.0.1")
        port = int(os.getenv("DB_PORT", "5432"))
        user = os.getenv("DB_USERNAME", "postgres")
        password = os.getenv("DB_PASSWORD", "")

        if not database:
            print(Style.error("DB_DATABASE is not set."))
            return

        try:
            conn = psycopg2.connect(
                host=host, port=port, user=user, password=password,
                dbname="postgres",
            )
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT 1 FROM pg_database WHERE datname = %s", [database]
            )
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f'CREATE DATABASE "{database}"')
                print(Style.success(f"Database '{database}' created."))
            else:
                print(Style.warn(f"Database '{database}' already exists."))

            cursor.close()
            conn.close()
        except Exception as e:
            print(Style.error(f"Failed to create PostgreSQL database: {e}"))


