# SQL Transpiler

## Description

This is a SQL transpiler that has full handling for MySQL, SQLServer, and Postgres (with some customizations for SQLite).
The entrypoint for this is `main.py/generate_sql` which will take in a dialect, field mapping, a query and some customizations (see below)
and output the SQL string in that particular dialect. Some architecture notes follow:

- All parsers live in `dialect_parsers`. These parsers will be the entrypoints for clause and field evaluation.
  - These parsers take some customization, namely different where clauses and field types.
- All where clause evaluators live in `clause_evaluators`. These evaluators handle different where clauses we might encounter (eq, neq, AND, OR, etc).
  - They all will take in the parser class in question and a dictionary of args (for now, this just includes the query it's meant to evaluate
    and the level of nesting we may be in).
  - There is some macro support built in. The macros would need to be passed in at runtime.
- All field evaluators live in `field_evaluators`. These evaluators handle the fields we may encounter (str, int, macros, columns, etc).

## How to run

As mentioned earlier, the main entrypoint is `main.py` but our test cases are written in a separate `test.py` file. To run these tests, within the direct parent directory of `sql_parser`, run `python -m sql_parser.test`.

## Customization
### How to add a new dialect?
	- Within /dialect_parsers, add a new class that inherits from `BaseParser`.
	- Add in any customizations you may need to add.
		- If the customizations involve field based customizations (eg: handling literals or columns differently), override `handle_potential_field_clause`.
		- If the customizations involve new where clause parsing or overrides on the existing where clauses supported
			- If you only want to override them for some calls, pass them into `mapping_overrides`.
			- Otherwise, define a new entry to the mapping in `clause_evalutors/__init__.py`
		- If the customizations involve any changes to the SQL structure (eg: MySQL placing LIMIT in a different place), you'll need to override the `generate_sql` method of the parser.
	- Add in the new parser to the `dialect_to_parser_class`
	- Alternatively, if you'd like to pass in the parser at runtime, you can also pass it into the method with the `parser_cls` param. See SQLiteParser for an example.

### How to add a new where clause evaluator?
	- If you'd like to add a parser for long term use:
		- The long term best practice would be to place it in `clause_evaluators/evaluators.py` and then override `base_mapping` in `clause_evaluators`.
		- Alternatively, you can define the evaluator elsewhere and still add it to the mapping. See `default_handle_between_clause` for an example.
	- If you'd like to pass it in at runtime:
		- Pass in the clause to `mapping_overrides`. The first portion of the where clause should match on (eg: `is-empty`, etc) the key and the value should be the evaluator.
	- If you'd like to override an existing operator:
		- You can handle it in the same way above and pass in the new method with the same operator at runtime. See `default_handle_like_query` for an example.

### How to add a new field clause evaluator?
	- If you'd like to add a new field evaluator for long term use:
		- The long term best practice would be to place it in `field_evaluators/evaluators.py` and then override `base_mapping` in `field_evaluators`.
		- Alternatively, you can define the evaluator elsewhere.
	- If you'd like to pass it in at runtime.
		- Pass in the mapping to `field_evaluators`. The type of the field should match the key and the value should be the evaluator.
		- See `default_handle_booleans` for an example.
