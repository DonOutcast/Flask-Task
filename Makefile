.PHONY: linters

linters:
	isort .
	absolufy-imports
	ruff --fix
	autoflake . --in-place -r
	black .
	vulture .
