from sql_parser.field_evaluators.evaluators import (
	default_handle_lists,
	default_handle_ints,
	default_handle_strs
)

base_mapping = {
	int: default_handle_ints,
	str: default_handle_strs,
	list: default_handle_lists
}
