class QueryBuilder:
    def __init__(self, driver, table):
        self._driver = driver
        self._table = table
        self._wheres = []
        self._orders = []
        self._limit = None
        self._offset = None
        self._joins = []
        self._grammar = driver.grammar(self)

    def where(self, col, op=None, val=None):
        if val is None:
            val = op
            op = "="
        self._wheres.append(("AND", col, op, val))
        return self

    def or_where(self, col, op=None, val=None):
        if val is None:
            val = op
            op = "="
        self._wheres.append(("OR", col, op, val))
        return self

    def order_by(self, col, direction="ASC"):
        self._orders.append((col, direction))
        return self

    def limit(self, n):
        self._limit = n
        return self

    def offset(self, n):
        self._offset = n
        return self

    def join(self, table, col1, op, col2, join_type="INNER"):
        self._joins.append((join_type, table, col1, op, col2))
        return self

    def get(self):
        sql, params = self._grammar.compile_select()
        return self._driver.query(sql, params)

    def first(self):
        self.limit(1)
        rows = self.get()
        return rows[0] if rows else None

    def find(self, id):
        return self.where("id", id).first()

    def count(self):
        sql, params = self._grammar.compile_count()
        result = self._driver.query(sql, params)
        return result[0]["count"] if result else 0

    def insert(self, data):
        sql, params = self._grammar.compile_insert(data)
        self._driver.execute(sql, params)
        return self._driver.last_insert_id()

    def update(self, data):
        sql, params = self._grammar.compile_update(data)
        self._driver.execute(sql, params)
        return self

    def delete(self):
        sql, params = self._grammar.compile_delete()
        self._driver.execute(sql, params)
        return self
