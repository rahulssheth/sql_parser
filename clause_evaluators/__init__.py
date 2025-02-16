from sql_parser.clause_evaluators.evaluators import (
	default_handle_and_or_clause,
	default_handle_gt_lt_clause,
	default_handle_eq_neq_clause,
	default_handle_isempty_isnotempty_clause,
	default_handle_macro_clause
)
from sql_parser.new_where_clause import default_handle_between_clause

base_mapping = {
	'and': default_handle_and_or_clause,
	'or': default_handle_and_or_clause,
	'<': default_handle_gt_lt_clause,
	'>': default_handle_gt_lt_clause,
	'=': default_handle_eq_neq_clause,
	'!=': default_handle_eq_neq_clause,
	'is-empty': default_handle_isempty_isnotempty_clause,
	'is-not-empty': default_handle_isempty_isnotempty_clause,
	'macro': default_handle_macro_clause,
	'between': default_handle_between_clause,
}
