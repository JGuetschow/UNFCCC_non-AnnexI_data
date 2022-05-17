""" Some definitions used for several CRF specifications"""

unit_info = {
    "default": {
        "unit_row": 0,
        "entity_row": "header",
        "regexp_entity": r".*",
        "regexp_unit": r"\((.*)\)",
        "manual_repl_unit": {},
        "default_unit": "kt",
    },
    "fgases": {
        "unit_row": 0,
        "entity_row": "header",
        "regexp_entity": r".*",
        "regexp_unit": r"\((.*)\)",
        "manual_repl_unit": {
            "CO2 equivalent (kt)": "kt CO2eq",
        },
        "default_unit": "t",
    },
    "industry": {  # contains fgas mixtures in CO2 eq units
        "unit_row": 0,
        "entity_row": "header",
        "regexp_entity": r".*",
        "regexp_unit": r"\((.*)\)",
        "manual_repl_unit": {
            "CO2 equivalent (kt)": "kt CO2eq",
        },
        "default_unit": "kt",
    },
}