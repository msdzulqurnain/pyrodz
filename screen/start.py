from framework import Buttons, Btn


async def start(client, message):
    await message.reply(
        "👋 Welcome to PyroDZ!\n\n"
        "🤖 A Telegram bot framework built on Pyrogram.\n"
        "⚡ Routing, handlers, screens, database & CLI included.\n\n"
        "Use /help to see available commands.",
        reply_markup=Buttons(
            Btn.url("📖 Documentation", "https://github.com/msdzulqurnain/pyrodz"),
        )
    )
