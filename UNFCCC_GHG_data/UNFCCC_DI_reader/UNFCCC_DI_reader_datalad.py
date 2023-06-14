from datetime import date
from typing import Union, Optional
import datalad.api
from datalad.support.exceptions import IncompleteResultsError
from UNFCCC_GHG_data.helper import root_path, code_path

from .UNFCCC_DI_reader_helper import get_input_and_output_files_for_country_DI
from .util import DI_date_format

## datalad and pydoit interface functions
def read_DI_for_country_datalad(
        country: str,
) -> None:
    """
    Wrapper around read_UNFCCC_DI_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data reading

    Parameters
    __________

    country: str
        country name or ISO 3-letter country code

    """

    # get date to determine output filename
    today = date.today()
    date_str = today.strftime(DI_date_format)

    # get all the info for the country
    country_info = get_input_and_output_files_for_country_DI(country, date_str,
                                                             raw=True, verbose=True)

    print(f"Attempting to read DI data for {country_info['name']}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_DI_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_DI_reader" / "read_UNFCCC_DI_for_country.py"
    script = script.relative_to(root_path)

    cmd = f"./venv/bin/python3 {script.as_posix()} --country={country_info['code']} " \
          f"--date={date_str}"
    try:
        datalad.api.run(
            cmd=cmd,
            dataset=root_path,
            message=f"Read DI data for {country_info['name']}.",
            inputs=country_info["input"],
            outputs=country_info["output"],
            dry_run=None,
            explicit=False,
        )
    except IncompleteResultsError as IRE:
        print(f"IncompleteResultsError occured when running {cmd}: {IRE}")
    except Exception as ex:
        print(f"Exception occurred when running {cmd}")
        print(ex.message)


def process_DI_for_country_datalad(
        country: str,
        date_str: Union[str, None],
) -> None:
    """
    Wrapper around process_UNFCCC_DI_for_country which takes care of selecting input
    and output files and using datalad run to trigger the data processing

    Parameters
    __________

    country: str
        country name or ISO 3-letter country code
    date_str: str
        Date of the data to be processed in the format %Y-%m-%d (e.g. 2023-01-30). If
        no date is given the last data read will be processed.
    """

    # get all the info for the country
    country_info = get_input_and_output_files_for_country_DI(country, date_str,
                                                             raw=True, verbose=True)

    print(f"Attempting to process DI data for {country_info['name']}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_DI_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_DI_reader" / "process_UNFCCC_DI_for_country.py"
    script = script.relative_to(root_path)

    cmd = f"./venv/bin/python3 {script.as_posix()} --country={country_info['code']} " \
          f"--date={date_str}"
    try:
        datalad.api.run(
            cmd=cmd,
            dataset=root_path,
            message=f"Read DI data for {country_info['name']}.",
            inputs=country_info["input"],
            outputs=country_info["output"],
            dry_run=None,
            explicit=False,
        )
    except IncompleteResultsError as IRE:
        print(f"IncompleteResultsError occurred when running {cmd}: {IRE}")
    except Exception as ex:
        print(f"Exception occurred when running {cmd}")
        print(ex.message)


def read_DI_for_country_group_datalad(
        annexI: bool=False,
) -> None:
    """
    Wrapper around read_UNFCCC_DI_for_country_group which takes care of selecting input
    and output files and using datalad run to trigger the data processing

    Parameters
    __________

    country: str
        country name or ISO 3-letter country code
    date_str: str
        Date of the data to be processed in the format %Y-%m-%d (e.g. 2023-01-30). If
        no date is given the last data read will be processed.
    """

    if annexI:
        country_group = "AnnexI"
    else:
        country_group = "non-AnnexI"

    print(f"Attempting to read DI data for {country_group}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_DI_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_DI_reader" / "read_UNFCCC_DI_for_country_group.py"
    script = script.relative_to(root_path)

    cmd = f"./venv/bin/python3 {script.as_posix()} "
    if annexI:
        cmd = cmd + f" --annexI"

    try:
        datalad.api.run(
            cmd=cmd,
            dataset=root_path,
            message=f"Read DI data for {country_group}.",
            inputs=[],
            outputs=[],
            dry_run=None,
            explicit=False,
        )
    except IncompleteResultsError as IRE:
        print(f"IncompleteResultsError occurred when running {cmd}: {IRE}")
    except Exception as ex:
        print(f"Exception occurred when running {cmd}")
        print(ex.message)


def process_DI_for_country_group_datalad(
        annexI: bool=False,
        date_str: Optional[str]=None,
) -> None:
    """
    Wrapper around read_UNFCCC_DI_for_country_group which takes care of selecting input
    and output files and using datalad run to trigger the data processing

    Parameters
    __________

    annexI: bool (default False)
        If True process all annexI countries (not implemented yet), else all non-AnnexI
        countries.
    date_str: str (default None)
        Date of the data to be processed in the format %Y-%m-%d (e.g. 2023-01-30). If
        no date is given the last data read will be processed.
    """

    if annexI:
        country_group = "AnnexI"
    else:
        country_group = "non-AnnexI"

    print(f"Attempting to process DI data for {country_group}.")
    print("#"*80)
    print("")
    print(f"Using the UNFCCC_DI_reader")
    print("")
    print(f"Run the script using datalad run via the python api")
    script = code_path / "UNFCCC_DI_reader" / "process_UNFCCC_DI_for_country_group.py"
    script = script.relative_to(root_path)

    cmd = f"./venv/bin/python3 {script.as_posix()} "
    if annexI:
        cmd = cmd + f" --annexI"
    if date_str is not None:
        cmd = cmd + f" --date_str={date_str}"
    else:
        date_str = "latest"

    try:
        datalad.api.run(
            cmd=cmd,
            dataset=root_path,
            message=f"Process DI data for {country_group} for date {date_str}",
            inputs=[],
            outputs=[],
            dry_run=None,
            explicit=False,
        )
    except IncompleteResultsError as IRE:
        print(f"IncompleteResultsError occurred when running {cmd}: {IRE}")
    except Exception as ex:
        print(f"Exception occurred when running {cmd}")
        print(ex.message)