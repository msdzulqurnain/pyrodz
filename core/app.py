from pyrogram import Client

from app.Config.Bot import Bot
from framework.route import routes

from framework.support.helpers import load_routes, register_routes
from framework.support.Log import Log


class App(Client):
    def __init__(self):
        super().__init__(
            name=Bot.NAME,
            workdir="storage/sessions",
            api_id=int(Bot.API_ID),
            api_hash=Bot.API_HASH,
            bot_token=Bot.BOT_TOKEN,
        )

        load_routes()
        register_routes(self, routes)
