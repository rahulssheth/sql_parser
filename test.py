from sql_parser.main import generate_sql
from sql_parser.sql_types import Dialect
from sql_parser.new_parser import SQLiteParser
from sql_parser.new_where_clause import default_handle_like_query
from sql_parser.new_literal_clause import default_handle_booleans

def handle_assertion(evaluated, expected):
	assert evaluated == expected, (evaluated, expected)

fields = {1: "id",
 2: "name",
 3: "date_joined",
 4: "age",
 5: "is_staff"}

def run_base_test_cases():
	# Test cases from the spec.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["=", ["field", 3], None]}), '''SELECT * FROM data WHERE "date_joined" IS NULL;''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, { "where": ["is-empty", ["field", 3]], "limit": 10 }), '''SELECT * FROM data WHERE "date_joined" IS NULL LIMIT 10;''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": [">", ["field", 4], 35]}), '''SELECT * FROM data WHERE "age" > 35;''')
	# This is a deviation from how the test case is presented in the spec but that's because MySQL should be using backticks, not double quotes for column identifiers.
	handle_assertion(generate_sql(Dialect.MYSQL, {1: "id", 2: "name"}, {"where": ["=", ["field", 2], "cam"], "limit": 10}), '''SELECT * FROM data WHERE `name` = 'cam' LIMIT 10;''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["=", ["field", 2], "joe"]]}), '''SELECT * FROM data WHERE "id" < 5 AND "name" = 'joe';''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["=", ["field", 4], 25, 26, 27]}), '''SELECT * FROM data WHERE "age" IN (25, 26, 27);''')
	# This is a deviation from how the test case is presented in the spec but that's because it had double quotes around the OR and did not double quote the "id" column.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["or", ["!=", ["field", 3], "2015-11-01"], ["=", ["field", 1], 456]]}), '''SELECT * FROM data WHERE "date_joined" <> '2015-11-01' OR "id" = 456;''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["!=", ["field", 3], None], ["or", [">", ["field", 4], 25], ["=", ["field", 2], "Jerry"]]]}), '''SELECT * FROM data WHERE "date_joined" IS NOT NULL AND ("age" > 25 OR "name" = 'Jerry');''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"limit": 20}), '''SELECT * FROM data LIMIT 20;''')
	handle_assertion(generate_sql(Dialect.SQLSERVER, fields, {"limit": 20}), '''SELECT TOP 20 * FROM data;''')

def run_edge_test_cases():
	# Edge cases not in spec.

	# Edge case where NULL is provided in an inequality.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["!=", ["field", 3], None]}), '''SELECT * FROM data WHERE "date_joined" IS NOT NULL;''')
	# Edge case where NULL is provided in an IN.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["=", ["field", 3], None, 35, 50]}), '''SELECT * FROM data WHERE "date_joined" IN (35, 50) OR "date_joined" IS NULL;''')
	# Edge case where NULL is provided in a NOT IN.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["!=", ["field", 3], None, 40, 60]}), '''SELECT * FROM data WHERE "date_joined" NOT IN (40, 60) AND "date_joined" IS NOT NULL;''')

	# Handle case with many OR's
	handle_assertion(generate_sql(Dialect.MYSQL, fields, {"where": ["or", ["<", ["field", 4], 5], [">", ["field", 4], 30], ["=", ["field", 4], None]]}), '''SELECT * FROM data WHERE `age` < 5 OR `age` > 30 OR `age` IS NULL;''')
	# Slightly complex AND/OR conditions with NULL handling.
	handle_assertion(generate_sql(Dialect.SQLSERVER, fields, {"limit": 50, "where": ["or", ["and", ["<", ["field", 1], 5], ["=", ["field", 2], "joe"]], ["or", [">", ["field", 1], 10], ["=", ["field", 2], "nash", "collin", None]]]}), 
		'''SELECT TOP 50 * FROM data WHERE ("id" < 5 AND "name" = 'joe') OR ("id" > 10 OR ("name" IN ('nash', 'collin') OR "name" IS NULL));''')

	# Default case where nothing is provided.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {}), "SELECT * FROM data;")

