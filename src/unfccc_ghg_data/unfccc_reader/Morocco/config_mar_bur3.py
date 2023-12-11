"""Config for Morocco's BUR3

Partial configuration for camelot adn data aggregation. PRIMAP2 conversion
config and metadata are define din the reading script

"""

# define which raw tables to combine
table_defs = {
    2010: {
        "Energy": [0, 1],
        "Agriculture": [10],
        "IPPU": [15, 16, 17],
        "LULUCF": [30],
        "Waste": [35],
    },
    2012: {
        "Energy": [2, 3],
        "Agriculture": [11],
        "IPPU": [18, 19, 20],
        "LULUCF": [31],
        "Waste": [36],
    },
    2014: {
        "Energy": [4, 5],
        "Agriculture": [10],
        "IPPU": [21, 22, 23],
        "LULUCF": [32],
        "Waste": [37],
    },
    2016: {
        "Energy": [6, 7],
        "Agriculture": [10],
        "IPPU": [24, 25, 26],
        "LULUCF": [33],
        "Waste": [38],
    },
    2018: {
        "Energy": [8, 9],
        "Agriculture": [14],
        "IPPU": [27, 28, 29],
        "LULUCF": [34],
        "Waste": [39],
    },
}

header_defs = {
    "Energy": [
        ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "COVNM", "SO2"],
        ["", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg"],
    ],
    "Agriculture": [
        ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "COVNM", "SO2"],
        ["", "Gg", "GgCO2eq", "GgCO2eq", "Gg", "Gg", "Gg", "Gg"],
    ],  # units are wrong
    # in BUR pdf
    "IPPU": [
        [
            "Catégories",
            "CO2",
            "CH4",
            "N2O",
            "HFCs",
            "PFCs",
            "SF6",
            "NOx",
            "CO",
            "COVNM",
            "SO2",
        ],
        [
            "",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "Gg",
            "Gg",
            "Gg",
            "Gg",
        ],
    ],
    "LULUCF": [
        ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "COVNM", "SO2"],
        ["", "GgCO2eq", "GgCO2eq", "GgCO2eq", "Gg", "Gg", "Gg", "Gg"],
    ],
    "Waste": [
        ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "COVNM", "SO2"],
        ["", "GgCO2eq", "GgCO2eq", "GgCO2eq", "Gg", "Gg", "Gg", "Gg"],
    ],
}

remove_cats = ["3.A.4", "3.B", "3.B.4", "1.B.2.a", "1.B.2.b", "1.B.2.c"]

cat_mapping = {
    "1.B.2.a.4": "1.B.2.a.iii.4",
    "1.B.2.a.5": "1.B.2.a.iii.5",
    "1.B.2.a.6": "1.B.2.a.iii.6",
    "1.B.2.b.2": "1.B.2.b.iii.2",
    "1.B.2.b.4": "1.B.2.b.iii.4",
    "1.B.2.b.5": "1.B.2.b.iii.5",
    "1.B.2.b.6": "1.B.2.b.iii.6",
    "1.B.2.c.1": "1.B.2.b.i",  # simplification, split to oil and gas ("1.B.2.X.i")
    "1.B.2.c.2": "1.B.2.b.ii",  # simplification, split to oil and gas ("1.B.2.X.ii")
    "1.A.2.g": "1.A.2.m",  # other industry
    "3.A": "3.A.1",  # enteric fermentation
    "3.A.1": "3.A.1.a",  # cattle
    "3.A.1.a": "3.A.1.a.i",
    "3.A.1.b": "3.A.1.a.ii",
    "3.A.2": "3.A.1.c",
    "3.A.3": "3.A.1.h",  # Swine
    "3.A.4.a": "3.A.1.d",  # goats
    "3.A.4.b": "3.A.1.e",  # camels
    "3.A.4.c": "3.A.1.f",  # horses
    "3.A.4.d": "3.A.1.g",  # Mules and asses
    "3.A.4.e": "3.A.1.i",  # poultry
    #    '3.B': '3.A.2', # Manure Management
    "3.B.1": "3.A.2.a",  # cattle
    "3.B.1.a": "3.A.2.a.i",
    "3.B.1.b": "3.A.2.a.ii",
    "3.B.2": "3.A.2.c",  # Sheep
    "3.B.3": "3.A.2.h",  # Swine
    "3.B.4.a": "3.A.2.d",  # Goats
    "3.B.4.b": "3.A.2.e",  # Camels
    "3.B.4.c": "3.A.2.f",  # Horses
    "3.B.4.d": "3.A.2.g",  # Mules and Asses
    "3.B.4.e": "3.A.2.i",  # Poultry
    "3.B.5": "3.C.6",  # indirect N2O from manure management
    "3.C": "3.C.7",  # rice
    "3.D": "M.3.C.45AG",  # Agricultural soils
    "3.D.a": "3.C.4",  # direct N2O from agri soils
    "3.D.a.1": "3.C.4.a",  # inorganic fertilizers
    "3.D.a.2": "3.C.4.b",  # organic fertilizers
    "3.D.a.3": "3.C.4.c",  # urine and dung by grazing animals
    "3.D.a.4": "3.C.4.d",  # N in crop residues
    "3.D.b": "3.C.5",  # indirect N2O from managed soils
    "3.D.b.1": "3.C.5.a",  # Atmospheric deposition
    "3.D.b.2": "3.C.5.b",  # nitrogen leeching and runoff
    "3.H": "3.C.3",  # urea application
    "LU.3.B.1": "3.B.1",  # forest
    "LU.3.B.2": "3.B.2",  # cropland
    "LU.3.B.3": "3.B.3",  # grassland
    "LU.3.B.4": "3.B.4",  # wetland
    "LU.3.B.5": "3.B.5",  # Settlements
    "LU.3.B.6": "3.B.6",  # other land
}

