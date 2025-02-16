def default_handle_booleans(parser, field):
	if field:
		return "TRUE"
	else:
		return "FALSE"
