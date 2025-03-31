import pytest

from src.unfccc_ghg_data.unfccc_crf_reader.crf_raw_for_year_sparse_arrays import (
    crf_raw_for_year_datatree
)
import primap2 as pm
import xarray as xr
import numpy as np

@pytest.fixture
def crt_dt(tmp_path):
    """Return a data tree object with CRT data for 25 countries"""
    n_countries = 100  # 25 of which are filled
    crt_dt = crf_raw_for_year_datatree(
        submission_year=1,
        submission_type="CRT",
        n_countries=n_countries,
        output_folder=tmp_path,
    )

    return crt_dt

def test_country_aggregation(crt_dt):

    # Nigeria (NGA)
    expected_NGA = 123840.3389332373
    assert np.squeeze(crt_dt["/NGA"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "2022-01-01"}).to_numpy()).item() == expected_NGA
    # NGA has data from 2000 to 2022
    assert len(crt_dt["/NGA"].time) == 23

    # Georgia (GEO)
    expected_GEO = 10954.899111969342
    assert np.squeeze(crt_dt["/GEO"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "2022-01-01"}).to_numpy()).item() == expected_GEO
    # GEO has data from 1990 to 2022
    assert len(crt_dt["/GEO"].time) == 33
    # we have a value for 1990
    assert np.squeeze(crt_dt["/GEO"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "1990-01-01"}).to_numpy()).item()

    # Remove country dimension and add
    crt_dt["/NGA_GEO"] = crt_dt["/NGA"].to_dataset().pr.loc[{"area (ISO3)" : "NGA"}] + crt_dt["/GEO"].to_dataset().pr.loc[{"area (ISO3)" : "GEO"}]

    # Check if the sum of NGA and GEO is equal to NGA_GEO
    # This will perform an inner join, NGA has 23 time steps, GEO has 33 time steps,
    # and the result will have 23 time steps
    assert np.squeeze(crt_dt["/NGA_GEO"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "2022-01-01"}).to_numpy()).item() == expected_NGA + expected_GEO
    assert len(crt_dt["/NGA_GEO"].time) == 23

    # The default option for arithmetic operations is to perform an inner join
    # set options to perform outer join
    with xr.set_options(arithmetic_join="outer"):
        crt_dt["/NGA_GEO_outer"] = crt_dt["/NGA"].to_dataset().pr.loc[{"area (ISO3)" : "NGA"}] + crt_dt["/GEO"].to_dataset().pr.loc[{"area (ISO3)" : "GEO"}]

    # Where there is overlap between NGA and GEO, the values will be added
    assert np.squeeze(crt_dt["/NGA_GEO_outer"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "2022-01-01"}).to_numpy()).item() == expected_NGA + expected_GEO
    # When only one time series has a value, the value will be set to nan
    # TODO Is that the behaviour we need?
    assert np.isnan(np.squeeze(crt_dt["/NGA_GEO_outer"]["CO2"].sel(
        {"category (CRT1)" : "1", "class" : "Total", "time" : "1990-01-01"}).to_numpy()).item())
    # Extra time steps will be added
    assert len(crt_dt["/NGA_GEO_outer"].time) == 33

    # How can we use data tree methods for this?

    # filter countries we need
    dt_geo_nga = crt_dt.filter(lambda x: x.name in ["NGA", "GEO"])

    # fails because, x will be a data set view object that does not have the attribute to_dataset
    # dt_geo_nga = dt_geo_nga.map_over_datasets(lambda x: x.to_dataset().pr.loc[{"area (ISO3)" : x.name}])



def test_crf_for_year_original_version(crt_dt):

    print(crt_dt.groups)
    # output:
    # ('/', '/DZA', '/ARG', '/AZE', '/BTN', '/BRA', '/BRN', '/CHL', '/CHN', '/COL', '/CIV', '/ECU', '/EGY', '/GEO',
    # '/GHA', '/GNB', '/GUY', '/IDN', '/KEN', '/LBN', '/MYS', '/MDV', '/MUS', '/MAR', '/NAM', '/NGA')
    # out of the 100 countries, 26 have CRT data

    # to make it more interesting, we also add primap-hist to the data tree
    primap_hist = pm.open_dataset("../../data/Guetschow_et_al_2025-PRIMAP-hist_v2.6.1_final_13-Mar-2025.nc")
    # Assign primap hist to the data tree
    crt_dt["primap_hist"] = primap_hist
    print(crt_dt.groups)
    # output:
    # ('/', '/DZA', '/ARG', '/AZE', '/BTN', '/BRA', '/BRN', '/CHL', '/CHN', '/COL', '/CIV', '/ECU', '/EGY', '/GEO',
    # '/GHA', '/GNB', '/GUY', '/IDN', '/KEN', '/LBN', '/MYS', '/MDV', '/MUS', '/MAR', '/NAM', '/NGA', '/primap_hist')

    # try some queries

    # get the data for category 1
    # this will filter the primap-hist data set, because the CRT comes with
    # the coordinate "category (CRT1)"
    # Note that the data tree will have the same structure, only the individual
    # data sets will be filtered
    # print(dt_crt.sel({"category (IPCC2006_PRIMAP)" : "1"}))

    # we can re-assign the primap hist data set with a renamed category dimension
    crt_dt["primap_hist"] = primap_hist.rename({"category (IPCC2006_PRIMAP)" : "category (CRT1)"})

    # Now we should be able to filter for categories over all nodes
    dt_cat1 = crt_dt.sel({"category (CRT1)" : "1"})
