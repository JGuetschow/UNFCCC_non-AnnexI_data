# config and functions for Taiwan NIR 2022

from typing import Union

import pandas as pd

gwp_to_use = "AR4GWP100"

def fix_rows(data: pd.DataFrame, rows_to_fix: list, col_to_use: str, n_rows: int)->pd.DataFrame:
    for row in rows_to_fix:
        #print(row)
        # find the row number and collect the row and the next two rows
        index = data.loc[data[col_to_use] == row].index
        if not list(index):
            print(f"Can't merge split row {row}")
            print(data[col_to_use])
        print(f"Merging split row {row}")
        indices_to_drop = []
        ####print(index)
        for item in index:
            loc = data.index.get_loc(item)
            ####print(data[col_to_use].loc[loc + 1])
            if n_rows == -2:
                locs_to_merge = list(range(loc - 1, loc + 1))
                loc_to_check = loc - 1
            #if n_rows == -3:
            #    locs_to_merge = list(range(loc - 1, loc + 2))
            #elif n_rows == -5:
            #    locs_to_merge = list(range(loc - 1, loc + 4))
            else:
                locs_to_merge = list(range(loc, loc + n_rows))
                loc_to_check = loc + 1

            if data[col_to_use].loc[loc_to_check] == '':
                rows_to_merge = data.iloc[locs_to_merge]
                indices_to_merge = rows_to_merge.index
                # replace numerical NaN values
                ####print(rows_to_merge)
                rows_to_merge = rows_to_merge.fillna('')
                ####print("fillna")
                ####print(rows_to_merge)
                # join the three rows
                new_row = rows_to_merge.agg(' '.join)
                # replace the double spaces that are created
                # must be done here and not at the end as splits are not always
                # the same and join would produce different col values
                new_row = new_row.str.replace("  ", " ")
                new_row = new_row.str.strip()
                #new_row = new_row.str.replace("N O", "NO")
                #new_row = new_row.str.replace(", N", ",N")
                #new_row = new_row.str.replace("- ", "-")
                data.loc[indices_to_merge[0]] = new_row
                indices_to_drop = indices_to_drop + list(indices_to_merge[1:])

        data = data.drop(indices_to_drop)
        data = data.reset_index(drop=True)
    return data

def make_wide_table(data: pd.DataFrame, keyword: str, col: Union[int, str], index_cols: list[Union[int, str]])->pd.DataFrame:
    index = data.loc[data[col] == keyword].index
    if not list(index):
        print("Keyword for table transformation not found")
        return data
    elif len(index)==1:
        print("Keyword for table transformation found only once")
        return data
    else:
        df_all = None
        for i, item in enumerate(index):
            loc = data.index.get_loc(item)
            if i < len(index) - 1:
                next_loc = data.index.get_loc(index[i + 1])
            else:
                next_loc = data.index[-1] + 1
            df_to_add = data.loc[list(range(loc, next_loc))]
            # select only cols which don't have NaN, Null, or '' as header
            filter_nan = ((~df_to_add.iloc[0].isnull()) & (df_to_add.iloc[0] != 'NaN')& (df_to_add.iloc[0] != ''))
            df_to_add = df_to_add.loc[: , filter_nan]
            df_to_add.columns = df_to_add.iloc[0]
            #print(df_to_add.columns)
            df_to_add = df_to_add.drop(loc)
            df_to_add = df_to_add.set_index(index_cols)

            if df_all is None:
                df_all = df_to_add
            else:
                df_all = pd.concat([df_all, df_to_add], axis=1, join='outer')
        return df_all


# page defs tp hold information on reading the table
page_defs = {
    '5': {
        "table_areas": ['36,523,563,68'],
        "split_text": False,
        "flavor": "stream",
    },
    '6': {
        "table_areas": ['34,562,563,53'],
        #"columns": ['195,228,263,295,328,363,395,428,462,495,529'], # works without
        "split_text": True,
        "flavor": "stream",
    },
    '7': {
        "table_areas": ['36,740,499,482', '36,430,564,53'],
        "split_text": True,
        "flavor": "stream",
    },
    '8': {
        "table_areas": ['35,748,503,567'],
        "split_text": True,
        "flavor": "stream",
    },
    '9': {
        "table_areas": ['35,747,565,315', '36,273,565,50'],
        "split_text": False,
        "flavor": "stream",
    },
    '11': {
        "table_areas": ['35,744,563,434'],
        "split_text": True,
        "flavor": "stream",
    },
    '12': {
        "table_areas": ['33,747,562,86'],
        "split_text": True,
        "flavor": "stream",
    },
    '13': {
        "table_areas": ['34,303,564,54'],
        "split_text": True,
        "flavor": "stream",
    },
    '14': {
        "table_areas": ['34,754,564,256'],
        "columns": ['220,251,283,314,344,371,406,438,470,500,530'],
        "split_text": True,
        "flavor": "stream",
    },
    '15': {
        "table_areas": ['34,487,564,42'],
        "split_text": True,
        "flavor": "stream",
    },
    '16': {
        "table_areas": ['34,418,564,125'],
        #"columns": ['107,209,241,273,306,338,369,402,433,466,498,533'],
        "split_text": True,
        "flavor": "lattice",
    }, # with stream the row index is messed up with lattice the column index ... red with lattice and fix col header manualy
    '17': {
        "table_areas": ['34,534,564,49'],
        "columns": ['188,232,263,298,331,362,398,432,464,497,530'],
        "split_text": True,
        "flavor": "stream",
    },
}

