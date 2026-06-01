"""
Read USA's 2026 inventory from xlsx

Files available here:
https://www.edf.org/freedom-information-act-documents-epas-greenhouse-gas-inventory

Only the overview tables are read as details are in several individual tables and
overview is sufficient for PRIMAP-hist

# Tables to read:
Tables not mentioned here are either not necessary or don't contain emissions data

## Chapter 3: energy
* 3-1, (detail not sufficient for all gases, stationary and mobile summed for CH4, N2O)
* 3-3, 1.A subsectors for CO2, CH4, N2O
* 3-8: CO2 details per fuel and sector. probably not necessary
* 3-9: CH4 details per fuel and sector. probably not necessary
* 3-10: N2O details per fuel and sector. probably not necessary
* 3-21, 3-22: coal mines (1.B.1)
* 3-23 CH4 from abandoned coal mines
* 3-25, 3-26, 3-27 Petroleum systems
* 3-28, 3-29, 3-30 Natural gas systems
* 3-21, 3-32, abandoned oil and gas wells
* 3-33 1.C
* 3-36: bunkers
* 3-39 Biomass CO2 (not necessary, included in 3-1)

##  chapter 4: IPPU
* 4-1: overview table covering all sectors and gases (no F-gas per gas data)
* 4-31: Details petrochemical production (optional)
* 4-33: HFC-22 production
* 4-35: f-gas production other than HFC-22
* 4-38: CO2 from non-EOR Utilization (probably optional)
* 4-45: Iron and steel details (optional)
* 4-50: Aluminum production gas details (needed for f-gases)
* 4-52: Magnesium production gas details (needed for f-gases)
* 4-57: electronics industry gas details (needed for f-gases)
* 4-49: ODS substitutes (needed for f-gases)
* 4-61: Electrical equipment (needed for f-gases)
* 4-62: Other product use (needed for f-gases)

## chapter 5: Agriculture
* 5-1: overview. not enough details to map to IPCC categories, but OK for PRIMAP-hist
* 5-3: CH4 enteric fermentation
* 5-6: Manure management
* 5-10: Agricultural soils direct and indirect
* 5-11: liming details (optional, detail not needed)
* 5-15: field burning (optional, detail not needed)

## chapter 6: LULUCF
* 6-1: overview (suffices for LULUCF without details)
* 6-7: forest fires. needed to split CH4 and N2O
* 6-14: grassland fires: needed to split CH4 and N2O
* 6-16: peatland remaining peatland: needed for non-CO2

## chapter 7: waste
7-1: overview: not much detail, but enough for PRIMAP-hist

TODO:
# sector mapping
* Where does metallurgical coke production fit. Reported in IPPU, but could also fit
into 1.B.1. Was in 2.C.1 in 2024 inventory
"""

from copy import deepcopy

import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    gas_baskets,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Taiwan.config_twn_nir2025 import gwp_to_use
from unfccc_ghg_data.unfccc_reader.United_States_of_America.config_usa_inv2026 import (
    # basket_copy_PFCS,
    basket_copy_UnspMix,
    cat_conversion,
    coords_cols_template,
    coords_defaults_template,
    coords_terminologies,
    filter_remove,
    inventory_files,
    meta_data,
    terminology_proc,
    time_format,
)

