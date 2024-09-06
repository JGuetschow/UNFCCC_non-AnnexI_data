"""Config for UZB BTR1 (NIR, no xls files)

General configuration for reading the NIR published as Uzbekistans BTR1.

"""

gwp_to_use = "AR4GWP100"
cat_code_regexp = r"(?P<code>^[a-zA-Z0-9\.]{1,13})\s.*"

## pdf reading config

# there several gas mappings which look useless, but they are necessary
# as the original values use characters that look the same but differ from
# the normal characters and thus the units are not recognized without mapping
table_def_trends = {
    "M0EL_gases": {
        "header": "entity",
        "tables": {
            "21": 0,
        },
        "split_kw": "Year",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.0.EL",
            "unit": "Mt CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                # "HFC": f"HFCS ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%. 2021", "∆(2010-2021)"],
            },
            "fN2O": {  # indirect N2O from manure missing
                "entity": ["N2O", "Total"],
            },
            "fHFC": {  # inconsistent with individual HFCs
                "entity": ["HFC"],
            },
        },
        "replace_str_data": {",": "."},
        "remove_vals": {
            "r1": {  # value inconsistent sector tables
                "entities": ["CO2", "CH4"],
                "filter": {"category": ["M.0.EL"], "time": ["2013"]},
            }
        },
    },
    "GHG_main_sectors": {
        "header": "category",
        "tables": {
            "23": 0,
        },
        "split_kw": "Year",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Mt CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Energy": "1",
                "IPPU": "2",
                # "Agriculture": "M.AG",
                "Waste": "4",
                "Total": "M.0.EL",
                "FOLU": "M.LULUCF",
                "Total (excluding FOLU)": "0",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%, 2021", "∆(2010-2021)"],
            },
            "fAG": {  # indirect N2O from manure missing
                "category": ["Agriculture"],
            },
        },
        "replace_str_data": {" ": ""},
        "remove_vals": {
            "rounding_error": {  # rounding error
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["M.LULUCF"], "time": ["2002"]},
            },
            "r1": {  # value inconsistent sector tables
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["M.0.EL", "1"], "time": ["2013"]},
            },
        },
    },
    "0_prec": {
        "header": "entity",
        "tables": {
            "24": 0,
        },
        "split_kw": "Year",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "0",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "СО": "CO",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
    },
    "energy_gases": {
        "header": "entity",
        "tables": {
            "29": 0,
        },
        "split_kw": "Year",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1",
            "unit": "Mt CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆(1990−2021)"],
            }
        },
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": ["CH4", f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["1"], "time": ["2013"]},
            }
        },
    },
    "energy_prec": {
        "tables": {
            "29": 1,
        },
        "split_kw": "Gas",
        "header": "entity",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "NOх": "NOx",
                "СО": "CO",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            },
            "f2": {
                "entity": ["NMVOCs"],  # inconsistent with inventory and subsectors
            },
        },
    },
    "GHG_energy_sectors": {
        "header": "category",
        "tables": {
            "30": 1,
        },
        "split_kw": "Category",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Mt CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Fuel Combustion": "1.A",
                "Fugitive Emissions": "1.B",
                "Fuel combustion": "1.A",
                "Fugitive emissions": "1.B",
                "Total": "1",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2017)", "%. 2021"],
            }
        },
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["1", "1.B"], "time": ["2013"]},
            },
        },
    },
    "bunkers_gases": {
        "header": "entity",
        "tables": {
            "36": 1,
        },
        "split_kw": ["Year", "Years"],
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.BK.A",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆ (1990-2021)"],
            }
        },
    },
    "bunkers_prec": {
        "tables": {
            "37": 0,
        },
        "split_kw": "Years",
        "header": "entity",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.BK.A",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)"],
            }
        },
        "replace_str_data": {",": "."},
    },
    "MBIO_CO2": {
        "dont_read": True,
        "header": "entity",
        "tables": {
            "38": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.BIO",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)"],
            }
        },
    },  # wrong by a factor of 10 until 2004 (compared to inventory and factor)
    "ffc_gases": {
        "header": "entity",
        "tables": {
            "38": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.A",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%, 2021", "∆(1990-2021)"],
            }
        },
    },
    "ffc_prec": {
        "header": "entity",
        "tables": {
            "39": 2,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.A",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "СО": "CO",  # looks useless, but necessary as special char present
                "NOх": "NOx",  # looks useless, but necessary as special char present
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
        "replace_str_data": {",": "."},
    },
    "GHG_ffc_sectors": {
        "header": "category",
        "tables": {
            "40": 0,
            "41": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Construction": "M.1.A.2.CON",
                "Manufacturing industries": "M.1.A.2.IND",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
        "remove_vals": {
            "r2": {  # GHG sum smaller than CO2 value
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["M.1.A.2.CON"], "time": ["2019", "2020"]},
            },
        },
    },
    "CO2_ffc_sectors": {
        "header": "category",
        "tables": {
            "42": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "CO2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Construction": "M.1.A.2.CON",
                "Manufacturing industries": "M.1.A.2.IND",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
    },
    "CH4_ffc_sectors": {
        "header": "category",
        "tables": {
            "43": 0,
            "44": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"CH4 ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Construction": "M.1.A.2.CON",
                "Manufacturing Industries": "M.1.A.2.IND",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990−2021)", "%, 2021"],
            }
        },
    },
    "N2O_ffc_sectors": {
        "header": "category",
        "tables": {
            "44": 1,
            "45": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"N2O ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Construction": "M.1.A.2.CON",
                "Manufacturing Industries": "M.1.A.2.IND",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
    },
    "CO_ffc_sectors": {
        "header": "category",
        "tables": {
            "45": 1,
            "46": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "CO",
            "unit": "Gg CO / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Manufacturing Industries and Construction": "1.A.2",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
    },
    "NOx_ffc_sectors": {
        "header": "category",
        "tables": {
            "46": 1,
            "47": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "NOx",
            "unit": "Gg NOx / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Manufacturing Industries and Construction": "1.A.2",
                "Transport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990−2021)", "%, 2021"],
            }
        },
    },
    "NMVOC_ffc_sectors": {
        "header": "category",
        "tables": {
            "47": 1,
            "48": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "NMVOC",
            "unit": "Gg NMVOC / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Manufacturing Industries and Construction": "1.A.2",
                "Тransport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990−2021)", "%, 2021"],
            }
        },
    },
    "SO2_ffc_sectors": {
        "dont_read": True,
        "header": "category",
        "tables": {
            "48": 1,
            "49": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "SO2",
            "unit": "t SO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Electricity and Heat Production": "1.A.1",
                "Manufacturing Industries and Construction": "1.A.2",
                "Тransport": "1.A.3",
                "Commercial sector": "1.A.4.a",
                "Residential sector": "1.A.4.b",
                "Agriculture": "1.A.4.c",
                "Total": "1.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990−2021)", "%2021"],
            }
        },
    },  # TODO: inconsistent (parially unit problem?)
    "fugitive_gases": {
        "header": "entity",
        "tables": {
            "55": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆ (1990-2021)"],
            }
        },
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": [f"KYOTOGHG ({gwp_to_use})", "CH4"],
                "filter": {"time": ["2013"]},
            }
        },
    },
    "GHG_fugitive_sectors": {
        "header": "category",
        "tables": {
            "56": 0,
        },
        "split_kw": "Year",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Coal mining": "1.B.1.a",
                "Oil": "1.B.2.a",
                "Natural gas": "1.B.2.b",
                "Total": "1.B",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%. 2021"],
            }
        },
        "remove_vals": {
            "2013_error": {
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["1.B.2.b", "1.B"], "time": ["2013"]},
            },
        },
    },
    "fugitive_prec": {
        "header": "entity",
        "tables": {
            "57": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (2021-1990"],
            }
        },
    },
    "CH4_coal_sectors": {
        "header": "category",
        "tables": {
            "58": 1,
            "59": 0,
        },
        "ffill_rows": [0],
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"CH4 ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Underground Mining": "1.B.1.a.i.1",
                "Underground Later stages": "1.B.1.a.i.2",  # not .3 as that's CO2 only and ere we have CH4 only
                "Underground Sum": "1.B.1.a.i",
                "Surface Mining": "1.B.1.a.ii.1",
                "Surface Later stages": "1.B.1.a.ii.2",
                "Surface Sum": "1.B.1.a.ii",
                "Total": "1.B.1.a",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)"],
            },
        },
        "rows_to_fix": {2: ["Years"]},
    },
    "oil_gases": {  # NMVOC is in Gg
        "header": "entity",
        "tables": {
            "61": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B.2.a",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆ (1990−2021)"],
            },
            "f_temp": {
                "entity": [
                    "NMVOCs, Gg"
                ],  # complicated because of different entity. skip for now
            },
        },
    },
    "GHG_oil_sectors": {
        "dont_read": True,
        "header": "category",
        "tables": {
            "62": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Oil production": "1.B.2.a.iii.2",
                "Oil transportation": "1.B.2.a.iii.3",
                "Total": "1.B.2.a",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990−2021)", "%. 2021"],
            }
        },
    },  # not consistent with inventory (other sector split)
    "oil_prod_gases": {  # NMVOC is in Gg
        "dont_read": True,
        "header": "entity",
        "tables": {
            "63": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B.2.a.iii.2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆ (1990-2021)"],
            },
            "f_temp": {
                "entity": [
                    "NMVOCs, Gg"
                ],  # complicated because of different entity. skip for now
            },
        },
    },  # venting and flaring summed, not compatble with inventory
    "oil_trans_gases": {  # NMVOC is in Gg
        "dont_read": True,
        "header": "entity",
        "tables": {
            "66": 1,
            "67": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B.2.a.iii.3",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%.2021", "∆ (1990-2021)"],
            },
            "f_temp": {
                "entity": [
                    "NMVOCs,Gg"
                ],  # complicated because of different entity. skip for now
            },
        },
    },  # summed with other sectors in inventory
    "gas_gases": {
        "header": "entity",
        "tables": {
            "69": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B.2.b",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆(1990-2021)"],
            },
        },
        "replace_str_data": {" ": ""},
    },
    "gas_prec": {
        "header": "entity",
        "tables": {
            "69": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "1.B.2.b",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
        "replace_str_data": {",": "."},
    },
    "IPPU_gases": {
        "header": "entity",
        "tables": {
            "76": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "Total": f"KYOTOGHG ({gwp_to_use})",
                "HFCs": f"HFCS ({gwp_to_use})",
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%. 2021", "∆ (1990-2021)"],
            },
        },
    },
    "IPPU_prec": {
        "header": "entity",
        "tables": {
            "77": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "СО": "CO",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
    },
    "GHG_IPPU_sectors": {
        "header": "category",
        "tables": {
            "78": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Mineral Industry": "2.A",
                "Chemical industry": "2.B",
                "Metal industry": "2.C",
                "Lubricant use": "2.D.1",
                "HFCs Use": "2.F",
                "Total": "2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
    },
    "CO2_2A_sectors": {
        "header": "category",
        "tables": {
            "81": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "CO2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Cement Production": "2.A.1",
                "Lime Production": "2.A.2",
                "Glass Production": "2.A.3",
                "Ceramics Production": "2.A.4.a",
                "Total": "2.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%, 2021"],
            }
        },
    },
    "2A1_gases": {
        "header": "entity",
        "tables": {
            "82": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.A.1",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "CO2 emissions from Cement Production": "CO2",
                "SO2 emissions from Cement Production": "SO2",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            },
        },
        "replace_str_data": {",": "."},
    },
    "2B_gases": {
        "header": "entity",
        "tables": {
            "92": 0,
            "93": 0,
        },
        "header_remove": [1],
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.B",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СО2,": "CO2",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O,": f"N2O ({gwp_to_use})",
                "Total GHG": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "", "%, 2021"],
            },
            "f2": {"entity": ["CO", "NOx", "SO2", "NMVOCs"]},
        },
    },
    "2B_prec": {
        "header": "entity",
        "tables": {
            "92": 0,
            "93": 0,
        },
        "header_remove": [1],
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.B",
            "unit": "Gg",
        },
        "coords_value_mapping": {"unit": "PRIMAP1", "entity": {"NMVOCs": "NMVOC"}},
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "", "%, 2021"],
            },
            "f2": {"entity": ["СО2,", "CH4", "N2O,", "Total GHG"]},
        },
    },
    "2C_gases": {
        "header": "entity",
        "tables": {
            "107": 0,
        },
        "header_remove": [1],
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.C",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СО2": "CO2",
                "CH4": f"CH4 ({gwp_to_use})",
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            },
            "f2": {"entity": ["CO", "NOx", "SO2", "NMVOCs"]},
        },
        "rows_to_fix": {-2: ["Years"]},
    },
    "2C_prec": {
        "header": "entity",
        "tables": {
            "107": 0,
        },
        "header_remove": [1],
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.C",
            "unit": "Gg",
        },
        "coords_value_mapping": {"unit": "PRIMAP1", "entity": {"NMVOCs": "NMVOC"}},
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            },
            "f2": {"entity": ["СО2", "CH4", "Total"]},
        },
        "rows_to_fix": {-2: ["Years"]},
    },
    "2D_gases": {
        "header": "entity",
        "tables": {
            "115": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.D",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990- 2021)"],
            },
        },
    },
    "2F_HFCs": {
        "header": "entity",
        "tables": {
            "116": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "2.F.1",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "HFC-32": f"HFC32 ({gwp_to_use})",
                "HFC-125": f"HFC125 ({gwp_to_use})",
                "HFC-134a": f"HFC134a ({gwp_to_use})",
                "HFC-143a": f"HFC143a ({gwp_to_use})",
                "Total HFCs": f"HFCS ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)"],
            },
        },
    },
    "2H_NMVOC_sectors": {
        "header": "category",
        "tables": {
            "119": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "NMVOC",
            "unit": "Gg NMVOC / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Subcategory Alcoholic beverages": "M.2.H.2.a",
                "Food products": "M.2.H.2.b",
                "Total": "2.H",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990−2021)", "%. 2021"],
            },
        },
        "rows_to_fix": {2: ["Years"]},
    },  # TODO: subsectors in IPCC cats?
    "MAG_gases": {
        "header": "entity",
        "tables": {
            "123": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.AG",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                # "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%, 2021", "∆(1990-2021)"],
            },
            "fN2O": {  # indirect N2O from manure missing
                "entity": ["N2O", "Total"],
            },
        },
    },
    "GHG_MAG_sectors": {
        "header": "category",
        "tables": {
            "124": 1,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Enteric Fermentation": "3.A.1",
                "Manure Management": "3.A.2",
                "Biomass Burning": "M.3.C.1.AG",
                "N2O Emissions from Managed Soils": "M.AS",  # 3.C.6 included? it's not in Manure management
                "Rice Cultivation": "3.C.7",
                # "Total": "M.AG",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%. 2021"],
            },
            "ftot": {  # indirect N2O from manure missing
                "category": ["Total"],
            },
        },
        "remove_vals": {
            "2020_error": {  # factor of 10 error
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["3.A.2"], "time": ["2020"]},
            },
            "mm_error": {  # doesn't fit gas sum
                "entities": [f"KYOTOGHG ({gwp_to_use})"],
                "filter": {"category": ["3.A.2"], "time": ["2004", "2005"]},
            },
        },
    },
    "CH4_3A1_sectors": {
        "header": "category",
        "tables": {
            "127": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"CH4 ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Dairy Cattle": "3.A.1.a.1",
                "Other Cattle": "3.A.1.a.2",
                "Sheep": "3.A.1.c",
                "Goats": "3.A.1.d",
                "Camels": "3.A.1.e",
                "Horses": "3.A.1.f",
                "Mules and Asses": "3.A.1.g",
                "Swine": "3.A.1.h",
                "Total": "3.A.1",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%, 2021"],
            }
        },
    },
    "CH4_3A2_sectors": {
        "header": "category",
        "tables": {
            "132": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"CH4 ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Dairy cattle": "3.A.2.a.1",
                "Other cattle": "3.A.2.a.2",
                "Sheep": "3.A.2.c",
                "Goats": "3.A.2.d",
                "Camels": "3.A.2.e",
                "Horses": "3.A.2.f",
                "Mules and Asses": "3.A.2.g",
                "Swine": "3.A.2.h",
                "Poultry": "3.A.2.i",
                "Total": "3.A.2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%,2021"],
            }
        },
    },
    "N2O_manure_management": {
        "header": "category",
        "tables": {
            "133": 1,
            "134": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"N2O ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Direct": "3.A.2",
                "Indirect": "3.C.6",
                "Total": "M.AG.MM.DirInd",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
    },
    "N2O_3A2_sectors": {
        "header": "category",
        "tables": {
            "134": 2,
            "135": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"N2O ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Dairy Cattle": "3.A.2.a.1",
                "Other Cattle": "3.A.2.a.2",
                "Dairy cattle": "3.A.2.a.1",
                "Other cattle": "3.A.2.a.2",
                "Sheep": "3.A.2.c",
                "Goats": "3.A.2.d",
                "Camels": "3.A.2.e",
                "Horses": "3.A.2.f",
                "Mules and Asses": "3.A.2.g",
                "Swine": "3.A.2.h",
                "Poultry": "3.A.2.i",
                "Total": "3.A.2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆ (1990-2021)", "%, 2021"],
            }
        },
    },
    "3C1b_gases": {
        "header": "entity",
        "tables": {
            "137": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "3.C.1.b",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {},
    },
    "3C1b_prec": {
        "header": "entity",
        "tables": {
            "138": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "3.C.1.b",
            "unit": "Gg",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "СО": "CO",
            },
        },
        "filter_remove": {},
        "replace_str_data": {",": ""},
    },
    "N2O_soils": {
        "header": "category",
        "tables": {
            "140": 0,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"N2O ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
            #'unit': 'Gg',
        },
        "coords_value_mapping": {
            "category": {
                "Direct emissions Synthetic fertilizers": "3.C.4.a",
                "Organic fertilizers": "3.C.4.b",
                "Livestock grazing": "3.C.4.c",
                "Crop residues": "3.C.4.d",
                "Indirect emissions Atmospheric deposition": "3.C.5.a",
                "Leaching / runoff": "3.C.5.b",
                "Total": "M.3.C.45.AG",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            },
        },
        "rows_to_fix": {2: ["Years"]},
    },
    "CH4_rice": {
        "header": "entity",
        "tables": {
            "144": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "3.C.7",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)"],
            }
        },
    },
    "CO2_land": {
        "header": "category",
        "tables": {
            "148": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": "CO2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Forest land": "3.B.1",
                "Cropland": "3.B.2",
                "Grassland": "3.B.3",
                "Total": "3.B",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%, 2021"],
            }
        },
    },
    "forest_fires_gases_prec": {
        "header": "entity",
        "tables": {
            "152": 1,
        },
        "long_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "M.FF",  # temp, need to find out where it's included
            "unit": "t",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "СН4": "CH4",
                "СО2": "CO2",
            },
        },
        "filter_remove": {
            "f1": {
                "time": ["%, 2021", "∆(1990-2021)"],
            },
        },
        "replace_str_data": {" ": ""},
    },
    "waste_gases": {
        "header": "entity",
        "tables": {
            "166": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "4",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["% 2021", "∆(1990-2021)"],
            },
        },
    },
    "GHG_waste_sectors": {
        "header": "category",
        "tables": {
            "167": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Solid Waste Disposal": "4.A",
                "Industrial Wastewater": "4.D.2",
                "Domestic Wastewater": "4.D.1",
                "Total": "4",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%2021"],
            },
            "f2": {
                "category": [
                    "Industrial Wastewater",
                    "Total",
                ],  # inconsistent with other tables
            },
        },
    },
    "CH4_solid_waste_sectors": {
        "header": "category",
        "tables": {
            "169": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"CH4 ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Municipal": "M.4.A.Mun",
                "Industrial": "M.4.A.Ind",
                "Total": "4.A",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%2021"],
            }
        },
    },
    "wastewater_gases": {
        "header": "entity",
        "tables": {
            "176": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "4.D",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%2021", "∆(1990-2021)"],
            },
        },
    },
    "wastewater_sectors": {
        "header": "category",
        "tables": {
            "177": 1,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "category": "category",
        },
        "coords_defaults": {
            "entity": f"KYOTOGHG ({gwp_to_use})",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "category": {
                "Domestic": "4.D.1",
                "Industrial": "4.D.2",
                "Total": "4.D",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%2021"],
            },
            "fsec": {  # inconsistent with CH4 data
                "category": ["Industrial", "Total"],
            },
        },
    },
    "domestic_ww_gases": {
        "header": "entity",
        "tables": {
            "179": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "4.D.1",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%2021", "∆(1990-2021)"],
            },
        },
    },
    "industrial_ww_gases": {
        "header": "entity",
        "tables": {
            "183": 1,
            "184": 0,
        },
        "split_kw": "Years",
        "long_var": "time",
        "coords_cols": {
            "entity": "entity",
        },
        "coords_defaults": {
            "category": "4.D.2",
            "unit": "Gg CO2 / yr",
        },
        "coords_value_mapping": {
            "entity": {
                "СН4": f"CH4 ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%2021", "∆(1990-2021)"],
            },
        },
    },
}

