import routes.bot

from framework.route import routes
from framework.console.style import Style


class RouteList:
    def handle(self, *args):
        print()
        print(Style.info("Registered routes"))
        print()

        if not routes:
            print(Style.warn("No routes registered"))
            return

        self.print_header()

        sorted_routes = sorted(
            routes,
            key=lambda route: (
                route["type"] != "command",
                route["name"]
            )
        )

        for route in sorted_routes:
            route_type = route["type"].upper()
            name = route["name"]
            raw_handler = route["handler"]
            filters = self.format_filter(route.get("filters"))

            if callable(raw_handler):
                handler = raw_handler.__qualname__
            else:
                handler = str(raw_handler)

            print(
                f"{Style.text(route_type.ljust(10), Style.GREEN)}"
                f"{name.ljust(18)}"
                f"{handler.ljust(22)}"
                f"{Style.muted(filters)}"
            )

        print()

    def print_header(self):
        print(
            f"{Style.muted('TYPE'.ljust(10))}"
            f"{Style.muted('ROUTE'.ljust(18))}"
            f"{Style.muted('HANDLER'.ljust(22))}"
            f"{Style.muted('FILTERS')}"
        )

        print(
            f"{Style.muted('-' * 8).ljust(10)}"
            f"{Style.muted('-' * 16).ljust(18)}"
            f"{Style.muted('-' * 20).ljust(22)}"
            f"{Style.muted('-' * 10)}"
        )

    def format_filter(self, expr):
        if expr is None:
            return "-"

        value = expr.expr

        if isinstance(value, str):
            return value

        op = value[0]

        if op == "and":
            return f"{self.format_filter(value[1])} & {self.format_filter(value[2])}"

        if op == "or":
            return f"{self.format_filter(value[1])} | {self.format_filter(value[2])}"

        if op == "not":
            return f"~{self.format_filter(value[1])}"

        return "-"