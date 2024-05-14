"""
Read Montenegro's BUR3 from pdf

This script reads data from Montenegro's BUR3
Data are read from pdf using camelot

"""


# ###
# imports
# ###
import copy
import re

import camelot
import pandas as pd
import primap2 as pm2
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path

from .config_mne_bur3 import aggregate_cats, cat_mapping, drop_data

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Montenegro" / "BUR3"
    output_folder = extracted_data_path / "UNFCCC" / "Montenegro"
    output_filename = "MNE_BUR3_2022_"
    compression = dict(zlib=True, complevel=9)

    inventory_file_pdf = "NIR-2021_MNE_Finalversion.pdf"

    # reading and processing
    years_to_read = range(1990, 2018 + 1)
    pages_to_read = range(535, 583)

    pos_entity = [0, 0]
    cat_code_col = 0
    cat_name_col = 1
    regex_unit = r"\((.*)\)"
    regex_entity = r"^(.*)\s\("

    gwp_to_use = "AR4GWP100"

    # conversion to PRIMAP2 format

    coords_terminologies = {
        "area": "ISO3",
        "category": "IPCC1996_2006_MNE_Inv",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "MNE-GHG-inventory ",
        "provenance": "measured",
        "area": "MNE",
        "scenario": "BUR3",
    }

    coords_value_mapping = {
        "unit": "PRIMAP1",
        "entity": {
            f"GHG ({gwp_to_use})": f"KYOTOGHG ({gwp_to_use})",
            f"HFC ({gwp_to_use})": f"HFCS ({gwp_to_use})",
            f"PFC ({gwp_to_use})": f"PFCS ({gwp_to_use})",
        },
        "category": {
            "Total national GHG emissions (with LULUCF)": "0",
            "Total national GHG emissions (without LULUCF)": "M.0.EL",
            "International Bunkers": "M.BK",
            "1.A.3.a.i": "M.BK.A",
            "1.A.3.d.i": "M.BK.M",
            "CO2 from Biomass Combustion for Energy Production": "M.BIO",
            "6 Other": "6",
            "2 H": "2.H",
        },
    }

    coords_value_filling = {
        "category": {
            "orig_cat_name": {
                "International Bunkers": "M.BK",
            },
        },
    }

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
    }

    filter_remove = {
        "f1": {
            "category": ["Memo items"],
        },
    }

    meta_data = {
        "references": "https://unfccc.int/documents/461972",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "title": "Montenegro. Biennial update report (BUR). "
        "BUR 3. National inventory report.",
        "comment": "Read fom pdf file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
    }

    # ###
    # Read all time series table from pdf
    # ###
    tables = camelot.read_pdf(
        str(input_folder / inventory_file_pdf),
        pages=",".join([str(page) for page in pages_to_read]),
        flavor="lattice",
    )

    # ###
    # process tables and combine them using the pm2 pr.merge function
    # ###
    data_all = None
    for i, table in enumerate(tables):
        df_current_table = table.df.copy(deep=True)
        # get entity and unit
        entity_unit = df_current_table.iloc[0, 0]
        match = re.search(regex_unit, entity_unit)
        unit = match.group(1)
        match = re.search(regex_entity, entity_unit)
        entity = match.group(1)
        if "CO2 equivalent" in unit:
            entity = f"{entity} ({gwp_to_use})"
            unit_parts = unit.split(" ")
            unit = f"{unit_parts[0]} CO2eq"

        # remove "/n" from category code and name columns
        df_current_table.iloc[:, 0] = df_current_table.iloc[:, 0].str.replace("\n", "")
        df_current_table.iloc[:, 1] = df_current_table.iloc[:, 1].str.replace("\n", "")

        # fix header
        df_current_table.iloc[0, 0] = "category"
        df_current_table.iloc[0, 1] = "orig_cat_name"
        df_current_table.columns = df_current_table.iloc[0]
        df_current_table = df_current_table.drop(0, axis=0)

        # remove ',' in numbers
        years = df_current_table.columns[2:]

        def repl(m):  # noqa: D103
            return m.group("part1") + m.group("part2")

        for year in years:
            df_current_table.loc[:, year] = df_current_table.loc[:, year].str.replace(
                "(?P<part1>[0-9]+),(?P<part2>[0-9\\.]+)$", repl, regex=True
            )

        # add entity and unit cols
        df_current_table["entity"] = entity
        df_current_table["unit"] = unit

        if i in drop_data:
            to_drop = drop_data[i]
            if "cats" in to_drop.keys():
                mask = df_current_table["category"].isin(to_drop["cats"])
                df_current_table = df_current_table.drop(
                    df_current_table[mask].index, axis=0
                )
            if "years" in to_drop.keys():
                df_current_table = df_current_table.drop(columns=to_drop["years"])

        df_current_table["category"] = df_current_table["category"].fillna(
            value=df_current_table["orig_cat_name"]
        )

        df_current_table = df_current_table.drop(columns="orig_cat_name")

        df_current_table_IF = pm2.pm2io.convert_wide_dataframe_if(
            df_current_table,
            coords_cols=coords_cols,
            coords_defaults=coords_defaults,
            coords_terminologies=coords_terminologies,
            coords_value_mapping=coords_value_mapping,
            filter_remove=filter_remove,
            meta_data=meta_data,
            convert_str=True,
        )

        current_table_pm2 = pm2.pm2io.from_interchange_format(df_current_table_IF)

        if data_all is None:
            data_all = current_table_pm2
        else:
            data_all = data_all.pr.merge(current_table_pm2, tolerance=0.001)

        print(f"{entity}, {unit}: {years[0]}-{years[-1]}")

    # ###
    # postprocessing
    # ###

    # convert to mass units from CO2eq
    entities_to_convert = ["N2O", "SF6", "CH4"]
    entities_to_convert = [f"{entity} ({gwp_to_use})" for entity in entities_to_convert]

    # for entity in entities_to_convert:
    #     converted = data_all[entity].pr.convert_to_mass()
    #     basic_entity = entity.split(" ")[0]
    #     converted = converted.to_dataset(name=basic_entity)
    #     data_all = data_all.pr.merge(converted)
    #     data_all[basic_entity].attrs["entity"] = basic_entity
    #
    # # drop the GWP data
    # data_all = data_all.drop_vars(entities_to_convert)

    # convert back to IF
    data_if = data_all.pr.to_interchange_format()

    # ###
    # convert to IPCC2006 categories
    # ###
    data_if_2006 = copy.deepcopy(data_if)
    data_if_2006.attrs = copy.deepcopy(data_if.attrs)

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
    for cat_to_agg in aggregate_cats:
        mask = data_if_2006["category (IPCC2006_PRIMAP)"].isin(
            aggregate_cats[cat_to_agg]["sources"]
        )
        df_test = data_if_2006[mask]
        # print(df_test)

        if len(df_test) > 0:
            print(f"Aggregating category {cat_to_agg}")
            df_combine = df_test.copy(deep=True)

            time_format = "%Y"
            time_columns = [
                col
                for col in df_combine.columns.to_numpy()
                if matches_time_format(col, time_format)
            ]

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

    encoding = {var: compression for var in data_all.data_vars}
    data_all.pr.to_netcdf(
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
