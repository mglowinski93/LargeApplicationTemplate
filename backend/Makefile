all: black-check isort-check import-linter-check ruff-check mypy-check bandit-check tests
	echo "All checks passed!"

black-check:
	echo "Checking black..."
	black --check ./
	echo "Black passed."

isort-check:
	echo "Checking isort..."
	isort --settings-path .isort.cfg --check-only .
	echo "Isort passed."

import-linter-check:
	echo "Checking import contracts..."
	lint-imports
	echo "Import contracts kept."

ruff-check:
	echo "Checking ruff..."
	ruff check ./
	echo "Ruff passed."

mypy-check:
	echo "Checking mypy..."
	mypy ./
	echo "Mypy passed."

bandit-check:
	echo "Checking bandit..."
	find . -name '*.py' | grep -v tests | xargs bandit
	echo "Bandit passed."

tests: unit-tests integrated-tests end-to-end-tests
	echo "All tests passed!"

unit-tests:
	echo "Running unit tests..."
	pytest tests/unit/
	echo "Unit tests passed."

integrated-tests:
	echo "Running integrated tests..."
	pytest tests/integrated/
	echo "Integrated tests passed."

end-to-end-tests:
	echo "Running end to end tests..."
	pytest tests/end_to_end/
	echo "End to end tests passed."
