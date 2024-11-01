
ifneq (,$(wildcard ./tests.env))
    include tests.env
    export
endif

requirements-tests:
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-test.txt

lint: requirements-tests
	python3 -m flake8 src tests --max-line-length=120
	python3 -m mypy --install-types --non-interactive src/ tests/

unit-tests: requirements-tests
	@args=$1

	python3 -m pytest tests/unit ${args}

integration-tests: requirements-tests
	@args=$1

	python3 -m pytest tests/integration ${args}
