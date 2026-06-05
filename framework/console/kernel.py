import sys
import importlib

from framework.console.style import Style


class Kernel:
    commands = {
        "start": (
            "framework.console.commands.start_command.StartCommand",
            "Start the Telegram bot",
        ),
        "route:list": (
            "framework.console.commands.route_list.RouteList",
            "Display all registered routes",
        ),
        "make:command": (
            "framework.console.commands.make_command.MakeCommand",
            "Scaffold a new command handler and route",
        ),
        "make:callback": (
            "framework.console.commands.make_callback.MakeCallback",
            "Scaffold a new callback handler and route",
        ),
        "make:model": (
            "framework.console.commands.make_model.MakeModel",
            "Generate a new model class",
        ),
        "make:migration": (
            "framework.console.commands.make_migration.MakeMigration",
            "Create a new migration file",
        ),
        "migrate": (
            "framework.console.commands.migrate.Migrate",
            "Run all pending migrations",
        ),
        "make:db": (
            "framework.console.commands.make_db.MakeDb",
            "Initialize the database",
        ),
        "update": (
            "framework.console.commands.update.Update",
            "Update the framework to the latest version",
        ),
    }

    groups = [
        (
            "Run & Debug",
            ["start", "route:list", "update"],
        ),
        (
            "Scaffolding",
            ["make:command", "make:callback", "make:model", "make:migration"],
        ),
        (
            "Database",
            ["migrate", "make:db"],
        ),
    ]

    specials = [
        ("migrate rollback", "Rollback the last migration batch"),
    ]

    no_args = {"start", "route:list", "migrate", "make:db", "update"}

    def handle(self):
        if len(sys.argv) < 2:
            self.show_help()
            return

        if sys.argv[1] in ("--version", "-v"):
            print(f"PyroDZ v{Style.FRAMEWORK_VERSION} ({Style.MODE})")
            return

        command_name = sys.argv[1]
        args = sys.argv[2:]

        entry = self.commands.get(command_name)

        if not entry:
            print(Style.error(f"Command not found: {command_name}"))
            print()
            self.show_help()
            return

        if command_name == "start":
            self.show_banner()

        command = self.resolve(entry[0])
        command.handle(*args)

    def resolve(self, command_path):
        module_name, class_name = command_path.rsplit(".", 1)

        module = importlib.import_module(module_name)
        command_class = getattr(module, class_name)

        return command_class()

    def show_banner(self):
        print()
        print(Style.brand())
        print()
        print(Style.system_info())
        print()

    def show_help(self):
        print()
        print(Style.brand())
        print()
        print(Style.muted("These are common pyrodz commands used in various situations:"))
        print()

        for title, cmd_names in self.groups:
            print(f"  {Style.text(title, Style.CYAN)}")
            for cmd in cmd_names:
                path, desc = self.commands[cmd]
                label = cmd if cmd in self.no_args else f"{cmd} <Name>"
                print(f"    {Style.text(label, Style.GREEN):<28} {Style.muted(desc)}")
            print()

        print(f"  {Style.text('Additional', Style.CYAN)}")
        for label, desc in self.specials:
            print(f"    {Style.text(label, Style.GREEN):<28} {Style.muted(desc)}")
