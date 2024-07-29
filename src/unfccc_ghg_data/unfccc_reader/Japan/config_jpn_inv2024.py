"""Config for Japan 2024 Inventroy

General configuration for reading the inventory files for Japan's official 2025
inventory from xlsx

"""


gwp_to_use = "AR5GWP100"

sheets_to_read = {
    "15.【Annex】UN-CO2": {
        "xls_params": {
            "usecols": "X:BG",
            "skiprows": 4,
            "nrows": 55,
        },
        "unit": "kt CO2 / year",
        "entity": "CO2",
        "cat_cols": ["Source / sink", "Unnamed: 24", "Unnamed: 25"],
        "cat_mapping": {
            "1.A. Fuel Combustion": "1.A",
            "1.A.1. Energy Industries": "1.A.1",
            "Public Electricity and Heat Production": "1.A.1.a",
            "Petroleum Refining": "1.A.1.b",
            "Manufacture of Solid Fuels and Other Energy Industries": "1.A.1.c",
            "1.A.2. Manufacturing Industries and Construction": "1.A.2",
            "Iron and Steel": "1.A.2.a",
            "Non-Ferrous Metals": "1.A.2.b",
            "Chemicals": "1.A.2.c",
            "Pulp, Paper and Print": "1.A.2.d",
            "Food Processing, Beverages and Tobacco": "1.A.2.e",
            "Non-metallic minerals": "1.A.2.f",
            "Other": "1.A.2.g",
            "1.A.3. Transport": "1.A.3",
            "Domestic Aviation": "1.A.3.a",
            "Road Transportation": "1.A.3.b",
            "Railways": "1.A.3.c",
            "Domestic Navigation": "1.A.3.d",
            "1.A.4. Other Sector": "1.A.4",
            "Commercial/Institutional": "1.A.4.a",
            "Residential": "1.A.4.b",
            "Agriculture/Forestry/Fisheries": "1.A.4.c",
            "1.B. Fugitive Emissions from Fuels": "1.B",
            "2. Industrial Processes and Product Use": "2",
            "2.A. Mineral Industries": "2.A",
            "Cement Production": "2.A.1",
            "Lime Production": "2.A.2",
            "Glass Production": "2.A.3",
            "Other Process Uses of Carbonates": "2.A.4",
            "2.B. Chemical Industry": "2.B",
            "Ammonia Production": "2.B.1",
            "Petrochemical, Carbon Black and Other Production": "2.B.8",
            "2.C. Metal Industry": "2.C",
            "2.D. Non-energy Products from Fuels and Solvent Use": "2.D",
            "2.H. Other (Utilization of Carbonated Gas, etc.)": "2.H",
            "3. Agriculture": "3",
            "3.G. Liming": "3.G",
            "3.H. Urea Application": "3.H",
            "4. Land-Use, Land-Use Change, and Forestry (LULUCF)": "4",
            "4.A. Forest land": "4.A",
            "4.B. Cropland": "4.B",
            "4.C. Grassland": "4.C",
            "4.D. Wetlands": "4.D",
            "4.E. Settlements": "4.E",
            "4.F. Other land": "4.F",
            "4.G. Harvest Wood Products": "4.G",
            "4.H. Other": "4.H",
            "5. Waste": "5",
            "5.C. Incineration and Open Burning of Waste (excluding waste for energy purposes)": "5.C",
            "5.E. Decomposition of Petroleum-Derived Surfactants": "5.E",
            "Indirect CO2": "M.Memo.IndCO2",
            "Total (excluding LULUCF, excluding indirect CO2)": "M.0.EL",
            "Total (including LULUCF, excluding indirect CO2)": "0",
            "Total (excluding LULUCF, including indirect CO2)": "",  # ignore
            "Total (including LULUCF, including indirect CO2)": "",  # ignore
        },
    },
    "6.CH4": {
        "xls_params": {
            "usecols": "X:Y,AA:BG",
            "skiprows": 3,
            "nrows": 25,
        },
        "unit": "kt CO2 / year",
        "entity": f"CH4 ({gwp_to_use})",
        "cat_cols": ["Unnamed: 23", "Unnamed: 24"],
        "cat_mapping": {
            "1.A. Fuel Combustion": "1.A",
            "1.A.1. Energy Industries": "1.A.1",
            "1.A.2. Manufacturing industries and construction": "1.A.2",
            "1.A.3. Transport": "1.A.3",
            "1.A.4. Commercial, Residential, Agriculture, etc.": "1.A.4",
            "1.A.5. Other": "1.A.5",
            "1.B. Fugitive Emissions from Fuels": "1.B",
            "1.B.1. Solid Fuels": "1.B.1",
            "1.B.2. Oil, Natural Gas and Other": "1.B.2",
            "2. Industrial Processes and Product Use": "2",
            "2.B. Chemical Industry": "2.B",
            "2.C. Metal Industry": "2.C",
            "3. Agriculture": "3",
            "3.A. Enteric Fermentation": "3.A",
            "3.B. Manure Management": "3.B",
            "3.C. Rice Cultivation": "3.C",
            "3.F. Field Burning of Agricultural Residues": "3.F",
            "5. Waste": "5",
            "5.A. Solid Waste Disposal": "5.A",
            "5.B. Biological Treatment of Solid Waste": "5.B",
            "5.C. Incineration and Open Burning of Waste (excluding waste for energy purposes)": "5.C",
            "5.D. Wastewater Treatment and Discharge": "5.D",
            "Waste for Energy Purposes": "M.5.WE",  # map to energy and recalculate sectors
            "Total": "0",
        },
    },
    "7.N2O": {
        "xls_params": {
            "usecols": "X:Y,AA:BG",
            "skiprows": 3,
            "nrows": 23,
        },
        "unit": "kt CO2 / year",
        "entity": f"N2O ({gwp_to_use})",
        "cat_cols": ["Unnamed: 23", "Unnamed: 24"],
        "cat_mapping": {
            "1.A./1.B.Energy": "1",
            "1.A. Fuel Combustion": "1.A",
            "1.A.1. Energy Industries": "1.A.1",
            "1.A.2. Manufacturing industries and construction": "1.A.2",
            "1.A.3. Transport": "1.A.3",
            "1.A.4. Commercial, Residential, Agriculture, etc.": "1.A.4",
            "1.A.5. Other": "1.A.5",
            "1.B. Fugitive Emissions from Fuel": "1.B",
            "2.Industrial Processes and Product Use": "2",
            "2.B. Chemical Industry": "2.B",
            "2.E. Electronics Industry": "2.E",
            "2.G. Other Product Manufacture and Use": "2.G",
            "3.Agriculture": "3",
            "3.B. Manure Management": "3.B",
            "3.D. Agricultural Soils": "3.D",
            "3.F. Field Burning of Agricultural Residues": "3.F",
            "5.Waste": "5",
            "5.B. Biological Treatment of Solid Waste": "5.B",
            "5.C. Incineration and Open Burning of Waste  (excluding waste for energy purposes)": "5.C",
            "5.D. Wastewater Treatment and Discharge": "5.D",
            "Waste for Energy Purposes": "M.5.WE",  # map to energy and recalculate sectors
            "Total": "0",
        },
    },
    "8.F-gas": {
        "xls_params": {
            "usecols": "X:Y,AA:BG",
            "skiprows": 3,
            "nrows": 32,
        },
        "unit": "kt CO2 / year",
        "entity": "COL_Unnamed: 23",
        "cat_cols": ["Unnamed: 24"],
        "cat_mapping": {
            "Total": "2",
            "Refrigeration and Air Conditioning Equipment": "M.1996.2.F.1",
            "Foam Blowing Agents": "M.1996.2.F.2",
            "Aerosols / MDI": "M.1996.2.F.4",
            "Solvents / Cleaning agents": "M.1996.2.F.5",
            "Fugitive emissions from HFCs manufacturing": "M.1996.2.E.2.a",
            "Semiconductor": "M.1996.2.F.7",
            "Liquid Crystals": "M.1996.2.F.6.b",
            "By-product emissions from HCFC-22": "M.1996.2.E.1.a",
            "Fire Protection": "M.1996.2.F.3",
            "Magnesium Production": "M.1996.2.C.4.b",
            "Other": "M.1996.2.G",  # checked where data is mapped to in CRF
            "Fugitive emissions from PFCs manufacturing": "M.1996.2.E.2.b",
            "Aluminum Production": "M.1996.2.C.4.a",
            "Accelerators": "M.1996.2.F.9.d",
            "Electrical Equipment": "M.1996.2.F.8",
            "Fugitive emissions from SF6 manufacturing": "M.1996.2.E.2.c",
            "Fugitive emissions from NF3 manufacturing": "M.1996.2.E.2.d",
        },
    },
}

