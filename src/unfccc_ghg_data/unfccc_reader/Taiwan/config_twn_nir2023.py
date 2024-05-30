"""
Configuration and custom functions for Taiwan's 2023 NIR
"""

gwp_to_use = "AR4GWP100"
terminology_proc = "IPCC2006_PRIMAP"

##### Table definitions
# page defs to hold information on reading the table
page_defs = {
    "5": {
        "table_areas": ["36,523,563,68"],
        "split_text": False,
        "flavor": "stream",
    },
    "6": {
        "table_areas": ["34,562,563,53"],
        # "columns": ['195,228,263,295,328,363,395,428,462,495,529'], # works without
        "split_text": True,
        "flavor": "stream",
    },
    "7": {
        "table_areas": ["36,743,531,482", "36,425,564,54"],
        "split_text": True,
        "flavor": "stream",
    },
    "8": {
        "table_areas": ["35,748,534,567"],
        "split_text": True,
        "flavor": "stream",
    },
    "9": {
        "table_areas": ["34,753,565,286", "34,235,565,63"],
        "split_text": False,
        "flavor": "stream",
    },
    "10": {
        "table_areas": ["34,753,565,449"],
        "split_text": False,
        "flavor": "stream",
    },
    "11": {
        "table_areas": ["32,522,566,208"],
        "split_text": True,
        "flavor": "stream",
    },
    "12": {
        "table_areas": ["33,549,562,64"],
        "split_text": True,
        "flavor": "stream",
    },
    "13": {
        "table_areas": ["31,761,532,517"],
        "split_text": True,
        "flavor": "stream",
    },
    "14": {
        "table_areas": ["32,751,563,70"],
        "columns": ["217,250,282,313,344,374,406,437,468,501,531"],
        "split_text": True,
        "flavor": "stream",
    },
    "15": {
        "table_areas": ["32,345,565,53"],
        "split_text": True,
        "flavor": "stream",
    },
    "16": {
        "table_areas": ["32,745,532,597"],
        "split_text": True,
        "flavor": "stream",
    },
    "18": {
        "table_areas": ["30,747,564,260"],
        "columns": ["188,232,263,298,331,362,398,432,464,497,530"],
        "split_text": True,
        "flavor": "stream",
    },  # correct mistakes later
}

