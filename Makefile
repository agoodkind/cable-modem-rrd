.PHONY: clean

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PY_SRC := src

activate:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate

setup: activate
	$(PIP) install '.'

setup-editable: activate
	$(PIP) install -I -e '.'

run-refresh: setup
	$(PYTHON) $(PY_SRC)/data/cli.py refresh --cycles 3 --sleep 15

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete