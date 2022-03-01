.SILENT: help
help:
	echo Options:
	echo make venv: create virtual environment

venv: code/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur code/requirements.txt
	touch venv
