from pathlib import Path
from framework.console.style import Style
from framework.console.command import Command


class MakeModel(Command):
    def handle(self, *args):
        if not args:
            print()
            print(Style.warn("Usage: python3 pyrodz make:model User"))
            return

        name = args[0]

        if not self.is_valid_class_name(name):
            self.invalid_name(name, "Model")
            return

        path = Path("app/Models") / f"{name}.py"

        if path.exists():
            print()
            print(Style.warn(f"{path} already exists"))
            return

        path.parent.mkdir(parents=True, exist_ok=True)

        snake = name[0].lower() + "".join(
            f"_{c.lower()}" if c.isupper() else c for c in name[1:]
        )

        content = f'''from framework.database import Model


class {name}(Model):
    table = "{snake}"
    fillable = []
    guarded = ["id"]
    timestamps = True
'''

        path.write_text(content, encoding="utf-8")

        print()
        print(Style.success(f"Model {name} created successfully"))
        print(Style.info(f"Location: {str(path)}"))
