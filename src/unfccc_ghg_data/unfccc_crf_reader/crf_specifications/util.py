"""Some definitions used for several CRF specifications"""

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
            "CO2 equivalent (kt) (2)": "kt CO2eq",  # TUN Table2(II)
            "CO2 equivalents (kt) (2)": "kt CO2eq",  # for AUS Table2(II)
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
            "CO2 equivalents (kt) (1) ": "kt CO2eq",  # for TUN table1
            "CO2 equivalents (kt)(1)": "kt CO2eq",  # for TUN table3
            "CO2 equivalents (kt) (1)": "kt CO2eq",  # for TUN table5
            "CO2 equivalent (kt) (2)": "kt CO2eq",  # for TUN table2(I)
            "CO2 equivalents (kt) (2) ": "kt CO2eq",  # for AUS Table1
            "CO2 equivalent (kt) (3)": "kt CO2eq",  # for AUS, Table2(I)
            "CO2 equivalents (kt) (3)": "kt CO2eq",  # for AUS, Table2(I)
            "CO2 equivalents (kt) (2)": "kt CO2eq",  # for AUS Table3
            "CO2 equivalents (kt) (4)": "kt CO2eq",  # for AUS Table4
        },
        "default_unit": "kt",
    },
    "summary": {  # contains fgas mixtures in CO2 eq units
        "unit_row": 0,
        "entity_row": "header",
        "regexp_entity": r".*",
        "regexp_unit": r"\((.*)\)",
        "manual_repl_unit": {
            "(kt CO2 equivalent)": "kt CO2eq",
            "CO2 equivalents (kt) (3)": "kt CO2eq",  # for AUS
            "CO2 equivalents (kt) (2)": "kt CO2eq",  # for TUN
            "CO2 equivalent (kt) (2)": "kt CO2eq",  # for TUN
        },
        "default_unit": "kt",
    },
}
