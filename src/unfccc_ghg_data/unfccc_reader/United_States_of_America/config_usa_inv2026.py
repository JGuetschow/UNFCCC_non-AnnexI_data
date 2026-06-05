"""Config for USA 2024 Inventroy

General configuration for reading the inventory files for USA's official draft 2025
inventory from csv

The EPA has never released the final inventory but was forced to publish the
draft inventory under the Freedom of Information Act

https://www.edf.org/freedom-information-act-documents-epas-greenhouse-gas-inventory

"""


gwp_to_use = "AR5GWP100"

filter_remove_cat = {
    "f_ignore": {
        "category": ["\\IGNORE"],
    }
}

# table definitions
inventory_files = {
    ## Chapter 3: energy
    # * 3-1, (detail not sufficient for all gases, stationary and mobile summed for CH4, N2O)
    "Chapter 3 - Energy": {
        "Table 3-1.csv": {
            "cat_col": "Gas/Source",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_CCS": {  # data inconsistent with table 3.33 because of rounding
                        "category": ["CO2 Transport, Injection, and Geological Storage"]
                    }
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "1",
                        "Fossil Fuel Combustion": "1.A",
                        "Transportation": "1.A.3",
                        "Electricity Generation": "1.A.1",
                        "Industrial": "1.A.2",
                        "Residential": "1.A.4.b",
                        "Commercial": "1.A.4.a",
                        "U.S. Territories": "1.A.5.a.v",
                        "Non-Energy Use of Fuels": "1.A.5.a.iii",  # not in 1.A sum
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Incineration of Waste": "1.A.5.a.iv",
                        "Coal Mining": "M.1.B.1.a",  # abandoned underground mines are missing
                        "CO2 Transport, Injection, and Geological Storage": "1.C",
                        "Abandoned Oil and Gas Wells": "M.1.B.2.ab.6",
                        "Biomass-Wooda": "M.Memo.Bio.Wood",
                        "International Bunker Fuelsb": "M.Memo.Int",
                        "Biofuels-Ethanola": "M.Memo.Bio.Ethanol",
                        "Biofuels-Biodiesela": "M.Memo.Bio.Biodiesel",
                        "Biomass-MSWa": "M.Memo.Bio.MSW",
                    },
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_Bunkers": {  # data inconsistent with table 3.36 because of
                        # rounding
                        "category": ["International Bunker Fuelsb"]
                    }
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "1",
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Coal Mining": "M.1.B.1.a",  # abandoned underground mines are missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Abandoned Oil and Gas Wells": "M.1.B.2.ab.6",
                        "Stationary Combustion": "M.1.A.STAT",
                        "Abandoned Underground Coal Mines": "1.B.1.a.i.3",
                        "Mobile Combustion": "M.1.A.MOB",
                        "Incineration of Waste": "1.A.5.a.iv",
                        "International Bunker Fuelsb": "M.Memo.Int",
                    },
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_Bunkers": {  # data inconsistent with table 3.36 because of
                        # rounding
                        "category": ["International Bunker Fuelsb"]
                    }
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "1",
                        "Natural Gas Systems": "M.1.B.2.b",  # abandoned wells missing
                        "Petroleum Systems": "M.1.B.2.a",  # abandoned wells missing
                        "Stationary Combustion": "M.1.A.STAT",
                        "Mobile Combustion": "M.1.A.MOB",
                        "Incineration of Waste": "1.A.5.a.iv",
                        "International Bunker Fuelsb": "M.Memo.Int",
                        "Total": "1",
                    },
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "1",
                    },
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq": None,
        },
        # * 3-3, 1.A subsectors for CO2, CH4, N2O
        "Table 3-3.csv": {
            "cat_col": "Sector/Gas",
            "Electric Power": {
                "coords_defaults": {
                    "category": "1.A.1",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Electric Power": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "Transportation": {
                "coords_defaults": {
                    "category": "1.A.3",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Transportation": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "Industrial": {
                "coords_defaults": {
                    "category": "1.A.2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Industrial": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "Residential": {
                "coords_defaults": {
                    "category": "1.A.4.b",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Residential": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "Commercial": {
                "coords_defaults": {
                    "category": "1.A.4.a",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Commercial": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "U.S. Territoriesa": {
                "coords_defaults": {
                    "category": "1.A.5.a.v",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "U.S. Territoriesa": f"KYOTOGHG ({gwp_to_use})",
                        "CO2": "CO2",
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "category": "1.A",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Total": f"KYOTOGHG ({gwp_to_use})",
                    }
                },
            },
            "a U.S. Territories are not apportioned by sector, and emissions shown in the "
            "table are total greenhouse gas emissions from all fuel combustion sources.": None,
        },
        #     * 3-8: CO2 details per fuel and sector. probably not necessary
        # * 3-9: CH4 details per fuel and sector. probably not necessary
        # * 3-10: N2O details per fuel and sector. probably not necessary
        # * 3-21, 3-22: coal mines (1.B.1)
        "Table 3-21.csv": {
            "cat_col": "Activity",
            "drop_cols": ["Unnamed: 2", "Unnamed: 4"],
            "UG Mining": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_rec": {"category": ["Liberated", "Recovered & Used"]}
                },
                "coords_value_mapping": {
                    "category": {
                        "UG Mining": "1.B.1.a.i.1",
                        # "Liberated": "\\IGNORE",
                        # "Recovered & Used": "\\IGNORE",
                        "Surface Mining": "1.B.1.a.ii.1",
                        "Post-Mining (UG)": "1.B.1.a.i.2",
                        "Post-Mining (Surface)": "1.B.1.a.ii.2",
                        "Total": "M.1.B.1.a",
                    }
                },
            },
            "Notes: Parentheses in above emissions tables indicate negative values. "
            "Totals may not sum due to independent rounding.": None,
        },
        "Table 3-22.csv": {
            "cat_col": "Activity",
            "Underground Mining": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_rec": {"category": ["Liberated", "Recovered & Used For Energy"]}
                },
                "coords_value_mapping": {
                    "category": {
                        "Underground Mining": "1.B.1.a.i.1",
                        # "Liberated": "\\IGNORE",
                        # "Recovered & Used For Energy": "\\IGNORE",
                        "Flaring": "1.B.1.a.i.4",
                        "Surface Mining": "1.B.1.a.ii.1",
                        "Total": "M.1.B.1.a",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        # * 3-23 CH4 from abandoned coal mines (no additional info)
        # * 3-25, 3-26, 3-27 Petroleum systems
        "Table 3-25.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.a.i",
                        "Production": "1.B.2.a.ii",
                        "Transportation": "1.B.2.a.iii",
                        "Refineries": "1.B.2.a.iv",
                        "total": "M.1.B.2.a",
                    }
                },
            },
        },
        "Table 3-26.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.a.i",
                        "Production": "1.B.2.a.ii",
                        "Transportation": "1.B.2.a.iii",
                        "Refineries": "1.B.2.a.iv",
                        "Total": "M.1.B.2.a",
                    }
                },
            },
        },
        "Table 3-27.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.a.i",
                        "Production": "1.B.2.a.ii",
                        "Transportation": "1.B.2.a.iii",
                        "Refineries": "1.B.2.a.iv",
                        "Total": "M.1.B.2.a",
                    }
                },
            },
            "+Less than 0.05 MMTCO2e": None,
        },
        # * 3-28, 3-29, 3-30 Natural gas systems
        # venting and flaring are included
        "Table 3-28.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.b.i",
                        "Production": "1.B.2.b.ii",
                        "Processing": "1.B.2.b.iii",
                        "Transmission and Storage": "1.B.2.b.iv",
                        "Distribution": "1.B.2.b.v",
                        "Post-Meter": "1.B.2.b.vi.1",
                        "Total": "M.1.B.2.b",
                    }
                },
            },
        },
        "Table 3-29.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.b.i",
                        "Production": "1.B.2.b.ii",
                        "Processing": "1.B.2.b.iii",
                        "Transmission and Storage": "1.B.2.b.iv",
                        "Distribution": "1.B.2.b.v",
                        "Post-Meter": "1.B.2.b.vi.1",
                        "Total": "M.1.B.2.b",
                    }
                },
            },
        },
        "Table 3-30.csv": {
            "cat_col": "Unnamed: 0",
            "Exploration": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Exploration": "1.B.2.b.i",
                        "Production": "1.B.2.b.ii",
                        "Processing": "1.B.2.b.iii",
                        "Transmission and Storage": "1.B.2.b.iv",
                        "Distribution": "1.B.2.b.v",
                        "Total": "M.1.B.2.b",
                    }
                },
            },
            "+Less than 0.05 MMTCO2e": None,
        },
        # * 3-31, 3-32, abandoned oil and gas wells
        "Table 3-31.csv": {
            "cat_col": "Unnamed: 0",
            "Abandoned Oil Wells": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Abandoned Oil Wells": "1.B.2.a.vi.1",
                        "Abandoned Gas Wells": "1.B.2.b.vi.2",
                        "Total": "M.1.B.2.ab.6",
                    }
                },
            },
        },
        "Table 3-32.csv": {
            "cat_col": "Unnamed: 0",
            "Abandoned Oil Wells": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Abandoned Oil Wells": "1.B.2.a.vi.1",
                        "Abandoned Gas Wells": "1.B.2.b.vi.2",
                        "Total": "M.1.B.2.ab.6",
                    }
                },
            },
            "+ Less than 0.05": None,
        },
        # * 3-33 1.C
        "Table 3-33.csv": {
            "cat_col": "Unnamed: 0",
            "Transport": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "kt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Transport": "1.C.1",
                        "InjectionÂ\xa0Â": "1.C.2.a",
                        "StorageÂ\xa0Â": "1.C.2.b",
                        "Total": "1.C",
                    }
                },
            },
            "NO (Not Occurring)": None,
        },
        # * 3-36: bunkers
        "Table 3-36.csv": {
            "cat_col": "Gas/Mode and Fuel Type",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "M.Memo.Int",
                        "Aviation": "M.Memo.Int.Avi",
                        "Commercial": "M.Memo.Int.Avi.com",
                        "Military": "M.Memo.Int.Avi.mil",
                        "Marine": "M.Memo.Int.Mar",
                    }
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "M.Memo.Int",
                        "Aviation": "M.Memo.Int.Avi",
                        "Marine": "M.Memo.Int.Mar",
                    }
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "M.Memo.Int",
                        "Aviation": "M.Memo.Int.Avi",
                        "Marine": "M.Memo.Int.Mar",
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "M.Memo.Int",
                    }
                },
            },
            "NO (Not Occurring)": None,
        },
    },
    # * 3-39 Biomass CO2 (not necessary, included in 3-1)
    # ##  chapter 4: IPPU
    "Chapter 4 - IPPU": {
        # * 4-1: overview table covering all sectors and gases (no F-gas per gas data)
        "Table 4-1.csv": {
            "cat_col": "Unnamed: 0",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {  # category name appears twice. need to read from
                    # different table
                    "f_rec": {
                        "category": [
                            "Other Process Uses of Carbonates",
                        ]
                    },
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "2",  # not in line with IPCC guidelines
                        "Iron and Steel Production & Metallurgical Coke Production": "2.C.1",  # Metallurgical coke could also go to 1.B.1
                        "Iron and Steel Production": "M.2.C.1.a",
                        "Metallurgical Coke Production": "M.2.C.1.b",
                        "Cement Production": "2.A.1",
                        "Petrochemical Production": "2.B.8",
                        "Ammonia Production": "2.B.1",
                        "Lime Production": "2.A.2",
                        # "Other Process Uses of Carbonates": "",
                        "Other Process Uses of Carbonates": "",
                        "Ceramics Production": "2.A.4.a",
                        "Other Uses of Soda Ash": "2.A.4.b",
                        "Non-Metallurgical Magnesia": "2.A.4.c",
                        "Urea Consumption for Non-Agricultural Purposes": "M.2.B.10.a",
                        "Non-EOR Carbon Dioxide Utilization": "2.H",
                        "Soda Ash Production": "2.B.7",
                        "Glass Production": "2.A.3",
                        "Titanium Dioxide Production": "2.B.6",
                        "Ferroalloy Production": "2.C.2",
                        "Aluminum Production": "2.C.3",
                        "Zinc Production": "2.C.6",
                        "Phosphoric Acid Production": "M.2.B.10.c",
                        "Lead Production": "2.C.5",
                        "Carbide Production and Consumption": "2.B.5",
                        "Substitution of Ozone Depleting Substancesa": "2.F",
                        "Magnesium Production and Processing": "2.C.4",
                    }
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "2",  # not in line with IPCC guidelines
                        "Iron and Steel Production & Metallurgical Coke Production": "2.C.1",  # Metallurgical coke could also go to 1.B.1
                        "Petrochemical Production": "2.B.8",
                        "Ferroalloy Production": "2.C.2",
                        "Carbide Production and Consumption": "2.B.5",
                    }
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "2",  # not in line with IPCC guidelines
                        "Nitric Acid Production": "2.B.2",
                        "N2O from Product Uses": "2.G.3",
                        "Caprolactam, Glyoxal, and Glyoxylic Acid Production": "2.B.4",
                        "Adipic Acid Production": "2.B.3",
                        "Electronics Industry": "2.E",
                    }
                },
            },
            "HFCs": {
                "coords_defaults": {
                    "entity": f"HFCS ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "HFCs": "2",
                        "Substitution of Ozone Depleting Substancesa": "2.F",
                        "Fluorochemical Production": "2.B.9",
                        "Electronics Industry": "2.E",
                        "Magnesium Production and Processing": "2.C.4",
                        "Other Product Manufacture and Use": "2.G",
                    }
                },
            },
            "PFCs": {
                "coords_defaults": {
                    "entity": f"PFCS ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "PFCs": "2",
                        "Substitution of Ozone Depleting Substances": "2.F",
                        "Fluorochemical Production": "2.B.9",
                        "Electronics Industry": "2.E",
                        "Aluminum Production": "2.C.3",
                        "Other Product Manufacture and Use": "2.G.2",  # according to report
                        "Electrical Equipment": "2.G.1",
                    }
                },
            },
            "SF6": {
                "coords_defaults": {
                    "entity": f"SF6 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "SF6": "2",
                        "Fluorochemical Production": "2.B.9",
                        "Electronics Industry": "2.E",
                        "Magnesium Production and Processing": "2.C.4",
                        "Other Product Manufacture and Use": "2.G.2",  # according to report
                        "Electrical Equipment": "2.G.1",
                    }
                },
            },
            "NF3": {
                "coords_defaults": {
                    "entity": f"NF3 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "NF3": "2",
                        "Fluorochemical Production": "2.B.9",
                        "Electronics Industry": "2.E",
                        "Other Product Manufacture and Use": "2.G.2",  # according to report
                    }
                },
            },
            "Total": {  # not exactly the same sector definitions as in CRF / IPCC
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "2",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        "Table 4-14.csv": {
            "cat_col": "Source",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "2.A.4",
                        "Other Uses of Carbonates": "2.A.4.d",
                        "Ceramics Production": "2.A.4.a",
                        "Other Uses of Soda Asha": "2.A.4.b",
                        "Non-Metallurgical Magnesia Production": "2.A.4.c",
                    },
                },
            },
            "a Soda ash consumption not associated with glass manufacturing.": None,
        },
        # * 4-31: Details petrochemical production (optional)
        "Table 4-31.csv": {
            "cat_col": "Source",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "2.B.8",
                        "Carbon Black": "2.B.8.f",
                        "Ethylene": "2.B.8.b",
                        "Ethylene Dichloride": "2.B.8.c",
                        "Ethylene Oxide": "2.B.8.d",
                        "Methanol": "2.B.8.a",
                        "Acrylonitrile": "2.B.8.e",
                    }
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_acr": {
                        "category": [
                            "Acrylonitrile",
                        ]
                    },
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "2.B.8",
                        # "Acrylonitrile": "2.B.8.e",  # data is not shown (+)
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "2.B.8",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        # * 4-33: HFC-22 production
        "Table 4-33.csv": {
            "cat_col": "Gas",
            "HFC-23": {
                "coords_defaults": {
                    "entity": f"HFC23 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "HFC-23": "2.B.9.a",
                    }
                },
            },
        },
        # * 4-35: f-gas production other than HFC-22
        "Table 4-35.csv": {
            "cat_col": "Gas",
            "HFC-23": {
                "coords_defaults": {
                    "category": "2.B.9.b",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "HFC-23": f"HFC23 ({gwp_to_use})",
                        "HFC-143a": f"HFC143a ({gwp_to_use})",
                        "HFC-134a": f"HFC134a ({gwp_to_use})",
                        "HFC-125": f"HFC125 ({gwp_to_use})",
                        "HFC-32": f"HFC32 ({gwp_to_use})",
                        "HFC-227ea": f"HFC227ea ({gwp_to_use})",
                        "Other HFCs": f"UnspMixOfHFCs ({gwp_to_use})",
                        "Perfluorocyclobutane": f"cC4F8 ({gwp_to_use})",
                        "PFC-14 (Perfluoromethane)": f"CF4 ({gwp_to_use})",
                        "Other PFCs": f"UnspMixOfPFCs ({gwp_to_use})",
                        "Nitrogen trifluoride": f"NF3 ({gwp_to_use})",
                        "Sulfur hexafluoride": f"SF6 ({gwp_to_use})",
                        "Total": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        # * 4-38: CO2 from non-EOR Utilization (probably optional)
        "Table 4-38.csv": {
            "cat_col": "Source",
            "Net CO2 from Food and Beverage": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_rec": {
                        "category": [
                            "CO2 Emitted from Food and Beverage",
                            "CO2 Sequestered from Food and Beverage",
                        ]
                    },
                },
                "coords_value_mapping": {
                    "category": {
                        "Net CO2 from Food and Beverage": "2.H.2",
                        "CO2 Emitted from Other Non-EOR Applications": "2.H.3",
                        "Total CO2 Emitted": "2.H",
                    }
                },
            },
            "IE (Included Elsewhere), meaning included in totals.": None,
        },
        # * 4-45: Iron and steel details (optional)
        # * 4-50: Aluminum production gas details (needed for f-gases)
        "Table 4-50.csv": {
            "cat_col": "Gas",
            "CO2": {
                "coords_defaults": {
                    "category": "2.C.3",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "CO2": "CO2",
                        "CF4": f"CF4 ({gwp_to_use})",
                        "C2F6": f"C2F6 ({gwp_to_use})",
                        "Total": f"KYOTOGHG ({gwp_to_use})",
                    }
                },
            },
            "+ Does not exceed 0,05 MMT CO2 Eq.": None,
        },
        # * 4-52: Magnesium production gas details (needed for f-gases)
        "Table 4-52.csv": {
            "cat_col": "Gas",
            "SF6": {
                "coords_defaults": {
                    "category": "2.C.4",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_FK_5-1-12": {
                        "entity": [
                            "FK 5-1-12a",
                        ]
                    },
                },
                "coords_value_mapping": {
                    "entity": {
                        "SF6": f"SF6 ({gwp_to_use})",
                        "CO2": "CO2",
                        "HFC-134a": f"HFC134a ({gwp_to_use})",
                        "Total": f"KYOTOGHG ({gwp_to_use})",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        # * 4-57: electronics industry gas details (needed for f-gases)
        "Table 4-57.csv": {
            "cat_col": "Gas/Source",
            "map_cols": {"Unnamed: 35": "2024"},
            "by_iloc_semicond": {
                "start": 0,
                "end": 13,
                "coords_defaults": {
                    "category": "2.E.1",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_unknown": {
                        "entity": [
                            "C4F6",
                            "C5F8",
                            "CH2F2",
                            "CH3F",
                            "CH2FCF3",
                        ]
                    },
                },
                "coords_value_mapping": {
                    "entity": {
                        "CF4": f"CF4 ({gwp_to_use})",
                        "C2F6": f"C2F6 ({gwp_to_use})",
                        "C3F8": f"C3F8 ({gwp_to_use})",
                        "C4F8": f"cC4F8 ({gwp_to_use})",
                        "HFC-23": f"HFC23 ({gwp_to_use})",
                        "SF6": f"SF6 ({gwp_to_use})",
                        "NF3": f"NF3 ({gwp_to_use})",
                        # "C4F6": f" ({gwp_to_use})",
                        # "C5F8": f" ({gwp_to_use})",
                        # "CH2F2": f" ({gwp_to_use})",
                        # "CH3F": f" ({gwp_to_use})",
                        # "CH2FCF3": f" ({gwp_to_use})",
                        "Total Semiconductors": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "by_iloc_MEMS": {
                "start": 13,
                "end": 21,
                "coords_defaults": {
                    "category": "2.E.5",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "CF4": f"CF4 ({gwp_to_use})",
                        "C2F6": f"C2F6 ({gwp_to_use})",
                        "C3F8": f"C3F8 ({gwp_to_use})",
                        "C4F8": f"cC4F8 ({gwp_to_use})",
                        "HFC-23": f"HFC23 ({gwp_to_use})",
                        "SF6": f"SF6 ({gwp_to_use})",
                        "NF3": f"NF3 ({gwp_to_use})",
                        "Total MEMS": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "by_iloc_PV": {
                "start": 21,
                "end": 28,
                "coords_defaults": {
                    "category": "2.E.3",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "CF4": f"CF4 ({gwp_to_use})",
                        "C2F6": f"C2F6 ({gwp_to_use})",
                        "C4F8": f"cC4F8 ({gwp_to_use})",
                        "HFC-23": f"HFC23 ({gwp_to_use})",
                        "SF6": f"SF6 ({gwp_to_use})",
                        "NF3": f"NF3 ({gwp_to_use})",
                        "Total PV": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "by_iloc_N2O": {
                "start": 28,
                "end": 32,
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {
                    "f_unknown": {
                        "category": [
                            "Total N2O",  # higher resolution in Table 4-1
                        ]
                    },
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O (Semiconductors)": "2.E.1",
                        "N2O (MEMS)": "2.E.5",
                        "N2O (PV)": "2.E.3",
                        # "Total N2O": "2.E",
                    }
                },
            },
            "by_iloc_HTFs": {
                # NOTE: make sure we have a basket copy with default values for this
                # category
                "start": 32,
                "end": 33,
                "coords_defaults": {
                    "entity": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "HFC, PFC and SF6 F-HTFs": "2.E.4",
                    }
                },
            },
            "by_iloc_total": {
                "start": 33,
                "end": 34,
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total Electronics Industry": "2.E",
                    }
                },
            },
        },
        # * 4-59: ODS substitutes (needed for f-gases)
        "Table 4-59.csv": {
            "cat_col": "Gas",
            "map_cols": {"Unnamed: 35": "2024"},
            "HFC-23": {
                "coords_defaults": {
                    "category": "2.F",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {"f_otherPFC": {"entity": ["Other PFCs and HFOsb"]}},
                "coords_value_mapping": {
                    "entity": {
                        "HFC-23": f"HFC23 ({gwp_to_use})",
                        "HFC-32": f"HFC32 ({gwp_to_use})",
                        "HFC-125": f"HFC125 ({gwp_to_use})",
                        "HFC-134a": f"HFC134a ({gwp_to_use})",
                        "HFC-143a": f"HFC143a ({gwp_to_use})",
                        "HFC-236fa": f"HFC236fa ({gwp_to_use})",
                        "CF4": f"CF4 ({gwp_to_use})",
                        "CO2": "CO2",
                        "Other Saturated HFCsa": f"UnspMixOfHFCs ({gwp_to_use})",
                        # "Other PFCs and HFOsb": f"UnspMixOfPFCs ({gwp_to_use})",
                        "Total": f"KYOTOGHG ({gwp_to_use})",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
        # * 4-61: Electrical equipment (needed for f-gases)
        "Table 4-61.csv": {
            "cat_col": "Source/Gas",
            "SF6": {
                "coords_defaults": {
                    "entity": f"SF6 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "SF6": "2.G.1",
                        "Electric Power Systems": "2.G.1.b",
                        "Electrical Equipment Manufacturers": "2.G.1.a",
                    }
                },
            },
            "CF4": {
                "coords_defaults": {
                    "entity": f"CF4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                # TODO: data for details is 0, total not. ignore subsector data
                "coords_value_mapping": {
                    "category": {
                        "CF4": "2.G.1",
                        "Electric Power Systems": "2.G.1.b",
                        "Electrical Equipment Manufacturers": "2.G.1.a",
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"FGASES ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "2.G.1",
                    }
                },
            },
            "Note: Totals may not sum due to independent rounding.": None,
        },
        # * 4-62: Other product use (needed for f-gases)
        "Table 4-62.csv": {
            "cat_col": "Gas/Source",
            "by_iloc_AWACS": {
                "start": 0,
                "end": 2,
                "coords_defaults": {
                    "category": "2.G.2.a.i",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "SF6": f"SF6 ({gwp_to_use})",
                        "Total AWACs": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            # "by_iloc_TOMA": {  # ignore as inconsistent
            #     "start": 2,
            #     "end": 6,
            #     "coords_defaults": {
            #         "category": "2.G.2.a.ii",
            #         "unit": "Mt CO2 / year",
            #     },
            #     "coords_value_mapping": {
            #         "entity": {
            #             "SF6": f"SF6 ({gwp_to_use})",
            #             "PFC": f"UnspMixOfPFCs ({gwp_to_use})",
            #             "NF3": f"NF3 ({gwp_to_use})",
            #             "Total Other Military Applications": f"FGASES ({gwp_to_use})",
            #         }
            #     },
            # },
            # "by_iloc_TPA": {  # ignore as inconsistent
            #     "start": 6,
            #     "end": 9,
            #     "coords_defaults": {
            #         "category": "2.G.2.b",
            #         "unit": "Mt CO2 / year",
            #     },
            #     "coords_value_mapping": {
            #         "entity": {
            #             "SF6": f"SF6 ({gwp_to_use})",
            #             "PFC-14": f"CF4 ({gwp_to_use})",
            #             "Total Particle Accelerators": f"FGASES ({gwp_to_use})",
            #         }
            #     },
            # },
            "by_iloc_TOSA": {
                "start": 9,
                "end": 14,
                "coords_defaults": {
                    "category": "2.G.2.c",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {  # inconsistent with 2.G for 2020
                    "f_hfc": {"entity": ["HFCsa,b"]},
                },
                "coords_value_mapping": {
                    "entity": {
                        "SF6": f"SF6 ({gwp_to_use})",
                        "PFC": f"UnspMixOfPFCs ({gwp_to_use})",
                        "NF3 b": f"NF3 ({gwp_to_use})",
                        # "HFCsa,b": f"HFCS ({gwp_to_use})",
                        "Total Other Scientific Applications": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "by_iloc_OPU": {
                "start": 14,
                "end": 15,
                "coords_defaults": {
                    "category": "2.G.2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "entity": {
                        "Total Other Product Use": f"FGASES ({gwp_to_use})",
                    }
                },
            },
            "+ Does not exceed 0.05 MMT CO2 Eq.": None,
        },
    },
    # ## chapter 5: Agriculture
    "Chapter 5 - Agriculture": {
        # * 5-1: overview. not enough details to map to IPCC categories, but sufficient for
        #     PRIMAP-hist
        "Table 5-1.csv": {
            "cat_col": "Gas/Source",
            "CO2": {
                "coords_defaults": {
                    "entity": "CO2",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CO2": "3",
                        "Liming": "3.G",
                        "Urea Fertilization": "3.H",
                    }
                },
            },
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "3",
                        "Enteric Fermentation": "3.A",
                        "Manure Management": "3.B",
                        "Rice Cultivation": "3.C",
                        "Field Burning of Agricultural Residues": "3.F",
                    }
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "3",
                        "Agricultural Soil Management": "3.A",
                        "Manure Management": "3.B",
                        "Field Burning of Agricultural Residues": "3.F",
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "3",
                    }
                },
            },
            "Note: Totals may not sum due to independent rounding.": None,
        },
        # * 5-3: CH4 enteric fermentation
        "Table 5-3.csv": {
            "cat_col": "Livestock Type",
            "map_cols": {"Unnamed: 35": "2024"},
            "Beef Cattle": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Beef Cattle": "3.A.1.b",
                        "Dairy Cattle": "3.A.1.a",
                        "Swine": "3.A.3",
                        "Horses": "3.A.4.e",
                        "Sheep": "3.A.2",
                        "Goats": "3.A.4.d",
                        "American Bison": "3.A.4.h",
                        "Mules and Asses": "3.A.4.f",
                        "Total": "3.A",
                    }
                },
            },
            "Note: Totals may not sum due to independent rounding.": None,
        },
        # * 5-6: Manure management
        "Table 5-6.csv": {
            "cat_col": "Gas/Animal Type",
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "3.B",
                        "Beef Cattle": "3.B.1.b",
                        "Dairy Cattle": "3.B.1.a",
                        "Swine": "3.B.3",
                        "Poultry": "3.B.4.g",
                        "Horses": "3.B.4.e",
                        "Sheep": "3.B.2",
                        "Goats": "3.B.4.d",
                        "American Bison": "3.B.4.h",
                        "Mules and Asses": "3.B.4.f",
                    }
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "3.B",
                        "Beef Cattle": "3.B.1.b",
                        "Dairy Cattle": "3.B.1.a",
                        "Swine": "3.B.3",
                        "Poultry": "3.B.4.g",
                        "Horses": "3.B.4.e",
                        "Sheep": "3.B.2",
                        "Goats": "3.B.4.d",
                        "American Bison": "3.B.4.h",
                        "Mules and Asses": "3.B.4.f",
                        "Total": "3.B",
                    }
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "3.B",
                    }
                },
            },
            "NA (Not Applicable)": None,
        },
        # * 5-10: Agricultural soils direct and indirect
        "Table 5-10.csv": {
            "cat_col": "Source",
            "Direct": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Direct": "3.D.1",
                        "Indirect": "3.D.2",
                        "Total": "3.D",
                    },
                },
            },
            "Note:Totals may not sum due to independent rounding.": None,
        },
        # * 5-11: liming details (optional, detail not needed)
        # * 5-15: field burning (optional, detail not needed)
    },
    # ## chapter 6: LULUCF
    "Chapter 6 - Land Use, Land Use-Change, and Forestry": {
        # * 6-1: overview (suffices for LULUCF without details)
        "Table 6-1.csv": {
            "cat_col": "Land-Use Category",
            "map_cols": {"Unnamed: 35": "2024"},
            "LULUCF Emissionsf": {
                "coords_defaults": {
                    "category": "4",
                    "unit": "Mt CO2 / year",
                },
                "filter_remove": {"f_nonCO2": {"entity": ["LULUCF Emissionsf"]}},
                "coords_value_mapping": {
                    "entity": {
                        "CH4": f"CH4 ({gwp_to_use})",
                        "N2O": f"N2O ({gwp_to_use})",
                        "LULUCF Carbon Stock Changeg": "CO2",
                        "LULUCF Sector Net Totalh": f"KYOTOGHG ({gwp_to_use})",
                    },
                },
            },
            "a Includes the net changes to carbon stocks stored in all forest ecosystem"
            " pools (estimates include carbon stock changes from drained organic soils "
            "from both forest land remaining forest land and land converted to forest "
            "land) and harvested wood products.": None,
        },
    },
    # for now we don't read the other LULUCf tables as we do not use the detailed data
    # and it is a lot of work to read because some of the tables have no clear
    # gas / sector structure
    # * 6-7: forest fires. needed to split CH4 and N2O
    # * 6-14: grassland fires: needed to split CH4 and N2O
    # * 6-16: peatland remaining peatland: needed for non-CO2
    # ## chapter 7: waste
    "Chapter 7 - Waste": {
        # 7-1: overview: not much detail, but enough for PRIMAP-hist
        "Table 7-1.csv": {
            "cat_col": "Gas/Source",
            "drop_cols": ["90-24 "],
            "CH4": {
                "coords_defaults": {
                    "entity": f"CH4 ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "CH4": "5",
                        "Landfills": "5.A.1",
                        "Wastewater Treatment": "5.D",
                        "Composting": "5.B.1",
                        "Anaerobic Digestion at Biogas Facilities": "5.B.2",
                    },
                },
            },
            "N2O": {
                "coords_defaults": {
                    "entity": f"N2O ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "N2O": "5",
                        "Wastewater Treatment": "5.D",
                        "Composting": "5.B.1",
                    },
                },
            },
            "Total": {
                "coords_defaults": {
                    "entity": f"KYOTOGHG ({gwp_to_use})",
                    "unit": "Mt CO2 / year",
                },
                "coords_value_mapping": {
                    "category": {
                        "Total": "5",
                    },
                },
            },
            "+ Does not exceed 0.5 kt.": None,
        },
    },
}

