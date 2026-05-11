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
    "category": "IPCC2006_PRIMAP",
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

## processing configuration

# TODO: check if this aggregation step is enough or if something is missing
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
            "2.F": {  # only 2.F has HFCS, but the sector lacks gas resolution
                "sources": ["2"],
                "sel": {
                    "variable": [
                        "HFC125",
                        "HFC134a",
                        "HFC143a",
                        "HFC227ea",
                        "HFC23",
                        "HFC245fa",
                        "HFC32",
                        "HFC365mfc",
                        "NF3",
                        "SF6",
                    ],
                },
            },
        },
    },
}

# TODO collection of issues
# UnspMix is zero for IPPU, but non-zero for 2.F.1, 2.F.2, 2.F.3
# the reason is the for cat 2 the gases are resolved while they are resolved while they
# are not resolved for 2.F.x

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
            ],
            "category": [
                "2.C.3",
                "2.F.1",
                "2.F.2",
                "2.F.3",
                "2.F.4",
            ],
        },
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
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
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
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.A.2.j": {
                "sources": [
                    "3.A.2.j.vi",
                ],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
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
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.A": {
                "sources": ["3.A.1", "3.A.2"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            ## 3.B (consistency check)
            "3.B": {
                "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            ## 3.C
            "3.C.1": {
                "sources": ["M.3.C.1.SAV", "3.C.1.b"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "M.3.C.1.AG": {
                "sources": ["M.3.C.1.SAV", "3.C.1.b"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.2": {
                "sources": ["M.3.C.2.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.3": {
                "sources": ["M.3.C.3.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.4": {
                "sources": ["M.3.C.4.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.4.a": {
                "sources": ["M.3.C.4.a.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.4.b": {
                "sources": ["M.3.C.4.b.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.4.e": {
                "sources": ["M.3.C.4.e.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.4.f": {
                "sources": ["M.3.C.4.f.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.C.5": {
                "sources": ["M.3.C.5.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },  # , "M.3.C.5.LU"]},
            "3.C": {
                "sources": [
                    "3.C.1",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                    "3.C.7",
                ],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
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
                ],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            # 3.D
            "M.3.D.2.AG": {
                "sources": ["M.3.D.2.a.AG", "M.3.D.2.b.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.D.2": {
                "sources": ["M.3.D.2.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "M.3.D.LU": {
                "sources": ["3.D.1"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "M.3.D.AG": {
                "sources": ["M.3.D.2.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3.D": {
                "sources": ["M.3.D.LU", "M.3.D.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG", "M.3.D.AG"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            # "3": {"sources": ["3.A", "3.B", "3.C", "3.D"]},
            # consistency check
            "M.AG": {
                "sources": ["3.A", "M.AG.ELV"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "M.LULUCF": {
                "sources": ["3.B", "M.3.D.LU"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
            "3": {
                "sources": ["M.AG", "M.LULUCF"],
                "sel": {"entity": [f"KYOTOGHG ({gwp_to_use})"]},
            },
        },
    },
    # downscale for 2020, 2021
}

# Note on downscaling: Data are always available for the same years: 2013-2019,
# so temporal downscaling does not makes sense here.
# TODO: Perhaps entity, category downscaling can be done?


# TODO: HFCs basket, F-gases basket,
gas_baskets = {
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O"],
}
