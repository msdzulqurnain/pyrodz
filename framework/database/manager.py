import os

from dotenv import load_dotenv

load_dotenv()

from .drivers.sqlite import SqliteDriver
from .drivers.mysql import MysqlDriver
from .drivers.postgres import PostgresDriver
DRIVERS = {
    "sqlite": SqliteDriver,
    "mysql": MysqlDriver,
    "pgsql": PostgresDriver,
}


class ConnectionManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._driver = None
        return cls._instance

    def driver(self):
        if self._driver is None:
            connection = os.getenv("DB_CONNECTION", "sqlite")
            driver_class = DRIVERS.get(connection)

            if not driver_class:
                raise ValueError(
                    f"Unsupported database driver: {connection}"
                )

            env_keys = {
                "database": "DB_DATABASE",
                "host": "DB_HOST",
                "port": "DB_PORT",
                "username": "DB_USERNAME",
                "password": "DB_PASSWORD",
            }
            config = {}
            for key, env_key in env_keys.items():
                value = os.getenv(env_key)
                if value is not None:
                    config[key] = value

            self._driver = driver_class()
            self._driver.connect(config)

        return self._driver
