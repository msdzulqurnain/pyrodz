import importlib
import inspect
import re

from .screen import ScreenResponse
from .Log import Log


def load_routes():
    import routes.bot


def resolve_filter(expr):
    from pyrogram import filters as pyro_filters

    if expr is None:
        return None

    if isinstance(expr.expr, str):
        return getattr(pyro_filters, expr.expr)

    op = expr.expr[0]

    if op == "and":
        return resolve_filter(expr.expr[1]) & resolve_filter(expr.expr[2])

    if op == "or":
        return resolve_filter(expr.expr[1]) | resolve_filter(expr.expr[2])

    if op == "not":
        return ~resolve_filter(expr.expr[1])


def resolve(path):
    if isinstance(path, type):
        return path

    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)

    return getattr(module, class_name)


def resolve_handler(handler):
    if callable(handler):
        class_name = handler.__qualname__.split(".")[0]
        module = importlib.import_module(handler.__module__)
        cls = getattr(module, class_name)

        return getattr(cls(), handler.__name__)

    if isinstance(handler, str):
        module_path, class_name, method_name = handler.rsplit(".", 2)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)

        return getattr(cls(), method_name)

    return handler


def parse_data_marker(pattern):
    parts = pattern.split("$")
    escaped = [re.escape(p) for p in parts]
    return f"^{'(.+)'.join(escaped)}$"


async def send_error(update, error):
    try:
        if hasattr(update, "message") and hasattr(update.message, "reply"):
            await update.message.reply(
                "An error occurred. Please try again later."
            )
        elif hasattr(update, "answer"):
            await update.answer(
                "An error occurred. Please try again.",
                show_alert=True,
            )
    except Exception:
        pass


async def handle_response(response, client, update):
    if not isinstance(response, ScreenResponse):
        return

    try:
        module_path = "screen." + response.name.replace("/", ".")
        module = importlib.import_module(module_path)
        handler = getattr(module, response.method)
        result = handler(client, update)

        if inspect.isawaitable(result):
            await result
    except Exception as e:
        Log.exception("Screen error")
        await send_error(update, e)


def register_routes(app, routes):
    from pyrogram import filters as pyro_filters

    def wrap(handler):
        async def wrapper(client, update):
            try:
                response = await handler(client, update)
                await handle_response(response, client, update)
            except Exception as e:
                Log.exception("Handler error")
                await send_error(update, e)

        return wrapper

    for route in routes:
        handler = resolve_handler(route["handler"])
        extra_filter = resolve_filter(route.get("filters"))

        if route["type"] == "command":
            route_filter = pyro_filters.command(route["name"])

            if extra_filter:
                route_filter = route_filter & extra_filter

            app.on_message(route_filter)(wrap(handler))

        elif route["type"] == "callback":
            raw = route["name"]

            if route["regex"] and "$" in raw:
                pattern = parse_data_marker(raw)
            elif route["regex"]:
                pattern = raw
            else:
                pattern = f'^{raw}$'

            route_filter = pyro_filters.regex(pattern)

            if extra_filter:
                route_filter = route_filter & extra_filter

            app.on_callback_query(route_filter)(wrap(handler))

        elif route["type"] == "inline":
            if extra_filter:
                app.on_inline_query(extra_filter)(wrap(handler))
            else:
                app.on_inline_query()(wrap(handler))
