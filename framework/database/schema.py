_UNSET = object()


class Column:
    def __init__(self, name, col_type, **opts):
        self.name = name
        self.col_type = col_type
        self._nullable = opts.get("nullable", False)
        self._default = opts.get("default", _UNSET)
        self._unique = opts.get("unique", False)
        self._primary = opts.get("primary", False)

    def set_nullable(self):
        self._nullable = True
        return self

    def set_default(self, value):
        self._default = value
        return self

    def set_unique(self):
        self._unique = True
        return self

    def set_primary(self):
        self._primary = True
        return self


class SchemaBuilder:
    def __init__(self, driver):
        self._driver = driver
        self._driver_type = self._detect_driver()

    def _detect_driver(self):
        name = type(self._driver).__name__
        if "Mysql" in name:
            return "mysql"
        if "Postgres" in name:
            return "pgsql"
        return "sqlite"

    def create(self, table, columns):
        if callable(columns):
            col_list = []
            columns(col_list)
            columns = col_list
        flat = []
        for col in columns:
            if isinstance(col, list):
                flat.extend(col)
            else:
                flat.append(col)
        sql = self._build_create(table, flat)
        self._driver.execute(sql)

    def drop(self, table):
        self._driver.execute(f"DROP TABLE IF EXISTS {table}")

    def table(self, table, callback):
        columns = []
        callback(columns)
        for col in columns:
            if isinstance(col, str) and col.startswith("__drop__"):
                _, column_name = col.split("__drop__", 1)
                self._driver.execute(f"ALTER TABLE {table} DROP COLUMN {column_name}")
            elif isinstance(col, str) and col.startswith("__rename__"):
                _, from_name, to_name = col.split("__rename__", 2)
                self._driver.execute(f"ALTER TABLE {table} RENAME COLUMN {from_name} TO {to_name}")
            else:
                sql = f"ALTER TABLE {table} ADD COLUMN {col.name} {col.col_type}"
                if not col._nullable:
                    sql += " NOT NULL"
                if col._default is not _UNSET:
                    if col._default is None:
                        sql += " DEFAULT NULL"
                    elif isinstance(col._default, str):
                        sql += f" DEFAULT '{col._default}'"
                    else:
                        sql += f" DEFAULT {col._default}"
                if col._unique:
                    sql += " UNIQUE"
                self._driver.execute(sql)

    def drop_column(self, table, column):
        self._driver.execute(f"ALTER TABLE {table} DROP COLUMN {column}")

    def rename_column(self, table, from_col, to_col):
        self._driver.execute(f"ALTER TABLE {table} RENAME COLUMN {from_col} TO {to_col}")

    def has_table(self, table):
        if self._driver_type == "mysql":
            sql = (
                "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = ?"
            )
        elif self._driver_type == "pgsql":
            sql = (
                "SELECT tablename FROM pg_catalog.pg_tables "
                "WHERE tablename = ?"
            )
        else:
            sql = (
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name=?"
            )

        result = self._driver.query(sql, [table])
        return len(result) > 0

    def _build_create(self, table, columns):
        col_defs = []
        has_timestamps = False

        for col in columns:
            if col._primary and col.col_type == "INTEGER":
                if self._driver_type == "pgsql":
                    defn = f"  {col.name} SERIAL PRIMARY KEY"
                elif self._driver_type == "mysql":
                    defn = f"  {col.name} INT AUTO_INCREMENT PRIMARY KEY"
                else:
                    defn = f"  {col.name} INTEGER PRIMARY KEY AUTOINCREMENT"
            else:
                defn = f"  {col.name} {col.col_type}"

                if col._primary:
                    defn += " PRIMARY KEY"

                if not col._nullable:
                    defn += " NOT NULL"

                if col._default is not _UNSET:
                    if col._default is None:
                        defn += " DEFAULT NULL"
                    elif isinstance(col._default, str):
                        defn += f" DEFAULT '{col._default}'"
                    else:
                        defn += f" DEFAULT {col._default}"

                if col._unique:
                    defn += " UNIQUE"

            col_defs.append(defn)

            if col.name in ("created_at", "updated_at"):
                has_timestamps = True

        sql = f"CREATE TABLE {table} (\n"
        sql += ",\n".join(col_defs)
        sql += "\n)"

        return sql

    @staticmethod
    def increments(name):
        return Column(name, "INTEGER", primary=True)

    @staticmethod
    def string(name, length=255):
        return Column(name, f"VARCHAR({length})")

    @staticmethod
    def integer(name):
        return Column(name, "INTEGER")

    @staticmethod
    def big_integer(name):
        return Column(name, "BIGINT")

    @staticmethod
    def text(name):
        return Column(name, "TEXT")

    @staticmethod
    def boolean(name):
        return Column(name, "BOOLEAN")

    @staticmethod
    def datetime(name):
        return Column(name, "DATETIME")

    @staticmethod
    def timestamps():
        return [
            Column("created_at", "DATETIME", nullable=True),
            Column("updated_at", "DATETIME", nullable=True),
        ]
