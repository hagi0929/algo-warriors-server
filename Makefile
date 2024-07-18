.ONESHELL:

FLASK_APP = app.py
FLASK := FLASK_APP=$(FLASK_APP) env/bin/flask
SETUP_DIR := ./setup
.PHONY: run
run:
	poetry run python app.py

.PHONY: run-prod
run-prod:
	poetry run python app.py --gunicorn --env prod

.PHONY: install
init:
	poetry install

.PHONY: clean
clean:
	rm -rf env
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