# table defs to hold information on how to process the tables
table_defs = {
    "ES2.2": {  # 1990-2021 Carbon Dioxide Emissions and Sequestration in Taiwan
        "tables": [1, 2],
        "rows_to_fix": {
            0: {
                3: [
                    "1.A.4.c Agriculture, Forestry, Fishery, and",
                    "2.D Non-Energy Products from Fuels and",
                    "4. Land Use, Land Use Change and Forestry",
                ],
            },
        },
        "index_cols": ["GHG Emission Source and Sinks"],
        "wide_keyword": "GHG Emission Source and Sinks",
        "col_wide_kwd": 0,
        "entity": "CO2",
        "unit": "kt",
        "cat_codes_manual": {
            "Net GHG Emission (including LULUCF)": "0",
            "Total GHG Emission (excluding LULUCF)": "M.0.EL",
        },
    },
    "ES2.3": {  # 1990-2021 Methane Emissions in Taiwan
        "tables": [3, 4],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        "entity": f"CH4 ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Total Methane Emissions": "0",
        },
        "drop_rows": [
            "5.B Garbage Biological Treatment",  # has lower significant digits than in table ES3.6
            "2. Industrial Process and Product Use Sector",  # inconsistent with subsector sum (rounding)
        ],
    },
    "ES2.4": {  # 1990-2021 Nitrous Oxide Emissions in Taiwan
        "tables": [5],
        "fix_cats": {
            0: {
                "Total Nitrous Oxide Emissionsl": "Total Nitrous Oxide Emissions",
            },
        },
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        "entity": f"N2O ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Total Nitrous Oxide Emissions": "0",
        },
        "drop_rows": [
            "3.F Field Burning of Agricultural Residues",  # has lower significant digits than in table ES3.4
            "5. Waste Sector",  # error in 1996 data
        ],
    },
    "ES2.5": {  # 1990-2021 Fluoride-Containing Gas Emissions in Taiwan
        "tables": [6, 7],
        "fix_cats": {},
        "rows_to_fix": {
            0: {
                -2: [
                    "Total PFCs Emissions (2.E Electronics Industry)",
                    "Total SF6 Emissions",
                    "Total NF3 Emissions (2.E Electronics Industry)",
                ],
            },
        },
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        "gas_splitting": {
            "Total HFCs Emissions": f"HFCS ({gwp_to_use})",
            "Total PFCs Emissions (2.E Electronics Industry)": f"PFCS ({gwp_to_use})",
            "Total SF6 Emissions": f"SF6 ({gwp_to_use})",
            "Total NF3 Emissions (2.E Electronics Industry)": f"NF3 ({gwp_to_use})",
            "Total Fluoride-Containing Gas Emissions": f"FGASES ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Total HFCs Emissions": "2",
            "Total PFCs Emissions (2.E Electronics Industry)": "2.E",
            "Total SF6 Emissions": "2",
            "Total NF3 Emissions (2.E Electronics Industry)": "2.E",
            "Total Fluoride-Containing Gas Emissions": "2",
        },
    },
    "ES3.1": {  # 1990-2021 Greenhouse Gas Emission in Taiwan by Sector
        "tables": [8],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Net GHG Emission (including LULUCF)": "0",
            "Total GHG Emission (excluding LULUCF)": "M.0.EL",
        },
    },
    "ES3.2": {  # 1990-2021 Greenhouse Gas Emissions Produced by Energy Sector in Taiwan
        "tables": [9, 10],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
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
            "Total CO2 Emission": "1",
            "Total CH4 Emission": "1",
            "Total N2O Emission": "1",
            "Total Emission from Energy Sector": "1",
        },
    },
    "ES3.3": {  # 1990-2021 Greenhouse Gas Emissions Produced by Industrial Process
        # and Product Use Sector (IPPU) in Taiwan
        "tables": [11],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
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
            "Total CO2 Emission": "2",
            "Total CH4 Emission": "2",
            "Total N2O Emission": "2",
            "Total HFCs Emission": "2",
            "Total PFCs Emission (2.E Electronics Industry)": "2.E",
            "Total SF6 Emission": "2",
            "Total NF3 Emission (2.E Electronics Industry)": "2.E",
            "Total Emission from IPPU Sector": "2",
        },
        "drop_rows": [
            #     ("2.D Non-Energy Products from Fuels and Solvent Use", "CO2"),
            # has lower significant digits than in table ES2.2
            "Total CH4 Emission",  # inconsistent with subsectors (rounding)
        ],
    },
    "ES3.4": {  # 1990-2021 Greenhouse Gas Emissions Produced by Agriculture Sector in Taiwan
        "tables": [12, 13],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
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
            "Total CO2 Emission (3.H Urea applied)": "3.H",
            "Total CH4 Emission": "3",
            "Total N2O Emission": "3",
            "Total Emission From Agriculture Sector": "3",
        },
    },
    "ES3.6": {  # 1990-2020 Greenhouse Gas Emissions in Taiwan by Waste Sector
        "tables": [14],
        "rows_to_fix": {
            0: {
                3: ["Total CO2 Emission"],
            },
        },
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,  # two column header
        "gas_splitting": {
            "Total CO2 Emission (5.C Incineration and Open Burning of Waste)": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total Emission from Waste Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Total CO2 Emission (5.C Incineration and Open Burning of Waste)": "5.C",
            "Total CH4 Emission": "5",
            "Total N2O Emission": "5",
            "Total Emission from Waste Sector": "5",
        },
    },
}

