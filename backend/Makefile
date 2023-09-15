all: tests black_check ruff_check mypy_check bandit_check
	echo "All checks passed!"

tests: unit_tests integrated_tests end_to_end_tests
	echo "All tests passed!"

unit_tests:
	echo "Running unit tests..."
	pytest tests/unit/
	echo "Unit tests passed."

integrated_tests:
	echo "Running integrated tests..."
	pytest tests/integrated/
	echo "Integrated tests passed."

end_to_end_tests:
	echo "Running end to end tests..."
	pytest tests/end_to_end/
	echo "End to end tests passed."

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

bandit_check:
	echo "Checking bandit..."
	find . -name '*.py' | grep -v tests | xargs bandit
	echo "Bandit passed."
