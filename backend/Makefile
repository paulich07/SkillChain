VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
DJANGO_DIR=backend

.PHONY: all venv install run

all: venv install run

venv:
	@if [ ! -d "$(VENV)" ]; then python3 -m venv $(VENV); fi

install: venv
	@bash -c "source $(VENV)/bin/activate && $(PIP) install -r requirements.txt"

run:
	@bash -c "source $(VENV)/bin/activate && cd $(DJANGO_DIR) && python manage.py runserver"
