"""
Input and output functions for the DI reader

Saving single country datasets and country groups datasets
"""
import datalad.api
import primap2 as pm2
import xarray as xr
from dask.base import tokenize

from unfccc_ghg_data.helper import root_path

from .unfccc_di_reader_helper import determine_dataset_filename, determine_filename


def save_DI_country_data(
    data_pm2: xr.Dataset,
    raw: bool = True,
):
    """
    Save primap2 and IF data to country folder

    Can be used for raw and processed data but for a single country only

    Parameters
    ----------
    data_pm2 (xr.Dataset)
        Data to be saved
    raw (bool: default = True)
        True if the data in raw, false if it is processed data

    Returns
    -------
    nothing
    """
    # preparations
    data_if = data_pm2.pr.to_interchange_format()

    ## get country
    countries = data_if[data_pm2.attrs["area"]].unique()
    if len(countries) > 1:
        raise ValueError(  # noqa: TRY003
            f"More than one country in input data. This function can only"
            f"handle single country data. Countries: {countries}"
        )
    else:
        country_code = countries[0]

    ## get timestamp
    scenario_col = data_pm2.attrs["scen"]
    scenarios = data_if[scenario_col].unique()
    if len(scenarios) > 1:
        raise ValueError(  # noqa: TRY003
            f"More than one scenario in input data. This function can only"
            f"handle single scenario data. Scenarios: {scenarios}"
        )
    else:
        scenario = scenarios[0]

    date_str = scenario[2:]

    # calculate the hash of the data to see if it's identical to present data
    data_for_token = data_if.drop(columns=[scenario_col])
    token = tokenize(data_for_token)

    # get the filename with the hash and check if it exists (separate for pm2 format
    # and IF to fix broken datasets if necessary)
    filename_hash = root_path / determine_filename(country_code, token, raw, hash=True)

    # primap2 native format
    filename_hash_nc = filename_hash.parent / (filename_hash.name + ".nc")
    if not (filename_hash_nc.exists() or filename_hash_nc.is_symlink()):
        # if parent dir does not exist create it
        if not filename_hash.parent.exists():
            filename_hash.parent.mkdir()
        # save the data
        print(f"Data has changed. Save to {filename_hash_nc.name}")
        compression = dict(zlib=True, complevel=9)
        encoding = {var: compression for var in data_pm2.data_vars}
        data_pm2.pr.to_netcdf(filename_hash_nc, encoding=encoding)
    elif not filename_hash_nc.exists() and filename_hash_nc.is_symlink():
        # This means that we have a broken symlink and need to download the data
        datalad.api.get(filename_hash_nc)

    # primap2 IF
    filename_hash_csv = filename_hash.parent / (filename_hash.name + ".csv")
    if not (filename_hash_csv.exists() or filename_hash_csv.is_symlink()):
        # save the data
        print(f"Data has changed. Save to {filename_hash.name + '.csv/.yaml'}")
        pm2.pm2io.write_interchange_format(filename_hash, data_if)
    else:
        print(f"Data unchanged for {country_code}. Create symlinks.")
        if not filename_hash_csv.exists() and filename_hash_csv.is_symlink():
            # This means that we have a broken symlink and need to download the data
            datalad.api.get(filename_hash_csv)

    # get the filename with the date
    filename_date = root_path / determine_filename(country_code, date_str, raw)

    # create the symlinks to the actual data (with the hash)
    suffixes = [".nc", ".csv", ".yaml"]
    for suffix in suffixes:
        file_date = filename_date.parent / (filename_date.name + suffix)
        file_hash = filename_hash.name + suffix
        if file_date.exists():
            file_date.unlink()
        file_date.symlink_to(file_hash)


def save_DI_dataset(
    data_pm2: xr.Dataset,
    raw: bool = True,
    annexI: bool = False,
):
    """
    Save primap2 and IF data to dataset folder

    Can be used for raw and processed data but not to save to country folders

    Parameters
    ----------
    data_pm2 (xr.Dataset)
        Data to be saved
    raw (bool: default = True)
        True if the data in raw, false if it is processed data
    annexI (bool: default = False)
        True if the data to save is from annexI countries, false if it's from
        non-annexi countries

    Returns
    -------
    nothing
    """
    """
    save primap2 and IF data to dataset folder
    can be used for raw and processed data but not to save to country folders
    """
    # preparations
    data_if = data_pm2.pr.to_interchange_format()
    if annexI:
        country_group = "AnnexI"
    else:
        country_group = "non-AnnexI"

    ## get timestamp
    scenario_col = data_pm2.attrs["scen"]
    scenarios = data_if[scenario_col].unique()
    if len(scenarios) > 1:
        raise ValueError(  # noqa: TRY003
            f"More than one scenario in input data. This function can only"
            f"handle single scenario data. Scenarios: {scenarios}"
        )
    else:
        scenario = scenarios[0]

    date_str = scenario[2:]

    # calculate the hash of the data to see if it's identical to present data
    data_for_token = data_if.drop(columns=[scenario_col])
    token = tokenize(data_for_token)

    # get the filename with the hash and check if it exists (separate for pm2 format
    # and IF to fix broken datasets if necessary)
    filename_hash = root_path / determine_dataset_filename(
        token, raw, annexI=annexI, hash=True
    )
    # primap2 native format
    filename_hash_nc = filename_hash.parent / (filename_hash.name + ".nc")
    if not (filename_hash_nc.exists() or filename_hash_nc.is_symlink()):
        # if parent dir does not exist create it
        # TODO double, also in determine_dataset_filename. same for country data
        if not filename_hash.parent.exists():
            filename_hash.parent.mkdir()
        # save the data
        print(f"Data has changed. Save to {filename_hash_nc.name}")
        compression = dict(zlib=True, complevel=9)
        encoding = {var: compression for var in data_pm2.data_vars}
        data_pm2.pr.to_netcdf(filename_hash_nc, encoding=encoding)
    elif not filename_hash_nc.exists() and filename_hash_nc.is_symlink():
        # This means that we have a broken symlink and need to download the data
        datalad.api.get(filename_hash_nc)

    # primap2 IF
    filename_hash_csv = filename_hash.parent / (filename_hash.name + ".csv")
    if not (filename_hash_csv.exists() or filename_hash_csv.is_symlink()):
        # save the data
        print(f"Data has changed. Save to {filename_hash.name + '.csv/.yaml'}")
        pm2.pm2io.write_interchange_format(filename_hash, data_if)
    else:
        print(f"Data unchanged for {country_group}. Create symlinks.")
        if not filename_hash_csv.exists() and filename_hash_csv.is_symlink():
            # This means that we have a broken symlink and need to download the data
            datalad.api.get(filename_hash_csv)

    # get the filename with the date
    filename_date = root_path / determine_dataset_filename(
        date_str, raw=raw, annexI=annexI, hash=False
    )

    # create the symlinks to the actual data (with the hash)
    suffixes = [".nc", ".csv", ".yaml"]
    for suffix in suffixes:
        file_date = filename_date.parent / (filename_date.name + suffix)
        file_hash = filename_hash.name + suffix
        if file_date.exists():
            file_date.unlink()
        file_date.symlink_to(file_hash)