# TODO: adapt to subfolders for csv files
if __name__ == "__main__":
    pd.set_option("future.no_silent_downcasting", True)

    # ###
    # configuration
    # ###

    # folders and files
    input_folder = (
        downloaded_data_path / "non-UNFCCC" / "United_States_of_America" / "2026_GHGIA"
    )
    output_folder = extracted_data_path / "non-UNFCCC" / "United_States_of_America"
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = "USA_2026-GHGIA_"
    compression = dict(zlib=True, complevel=9)

    # ###
    # start data reading
    # ###

    data_pm2 = None

    for folder, files in inventory_files.items():
        for file, file_config in files.items():
            print(f"reading {file}")
            category_col = file_config.pop("cat_col")
            # TODO: move to function if it works like this
            data_current_pd = pd.read_csv(
                input_folder / folder / file, header=[1], encoding="ISO-8859-1"
            )
            # remove the thousands separators (can't be done during reading as data is
            # stored as string)
            if "drop_cols" in file_config.keys():
                cols_to_drop = file_config.pop("drop_cols")
                data_current_pd = data_current_pd.drop(columns=cols_to_drop)
            if "map_cols" in file_config.keys():
                col_mapping = file_config.pop("map_cols")
                data_current_pd = data_current_pd.rename(columns=col_mapping)

            all_cols = data_current_pd.columns
            data_cols = [col for col in all_cols if col != category_col]
            for col in data_cols:
                if data_current_pd.dtypes[col] in ["object", "string"]:
                    data_current_pd[col] = data_current_pd[col].str.replace(",", "")

            # strip spaces from category col
            data_current_pd[category_col] = data_current_pd[category_col].str.strip()

            section_keys = file_config.keys()
            key_info = {}
            # find the ilocs for the section keys
            last_key = None
            for i, row in data_current_pd.iterrows():
                if row[category_col] in section_keys:
                    key_info[row[category_col]] = {}
                    key_info[row[category_col]]["start"] = i
                    if last_key is not None:
                        key_info[last_key]["end"] = i
                    last_key = row[category_col]

            # fill the key info for section keys with ilocs given
            for section_key in section_keys:
                if section_key.startswith("by_iloc"):
                    key_info[section_key] = {}
                    key_info[section_key]["start"] = file_config[section_key].pop(
                        "start"
                    )
                    key_info[section_key]["end"] = file_config[section_key].pop("end")

            for section_key in section_keys:
                current_config = file_config[section_key]
                if current_config is not None:
                    # get the data
                    if "end" in key_info[section_key].keys():
                        data_section = data_current_pd.iloc[
                            key_info[section_key]["start"] : key_info[section_key][
                                "end"
                            ]
                        ].copy()
                    else:
                        data_section = data_current_pd.iloc[
                            key_info[section_key]["start"] :
                        ].copy()

                    # convert to primap2 IF
                    coords_defaults = coords_defaults_template.copy()
                    coords_defaults.update(current_config["coords_defaults"])
                    coords_value_mapping = current_config["coords_value_mapping"]
                    coords_cols = coords_cols_template.copy()
                    for col in coords_value_mapping.keys():
                        # make a copy of the category column as we also need if for
                        # entity
                        data_section[col] = data_section[category_col]
                        coords_cols[col] = col
                    # drop the original col
                    data_section = data_section.drop(columns=category_col)

                    if "filter_remove" in current_config.keys():
                        filter_remove_current = current_config["filter_remove"]
                    else:
                        filter_remove_current = filter_remove

                    data_section_if = pm2.pm2io.convert_wide_dataframe_if(
                        data_section,
                        coords_cols=coords_cols,
                        coords_terminologies=coords_terminologies,
                        coords_defaults=coords_defaults,
                        coords_value_mapping=coords_value_mapping,
                        filter_remove=filter_remove_current,
                        meta_data=meta_data,
                        time_format=time_format,
                        convert_str={"+": 0, "+ ": 0},
                    )
                    # convert to primap2 native format
                    data_section_pm2 = pm2.pm2io.from_interchange_format(
                        data_section_if
                    )

                    # merge with other data
                    if data_pm2 is None:
                        data_pm2 = data_section_pm2
                    else:
                        data_pm2 = data_pm2.pr.merge(data_section_pm2)

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
    # the processing is done in several steps because of limitations of the current
    # processing function

    # we first need to make some copies of gwp weighted gas baskets with default
    # conversion factors as gas information is missing for a few cases
    country_processing_step1 = {
        # "basket_copy": basket_copy_PFCS,
        "aggregate_gases": {
            f"UnspMixOfPFCs ({gwp_to_use})": {
                "sources": [f"PFCS ({gwp_to_use})"],
                "sel": {
                    "category": ["2.G.2"],
                },
            },
        },
    }

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets={},
        processing_info_country=country_processing_step1,
    )

    country_processing_step2 = {
        "basket_copy": basket_copy_UnspMix,
    }

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets={},
        processing_info_country=country_processing_step2,
    )

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets={},
        processing_info_country=None,
        cat_terminology_out=terminology_proc,
        category_conversion=cat_conversion,
        # sectors_out=sectors_to_save,
    )

    country_processing_step4 = {
        "tolerance": 0.065  #  2.7% for HFC basket
        # for PFCs in 2.E we need 6.5%
        # for FGASES we need 2.5% (2.G.2.c)
    }

    gas_baskets_step4 = deepcopy(gas_baskets)
    gas_baskets_step4.pop("KYOTOGHG (AR5GWP100)")

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets=gas_baskets_step4,
        processing_info_country=country_processing_step4,
    )

    country_processing_step5 = {
        "tolerance": 0.01  # 25 # for HFC basket
        # for PFCs in 2.E we need 6.5%
    }

    gas_baskets.pop("HFCS (AR5GWP100)")
    gas_baskets.pop("PFCS (AR5GWP100)")
    gas_baskets.pop("FGASES (AR5GWP100)")

    data_pm2_2006 = process_data_for_country(
        data_pm2_2006,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        processing_info_country=country_processing_step5,
    )

    # adapt source and metadata
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
