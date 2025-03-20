venv=. venv/bin/activate

makemigrations:
	$(venv); python makemigrations.py

build:
	$(venv); python -m build

publish:
	$(venv); python3 -m twine upload --repository pypi dist/*

