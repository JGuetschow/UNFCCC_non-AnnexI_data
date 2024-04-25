# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "GIN-GHG-Inventory",
    "provenance": "measured",
    "area": "GIN",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# gwp conversion is mentioned on page 20 in the report
gwp_to_use = "AR4GWP100"
coords_value_mapping = {
    "main": {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            "HFCs": f"HFCS ({gwp_to_use})",
            "PFCs": f"PFCS ({gwp_to_use})",
            "SF6": f"SF6 ({gwp_to_use})",
            "NMVOCs": "NMVOC",
        },
    },
    "energy": {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            "NMVOCs": "NMVOC",
        },
    },
    "afolu": {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            "NMVOCs": "NMVOC",
        },
    },
    "waste": {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            "NMVOCs": "NMVOC",
        },
    },
    "trend": {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            "NMVOCs": "NMVOC",
        },
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
}

meta_data = {
    "references": "https://unfccc.int/documents/629549",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Guinea. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

page_def_templates = {
    "110": {
        "area": ["36,718,589,87"],
        "cols": ["290,340,368,392,425,445,465,497,535,564"],
    },
    "111": {
        "area": ["36,736,587,107"],
        "cols": ["293,335,369,399,424,445,468,497,535,565"],
    },
    "112": {
        "area": ["35,733,588,106"],
        "cols": ["293,335,369,399,424,445,468,497,535,565"],
    },
    "113": {
        "area": ["35,733,588,106"],
        "cols": ["293,335,365,399,424,445,468,497,535,565"],
    },
    "131": {
        "area": ["36,718,590,83"],
        "cols": ["293,332,370,406,442,480,516,554"],
    },
}

# for main table
header_inventory = [
    "Greenhouse gas source and sink categories",
    "CO2",
    "CH4",
    "N2O",
    "HFCs",
    "PFCs",
    "SF6",
    "NOx",
    "CO",
    "NMVOCs",
    "SO2",
]

unit_inventory = ["-"] + ["Gg"] * len(
    header_inventory
)  # one extra for the category columns
unit_inventory[4] = "GgCO2eq"
unit_inventory[5] = "GgCO2eq"
unit_inventory[6] = "GgCO2eq"

# for energy tables
header_energy = [
    "Greenhouse gas source and sink categories",
    "CO2",
    "CH4",
    "N2O",
    "NOx",
    "CO",
    "NMVOCs",
    "SO2",
]
unit_energy = ["-"] + ["Gg"] * len(header_energy)  # one extra for the category columns

# for afolu tables
header_afolu = [
    "Greenhouse gas source and sink categories",
    "CO2",
    "CH4",
    "N2O",
    "NOx",
    "CO",
    "NMVOCs",
]
unit_afolu = ["-"] + ["Gg"] * (len(header_afolu) - 1)

# for waste table
header_waste = [
    "Greenhouse gas source and sink categories",
    "CO2",
    "CH4",
    "N2O",
    "NOx",
    "CO",
    "NMVOCs",
    "SO2",
]
unit_waste = ["-"] + ["Gg"] * (len(header_waste) - 1)

# for trend table (unit is always Gg for this table)
# 'data' prefix is needed for pd.wide_to_long() later
header_trend = [
    "orig_cat_name",
    "data1990",
    "data1995",
    "data2000",
    "data2005",
    "data2010",
    "data2015",
    "data2018",
    "data2019",
]

set_value = {
    "main": {
        "110": [
            (4, 0, "1.A.1 - Industries énergétiques"),
            (8, 0, "1.A.4 - Autres secteurs"),
        ],
        "111": [
            (4, 0, "1.A.1 - Industries énergétiques"),
            (8, 0, "1.A.4 - Autres secteurs"),
        ],
        "112": [
            (4, 0, "1.A.1 - Industries énergétiques"),
            (8, 0, "1.A.4 - Autres secteurs"),
        ],
    }
}

delete_row = {"main": {"110": [3, 7], "111": [3, 7], "112": [3, 7]}}

delete_rows_by_category = {
    "energy": {
        "116": [
            "1.A.3.a.i - Aviation internationale (Soutes internationales)",
            "Éléments pour information",
            "1.A.3.d.i - Navigation internationale (soutes internationales)",
            "1.A.5.c - Opérations multilatérales (Éléments pour information)",
        ],
        "117": [
            "1.A.3.a.i - Aviation internationale (Soutes internationales)",
            "Éléments pour information",
            "1.A.3.d.i - Navigation internationale (soutes internationales)",
            "1.A.5.c - Opérations multilatérales (Éléments pour information)",
        ],
        "118": [
            "1.A.3.a.i - Aviation internationale (Soutes internationales)",
            "Éléments pour information",
            "1.A.3.d.i - Navigation internationale (soutes internationales)",
            "1.A.5.c - Opérations multilatérales (Éléments pour information)",
        ],
        "119": [
            "1.A.3.a.i - Aviation internationale (Soutes internationales)",
            "Information Items",
            "1.A.3.d.i - Navigation internationale (soutes internationales)",
            "1.A.5.c - Opérations multilatérales (Éléments pour information)",
        ],
    },
    "trend": {
        # The categories 3.D / 3.D.1 / 3.D.2 contain values different to the main table
        # They should also not contain negative values according to IPCC methodology:
        # https://www.ipcc-nggip.iges.or.jp/public/2006gl/
        # Therefore, the rows are deleted from the table.
        "131": [
            "3.D - Autres",
            "3.D.1 - Produits ligneux récoltés",
            "3.D.2 - Autres (veuillez spécifier)",
        ],
        # Delete empty line for pages 132-137.
        "132": [""],
        "133": [""],
        "134": [""],
        "135": [""],
        "136": [""],
        "137": [""],
    },
}

# define config dict
inv_conf = {
    "header": header_inventory,
    "unit": unit_inventory,
    "header_energy": header_energy,
    "unit_energy": unit_energy,
    "header_afolu": header_afolu,
    "unit_afolu": unit_afolu,
    "header_waste": header_waste,
    "unit_waste": unit_waste,
    "header_trend": header_trend,
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    "pages_to_read": {
        "main": ["110", "111", "112", "113"],
        "energy": ["116", "117", "118", "119"],
        "afolu": ["124", "125", "126", "127"],
        "waste": ["128", "130"],
        # The table for CO (page 135) seems completely mixed up and should not be considered.
        # The total CO values for 1990 equal the values in the main table.
        # The total CO values for 1995 equal the values for 2000 in the main table.
        # The total CO values for 2000 equal the values for 2010 in the main table.
        # The total CO values for 2005 are identical to the 2019 values in the same table.
        # The total CO values for 2010 are identical to the 1990 values in the same table.
        # The total CO values for 2019 are identical to the 1995 values in the same table.
        # And so on.
        "trend": ["131", "132", "133", "134", "136", "137"],
    },
    "entity_for_page": {"trend": ["CO2", "CH4", "N2O", "NOx", "NMVOCs", "SO2"]},
    "year": {
        "110": 1990,
        "111": 2000,
        "112": 2010,
        "113": 2019,
        "116": 1990,
        "117": 2000,
        "118": 2010,
        "119": 2019,
        "124": 1990,
        "125": 2000,
        "126": 2010,
        "127": 2019,
    },
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "cat_codes_manual": {
        "main": {
            "Éléments pour mémoire": "MEMO",
            "Soutes internationales": "M.BK",
            "1.A.3.a.i - Aviation internationale (soutes internationales)": "M.BK.A",
            "1.A.3.d.i - Navigation internationale (soutes internationales)": "M.BK.M",
            "1.A.5.c - Opérations multilatérales": "M.MULTIOP",
            "Total des émissions et absorptions nationales": "0",
            "2A5: Autre": "2A5",
        },
        "energy": {
            "International Bunkers": "M.BK",
            "1.A.3.a.i - Aviation internationale (soutes internationales)": "M.BK.A",
            "1.A.3.d.i - Navigation internationale (soutes internationales)": "M.BK.M",
            "1.A.5.c - Opérations multilatérales": "M.MULTIOP",
            "CO2 from Biomass Combustion for Energy Production": "M.BIO",
        },
        "trend": {
            "Total des émissions et absorptions nationales": "0",
            "2A5: Autre": "2A5",
            "Éléments pour mémoire": "MEMO",
            "Soutes internationales": "M.BK",
            "1.A.3.a.i - Aviation internationale (soutes internationales)": "M.BK.A",
            "1.A.3.d.i - Navigation internationale (soutes internationales)": "M.BK.M",
            "1.A.5.c - Opérations multilatérales": "M.MULTIOP",
        },
    },
}

country_processing_step1 = {
    "aggregate_cats": {
        "M.3.C.AG": {
            "sources": [
                "3.C.1",
                "3.C.2",
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.6",
                "3.C.7",
                "3.C.8",
            ],
            "name": "Aggregate sources and non-CO2 emissions sources on land "
            "(Agriculture)",
        },
        "M.3.D.AG": {"sources": ["3.D.2"], "name": "Other (Agriculture)"},
        "M.AG.ELV": {
            "sources": ["M.3.C.AG", "M.3.D.AG"],
            "name": "Agriculture excluding livestock",
        },
        "M.AG": {"sources": ["3.A", "M.AG.ELV"], "name": "Agriculture"},
        "M.3.D.LU": {"sources": ["3.D.1"], "name": "Other (LULUCF)"},
        "M.LULUCF": {"sources": ["3.B", "M.3.D.LU"], "name": "LULUCF"},
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
            "name": "National total emissions excluding LULUCF",
        },
    },
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS"],
        "source_GWP": gwp_to_use,
    },
}

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

