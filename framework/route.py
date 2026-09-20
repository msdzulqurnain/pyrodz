route_registry = []


class Route:
    @staticmethod
    def command(name, handler, filters=None):
        route_registry.append({
            "type": "command",
            "name": name,
            "handler": handler,
            "filters": filters,
        })

    @staticmethod
    def callback(name, handler, filters=None, regex=False):
        route_registry.append({
            "type": "callback",
            "name": name,
            "handler": handler,
            "filters": filters,
            "regex": bool(regex),
        })

    @staticmethod
    def regex(pattern, handler, filters=None):
        return Route.callback(pattern, handler, filters, regex=True)

    @staticmethod
    def inline(handler, filters=None):
        route_registry.append({
            "type": "inline",
            "name": "[inline query]",
            "handler": handler,
            "method": "inline",
            "filters": filters,
        })

    @staticmethod
    def current(handler, filters=None):
        route_registry.append({
            "type": "inline",
            "name": "[current inline query]",
            "handler": handler,
            "method": "current",
            "filters": filters,
        })

    @staticmethod
    def message(*args, **kwargs):
        if args and callable(args[0]):
            pattern = None
            handler = args[0]
            extra = kwargs.get("filters", args[1] if len(args) > 1 else None)
        elif len(args) >= 2 and isinstance(args[0], str) and callable(args[1]):
            pattern = args[0]
            handler = args[1]
            extra = kwargs.get("filters", args[2] if len(args) > 2 else None)
        else:
            raise TypeError("Route.message() expects (pattern, handler, filters=None) or (handler, filters=None)")

        route_registry.append({
            "type": "message",
            "pattern": pattern,
            "handler": handler,
            "filters": extra,
        })


routes = route_registry