aggregate_cats = {
    "1.B.2.a.iii": {
        "sources": ["1.B.2.a.iii.4", "1.B.2.a.iii.5", "1.B.2.a.iii.6"],
        "name": "All Other",
    },
    "1.B.2.b.iii": {
        "sources": [
            "1.B.2.b.iii.2",
            "1.B.2.b.iii.4",
            "1.B.2.b.iii.5",
            "1.B.2.b.iii.6",
        ],
        "name": "All Other",
    },
    "1.B.2.a": {"sources": ["1.B.2.a.iii"], "name": "Oil"},
    "1.B.2.b": {
        "sources": ["1.B.2.b.i", "1.B.2.b.ii", "1.B.2.b.iii"],
        "name": "Natural Gas",
    },
    "2.D": {
        "sources": ["2.D.4"],
        "name": "Non-Energy Products from Fuels and Solvent Use",
    },
    "2.F.1": {
        "sources": ["2.F.1.a", "2.F.1.b"],
        "name": "Refrigeration and Air Conditioning",
    },
    "2.F": {
        "sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4", "2.F.5", "2.F.6"],
        "name": "Product uses as Substitutes for Ozone Depleting Substances",
    },
    "2.H": {"sources": ["2.H.1", "2.H.2", "2.H.3"], "name": "Other"},
    "3.A.2": {
        "sources": [
            "3.A.2.a",
            "3.A.2.c",
            "3.A.2.d",
            "3.A.2.e",
            "3.A.2.f",
            "3.A.2.g",
            "3.A.2.h",
            "3.A.2.i",
        ],
        "name": "Manure Management",
    },
    "3.A": {"sources": ["3.A.1", "3.A.2"], "name": "Livestock"},
    "3.B": {
        "sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"],
        "name": "Land",
    },
    "3.C": {
        "sources": ["3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
        "name": "Aggregate sources and non-CO2 emissions sources on land",
    },
    "M.3.C.AG": {
        "sources": ["3.C.3", "3.C.4", "3.C.5", "3.C.6", "3.C.7"],
        "name": "Aggregate sources and non-CO2 emissions sources on land (Agriculture)",
    },
    "M.AG": {"sources": ["3.A", "M.3.C.AG"], "name": "Agriculture"},
    "3": {"sources": ["M.AG", "M.LULUCF"], "name": "AFOLU"},
    "M.AG.ELV": {
        "sources": ["M.3.C.AG"],
        "name": "Agriculture excluding livestock emissions",
    },
    "4": {"sources": ["4.A", "4.D"], "name": "Waste"},
    "0": {"sources": ["1", "2", "3", "4"]},
    "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
}

zero_cats = ["1.B.2.a.i", "1.B.2.a.ii"]  # venting and flaring with 0 for oil as
# all mapped to natural gas