replace_info = {
    "main": [
        ("3", "CO", "2019", 27.406),
        ("3.C", "CO", "2019", 27.406),
        ("3.C.1", "CO", "2019", 27.406),
        ("3", "N2O", "1990", 2.190),
        ("3", "NOx", "2019", 1.644),
        ("3.C", "NOx", "2019", 1.644),
        ("3.C.1", "NOx", "2019", 1.644),
        ("M.BK", "NOx", "1990", 0.001),
        ("M.BK", "NOx", "2000", 0.003),
        ("M.BK", "NOx", "2010", 0.052),
        ("M.BK", "CO", "1990", 0.0002),
        ("M.BK", "CO", "2000", 0.0006),
        ("M.BK", "CO", "2010", 0.01),
        ("M.BK", "NMVOC", "1990", 0.0001),
        ("M.BK", "NMVOC", "2000", 0.0002),
        ("M.BK", "NMVOC", "2010", 0.003),
    ],
    "trend": [
        ("M.BK", "CH4", "1990"),
        ("M.BK.A", "CH4", "1990"),
        ("M.BK", "CH4", "2000"),
        ("M.BK.A", "CH4", "2000"),
        ("M.BK", "CH4", "2010"),
        ("M.BK.A", "CH4", "2010"),
        ("1.A.2", "N2O", "1990"),
        ("M.BK", "N2O", "1990"),
        ("M.BK.A", "N2O", "1990"),
        ("M.BK", "N2O", "2000"),
        ("M.BK.A", "N2O", "2000"),
        ("M.BK", "N2O", "2010"),
        ("M.BK.A", "N2O", "2010"),
        ("M.BK", "N2O", "2019"),
        ("M.BK.A", "N2O", "2019"),
        ("M.BK", "NOx", "1990"),
        ("M.BK", "NOx", "2000"),
        ("M.BK", "NOx", "2010"),
        ("3.C", "NOx", "2019"),
        ("3.C.1", "NOx", "2019"),
        ("3", "NOx", "2019"),
        ("1.A.2", "NMVOC", "1990"),
        ("M.BK", "NMVOC", "1990"),
        ("0", "NMVOC", "2000"),
        ("1", "NMVOC", "2000"),
        ("1.A", "NMVOC", "2000"),
        ("1.A.1", "NMVOC", "2000"),
        ("1.A.2", "NMVOC", "2000"),
        ("1.A.3", "NMVOC", "2000"),
        ("1.A.4", "NMVOC", "2000"),
        ("2", "NMVOC", "2000"),
        ("2.H", "NMVOC", "2000"),
        ("2.H.2", "NMVOC", "2000"),
        ("M.BK", "NMVOC", "2000"),
        ("0", "NMVOC", "2010"),
        ("1", "NMVOC", "2010"),
        ("1.A", "NMVOC", "2010"),
        ("1.A.1", "NMVOC", "2010"),
        ("1.A.2", "NMVOC", "2010"),
        ("1.A.3", "NMVOC", "2010"),
        ("1.A.4", "NMVOC", "2010"),
        ("2", "NMVOC", "2010"),
        ("M.BK", "NMVOC", "2010"),
        ("1.A.2", "NMVOC", "2019"),
    ],
}

replace_categories = {
    "afolu": {
        "124-126": [
            (17, "3.A.2.a.i - Vaches laitières"),
            (18, "3.A.2.a.ii - Autres bovins"),
            (19, "3.A.2.b - Buffle"),
            (20, "3.A.2.c - Ovins"),
            (21, "3.A.2.d - Caprins"),
            (22, "3.A.2.e - Chameaux"),
            (23, "3.A.2.f - Chevaux"),
            (24, "3.A.2.g - Mules et ânes"),
            (25, "3.A.2.h - Porcins"),
            (26, "3.A.2.i - Volailles"),
        ],
        "127": [
            (19, "3.A.2.a.i - Vaches laitières"),
            (20, "3.A.2.a.ii - Autres bovins"),
            (21, "3.A.2.b - Buffle"),
            (22, "3.A.2.c - Ovins"),
            (23, "3.A.2.d - Caprins"),
            (24, "3.A.2.e - Chameaux"),
            (25, "3.A.2.f - Chevaux"),
            (26, "3.A.2.g - Mules et ânes"),
            (27, "3.A.2.h - Porcins"),
            (28, "3.A.2.i - Volailles"),
            (29, "3.A.2.j - Autres (préciser)"),
        ],
    }
}
