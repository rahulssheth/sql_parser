from sql_parser.dialect_parsers.base_parser import BaseParser
from sql_parser.field_evaluators.evaluators import handle_mysql_list

def handle_sqlite_bool(parser, field):
	return 1 if field else 0

class SQLiteParser(BaseParser):
	def __init__(self, fields, mapping_overrides={}, macros={}, literal_overrides={}):
		super().__init__(fields, mapping_overrides, macros, {**literal_overrides, bool: handle_sqlite_bool})
