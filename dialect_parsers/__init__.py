from sql_parser.dialect_parsers.mysql_parser import MySQLParser
from sql_parser.dialect_parsers.sqlserver_parser import SQLServerParser
from sql_parser.dialect_parsers.postgres_parser import PostgresParser
from sql_parser.dialect_parsers.base_parser import BaseParser
from sql_parser.sql_types import Dialect

dialect_to_parser_class: dict[Dialect, BaseParser] = {
	Dialect.POSTGRES: PostgresParser,
	Dialect.SQLSERVER: SQLServerParser,
	Dialect.MYSQL: MySQLParser
}
