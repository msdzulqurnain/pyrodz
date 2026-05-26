from .base import Grammar


class SqliteGrammar(Grammar):
    def _build_where(self):
        q = self._query
        if not q._wheres:
            return "", []

        clauses = []
        params = []

        for i, (connector, col, op, val) in enumerate(q._wheres):
            prefix = "WHERE" if i == 0 else connector
            clauses.append(f"{prefix} {col} {op} ?")
            params.append(val)

        return " ".join(clauses), params

    def compile_select(self):
        q = self._query
        sql = f"SELECT * FROM {q._table}"

        for join_type, table, col1, op, col2 in q._joins:
            sql += f" {join_type} JOIN {table} ON {col1} {op} {col2}"

        where_clause, params = self._build_where()

        if where_clause:
            sql += f" {where_clause}"

        if q._orders:
            orders = ", ".join(f"{col} {dir}" for col, dir in q._orders)
            sql += f" ORDER BY {orders}"

        if q._limit is not None:
            sql += f" LIMIT {q._limit}"

        if q._offset is not None:
            sql += f" OFFSET {q._offset}"

        return sql, params

    def compile_insert(self, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        sql = (
            f"INSERT INTO {self._query._table} "
            f"({columns}) VALUES ({placeholders})"
        )
        return sql, list(data.values())

    def compile_update(self, data):
        q = self._query
        sets = ", ".join(f"{col} = ?" for col in data)
        sql = f"UPDATE {q._table} SET {sets}"
        params = list(data.values())

        where_clause, where_params = self._build_where()

        if where_clause:
            sql += f" {where_clause}"
            params.extend(where_params)

        return sql, params

    def compile_delete(self):
        q = self._query
        sql = f"DELETE FROM {q._table}"
        where_clause, params = self._build_where()

        if where_clause:
            sql += f" {where_clause}"

        return sql, params

    def compile_count(self):
        q = self._query
        sql = f"SELECT COUNT(*) as count FROM {q._table}"
        where_clause, params = self._build_where()

        if where_clause:
            sql += f" {where_clause}"

        return sql, params
