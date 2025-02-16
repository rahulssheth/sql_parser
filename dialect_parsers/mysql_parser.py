from sql_parser.dialect_parsers.base_parser import BaseParser
from sql_parser.field_evaluators.evaluators import handle_mysql_list

class MySQLParser(BaseParser):
	def __init__(self, fields, mapping_overrides={}, macros={}, literal_overrides={}):
		super().__init__(fields, mapping_overrides, macros, {**literal_overrides, list: handle_mysql_list})
