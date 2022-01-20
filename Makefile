.SILENT: help
help:
	echo Options:
	echo make update-bur: Update list of BUR submissions
	echo make download-bur: Download BUR submissions
	echo make update-nc: Update list of NC submissions
	echo make download-nc: Download NC submissions
	echo make download-ndc: Download NDC submissions
	echo make venv: create virtual environment

update-bur: venv
	datalad run -m "Fetch BUR submissions" -o downloaded_data/UNFCCC/submissions-bur.csv ./venv/bin/python code/UNFCCC_downloader/fetch_submissions_bur.py

download-bur: venv
	datalad run -m "Download BUR submissions" -i downloaded_data/UNFCCC/submissions-bur.csv ./venv/bin/python code/UNFCCC_downloader/download_bur.py

update-nc: venv
	datalad run -m "Fetch NC submissions" -o downloaded_data/UNFCCC/submissions-nc.csv ./venv/bin/python code/UNFCCC_downloader/fetch_submissions_nc.py

download-nc: venv
	datalad run -m "Download NC submissions" -i downloaded_data/UNFCCC/submissions-nc.csv ./venv/bin/python code/UNFCCC_downloader/download_nc.py

download-ndc: venv
	datalad run -m "Download NDC submissions" ./venv/bin/python code/UNFCCC_downloader/download_ndc.py

venv: code/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur code/requirements.txt
	touch venv
