"""
Configuration and custom functions for Taiwan's 2023 NIR
"""

gwp_to_use = "AR5GWP100"
terminology_proc = "IPCC2006_PRIMAP"

##### Table definitions
# page defs to hold information on reading the table
page_defs = {
    "5": {
        "table_areas": ["39,226,563,66"],
        "split_text": False,
        "flavor": "stream",
    },
    "6": {
        "table_areas": ["35,757,561,436", "34,363,563,60"],
        # "columns": ['195,228,263,295,328,363,395,428,462,495,529'], # works without
        "split_text": True,
        "flavor": "stream",
    },
    "7": {
        "table_areas": ["34,761,565,153"],
        "split_text": True,
        "flavor": "stream",
    },
    "8": {
        "table_areas": ["34,583,562,42"],
        "split_text": True,
        "flavor": "stream",
    },
    "9": {
        "table_areas": ["31,511,561,49"],
        "split_text": False,
        "flavor": "stream",
    },
    "10": {
        "table_areas": ["31,547,563,68"],
        "split_text": False,
        "flavor": "stream",
    },
    "12": {
        "table_areas": ["31,755,562,447"],
        "split_text": True,
        "flavor": "stream",
    },
    "13": {
        "table_areas": ["31,758,562,76"],
        "split_text": True,
        "flavor": "stream",
    },
    "14": {
        "table_areas": ["31,345,562,61"],
        "columns": ["216,250,280,313,343,374,406,435,466,497,529"],
        "split_text": True,
        "flavor": "stream",
    },
    "15": {
        "table_areas": ["31,764,562,194"],
        "columns": ["216,250,280,313,343,374,406,435,466,497,529"],
        "split_text": True,
        "flavor": "stream",
    },
    "16": {
        "table_areas": ["31,342,562,54"],
        "split_text": True,
        "flavor": "stream",
    },
    "17": {
        "table_areas": ["31,767,562,623"],
        "split_text": True,
        "flavor": "stream",
    },
    "18": {
        "table_areas": ["31,254,563,70"],
        "split_text": False,
        "flavor": "stream",
    },
    "19": {
        "table_areas": ["31,754,562,439"],
        "split_text": False,
        "flavor": "stream",
    },
}

# table defs to hold information on how to process the tables
table_defs = {
    "ES2.2": {  # 1990-2022 Carbon Dioxide Emissions and Sequestration in Taiwan
        "tables": [2, 3],
        "rows_to_fix": {
            0: {
                3: [
                    "1.A.4.c Agriculture, Forestry, Fishery, and",
                    "2.D Non-Energy Products from Fuels and",
                    "4. Land Use, Land Use Change and Forestry",
                ],
            },
        },
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,
        "entity": "CO2",
        "unit": "kt",
        "cat_codes_manual": {
            "Net GHG Emission (including LULUCF)": "0",
            "Total GHG Emission (excluding LULUCF)": "M.0.EL",
        },
    },
    "ES2.3": {  # 1990-2022 Methane Emissions in Taiwan
        "tables": [4],
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
    "ES2.4": {  # 1990-2022 Nitrous Oxide Emissions in Taiwan
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
        # "drop_rows": [
        #     "3.F Field Burning of Agricultural Residues",  # has lower significant digits than in table ES3.4
        #     "5. Waste Sector",  # error in 1996 data
        # ],
    },
    "ES2.5": {  # 1990-2022 Fluoride-Containing Gas Emissions in Taiwan
        "tables": [6],
        "fix_cats": {},
        "rows_to_fix": {},
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
    "ES3.1": {  # 1990-2022 Greenhouse Gas Emission in Taiwan by Sector
        "tables": [7],
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
    "ES3.2": {  # 1990-2022 Greenhouse Gas Emissions Produced by Energy Sector in Taiwan
        "tables": [8],
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
    "ES3.3": {  # 1990-2022 Greenhouse Gas Emissions Produced by Industrial Process
        # and Product Use Sector (IPPU) in Taiwan
        "tables": [9, 10],
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
    "ES3.4": {  # 1990-2022 Greenhouse Gas Emissions Produced by Agriculture Sector in Taiwan
        "tables": [11, 12],
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
    "ES3.6": {  # 1990-2022 Greenhouse Gas Emissions in Taiwan by Waste Sector
        "tables": [13, 14],
        "rows_to_fix": {},
        "index_cols": ["GHG Emission Sources and Sinks"],
        "wide_keyword": "GHG Emission Sources and Sinks",
        "col_wide_kwd": 0,  # two column header
        "gas_splitting": {
            "Total CO2 Emission": "CO2",
            "Total CH4 Emission": f"CH4 ({gwp_to_use})",
            "Total N2O Emission": f"N2O ({gwp_to_use})",
            "Total Emission from Waste Sector": f"KYOTOGHG ({gwp_to_use})",
            "GHG Emission Sources and Sinks": "entity",
        },
        "unit": "ktCO2eq",
        "cat_codes_manual": {
            "Total CO2 Emission": "5",
            "Total CH4 Emission": "5",
            "Total N2O Emission": "5",
            "Total Emission from Waste Sector": "5",
        },
    },
}

table_defs_skip = {
    "ES2.1": {  # 1990-2020 Greenhouse Gas Emissions and Sequestration in Taiwan by Type
        "tables": [0, 1],
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
    "scenario": "2024NIR",
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
    "references": "https://www.cca.gov.tw/en/information-service/publications/national-ghg-inventory-report/12003.html",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "2024 Republic of China - National Greenhouse Gas Report",
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
    "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
    "entities": ["HFCS", "PFCS"],
    "source_GWP": gwp_to_use,
}
