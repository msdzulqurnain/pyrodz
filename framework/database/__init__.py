from .manager import ConnectionManager
from .query import QueryBuilder
from .model import Model
from .mongo import mongo


class DB:
    @staticmethod
    def table(name):
        driver = ConnectionManager().driver()
        return QueryBuilder(driver, name)


class Schema:
    @staticmethod
    def create(table, columns):
        from .schema import SchemaBuilder
        SchemaBuilder(ConnectionManager().driver()).create(table, columns)

    @staticmethod
    def table(table, callback):
        from .schema import SchemaBuilder
        SchemaBuilder(ConnectionManager().driver()).table(table, callback)

    @staticmethod
    def drop_column(table, column):
        from .schema import SchemaBuilder
        SchemaBuilder(ConnectionManager().driver()).drop_column(table, column)

    @staticmethod
    def rename_column(table, from_col, to_col):
        from .schema import SchemaBuilder
        SchemaBuilder(ConnectionManager().driver()).rename_column(table, from_col, to_col)

    @staticmethod
    def drop(table):
        from .schema import SchemaBuilder
        SchemaBuilder(ConnectionManager().driver()).drop(table)

    @staticmethod
    def has_table(table):
        from .schema import SchemaBuilder
        return SchemaBuilder(ConnectionManager().driver()).has_table(table)

    @staticmethod
    def increments(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.increments(name)

    @staticmethod
    def string(name, length=255):
        from .schema import SchemaBuilder
        return SchemaBuilder.string(name, length)

    @staticmethod
    def integer(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.integer(name)

    @staticmethod
    def big_integer(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.big_integer(name)

    @staticmethod
    def text(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.text(name)

    @staticmethod
    def boolean(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.boolean(name)

    @staticmethod
    def datetime(name):
        from .schema import SchemaBuilder
        return SchemaBuilder.datetime(name)

    @staticmethod
    def timestamps():
        from .schema import SchemaBuilder
        return SchemaBuilder.timestamps()


__all__ = [
    "DB",
    "Schema",
    "Model",
    "QueryBuilder",
    "mongo",
]
