"""
Configuration file to read Saint Kitts and Nevis' BUR 1.
"""

conf_general = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
}

conf = {
    "energy": {
        "header": ["orig_category", "CO2", "CH4", "N2O", "NOX", "CO", "NMVOCs", "SO2"],
        "unit": [8 * "Gg"],
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
    }
}
