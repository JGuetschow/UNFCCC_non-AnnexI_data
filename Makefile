.SILENT: help
help:
	echo Options:
	echo make update-bur: Update list of BUR submissions
	echo make download-bur: Download BUR submissions
	echo make update-nc: Update list of NC submissions
	echo make download-nc: Download NC submissions
	echo make venv: create virtual environment

update-bur: venv
	./venv/bin/python scripts/fetch_submissions_bur.py

download-bur: venv
	./venv/bin/python scripts/download_bur.py

update-nc: venv
		./venv/bin/python scripts/fetch_submissions_nc.py

download-nc: venv
		./venv/bin/python scripts/download_nc.py

venv: code/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur code/requirements.txt
	touch venv
