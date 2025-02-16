from sql_parser.dialect_parsers.base_parser import BaseParser

class SQLServerParser(BaseParser):
	def generate_sql(self, query):
		limit = query.get("limit")
		base_str = "SELECT * FROM data"
		if limit:
			base_str = f"SELECT TOP {limit} * FROM data"

		where_clause = query.get("where")
		if where_clause:
			where = self.handle_where_clause(where_clause)
			base_str += f" WHERE {where}"
		return f"{base_str};"
