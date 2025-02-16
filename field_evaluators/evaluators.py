def default_handle_ints(parser, field):
	return field

def default_handle_strs(parser, field):
	return f"'{field}'"

def default_handle_lists(parser, field):
	if field[0] == "field":
		return f'"{parser.fields[field[1]]}"'
	if field[0] == "macro":
		return parser.handle_where_clause(macros[field[1]])
	raise Exception("Unknown field encountered")

def handle_mysql_list(parser, field):
	if field[0] == "field":
		return f'`{parser.fields[field[1]]}`'
	if field[0] == "macro":
		return parser.handle_where_clause(macros[field[1]])
	raise Exception("Unknown field encountered")
