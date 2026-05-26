from pathlib import Path
from framework.console.style import Style
from framework.console.command import Command


class MakeCommand(Command):
    SUFFIX = "Handler"

    def handle(self, *args):
        if not args:
            print()
            print(Style.warn("Usage: python3 pyrodz make:command Help"))
            return

        raw_name = args[0]

        if not self.is_valid_class_name(raw_name):
            self.invalid_name(raw_name, self.SUFFIX)
            return

        if raw_name.endswith(self.SUFFIX):
            name = raw_name
        else:
            name = raw_name + self.SUFFIX

        command_name = raw_name.replace(self.SUFFIX, "").lower()
        method_name = command_name

        path = Path("app/Handlers") / f"{name}.py"
        path.parent.mkdir(parents=True, exist_ok=True)

        method_code = (
            f'\n    async def {method_name}(self, client, message):'
            f'\n        await message.reply(f"Hello! You used /{method_name}")'
            f'\n'
        )

        if path.exists():
            content = path.read_text(encoding="utf-8")
            if f"def {method_name}(" in content:
                print()
                print(Style.warn(f'Method "{method_name}" already exists in {path}'))
                return
            path.write_text(content.rstrip() + "\n" + method_code, encoding="utf-8")
        else:
            path.write_text(f"class {name}:{method_code}", encoding="utf-8")

        self.add_route(name, command_name, method_name)

        print()
        print(Style.success(f"Command /{command_name} created successfully"))
        print(Style.info(f'Location: {str(path)}'))

    def add_route(self, class_name, command_name, method_name):
        route_path = Path("routes/bot.py")

        if not route_path.exists():
            route_path.parent.mkdir(parents=True, exist_ok=True)
            route_path.write_text(
                "from framework.route import Route\n\n",
                encoding="utf-8"
            )

        import_line = f'from app.Handlers.{class_name} import {class_name}'
        route_line = f'Route.command("{command_name}", {class_name}.{method_name})'

        content = route_path.read_text(encoding="utf-8")

        if route_line in content:
            if not self.confirm(Style.info(f'Route "{command_name}" already exists. Overwrite?')):
                print()
                print(Style.warn("Route registration skipped"))
                return

            content = content.replace(route_line, "")
            lines = content.splitlines()
            import_match = [l for l in lines if import_line in l]
            for l in import_match:
                content = content.replace(l, "")
            content = content.strip() + "\n"

        if import_line not in content:
            lines = content.splitlines()
            last_import_idx = -1
            for i, line in enumerate(lines):
                if line.strip().startswith("from ") or line.strip().startswith("import "):
                    last_import_idx = i
            if last_import_idx >= 0:
                lines.insert(last_import_idx + 1, import_line)
            else:
                lines.insert(0, import_line)
            content = "\n".join(lines) + "\n"

        content = content.rstrip() + "\n" + route_line + "\n"

        route_path.write_text(content, encoding="utf-8")
