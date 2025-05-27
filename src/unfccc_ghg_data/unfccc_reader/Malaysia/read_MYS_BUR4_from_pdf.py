"""
Read Malaysia's BUR3 from pdf

This script reads data from Malaysia's BUR3
Data are read from pdf using camelot

Code ist mostly identical to BUR3
"""

import camelot
import primap2 as pm2
from primap2.pm2io._conversion import convert_ipcc_code_primap_to_primap2

from unfccc_ghg_data.helper import (
    downloaded_data_path,
    extracted_data_path,
    fix_rows,
    process_data_for_country,
)
from unfccc_ghg_data.unfccc_reader.Malaysia.config_mys_bur4 import (
    cat_code_regexp,
    cat_codes_manual,
    cat_names_fix,
    cats_remove,
    cols_for_space_stripping,
    coords_cols,
    coords_defaults,
    coords_terminologies,
    country_processing_step1,
    gas_baskets,
    index_cols,
    meta_data,
    table_def_templates,
    table_defs,
    terminology_proc,
    values_replacement,
)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / "UNFCCC" / "Malaysia" / "BUR4"
    output_folder = extracted_data_path / "UNFCCC" / "Malaysia"
    if not output_folder.exists():
        output_folder.mkdir()

    pdf_file = "MY_BUR4_2022.pdf"
    pdf_pages = range(203, 267)
    # CO2: 203 - 218
    # CH4: 219 - 230
    # N2O: 231 - 2242
    # HFCS: 243 - 248
    # PFCs: 249 - 254
    # SF6: 255 - 260
    # NF3: 261 - 266

    output_filename = "MYS_BUR4_2022_"
    compression = dict(zlib=True, complevel=9)

    # ###
    # reading data and aggregation into one dataframe
    # ###
    df_all = None
    for page in pdf_pages:
        print("++++++++++++++++++++++++++++++++")
        print(f"+++++ Working on page {page} ++++++")
        print("++++++++++++++++++++++++++++++++")
        page_template_nr = table_defs[str(page)]["template"]
        area = table_def_templates[page_template_nr]["area"]
        if "cols" in table_def_templates[page_template_nr].keys():
            cols = table_def_templates[page_template_nr]["cols"]
            tables = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=str(page),
                flavor="stream",
                table_areas=area,
                columns=cols,
                split_text=True,
            )
        else:
            tables = camelot.read_pdf(
                str(input_folder / pdf_file),
                pages=str(page),
                flavor="stream",
                table_areas=area,
            )

        df_current = tables[0].df.copy()
        df_current.iloc[0, 0] = "Categories"
        df_current.columns = df_current.iloc[0]
        df_current = df_current.drop(0)
        # replace double \n
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("\n", " ")
        # replace double and triple spaces
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("   ", " ")
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("  ", " ")

        # fix the split rows
        if "rows_to_fix" in table_def_templates[page_template_nr].keys():
            for n_rows in table_def_templates[page_template_nr]["rows_to_fix"].keys():
                df_current = fix_rows(
                    df_current,
                    table_def_templates[page_template_nr]["rows_to_fix"][n_rows],
                    index_cols[0],
                    n_rows,
                )

        # replace category names with typos
        df_current[index_cols[0]] = df_current[index_cols[0]].replace(cat_names_fix)

        # replace empty stings
        df_current = df_current.replace(values_replacement)

        # add entity and unit information
        df_current.insert(1, "unit", table_defs[str(page)]["unit"])
        df_current.insert(1, "entity", table_defs[str(page)]["entity"])

        # set index
        # df_current = df_current.set_index(index_cols)
        # strip trailing and leading spaces
        for col in cols_for_space_stripping:
            df_current[col] = df_current[col].str.strip()

        # print(df_current.columns.to_numpy())

        # aggregate dfs
        if df_all is None:
            df_all = df_current
        else:
            # find intersecting cols
            cols_all = df_all.columns.to_numpy()
            cols_current = df_current.columns.to_numpy()
            cols_both = list(set(cols_all).intersection(set(cols_current)))
            # print(cols_both)
            if len(cols_both) > 0:
                df_all = df_all.merge(
                    df_current, how="outer", on=cols_both, suffixes=(None, None)
                )
            else:
                df_all = df_all.merge(df_current, how="outer", suffixes=(None, None))
            df_all = df_all.groupby(index_cols).first().reset_index()
            # df_all = df_all.join(df_current, how='outer')

    # ###
    # conversion to primap2 interchange format
    # ###
    # drop the rows with memo items etc
    for cat in cats_remove:
        df_all = df_all.drop(df_all[df_all["Categories"] == cat].index)
    # make a copy of the categories row
    df_all["orig_cat_name"] = df_all["Categories"]

    # replace cat names by codes in col "Categories"
    # first the manual replacements
    df_all["Categories"] = df_all["Categories"].replace(cat_codes_manual)

    # then the regex repalcements
    def repl(m):  # noqa: D103
        return convert_ipcc_code_primap_to_primap2("IPC" + m.group("code"))

    df_all["Categories"] = df_all["Categories"].str.replace(
        cat_code_regexp, repl, regex=True
    )

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

    # remove thousands separators as pd.to_numeric can't deal with that
    # also replace None with NaN
    year_cols = list(
        set(df_all.columns) - set(["Categories", "entity", "unit", "orig_cat_name"])
    )
    for col in year_cols:
        df_all.loc[:, col] = df_all.loc[:, col].str.strip()

        def repl(m):  # noqa: D103
            return m.group("part1") + m.group("part2")

        df_all.loc[:, col] = df_all.loc[:, col].str.replace(
            "(?P<part1>[0-9]+),(?P<part2>[0-9\\.]+)$", repl, regex=True
        )
        df_all[col][df_all[col].isna()] = "NaN"
        # manually map code NENO to nan
        df_all.loc[:, col] = df_all.loc[:, col].str.replace("NENO", "NaN")
        df_all.loc[:, col] = df_all.loc[:, col].str.replace("O NANaN", "NaN")
        df_all.loc[:, col] = df_all.loc[:, col].str.replace("IE NO", "0")
        df_all.loc[:, col] = df_all.loc[:, col].str.replace("IE NA NO I", "0")
        # TODO: add code to PRIMAP2

    # drop orig_cat_name as it's non-unique per category
    df_all = df_all.drop(columns=["orig_cat_name"])

    data_if = pm2.pm2io.convert_wide_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        # coords_value_mapping=coords_value_mapping,
        # coords_value_filling=coords_value_filling,
        # filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    data_pm2 = pm2.pm2io.from_interchange_format(data_if)

    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save raw data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
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

    # ###
    # ## process the data
    # ###
    data_proc_pm2 = data_pm2

    # actual processing
    data_proc_pm2 = process_data_for_country(
        data_proc_pm2,
        gas_baskets=gas_baskets,
        entities_to_ignore=[],
        processing_info_country=country_processing_step1,
    )

    # adapt source and metadata
    current_source = data_proc_pm2.coords["source"].to_numpy()[0]
    data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
    data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)

    # ###
    # save data to IF and native format
    # ###
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