# table defs to hold information on how to process the tables
table_defs = {
    'ES2.2': { # 1990-2020 Carbon Dioxide Emissions and Sequestration in Taiwan
        "tables": [1, 2],
        "rows_to_fix": {
            0: {
                3: ['1.A.4.c Agriculture, Forestry, Fishery, and',
                    '2.D Non-Energy Products from Fuels and',
                    '4. Land Use, Land Use Change and Forestry'],
            },
        },
        "index_cols": ['GHG Emission Source and Sinks'],
        "wide_keyword": 'GHG Emission Source and Sinks',
        "col_wide_kwd": 0,
        "entity": "CO2",
        "unit": "kt",
        "cat_codes_manual": {
            'Net GHG Emission (including LULUCF)': '0',
            'Total GHG Emission (excluding LULUCF)': 'M.0.EL',
        },
    },
    'ES2.3': { # 1990-2020 Methane Emissions in Taiwan
        "tables": [3, 4],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "entity": f"CH4 ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total Methane Emissions': '0',
        },
    },
    'ES2.4': { # 1990-2020 Nitrous Oxide Emissions in Taiwan
        "tables": [5],
        "fix_cats": {
            0: {
                "Total Nitrous Oxide Emissionsl": "Total Nitrous Oxide Emissions",
            },
        },
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "entity": f"N2O ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total Nitrous Oxide Emissions': '0',
        },
    },
    'ES3.1': { # 1990-2020 Greenhouse Gas Emission in Taiwan by Sector
        "tables": [7],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Net GHG Emission (including LULUCF)': '0',
            'Total GHG Emission (excluding LULUCF)': 'M.0.EL',
        },
    },
    'ES3.2': { # 1990-2020 Greenhouse Gas Emissions Produced by Energy Sector in Taiwan
        "tables": [8],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "gas_splitting": {
            "Total CO2 Emission": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total Emission from Energy Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total CO2 Emission': '1',
            'Total CH4 Emission': '1',
            'Total N2O Emission': '1',
            'Total Emission from Energy Sector': '1',
        },
    },
    'ES3.3': { # 1990-2020 Greenhouse Gas Emissions Produced by Industrial Process and Product Use Sector (IPPU) in Taiwan
        "tables": [9,10],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "gas_splitting": {
            "Total CO2 Emission": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total HFCs Emission": f"HFCS ({gwp_to_use})",
            "Total PFCs Emission (2.E Electronics Industry)": f"PFCS ({gwp_to_use})",
            "Total SF6 Emission": f"SF6 ({gwp_to_use})",
            "Total NF3 Emission (2.E Electronics Industry)": f"NF3 ({gwp_to_use})",
            "Total Emission from IPPU Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total CO2 Emission': '2',
            'Total CH4 Emission': '2',
            'Total N2O Emission': '2',
            'Total HFCs Emission': '2',
            'Total PFCs Emission (2.E Electronics Industry)': '2.E',
            'Total SF6 Emission': '2',
            'Total NF3 Emission (2.E Electronics Industry)': '2.E',
            'Total Emission from IPPU Sector': '2',
        },
        "drop_rows": [
            ("2.D Non-Energy Products from Fuels and Solvent Use", "CO2"), # has lower significant digits than in table ES2.2
        ]
    },
    'ES3.4': { # 1990-2020 Greenhouse Gas Emissions Produced by Agriculture Sector in Taiwan
        "tables": [11],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        "gas_splitting": {
            "Total CO2 Emission (3.H Urea applied)": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total Emission From Agriculture Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total CO2 Emission (3.H Urea applied)': '3.H',
            'Total CH4 Emission': '3',
            'Total N2O Emission': '3',
            'Total Emission From Agriculture Sector': '3',
        },
    },
    'ES3.6': { # 1990-2020 Greenhouse Gas Emissions in Taiwan by Waste Sector
        "tables": [13],
        "rows_to_fix": {
            0: {
                3: ["Total CO2 Emission"],
            },
        },
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0, # two column header
        "gas_splitting": {
            "Total CO2 Emission (5.C Incineration and Open Burning of Waste)": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total Emission from Waste Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            'Total CO2 Emission (5.C Incineration and Open Burning of Waste)': '5.C',
            'Total CH4 Emission': '5',
            'Total N2O Emission': '5',
            'Total Emission from Waste Sector': '5',
        },
    },
}

table_defs_skip = {
    'ES2.1': { # 1990-2020 Greenhouse Gas Emissions and Sequestration in Taiwan by Type
        "tables": [0],
        "rows_to_fix": {
            0: {
                3: ['CO2'],
            },
            1: {  # wherte col 0 is empty
                3: ['Net GHG Emission', 'Total GHG Emission'],
            },
        },
        "index_cols": ['GHG', 'GWP'],
        "wide_keyword": 'GHG',
        "col_wide_kwd": 0,
        "unit": "ktCO2eq",
    },
    'ES2.5': { # 1990-2020 Fluoride-Containing Gas Emissions in Taiwan
        "tables": [6],
        "rows_to_fix": {
            0: {
                -2: ['Total SF6 Emissions',
                     'Total NF3 Emissions'],
            },
        },
        "index_cols": ['GHG Emission Sources and Sinks'],
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0,
        #"entity": "CO2",
        "unit": "ktCO2eq",
    },
    'ES3.5': { # skip for now: 1990-2020 Changes in Carbon Sequestration by LULUCF Sector in Taiwan2],
        "tables": [12],
        "rows_to_fix": {},
        "index_cols": ['GHG Emission Sources and Sinks'], #header is merged col :-(
        "wide_keyword": 'GHG Emission Sources and Sinks',
        "col_wide_kwd": 0, # two column header
        "unit": "kt",
        "entity": "CO2",
    }, # need to consider the two columns specially (merge?)
}
