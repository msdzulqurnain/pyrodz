from datetime import datetime

from .manager import ConnectionManager
from .query import QueryBuilder


class Model:
    table = None
    fillable = []
    primary_key = "id"
    timestamps = False

    def __init__(self, attributes=None):
        self._attributes = {}
        self._dirty = {}
        self._exists = False

        if attributes:
            self._attributes = dict(attributes)

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(
            f"'{type(self).__name__}' has no attribute '{name}'"
        )

    def __setattr__(self, name, value):
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._attributes[name] = value
            self._dirty[name] = value

    @staticmethod
    def _now():
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def _new_query(cls):
        driver = ConnectionManager().driver()
        return QueryBuilder(driver, cls.table)

    @classmethod
    def find(cls, id):
        row = cls._new_query().where(cls.primary_key, id).first()

        if row:
            instance = cls(row)
            instance._exists = True
            return instance

        return None

    @classmethod
    def create(cls, data=None, **kwargs):
        if data is None:
            data = kwargs

        filtered = (
            {k: v for k, v in data.items() if k in cls.fillable}
            if cls.fillable else data
        )

        if cls.timestamps:
            now = cls._now()
            filtered["created_at"] = now
            filtered["updated_at"] = now

        pk = cls._new_query().insert(filtered)
        return cls.find(pk)

    @classmethod
    def where(cls, col, op=None, val=None):
        return cls._new_query().where(col, op, val)

    @classmethod
    def all(cls):
        return cls._new_query().get()

    def save(self):
        if self._exists:
            filtered = (
                {k: v for k, v in self._dirty.items() if k in self.fillable}
                if self.fillable else self._dirty
            )

            if filtered:
                if self.timestamps:
                    now = self._now()
                    filtered["updated_at"] = now
                    self._attributes["updated_at"] = now
                pk_val = self._attributes.get(self.primary_key)
                self._new_query().where(self.primary_key, pk_val).update(filtered)
                self._dirty = {}
        else:
            data = dict(self._attributes)
            filtered = (
                {k: v for k, v in data.items() if k in self.fillable}
                if self.fillable else data
            )

            if self.timestamps:
                now = self._now()
                filtered.setdefault("created_at", now)
                filtered["updated_at"] = now

            pk = self._new_query().insert(filtered)
            fresh = type(self).find(pk)
            self._attributes = dict(fresh._attributes) if fresh else {}
            self._exists = True
            self._dirty = {}

    def delete(self):
        if self._exists:
            pk_val = self._attributes.get(self.primary_key)
            self._new_query().where(self.primary_key, pk_val).delete()
            self._exists = False
