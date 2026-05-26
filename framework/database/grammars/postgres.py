from .sqlite import SqliteGrammar


class PostgresGrammar(SqliteGrammar):
    def _build_where(self):
        sql, params = super()._build_where()
        return sql.replace("?", "%s"), params

    def compile_select(self):
        sql, params = super().compile_select()
        return sql.replace("?", "%s"), params

    def compile_insert(self, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join("%s" for _ in data)
        sql = (
            f"INSERT INTO {self._query._table} "
            f"({columns}) VALUES ({placeholders})"
        )
        return sql + " RETURNING id", list(data.values())

    def compile_update(self, data):
        sql, params = super().compile_update(data)
        return sql.replace("?", "%s"), params

    def compile_delete(self):
        sql, params = super().compile_delete()
        return sql.replace("?", "%s"), params

    def compile_count(self):
        sql, params = super().compile_count()
        return sql.replace("?", "%s"), params
