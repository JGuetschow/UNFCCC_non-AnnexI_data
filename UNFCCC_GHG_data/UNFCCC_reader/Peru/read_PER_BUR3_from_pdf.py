# read Singapore fifth BUR from pdf


import camelot
import primap2 as pm2
import pandas as pd

import locale

from UNFCCC_GHG_data.helper import process_data_for_country, gas_baskets
from UNFCCC_GHG_data.helper import downloaded_data_path, extracted_data_path
from UNFCCC_GHG_data.helper import fix_rows
from primap2.pm2io._conversion import convert_ipcc_code_primap_to_primap2
from config_PER_BUR3 import table_def_templates, table_defs, index_cols
from config_PER_BUR3 import values_replacement, header_long, cats_remove
from config_PER_BUR3 import cat_codes_manual, cat_code_regexp, cat_names_fix
from config_PER_BUR3 import coords_cols, coords_terminologies, coords_defaults
from config_PER_BUR3 import coords_terminologies_2006
from config_PER_BUR3 import coords_value_mapping, meta_data, filter_remove
from config_PER_BUR3 import processing_info, cat_conversion

### general configuration
input_folder = downloaded_data_path / "UNFCCC" / "Peru" / "BUR3"
output_folder = extracted_data_path / "UNFCCC" / "Peru"
if not output_folder.exists():
    output_folder.mkdir()

output_filename = "PER_BUR3_2023_"
inventory_file_pdf = "Tercer_BUR_Per%C3%BA_Jun2023.pdf"
# years_to_read = range(1990, 2018 + 1)

# define locale to use for str to float conversion
locale_to_use = "es_PE.UTF-8"
locale.setlocale(locale.LC_NUMERIC, locale_to_use)

pagesToRead = table_defs.keys()

compression = dict(zlib=True, complevel=9)

## part 1: read the data from pdf
### part 1.a: 2016 inventory

