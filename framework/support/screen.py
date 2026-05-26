class ScreenResponse:
    def __init__(self, name: str, method: str = "handle"):
        self.name = name
        self.method = method


def screen(name: str, method: str = "handle"):
    return ScreenResponse(name, method)


_1 = 1
_2 = 2
_3 = 3
_4 = 4
_5 = 5


def data(callback_query, n):
    return callback_query.matches[0].group(n)
