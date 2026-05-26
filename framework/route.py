routes = []


class Route:
    @staticmethod
    def command(name, handler, filters=None):
        routes.append({
            "type": "command",
            "name": name,
            "handler": handler,
            "filters": filters,
        })

    @staticmethod
    def callback(name, handler, filters=None):
        routes.append({
            "type": "callback",
            "name": name,
            "handler": handler,
            "filters": filters,
            "regex": False,
        })

    @staticmethod
    def regex(pattern, handler, filters=None):
        routes.append({
            "type": "callback",
            "name": pattern,
            "handler": handler,
            "filters": filters,
            "regex": True,
        })

    @staticmethod
    def inline(handler, filters=None):
        routes.append({
            "type": "inline",
            "name": "[inline query]",
            "handler": handler,
            "method": "inline",
            "filters": filters,
        })
    
    @staticmethod
    def current(handler, filters=None):
        routes.append({
            "type": "inline",
            "name": "[current inline query]",
            "handler": handler,
            "method": "current",
            "filters": filters,
        })