data_pm2 = None
for page in pagesToRead:
    print(f"++++++++++++++++++++++++++++++++")
    print(f"+++++ Working on page {page} ++++++")
    print(f"++++++++++++++++++++++++++++++++")

    df_this_page = None
    for table_on_page in table_defs[page]["templates"]:
        print(f"Reading table {table_on_page}")
        area = table_def_templates[table_on_page]["area"]
        cols = table_def_templates[table_on_page]["cols"]
        tables = camelot.read_pdf(
            str(input_folder / inventory_file_pdf),
            pages=str(page),
            flavor="stream",
            table_areas=area,
            columns=cols,
        )

        df_current = tables[0].df.copy(deep=True)
        # drop the old header
        if "drop_rows" in table_defs[page].keys():
            df_current = df_current.drop(table_defs[page]["drop_rows"])
        elif "drop_rows" in table_def_templates[table_on_page].keys():
            df_current = df_current.drop(
                table_def_templates[table_on_page]["drop_rows"]
            )
        # add new header
        if "header" in table_defs[page].keys():
            df_current.columns = pd.MultiIndex.from_tuples(
                zip(
                    table_defs[page]["header"]["entity"],
                    table_defs[page]["header"]["unit"],
                )
            )
        else:
            df_current.columns = pd.MultiIndex.from_tuples(
                zip(
                    table_def_templates[table_on_page]["header"]["entity"],
                    table_def_templates[table_on_page]["header"]["unit"],
                )
            )

        # drop cols if necessary
        if "drop_cols" in table_defs[page].keys():
            # print(df_current.columns.values)
            df_current = df_current.drop(columns=table_defs[page]["drop_cols"])
        elif "drop_cols" in table_def_templates[table_on_page].keys():
            df_current = df_current.drop(columns=table_defs[page]["drop_cols"])

        # rename category column
        df_current.rename(
            columns={table_defs[page]["category_col"]: index_cols[0]}, inplace=True
        )

        # replace double \n
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("\n", " ")
        # replace double and triple spaces
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("   ", " ")
        df_current[index_cols[0]] = df_current[index_cols[0]].str.replace("  ", " ")

        # fix the split rows
        for n_rows in table_def_templates[table_on_page]["rows_to_fix"].keys():
            df_current = fix_rows(
                df_current,
                table_def_templates[table_on_page]["rows_to_fix"][n_rows],
                index_cols[0],
                n_rows,
            )

        # replace category names with typos
        df_current[index_cols[0]] = df_current[index_cols[0]].replace(cat_names_fix)

        # replace empty stings
        df_current = df_current.replace(values_replacement)

        # set index
        # df_current = df_current.set_index(index_cols)
        # strip trailing and leading  and remove "^"
        for col in df_current.columns.values:
            df_current[col] = df_current[col].str.strip()
            df_current[col] = df_current[col].str.replace("^", "")

        # print(df_current)
        # aggregate dfs for this page
        if df_this_page is None:
            df_this_page = df_current.copy(deep=True)
        else:
            # find intersecting cols
            cols_this_page = df_this_page.columns.values
            # print(f"cols this page: {cols_this_page}")
            cols_current = df_current.columns.values
            # print(f"cols current: {cols_current}")
            cols_both = list(set(cols_this_page).intersection(set(cols_current)))
            # print(f"cols both: {cols_both}")
            if len(cols_both) > 0:
                df_this_page = df_this_page.merge(
                    df_current, how="outer", on=cols_both, suffixes=(None, None)
                )
            else:
                df_this_page = df_this_page.merge(
                    df_current,
                    how="outer",
                    left_index=True,
                    right_index=True,
                    suffixes=(None, None),
                )

            df_this_page = df_this_page.groupby(index_cols).first().reset_index()
            # print(df_this_page)
            # df_all = df_all.join(df_current, how='outer')

    # set index and convert to long format
    df_this_page = df_this_page.set_index(index_cols)
    df_this_page_long = pm2.pm2io.nir_convert_df_to_long(
        df_this_page, table_defs[page]["year"], header_long
    )

    # drop the rows with memo items etc
    for cat in cats_remove:
        df_this_page_long = df_this_page_long.drop(
            df_this_page_long.loc[df_this_page_long.loc[:, index_cols[0]] == cat].index
        )

    # make a copy of the categories row
    df_this_page_long.loc[:, "category"] = df_this_page_long.loc[:, index_cols[0]]

    # replace cat names by codes in col "Categories"
    # first the manual replacements
    df_this_page_long.loc[:, "category"] = df_this_page_long.loc[:, "category"].replace(
        cat_codes_manual
    )
    # then the regex replacements
    repl = lambda m: convert_ipcc_code_primap_to_primap2("IPC" + m.group("code"))
    df_this_page_long.loc[:, "category"] = df_this_page_long.loc[
        :, "category"
    ].str.replace(cat_code_regexp, repl, regex=True)
    df_this_page_long.loc[:, "category"].unique()

    # strip spaces in data col
    df_this_page_long.loc[:, "data"] = df_this_page_long.loc[:, "data"].str.strip()

    df_this_page_long = df_this_page_long.reset_index(drop=True)

    # make sure all col headers are str
    df_this_page_long.columns = df_this_page_long.columns.map(str)

    # remove thousands separators as pd.to_numeric can't deal with that
    df_this_page_long.loc[:, "data"] = df_this_page_long.loc[:, "data"].str.replace(
        ".", ""
    )
    pat = r"^(?P<first>[0-9\.,]*),(?P<last>[0-9\.,]*)$"
    repl = lambda m: f"{m.group('first')}.{m.group('last')}"
    df_this_page_long.loc[:, "data"] = df_this_page_long.loc[:, "data"].str.replace(
        pat, repl, regex=True
    )

    # df_this_page_long["data"] = df_this_page_long["data"].str.replace("^.$","",
    #                                                                   regex=True)

    # drop orig cat name as it's not unique over all tables (keep until here in case
    # it's needed for debugging)
    df_this_page_long = df_this_page_long.drop(columns="orig_cat_name")

    data_page_if = pm2.pm2io.convert_long_dataframe_if(
        df_this_page_long,
        coords_cols=coords_cols,
        # add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping[
            table_defs[page]["coords_value_mapping"]
        ],
        # coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        # filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True,
        time_format="%Y",
    )

    # conversion to PRIMAP2 native format
    data_page_pm2 = pm2.pm2io.from_interchange_format(data_page_if)

    # combine with tables from other pages
    if data_pm2 is None:
        data_pm2 = data_page_pm2
    else:
        data_pm2 = data_pm2.pr.merge(data_page_pm2)

# convert back to IF to have units in the fixed format
data_if = data_pm2.pr.to_interchange_format()

# ###
# save data to IF and native format
# ###
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw"),
    data_if,
)

encoding = {var: compression for var in data_pm2.data_vars}
data_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies["category"] + "_raw.nc"),
    encoding=encoding,
)

#### continue here

# ###
# ## process the data
# ###
data_proc_pm2 = data_pm2

# actual processing

data_proc_pm2 = process_data_for_country(
    data_proc_pm2,
    entities_to_ignore=[],
    gas_baskets=gas_baskets,
    processing_info_country=processing_info,
    cat_terminology_out=coords_terminologies_2006["category"],
    category_conversion=cat_conversion,
)

# adapt source and metadata
current_source = data_proc_pm2.coords["source"].values[0]
data_temp = data_proc_pm2.pr.loc[{"source": current_source}]
data_proc_pm2 = data_proc_pm2.pr.set("source", "BUR_NIR", data_temp)

# ###
# save data to IF and native format
# ###
data_proc_if = data_proc_pm2.pr.to_interchange_format()
if not output_folder.exists():
    output_folder.mkdir()
pm2.pm2io.write_interchange_format(
    output_folder / (output_filename + coords_terminologies_2006["category"]),
    data_proc_if,
)

encoding = {var: compression for var in data_proc_pm2.data_vars}
data_proc_pm2.pr.to_netcdf(
    output_folder / (output_filename + coords_terminologies_2006["category"] + ".nc"),
    encoding=encoding,
)
