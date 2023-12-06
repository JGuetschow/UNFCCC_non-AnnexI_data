# this script reads data from Colombia's BUR3
# Data is read from the xlsx file which has been exported from the google docs
# spreadsheet which is linked in the BUR

import pandas as pd
import primap2 as pm2
from primap2.pm2io._data_reading import matches_time_format

from unfccc_ghg_data.helper import downloaded_data_path, extracted_data_path

# TODO: add fgases, sector summing (proc version)

if __name__ == "__main__":
    # ###
    # configuration
    # ###
    input_folder = downloaded_data_path / 'UNFCCC' / 'Colombia' / 'BUR3'
    output_folder = extracted_data_path / 'UNFCCC' / 'Colombia'
    if not output_folder.exists():
        output_folder.mkdir()

    output_filename = 'COL_BUR3_2022_'

    inventory_file = 'TR_1990-2018_BUR3-AR5_VF.xlsx'
    years_to_read = range(1990, 2018 + 1)

    sheet_to_read = 'TR 1990-2018'
    cols_to_read = range(0, 47)

    compression = dict(zlib=True, complevel=9)

    unit_row = 0

    coords_cols = {
        "category": "category",
        "entity": "entity",
        "unit": "unit",
    }


    coords_terminologies = {
        "area": "ISO3",
        "category": "IPCC2006",
        "scenario": "PRIMAP",
    }

    coords_defaults = {
        "source": "COL-GHG-Inventory",
        "provenance": "measured",
        "area": "COL",
        "scenario": "BUR3",
    }

    coords_value_mapping = {
        "unit": "PRIMAP1",
        "entity": {
            'Absorciones CO2': 'CO2 Absorptions',
            'Emisiones CO2': 'CO2 Emissions',
            'Emisiones netas (AR5GWP100)': 'KYOTOGHG (AR5GWP100)',
            'HFC-23': 'HFC23',
            'HFC-32': 'HFC32',
            #'HFC-41': 'HFC41',
            'HFC-43-10mee': 'HFC4310mee',
            'HFC-125': 'HFC125',
            #'HFC-134': 'HFC134',
            'HFC-134a': 'HFC134a',
            'HFC-152a': 'HFC152a',
            #'HFC-143': 'HFC143',
            'HFC-143a': 'HFC143a',
            'HFC-227ea': 'HFC227ea',
            'HFC-236fa': 'HFC236fa',
            #'HFC-245ca': 'HFC245ca',
            'HFC-245fa': 'HFC245fa',
            'HFC-365mfc': 'HFC365mfc',
            'PFC-116': 'C2F6',
            'PFC-14': 'CF4',
        },
    }


    filter_remove = {
        "fGWP": {
            "entity": [
                'Absorciones CO2 (AR5GWP100)',
                'Absorciones totales (AR5GWP100)',
                'CH4 (AR5GWP100)',
                'Emisiones CO2 (AR5GWP100)',
                'Total emisiones (AR5GWP100)',
                'HFC-125 (AR5GWP100)',
                'HFC-134a (AR5GWP100)',
                'HFC-143a (AR5GWP100)',
                'HFC-152a (AR5GWP100)',
                'HFC-227ea (AR5GWP100)',
                'HFC-23 (AR5GWP100)',
                'HFC-236fa (AR5GWP100)',
                'HFC-245fa (AR5GWP100)',
                'HFC-32 (AR5GWP100)',
                'HFC-365mfc (AR5GWP100)',
                'HFC-43-10mee (AR5GWP100)',
                'N2O (AR5GWP100)',
                'PFC-116 (AR5GWP100)',
                'PFC-14 (AR5GWP100)',
                'SF6 (AR5GWP100)',
            ],
        },
    }

    filter_keep = {}

    meta_data = {
        "references": "https://unfccc.int/documents/424157",
        "rights": "",
        "contact": "mail@johannes-guestchow.de",
        "title": "Colombia. Biennial update report (BUR). BUR3",
        "comment": "Read fom xlsx file (exported from google docs) by Johannes Gütschow",
        "institution": "UNFCCC",
    }


    # read the data
    data_raw = pd.read_excel(input_folder / inventory_file, sheet_name=sheet_to_read,
                             skiprows=0, nrows=15025, usecols=cols_to_read,
                             engine="openpyxl", header=None)

    # fill the units to the right as for merged cells the unit is only in the first cell
    data_raw.iloc[unit_row] = data_raw.iloc[unit_row].fillna(axis=0, method="ffill")
    merge_rows = [1, 2]
    for row in merge_rows:
        data_raw.iloc[row] = data_raw.iloc[row].astype(str).str.replace("nan", "")
    data_raw.iloc[merge_rows[0]] = (
    data_raw.iloc[merge_rows[0]].astype(str) + " " + data_raw.iloc[
            merge_rows[1]].astype(str))
    data_raw.iloc[merge_rows[0]] = data_raw.iloc[merge_rows[0]].str.strip()
    data_raw = data_raw.drop(index=data_raw.index[merge_rows[1]])

    # merge the category cols
    def join_code_parts(series):
        code = series.iloc[0]
        for part in series.iloc[1:]:
            if part != "nan":
                code = code + "." + part
        if code == "nan":
            code = "0"
        return code

    cat_columns = [0, 1, 2, 3, 4, 5] # xlsx cols are ["MOD","CAP","CAT","SCAT","NROM",
    # "NUM"]
    data_raw["category"] = data_raw[cat_columns].astype(str).agg(func=join_code_parts,
                                                                 axis=1)
    data_raw = data_raw.drop(columns=cat_columns)

    # prepare the dataframe for processig with primap2 functions
    col_index = pd.MultiIndex.from_tuples(zip(data_raw.iloc[0], data_raw.iloc[1]))
    data_raw.columns = col_index
    data_raw = data_raw.drop(index=data_raw.index[0:2])

    data_raw = data_raw.set_index("MOD.CAP.CAT.SCAT.NROM.NUM")

    # loop over years to use pm2 stack operation
    years = data_raw["ANO"].unique()
    df_all = None
    for year in years:
        data_year = data_raw[data_raw["ANO"] == year]
        data_year = data_year.drop(columns=["ANO", "Categorías de fuente y sumideros"])
        df_long_new = pm2.pm2io.nir_convert_df_to_long(data_year, year,
                                                       ["category", "unit", "entity",
                                                        "time", "data"])
        if df_all is None:
            df_all = df_long_new
        else:
            df_all = pd.concat([df_all, df_long_new], axis=0, join='outer')

    df_all["category"] = df_all["category"].str[0]

    # map units
    df_all["unit"] = df_all["unit"].replace({
        'GEI DIRECTOS - Gg ': 'Gg',
        'GEI DIRECTOS - Gg CO2 equivalente': 'GgCO2eq',
    }
    )

    # add GWP information to entity
    for entity in df_all["entity"].unique():
        df_all["entity"][(df_all["entity"] == entity) & (
                    df_all["unit"] == "GgCO2eq")] = f"{entity} (AR5GWP100)"

    # reset index before conversion to pm2 IF
    df_all = df_all.reset_index(drop=True)

    # make sure all col headers are str
    df_all.columns = df_all.columns.map(str)

    # ###
    # convert to PRIMAP2 interchange format
    # ###
    data_if = pm2.pm2io.convert_long_dataframe_if(
        df_all,
        coords_cols=coords_cols,
        #add_coords_cols=add_coords_cols,
        coords_defaults=coords_defaults,
        coords_terminologies=coords_terminologies,
        coords_value_mapping=coords_value_mapping,
        #coords_value_filling=coords_value_filling,
        filter_remove=filter_remove,
        #filter_keep=filter_keep,
        meta_data=meta_data,
        convert_str=True
        )


    # combine CO2 emissions and absorptions
    data_CO2 = data_if[data_if["entity"].isin([
        'CO2 Absorptions', 'CO2 Emissions'])]

    time_format = '%Y'
    time_columns = [
        col
        for col in data_CO2.columns.values
        if matches_time_format(col, time_format)
    ]

    for col in time_columns:
        data_CO2[col] = pd.to_numeric(data_CO2[col], errors="coerce")

    data_CO2 = data_CO2.groupby(
        by=['source', 'scenario (PRIMAP)', 'provenance', 'area (ISO3)',
            f"category ({coords_terminologies['category']})",
            'unit']).sum(min_count = 1)

    data_CO2.insert(0, 'entity', 'CO2')
    data_CO2 = data_CO2.reset_index()

    data_if = pd.concat([data_if, data_CO2])



    data_pm2 = pm2.pm2io.from_interchange_format(data_if)


    # convert back to IF to have units in the fixed format
    data_if = data_pm2.pr.to_interchange_format()

    # ###
    # save data to IF and native format
    # ###
    if not output_folder.exists():
        output_folder.mkdir()
    pm2.pm2io.write_interchange_format(output_folder / (output_filename + coords_terminologies["category"]), data_if)

    encoding = {var: compression for var in data_pm2.data_vars}
    data_pm2.pr.to_netcdf(output_folder / (output_filename + coords_terminologies["category"] + ".nc"), encoding=encoding)