page_def_trends = {
    "21": {  # M.0.EL, main gases
    },
    "23": {  # main sectors, KYOTOGHG
        # 'flavor': 'stream',
        # 'table_areas': ['83,449,563,134'],
        # 'columns': ['110,155,165,191,214,244,270,301,340,369,401,435,470,503,534'],
        "flavor": "lattice",
        "split_text": True,
    },
    "24": {  # M.0.EL precursors
    },
    "29": {  # Energy, main gases / precursors
    },
    "30": {  # Energy sectors, KyotoGHG
    },
    "36": {  # bunkers, gases
    },
    "37": {  # bunkers, prec
    },
    "38": {  # Bio CO2 / 1.A gases
    },
    "39": {  # 1.A prec
    },
    "40": {  # 1.A sectors, GHG
    },
    "41": {  # 1.A sectors, GHG
    },
    "42": {  # 1.A sectors, CO2
    },
    "43": {  # 1.A sectors, CH4
    },
    "44": {  # 1.A sectors, CH4, N2O
    },
    "45": {  # 1.A sectors, N2O, CO
    },
    "46": {  # 1.A sectors, CO, NOx
    },
    "47": {  # 1.A sectors, NOx, NMVOC
    },
    "48": {  # 1.A sectors, NMVOC, SO2
    },
    "49": {  # 1.A sectors, SO2
    },
    "55": {  # 1.B gases
    },
    "56": {  # 1.B sectors, GHG
    },
    "57": {  # 1.B prec
    },
    "58": {  # 1.B.1.a subsectors CH4
    },
    "59": {  # 1.B.1.a subsectors CH4
    },
    "61": {  # 1.B.2.a gases
    },
    "62": {  # 1.B.2.a subsectors GHG
    },
    "63": {  # 1.B.2.a.iii.2 gases
    },
    "66": {  # 1.B.2.a.iii.3 gases
    },
    "67": {  # 1.B.2.a.iii.3 gases
    },
    "69": {  # 1.B.2.b gases & prec
    },
    "76": {  # IPPU gases
    },
    "77": {  # IPPU prec
    },
    "78": {  # IPPU subsectors, GHG
    },
    "81": {  # 2.A subsectors, CO2
    },
    "82": {  # 2.A1, CO2 SO2
    },
    "92": {  # 2.B, gases and prec
        "flavor": "stream",
        "table_areas": ["37,271,513,113"],
        "columns": ["85,135,183,244,309,360,411,463"],
    },
    "93": {  # 2.B, gases and prec
        "flavor": "stream",
        "table_areas": ["83,771,554,427"],
        "columns": ["122,175,235,294,354,400,450,509"],
    },
    "107": {  # 2.C, gases, prec
        "flavor": "stream",
        "table_areas": ["88,770,551,305"],
        "columns": ["129,184,261,318,382,436,504"],
    },
    "115": {  # 2.D.1, CO2
    },
    "116": {  # 2.F, HFCs
    },
    "119": {  # 2.H, NMVOC
    },
    "123": {  # M.AG, gases
    },
    "124": {  # M.AG sectors, GHG
    },
    "127": {  # 3.A.1 subsectors, CH4
    },
    "132": {  # 3.A.2 subsectors, CH4
    },
    "133": {  # manure management, N2O
    },
    "134": {  # manure management, N2O & 3.A.2 subsectors, N2O
    },
    "135": {  # 3.A.2 subsectors, N2O
    },
    "137": {  # crop residues burning, gases
    },
    "138": {  # crop residues burning, prec
    },
    "140": {  # soils N2O
    },
    "144": {  # rice CH4
    },
    "148": {  # land subsectors, CO2
    },
    "152": {  # forest fires, gases
    },
    "166": {  # waste, gases
    },
    "167": {  # waste, sectors
    },
    "169": {  # Solid waste, sectors
    },
    "176": {  # wastewater, gases
    },
    "177": {  # wastewater subsectors, GHG
    },
    "179": {  # domestic wastewater, gases
    },
    "183": {  # industrial wastewater, gases
    },
    "184": {  # industrial wastewater, gases
    },
}

