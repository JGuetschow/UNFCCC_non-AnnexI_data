"""
Configuration file to read Bangladesh's BTR 1.

Overview of all available GHG tables

As the data is spread over multiple tables we collect data from small tables manually
in a xlsx file which we then read using pandas. The origin of the data points is
specified in the xls files. Additionally, we read the key category analysis (Annex-IX)
which contains detailed information for 2019 and 2022
"""

## general configuration
coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_BGD",
    "scenario": "PRIMAP",
}

# primap2 format conversion
coords_defaults = {
    "source": "BGD-GHG-Inventory",
    "provenance": "measured",
    "area": "BGD",
    "scenario": "BTR1",
}

gwp_to_use = "AR5GWP100"

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
}

filter_remove = {
    # "f_memo": {"category": "MEMO"},
    # "f_info": {"category": "INFO"},
}

meta_data = {
    "references": "https://unfccc.int/documents/655314",
    "rights": "",  # unknown
    "contact": "mail@johannes-guetschow.de",
    "title": " Bangladesh. 2024 Biennial Transparency Report (BTR). BTR1. ",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

## configuration for the individual tables
coords_cols_individual = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_value_mapping_individual = {
    "unit": "PRIMAP1",
    "entity": {
        "Total GHG Emission": f"KYOTOGHG ({gwp_to_use})",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
        "HFCs": f"HFCS ({gwp_to_use})",
        "HFC-23": f"HFC23 ({gwp_to_use})",
        "HFC-32": f"HFC32 ({gwp_to_use})",
        "HFC-125": f"HFC125 ({gwp_to_use})",
        "HFC-134a": f"HFC134a ({gwp_to_use})",
        "HFC-143a": f"HFC143a ({gwp_to_use})",
        "HFC-227ea": f"HFC227ea ({gwp_to_use})",
        "HFC-245fa": f"HFC245fa ({gwp_to_use})",
        "HFC-365mfc": f"HFC365mfc ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "Unspecified mix of HFCs and PFCs": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NF3": f"NF3 ({gwp_to_use})",
    },
}

cols_to_drop_individual = ["comment", "orig_cat_name", "source"]

## configuration for the key category analysis
page_defs = {
    "430": {
        "table_areas": ["38,746,561,76"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "431": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "432": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "433": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "434": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "435": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "436": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "437": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "438": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "439": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "440": {
        "table_areas": ["36,777,563,691"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
}

cols_to_drop_key_cat = [
    "Trend Assessment (Txt)",
    "% Contribution to Trend",
    "Cumulative Total of Column G",
]

unit_key_cat = "GgCO2eq"

cols_to_rename_key_cat = {
    "2019 Year Estimate Ex0 (Gg CO2 Eq)": "2019",
    "2022 Year Estimate Ext (Gg CO2 Eq)": "2022",
}

coords_cols_key_cat = {
    "category": "IPCC Category code",
    "entity": "Greenhouse gas",
    "unit": "unit",
    "fuel_type": "IPCC Category",
}

coords_value_mapping_key_cat = {
    "unit": "PRIMAP1",
    "entity": {
        "HFCs (HFCs)": f"HFCS ({gwp_to_use})",
        "HFCs, PFCs": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
        "PFCs (PFCs)": f"PFCS ({gwp_to_use})",
        "SF6, PFCs, HFCs and other halogenated gases": f"FGASES ({gwp_to_use})",
        "SF6, PFCs": f"FGASES ({gwp_to_use})",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
    },
    "fuel_type": {
        "Road Transportation -Gaseous Fuels": "gaseous",
        "Coal mining and handling": "all",
        "Natural Gas": "all",
        "Enteric Fermentation": "all",
        "Manure Management": "all",
        "Rice cultivation": "all",
        "Solid Waste Disposal": "all",
        "Wastewater Treatment and Discharge": "all",
        "Energy Industries -Gaseous Fuels": "gaseous",
        "Energy Industries -Liquid Fuels": "liquid",
        "Energy Industries -Solid Fuels": "solid",
        "Manufacturing Industries and Construction -Gaseous Fuels": "gaseous",
        "Manufacturing Industries and Construction -Solid Fuels": "solid",
        "Road Transportation -Liquid Fuels": "liquid",
        "Railways - Liquid Fuels": "liquid",
        "Water-borne Navigation -Liquid Fuels": "liquid",
        "Other Sectors -Gaseous Fuels": "gaseous",
        "Other Sectors -Liquid Fuels": "liquid",
        "Cement production": "all",
        "Ammonia Production": "all",
        "Forest land Remaining Forest land": "all",
        "Land Converted to Forest land": "all",
        "Land Converted to Cropland": "all",
        "Land Converted to Grassland": "all",
        "Land Converted to Wetlands": "all",
        "Land Converted to Settlements": "all",
        "Land Converted to Other land": "all",
        "Urea application": "all",
        "Refrigeration and Air Conditioning": "all",
        "Aerosols": "all",
        "Iron and Steel Production": "all",
        "Biological Treatment of Solid Waste": "all",
        "Manufacturing Industries and Construction -Liquid Fuels": "liquid",
        "Civil Aviation - Liquid Fuels": "liquid",
        "Railways -Solid Fuels": "solid",
        "Glass Production": "all",
        "Non-Energy Products from Fuels and Solvent Use": "all",
        "Foam Blowing Agents": "all",
        "N2O Emissions from Aquaculture": "all",
        "Direct N2O Emissions from managed soils": "all",
        "Indirect N2O Emissions from managed soils": "all",
        "Indirect N2O Emissions from manure management": "all",
        "Fire Protection": "all",
        "Energy Industries": "all",
        "Energy Industries - Peat": "peat",
        "Energy Industries -Biomass -gas": "bio_gas",
        "Energy Industries -Biomass -liquid": "bio_liquid",
        "Energy Industries -Biomass -other": "bio_other",
        "Energy Industries -Biomass -solid": "bio_solid",
        "Energy Industries -Other Fossil Fuels": "other_fossil",
        "Railways - Solid Fuels": "solid",
        "Incineration and Open Burning of Waste": "all",
        "Manufacturing Industries and Construction -Other Fossil Fuels": "other_fossil",
        "Manufacturing Industries and Construction -Peat": "peat",
        "Grassland Remaining Grassland": "all",
        "Manufacturing Industries and Construction -Biomass -gas": "bio_gas",
        "Manufacturing Industries and Construction -Biomass -liquid": "bio_liquid",
        "Manufacturing Industries and Construction -Biomass -other": "bio_other",
        "Manufacturing Industries and Construction -Biomass -solid": "bio_solid",
        "Civil Aviation - Solid Fuels": "solid",
        "Civil Aviation -Biomass -liquid": "bio_liquid",
        "Civil Aviation -Biomass -solid": "bio_solid",
        "Civil Aviation -Gaseous Fuels": "gaseous",
        "Civil Aviation -Other Fossil Fuels": "other_fossil",
        "Civil Aviation -Biomass -gas": "bio_gas",
        "Civil Aviation -Biomass -other": "bio_other",
        "Road Transportation -Biomass -gas": "bio_gas",
        "Road Transportation -Biomass -liquid": "bio_liquid",
        "Road Transportation -Biomass -other": "bio_other",
        "Road Transportation -Biomass -solid": "bio_solid",
        "Road Transportation -Other Fossil Fuels": "other_fossil",
        "Road Transportation -Solid Fuels": "solid",
        "Railways -Gaseous Fuels": "gaseous",
        "Road Transportation": "all",
        "Railways - Biomass - gas": "bio_gas",
        "Railways - Biomass - liquid": "bio_liquid",
        "Railways - Biomass - other": "bio_other",
        "Railways - Biomass - solid": "bio_solid",
        "Railways - Gaseous Fuels": "gaseous",
        "Railways -Other Fossil Fuels": "other_fossil",
        "Water-borne Navigation -Biomass -gas": "bio_gas",
        "Water-borne Navigation -Biomass -liquid": "bio_liquid",
        "Water-borne Navigation -Biomass -other": "bio_other",
        "Water-borne Navigation -Biomass -solid": "bio_solid",
        "Water-borne Navigation -Gaseous Fuels": "gaseous",
        "Water-borne Navigation -Other Fossil Fuels": "other_fossil",
        "Water-borne Navigation -Solid Fuels": "solid",
        "Other Transportation -Gaseous Fuels": "gaseous",
        "Other Transportation -Liquid Fuels": "liquid",
        "Other Transportation -Solid Fuels": "solid",
        "Other Transportation -Biomass -gas": "bio_gas",
        "Other Transportation -Biomass -liquid": "bio_liquid",
        "Other Transportation -Biomass -other": "bio_other",
        "Other Transportation -Biomass -solid": "bio_solid",
        "Other Transportation -Other Fossil Fuels": "other_fossil",
        "Other Sectors - Peat": "peat",
        "Other Sectors - Solid Fuels": "solid",
        "Other Sectors -Biomass -gas": "bio_gas",
        "Other Sectors -Biomass -liquid": "bio_liquid",
        "Other Sectors -Biomass -solid": "bio_solid",
        "Other Sectors -Other Fossil Fuels": "other_fossil",
        "Other Sectors -Biomass -other": "bio_other",
        "Non-Specified - Peat": "peat",
        "Non-Specified - Solid Fuels": "solid",
        "Non-Specified -Biomass -gas": "bio_gas",
        "Non-Specified -Biomass -liquid": "bio_liquid",
        "Non-Specified -Biomass -other": "bio_other",
        "Non-Specified -Biomass -solid": "bio_solid",
        "Non-Specified -Gaseous Fuels": "gaseous",
        "Non-Specified -Liquid Fuels": "liquid",
        "Non-Specified -Other Fossil Fuels": "other_fossil",
        "Oil": "all",
        "Other emissions from Energy Production": "all",
        "Other (please specify)": "all",
        "Carbide Production": "all",
        "Petrochemical and Carbon Black Production": "all",
        "Iron and Steel Production -Solid Fuels": "solid",
        "Ferroalloys Production": "all",
        "Carbon dioxide Transport and Storage": "all",
        "Lime production": "all",
        "Other Process Uses of Carbonates": "all",
        "Titanium Dioxide Production": "all",
        "Soda Ash Production": "all",
        "Aluminium production": "all",
        "Magnesium production": "all",
        "Lead Production": "all",
        "Zinc Production": "all",
        "Fluorochemical Production": "all",
        "Electronics Industry": "all",
        "Other Product Manufacture and Use": "all",
        "Nitric Acid Production": "all",
        "Adipic Acid Production": "all",
        "Caprolactam, Glyoxal and Glyoxylic Acid Production": "all",
        "Uncontrolled combustion and burning coal dumps -Solid Fuels": "solid",
        "Fuel transformation": "all",
        "Hydrogen Production": "all",
        "Other": "all",
        "Burning": "all",
        "CH4 from Rewetting of Organic Soils": "all",
        "CH4 Emissions from Rewetting of Mangroves and Tidal Marshes": "all",
        "CH4 Emissions from Rewetted and Created Wetlands on Inland Wetland Mineral Soils": "all",
        "CH4 from Drained Organic Soils": "all",
        "CH4 from Drainage Ditches on Organic Soils": "all",
        "Rare Earths Production": "all",
        "Cropland Remaining Cropland": "all",
        "Peatlands remaining peatlands": "all",
        "Liming": "all",
        "Harvested Wood Products": "all",
        "Indirect CO2 emissions from the atmospheric oxidation of CH4, CO and NMVOC": "all",
        "Indirect N2O emissions from the atmospheric deposition of nitrogen in NOx and NH3": "all",
        "Settlements Remaining Settlements": "all",
    },
}

agg_fuel_type = {
    "fuel_type": {
        "all": {
            "sources": [
                "bio_gas",
                "bio_liquid",
                "bio_other",
                "bio_solid",
                "gaseous",
                "liquid",
                "other_fossil",
                "peat",
                "solid",
            ],
        }
    }
}

# data to drop because it is inconsistent between fuel types and aggregates
data_to_remove = {
    "1A1": {
        "entities": ["CO2", "CH4"],
        "category (IPCC2006_BGD)": ["1.A.1"],
        "time": ["2019", "2022"],
        "fuel_type": ["all"],
    },
    "2C1": {
        "entities": ["CO2", "CH4"],
        "category (IPCC2006_BGD)": ["2.C.1"],
        "time": ["2019", "2022"],
        "fuel_type": ["solid"],
    },
    "1A3b": {
        "entities": ["CO2"],
        "category (IPCC2006_BGD)": ["1.A.3.b"],
        "time": ["2019", "2022"],
        "fuel_type": ["all"],
    },
    "LULUCF": {  # all LULUCF data is inconsistent with the inventory
        "entities": ["CO2", "N2O"],
        "category (IPCC2006_BGD)": [
            "3.B.1.a",
            "3.B.1.b",
            "3.B.2.a",
            "3.B.2.b",
            "3.B.3.a",
            "3.B.3.b",
            "3.B.4.a.i",
            "3.B.4.b",
            "3.B.5.a",
            "3.B.5.b",
            "3.B.6.b",
            "3.D.2",
            "3.D.1",
        ],
    },
}

## processing configuration
terminology_proc = "IPCC2006_PRIMAP"

LULUCF_data_copy_cats = [
    "3.B.1",
    "3.B.1.a",
    "3.B.1.b",
    "3.B.2",
    "3.B.2.a",
    "3.B.2.b",
    "3.B.3",
    "3.B.3.a",
    "3.B.3.b",
    "3.B.4",
    "3.B.4.a",
    "3.B.4.b",
    "3.B.5",
    "3.B.5.a",
    "3.B.5.b",
    "3.B.6",
    "3.B.6.a",
    "3.B.6.b",
    "3.D.1",
    "M.LULUCF",
]


country_processing_step1 = {
    # aggregate gases
    "aggregate_gases": {
        f"KYOTOGHG ({gwp_to_use})": {
            "sources": ["CO2", "CH4", "N2O"],
            "sel": {
                "cat": [
                    "2.A.1",
                    "2.A.3",
                    "2.C.1",
                    "2.C.2",
                    "2.C.3",
                    "2.C.4",
                    "2.C.5",
                    "2.C.6",
                    "2.C.7",
                    "2.C.8",
                    "2.D.1",
                    "2.D.2",
                    "2.D.3",
                    "2.D.4",
                    "4.A",
                    "4.A.1",
                    "4.A.2",
                    "4.A.3",
                    "3.C.7",
                ]
            },
        },
    },
    # aggregate categories
    "aggregate_coords": {
        "category": {
            "1.A.3.a": {
                "sources": ["1.A.3.a.ii"],
                "sel": {
                    "variable": [f"KYOTOGHG ({gwp_to_use})"],
                },
            },
            "1.A.3.d": {
                "sources": ["1.A.3.d.ii"],
                "sel": {
                    "variable": [f"KYOTOGHG ({gwp_to_use})"],
                },
            },
            # don't copy to 2.F as this would mean we also have to downscale the zero
            # F/gas data for 2.B, 2.E, 2.G to individual gases or at least gas groups
            # for consistency
            # "2.F": {  # only 2.F has HFCS, but the sector lacks gas resolution
            #     "sources": ["2"],
            #     "sel": {
            #         "variable": [
            #             "HFC125",
            #             "HFC134a",
            #             "HFC143a",
            #             "HFC227ea",
            #             "HFC23",
            #             "HFC245fa",
            #             "HFC32",
            #             "HFC365mfc",
            #             "NF3",
            #             "SF6",
            #         ],
            #     },
            # },
            "3.B.4.a": {
                "sources": ["3.B.4.a.i"],
                "sel": {
                    "variable": ["CO2"],
                },
            },
            "M.3.C.8.LU": {  # all the extra 3.C categories which are part of Land use
                "sources": [
                    "3.C.8",
                    "3.C.9",
                    "3.C.10",
                    "3.C.11",
                    "3.C.13",
                    "3.C.14",
                ],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O"],
                },
            },
            "M.3.C.8.b": {  # for consistency with key category table
                "sources": ["3.C.12"],
                "sel": {
                    "entity": ["N2O"],
                },
            },
        },
    },
}

country_processing_step2 = {
    "tolerance": 0.01,
    "remove_ts": {
        "fgas_subsectors": {  # we have gas detail for IPPU and sector detail for
            # aggregates. No consistent downscaling is possible with this configuration
            # as we currently only need IPPU for primap-hist, we keep the gas detail
            # to allow for proper GWP conversions. category 2.F can be constructed as
            # fgases are only non-zero for 2.F (see first step)
            "entities": [
                f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                f"PFCS ({gwp_to_use})",
                f"HFCS ({gwp_to_use})",
                f"FGASES ({gwp_to_use})",
            ],
            "category": [
                "2.C.3",
                "2.F.1",
                "2.F.2",
                "2.F.3",
                "2.F.4",
                "2.B",
                "2.B.9",
                "2.E",
                "2.G",
            ],
        },
        "3C_custom": {
            # remove the source specific 3.C subcategories which were combined to 3.C.8
            "category": [
                "3.C.8",
                "3.C.9",
                "3.C.10",
                "3.C.11",
                "3.C.12",
                "3.C.13",
                "3.C.14",
            ]
        },
        "4C_2019": {
            # 0 for gases but actually NE
            "category": ["4.C"],
            "entities": ["CO2", "CH4", "N2O"],
            "time": ["2019"],
        },
        # "N2O_3B": {
        #     "entities": ["N2O"],
        #     "category": ["3.B.4.a.i", "3.B.4.b"],
        # },
    },
    # interpolate timeseries for IPPU subsectors as they either have explicit information
    # or are zero only
    "interpolate_ts": {
        "IPPU_CH4": {
            "entities": ["CH4"],
            "category": [
                "2.A",
                "2.A.5",
                "2.B",
                "2.B.10",
                "2.B.5",
                "2.B.8",
                "2.D",
                "2.H",
            ],
        },
        "IPPU_CO2": {
            "entities": ["CO2"],
            "category": [
                "2.A.2",
                "2.A.4",
                "2.A.5",
                "2.B.10",
                "2.B.5",
                "2.B.6",
                "2.B.7",
                "2.B.8",
                "2.H",
            ],
        },
        "IPPU_FGASES": {
            "entities": [f"FGASES ({gwp_to_use})"],
            "category": [
                "2",
                "2.B",
                "2.B.9",
                "2.E",
                "2.G",
            ],
        },
        "IPPU_N2O": {
            "entities": ["N2O"],
            "category": [
                "2.A",
                "2.A.5",
                "2.B",
                "2.B.10",
                "2.B.2",
                "2.B.3",
                "2.B.4",
                "2.D",
                "2.E",
                "2.G",
                "2.H",
            ],
        },
        "3D2": {
            "entities": ["CH4", "CO2", "N2O"],
            "category": ["3.D.2"],
        },
        # "5": {
        #     "entities": ["CO2", "N2O"],
        #     "category": ["5.A", "5.B"],
        # },
        # "LULUCF": {
        #     "entities": ["CH4", "N2O"],
        #     "category": ["M.LULUCF"],
        # },
        # "1B3_1C": {
        #     "category": ["1.B.3", "1.C"],
        #     "entities": ["CO2", "CH4", "N2O"],
        # }
    },
    "aggregate_coords": {
        "category": {
            # aggregation for the key category analysis
            "1.A.3": {
                "sources": [
                    "1.A.3.a",
                    "1.A.3.b",
                    "1.A.3.c",
                    "1.A.3.d",
                    "1.A.3.e",
                ]
            },
            "1.A": {
                "sources": [
                    "1.A.1",
                    "1.A.2",
                    "1.A.3",
                    "1.A.4",
                    "1.A.5",
                ]
            },
            "1.B.1": {
                "sources": [
                    "1.B.1.a",
                    "1.B.1.b",
                    "1.B.1.c",
                ]
            },
            "1.B.2": {
                "sources": [
                    "1.B.2.a",
                    "1.B.2.b",
                ]
            },
            "1.B": {
                "sources": [
                    "1.B.1",
                    "1.B.2",
                    "1.B.3",
                ]
            },
            "1": {
                "sources": [
                    "1.A",
                    "1.B",
                    "1.C",
                ]
            },
            "2.A": {
                "sources": [
                    "2.A.1",
                    "2.A.2",
                    "2.A.3",
                    "2.A.4",
                    "2.A.5",
                ]
            },
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
            "2.C": {
                "sources": [
                    "2.C.1",
                    "2.C.2",
                    "2.C.3",
                    "2.C.4",
                    "2.C.5",
                    "2.C.6",
                    "2.C.7",
                    "2.C.8",
                ]
            },
            "2.D": {
                "sources": [
                    "2.D.1",
                    "2.D.2",
                    "2.D.3",
                    "2.D.4",
                ]
            },
            "2.F": {
                "sources": [
                    "2.F.1",
                    "2.F.2",
                    "2.F.3",
                    "2.F.4",
                ]
            },
            "2": {"sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"]},
            ## for the data from the individual tables
            # 3
            ## 3.A
            "3.A.1.j": {
                "sources": [
                    "3.A.1.j.vi",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.A.1": {  # consistency check
                "sources": [
                    "3.A.1.a",
                    "3.A.1.b",
                    "3.A.1.c",
                    "3.A.1.d",
                    "3.A.1.e",
                    "3.A.1.f",
                    "3.A.1.g",
                    "3.A.1.h",
                    "3.A.1.i",
                    "3.A.1.j",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.A.2.j": {
                "sources": [
                    "3.A.2.j.vi",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.A.2": {
                "sources": [
                    "3.A.2.a",
                    "3.A.2.b",
                    "3.A.2.c",
                    "3.A.2.d",
                    "3.A.2.e",
                    "3.A.2.f",
                    "3.A.2.g",
                    "3.A.2.h",
                    "3.A.2.i",
                    "3.A.2.j",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.A": {
                "sources": ["3.A.1", "3.A.2"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            ## 3.B (consistency check)
            "3.B": {
                "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
                "sel": {"entity": ["KYOTOGHG", "CO2"]},
            },
            ## 3.C
            "3.C.1": {
                "sources": ["M.3.C.1.SAV", "3.C.1.b"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "M.3.C.1.AG": {
                "sources": ["M.3.C.1.SAV", "3.C.1.b"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.2": {
                "sources": ["M.3.C.2.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.3": {
                "sources": ["M.3.C.3.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.4": {
                "sources": ["M.3.C.4.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.4.a": {
                "sources": ["M.3.C.4.a.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.4.b": {
                "sources": ["M.3.C.4.b.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.4.e": {
                "sources": ["M.3.C.4.e.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.4.f": {
                "sources": ["M.3.C.4.f.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.C.5": {
                "sources": ["M.3.C.5.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },  # , "M.3.C.5.LU"]},
            "M.3.C.8.AG": {
                "sources": ["M.3.C.8.a", "M.3.C.8.b"],
                "sel": {"entity": ["KYOTOGHG", "N2O"]},
            },
            "3.C.8": {
                "sources": ["M.3.C.8.AG", "M.3.C.8.LU"],
                "sel": {"entity": ["KYOTOGHG", "N2O", "CH4"]},
            },
            "3.C": {
                "sources": [
                    "3.C.1",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                    "3.C.7",
                    "3.C.8",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "M.3.C.AG": {
                "sources": [
                    "M.3.C.1.AG",
                    "M.3.C.2.AG",
                    "M.3.C.3.AG",
                    "M.3.C.4.AG",
                    "M.3.C.5.AG",
                    "3.C.6",
                    "3.C.7",
                    "M.3.C.8.AG",
                ],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            # 3.D
            "M.3.D.LU": {
                "sources": ["3.D.1"],
                "sel": {"entity": ["KYOTOGHG", "CO2"]},
            },
            "M.3.D.AG": {
                "sources": ["M.3.D.2.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "3.D": {
                "sources": ["M.3.D.LU", "M.3.D.AG"],
                "sel": {"entity": ["KYOTOGHG", "CH4", "N2O", "CO2"]},
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG", "M.3.D.AG"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            # "3": {"sources": ["3.A", "3.B", "3.C", "3.D"]},
            # consistency check
            "M.AG": {
                "sources": ["3.A", "M.AG.ELV"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
            "M.LULUCF": {
                "sources": ["3.B", "M.3.C.8.LU", "M.3.D.LU"],
                "sel": {"entity": ["KYOTOGHG", "CO2"]},
            },
            "3": {
                "sources": ["M.AG", "M.LULUCF"],
                "sel": {"entity": ["KYOTOGHG"]},
            },
        },
    },
}

# step 3 downscaling and aggregation after downscaling
country_processing_step3 = {
    # downscale for 2020, 2021
    "downscale": {
        "entities": {
            "KYOTO_1": {
                "basket": f"KYOTOGHG ({gwp_to_use})",
                "basket_contents": ["CH4", "CO2", "N2O"],
                "sel": {
                    "category (IPCC2006_BGD)": [
                        "1.A",
                        "1.A.1",
                        "1.A.2",
                        "1.A.3",
                        "1.A.4",
                        "1.A.5",
                        "1.B",
                        "1.B.1",
                        "1.B.2",
                        "1.C",
                    ]
                },
            },
            "KYOTO_2": {
                "basket": f"KYOTOGHG ({gwp_to_use})",
                "basket_contents": ["CH4", "CO2", "N2O"],
                "sel": {
                    "category (IPCC2006_BGD)": [
                        "1.A",
                        "1.A.1",
                        "1.A.2",
                        "1.A.3",
                        "1.A.4",
                        "1.B",
                        "1.B.1",
                        "1.B.2",
                        "1.C",
                    ]
                },
            },
            "KYOTO_3A": {
                "basket": f"KYOTOGHG ({gwp_to_use})",
                "basket_contents": ["CH4", "N2O"],
                "sel": {"category (IPCC2006_BGD)": ["3.A.1", "3.A.2"]},
            },
            "KYOTO_3C": {
                "basket": f"KYOTOGHG ({gwp_to_use})",
                "basket_contents": ["CO2", "CH4", "N2O"],
                "sel": {
                    "category (IPCC2006_BGD)": [
                        "3.C.1",
                        "3.C.2",
                        "3.C.3",
                        "3.C.4",
                        "3.C.5",
                        "3.C.6",
                        "3.C.8",
                        "M.3.C.8.AG",
                        "M.3.C.8.LU",
                        "M.3.C.8.b",
                    ]
                },
            },
            "KYOTO_4": {
                "basket": f"KYOTOGHG ({gwp_to_use})",
                "basket_contents": ["CO2", "CH4", "N2O"],
                "sel": {"category (IPCC2006_BGD)": ["4.B", "4.C", "4.D"]},
            },
        },
    },
    # interpolate timeseries for IPPU subsectors as they either have explicit information
    # or are zero only
    "interpolate_ts": {
        "5": {
            "entities": ["CO2", "N2O"],
            "category": ["5.A", "5.B"],
        },
        "LULUCF": {
            "entities": ["CH4", "N2O"],
            "category": ["M.LULUCF"],
        },
        # interpolation needed because of a bug in the downscaling which is not
        # working when all data is nan or 0
        # Maybe there is a fix implemented that's not yet in primap2
        "1A5": {
            "category": [
                "1.A.5",
                "1.B.3",
                "1.C",
                "3.C.1",
                "3.C.2",
                "M.3.C.8.LU",
            ],
            "entities": ["CO2", "CH4", "N2O"],
        },
    },
    ## aggregating downscaled categories
    "aggregate_coords": {
        "category": {
            "3.A": {
                "sources": ["3.A.1", "3.A.2"],
            },
            "3.C": {
                "sources": [
                    "3.C.1",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                    "3.C.7",
                    "3.C.8",
                ],
            },
            "M.3.C.AG": {
                "sources": [
                    "3.C.1",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                    "3.C.7",
                    "M.3.C.8.AG",
                ],
            },
            # 3.D
            "M.3.D.LU": {
                "sources": ["3.D.1"],
            },
            "M.3.D.AG": {
                "sources": ["M.3.D.2.AG"],
            },
            "3.D": {
                "sources": ["M.3.D.LU", "M.3.D.AG"],
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG", "M.3.D.AG"],
            },
            "M.AG": {
                "sources": ["3.A", "M.AG.ELV"],
            },
            "M.LULUCF": {
                "sources": ["3.B", "M.3.C.8.LU", "M.3.D.LU"],
            },
            "3": {
                "sources": ["M.AG", "M.LULUCF"],
            },
            "5": {
                "sources": ["5.A", "5.B"],
            },
            "M.0.EL": {
                "sources": ["1", "2", "M.AG", "4", "5"],
            },
            "0": {
                "sources": ["M.0.EL", "M.LULUCF"],
            },
        }
    },
}


# TODO: HFCs basket, F-gases basket,

basket_copy = (
    {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["UnspMixOfHFCsPFCs", "UnspMixOfPFCs", "PFCS"],
        "source_GWP": gwp_to_use,
    },
)

gwps_for_basket_aggregation = [
    "SARGWP100",
    "AR4GWP100",
    "AR5GWP100",
    "AR6GWP100",
]

gas_baskets = {}
for gwp in gwps_for_basket_aggregation:
    gas_baskets.update(
        {
            f"HFCS ({gwp})": [
                "HFC23",
                "HFC32",
                "HFC125",
                "HFC134",
                "HFC134a",
                "HFC143a",
                "HFC227ea",
                "HFC245fa",
                "HFC365mfc",
                f"UnspMixOfHFCs ({gwp})",
            ],
            f"FGASES ({gwp})": [
                f"HFCS ({gwp})",
                f"PFCS ({gwp})",
                "SF6",
                "NF3",
                f"UnspMixOfHFCsPFCs ({gwp})",
            ],
            f"KYOTOGHG ({gwp})": [
                "CO2",
                "CH4",
                "N2O",
                f"FGASES ({gwp})",
            ],
        }
    )
