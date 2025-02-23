SHELL := /bin/bash
REQUIREMENTS_TXT := requirements.txt
PYTHON := python3

.PHONY: python-deps
python-deps:
	pip install -r $(REQUIREMENTS_TXT)

.PHONY: compile-requirements
compile-requirements:
	pip install pip-tools --upgrade
	CUSTOM_COMPILE_COMMAND="./make compile-requirements" pip-compile -o $(REQUIREMENTS_TXT)

.PHONY: clean
clean:
	rm -rf .venv
