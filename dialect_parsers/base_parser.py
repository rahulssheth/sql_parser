from sql_parser.clause_evaluators import base_mapping as base_clause_mapping
from sql_parser.field_evaluators import base_mapping as base_field_mapping

class BaseParser:
	def __init__(self, fields, mapping_overrides={}, macros={}, literal_overrides={}):
		self.fields = fields
		self.evaluator_mapping = {**base_clause_mapping, **mapping_overrides}
		self.field_mapping = {**base_field_mapping, **literal_overrides}
		self.macros = macros

	def handle_potential_field_clause(self, field) -> str:
		if type(field) in self.field_mapping:
			return self.field_mapping[type(field)](self, field)
		raise Exception(f"Unknown field encountered of type {type(field)}")

	def handle_where_clause(self, query, level=0) -> str:
		if query[0] not in self.evaluator_mapping:
			raise Exception(f"Operator {query[0]} not handled in mapping")
		return self.evaluator_mapping[query[0]](self, {"query": query, "level": level})

	def generate_sql(self, query):
		base_str = "SELECT * FROM data"
		limit = query.get("limit")
		# Handle WHERE
		where_clause = query.get("where")
		if where_clause:
			where = self.handle_where_clause(where_clause)
			base_str += f" WHERE {where}"
		if limit:
			base_str += f" LIMIT {limit}"
		return f"{base_str};"
