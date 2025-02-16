# This is a new where clause passed in at runtime.
def default_handle_like_query(parser, args) -> str:
	query = args["query"]
	return f"{parser.handle_potential_field_clause(query[1])} LIKE {parser.handle_potential_field_clause(query[2])}"

# This is a new where clause passed into the mapping.
def default_handle_between_clause(parser, args) -> str:
	query = args["query"]

	return f"{parser.handle_potential_field_clause(query[1])} BETWEEN {parser.handle_potential_field_clause(query[2])} AND {parser.handle_potential_field_clause(query[3])}"
