"""
Read Morocco's BUR3 from pdf

This script reads data from Morocco's BUR3
Data are read from pdf using camelot

"""

import copy

import camelot
import pandas as pd
import primap2 as pm2
from primap2.pm2io._data_reading import filter_data, matches_time_format

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path
from unfccc_ghg_data.unfccc_reader.Morocco.config_mar_bur3 import (
    aggregate_cats,
    cat_mapping,
    header_defs,
    remove_cats,
    table_defs,
    zero_cats,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Morocco" / "BUR3"
    output_folder = extracted_data_path / "UNFCCC" / "Morocco"
    output_filename = "MAR_BUR3_2022_"
    inventory_file = "Morocco_BUR3_Fr.pdf"
    gwp_to_use = "AR4GWP100"

    # years to read
    years = [2010, 2012, 2014, 2016, 2018]
    pages_to_read = range(104, 138)

    compression = dict(zlib=True, complevel=9)

    # special header as category code and name in one column
    header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

    index_cols = ["Catégories"]

    # rows to remove
    cats_remove = ["Agriculture"]  # always empty

    # manual category codes
    cat_codes_manual = {
        "1.A.2.e -Industries agro-alimentaires et du tabac": "1.A.2.e",
        "1.A.2.f -Industries des minéraux non- métalliques": "1.A.2.f",
        #'Agriculture': 'M.AG',
        "2. PIUP": "2",
        "UTCATF": "M.LULUCF",
        "3.B.1 Terres forestières": "LU.3.B.1",
        "3.B.2 Terres cultivées": "LU.3.B.2",
        "3.B.3 Prairies": "LU.3.B.3",
        "3.B.4 Terres humides": "LU.3.B.4",
        "3.B.5 Etablissements": "LU.3.B.5",
        "3.B.6 Autres terres": "LU.3.B.6",
        "1.B.1.a.i.1 -Exploitation minière": "1.A.1.a.i.1",
    }

    cat_code_regexp = r"(?P<code>^[a-zA-Z0-9\.]{1,14})\s-\s.*"

    coords_terminologies = {
        "area": "ISO3",
        "category": "IPCC1996_2006_MAR_Inv",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "MAR-GHG-inventory ",
        "provenance": "measured",
        "area": "MAR",
        "scenario": "BUR3",
    }

    coords_value_mapping = {
        "unit": "PRIMAP1",
        "entity": {
            "HFCs (AR4GWP100)": "HFCS (AR4GWP100)",
            "PFCs (AR4GWP100)": "PFCS (AR4GWP100)",
            "COVNM": "NMVOC",
        },
    }

    coords_cols = {"category": "category", "entity": "entity", "unit": "unit"}

    # add_coords_cols = {
    #    "orig_cat_name": ["orig_cat_name", "category"],
    # }

    filter_remove = {
        "f1": {
            "entity": [
                "Other halogenated gases without CO2 equivalent conversion factors (2)"
            ],
        },
    }

    meta_data = {
        "references": "https://unfccc.int/documents/470340",
        "rights": "XXXX",
        "contact": "mail@johannes-guetschow.de",
        "title": "Morocco. Biennial update report (BUR). BUR 3.",
        "comment": "Read fom pdf file by Johannes Gütschow.",
        "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
    }

    ##### read the raw data from pdf #####
    tables = camelot.read_pdf(
        str(input_folder / inventory_file),
        pages=",".join([str(page) for page in pages_to_read]),
        flavor="lattice",
    )

    ##### combine tables and convert to long format #####
    df_all = None
    for year in table_defs.keys():
        current_def = table_defs[year]
        for sector in current_def.keys():
            sector_tables = current_def[sector]
            # print(f"{year}, {sector}")
            df_first = tables[sector_tables[0]].df
            if len(sector_tables) > 1:
                for table in sector_tables[1:]:
                    df_this_table = pd.concat(
                        [df_first, tables[table].df], axis=0, join="outer"
                    )
            else:
                df_this_table = df_first

            # fix the header
            df_this_table = df_this_table.drop(df_this_table.iloc[0:2].index)
            df_this_table.columns = header_defs[sector]

            # fix 2018 agri table
            if (year == 2018) & (sector == "Agriculture"):  # noqa: PLR2004
                last_shift_row = 25
                df_temp = df_this_table.iloc[0:last_shift_row, 1:].copy()
                df_this_table.iloc[0, 1:] = ""
                df_this_table.iloc[1 : last_shift_row + 1, 1:] = df_temp

            # replace line breaks, long hyphens, double, and triple spaces in category
            # names
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("\n", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("   ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("  ", " ")
            df_this_table.iloc[:, 0] = df_this_table.iloc[:, 0].str.replace("-", "-")

            # set index and convert to long format
            df_this_table = df_this_table.set_index(index_cols)
            df_this_table_long = pm2.pm2io.nir_convert_df_to_long(
                df_this_table, year, header_long
            )

            # print(df_this_table_long.head())
            if df_all is None:
                df_all = df_this_table_long
            else:
                df_all = pd.concat([df_all, df_this_table_long], axis=0, join="outer")

    df_all = df_all.reset_index(drop=True)

    ##### conversion to PRIMAP2 interchange format #####
    # drop the rows with memo items etc
    for cat in cats_remove:
        df_all = df_all.drop(df_all[df_all["orig_cat_name"] == cat].index)

    # make a copy of the categories row
    df_all["category"] = df_all["orig_cat_name"]

    # replace cat names by codes in col "category"
    # first the manual replacements
    df_all["category"] = df_all["category"].replace(cat_codes_manual)

    # then the regex replacements
    def repl(m):  # noqa: D103
        return m.group("code")

    df_all["category"] = df_all["category"].str.replace(
        cat_code_regexp, repl, regex=True
    )
    df_all = df_all.reset_index(drop=True)

    # prepare numbers for pd.to_numeric
    df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(" ", "")

    def repl(m):  # noqa: D103
        return m.group("part1") + "." + m.group("part2")

    df_all.loc[:, "data"] = df_all.loc[:, "data"].str.replace(
        "(?P<part1>[0-9]+),(?P<part2>[0-9\\.]+)$", repl, regex=True
    )
    df_all["data"][df_all["data"].isna()] = "NaN"

    # add GWP information to entity
    for entity in df_all["entity"].unique():
        df_all["entity"][
            (df_all["entity"] == entity) & (df_all["unit"] == "GgCO2eq")
        ] = f"{entity} ({gwp_to_use})"

    # drop "original_cat_name" as it has non-unique values per category
    df_all = df_all.drop(columns="orig_cat_name")

    data_if = pm2.pm2io.convert_long_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

    # conversion to PRIMAP2 native format
    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    entities_to_convert = [
        "CO2"
    ]  # ['N2O', 'SF6', 'CO2', 'CH4'] # CO2 is not converted on
    # conversion to IF as data with and without GWP exists. needs to be fixed in primap2
    entities_to_convert = [f"{entity} (AR4GWP100)" for entity in entities_to_convert]

    # convert GWP units to mass units
    for entity in entities_to_convert:
        converted = data_pm2[entity].pr.convert_to_mass()
        basic_entity = entity.split(" ")[0]
        converted = converted.to_dataset(name=basic_entity)
        data_pm2 = data_pm2.pr.merge(converted)
        data_pm2[basic_entity].attrs["entity"] = basic_entity

    # drop the GWP data
    data_pm2 = data_pm2.drop_vars(entities_to_convert)

    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # convert to IPCC2006 categories
    # ###
    data_if_2006 = copy.deepcopy(data_if)
    data_if_2006.attrs = copy.deepcopy(data_if.attrs)

    filter_remove_cats = {
        "cat": {f"category ({coords_terminologies['category']})": remove_cats},
    }

    filter_data(data_if_2006, filter_remove=filter_remove_cats)

    # map categories
    data_if_2006 = data_if_2006.replace(
        {f"category ({coords_terminologies['category']})": cat_mapping}
    )
    data_if_2006[f"category ({coords_terminologies['category']})"].unique()

    # rename the category col
    data_if_2006 = data_if_2006.rename(
        columns={
            f"category ({coords_terminologies['category']})": "category (IPCC2006_PRIMAP)"  # noqa: E501
        }
    )
    data_if_2006.attrs["attrs"]["cat"] = "category (IPCC2006_PRIMAP)"
    data_if_2006.attrs["dimensions"]["*"] = [
        "category (IPCC2006_PRIMAP)"
        if item == f"category ({coords_terminologies['category']})"
        else item
        for item in data_if_2006.attrs["dimensions"]["*"]
    ]
    # aggregate categories
    time_format = "%Y"
    time_columns = [
        col
        for col in data_if_2006.columns.to_numpy()
        if matches_time_format(col, time_format)
    ]

    for cat_to_agg in aggregate_cats:
        mask = data_if_2006["category (IPCC2006_PRIMAP)"].isin(
            aggregate_cats[cat_to_agg]["sources"]
        )
        df_test = data_if_2006[mask]
        # print(df_test)

        if len(df_test) > 0:
            print(f"Aggregating category {cat_to_agg}")
            df_combine = df_test.copy(deep=True)

            for col in time_columns:
                df_combine[col] = pd.to_numeric(df_combine[col], errors="coerce")

            df_combine = df_combine.groupby(
                by=[
                    "source",
                    "scenario (PRIMAP)",
                    "provenance",
                    "area (ISO3)",
                    "entity",
                    "unit",
                ]
            ).sum(min_count=1)

            df_combine.insert(0, "category (IPCC2006_PRIMAP)", cat_to_agg)
            # df_combine.insert(1, "cat_name_translation",
            # aggregate_cats[cat_to_agg]["name"])
            # df_combine.insert(2, "orig_cat_name", "computed")

            df_combine = df_combine.reset_index()

            data_if_2006 = pd.concat([data_if_2006, df_combine], axis=0, join="outer")
            data_if_2006 = data_if_2006.reset_index(drop=True)
        else:
            print(f"no data to aggregate category {cat_to_agg}")

    for cat in zero_cats:
        entities = data_if_2006["entity"].unique()
        data_zero = data_if_2006[
            data_if_2006["category (IPCC2006_PRIMAP)"] == "1"
        ].copy(deep=True)
        data_zero["category (IPCC2006_PRIMAP)"] = cat
        for col in time_columns:
            data_zero[col] = 0

        data_if_2006 = pd.concat([data_if_2006, data_zero])

    # conversion to PRIMAP2 native format
    data_pm2_2006 = pm2.pm2io.from_interchange_format(data_if_2006)

    # convert back to IF to have units in the fixed format
    data_if_2006 = data_pm2_2006.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()

    # data in original categories
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"]), data_if
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder / (output_filename + coords_terminologies["category"] + ".nc"),
        encoding=encoding,
    )

    # data in 2006 categories
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + "IPCC2006_PRIMAP"), data_if_2006
    )

    encoding = {var: compression for var in data_pm2_2006.data_vars}
    data_pm2_2006.pr.to_netcdf(
        output_folder / (output_filename + "IPCC2006_PRIMAP" + ".nc"), encoding=encoding
    )
