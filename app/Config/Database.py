import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    CONNECTION = os.getenv("DB_CONNECTION", "sqlite")
    DATABASE = os.getenv("DB_DATABASE", "storage/database.sqlite")
    HOST = os.getenv("DB_HOST", "127.0.0.1")
    PORT = os.getenv("DB_PORT", "3306")
    USERNAME = os.getenv("DB_USERNAME", "root")
    PASSWORD = os.getenv("DB_PASSWORD", "")

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE", "pyrodz")