table_defs_skip = {
    "ES2.1": {  # 1990-2020 Greenhouse Gas Emissions and Sequestration in Taiwan by Type
        "tables": [0],
        "rows_to_fix": {
            0: {
                3: ["CO2"],
            },
            1: {  # wherte col 0 is empty
                3: ["Net GHG Emission", "Total GHG Emission"],
            },
        },
        "index_cols": ["GHG", "GWP"],
        "wide_keyword": "GHG",
        "col_wide_kwd": 0,
        "unit": "ktCO2eq",
    },
    "ES2.5": {  # 1990-2020 Fluoride-Containing Gas Emissions in Taiwan
        "tables": [6],
        "rows_to_fix": {
            0: {
                -2: ["Total SF6 Emissions", "Total NF3 Emissions"],
            },
        },
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        # "entity": "CO2",
        "unit": "ktCO2eq",
    },
    "ES3.5": {  # skip for now: 1990-2020 Changes in Carbon Sequestration by LULUCF Sector in Taiwan2],
        "tables": [12],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],  # header is merged col :-(
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,  # two column header
        "unit": "kt",
        "entity": "CO2",
    },  # need to consider the two columns specially (merge?)
}


##### primap2 metadata
cat_code_regexp = r"(?P<code>^[a-zA-Z0-9\.]{1,7})\s.*"

time_format = "%Y"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
    # "area": "Geo_code",
}

add_coords_cols = {
    #    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_1996_Taiwan_Inv",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "TWN-GHG-Inventory",
    "provenance": "measured",
    "scenario": "2023NIR",
    "area": "TWN",
    # unit fill by table
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
}

coords_value_filling = {}

#
filter_remove = {}

filter_keep = {}

meta_data = {
    "references": "https://www.cca.gov.tw/information-service/publications/national-ghg-inventory-report/1851.html",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "2023 Republic of China - National Greenhouse Gas Report",
    "comment": "Read fom pdf file and converted to PRIMAP2 format by Johannes Gütschow",
    "institution": "Republic of China - Environmental Protection Administration",
}

##### processing information
cat_conversion = {
    "mapping": {
        "0": "0",
        "M.0.EL": "M.0.EL",
        "1": "1",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.A.4.a": "1.A.4.a",
        "1.A.4.b": "1.A.4.b",
        "1.A.4.c": "1.A.4.c",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "2": "2",
        "2.A": "2.A",
        "2.B": "2.B",
        "2.C": "2.C",
        "2.D": "2.D",
        "2.E": "2.E",
        "2.F": "2.F",
        "2.G": "2.G",
        "2.H": "2.H",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.AS",
        "3.F": "3.C.1.b",
        "3.H": "3.C.3",
        "4": "M.LULUCF",
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.B",
        "5.C": "4.C",
        "5.D": "4.D",
        "5.D.1": "4.D.1",
        "5.D.2": "4.D.2",
    },
    "aggregate": {
        "1.A": {
            "sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4"],
            # "name": "Fuel Combustion Activities",
        },
        "1.B": {
            "sources": ["1.B.1", "1.B.2"],
            # "name": "Fugitive Emissions from Fuels"
        },
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"],
            # "name": "Industrial Process and Product Use Sector",
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            # "name": "Livestock"
        },
        "3.B": {
            "sources": ["M.LULUCF"],
            # "name": "Land"
        },
        "3.C.1": {
            "sources": ["3.C.1.b"],
            # "name": "Emissions from Biomass Burning"
        },
        "3.C.5": {
            "sources": ["3.C.5.a", "3.C.5.b"],
            # "name": "Indirect N2O Emissions from Managed Soils",
        },
        "3.C": {
            "sources": ["3.C.1", "3.C.3", "M.3.AS", "3.C.7"],
            # "name": "Aggregate sources and non-CO2 emissions sources on land",
        },
        "M.AG.ELV": {
            "sources": ["3.C"],
            # "name": "Agriculture excluding livestock emissions",
        },
        "M.AG": {
            "sources": ["3.A", "3.C"],
            # "name": "Agriculture"
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            # "name": "AFOLU"
        },  # consistency check
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},  # consistency check
        "0": {"sources": ["1", "2", "3", "4"]},  # consistency check
    },
}

basket_copy = {
    "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
    "entities": ["HFCS", "PFCS"],
    "source_GWP": gwp_to_use,
}
