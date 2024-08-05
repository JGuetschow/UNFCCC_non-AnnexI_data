"""
Configuration file to read Saint Kitts and Nevis' BUR 1.
"""

gwp_to_use = "AR5GWP100"

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "KNA-GHG-Inventory",
    "provenance": "measured",
    "area": "KNA",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "NMVOCs": "NMVOC",
        "Other halogenated gases with CO2 equivalent conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/633382",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Saint Kitts and Nevis. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_HFCS": {
        "category": "Other halogenated gases without CO2 equivalent conversion factors (2)"
    },
}

conf_general = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
}

conf = {
    "energy": {
        "entities": ["CO2", "CH4", "N2O", "NOX", "CO", "NMVOCs", "SO2"],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "149": {"skip_rows_start": 2},
            "150": {"skip_rows_start": 2},
            "151": {"skip_rows_start": 2},
            "152": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
    },
    "ipuu": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "HFCS",
            "PFCS",
            "SF6",
            "Other halogenated gases with CO2 equivalent conversion factors (1)",
            "Other halogenated gases without CO2 equivalent conversion factors (2)",
            "NOX",
            "CO",
            "NMVOC",
            "SO2",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "153": {"skip_rows_start": 2},
            "154": {"skip_rows_start": 2},
            "155": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "HFCS": "GgCO2eq",
            "PFCS": "GgCO2eq",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2 equivalent conversion factors (1)": "GgCO2eq",
            "Other halogenated gases without CO2 equivalent conversion factors (2)": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
            "SO2": "Gg",
        },
    },
    "AFOLU": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "NOX",
            "CO",
            "NMVOC",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "156": {"skip_rows_start": 3},
            "157": {"skip_rows_start": 3},
            "158": {"skip_rows_start": 3},
        },
        "replace_data_entries": {
            "NO,NA": "NO",
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
        },
    },
}
