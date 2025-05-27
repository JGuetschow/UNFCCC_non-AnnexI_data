"""Config for Thailand's BUR5

Full configuration including PRIMAP2 conversion config and metadata

"""
# ###
# for reading
# ###

# general
gwp_to_use = "AR4GWP100"
terminology_proc = "IPCC2006_PRIMAP"

# 2019 inventory
inv_conf = {
    "year": 2019,
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    # special header as category UNFCCC_GHG_data and name in one column
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    # manual category codes (manual mapping to primap1, will be mapped to primap2
    # # automatically with the other codes)
    "cat_codes_manual": {
        "Total national emissions and removals": "0",
        "Memo Items (not accounted in total Emissions)": "MEMO",
        "International Bunkers": "MBK",
        "Aviation International Bunkers": "MBKA",
        "Marine-International Bunkers": "MBKM",
        "CO2 from biomass": "MBIO",
    },
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9]{1,4})[\s\.].*",
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_2006_THA_Inv",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR4",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NMVOCs": "NMVOC",
        "Nox": "NOx",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/624750",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Thailand. Biennial update report (BUR). BUR4",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

# main sector time series
# manual category codes (manual mapping to primap1, will be mapped to primap2
# automatically with the other codes)
cat_codes_manual_main_sector_ts = {
    "Energy": "1",
    "Industrial Processes and Product Use": "2",
    "Agriculture": "3",
    "LULUCF": "4",
    "Waste": "5",
    "Net emissions (Include LULUCF)": "0",
    "Total emissions (Exclude LULUCF)": "M0EL",
}

coords_cols_main_sector_ts = {
    "category": "category",
}

coords_defaults_main_sector_ts = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR4",
    "entity": f"KYOTOGHG ({gwp_to_use})",
    "unit": "GgCO2eq",
}

# indirect gases time series
coords_cols_indirect = {
    "entity": "entity",
}

coords_defaults_indirect = {
    "source": "THA-GHG-Inventory",
    "provenance": "measured",
    "area": "THA",
    "scenario": "BUR4",
    "category": "0",
    "unit": "Gg",
}

# ###
# for processing
# ###
# aggregate categories
country_processing_step1 = {
    "aggregate_cats": {
        "2.A.4": {
            "sources": ["2.A.4.b", "2.A.4.d"],
            "name": "Other Process uses of Carbonates",
        },
        "2.B.8": {
            "sources": ["2.B.8.b", "2.B.8.c", "2.B.8.e", "2.B.8.f"],
            "name": "Petrochemical and Carbon Black production",
        },
    },
    "aggregate_gases": {
        "KYOTOGHG": {
            "basket": "KYOTOGHG (AR4GWP100)",
            "basket_contents": [
                "CO2",
                "CH4",
                "N2O",
                "SF6",
                "HFCS (AR4GWP100)",
                "PFCS (AR4GWP100)",
            ],
            "skipna": True,
            "min_count": 1,
            "sel": {
                f"category ({coords_terminologies['category']})": [
                    "0",
                    "1",
                    "1.A",
                    "1.A.1",
                    "1.A.2",
                    "1.A.3",
                    "1.A.4",
                    "1.A.5",
                    "1.B",
                    "1.B.1",
                    "1.B.2",
                    "1.B.3",
                    "1.C",
                    "2",
                    "2.A",
                    "2.A.1",
                    "2.A.2",
                    "2.A.3",
                    "2.A.4",
                    "2.B",
                    "2.C",
                    "2.D",
                    "2.F",
                    "2.G",
                    "2.H",
                    "3",
                    "3.A",
                    "3.B",
                    "3.C",
                    "3.D",
                    "3.E",
                    "3.F",
                    "3.G",
                    "3.H",
                    "3.I",
                    "4",
                    "4.A",
                    "4.B",
                    "4.C",
                    "4.D",
                    "4.E",
                    "4.E.1",
                    "4.E.2",
                    "4.E.3",
                    "5",
                    "5.A",
                    "5.B",
                    "5.C",
                    "5.D",
                ]
            },  # not tested
        },
    },
}

