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
                "Total": f"KYOTGHG ({gwp_to_use})",
                "HFC": f"HFCS ({gwp_to_use})",
                "CH4": f"CH4 ({gwp_to_use})",
                "N2O": f"N2O ({gwp_to_use})",
                "СО2": "CO2",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%. 2021", "∆(2010-2021)"],
            }
        },
        "replace_str_data": {",": "."},
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
                "Agriculture": "M.AG",
                "Waste": "4",
                "Total": "M.0.EL",
                "FOLU": "M.LULUCF",
                "Total (excluding FOLU)": "0",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%, 2021", "∆(2010-2021)"],
            }
        },
        "replace_str_data": {" ": ""},
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
            }
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
            }
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
    },
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
    # 'SO2_ffc_sectors': {
    #     'header': 'category',
    #     'tables': {
    #         '48': 1,
    #         '49': 0,
    #     },
    #     'long_kw': 'Years',
    #     'long_var': 'time',
    #     "coords_cols": {
    #         "category": "category",
    #     },
    #     "coords_defaults": {
    #         'entity': 'SO2',
    #         'unit': 't SO2 / yr',
    #     },
    #     "coords_value_mapping": {
    #         "category": {
    #             'Electricity and Heat Production': '1.A.1',
    #             'Manufacturing Industries and Construction': '1.A.2',
    #             'Тransport': '1.A.3',  # noqa: RUF003
    #             'Commercial sector': '1.A.4.a',
    #             'Residential sector': '1.A.4.b',
    #             'Agriculture': '1.A.4.c',
    #             'Total': '1.A',
    #         }
    #     },
    #     "filter_remove": {
    #         "f1": {
    #             "time": ["∆(1990−2021)", "%2021"],  # noqa: RUF003
    #         }
    #     },
    # },  # TODO: inconsistent (parially unit problem?)
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
    },
    "oil_prod_gases": {  # NMVOC is in Gg
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
    },
    "oil_trans_gases": {  # NMVOC is in Gg
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
    },
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
                "Total": f"KYOTGHG ({gwp_to_use})",
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
                "Total": f"KYOTOGHG ({gwp_to_use})",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["%, 2021", "∆(1990-2021)"],
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
                "Enteric Fermentation": "3.A",
                "Manure Management": "3.A.2",
                "Biomass Burning": "M.3.C.AG",
                "N2O Emissions from Managed Soils": "M.AS",  # 3.C.6 included? it's not in Manure management
                "Rice Cultivation": "3.C.7",
                "Total": "M.AG",
            }
        },
        "filter_remove": {
            "f1": {
                "time": ["∆(1990-2021)", "%. 2021"],
            }
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
            }
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
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"OtherHFCS ({gwp_to_use})",
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
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"OtherHFCS ({gwp_to_use})",
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
                "Other halogenated gases with CO2-eq. conversion factors (1)": f"OtherHFCS ({gwp_to_use})",
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


#######################3

# for processing
terminology_proc = "IPCC2006_PRIMAP"

