SHELL 				:= /bin/bash
PYTHON 				:= source .venv/bin/activate && python
PIP 				:= $(PYTHON) -m pip
REQUIREMENTS_TXT 	:= vision/requirements.txt
REQUIREMENTS_IN 	:= vision/requirements.in

.venv:
	python3.12 -m venv .venv

.PHONY: compile-requirements
compile-requirements: .venv
	$(PIP) install pip-tools --upgrade && CUSTOM_COMPILE_COMMAND="make compile-requirements" pip-compile -o $(REQUIREMENTS_TXT) $(REQUIREMENTS_IN)

.PHONY: python-deps
python-deps: compile-requirements
	$(PIP) install -r $(REQUIREMENTS_TXT)

.PHONY: clean
clean:
	rm -rf .venv

.PHONY: dev
dev:
	$(PYTHON)