table_def_inventory = {
    "1990_energy": {
        "time": "1990",
        "unit": "Gg",
        "tables": {
            "187": 0,
            "188": 0,
            "189": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {
            "International Bunkers": "M.BK",
            "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
            "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
            "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
            "CO2 from Biomass Combustion": "M.BIO",
            "CO2 from Biomass Combustion Captured": "M.BIOCCS",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "fcat": {"category": ["Memo Items (3)", "Information Items"]},
        },
        "remove_vals": {
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "1.A.4.a",
                        "1.A.4.b",
                        "1.A.4.c",
                        "1.A.4",
                        "1.B",
                        "1.B.2.a",
                        "1.B.2.b",
                        "1.B.2",
                        "M.BK.A",
                        "1.A.2",
                    ]
                },
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {"category": ["M.BK.A"]},
            },
            "SO2_rounding": {  # rounding errors
                "entities": ["SO2"],
                "filter": {"category": ["1.A.4", "1.A.4.a", "1.A.4.b", "1.A.4.c"]},
            },
        },
    },
    "2010_energy": {
        "time": "2010",
        "unit": "Gg",
        "tables": {
            "189": 1,
            "190": 0,
            "191": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {
            "International Bunkers": "M.BK",
            "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
            "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
            "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
            "CO2 from Biomass Combustion": "M.BIO",
            "CO2 from Biomass Combustion Captured": "M.BIOCCS",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "fcat": {"category": ["Memo Items (3)", "Information Items"]},
        },
        "remove_vals": {
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "1.A.4.a",
                        "1.A.4.b",
                        "1.A.4.c",
                        "1.A.4",
                        "1.A.1",
                        "1.B",
                        "1.B.2.a",
                        "1.B.2.b",
                        "1.B.2",
                        "M.BK.A",
                        "1.A.2",
                    ]
                },
            },
            "NMVOC": {  # reason unclear
                "entities": ["NMVOC"],
                "filter": {"category": ["1.A.4.c"]},
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {
                    "category": [
                        "1.A.4.c",
                        "1.B.1.a.i.2",
                        "1.B.1.a.ii.2",
                        "M.BK.A",
                        "1.A.2",
                    ]
                },
            },
            "SO2_rounding": {  # rounding errors
                "entities": ["SO2"],
                "filter": {"category": ["1.A.4", "1.A.4.a", "1.A.4.b", "1.A.4.c"]},
            },
        },
    },
    "2021_energy": {
        "time": "2021",
        "unit": "Gg",
        "tables": {
            "191": 1,
            "192": 0,
            "193": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {
            "International Bunkers": "M.BK",
            "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
            "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
            "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
            "CO2 from Biomass Combustion": "M.BIO",
            "CO2 from Biomass Combustion Captured": "M.BIOCCS",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {
            "fcat": {"category": ["Memo Items (3)", "Information Items"]},
        },
        "remove_vals": {
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "1.A.4.a",
                        "1.A.4.b",
                        "1.A.4.c",
                        "1.B",
                        "1.B.2.a",
                        "1.B.2.b",
                        "1.B.2",
                        "M.BK.A",
                        "1.A.2",
                    ]
                },
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {"category": ["1.A.4.c", "M.BK.A"]},
            },
        },
    },
    "1990_IPPU": {
        "time": "1990",
        "tables": {
            "194": 0,
            "195": 0,
            "196": 0,
        },
        "unit_row": 0,
        "entity_row": 1,
        "manual_repl_unit": {
            "(Gg)": "Gg",
            "CO2 Equivalents(Gg)": "GgCO2eq",
            "N2O": "Gg",
            "HFCs": "GgCO2eq",
            "PFCs": "GgCO2eq",
            "CO2": "Gg",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2-eq. conversion factors (1)": "GgCO2eq",
            "NOx": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
        "cat_codes_manual": {
            "2.B.10 - Other (Sulphuric Acid) (3)": "M.2.B.10.a",
            "2.B.10 - Other (Formaldehyd) (3)": "M.2.B.10.b",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "PFCs": f"PFCS ({gwp_to_use})",
                "HFCs": f"HFCS ({gwp_to_use})",
                "NF3": f"NF3 ({gwp_to_use})",
                "SF6": f"SF6 ({gwp_to_use})",
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
            },
        },
        "filter_remove": {
            # "fcat": {
            #     "category": ["Memo Items (3)", "Information Items"]
            # },
            "HFCs": {
                "entity": [
                    "Other halogenated gases without  CO2-eq. conversion factors (2)",
                    "Other halogenated gases without CO2-eq. conversion factors (2)",
                ]
            }
        },
        "ffill_rows": [0],
        "remove_vals": {
            "NMVOC_rounding": {  # rounding errors
                "entities": ["NMVOC"],
                "filter": {"category": ["2.C"]},
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {"category": ["2", "2.B"]},
            },
        },
    },
    "2010_IPPU": {
        "time": "2010",
        # unit is in header. We need a header def here
        "tables": {
            "196": 1,
            "197": 0,
            "198": 0,
        },
        "unit_row": 0,
        "entity_row": 1,
        "manual_repl_unit": {
            "(Gg)": "Gg",
            "CO2 Equivalents(Gg)": "GgCO2eq",
            "N2O": "Gg",
            "HFCs": "GgCO2eq",
            "PFCs": "GgCO2eq",
            "CO2": "Gg",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2-eq. conversion factors (1)": "GgCO2eq",
            "NOx": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
        "cat_codes_manual": {
            "2.B.10 - Other (Sulphuric Acid) (3)": "M.2.B.10.a",
            "2.B.10 - Other (Formaldehyd) (3)": "M.2.B.10.b",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "PFCs": f"PFCS ({gwp_to_use})",
                "HFCs": f"HFCS ({gwp_to_use})",
                "NF3": f"NF3 ({gwp_to_use})",
                "SF6": f"SF6 ({gwp_to_use})",
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
            },
        },
        "filter_remove": {
            # "fcat": {
            #     "category": ["Memo Items (3)", "Information Items"]
            # },
            "HFCs": {
                "entity": [
                    "Other halogenated gases without  CO2-eq. conversion factors (2)",
                    "Other halogenated gases without CO2-eq. conversion factors (2)",
                ]
            }
        },
        "ffill_rows": [0],
        "remove_vals": {
            "NMVOC_rounding": {  # rounding errors (2.B sum error)
                "entities": ["NMVOC"],
                "filter": {"category": ["2.C", "2.B"]},
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {"category": ["2", "2.B"]},
            },
        },
    },
    "2021_IPPU": {
        "time": "2021",
        # 'unit': 'Gg',
        # unit is in header. We need a header def here
        "tables": {
            "199": 0,
            "200": 0,
            "201": 0,
        },
        "unit_row": 0,
        "entity_row": 1,
        "manual_repl_unit": {
            "(Gg)": "Gg",
            "CO2 Equivalents(Gg)": "GgCO2eq",
            "N2O": "Gg",
            "HFCs": "GgCO2eq",
            "PFCs": "GgCO2eq",
            "CO2": "Gg",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2-eq. conversion factors (1)": "GgCO2eq",
            "NOx": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
        "cat_codes_manual": {
            "2.B.10 - Other (Sulphuric Acid) (3)": "M.2.B.10.a",
            "2.B.10 - Other (Formaldehyd) (3)": "M.2.B.10.b",
        },
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "NMVOCs": "NMVOC",
                "PFCs": f"PFCS ({gwp_to_use})",
                "HFCs": f"HFCS ({gwp_to_use})",
                "NF3": f"NF3 ({gwp_to_use})",
                "SF6": f"SF6 ({gwp_to_use})",
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
            },
        },
        "filter_remove": {
            # "fcat": {
            #     "category": ["Memo Items (3)", "Information Items"]
            # },
            "HFCs": {
                "entity": [
                    "Other halogenated gases without  CO2-eq. conversion factors (2)",
                    "Other halogenated gases without CO2-eq. conversion factors (2)",
                ]
            }
        },
        "ffill_rows": [0],
        "remove_vals": {
            "NMVOC_rounding": {  # 2.B sum error
                "entities": ["NMVOC"],
                "filter": {"category": ["2.B"]},
            },
            "CH4_rounding": {
                "entities": ["CH4"],
                "filter": {"category": ["2.C"]},
            },
        },
    },
    "1990_AFOLU": {
        "time": "1990",
        "unit": "Gg",
        "tables": {
            "202": 0,
            "203": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "Net CO2 emissions / removals": "CO2",
                "CH4": "CH4",
                "Emissions CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "Emissions NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {},
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": ["CO2"],
                "filter": {"category": ["3.B.1", "3.B.2", "3.B.3"]},
            },
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "3.A.2.c",
                        "3.A.2.d",
                        "3.A.2.e",
                        "3.A.2.f",
                        "3.A.2.g",
                        "3.A.2.h",
                        "3.A.2.i",
                        "3.C.1.b",
                        "3.C.1",
                    ]
                },
            },
            "CH4_rounding": {  # rounding errors
                "entities": ["CH4"],
                "filter": {
                    "category": [
                        "3.A.2.e",
                        "3.A.2.f",
                        "3.A.2.g",
                        "3.C.1",  # sum error
                    ]
                },
            },
        },
    },
    "2010_AFOLU": {
        "time": "2010",
        "unit": "Gg",
        "tables": {
            "204": 0,
            "205": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "Net CO2 emissions / removals": "CO2",
                "CH4": "CH4",
                "Emissions CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "Emissions NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {},
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": ["NOx", "CO"],
                "filter": {"category": ["3.B.1"]},
            },
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "3.A.2.d",
                        "3.A.2.e",
                        "3.A.2.f",
                        "3.A.2.g",
                        "3.A.2.h",
                    ]
                },
            },
            "CH4_rounding": {  # rounding errors
                "entities": ["CH4"],
                "filter": {
                    "category": [
                        "3.A.2.e",
                        "3.A.1.h",
                        "3.A.2.h",
                    ]
                },
            },
        },
    },
    "2021_AFOLU": {
        "time": "2021",
        "unit": "Gg",
        "tables": {
            "206": 0,
            "207": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "Net CO2 emissions / removals": "CO2",
                "CH4": "CH4",
                "Emissions CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "Emissions NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
            },
        },
        "filter_remove": {},
        "remove_vals": {
            "r1": {  # value inconsistent with fugitive table
                "entities": ["NOx", "CO"],
                "filter": {"category": ["3.B.1"]},
            },
            "N2O_rounding": {  # rounding errors
                "entities": ["N2O"],
                "filter": {
                    "category": [
                        "3.A.2.d",
                        "3.A.2.e",
                        "3.A.2.f",
                        "3.A.2.g",
                        "3.A.2.h",
                    ]
                },
            },
            "CH4_rounding": {  # rounding errors
                "entities": ["CH4"],
                "filter": {"category": ["3.A.1.h", "3.A.2.e", "3.A.2.g", "3.A.2.h"]},
            },
        },
    },
    "1990_waste": {
        "time": "1990",
        "unit": "Gg",
        "tables": {
            "208": 0,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "CO2": "CO2",
                "CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
                "SO2": "SO2",
            },
        },
        "filter_remove": {},
    },
    "2010_waste": {
        "time": "2010",
        "unit": "Gg",
        "tables": {
            "208": 1,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "CO2": "CO2",
                "CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
                "SO2": "SO2",
            },
        },
        "filter_remove": {},
    },
    "2021_waste": {
        "time": "2021",
        "unit": "Gg",
        "tables": {
            "208": 2,
        },
        "unit_row": 0,
        "entity_row": 0,
        "cat_codes_manual": {},
        "coords_value_mapping": {
            "unit": "PRIMAP1",
            "entity": {
                "CO2": "CO2",
                "CH4": "CH4",
                "N2O": "N2O",
                "NOx": "NOx",
                "CO": "CO",
                "NMVOCs": "NMVOC",
                "SO2": "SO2",
            },
        },
        "filter_remove": {},
    },
}

