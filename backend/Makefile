all: tests black_check ruff_check mypy_check import_linter_check
	echo "All checks passed!"

tests:
	echo "Running automated tests..."
	pytest
	echo "Automated tests passed."

black_check:
	echo "Checking black..."
	black --check ./
	echo "Black passed."

ruff_check:
	echo "Checking ruff..."
	ruff check ./
	echo "Ruff passed."

mypy_check:
	echo "Checking mypy..."
	mypy ./
	echo "Mypy passed."

import_linter_check:
	echo "Checking imports restrictions..."
	lint-imports
	echo "Import restrictions met."
