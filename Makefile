VENV_PATH := .venv
REQUIREMENTS_IN := requirements.in
REQUIREMENTS_TXT := requirements.txt

.PHONY: source-venv
source-venv:
ifeq ("","$(wildcard $(VENV_PATH))")
	python -m venv .venv
endif
	. $(VENV_PATH)/bin/activate

.PHONY: python-deps
python-deps: source-venv
	pip install -r $(REQUIREMENTS_TXT)

.PHONY: compile-requirements
compile-requirements: source-venv
	pip install req-compile --upgrade
	req-compile --index-url="https://pypi.org/simple" $(REQUIREMENTS_IN) > $(REQUIREMENTS_TXT)