cat_conversion = {
    "mapping": {
        "1.A.1.a.i": "1.A.1.a.i",  # 1A1ai_Public_Electricity&Heat_Production
        "1.A.1.a.iii": "1.A.1.a.iii",  # 1A1aiii_Public_Heat_Production
        "1.A.1.b": "1.A.1.b",  # 1A1b_Petroleum_Refining
        "1.A.1.c.i": "1.A.1.c.i",  # 1A1ci_Manufacture_of_solid_fuels
        "1.A.1.c.ii": "1.A.1.c.ii",  # 1A1cii_Oil_and_gas_extraction
        "1.A.1.c.iii": "1.A.1.c.iii",  # 1A1ciii_Other_energy_industries
        "1.A.2.a": "1.A.2.a",  # 1A2a_Iron_and_steel
        "1.A.2.b": "1.A.2.b",  # 1A2b_Non-Ferrous_Metals
        "1.A.2.c": "1.A.2.c",  # 1A2c_Chemicals
        "1.A.2.d": "1.A.2.d",  # 1A2d_Pulp_Paper_Print
        "1.A.2.e": "1.A.2.e",  # 1A2e_food_processing_beverages_and_tobacco
        "1.A.2.f": "1.A.2.f",  # 1A2f_Non-metallic_minerals
        "1.A.2.g.iii": "1.A.2.i",  # 1A2giii_Mining_and_quarrying
        "1.A.2.g.v": "1.A.2.k",  # 1A2gv_Construction
        "1.A.2.g.vii": "1.A.2.m.i",  # 1A2gvii_Off-road_vehicles_and_other_machinery
        "1.A.2.g.v.iii": "1.A.2.m.ii",  # 1A2gviii_Other_manufacturing_industries_and_construction
        "1.A.3.a": "1.A.3.a.ii",  # 1A3a_Domestic_aviation
        "1.A.3.b.i": "1.A.3.b.i",  # 1A3bi_Cars
        "1.A.3.b.ii": "1.A.3.b.ii",  # 1A3bii_Light_duty_trucks
        "1.A.3.b.iii": "1.A.3.b.iii",  # 1A3biii_Heavy_duty_trucks_and_buses
        "1.A.3.b.iv": "1.A.3.b.iv",  # 1A3biv_Motorcycles
        "1.A.3.b.v": "M.1.A.3.b.v",  # 1A3bv_Other_road_transport (no direct match in IPCC2006)
        "1.A.3.c": "1.A.3.c",  # 1A3c_Railways
        "1.A.3.d": "1.A.3.d.ii",  # 1A3d_Domestic_navigation
        "1.A.3.e.ii": "1.A.3.e.ii",  # 1A3eii_Other_Transportation (subsector consistent with CRF reporting)
        "1.A.4.a.i": "1.A.4.a.i",  # 1A4ai_Commercial/Institutional (stationary)
        "1.A.4.a.ii": "1.A.4.a.ii",  # 1A4aii_Commercial/Institutional_Mobile
        "1.A.4.b.i": "1.A.4.b.i",  # 1A4bi_Residential_stationary
        "1.A.4.b.ii": "1.A.4.b.ii",  # 1A4bii_Residential:Off-road
        "1.A.4.c.i": "1.A.4.c.i",  # 1A4ci_Agriculture/Forestry/Fishing:Stationary
        "1.A.4.c.ii": "1.A.4.c.ii",  # 1A4cii_Agriculture/Forestry/Fishing:Off-road
        "1.A.4.c.iii": "1.A.4.c.iii",  # 1A4ciii_Fishing
        "1.A.5.b": "1.A.5.b",  # 1A5b_Other:Mobile
        "1.B.1.a.i.1": "1.B.1.a.i.1",  # 1B1ai_Underground_mines:Mining_activities
        "1.B.1.a.i.2": "1.B.1.a.i.2",  # 1B1ai_Underground_mines:Post-mining_activities
        "1.B.1.a.i.3": "1.B.1.a.i.3",  # 1B1ai_Underground_mines:Abandoned
        "1.B.1.a.ii.1": "1.B.1.a.ii.1",  # 1B1aii_Surface_mines:Mining_activities
        "1.B.1.b": "1.B.1.c",  # 1B1b_Solid_Fuel_Transformation
        "1.B.2.a.1": "1.B.2.a.iii.1",  # 1B2a1_Oil_exploration
        "1.B.2.a.2": "1.B.2.a.iii.2",  # 1B2a2_Oil_Production
        "1.B.2.a.3": "1.B.2.a.iii.3",  # 1B2a3_Oil_transport
        "1.B.2.a.4": "1.B.2.a.iii.4",  # 1B2a4_Oil_refining/storage
        "1.B.2.a.6": "1.B.2.a.iii.6",  # 1B2a6_Oil_Production
        "1.B.2.b.1": "1.B.2.b.iii.1",  # 1B2b1_Gas_exploration
        "1.B.2.b.2": "1.B.2.b.iii.2",  # 1B2b2_Gas_production
        "1.B.2.b.3": "1.B.2.b.iii.3",  # 1B2b3_Gas_processing
        "1.B.2.b.4": "1.B.2.b.iii.4",  # 1B2b4_Gas_transmission_and_storage
        "1.B.2.b.5": "1.B.2.b.iii.5",  # 1B2b5_Gas_distribution
        "1.B.2.c-ven.i": "1.B.2.a.i",  # 1B2c_Venting_Oil
        "1.B.2.c-ven.ii": "1.B.2.b.i",  # 1B2c_Venting_Gas
        "1.B.2.c-fla.i": "1.B.2.a.ii",  # 1B2c_Flaring_Oil
        "1.B.2.c-fla.ii": "1.B.2.b.ii",  # 1B2c_Flaring_Gas
        "1.B.2.d": "1.B.3.b",  # 1B2d_Other_energy_industries
        "2.A.1": "2.A.1",  # 2A1_Cement_Production
        "2.A.2": "2.A.2",  # 2A2_Lime_Production
        "2.A.3": "2.A.3",  # 2A3_Glass_production
        "2.A.4.a": "2.A.4.a",  # 2A4a_Other_process_uses_of_carbonates:ceramics
        "2.A.4.b": "2.A.4.b",  # 2A4b_Other_uses_of_Soda_Ash
        "2.A.4.d": "2.A.4.d",  # 2A4d_Other_process_uses_of_carbonates:other
        "2.B.1": "2.B.1",  # 2B1_Chemical_Industry:Ammonia_production
        "2.B.10": "2.B.10",  # 2B10_Chemical_Industry:Other
        "2.B.2": "2.B.2",  # 2B2_Nitric_Acid_Production
        "2.B.3": "2.B.3",  # 2B3_Adipic_Acid_Production
        "2.B.6": "2.B.6",  # 2B6_Titanium_dioxide_production
        "2.B.7": "2.B.7",  # 2B7_Soda_Ash_Production
        "2.B.8.a": "2.B.8.a",  # 2B8a_Methanol_production
        "2.B.8.b": "2.B.8.b",  # 2B8b_Ethylene_Production
        "2.B.8.c": "2.B.8.c",  # 2B8c_Ethylene_Dichloride_and_Vinyl_Chloride_Monomer
        "2.B.8.d": "2.B.8.d",  # 2B8d_Ethylene_Oxide
        "2.B.8.e": "2.B.8.e",  # 2B8e_Acrylonitrile
        "2.B.8.f": "2.B.8.f",  # 2B8f_Carbon_black_production
        "2.B.8.g": "2.B.8.g",  # 2B8g_Petrochemical_and_carbon_black_production:Other
        "2.B.9.a.i": "2.B.9.a.i",  # 2B9a1_Fluorchemical_production:By-product_emissions
        "2.B.9.b.iii": "2.B.9.b.iii",  # 2B9b3_Fluorchemical_production:Fugitive_emissions
        "2.C.1.a": "2.C.1.a",  # 2C1a_Steel
        "2.C.1.b": "2.C.1.b",  # 2C1b_Pig_iron
        "2.C.1.d": "2.C.1.d",  # 2C1d_Sinter
        "2.C.3.a": "2.C.3.a",  # 2C3_Aluminium_Production
        "2.C.3.b": "2.C.3.b",  # 2C3_Aluminium_Production
        "2.C.4": "2.C.4",  # 2C4_Magnesium_production
        "2.C.6": "2.C.6",  # 2C6_Zinc_Production
        "2.D.1": "2.D.1",  # 2D1_Lubricant_Use
        "2.D.2": "2.D.2",  # 2D2 Non-energy_products_from_fuels_and_solvent_use:Paraffin_wax_use
        "2.D.3": "2.D.3",  # 2D3_Other_NEU
        "2.E.1": "2.E.1",  # 2E1_Integrated_circuit_or_semiconductor
        "2.F.1.a": "M.2.F.1.a.i",  # 2F1a_Commercial_refrigeration
        "2.F.1.b": "M.2.F.1.a.ii",  # 2F1b_Domestic_refrigeration
        "2.F.1.c": "M.2.F.1.a.iii",  # 2F1c_Industrial_refrigeration
        "2.F.1.d": "M.2.F.1.a.iv",  # 2F1d_Transport_refrigeration
        "2.F.1.e": "2.F.1.b",  # 2F1e_Mobile_air_conditioning
        "2.F.1.f": "M.2.F.1.a.v",  # 2F1f_Stationary_air_conditioning
        "2.F.2.a": "M.2.F.2.a",  # 2F2a_Closed_foam_blowing_agents (not in CRF2023_2023)
        "2.F.2.b": "M.2.F.2.b",  # 2F2b_Open_foam_blowing_agents (not in CRF2023_2023)
        "2.F.3": "2.F.3",  # 2F3_Fire_Protection
        "2.F.4.a": "M.2.F.4.a",  # 2F4a_Metered_dose_inhalers
        "2.F.4.b": "M.2.F.4.b",  # 2F4b_Aerosols:Other
        "2.F.5": "2.F.5",  # 2F5_Solvents
        "2.F.6.b": "2.F.6.b",  # 2F6b_Other_Applications:Contained-Refrigerant_containers
        "2.G.1": "2.G.1",  # 2G1_Electrical_equipment
        "2.G.2.a": "2.G.2.a",  # 2G2_Military_applications
        "2.G.2.b": "2.G.2.b",  # 2G2_Particle_accelerators
        "2.G.2.e": "M.2.G.2.c.i",  # 2G2e_Electronics_and_shoes
        "2.G.3.a": "2.G.3.a",  # 2G3a_Medical aplications
        "2.G.3.b": "2.G.3.c",  # 2G3b_N2O_from_product_uses:_Other
        "2.G.4": "2.G.4",  # 2G4_Other_product_manufacture_and_use
        "3.A.1.Aa": "3.A.1.a.i",  # 3A1a_Enteric_Fermentation_dairy_cattle
        "3.A.1.Ab": "3.A.1.a.ii",  # 3A1b_Enteric_Fermentation_non-dairy_cattle
        "3.A.2": "3.A.1.c",  # 3A2_Enteric_Fermentation_sheep
        "3.A.3": "3.A.1.h",  # 3A3_Enteric_Fermentation_swine
        "3.A.4": "3.A.1.j",  # 3A4_Enteric_Fermentation_other:deer
        "3.B.1.Aa": "3.A.2.a.i",  # 3B21a_Manure_Management_X_dairy_cattle
        "3.B.1.Ab": "3.A.2.a.ii",  # 3B21b_Manure_Management_X_non-dairy_cattle
        "3.B.2": "3.A.2.c",  # 3B22_Manure_Management_X_sheep
        "3.B.3": "3.A.2.h",  # 3B23_Manure_Management_X_swine
        "3.B.4": "3.A.2.i",  # 3B24_Manure_Management_X_other:poultry
        "3.B.5": "3.C.6",  # 3B25_Manure_Management_Indirect_Emissions_swine
        "3.D.a.1": "M.3.C.4.a.AG",  # 3D11_Agriculural_Soils_Inorganic_N_Fertilisers
        "3.D.a.2.a": "M.3.C.4.b.i.AG",  # 3D12a_Agricultural_Soils_Manure_Applied_to_Soils
        "3.D.a.2.b": "M.3.C.4.b.ii.AG",  # 3D12b_Agricultural_Soils_Sewage_Sludge_Applied_to_Soils
        "3.D.a.2.c": "M.3.C.4.b.iii.AG",  # 3D12c_Agricultural_Soils_Other_Organic_Fertilisers_Applied_to_Soils
        "3.D.a.3": "3.C.4.c",  # 3D13_Agricultural_Soils_Manure_Deposited_by_Grazing_Animals
        "3.D.a.4": "3.C.4.d",  # 3D14_Agriculural_Soils_Residues
        "3.D.a.5": "M.3.C.4.e.AG",  # 3D15_Agricultural_soils_Mineralization/Immobilization
        "3.D.a.6": "M.3.C.4.f.AG",  # 3D16_Agricultural_soils_Cultivation_of_Organic_Soils
        "3.D.b.1": "M.3.C.5.a.AG",  # 3D21_Agriculural_Soils_Indirect_Deposition
        "3.D.b.2": "M.3.C.5.b.AG",  # 3D22_Agriculural_Soils_Indirect_Leaching_and_Run-off
        "3.F.1.a": "M.3.C.1.b.i",  # 3F11_Field_burning_wheat
        "3.F.1.b": "M.3.C.1.b.ii",  # 3F12_Field_burning_barley
        "3.F.1.d": "M.3.C.1.b.iii",  # 3F14_Field_burning_other_cereals
        "3.F.5": "M.3.C.1.b.iv",  # 3F5_Field_burning_other_residues
        "3.G.1": "M.3.C.2.a",  # 3G1_Liming - limestone
        "3.G.2": "M.3.C.2.b",  # 3G2_Liming - dolomite
        "3.H": "M.3.C.3.AG",  # 3H_Urea application
        "4": "M.3.C.5.LU",  # 4_Indirect_N2O_Emissions (LULUCF)
        "4.A": "M.3.B.1.DR",  # 4A_Forest Land_Emissions_from_Drainage
        "4.A.1": "3.B.1.a",  # 4A1_ Forest Land remaining Forest Land
        "4.A.2": "3.B.1.b",  # 4A2_Cropland_converted_to_Forest_Land (and other land types)
        "4.B.1": "3.B.2.a",  # 4B1_Cropland Remaining Cropland
        "4.B.2": "3.B.2.b",  # 4B2_Forest_Land_converted_to_Cropland (and other land types)
        "4.C": "M.3.B.3.DR",  # 4C_Grassland_Emissions_from_Drainage
        "4.C.1": "3.B.3.a",  # 4C1_Grassland Remaining Grassland
        "4.C.2": "3.B.3.b",  # 4C2_Forest_Land_converted_to_Grassland (and other land types)
        "4.D": "M.3.B.4.DR",  # 4D_Wetlands_Emissions_from_Drainage
        "4.D.1": "3.B.4.a",  # 4D1_Wetlands remaining wetlands
        "4.D.2": "3.B.4.b",  # 4D2_Land_converted_to_Wetlands_Peat_Extraction
        "4.E": "M.3.B.5.DR",  # 4E_Settlements_Emissions_from_Drainage
        "4.E.1": "3.B.5.a",  # 4E1_Settlements remaining settlements
        "4.E.2": "3.B.5.b",  # 4E2_Forest_Land_converted_to_Settlements (and other land types)
        "4.G": "3.D.1",  # 4G_Harvested Wood Products
        "5.A.1.a": "M.4.A.1.a",  # 5A1a_Managed_Waste_Disposal_sites_anaerobic
        "5.B.1.a": "M.4.B.1.a",  # 5B1a_composting_municipal_solid_waste
        "5.B.2.a": "M.4.B.2.a",  # 5B2a_Anaerobic_digestion_municipal_solid_waste
        "5.C.1.a.ii.4": "M.4.C.1.a.ii.4",  # 5C1.1b_Biogenic:Sewage_sludge
        "5.C.1.b.i": "M.4.C.1.b.i",  # 5C1.2a_Non-biogenic:municipal_solid_waste
        "5.C.1.b.ii.3": "M.4.C.1.b.ii.3",  # 5C1.2b_Non-biogenic:Clinical_waste
        "5.C.2.a.ii.5": "M.4.C.2.a.ii.5",  # 5C2.1b_Biogenic:Other
        "5.C.2.b.ii.5": "M.4.C.2.b.ii.5",  # 5C2.2b_Non-biogenic:Other
        "5.D.1": "4.D.1",  # 5D1_Domestic_wastewater_treatment
        "5.D.2": "4.D.2",  # 5D2_Industrial_wastewater_treatment
        "Aviation_Bunkers": "M.BK.A",  # Aviation_Bunkers
        "Marine_Bunkers": "M.BK.B",  # Marine_Bunkers
    },
    "aggregate": {
        # need to aggregate the whole tree as only leaves are given in the data
        # 1
        ## 1.A
        "1.A.1.a": {"sources": ["1.A.1.a.i", "1.A.1.a.iii"]},
        "1.A.1.c": {"sources": ["1.A.1.c.i", "1.A.1.c.ii", "1.A.1.c.iii"]},
        "1.A.1": {"sources": ["1.A.1.a", "1.A.1.b", "1.A.1.c"]},
        "1.A.2.m": {"sources": ["1.A.2.m.i", "1.A.2.m.ii"]},
        "1.A.2": {
            "sources": [
                "1.A.2.a",
                "1.A.2.b",
                "1.A.2.c",
                "1.A.2.d",
                "1.A.2.e",
                "1.A.2.f",
                "1.A.2.i",
                "1.A.2.k",
                "1.A.2.m",
            ]
        },
        "1.A.3.a": {"sources": ["1.A.3.a.ii"]},
        "1.A.3.b": {
            "sources": [
                "1.A.3.b.i",
                "1.A.3.b.ii",
                "1.A.3.b.iii",
                "1.A.3.b.iv",
                "M.1.A.3.b.v",
            ]
        },
        "1.A.3.d": {"sources": ["1.A.3.d.ii"]},
        "1.A.3.e": {"sources": ["1.A.3.e.ii"]},
        "1.A.3": {"sources": ["1.A.3.a", "1.A.3.b", "1.A.3.c", "1.A.3.d", "1.A.3.e"]},
        "1.A.4.a": {"sources": ["1.A.4.a.i", "1.A.4.a.ii"]},
        "1.A.4.b": {"sources": ["1.A.4.b.i", "1.A.4.b.ii"]},
        "1.A.4.c": {"sources": ["1.A.4.c.i", "1.A.4.c.ii", "1.A.4.c.iii"]},
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"]},
        "1.A.5": {"sources": ["1.A.5.b"]},
        "1.A": {"sources": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"]},
        ## 1.B
        "1.B.1.a.i": {"sources": ["1.B.1.a.i.1", "1.B.1.a.i.2", "1.B.1.a.i.3"]},
        "1.B.1.a.ii": {"sources": ["1.B.1.a.ii.1"]},
        "1.B.1.a": {"sources": ["1.B.1.a.i", "1.B.1.a.ii"]},
        "1.B.1": {"sources": ["1.B.1.a", "1.B.1.c"]},
        "1.B.2.a.iii": {
            "sources": [
                "1.B.2.a.iii.1",
                "1.B.2.a.iii.2",
                "1.B.2.a.iii.3",
                "1.B.2.a.iii.4",
                "1.B.2.a.iii.6",
            ]
        },
        "1.B.2.a": {"sources": ["1.B.2.a.i", "1.B.2.a.ii", "1.B.2.a.iii"]},
        "1.B.2.b.iii": {
            "sources": [
                "1.B.2.b.iii.1",
                "1.B.2.b.iii.2",
                "1.B.2.b.iii.3",
                "1.B.2.b.iii.4",
                "1.B.2.b.iii.5",
            ]
        },
        "1.B.2.b": {"sources": ["1.B.2.b.i", "1.B.2.b.ii", "1.B.2.b.iii"]},
        "1.B.2": {"sources": ["1.B.2.a", "1.B.2.b"]},
        "1.B.3": {"sources": ["1.B.3.b"]},
        "1.B": {"sources": ["1.B.1", "1.B.2", "1.B.3"]},
        ## 1
        "1": {"sources": ["1.A", "1.B"]},
        # 2
        ## 2.A
        "2.A.4": {"sources": ["2.A.4.a", "2.A.4.b", "2.A.4.d"]},
        "2.A": {"sources": ["2.A.1", "2.A.2", "2.A.3", "2.A.4"]},
        ## 2.B
        "2.B.8": {
            "sources": [
                "2.B.8.a",
                "2.B.8.b",
                "2.B.8.c",
                "2.B.8.d",
                "2.B.8.e",
                "2.B.8.f",
                "2.B.8.g",
            ]
        },
        "2.B.9.a": {"sources": ["2.B.9.a.i"]},
        "2.B.9.b": {"sources": ["2.B.9.b.iii"]},
        "2.B.9": {"sources": ["2.B.9.a", "2.B.9.b"]},
        "2.B": {
            "sources": [
                "2.B.1",
                "2.B.2",
                "2.B.3",
                "2.B.6",
                "2.B.7",
                "2.B.8",
                "2.B.9",
                "2.B.10",
            ]
        },
        ## 2.C
        "2.C.1": {"sources": ["2.C.1.a", "2.C.1.b", "2.C.1.d"]},
        "2.C.3": {"sources": ["2.C.3.a", "2.C.3.b"]},
        "2.C": {"sources": ["2.C.1", "2.C.3", "2.C.4", "2.C.6"]},
        ## 2.D
        "2.D": {"sources": ["2.D.1", "2.D.2", "2.D.3"]},
        ## 2.E
        "2.E": {"sources": ["2.E.1"]},
        ## 2.F
        "2.F.1.a": {
            "sources": [
                "M.2.F.1.a.i",
                "M.2.F.1.a.ii",
                "M.2.F.1.a.iii",
                "M.2.F.1.a.iv",
                "M.2.F.1.a.v",
            ]
        },
        "2.F.1": {"sources": ["2.F.1.a", "2.F.1.b"]},
        "2.F.2": {"sources": ["M.2.F.2.a", "M.2.F.2.b"]},
        "2.F.4": {"sources": ["M.2.F.4.a", "M.2.F.4.b"]},
        "2.F.6": {"sources": ["2.F.6.b"]},
        "2.F": {"sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4", "2.F.5", "2.F.6"]},
        ## 2.G
        "2.G.2.c": {"sources": ["M.2.G.2.c.i"]},
        "2.G.2": {"sources": ["2.G.2.a", "2.G.2.b", "2.G.2.c"]},
        "2.G.3": {"sources": ["2.G.3.a", "2.G.3.c"]},
        "2.G": {"sources": ["2.G.1", "2.G.2", "2.G.3", "2.G.4"]},
        ## 2
        "2": {"sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G"]},
        # 3
        ## 3.A
        "3.A.1.a": {"sources": ["3.A.1.a.i", "3.A.1.a.ii"]},
        "3.A.1": {"sources": ["3.A.1.a", "3.A.1.c", "3.A.1.h", "3.A.1.j"]},
        "3.A.2.a": {"sources": ["3.A.2.a.i", "3.A.2.a.ii"]},
        "3.A.2": {"sources": ["3.A.2.a", "3.A.2.c", "3.A.2.h", "3.A.2.i"]},
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        ## 3.B
        "3.B.1": {"sources": ["3.B.1.a", "3.B.1.b", "M.3.B.1.DR"]},
        "3.B.2": {"sources": ["3.B.2.a", "3.B.2.b"]},
        "3.B.3": {"sources": ["3.B.3.a", "3.B.3.b", "M.3.B.3.DR"]},
        "3.B.4": {"sources": ["3.B.4.a", "3.B.4.b", "M.3.B.4.DR"]},
        "3.B.5": {"sources": ["3.B.5.a", "3.B.5.b", "M.3.B.5.DR"]},
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5"]},
        ## 3.C
        "3.C.1.b": {
            "sources": ["M.3.C.1.b.i", "M.3.C.1.b.ii", "M.3.C.1.b.iii", "M.3.C.1.b.iv"]
        },
        "3.C.1": {"sources": ["3.C.1.b"]},
        "M.3.C.1.AG": {"sources": ["3.C.1.b"]},
        "M.3.C.2.AG": {"sources": ["M.3.C.2.a.AG", "M.3.C.2.b.AG"]},
        "3.C.2": {"sources": ["M.3.C.2.AG"]},
        "3.C.3": {"sources": ["M.3.C.3.AG"]},
        "3.C.4.a": {"sources": ["M.3.C.4.a.AG"]},
        "M.3.C.4.b.AG": {
            "sources": ["M.3.C.4.b.i.AG", "M.3.C.4.b.ii.AG", "M.3.C.4.b.iii.AG"]
        },
        "3.C.4.b": {"sources": ["M.3.C.4.b.AG"]},
        "3.C.4.e": {"sources": ["M.3.C.4.e.AG"]},
        "3.C.4.f": {"sources": ["M.3.C.4.f.AG"]},
        "M.3.C.4.AG": {
            "sources": [
                "3.C.4.a.AG",
                "3.C.4.b.AG",
                "3.C.4.c",
                "3.C.4.d",
                "M.3.C.4.e.AG",
                "M.3.C.4.f.AG",
            ]
        },
        "3.C.4": {
            "sources": [
                "3.C.4.a",
                "3.C.4.b",
                "3.C.4.c",
                "3.C.4.d",
                "3.C.4.e",
                "3.C.4.f",
            ]
        },
        "M.3.C.5.AG": {"sources": ["M.3.C.5.a.AG", "M.3.C.5.b.AG"]},
        "3.C.5": {"sources": ["M.3.C.5.AG", "M.3.C.5.LU"]},
        "3.C": {"sources": ["3.C.1", "3.C.2", "3.C.3", "3.C.4", "3.C.5", "3.C.6"]},
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "M.3.C.2.AG",
                "M.3.C.3.AG",
                "M.3.C.4.AG",
                "M.3.C.5.AG",
                "3.C.6",
            ]
        },
        "M.3.C.LU": {"sources": ["M.3.C.5.LU"]},
        "M.3.D.LU": {"sources": ["3.D.1"]},
        # 3.D
        "3.D": {"sources": ["3.D.1"]},
        "M.AG.ELV": {"sources": ["M.3.C.AG"]},
        "3": {"sources": ["3.A", "3.B", "3.C", "3.D"]},
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},
        "M.LULUCF": {"sources": ["3.B", "M.3.C.LU", "M.3.D.LU"]},
        # 4
        "4.A.1": {"sources": ["M.4.A.1.a"]},
        "4.A": {"sources": ["4.A.1"]},
        "4.B.1": {"sources": ["M.4.B.1.a"]},
        "4.B.2": {"sources": ["M.4.B.2.a"]},
        "4.B": {"sources": ["4.B.1", "4.B.2"]},
        "4.C.1": {"sources": ["M.4.C.1.a.ii.4", "M.4.C.1.b.i", "M.4.C.1.b.ii.3"]},
        "4.C.2": {"sources": ["M.4.C.2.a.ii.5", "M.4.C.2.b.ii.5"]},
        "4.C": {"sources": ["4.C.1", "4.C.2"]},
        "4.D": {"sources": ["4.D.1", "4.D.2"]},
        "4": {"sources": ["4.A", "4.B", "4.C", "4.D"]},
        # top level and bunkers
        "0": {"sources": ["1", "2", "3", "4"]},
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
        "M.BK": {"sources": ["M.BK.A", "M.BK.B"]},
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
