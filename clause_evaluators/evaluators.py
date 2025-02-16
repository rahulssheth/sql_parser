def default_handle_and_or_clause(parser, args) -> str:
	query = args["query"]
	level = args["level"]

	recurse_str = parser.handle_where_clause(query[1], level+1)
	for clause in query[2:]:
		parsed_clause = parser.handle_where_clause(clause, level+1)
		recurse_str += f" {query[0].upper()} {parsed_clause}"
	if level != 0:
		return f"({recurse_str})"
	return recurse_str

def default_handle_gt_lt_clause(parser, args) -> str:
	query = args["query"]

	return f"{parser.handle_potential_field_clause(query[1])} {query[0]} {parser.handle_potential_field_clause(query[2])}"

def default_handle_macro_clause(parser, args) -> str:
	query = args["query"]
	level = args["level"]
	if query[1] not in parser.macros:
		raise Exception(f"{query[1]} not found in current parser macros.")

	return parser.handle_where_clause(parser.macros[query[1]], level)

def default_handle_eq_neq_clause(parser, args):
	query = args["query"]
	level = args["level"]

	if len(query) > 3:
		operator = 'IN' if query[0] == '=' else 'NOT IN'
		in_str = ""
		handle_null = False
		for in_field in query[2:len(query)-1]:
			if in_field is None:
				handle_null = True
			else:
				in_str += f"{parser.handle_potential_field_clause(in_field)}, "
		if query[-1] is None:
			handle_null = True
			# We included an extra ", " which we'll need to remove
			in_str = in_str[0:-2]
		else:
			in_str += f"{parser.handle_potential_field_clause(query[-1])}"
		base_clause = f"{parser.handle_potential_field_clause(query[1])} {operator} ({in_str})"
		if handle_null:
			if operator == 'IN':
				base_str = f"{base_clause} OR {parser.handle_potential_field_clause(query[1])} IS NULL"
				if level > 0:
					return f"({base_str})"
				return base_str
			else:
				base_str = f"{base_clause} AND {parser.handle_potential_field_clause(query[1])} IS NOT NULL"
				if level > 0:
					return f"({base_str})"
				return base_str
		return base_clause
	else:
		if query[2] == None:
			if query[0] == '=':
				return f"{parser.handle_potential_field_clause(query[1])} IS NULL"
			if query[0] == '!=':
				return f"{parser.handle_potential_field_clause(query[1])} IS NOT NULL"
		op = query[0] if query[0] == '=' else '<>'
		return f"{parser.handle_potential_field_clause(query[1])} {op} {parser.handle_potential_field_clause(query[2])}"

def default_handle_isempty_isnotempty_clause(parser, args):
	query = args["query"]

	append_str = "IS NULL" if query[0] == 'is-empty' else "IS NOT NULL"
	return f"{parser.handle_potential_field_clause(query[1])} {append_str}"

def default_handle_not_clause(parser, args):
	query = args["query"]
	level = args["level"]

	return f"NOT ({parser.handle_where_clause(query[1], level+1)})"
