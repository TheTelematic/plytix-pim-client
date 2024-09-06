build:
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade setuptools[core]
	python3 -m pip install --upgrade build
	python3 -m build

publish:
	python3 -m pip install --upgrade twine
	python3 -m twine upload dist/*
	rm -rf dist
