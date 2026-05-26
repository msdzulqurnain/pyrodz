from pyrogram import Client

from core.app import App
from app.Config.Bot import Bot
from framework.console.style import Style


class StartCommand:
    def handle(self, *args):
        if not self.credentials_are_valid():
            return

        self.show_bot_info()

        print()
        print(Style.success("Starting bot..."))
        print(Style.info("Press CTRL+C to stop"))
        print()

        try:
            App().run()
        except KeyboardInterrupt:
            print()
            print(Style.warn("Bot stopped"))

    def credentials_are_valid(self):
        missing = []

        if not Bot.API_ID:
            missing.append("API_ID")

        if not Bot.API_HASH:
            missing.append("API_HASH")

        if not Bot.BOT_TOKEN:
            missing.append("BOT_TOKEN")

        if missing:
            print(Style.warn("Telegram bot credentials are not configured"))
            print()

            for item in missing:
                print(Style.info(f"Missing: {item}"))

            print()
            print(Style.muted("Please update your .env file"))
            return False

        return True

    def show_bot_info(self):
        try:
            with Client(
                name=f"{Bot.NAME}_info",
                workdir="storage/sessions",
                api_id=int(Bot.API_ID),
                api_hash=Bot.API_HASH,
                bot_token=Bot.BOT_TOKEN,
                in_memory=True,
            ) as client:
                me = client.get_me()

                print(Style.success("Telegram credentials loaded"))
                print()
                print(Style.muted(f"Bot Name    {me.first_name}"))
                print(Style.muted(f"Bot ID      {me.id}"))
                print(Style.muted(f"Username    @{me.username}"))

        except Exception as e:
            print(Style.error("Failed to connect to Telegram"))
            print(Style.muted(str(e)))
