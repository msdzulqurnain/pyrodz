import importlib.util
import os
import glob

from .manager import ConnectionManager
from .schema import SchemaBuilder


class Migration:
    def __init__(self):
        self._driver = ConnectionManager().driver()
        self._schema = SchemaBuilder(self._driver)
        self._ensure_table()

    def _ensure_table(self):
        if not self._schema.has_table("_migrations"):
            driver_type = type(self._driver).__name__

            if "Mysql" in driver_type:
                sql = (
                    "CREATE TABLE _migrations ("
                    "  id INT AUTO_INCREMENT PRIMARY KEY,"
                    "  migration VARCHAR(255) NOT NULL,"
                    "  batch INT NOT NULL"
                    ")"
                )
            elif "Postgres" in driver_type:
                sql = (
                    "CREATE TABLE _migrations ("
                    "  id SERIAL PRIMARY KEY,"
                    "  migration VARCHAR(255) NOT NULL,"
                    "  batch INT NOT NULL"
                    ")"
                )
            else:
                sql = (
                    "CREATE TABLE _migrations ("
                    "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "  migration TEXT NOT NULL,"
                    "  batch INTEGER NOT NULL"
                    ")"
                )

            self._driver.execute(sql)

    def _get_batch(self):
        result = self._driver.query("SELECT MAX(batch) as batch FROM _migrations")
        row = result[0] if result else None
        return row["batch"] or 0 if row else 0

    def _get_ran(self):
        result = self._driver.query("SELECT migration FROM _migrations")
        return {r["migration"] for r in result}

    def up(self):
        ran = self._get_ran()
        batch = self._get_batch() + 1
        files = sorted(glob.glob("app/Migrations/*.py"))

        for filepath in files:
            name = os.path.basename(filepath).replace(".py", "")

            if name.startswith("__"):
                continue

            if name in ran:
                continue

            module = self._load_module(name, filepath)

            for attr in dir(module):
                cls = getattr(module, attr)

                if isinstance(cls, type) and hasattr(cls, "up") and hasattr(cls, "down"):
                    instance = cls()
                    instance.up()
                    break

            self._driver.execute(
                "INSERT INTO _migrations (migration, batch) VALUES (?, ?)",
                [name, batch]
            )

    def rollback(self):
        batch = self._get_batch()

        if batch == 0:
            return

        ran = self._driver.query(
            "SELECT migration FROM _migrations "
            "WHERE batch = ? ORDER BY id DESC",
            [batch]
        )

        for row in ran:
            name = row["migration"]
            filepath = f"app/Migrations/{name}.py"

            if os.path.exists(filepath):
                module = self._load_module(name, filepath)

                for attr in dir(module):
                    cls = getattr(module, attr)

                    if isinstance(cls, type) and hasattr(cls, "up") and hasattr(cls, "down"):
                        instance = cls()
                        instance.down()
                        break

            self._driver.execute(
                "DELETE FROM _migrations WHERE migration = ?",
                [name]
            )

    def _load_module(self, name, filepath):
        spec = importlib.util.spec_from_file_location(name, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
