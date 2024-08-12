"""Config for USA 2024 Inventroy

General configuration for reading the inventory files for USA's official 2024
inventory from xlsx

"""

gwp_to_use = "AR5GWP100"
category_mapping = {
    "Abandoned Oil and Gas Wells": "M.1.B.2.ab.6",
    "Abandoned Underground Coal Mines": "1.B.1.a.i.3",
    "Adipic Acid Production": "2.B.3",
    "Agricultural Soil Management": "3.D",
    "Aluminum Production": "2.C.3",
    "Ammonia Production": "2.B.1",
    "Anaerobic Digestion at Biogas Facilities": "5.B.2",
    "Biomass and Biodiesel Consumptiona": "M.Memo.Bio",
    #'CH4': '4',
    "CH4c": "M.0.EL",
    "CO2": "M.0.EL",
    "Caprolactam, Glyoxal, and Glyoxylic Acid Production": "2.B.4",
    "Carbide Production and Consumption": "2.B.5",
    "Carbon Dioxide Consumption": "M.2.B.10.b",
    "Cement Production": "2.A.1",
    "Coal Mining": "M.1.B.1.a",  # abandoned underground mines are missing
    "Commercial": "1.A.4.a",
    "Composting": "5.B.1",
    "Electric Power Sector": "1.A.1",
    "Electrical Equipment": "2.G.1",
    "Electronics Industry": "2.E",
    "Enteric Fermentation": "3.A",
    "Ferroalloy Production": "2.C.2",
    "Field Burning of Agricultural Residues": "3.F",
    "Fluorochemical Production": "2.B.9",
    "Fossil Fuel Combustion": "1.A",
    "Glass Production": "2.A.3",
    "HFCs": "2",
    "Incineration of Waste": "1.A.5.a.iv",
    "Industrial": "1.A.2",
    "International Bunker Fuelsb": "M.Memo.Int",
    "Iron and Steel Production & Metallurgical Coke Production": "2.C.1",
    # 'LULUCF Carbon Stock Changee': '',
    # 'LULUCF Emissionsc': '',
    # 'LULUCF Sector Net Totalf': '',
    "Landfills": "5.A.1",
    "Lead Production": "2.C.5",
    "Lime Production": "2.A.2",
    "Liming": "3.G",
    "Magnesium Production and Processing": "2.C.4",
    "Manure Management": "3.B",
    "Mobile Combustion": "M.1.A.MOB",
    #'N2O': '4',
    "N2O from Product Uses": "2.G.3",
    "N2Oc": "M.0.EL",
    "NF3": "2",
    "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
    "Net Emissions (Sources and Sinks)": "0",
    "Nitric Acid Production": "2.B.2",
    "Non-Energy Use of Fuels": "1.A.5.a.iii",
    "Other Process Uses of Carbonates": "2.A.4",
    "PFCs": "2",
    "Petrochemical Production": "2.B.8",
    "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
    "Phosphoric Acid Production": "M.2.B.10.c",
    "Residential": "1.A.4.b",
    "Rice Cultivation": "3.C",
    "SF6": "2",
    "SF6 and PFCs from Other Product Use": "2.G.2",
    "Soda Ash Production": "2.B.7",
    "Stationary Combustion": "M.1.A.STAT",
    "Substitution of Ozone Depleting Substances": "2.F",
    "Titanium Dioxide Production": "2.B.6",
    "Total Gross Emissions (Sources)": "M.0.EL",
    "Transportation": "1.A.3",
    "U.S. Territories": "1.A.5.a.v",
    "Urea Consumption for Non-Agricultural Purposes": "M.2.B.10.a",
    "Urea Fertilization": "3.H",
    "Wastewater Treatment": "5.D",
    "Zinc Production": "2.C.6",
}

