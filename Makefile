
include tests.env

integration-tests:
	python3 -m pip install -r requirements.txt
	python3 -m pip install -r requirements-test.txt
	python3 -m pytest tests/integration
