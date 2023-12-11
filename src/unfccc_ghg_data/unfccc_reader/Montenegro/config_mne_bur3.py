"""Config for Montenegro's BUR3

Partial configuration for camelot adn data aggregation. PRIMAP2 conversion
config and metadata are define din the reading script

"""

# most time series are contained twice and 2005 data is also contained twice. Some
# data is inconsistent and we remove the time series with errors
drop_data = {
    2: {  # individual sector time series are (mostly) wrong, leave only 0.EL timeseries
        "cats": [
            "1",
            "1.A",
            "1.A.1",
            "1.A.1",
            "1.A.2",
            "1.A.3",
            "1.A.4",
            "1.A.5",
            "1.B",
            "1.B.1",
            "1.B.2",
            "2",
            "2.A",
            "2.B",
            "2.C",
            "2.D",
            "2.E",
            "2.F",
            "2.G",
            "2.H",
            "3",
            "3.A",
            "3.B",
        ],
        # "years": ["2005"], # 2005 data copy of 2019
    },
    3: {  # individual sector time series are (mostly) wrong, leave only 0.EL timeseries
        "cats": [
            "3.C",
            "3.D",
            "3.E",
            "3.F",
            "3.G",
            "5",
            "5.A",
            "5.B",
            "5.C",
            "5.D",
            "6",
        ]
        # "years": ["2005"],
    },
    6: {  # 2005 data copy of 2019
        "years": ["2005"],
    },
    7: {  # 2005 data copy of 2019 for 3.G
        "years": ["2005"],
    },
    25: {  # 2005 data copy of 2019 (CO2, 2005-2019, first table)
        "years": ["2005"],
    },
    26: {  # 2005 data copy of 2019 (CO2, 2005-2019, second table)
        "years": ["2005"],
    },
}

cat_mapping = {
    "3": "M.AG",
    "3.A": "3.A.1",
    "3.B": "3.A.2",
    "3.C": "3.C.7",  # rice
    "3.D": "M.3.C.45AG",  # Agricultural soils
    "3.E": "3.C.1.c",  # prescribed burning of savanna
    "3.F": "3.C.1.b",  # field burning of agricultural residues
    "3.G": "3.C.3",  # urea application
    "4": "M.LULUCF",
    "4.A": "3.B.1",  # forest
    "4.B": "3.B.2",  # cropland
    "4.C": "3.B.3",  # grassland
    "4.D": "3.B.4",  # wetland
    "4.E": "3.B.5",  # Settlements
    "4.F": "3.B.6",  # other land
    "4.G": "3.D.1",  # HWP
    "5": "4",
    "5.A": "4.A",
    "5.B": "4.B",
    "5.C": "4.C",
    "5.D": "4.D",
    "6": "5",
}

aggregate_cats = {
    "3.A": {"sources": ["3.A.1", "3.A.2"], "name": "Livestock"},
    "3.B": {
        "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
        "name": "Land",
    },
    "M.3.C.1.AG": {
        "sources": ["3.C.1.c", "3.C.1.b"],
        "name": "Emissions from Biomass " "Burning (Agriculture)",
    },
    "3.C.1": {
        "sources": ["3.C.1.c", "3.C.1.b"],
        "name": "Emissions from Biomass Burning",
    },
    "3.C": {
        "sources": ["3.C.1", "3.C.3", "M.3.C.45AG", "3.C.7"],
        "name": "Aggregate sources and non-CO2 emissions sources on land",
    },
    "M.3.C.AG": {
        "sources": ["3.C.1.AG", "3.C.3", "M.3.C.45AG", "3.C.7"],
        "name": "Aggregate sources and non-CO2 emissions sources on land (Agriculture)",
    },
    "3.D": {"sources": ["3.D.1"], "name": "Other"},
    "3": {"sources": ["M.AG", "M.LULUCF"], "name": "AFOLU"},
    "M.AG.ELV": {
        "sources": ["M.3.C.AG"],
        "name": "Agriculture excluding livestock emissions",
    },
    "0": {"sources": ["1", "2", "3", "4", "5"]},
}