coords_cols_template = {}

coords_terminologies = {
    "area": "ISO3",
    "category": "CRF2013_2023",
    "scenario": "PRIMAP",
}

coords_defaults_template = {
    "source": "USA-GHGAI",
    "provenance": "measured",
    "area": "USA",
    "scenario": "2026INV",
}

filter_remove = {}

meta_data = {
    "references": "https://ghgi.cgs.umd.edu/index.html",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Greenhouse Gas Inventory and Analysis for the United States",
    "comment": "Read fom csv files by Johannes Gütschow",
    "institution": "University of Maryland - Center for Global Sustainability",
}

time_format = "%Y"

###
# processing
###

terminology_proc = "IPCC2006_PRIMAP"

cat_conversion = {
    "mapping": {
        "0": "0",
        # omit 1 as non-energy use is included
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4.a": "1.A.4.a",
        "1.A.4.b": "1.A.4.b",
        "1.A.5.a.iii": "2.D",  # non energy fuel use
        "1.A.5.a.iv": "M.1.A.5.a.iv",  # waste incineration
        "1.A.5.a.v": "M.1.A.5.a.v",  # US Territories
        "1.B.1.a.i.1": "1.B.1.a.i.1",
        "1.B.1.a.i.2": "1.B.1.a.i.2",
        "1.B.1.a.i.3": "1.B.1.a.i.3",
        "1.B.1.a.i.4": "1.B.1.a.i.4",
        "1.B.1.a.ii.1": "1.B.1.a.ii.1",
        "1.B.1.a.ii.2": "1.B.1.a.ii.2",
        # the subcategories don't really fit as venting and flaring seems to be included
        # in the other subcategories
        "1.B.2.a.i": "1.B.2.a.iii.1",
        "1.B.2.a.ii": "1.B.2.a.iii.2",
        "1.B.2.a.iii": "1.B.2.a.iii.3",
        "1.B.2.a.iv": "1.B.2.a.iii.4",
        "1.B.2.a.vi.1": "1.B.2.a.iii.6",
        "1.B.2.b.i": "1.B.2.b.iii.1",
        "1.B.2.b.ii": "1.B.2.b.iii.2",
        "1.B.2.b.iii": "1.B.2.b.iii.3",
        "1.B.2.b.iv": "1.B.2.b.iii.4",
        "1.B.2.b.v": "1.B.2.b.iii.5",
        "1.B.2.b.vi.1": "1.B.2.b.iii.6.a",
        "1.B.2.b.vi.2": "1.B.2.b.iii.6.b",
        "1.C": "1.C",
        "1.C.1": "1.C.1",
        "1.C.2.a": "1.C.2.a",
        "1.C.2.b": "1.C.2.b",
        # don't map the sums as they don't correspond to IPCC categories
        # "M.1.B.1.a": "M.1.B.1.a",
        # "M.1.B.2.a": "M.1.B.2.a",
        # "M.1.B.2.ab.6": "M.1.B.2.ab.6",
        # "M.1.B.2.b": "M.1.B.2.b",
        # "2": "2", not consistent, 2.D added from 1
        "2.A.1": "2.A.1",
        "2.A.2": "2.A.2",
        "2.A.3": "2.A.3",
        "2.A.4": "2.A.4",
        "2.A.4.a": "2.A.4.a",
        "2.A.4.b": "2.A.4.b",
        "2.A.4.c": "2.A.4.c",
        "2.A.4.d": "2.A.4.d",
        "2.B.1": "2.B.1",
        "2.B.2": "2.B.2",
        "2.B.3": "2.B.3",
        "2.B.4": "2.B.4",
        "2.B.5": "2.B.5",
        "2.B.6": "2.B.6",
        "2.B.7": "2.B.7",
        "2.B.8": "2.B.8",
        "2.B.8.a": "2.B.8.a",
        "2.B.8.b": "2.B.8.b",
        "2.B.8.c": "2.B.8.c",
        "2.B.8.d": "2.B.8.d",
        "2.B.8.e": "2.B.8.e",
        "2.B.8.f": "2.B.8.f",
        "2.B.9": "2.B.9",
        "2.B.9.a": "2.B.9.a",
        "2.B.9.b": "2.B.9.b",
        "M.2.B.10.a": "M.2.B.10.a",
        "M.2.B.10.c": "M.2.B.10.c",
        "2.C.1": "2.C.1",
        "2.C.2": "2.C.2",
        "2.C.3": "2.C.3",
        "2.C.4": "2.C.4",
        "2.C.5": "2.C.5",
        "2.C.6": "2.C.6",
        "2.E": "2.E",
        "2.E.1": "2.E.1",
        "2.E.3": "2.E.3",
        "2.E.4": "2.E.4",
        "2.E.5": "2.E.5",
        "2.F": "2.F",
        "2.G": "2.G",
        "2.G.1": "2.G.1",
        "2.G.1.a": "2.G.1.a",
        "2.G.1.b": "2.G.1.b",
        "2.G.2": "2.G.2",
        "2.G.2.a.i": "2.G.2.a.i",
        "2.G.2.a.ii": "2.G.2.a.ii",
        "2.G.2.b": "2.G.2.b",
        "2.G.2.c": "2.G.2.c",
        "2.G.3": "2.G.3",
        "2.H": "2.H",
        "2.H.2": "2.H.2",
        "2.H.3": "2.H.3",
        "3.A": "3.A.1",
        "3.A.1.a": "3.A.1.a.i",
        "3.A.1.b": "3.A.1.a.ii",
        "3.A.2": "3.A.1.c",
        "3.A.3": "3.A.1.h",
        "3.A.4.d": "3.A.1.d",
        "3.A.4.e": "3.A.1.f",
        "3.A.4.f": "3.A.1.g",
        "3.A.4.h": "3.A.1.j",
        "3.B": "3.A.2",
        "3.B.1.a": "3.A.2.a.i",
        "3.B.1.b": "3.A.2.a.ii",
        "3.B.2": "3.A.2.c",
        "3.B.3": "3.A.2.h",
        "3.B.4.d": "3.A.2.d",
        "3.B.4.e": "3.A.2.f",
        "3.B.4.f": "3.A.2.g",
        "3.B.4.g": "3.A.2.i",
        "3.B.4.h": "3.A.2.j",
        "3.C": "3.C.7",
        "3.D": "M.3.C.45.AG",
        "3.D.1": "M.3.C.4.AG",
        "3.D.2": "M.3.C.5.AG",
        "3.F": "M.3.C.1.AG",
        "3.G": "3.C.2",
        "3.H": "3.C.3",
        "4": "M.LULUCF",
        "5.A.1": "4.A.1",
        "5.B.1": "4.B.1",
        "5.B.2": "4.B.2",
        "5.D": "4.D",
        "M.0.EL": "M.0.EL",
        "M.Memo.Bio": "M.BIO",
        "M.Memo.Int": "M.BK",
        "M.Memo.Int.Avi": "M.BK.A",
        "M.Memo.Int.Mar": "M.BK.M",
    },
    "aggregate": {
        # 1
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b"]},
        "1.A.5.a": {
            "sources": ["M.1.A.5.a.iv", "M.1.A.5.a.v"],
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                ]
            },
        },
        "1.A.5": {
            "sources": ["1.A.5.a"],
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                ]
            },
        },
        "1.A": {
            "sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"],
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                ]
            },
        },
        "1.B.1.a.i": {
            "sources": ["1.B.1.a.i.1", "1.B.1.a.i.2", "1.B.1.a.i.3", "1.B.1.a.i.4"]
        },
        "1.B.1.a.ii": {"sources": ["1.B.1.a.ii.1", "1.B.1.a.ii.2"]},
        "1.B.1.a": {"sources": ["1.B.1.a.i", "1.B.1.a.ii"]},
        "1.B.1": {"sources": ["1.B.1.a"]},
        "1.B.2.a.iii": {
            "sources": [
                "1.B.2.a.iii.1",
                "1.B.2.a.iii.2",
                "1.B.2.a.iii.3",
                "1.B.2.a.iii.4",
                "1.B.2.a.iii.6",
            ]
        },
        "1.B.2.a": {"sources": ["1.B.2.a.iii"]},
        "1.B.2.b.iii.6": {"sources": ["1.B.2.b.iii.6.a", "1.B.2.b.iii.6.b"]},
        "1.B.2.b.iii": {
            "sources": [
                "1.B.2.b.iii.1",
                "1.B.2.b.iii.2",
                "1.B.2.b.iii.3",
                "1.B.2.b.iii.4",
                "1.B.2.b.iii.5",
                "1.B.2.b.iii.6",
            ]
        },
        "1.B.2.b": {"sources": ["1.B.2.b.iii"]},
        "1.B.2": {"sources": ["1.B.2.a", "1.B.2.b"]},
        "1.B": {"sources": ["1.B.1", "1.B.2"]},
        "1.C.2": {"sources": ["1.C.1", "1.C.2"]},
        "1": {
            "sources": ["1.A", "1.B", "1.C"],
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                ]
            },
        },
        # 2
        "2.A": {"sources": ["2.A.1", "2.A.2", "2.A.3", "2.A.4"]},
        "2.B.9": {
            "sources": ["2.B.9.a", "2.B.9.b"],
            "sel": {
                "entity": [
                    "CF4",
                    "cC4F8",
                    "SF6",
                    "NF3",
                    "HFC134a",
                    "HFC125",
                    "HFC143a",
                    "HFC227ea",
                    "HFC23",
                    "HFC32",
                    "UnspMixOfHFCs",
                    "UnspMixOfPFCs",
                    "HFCS",
                    "PFCS",
                ]
            },
        },
        "2.B.10": {"sources": ["M.2.B.10.a", "M.2.B.10.c"]},
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
            ],
            # "sel": {"entity": Not(["KYOTOGHG"])}
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                    "CF4",
                    "cC4F8",
                    "SF6",
                    "NF3",
                    "HFC134a",
                    "HFC125",
                    "HFC143a",
                    "HFC227ea",
                    "HFC23",
                    "HFC32",
                    "UnspMixOfHFCs",
                    "UnspMixOfPFCs",
                    "HFCS",
                    "PFCS",
                ]
            },
        },
        "2.C": {
            "sources": ["2.C.1", "2.C.2", "2.C.3", "2.C.4", "2.C.5", "2.C.6"],
            # "sel": {"entity": Not(["KYOTOGHG"])}
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "C2F6",
                    "CF4",
                    "SF6",
                    "HFC134a",
                    "HFCS",
                    "PFCS",
                ]
            },
        },
        "2.E": {
            "sources": ["2.E.1", "2.E.3", "2.E.4", "2.E.5"],
            "sel": {
                "entity": [
                    # don't merge for N2O, SF6, NF3 as subsector data partly zero
                    "C2F6",
                    "C3F8",
                    "cC4F8",
                    "CF4",
                    "HFC23",
                    "PFCS",
                    "HFCS",
                    # "FGASES",
                ]
            },
        },
        # "2.G.2": {
        #     "sources": ["2.G.2.a.i", "2.G.2.a.ii", "2.G.2.b", "2.G.2.c"],
        #     "sel": {
        #         "entity": [
        #             # don't merge for SF6, NF3, FGASES as subsector data partly inconsistent
        #             "UnspMixOfPFCs", "PFCS",
        #         ]
        #     },
        # },
        "2.G": {"sources": ["2.G.1", "2.G.2", "2.G.3"]},
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"],
            # "sel": {
            #     "entity": Not(
            #         ["KYOTOGHG", "FGASES"]
            #     )
            # }
            "sel": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                    "C2F6",
                    "C3F8",
                    "CF4",
                    "cC4F8",
                    "SF6",
                    "NF3",
                    "HFC134a",
                    "HFC125",
                    "HFC143a",
                    "HFC227ea",
                    "HFC23",
                    "HFC236fa",
                    "HFC32",
                    "UnspMixOfHFCs",
                    "UnspMixOfPFCs",
                    "HFCS",
                    "PFCS",
                ]
            },
            # "tolerance": 0.251,  # rounding inconsistencies in NF3 and PFCs after 2008
        },
        # M.AG
        "3.A.1.a": {"sources": ["3.A.1.a.i", "3.A.1.a.ii"]},
        "3.A.2.a": {"sources": ["3.A.2.a.i", "3.A.2.a.ii"]},
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            # "sel": {"entity": Not(["KYOTOGHG"])},
            "sel": {"entity": ["N2O", "CH4"]},
        },
        "3.C.1": {"sources": ["M.3.C.1.AG"]},
        "3.C.4": {"sources": ["M.3.C.4.AG"]},
        "3.C.5": {"sources": ["M.3.C.5.AG"]},
        "M.3.C.AG": {
            "sources": ["3.C.1", "3.C.2", "3.C.3", "M.3.C.4.AG", "M.3.C.5.AG", "3.C.7"]
        },
        "3.C": {"sources": ["M.3.C.AG"]},
        "M.AG.ELV": {"sources": ["M.3.C.AG"]},
        "M.AG": {
            "sources": ["M.AG.ELV", "3.A"],
            # "sel": {"entity": Not(["KYOTOGHG"])},
            "sel": {"entity": ["N2O", "CH4", "CO2"]},
        },
        # 3
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            # "sel": {"entity": Not(["KYOTOGHG"])},
            "sel": {"entity": ["N2O", "CH4", "CO2"]},
        },
        # 4
        "4.A": {"sources": ["4.A.1"]},
        "4.B": {"sources": ["4.B.1", "4.B.2"]},
        "4": {"sources": ["4.A", "4.B", "4.D"]},
        # consistency check
        "0": {
            "sources": ["1", "2", "3", "4"],
            "sel": {"entity": ["CH4", "N2O", "CO2", "NF3", "SF6", "HFCS", "PFCS"]},
        },
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
    },
}


# we need to copy some f-gas baskets for a few sectors
# basket_copy_PFCS = {
#     "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
#     "entities": ["PFCS"],
#     "source_GWP": gwp_to_use,
#     "sel": {"category": ["2.G.2"]},
# }

basket_copy_UnspMix = {
    "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
    "entities": ["UnspMixOfHFCs", "UnspMixOfPFCs"],
    "source_GWP": gwp_to_use,
    "sel": {"category": ["2.G.2", "2.B.9.b", "2.F"]},  # "2.G.2.a.ii", "2.G.2.c",
}
