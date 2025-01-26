VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: all venv install run

all: venv install run

venv:
	@if [ ! -d "$(VENV)" ]; then python3 -m venv $(VENV); fi

install: venv
	$(PIP) install -r requirements.txt

run:
	cd backend &&
	$(PYTHON) manage.py runserver