category_col = "Gas/Source"
inventory_files = {
    "Table 2-1.csv": {
        "CO2": None,
        "CH4c": None,
        "N2Oc": None,
        "HFCs": {
            "coords_defaults": {
                "entity": f"HFCS ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "PFCs": {
            "coords_defaults": {
                "entity": f"PFCS ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "SF6": {
            "coords_defaults": {
                "entity": f"SF6 ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "NF3": {
            "coords_defaults": {
                "entity": f"NF3 ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "Total Gross Emissions (Sources)": {
            "coords_defaults": {
                "entity": f"KYOTOGHG ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "LULUCF Emissionsc": {
            "coords_defaults": {"unit": "Mt CO2 / year"},
            "coords_value_mapping": {
                "entity": {
                    #'LULUCF Emissionsc': '',
                    "CH4": f"CH4 ({gwp_to_use})",
                    "N2O": f"N2O ({gwp_to_use})",
                    "LULUCF Carbon Stock Changee": "CO2",
                    "LULUCF Sector Net Totalf": f"KYOTGHG ({gwp_to_use})",
                },
                "category": {
                    #'LULUCF Emissionsc': '',
                    "CH4": "4",
                    "N2O": "4",
                    "LULUCF Carbon Stock Changee": "4",
                    "LULUCF Sector Net Totalf": "4",
                },
            },
        },
        "Net Emissions (Sources and Sinks)": {
            "coords_defaults": {
                "entity": f"KYOTOGHG ({gwp_to_use})",
                "unit": "Mt CO2 / year",
            },
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "+ Does not exceed 0.05 MMT CO2 Eq.": None,
    },
    "Table 2-2.csv": {
        "CO2": {
            "coords_defaults": {"entity": "CO2", "unit": "kt CO2 / year"},
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "CH4c": {
            "coords_defaults": {"entity": "CH4", "unit": "kt CH4 / year"},
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "N2Oc": {
            "coords_defaults": {"entity": "N2O", "unit": "kt N2O / year"},
            "coords_value_mapping": {
                "category": category_mapping,
            },
        },
        "HFCs": None,
        "PFCs": None,
        "SF?": None,
        "NF?": None,
        "+ Does not exceed 0.5 kt.": None,
    },
}

time_format = "%Y"

coords_cols_template = {
    "category": category_col,
}

coords_terminologies = {
    "area": "ISO3",
    "category": "CRF2013_2023",
    "scenario": "PRIMAP",
}

coords_defaults_template = {
    "source": "USA-GHG-Inventory",
    "provenance": "measured",
    "area": "USA",
    "scenario": "2024INV",
}

meta_data = {
    "references": "https://www.epa.gov/ghgemissions/"
    "inventory-us-greenhouse-gas-emissions-and-sinks-1990-2022",
    "rights": "",
    "contact": "johannes.guetschow@climate-resource.com",
    "title": "Inventory of U.S. Greenhouse Gas Emissions and Sinks: 1990-2022",
    "comment": "Read fom csv files by Johannes Gütschow",
    "institution": "United States Environmental Protection Agency",
}

filter_remove = {
    "f1": {
        category_col: [
            "LULUCF Emissionsc",
        ]
    }
}

### processing

cat_conversion = {
    "mapping": {
        "0": "0",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4.a": "1.A.4.a",
        "1.A.4.b": "1.A.4.b",
        "1.A.5.a.iii": "2.D",  # non energy fuel use
        "1.A.5.a.iv": "M.1.A.5.a.iv",  # waste incineration
        "1.A.5.a.v": "1.A.5.a.v",  # US Territories
        "1.B.1.a.i.3": "1.B.1.a.i.3",
        "2": "2",
        "2.A.1": "2.A.1",
        "2.A.2": "2.A.2",
        "2.A.3": "2.A.3",
        "2.A.4": "2.A.4",
        "2.B.1": "2.B.1",
        "2.B.2": "2.B.2",
        "2.B.3": "2.B.3",
        "2.B.4": "2.B.4",
        "2.B.5": "2.B.5",
        "2.B.6": "2.B.6",
        "2.B.7": "2.B.7",
        "2.B.8": "2.B.8",
        "2.B.9": "2.B.9",
        "2.C.1": "2.C.1",
        "2.C.2": "2.C.2",
        "2.C.3": "2.C.3",
        "2.C.4": "2.C.4",
        "2.C.5": "2.C.5",
        "2.C.6": "2.C.6",
        "2.E": "2.E",
        "2.F": "2.F",
        "2.G.1": "2.G.1",
        "2.G.2": "2.G.2",
        "2.G.3": "2.G.3",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.C.45.AG",
        "3.F": "M.3.C.1.AG",
        "3.G": "3.C.2",
        "3.H": "3.C.3",
        "4": "M.LULUCF",
        "5.A.1": "4.A.1",
        "5.B.1": "4.B.1",
        "5.B.2": "4.B.2",
        "5.D": "4.D",
        "M.0.EL": "M.0.EL",
        "M.1.A.MOB": "M.1.A.MOB",
        "M.1.A.STAT": "M.1.A.STAT",
        "M.1.B.1.a": "M.1.B.1.a",
        "M.1.B.2.a": "M.1.B.2.a",
        "M.1.B.2.ab.6": "M.1.B.2.ab.6",
        "M.1.B.2.b": "M.1.B.2.b",
        "M.2.B.10.a": "M.2.B.10.a",
        "M.2.B.10.b": "M.2.B.10.b",
        "M.2.B.10.c": "M.2.B.10.c",
        "M.Memo.Bio": "M.BIO",
        "M.Memo.Int": "M.BK",
    },
    "aggregate": {
        # 1
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b"]},
        "1.A.5.a": {"sources": ["M.1.A.5.a.iv", "M.1.A.5.a.v"]},
        "1.A.5": {"sources": ["1.A.5.a"]},
        "1.A": {
            "sources": ["M.1.A.MOB", "M.1.A.STAT", "1.A.5"],
            "filter": {"entity": ["CH4", "N2O"]},
        },
        "1.B.1": {"sources": ["M.1.B.1.a", "1.B.1.a.i.3"]},
        "1.B.2": {"sources": ["M.1.B.2.a", "M.1.B.2.b", "M.1.B.2.ab.6"]},
        "1.B": {"sources": ["1.B.1", "1.B.2"]},
        "1": {"sources": ["1.A", "1.B"]},
        # 2
        "2.A": {"sources": ["2.A.1", "2.A.2", "2.A.3", "2.A.4"]},
        "2.B.10": {"sources": ["M.2.B.10.a", "M.2.B.10.b", "M.2.B.10.c"]},
        "2.B": {
            "sources": [
                "2.B.1",
                "2.B.2",
                "2.B.3",
                "2.B.4",
                "2.B.5",
                "2.B.6",
                "2.B.7",
                "2.B.8",
                "2.B.9",
                "2.B.10",
            ]
        },
        "2.C": {"sources": ["2.C.1", "2.C.2", "2.C.3", "2.C.4", "2.C.5", "2.C.6"]},
        "2.G": {"sources": ["2.G.1", "2.G.2", "2.G.3"]},
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G"],
            "tolerance": 0.251,  # rounding inconsistencies in NF3 and PFCs after 2008
        },
        # M.AG
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        "3.C.1": {"sources": ["M.3.C.1.AG"]},
        "M.3.C.AG": {"sources": ["3.C.1", "3.C.2", "3.C.3", "M.3.C.45.AG", "3.C.7"]},
        "3.C": {"sources": ["M.3.C.AG"]},
        "M.AG.ELV": {"sources": ["M.3.C.AG"]},
        "M.AG": {"sources": ["M.AG.ELV", "3.A"]},
        # 3
        "3": {"sources": ["M.AG", "M.LULUCF"]},
        # 4
        "4.A": {"sources": ["4.A.1"]},
        "4.B": {"sources": ["4.B.1", "4.B.2"]},
        "4": {"sources": ["4.A", "4.B", "4.D"]},
        # consistency check
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

terminology_proc = "IPCC2006_PRIMAP"
