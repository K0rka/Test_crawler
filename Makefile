requirements.txt: requirements/requirements.in
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile -r --no-emit-index-url --output-file requirements.txt requirements/requirements.in

requirements-dev.txt: requirements/requirements.in requirements/requirements-dev.in
	CUSTOM_COMPILE_COMMAND="make freeze" pip-compile -r --no-emit-index-url --output-file requirements-dev.txt requirements/requirements.in requirements/requirements-dev.in

freeze: requirements.txt requirements-dev.txt

freeze-upgrade:
	CUSTOM_COMPILE_COMMAND="make freeze-upgrade" pip-compile -r --no-emit-index-url --upgrade --output-file requirements.txt requirements/requirements.in
	CUSTOM_COMPILE_COMMAND="make freeze-upgrade" pip-compile -r --no-emit-index-url --upgrade --output-file requirements-dev.txt requirements/requirements.in requirements/requirements-dev.in

install:
	PIP_CONFIG_FILE=pip.conf pip install -r requirements.txt .

install-dev:
	PIP_CONFIG_FILE=pip.conf pip install -r requirements-dev.txt -e .

test:
	black -l 120 -t py37 src/ tests/
	pytest -sv tests/

black:
	black -l 120 -t py37 src/ tests/