country_processing_step2 = {
    "downscale": {
        # main sectors present as KYOTOGHG sum. subsectors need to be downscaled
        # TODO: downscale CO, NOx, NMVOC, SO2 (national total present)
        "sectors": {
            "1": {
                "basket": "1",
                "basket_contents": ["1.A", "1.B", "1.C"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "1.A": {
                "basket": "1.A",
                "basket_contents": ["1.A.1", "1.A.2", "1.A.3", "1.A.4", "1.A.5"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "1.B": {
                "basket": "1.B",
                "basket_contents": ["1.B.1", "1.B.2", "1.B.3"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "2": {
                "basket": "2",
                "basket_contents": ["2.A", "2.B", "2.C", "2.D", "2.F", "2.G", "2.H"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "2.A": {
                "basket": "2.A",
                "basket_contents": ["2.A.1", "2.A.2", "2.A.3", "2.A.4"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "3": {
                "basket": "3",
                "basket_contents": [
                    "3.A",
                    "3.B",
                    "3.C",
                    "3.D",
                    "3.E",
                    "3.F",
                    "3.G",
                    "3.H",
                    "3.I",
                ],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "4": {
                "basket": "4",
                "basket_contents": ["4.A", "4.B", "4.C", "4.D", "4.E"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "4.E": {
                "basket": "4.E",
                "basket_contents": ["4.E.1", "4.E.2", "4.E.3"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
            "5": {
                "basket": "5",
                "basket_contents": ["5.A", "5.B", "5.C", "5.D"],
                "entities": ["KYOTOGHG (AR4GWP100)"],
                "dim": f"category ({coords_terminologies['category']})",
            },
        },
        "entities": {
            "KYOTO": {
                "basket": "KYOTOGHG (AR4GWP100)",
                "basket_contents": [
                    "CH4",
                    "CO2",
                    "N2O",
                    "HFCS (AR4GWP100)",
                    "PFCS (AR4GWP100)",
                    "SF6",
                ],
                "sel": {
                    f"category ({coords_terminologies['category']})": [
                        "1",
                        "1.A",
                        "1.A.1",
                        "1.A.2",
                        "1.A.3",
                        "1.A.4",
                        "1.A.5",
                        "1.B",
                        "1.B.1",
                        "1.B.2",
                        "1.B.3",
                        "1.C",
                        "2",
                        "2.A",
                        "2.A.1",
                        "2.A.2",
                        "2.A.3",
                        "2.A.4",
                        "2.B",
                        "2.C",
                        "2.D",
                        "2.F",
                        "2.G",
                        "2.H",
                        "3",
                        "3.A",
                        "3.B",
                        "3.C",
                        "3.D",
                        "3.E",
                        "3.F",
                        "3.G",
                        "3.H",
                        "3.I",
                        "4",
                        "4.A",
                        "4.B",
                        "4.C",
                        "4.D",
                        "4.E",
                        "4.E.1",
                        "4.E.2",
                        "4.E.3",
                        "5",
                        "5.A",
                        "5.B",
                        "5.C",
                        "5.D",
                    ]
                },
            },
        },
    },
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS"],
        "source_GWP": gwp_to_use,
    },
}

cat_conversion = {
    "mapping": {
        "0": "0",
        "M.0.EL": "M.0.EL",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.1.a": "1.A.1.a",
        "1.A.1.b": "1.A.1.b",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.3.a": "1.A.3.a",
        "1.A.3.b": "1.A.3.b",
        "1.A.3.c": "1.A.3.c",
        "1.A.3.d": "1.A.3.d",
        "1.A.4": "1.A.4",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "1.B.3": "1.B.3",
        "1.C": "1.C",
        "1.C.1": "1.C.1",
        "1.C.2": "1.C.2",
        "1.C.3": "1.C.3",
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",
        "2.A.2": "2.A.2",
        "2.A.3": "2.A.3",
        "2.A.4": "2.A.4",
        "2.A.4.b": "2.A.4.b",
        "2.A.4.d": "2.A.4.d",
        "2.B": "2.B",
        "2.B.2": "2.B.2",
        "2.B.4": "2.B.4",
        "2.B.8": "2.B.8",
        "2.B.8.b": "2.B.8.b",
        "2.B.8.c": "2.B.8.c",
        "2.B.8.e": "2.B.8.e",
        "2.B.8.f": "2.B.8.f",
        "2.C": "2.C",
        "2.C.1": "2.C.1",
        "2.D": "2.D",
        "2.D.1": "2.D.1",
        "2.F": "2.F",
        "2.F.1": "2.F.1",
        "2.G": "2.G",
        "2.G.1": "2.G.1",
        "2.H": "2.H",
        "2.H.1": "2.H.1",
        "2.H.2": "2.H.2",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "M.3.C.1.b.i",  # field burning of agricultural residues
        "3.D": "3.C.2",  # Liming
        "3.E": "3.C.3",  # urea application
        "3.F": "3.C.4",  # direct N2O from agri soils
        "3.G": "3.C.5",  # indirect N2O from agri soils
        "3.H": "3.C.6",  # indirect N2O from manure management
        "3.I": "3.C.7",  # rice
        #'4': 'M.LULUCF',
        "4.A": "3.B.1.a",  # forest remaining forest
        "4.B": "3.B.2.a",  # cropland remaining cropland
        "4.C": "3.B.2.b",  # land converted to cropland
        "4.D": "3.B.6.b",  # land converted to other land
        #'4.E': 'M.3.C.1.LU',  # biomass burning (LULUCF)
        "4.E.1": "3.C.1.a",  # biomass burning (Forest Land)
        "4.E.2": "M.3.C.1.b.ii",  # biomass burning (Cropland)
        "4.E.3": "3.C.1.d",  # biomass burning (Other Land)
        "5": "4",
        "5.A": "4.A",
        "5.A.1": "4.A.1",
        "5.A.2": "4.A.2",
        "5.B": "4.B",
        "5.C": "4.C",
        "5.C.1": "4.C.1",
        "5.D": "4.D",
        "5.D.1": "4.D.1",
        "5.D.2": "4.D.2",
        "M.BK": "M.BK",
        "M.BK.A": "M.BK.A",
        "M.BK.M": "M.BM.M",
        "M.BIO": "M.BIO",
    },
    "aggregate": {
        "3.A": {"sources": ["3.A.1", "3.A.2"], "name": "Livestock"},
        "3.C.1.b": {
            "sources": ["M.3.C.1.b.i", "M.3.C.1.b.ii"],
            "name": "Biomass Burning In Cropland",
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            "name": "Biomass Burning (Agriculture)",
        },
        "M.3.C.1.LU": {
            "sources": ["3.C.1.a", "3.C.1.d"],
            "name": "Biomass Burning (LULUCF)",
        },
        "3.C.1": {
            "sources": ["M.3.C.1.AG", "M.3.C.1.LU"],
            "name": "Emissions from Biomass Burning",
        },
        "3.C": {
            "sources": ["3.C.1", "3.C.2", "3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
            "name": "Aggregate sources and non-CO2 emissions sources on land",
        },
        "M.3.C.AG": {
            "sources": [
                "M.3.C.1.AG",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
            ],
            "name": "Aggregate sources and non-CO2 emissions sources on land (Agriculture)",
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            "name": "Agriculture excluding livestock emissions",
        },
        "M.3.C.LU": {
            "sources": ["M.3.C.1.LU"],
            "name": "Aggregate sources and non-CO2 emissions sources on land (Land use)",
        },
        "3.B.1": {"sources": ["3.B.1.a"], "name": "Forest Land"},
        "3.B.2": {"sources": ["3.B.2.a", "3.B.2.b"], "name": "Cropland"},
        "3.B.6": {"sources": ["3.B.6.b"], "name": "Other Land"},
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.6"], "name": "Land"},
        "M.LULUCF": {"sources": ["3.B", "N.3.C.LU"], "name": "LULUCF"},
        "3": {"sources": ["M.AG", "M.LULUCF"], "name": "AFOLU"},
    },
}

sectors_to_save = [
    "1",
    "1.A",
    "1.A.1",
    "1.A.1.a",
    "1.A.1.b",
    "1.A.2",
    "1.A.3",
    "1.A.3.a",
    "1.A.3.b",
    "1.A.3.c",
    "1.A.3.d",
    "1.A.4",
    "1.A.5",
    "1.B",
    "1.B.1",
    "1.B.2",
    "1.B.3",
    "1.C",
    "1.C.1",
    "1.C.2",
    "1.C.3",
    "2",
    "2.A",
    "2.A.1",
    "2.A.2",
    "2.A.3",
    "2.A.4",
    "2.A.4.b",
    "2.A.4.d",
    "2.B",
    "2.B.2",
    "2.B.4",
    "2.B.8",
    "2.B.8.a",
    "2.B.8.c",
    "2.B.8.e",
    "2.B.8.f",
    "2.C",
    "2.C.1",
    "2.F",
    "2.F.1",
    "2.G",
    "2.G.1",
    "2.H",
    "2.H.1",
    "2.H.2",
    "3",
    "M.AG",
    "3.A",
    "3.A.1",
    "3.A.2",
    "3.C",
    "3.C.1",
    "3.C.1.a",
    "3.C.1.b",
    "3.C.1.d",
    "3.C.2",
    "3.C.3",
    "3.C.4",
    "3.C.5",
    "3.C.6",
    "3.C.7",
    "M.3.C.1.AG",
    "M.3.C.AG",
    "M.AG.ELV",
    "M.LULUCF",
    "M.3.C.1.LU",
    "M.3.C.LU",
    "3.B",
    "3.B.1",
    "3.B.1.a",
    "3.B.2",
    "3.B.2.a",
    "3.B.2.b",
    "3.B.6",
    "3.B.6.b",
    "4",
    "4.A",
    "4.A.1",
    "4.A.2",
    "4.B",
    "4.C",
    "4.C.1",
    "4.D",
    "4.D.1",
    "4.D.2",
    "0",
    "M.0.EL",
    "M.BK",
    "M.BK.A",
    "M.BK.M",
    "M.BIO",
]


# gas baskets
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
