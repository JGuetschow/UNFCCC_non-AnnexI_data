"""Specification for CTF-NDC tables submission round 1"""

gwp_to_use = "AR5GWP100"

CTF1 = {
    "Table7": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 30,
            "header": ["unit", "time"],
            "col_for_categories": "category_entity",  # renamed in code
            "categories": ["category", "entity"],
            "cols_to_ignore": [],
            "stop_cats": [
                "nan",
                "a Each Party shall report projections pursuant to paras. 93–101 of "  # noqa: RUF001
                "the MPGs; those developing country Parties that need flexibility in "
                "the light of their capacities are instead encouraged to report "
                "such projections (para. 92 of the MPGs).",
            ],
            "unit_replacement": {
                "(kt CO2 eq)c": "kt CO2eq",
                "(kt CO2 eq)c.1": "kt CO2eq",
            },
        },
        "sector_mapping": [
            ["Sectord", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Energy", ["1.A.1", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Transport", ["1.A.3", f"KYOTOGHG ({gwp_to_use})"], 1],
            [
                "Industrial processes and product use",
                ["2", f"KYOTOGHG ({gwp_to_use})"],
                1,
            ],
            ["Agriculture", ["M.AG", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Forestry/LULUCF", ["M.LULUCF", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Waste management/waste", ["4", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Other (specify)", ["5", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Gas", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["CO2 emissions including net CO2 from LULUCF", ["0", "CO2"], 1],
            ["CO2 emissions excluding net CO2 from LULUCF", ["M.0.EL", "CO2"], 1],
            [
                "CH4 emissions including CH4 from LULUCF",
                ["0", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "CH4 emissions excluding CH4 from LULUCF",
                ["M.0.EL", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions including N2O from LULUCF",
                ["0", f"N2O ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions excluding N2O from LULUCF",
                ["M.0.EL", f"N2O ({gwp_to_use})"],
                1,
            ],
            ["HFCs", ["M.0.EL", f"HFCS ({gwp_to_use})"], 1],
            ["PFCs", ["M.0.EL", f"PFCS ({gwp_to_use})"], 1],
            ["SF6", ["M.0.EL", f"SF6 ({gwp_to_use})"], 1],
            ["NF3", ["M.0.EL", f"NF3 ({gwp_to_use})"], 1],
            ["Other (specify)", ["\\IGNORE", "\\IGNORE"], 1],
            ["Total with LULUCF", ["0", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Total without LULUCF", ["M.0.EL", f"KYOTOGHG ({gwp_to_use})"], 0],
        ],
        "coords_defaults": {
            "scenario": "with measures",
        },
    },  # tested
    "Table8": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 30,
            "header": ["unit", "time"],
            "col_for_categories": "category_entity",  # renamed in code
            "categories": ["category", "entity"],
            "cols_to_ignore": [],
            "stop_cats": [
                "nan",
                "a Each Party shall report projections pursuant to paras. 93–101 of "  # noqa: RUF001
                "the MPGs; those developing country Parties that need flexibility in "
                "the light of their capacities are instead encouraged to report "
                "such projections (para. 92 of the MPGs).",
            ],
            "unit_replacement": {
                "(kt CO2 eq)c": "kt CO2eq",
                "(kt CO2 eq)c.1": "kt CO2eq",
            },
        },
        "sector_mapping": [
            ["Sectord", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Energy", ["1.A.1", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Transport", ["1.A.3", f"KYOTOGHG ({gwp_to_use})"], 1],
            [
                "Industrial processes and product use",
                ["2", f"KYOTOGHG ({gwp_to_use})"],
                1,
            ],
            ["Agriculture", ["M.AG", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Forestry/LULUCF", ["M.LULUCF", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Waste management/waste", ["4", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Other (specify)", ["5", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Gas", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["CO2 emissions including net CO2 from LULUCF", ["0", "CO2"], 1],
            ["CO2 emissions excluding net CO2 from LULUCF", ["M.0.EL", "CO2"], 1],
            [
                "CH4 emissions including CH4 from LULUCF",
                ["0", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "CH4 emissions excluding CH4 from LULUCF",
                ["M.0.EL", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions including N2O from LULUCF",
                ["0", f"N2O ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions excluding N2O from LULUCF",
                ["M.0.EL", f"N2O ({gwp_to_use})"],
                1,
            ],
            ["HFCs", ["M.0.EL", f"HFCS ({gwp_to_use})"], 1],
            ["PFCs", ["M.0.EL", f"PFCS ({gwp_to_use})"], 1],
            ["SF6", ["M.0.EL", f"SF6 ({gwp_to_use})"], 1],
            ["NF3", ["M.0.EL", f"NF3 ({gwp_to_use})"], 1],
            ["Other (specify)", ["\\IGNORE", "\\IGNORE"], 1],
            ["Total with LULUCF", ["0", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Total without LULUCF", ["M.0.EL", f"KYOTOGHG ({gwp_to_use})"], 0],
        ],
        "coords_defaults": {
            "scenario": "with additional measures",
        },
    },  # tested
    "Table9": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 30,
            "header": ["unit", "time"],
            "col_for_categories": "category_entity",  # renamed in code
            "categories": ["category", "entity"],
            "cols_to_ignore": [],
            "stop_cats": [
                "nan",
                "a Each Party shall report projections pursuant to paras. 93–101 of "  # noqa: RUF001
                "the MPGs; those developing country Parties that need flexibility in "
                "the light of their capacities are instead encouraged to report "
                "such projections (para. 92 of the MPGs).",
            ],
            "unit_replacement": {
                "(kt CO2 eq)c": "kt CO2eq",
                "(kt CO2 eq)c.1": "kt CO2eq",
            },
        },
        "sector_mapping": [
            ["Sectord", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Energy", ["1.A.1", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Transport", ["1.A.3", f"KYOTOGHG ({gwp_to_use})"], 1],
            [
                "Industrial processes and product use",
                ["2", f"KYOTOGHG ({gwp_to_use})"],
                1,
            ],
            ["Agriculture", ["M.AG", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Forestry/LULUCF", ["M.LULUCF", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Waste management/waste", ["4", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Other (specify)", ["5", f"KYOTOGHG ({gwp_to_use})"], 1],
            ["Gas", ["\\IGNORE", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["CO2 emissions including net CO2 from LULUCF", ["0", "CO2"], 1],
            ["CO2 emissions excluding net CO2 from LULUCF", ["M.0.EL", "CO2"], 1],
            [
                "CH4 emissions including CH4 from LULUCF",
                ["0", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "CH4 emissions excluding CH4 from LULUCF",
                ["M.0.EL", f"CH4 ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions including N2O from LULUCF",
                ["0", f"N2O ({gwp_to_use})"],
                1,
            ],
            [
                "N2O emissions excluding N2O from LULUCF",
                ["M.0.EL", f"N2O ({gwp_to_use})"],
                1,
            ],
            ["HFCs", ["M.0.EL", f"HFCS ({gwp_to_use})"], 1],
            ["PFCs", ["M.0.EL", f"PFCS ({gwp_to_use})"], 1],
            ["SF6", ["M.0.EL", f"SF6 ({gwp_to_use})"], 1],
            ["NF3", ["M.0.EL", f"NF3 ({gwp_to_use})"], 1],
            ["Other (specify)", ["\\IGNORE", "\\IGNORE"], 1],
            ["Total with LULUCF", ["0", f"KYOTOGHG ({gwp_to_use})"], 0],
            ["Total without LULUCF", ["M.0.EL", f"KYOTOGHG ({gwp_to_use})"], 0],
        ],
        "coords_defaults": {
            "scenario": "without measures",
        },
    },  # tested
}
