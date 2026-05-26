from pathlib import Path
from datetime import datetime
from framework.console.style import Style
from framework.console.command import Command


class MakeMigration(Command):
    def handle(self, *args):
        if not args:
            print()
            print(Style.warn("Usage: python3 pyrodz make:migration create_users_table"))
            return

        name = args[0]
        filename = f"{datetime.now():%Y_%m_%d_%H%M%S}_{name}.py"
        path = Path("app/Migrations") / filename

        path.parent.mkdir(parents=True, exist_ok=True)

        class_name = "".join(
            word.capitalize() for word in name.replace("-", "_").split("_")
        )

        table = name.replace("create_", "").replace("_table", "")

        content = f'''from framework.database import Schema


class {class_name}:
    def up(self):
        Schema.create("{table}", [
            Schema.increments("id"),
            Schema.timestamps(),
        ])

    def down(self):
        Schema.drop("{table}")
'''

        path.write_text(content, encoding="utf-8")

        print()
        print(Style.success(f"Migration created successfully"))
        print(Style.info(f"Location: {str(path)}"))