page_def_inventory = {
    "187": {  # 1990, energy 1
        # unit: Gg
    },
    "188": {  # 1990, energy 2
        # unit: Gg
    },
    "189": {  # 1990, energy 3 / 2010, energy 1
        # unit: Gg
    },
    "190": {  # 2010, energy 2
        # unit: Gg
    },
    "191": {  # 2010, energy 3 / 2021, energy 1
        "split_text": True,
        # unit: Gg
    },
    "192": {  # 2021, energy 2
        # unit: Gg
    },
    "193": {  # 2021, energy 3
        # unit: Gg
    },
    "194": {  # 1990, IPPU 1
        # unit: header
    },
    "195": {  # 1990, IPPU 2
        "flavor": "stream",
        "table_areas": ["50,513,789,56"],
        "columns": ["287,323,355,383,410,438,466,495,566,638,679,714,754"],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            }
        },
    },
    "196": {  # 1990, IPPU 3 / 2010, IPPU 1
        "flavor": "stream",
        "table_areas": ["50,513,789,330", "50,303,789,50"],
        "columns": [
            "287,323,355,383,410,438,466,495,566,638,679,714,754",
            "287,323,355,383,410,438,466,495,566,638,679,714,754",
        ],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            },
            1: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            },
        },
    },
    "197": {  # 2010, IPPU 2
        "flavor": "stream",
        "table_areas": ["50,513,789,56"],
        "columns": ["287,323,355,383,410,438,466,495,566,638,679,714,754"],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            }
        },
    },
    "198": {  # 2010, IPPU 3
        "flavor": "stream",
        "table_areas": ["50,513,789,153"],
        "columns": ["287,323,355,383,410,438,466,495,566,638,679,714,754"],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            }
        },
    },
    "199": {  # 2021, IPPU 1
        "flavor": "lattice",
        # unit: header
    },
    "200": {  # 2021, IPPU 2
        "flavor": "stream",
        "table_areas": ["50,513,789,53"],
        "columns": ["287,323,355,383,410,438,466,495,566,638,679,714,754"],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            }
        },
    },
    "201": {  # 2010, IPPU 3
        "flavor": "stream",
        "table_areas": ["50,513,789,320"],
        "columns": ["287,323,355,383,410,438,466,495,566,638,679,714,754"],
        # unit: header
        "table_config": {
            0: {
                "rows_to_fix": {-5: ["Categories"]},
                "bfill_header": [0, 1],
            }
        },
    },
    "202": {  # 1990, AFOLU 1
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {2: ["Categories"]},
            }
        },
    },
    "203": {  # 1990, AFOLU 2
        "flavor": "stream",
        "table_areas": ["81,787,556,233"],
        "columns": ["291,353,394,433,475,515"],
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {-4: ["Categories"]},
            }
        },
    },
    "204": {  # 2010, AFOLU 1
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {2: ["Categories"]},
            }
        },
    },
    "205": {  # 2010, AFOLU 2
        "flavor": "stream",
        "table_areas": ["81,787,556,233"],
        "columns": ["291,353,394,433,475,515"],
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {-4: ["Categories"]},
            }
        },
    },
    "206": {  # 2021, AFOLU 1
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {2: ["Categories"]},
            }
        },
    },
    "207": {  # 2021, AFOLU 2
        "flavor": "stream",
        "table_areas": ["81,787,556,233"],
        "columns": ["291,353,394,433,475,515"],
        # unit: Gg
        "table_config": {
            0: {
                "rows_to_fix": {-4: ["Categories"]},
            }
        },
    },
    "208": {  # Waste, 1990, 2010, 2021
        # unit: Gg
    },
}