time_format = "%Y"

coords_cols = {
    "category": "category",
}

# add_coords_cols = {
#     "orig_cat_name": ["orig_cat_name", "category"],
# }

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_2006_Japan_INV",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "JPN-GHG-Inventory",
    "provenance": "measured",
    "area": "JPN",
    "scenario": "2024INV",
}

coords_value_mapping = {
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NF3": f"NF3 ({gwp_to_use})",
        "Total F-gases": f"FGASES ({gwp_to_use})",
    },
}

meta_data = {
    "references": "https://www.nies.go.jp/gio/en/aboutghg/index.html",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "National GHG Inventory of Japan, 2024",
    "comment": "Read fom xlsx file by Johannes Gütschow",
    "institution": "National Institute for Environmental Studies Japan",
}

filter_remove = {
    "f1": {
        "category": [
            "Total (excluding LULUCF, including indirect CO2)",
            "Total (including LULUCF, including indirect CO2)",
        ]
    }
}

# for processing
terminology_proc = "IPCC2006_PRIMAP"

cat_conversion = {
    "mapping": {
        "0": "0",
        #'1': '1',  # reaggregate because of energy from waste
        #'1.A': '1.A',  # reaggregate because of energy from waste
        "1.A.1": "M.1.A.1.EXW",  # reaggregate because of energy from waste
        "1.A.1.a": "1.A.1.a",
        "1.A.1.b": "1.A.1.b",
        "1.A.1.c": "1.A.1.c",
        "1.A.2": "1.A.2",
        "1.A.2.a": "1.A.2.a",
        "1.A.2.b": "1.A.2.b",
        "1.A.2.c": "1.A.2.c",
        "1.A.2.d": "1.A.2.d",
        "1.A.2.e": "1.A.2.e",
        "1.A.2.f": "1.A.2.f",
        "1.A.2.g": "1.A.2.m",
        "1.A.3": "1.A.3",
        "1.A.3.a": "1.A.3.a.1",
        "1.A.3.b": "1.A.3.b",
        "1.A.3.c": "1.A.3.c",
        "1.A.3.d": "1.A.3.d.1",
        "1.A.4": "1.A.4",
        "1.A.4.a": "1.A.4.a",
        "1.A.4.b": "1.A.4.b",
        "1.A.4.c": "1.A.4.c",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",
        "2.A.2": "2.A.2",
        "2.A.3": "2.A.3",
        "2.A.4": "2.A.4",
        "2.B": "2.B",
        "2.B.1": "2.B.1",
        "2.B.8": "2.B.8",
        "2.C": "2.C",
        "M.1996.2.C.4.a": "2.C.3",
        "M.1996.2.C.4.b": "2.C.4",
        "2.D": "2.D",
        "2.E": "2.E",
        "M.1996.2.E.1.a": "M.2.B.9.a.i",
        "M.1996.2.E.2.a": "M.2.B.9.b.i",
        "M.1996.2.E.2.b": "M.2.B.9.b.ii",
        "M.1996.2.E.2.c": "M.2.B.9.b.iii",
        "M.1996.2.E.2.d": "M.2.B.9.b.iv",
        "M.1996.2.F.1": "2.F.1",
        "M.1996.2.F.2": "2.F.2",
        "M.1996.2.F.3": "2.F.3",
        "M.1996.2.F.4": "2.F.4",
        "M.1996.2.F.5": "2.F.5",
        "M.1996.2.F.6.b": "2.E.2",
        "M.1996.2.F.7": "2.E.1",
        "M.1996.2.F.8": "2.G.1.a",
        "M.1996.2.F.9.d": "2.G.2.b",
        "M.1996.2.G": "2.G.2.c",
        "2.G": "2.G",
        "2.H": "2.H",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.C.45.AG",
        "3.F": "M.3.C.1.AG",
        "3.G": "3.C.2",
        "3.H": "3.C.3",
        "4": "M.LULUCF",
        "4.A": "3.B.1",
        "4.B": "3.B.2",
        "4.C": "3.B.3",
        "4.D": "3.B.4",
        "4.E": "3.B.5",
        "4.F": "3.B.6",
        "4.G": "3.D.1",
        "4.H": "M.3.D.2.LU",
        # '5': '5',  # reaggregate because of energy from waste
        "5.A": "4.A",
        "5.B": "4.B",
        "5.C": "4.C",
        "5.D": "4.D",
        "5.E": "4.E",
        "M.0.EL": "M.0.EL",
        "M.5.WE": "M.1.A.1.a.ii",
        "M.Memo.IndCO2": "M.Memo.IndCO2",
    },
    "aggregate": {
        "1.A.1": {"sources": ["M.1.A.1.a.ii", "M.1.A.1.EXW"]},
        "1.A": {"sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"]},
        "1": {"sources": ["1.A", "1.B"]},
        "2.B.9.a": {"sources": ["M.2.B.9.a.i"]},
        "2.B.9.b": {
            "sources": ["M.2.B.9.b.i", "M.2.B.9.b.ii", "M.2.B.9.b.iii", "M.2.B.9.b.iv"]
        },
        "2.B.9": {"sources": ["2.B.9.a", "2.B.9.b"]},
        "2.B": {  # reaggregation only for f-gases should create no conflicts
            "sources": ["2.B.1", "2.B.8", "2.B.9"]
        },
        "2.C": {  # reaggregation only for f-gases should create no conflicts
            "sources": ["2.C.3", "2.C.4"]
        },
        "2.E": {  # reaggregation only for f-gases should create no conflicts
            "sources": ["2.E.1", "2.E.2"]
        },
        "2.F": {  #  only for f-gases
            "sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4", "2.F.5"]
        },
        "2.G.1": {"sources": ["2.G.1.a"]},
        "2.G.2": {"sources": ["2.G.2.b", "2.G.2.c"]},
        "2.G": {  # reaggregation only for f-gases should create no conflicts
            "sources": ["2.G.1", "2.G.2", "2.G.4"]
        },
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"]},
        "3.C.1": {"sources": ["3.C.1.AG"]},
        "M.3.C.AG": {"sources": ["3.C.1", "3.C.2", "3.C.3", "M.3.C.45.AG", "3.C.7"]},
        "3.C": {"sources": ["M.3.C.AG"]},
        "M.3.D.LU": {"sources": ["3.D.1", "M.3.D.2.LU"]},
        "3.D": {"sources": ["M.3.D.LU"]},
        "M.AG.ELV": {"sources": ["3.C"]},
        "3": {"sources": ["3.A", "3.B", "3.C", "3.D"]},
        "4": {"sources": ["4.A", "4.B", "4.C", "4.D", "4.E"]},
        # consistency check
        "2": {"sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"]},
        "M.AG": {"sources": ["M.AG.ELV", "3.A"]},
        "0": {"sources": ["1", "2", "3", "4"]},
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
    },
}

basket_copy = {
    "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
    "entities": ["HFCS", "PFCS"],
    "source_GWP": gwp_to_use,
}

gas_baskets = {
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)", "PFCS (SARGWP100)", "SF6", "NF3"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)", "PFCS (AR4GWP100)", "SF6", "NF3"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)", "PFCS (AR5GWP100)", "SF6", "NF3"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)", "PFCS (AR6GWP100)", "SF6", "NF3"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}

### copied


coords_terminologies_2006 = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}
