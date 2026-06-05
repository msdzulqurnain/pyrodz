import os

from dotenv import load_dotenv

load_dotenv()


class App:
    ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("APP_DEBUG", "true").lower() == "true"