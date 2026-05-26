from abc import ABC, abstractmethod


class Grammar(ABC):
    def __init__(self, query):
        self._query = query

    @abstractmethod
    def compile_select(self):
        ...

    @abstractmethod
    def compile_insert(self, data):
        ...

    @abstractmethod
    def compile_update(self, data):
        ...

    @abstractmethod
    def compile_delete(self):
        ...

    @abstractmethod
    def compile_count(self):
        ...
