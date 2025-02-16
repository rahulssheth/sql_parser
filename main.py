from sql_parser.dialect_parsers import dialect_to_parser_class
from sql_parser.dialect_parsers.base_parser import BaseParser
from sql_parser.sql_types import Dialect

from typing import Any, Callable

def get_all_macros(macro_array: list[Any]) -> list[str]:
	found_macros = []
	for elem in macro_array:
		if type(elem) == list:
			if elem[0] == "macro":
				found_macros.append(elem[1])
			else:
				found_macros += get_all_macros(elem)
	return found_macros

def verify_macro_dictionary(macros: dict[str, Any]) -> bool:
	macro_dependency = {}
	for macro_key, macro_value in macros.items():
		all_macros = get_all_macros(macro_value)
		for dependent_macro in all_macros:
			if macro_dependency.get(dependent_macro) and macro_key in macro_dependency[dependent_macro]:
				raise Exception(f"Circular dependency found in macros with {macro_key} and {dependent_macro}")
		macro_dependency[macro_key] = all_macros
	return True

def generate_sql(dialect: Dialect, fields: dict[int, str], query: dict[str, Any], parser_cls: BaseParser=None, mapping_overrides: dict[str, Callable]={}, macros: dict[str, Any]={}, literal_overrides: dict[str, Callable]={}):
	if macros:
		verify_macro_dictionary(macros)

	if not parser_cls:
		parser_class = dialect_to_parser_class[dialect](fields, mapping_overrides=mapping_overrides, macros=macros, literal_overrides=literal_overrides)
	else:
		parser_class = parser_cls(fields, mapping_overrides=mapping_overrides, macros=macros, literal_overrides=literal_overrides)
	return parser_class.generate_sql(query)
