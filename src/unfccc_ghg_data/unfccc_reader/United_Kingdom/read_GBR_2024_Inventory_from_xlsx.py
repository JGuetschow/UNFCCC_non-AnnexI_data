"""
Read UK's 2024 inventory from xlsx

Files available here: https://naei.beis.gov.uk/reports/reports?report_id=1140

Currently not all detail is read as the same IPCC code is used for subcategories
in some cases. For animal species this leads to wrong attribution of emissions
from several species to one.

"""
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.United_Kingdom.config_uk_inv2024 import (
    basket_copy,
    cat_conversion,
    cols_to_drop,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    entity_unit_filter,
    gas_baskets,
    meta_data,
    terminology_proc,
    time_format,
)

if __name__ == "__main__":
    pd.set_option("future.no_silent_downcasting", True)

    # ###
    # configuration
    # ###

    # folders and files
    input_folder = (
        downloaded_data_path
        / "non-UNFCCC"
        / "United_Kingdom_of_Great_Britain_and_Northern_Ireland"
        / "2024-Inventory"
    )
    output_folder = extracted_data_path / "non-UNFCCC" / "United_Kingdom"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "GBR_2024-Inventory_"

    inventory_file = "2406181003_DA_GHGI_1990-2022_v2.1.xlsx"
    sheet_to_read = "BySource_data"

    name_for_cat_col = "category"
    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    data_pd = pd.read_excel(
        input_folder / inventory_file,
        sheet_name=sheet_to_read,
        engine="openpyxl",
        skiprows=6,
        usecols="C:P",
    )
    data_pd = data_pd.drop(columns=cols_to_drop)

    # filter for the right unit per gas
    data_pd_unit = None
    for entity in entity_unit_filter:
        unit = entity_unit_filter[entity]["from"]
        data_current = data_pd.query(
            f"Pollutant == '{entity}' " f"& ConvertTo == '{unit}'"
        ).copy()
        data_current["ConvertTo"] = data_current["ConvertTo"].replace(
            {unit: entity_unit_filter[entity]["to"]}
        )

        if data_pd_unit is None:
            data_pd_unit = data_current
        else:
            data_pd_unit = pd.concat([data_pd_unit, data_current])

    # remove base year data
    data_pd = data_pd_unit.query("EmissionYear != 'BaseYear'")

    # combine timeseries for given category, area, entity
    coords_to_keep = ["EmissionYear", "IPCC_code", "ConvertTo", "Pollutant"]
    more_cols_to_drop = ["RegionName", "Sourcecode", "IPCC_name", "TESS2", "TESS3"]
    data_grouped = data_pd.groupby(coords_to_keep).sum().reset_index()

    data_grouped = data_grouped.drop(columns=more_cols_to_drop)

    data_if = pm2.pm2io.convert_long_dataframe_if(
        data_grouped,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        meta_data=meta_data,
        time_format=time_format,
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # ###
    # conversion to ipcc 2006 categories
    # ###

    data_pm2_2006 = data_pm2.copy()

    # actual processing

    country_processing = {
        "basket_copy": basket_copy,
    }

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion,
        # sectors_out=sectors_to_save,
    )

    # adapt source and metadata
    # TODO: processing info is present twice
    current_source = data_pm2_2006.coords["source"].to_numpy()[0]
    data_temp = data_pm2_2006.pr.loc[{"source": current_source}]
    data_pm2_2006 = data_pm2_2006.pr.set("source", "AI_INV", data_temp)
    data_pm2_2006 = data_pm2_2006.pr.loc[{"source": ["AI_INV"]}]

    # convert back to IF to have units in the fixed format
    data_if_2006 = data_pm2_2006.pr.to_interchange_format()

    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc),
        data_if_2006,
    )

    encoding = {var: compression for var in data_pm2_2006.data_vars}
    data_pm2_2006.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"),
        encoding=encoding,
    )
