import os
from dotenv import load_dotenv

load_dotenv()

class Bot:
    NAME = os.getenv("BOT_NAME", "pyrodz-bot")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")