config_general = {
    "time_format": "%Y",
    "coords_defaults": {
        "area": "UZB",
        "source": "UZB-GHG-Inventory",
        "provenance": "measured",
        "scenario": "BTR1",
    },
    "coords_terminologies": {
        "area": "ISO3",
        "category": "IPCC2006_PRIMAP",
        "scenario": "PRIMAP",
    },
    "meta_data": {
        "rights": "",
        "references": "https://unfccc.int/documents/640099",
        "contact": "mail@johannes-guetschow.de",
        "title": "NATIONAL REPORT - Inventory of anthropogenic emissions sources and sinks of greenhouse gases in the Republic of Uzbekistan 1990-2021",
        "comment": "Read fom pdf file by Johannes Gütschow",
        "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
    },
}


aggregate_coords = {
    f"category ({config_general['coords_terminologies']['category']})": {
        "1.A.2": {
            "sources": ["M.1.A.2.CON", "M.1.A.2.IND"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O", f"KYOTOGHG ({gwp_to_use})"],
            },
        },
        "1.A.4": {
            "sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"],
            "filter": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                    f"KYOTOGHG ({gwp_to_use})",
                    "SO2",
                    "NMVOC",
                    "CO",
                    "NOx",
                ],
            },
        },
        "1.B.1": {
            "sources": ["1.B.1.a"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "1.B.2": {
            "sources": ["1.B.2.a", "1.B.2.b"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "1.B": {
            "sources": ["1.B.1", "1.B.2", "1.B.3"],
            "filter": {
                "entity": ["CH4"],
                "time": ["2013"],
            },
        },
        "1": {
            "sources": ["1.A", "1.B", "1.C"],
            "filter": {
                "entity": ["CH4"],
                "time": ["2013"],
            },
        },
        "2.F": {
            "sources": ["2.F.1"],
            "filter": {
                "entity": ["HFC125", "HFC134a", "HFC143a", "HFC32"],
            },
        },
        "2": {
            "sources": ["2.F"],
            "filter": {
                "entity": ["HFC125", "HFC134a", "HFC143a", "HFC32"],
            },
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "3.C.1": {
            "sources": ["3.C.1.a", "3.C.1.b"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.3.C.1.LU": {
            "sources": ["3.C.1.a"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        # "3.C": {"sources": [
        #     "3.C.1", "3.C.4", "3.C.5", "3.C.6", "3.C.7", "3.C.8", "3.C.9",
        #     "3.C.10", "3.C.11", "3.C.12", "3.C.13"]},
        "3.C": {
            "sources": [  # build from available time-series not inventory
                "3.C.1",
                "M.3.C.45.AG",
                "3.C.6",
                "3.C.7",
            ],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.3.C.AG": {
            "sources": [  # build from available time-series not inventory
                "M.3.C.1.AG",
                "M.3.C.45.AG",
                "3.C.6",
                "3.C.7",
            ],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.AG": {  # consistency check
            "sources": ["M.AG.ELV", "3.A"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "M.LULUCF": {
            "sources": ["3.B", "3.D", "M.3.C.1.LU"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O"],
            },
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            "filter": {
                "entity": ["CH4", "CO2", "N2O", f"KYOTOGHG ({gwp_to_use})"],
            },
        },
        "0": {  # consistency check
            "sources": ["1", "2", "3", "4"],
            "filter": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                    "HFC125",
                    "HFC134a",
                    "HFC143a",
                    "HFC32",
                    f"UnspMixOfHFCs ({gwp_to_use})",
                ],
            },
        },
        "M.0.EL": {  # consistency check
            "sources": ["1", "2", "M.AG", "4"],
            "filter": {
                "entity": [
                    "CH4",
                    "CO2",
                    "N2O",
                    "HFC125",
                    "HFC134a",
                    "HFC143a",
                    "HFC32",
                    f"UnspMixOfHFCs ({gwp_to_use})",
                ],
            },
        },
    }
}

basket_copy = {
    "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
    "entities": ["UnspMixOfHFCs", "PFCS"],
    "source_GWP": gwp_to_use,
}

gas_baskets = {
    "HFCS (SARGWP100)": [
        "HFC125",
        "HFC134a",
        "HFC143a",
        "HFC32",
        "UnspMixOfHFCs (SARGWP100)",
    ],
    "HFCS (AR4GWP100)": [
        "HFC125",
        "HFC134a",
        "HFC143a",
        "HFC32",
        "UnspMixOfHFCs (AR4GWP100)",
    ],
    "HFCS (AR5GWP100)": [
        "HFC125",
        "HFC134a",
        "HFC143a",
        "HFC32",
        "UnspMixOfHFCs (AR5GWP100)",
    ],
    "HFCS (AR6GWP100)": [
        "HFC125",
        "HFC134a",
        "HFC143a",
        "HFC32",
        "UnspMixOfHFCs (AR6GWP100)",
    ],
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)", "PFCS (SARGWP100)", "SF6", "NF3"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)", "PFCS (AR4GWP100)", "SF6", "NF3"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)", "PFCS (AR5GWP100)", "SF6", "NF3"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)", "PFCS (AR6GWP100)", "SF6", "NF3"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
