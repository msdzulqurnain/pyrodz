from pyrogram import Client

from app.Config.Bot import Bot
from framework.route import route_registry
from framework.router import import_routes, register_routes


class BotApp(Client):
    def __init__(self):
        super().__init__(
            name=Bot.NAME,
            workdir="storage/sessions",
            api_id=int(Bot.API_ID),
            api_hash=Bot.API_HASH,
            bot_token=Bot.BOT_TOKEN,
        )

        import_routes()
        register_routes(self, route_registry)