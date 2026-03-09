"""Config for Thailand's BUR4

Full configuration including PRIMAP2 conversion config and metadata

"""


# ###
# for reading
# ###

# general
gwp_to_use = "SARGWP100"
terminology_proc = "IPCC2006_PRIMAP"

# inventory
def_inv_config = {
    # "entity_row": 1,
    # "unit_row": 0,
    "index_cols": "Categories",
    # "header": header_inventory,
    # "unit": unit_inventory,
    # special header as category UNFCCC_GHG_data and name in one column
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    # manual category codes (manual mapping to primap1, will be mapped to primap2
    # # automatically with the other codes)
    "cat_codes_manual": {
        "International Bunkers": "M.BK",
        "1.A.3.d.i - International water-borne navigation (International bunkers) (2)": "M.BK.M",
        "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
        "1.A.3.a.i - International Aviation (International Bunkers) (2)": "M.BK.A",
        "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
        "CO2 from Biomass": "M.BIO",
        "CO2 from Biomass Combustion for Energy Production": "M.BIO",
        "": "\\IGNORE",
        # "Memo Items (5)": "\\IGNORE",
        "1.A.5.c - Multilateral Operations (5)": "M.MULTIOP",
        "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
        "Total National Emissions and Removals": "0",
        "Total Net emissions": "0",
    },
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s].*",
    "unit_replace": {
        "(Gg)": "Gg",
        "CO2 Equivalents (Gg)": "GgCO2eq",
    },
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006",
    "scenario": "PRIMAP",
}

coords_terminologies_1996 = {
    "area": "ISO3",
    "category": "IPCC1996",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "IRQ-GHG-Inventory",
    "provenance": "measured",
    "area": "IRQ",
    "scenario": "BUR1",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "Net CO2 (1)(2)": "CO2",
        "2Net CO": "CO2",
        "Net CO2 emissions/removals": "CO2",
        "Net CO2 emissions / removals": "CO2",
        "EmissionsCH4": "CH4",
        "4 CH": "CH4",
        "O2N": "N2O",
        "CO Gg": "CO",
        "X NO": "NOx",
        "x NO": "NOx",
        "xSO": "SOx",
        "xSo": "SOx",
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NMVOCs": "NMVOC",
        "Other halogenated gases with CO2 equivalent conversion factors (3)": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
    },
}

filter_remove = {
    "f_memo": {"category": ["\\IGNORE", "Memo", "Information"]},
    "f_other": {
        "entity": [
            "Other halogenated gases without CO2 equivalent conversion factors (4)"
        ],
    },
}
filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/650065",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Traq. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

################################### OLD ##############################

# ###
# for processing
# ###
# aggregate categories
country_processing_step1 = {
    "basket_copy": {
        "GWPs_to_add": ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS", "UnspMixOfHFCsPFCs"],
        "source_GWP": gwp_to_use,
    },
    "aggregate_coords": {
        f"category ({coords_terminologies['category']})": {
            "1.B": {  # because we had to fix 1.B for year 2000
                "sources": ["1.B.1", "1.B.2", "1.C"],
                "sel": {
                    "entity": ["CO2", "CH4", "N2O", "NOx", "CO", "SO2", "NMVOC"],
                },
            },
            "1": {  # because we had to fix 1.B for year 2000
                "sources": ["1.A", "1.B", "1.C"],
                "sel": {
                    "entity": ["CO2", "CH4", "N2O", "NOx", "CO", "SO2", "NMVOC"],
                },
            },
            "M.3.C.1.AG": {
                "sources": ["3.C.1.b"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.3.C.1.LU": {
                "sources": ["3.C.1.a"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.3.C.AG": {
                "sources": [
                    "M.3.C.1.AG",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                ],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.AG": {
                "sources": ["M.AG.ELV", "3.A"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "M.LULUCF": {
                "sources": ["3.B", "3.D", "M.3.C.1.LU"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "3": {  # conmsistency check
                "sources": ["M.AG", "M.LULUCF"],
                "sel": {
                    "entity": ["CH4", "CO2", "N2O", "NOx", "CO"],
                },
            },
            "0": {  # consistency check
                "sources": ["1", "2", "3", "4"],
                "sel": {
                    "entity": [
                        "CH4",
                        "CO2",
                        "N2O",
                        "NOx",
                        "CO",
                        "SO2",
                        "NMVOC",
                        "SF6",
                        f"HFCS ({gwp_to_use})",
                        f"PFCS ({gwp_to_use})",
                        f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                    ],
                },
            },
            "M.0.EL": {
                "sources": ["1", "2", "M.AG", "4"],
                "sel": {
                    "entity": [
                        "CH4",
                        "CO2",
                        "N2O",
                        "NOx",
                        "CO",
                        "SO2",
                        "NMVOC",
                        "SF6",
                        f"HFCS ({gwp_to_use})",
                        f"PFCS ({gwp_to_use})",
                        f"UnspMixOfHFCsPFCs ({gwp_to_use})",
                    ],
                },
            },
        }
    },
}

gas_baskets = {
    "FGASES (SARGWP100)": [
        "HFCS (SARGWP100)",
        "PFCS (SARGWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (SARGWP100)",
    ],
    "FGASES (AR4GWP100)": [
        "HFCS (AR4GWP100)",
        "PFCS (AR4GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR4GWP100)",
    ],
    "FGASES (AR5GWP100)": [
        "HFCS (AR5GWP100)",
        "PFCS (AR5GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR5GWP100)",
    ],
    "FGASES (AR6GWP100)": [
        "HFCS (AR6GWP100)",
        "PFCS (AR6GWP100)",
        "SF6",
        "UnspMixOfHFCsPFCs (AR6GWP100)",
    ],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
