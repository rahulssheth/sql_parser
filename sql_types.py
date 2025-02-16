from enum import Enum

class Dialect(str, Enum):
	POSTGRES = "postgres"
	MYSQL = "mysql"
	SQLSERVER = "sqlserver"
