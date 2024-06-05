FLASK_APP = app.py
FLASK := FLASK_APP=$(FLASK_APP) env/bin/flask
SETUP_DIR := ./setup
.PHONY: run
run:
	flask run --debug

.PHONY: run-prod
run-production:
	flask run

.PHONY: init
init:
	@sh ${SETUP_DIR}/init_setup.sh

.PHONY: clean
clean:
	rm -rf env
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +