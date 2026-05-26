import os

from dotenv import load_dotenv

load_dotenv()


class _Mongo:
    _client = None
    _db = None

    def _connect(self):
        if self._client is not None:
            return

        try:
            from pymongo import MongoClient
        except ImportError:
            raise ImportError(
                "MongoDB requires pymongo. Install: pip install pymongo"
            )

        uri = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017")
        database = os.getenv("MONGO_DATABASE", "pyrodz")

        self._client = MongoClient(uri)
        self._db = self._client[database]

    def __getattr__(self, name):
        self._connect()
        return getattr(self._db, name)


mongo = _Mongo()
