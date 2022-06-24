from pathlib import Path

root_path = Path(__file__).parents[2].absolute()
root_path = root_path.resolve()
log_path = root_path / "log"
code_path = root_path / "code"
downloaded_data_path = root_path / "downloaded_data" / "UNFCCC"
extracted_data_path = root_path / "extracted_data" / "UNFCCC"

class NoDIDataError(Exception):
    pass