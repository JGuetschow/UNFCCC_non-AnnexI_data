"""
Read Saint Kitts and Nevis' BUR1 from pdf
"""
import camelot
import pandas as pd
import primap2 as pm2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Saint_Kitts_and_Nevis.config_kna_bur1 import (
    conf,
    conf_general,
    conf_trend,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    coords_value_mapping,
    country_processing_step1,
    filter_remove,
    fix_values_main,
    fix_values_trend,
    gas_baskets,
    meta_data,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###

    input_folder = downloaded_data_path / "UNFCCC" / "Saint_Kitts_and_Nevis" / "BUR1"
    output_folder = extracted_data_path / "UNFCCC" / "Saint_Kitts_and_Nevis"
    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "First_BUR_St.Kitts_Nevis.pdf"
    output_filename = "KNA_BUR1_2023_"
    compression = dict(zlib=True, complevel=9)

    def repl(m):  # noqa: D103
        return m.group("code")

    # ###
    # 2. Read trend tables
    # ###

    df_trend = None
    for table in conf_trend.keys():
        print("-" * 45)
        print(f"Reading {table} trend table.")
        df_table = None
        for page in conf_trend[table]["page_defs"].keys():
            print(f"Page {page}")
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                # flavor="lattice",
                split_text=True,
                **conf_trend[table]["page_defs"][page]["read_params"],
            )

            df_page = tables_inventory_original[0].df

            skip_rows_start = conf_trend[table]["page_defs"][page]["skip_rows_start"]
            if not skip_rows_start == 0:
                df_page = df_page[skip_rows_start:]

            if df_table is None:
                # Reset index to avoid pandas' SettingWithCopyWarning
                df_table = df_page.reset_index(drop=True)
            else:
                df_table = pd.concat(
                    [
                        df_table,
                        df_page,
                    ],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

        # fix content that spreads across multiple rows
        if "rows_to_fix" in conf_trend[table]:
            for n_rows in conf_trend[table]["rows_to_fix"].keys():
                print(f"Merge content for {n_rows=}")
                df_table = fix_rows(
                    df_table,
                    rows_to_fix=conf_trend[table]["rows_to_fix"][n_rows],
                    col_to_use=0,
                    n_rows=n_rows,
                )

        df_table.columns = (
            conf_trend[table]["header"]
            + conf_trend[table]["years"]
            + conf_trend[table]["extra_columns"]
        )

        # drop columns if needed
        if "drop_cols" in conf_trend[table].keys():
            df_table = df_table.drop(columns=conf_trend[table]["drop_cols"])

        # category codes from category names
        df_table["category"] = df_table["orig_category"]
        # Remove line break characters
        df_table["category"] = df_table["category"].str.replace("\n", " ")
        # first the manual replacements
        if "cat_codes_manual" in conf_trend[table].keys():
            df_table["category"] = df_table["category"].replace(
                conf_trend[table]["cat_codes_manual"]
            )
        # remove dots from category codes
        df_table["category"] = df_table["category"].str.replace(".", "")
        # then the regex replacements
        df_table["category"] = df_table["category"].str.replace(
            conf_general["cat_code_regexp"], repl, regex=True
        )

        df_table = df_table.drop(columns="orig_category")

        # drop rows if needed
        if "rows_to_drop" in conf_trend[table].keys():
            for row in conf_trend[table]["rows_to_drop"]:
                row_to_delete = df_table.index[df_table["category"] == row][0]
                df_table = df_table.drop(index=row_to_delete)

        # clean values
        for year in conf_trend[table]["years"]:
            if "replace_data_entries" in conf_trend[table].keys():
                df_table[year] = df_table[year].replace(
                    conf_trend[table]["replace_data_entries"]
                )
            df_table[year] = df_table[year].str.replace("\n", "")
            df_table[year] = df_table[year].str.replace(",", ".")
            # invisible numbers in trend table on page 112
            if "split_values" in conf_trend[table].keys():
                cat = conf_trend[table]["split_values"]["cat"]
                keep_value_no = conf_trend[table]["split_values"]["keep_value_no"]
                new_value = (
                    df_table.loc[df_table["category"] == cat, year]
                    .item()
                    .split(" ")[keep_value_no]
                )
                df_table.loc[df_table["category"] == cat, year] = new_value

        if "fix_single_value" in conf_trend[table].keys():
            cat = conf_trend[table]["fix_single_value"]["cat"]
            year = conf_trend[table]["fix_single_value"]["year"]
            new_value = conf_trend[table]["fix_single_value"]["new_value"]
            df_table.loc[df_table["category"] == cat, year] = new_value

        df_table["unit"] = conf_trend[table]["unit"]
        df_table["entity"] = conf_trend[table]["entity"]

        # stack the tables vertically
        if df_trend is None:
            df_trend = df_table.reset_index(drop=True)
        else:
            df_trend = pd.concat(
                [
                    df_trend,
                    df_table,
                ],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

    # some categories present in main and detailled tables
    df_trend = df_trend.drop_duplicates()

    for cat, year, new_value in fix_values_trend:
        # make sure there is exactly one value that matches the filter
        # TODO ruff wants to remove the assert statements here
        assert len(df_trend.loc[df_trend["category"] == cat, year]) == 1  # noqa: S101
        df_trend.loc[df_trend["category"] == cat, year] = new_value

    df_trend_if = pm2.pm2io.convert_wide_dataframe_if(
        df_trend,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
    )
    #
    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_trend_pm2 = pm2.pm2io.from_interchange_format(df_trend_if)

    # ###
    # 1. Read in main tables
    # ###

    df_main = None
    for sector in reversed(conf.keys()):
        print("-" * 45)
        print(f"Reading table for {sector}.")

        df_sector = None
        for page in conf[sector]["page_defs"].keys():
            print(f"Page {page}")
            tables_inventory_original = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=page,
                flavor="lattice",
                # split_text=True,
            )

            df_page = tables_inventory_original[0].df

            skip_rows_start = conf[sector]["page_defs"][page]["skip_rows_start"]
            if not skip_rows_start == 0:
                df_page = df_page[skip_rows_start:]

            if df_sector is None:
                # Reset index to avoid pandas' SettingWithCopyWarning
                df_sector = df_page.reset_index(drop=True)
            else:
                df_sector = pd.concat(
                    [
                        df_sector,
                        df_page,
                    ],
                    axis=0,
                    join="outer",
                ).reset_index(drop=True)

        df_sector.columns = conf[sector]["header"] + conf[sector]["entities"]

        df_sector["category"] = df_sector["orig_category"]

        # Remove line break characters
        df_sector["category"] = df_sector["category"].str.replace("\n", " ")

        # first the manual replacements
        df_sector["category"] = df_sector["category"].replace(
            conf[sector]["cat_codes_manual"]
        )

        # remove dots from category codes
        df_sector["category"] = df_sector["category"].str.replace(".", "")

        # then the regex replacements
        df_sector["category"] = df_sector["category"].str.replace(
            conf_general["cat_code_regexp"], repl, regex=True
        )

        df_sector = df_sector.drop(columns="orig_category")

        # bring in long format, so it can be concatenated with other tables
        df_sector = pd.melt(
            df_sector,
            id_vars="category",
            value_vars=conf[sector]["entities"],
        )

        # pd.melt always outputs value and variable as column names
        df_sector = df_sector.rename({"value": "data", "variable": "entity"}, axis=1)

        # clean data column
        df_sector["data"] = df_sector["data"].replace(
            conf[sector]["replace_data_entries"]
        )
        df_sector["data"] = df_sector["data"].str.replace(",", ".")
        df_sector["data"] = df_sector["data"].str.replace("\n", "")

        df_sector["unit"] = df_sector["entity"].replace(conf[sector]["unit_mapping"])

        if df_main is None:
            df_main = df_sector
        else:
            df_main = pd.concat(
                [
                    df_sector,
                    df_main,
                ],
                axis=0,
                join="outer",
            ).reset_index(drop=True)

        # break

    # year is the same for all sector tables
    df_main["time"] = "2018"

    # fix values
    for cat, ent, new_value in fix_values_main:
        # Make sure value to replace is found in data frame
        # TODO ruff wants to remove the assert statements here
        assert (  # noqa: S101
            len(
                df_main.loc[
                    (df_main["category"] == cat) & (df_main["entity"] == ent), "data"
                ]
            )
            == 1
        )
        df_main.loc[
            (df_main["category"] == cat) & (df_main["entity"] == ent), "data"
        ] = new_value

    ### convert to interchange format ###
    print("Converting to interchange format.")
    df_main_IF = pm2.pm2io.convert_long_dataframe_if(
        df_main,
        coords_cols=coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        filter_remove=filter_remove,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    ### convert to primap2 format ###
    print("Converting to primap2 format.")
    data_main_pm2 = pm2.pm2io.from_interchange_format(df_main_IF)

    # # ###
    # # Merge tables.
    # # ###

    print("Merging main and trend table.")
    data_pm2 = data_main_pm2.pr.merge(data_trend_pm2, tolerance=1)

    # # ###
    # # Save raw data to IF and native format.
    # # ###

    data_if = data_pm2.pr.to_interchange_format()

    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
        data_if,
    )

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(
        output_folder
        / (output_filename + coords_terminologies["category"] + "_raw.nc"),
        encoding=encoding,
    )

    # # ###
    # # Processing
    # # ###

    # create the gas baskets before aggregating the categories
    data_proc_pm2 = process_data_for_country(
        data_country=data_pm2,
        entities_to_ignore=[],
        gas_baskets=gas_baskets,
        filter_dims=None,
        cat_terminology_out=None,
        category_conversion=None,
        sectors_out=None,
        processing_info_country=country_processing_step1,
    )

    # # ###
    # # save processed data to IF and native format
    # # ###

    terminology_proc = coords_terminologies["category"]

    data_proc_if = data_proc_pm2.pr.to_interchange_format()

    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(
        output_folder / (output_filename + terminology_proc), data_proc_if
    )

    encoding = {var: compression for var in data_proc_pm2.data_vars}
    data_proc_pm2.pr.to_netcdf(
        output_folder / (output_filename + terminology_proc + ".nc"), encoding=encoding
    )

    print("Saved processed data.")
