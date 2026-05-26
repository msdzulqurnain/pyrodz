from framework.console.style import Style
from framework.database.migration import Migration


class Migrate:
    def handle(self, *args):
        if args and args[0] == "rollback":
            self._rollback()
        else:
            self._up()

    def _up(self):
        print()
        print(Style.info("Running migrations..."))
        print()

        try:
            Migration().up()
            print(Style.success("Migrations completed"))
        except Exception as e:
            print(Style.error(f"Migration failed: {e}"))

    def _rollback(self):
        print()
        print(Style.info("Rolling back migrations..."))
        print()

        try:
            Migration().rollback()
            print(Style.success("Rollback completed"))
        except Exception as e:
            print(Style.error(f"Rollback failed: {e}"))
