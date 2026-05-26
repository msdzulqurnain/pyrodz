from abc import ABC, abstractmethod


class BaseDriver(ABC):
    @abstractmethod
    def connect(self, config):
        ...

    @abstractmethod
    def query(self, sql, params=None):
        ...

    @abstractmethod
    def execute(self, sql, params=None):
        ...

    @abstractmethod
    def last_insert_id(self):
        ...

    @abstractmethod
    def close(self):
        ...

    @abstractmethod
    def grammar(self, query):
        ...