def run_new_where_clauses_test_cases():
	# This is being passed in at runtime.
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["like", ["field", 2], "jo%"]]}, mapping_overrides={'like': default_handle_like_query}), '''SELECT * FROM data WHERE "id" < 5 AND "name" LIKE 'jo%';''')
	# This has been defined in a different file and is added to the mapping.
	handle_assertion(generate_sql(Dialect.MYSQL, fields, {"where": ["between", ["field", 4], 25, 50]}), '''SELECT * FROM data WHERE `age` BETWEEN 25 AND 50;''')

def run_new_literals_test_case():
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["=", ["field", 5], True]}, literal_overrides={bool: default_handle_booleans}), '''SELECT * FROM data WHERE "is_staff" = TRUE;''')

def run_new_parser_test_case():
	handle_assertion(generate_sql("sqlite", fields, {"where": ["=", ["field", 5], True]}, parser_cls=SQLiteParser), '''SELECT * FROM data WHERE "is_staff" = 1;''')

def run_macros_test_cases():
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["macro", "is_joe"]]}, macros={"is_joe": ["=", ["field", 2], "joe"]}), '''SELECT * FROM data WHERE "id" < 5 AND "name" = 'joe';''')
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["macro", "is_joe"]}, macros={"is_joe": ["=", ["field", 2], "joe"]}), '''SELECT * FROM data WHERE "name" = 'joe';''')

	# Nested macro defined as a complex macro.
	handle_assertion(generate_sql(Dialect.MYSQL, fields, {"where": ["macro", "is_adult_joe"]}, macros={"is_adult_joe": ["and", ["=", ["field", 2], "joe"], [">", ["field", 4], 21]]}), '''SELECT * FROM data WHERE `name` = 'joe' AND `age` > 21;''')

	try:
		generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["macro", "is_jim"]]}, macros={"is_joe": ["=", ["field", 2], "joe"]})
	except Exception as e:
		assert str(e) == "is_jim not found in current parser macros."
	else:
		raise Exception("Failed test case with undefined macro.")

def run_nested_macros_test_cases():
	nested_macros = {"is_joe": ["=", ["field", 2], "joe"],
	 "is_adult": [">", ["field", 4], 18],
	 "is_adult_joe": ["and", ["macro", "is_joe"], ["macro", "is_adult"]]}
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["macro", "is_adult_joe"]]}, macros=nested_macros), '''SELECT * FROM data WHERE "id" < 5 AND ("name" = 'joe' AND "age" > 18);''')

	circular_macros = {"is_good": ["and", ["macro", "is_decent"], [">", ["field", 4], 18]],
	 "is_decent": ["and", ["macro", "is_good"], ["<", ["field", 5], 5]]}
	try:
		generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 1], 5], ["macro", "is_adult_joe"]]}, macros=circular_macros)
	except Exception as e:
		assert str(e) == "Circular dependency found in macros with is_decent and is_good"
	else:
		raise Exception("Failed test case with circular macro.")

	other_nested_macros = {"is_jim": ["=", ["field", 2], "joe"],
	 "is_jade": ["=", ["field", 2], "jade"],
	 "is_jim_or_jade": ["or", ["macro", "is_jim"], ["macro", "is_jade"]]}
	handle_assertion(generate_sql(Dialect.POSTGRES, fields, {"where": ["and", ["<", ["field", 4], 5], ["macro", "is_jim_or_jade"]]}, macros=other_nested_macros), '''SELECT * FROM data WHERE "age" < 5 AND ("name" = 'joe' OR "name" = 'jade');''')
	handle_assertion(generate_sql("postgres", fields, {"where": ["and", ["<", ["field", 4], 5], ["macro", "is_jim_or_jade"]]}, macros=other_nested_macros), '''SELECT * FROM data WHERE "age" < 5 AND ("name" = 'joe' OR "name" = 'jade');''')

run_base_test_cases()
run_edge_test_cases()
run_new_parser_test_case()
run_new_where_clauses_test_cases()
run_new_literals_test_case()
run_macros_test_cases()
run_nested_macros_test_cases()

print("Test Cases Succeded")