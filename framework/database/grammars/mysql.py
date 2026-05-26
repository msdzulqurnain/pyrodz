from .sqlite import SqliteGrammar


class MysqlGrammar(SqliteGrammar):
    def _build_where(self):
        sql, params = super()._build_where()
        return sql.replace("?", "%s"), params

    def compile_select(self):
        sql, params = super().compile_select()
        return sql.replace("?", "%s"), params

    def compile_insert(self, data):
        sql, params = super().compile_insert(data)
        return sql.replace("?", "%s"), params

    def compile_update(self, data):
        sql, params = super().compile_update(data)
        return sql.replace("?", "%s"), params

    def compile_delete(self):
        sql, params = super().compile_delete()
        return sql.replace("?", "%s"), params

    def compile_count(self):
        sql, params = super().compile_count()
        return sql.replace("?", "%s"), params
