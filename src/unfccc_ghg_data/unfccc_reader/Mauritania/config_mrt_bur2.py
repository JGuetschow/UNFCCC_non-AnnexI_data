"""Config for Mauritania BUR2

Configuration for reading the Mauritania's BUR2 from pdf.
Full configuration is contained here including configuraton for conversions to
primap2 data format.

Not nicely structured, just copied from old script as this was integrated under time
pressure to fix a GWP bug (wrong GWP stated in report)
"""

gwp_to_use = "AR4GWP100"
terminology_proc = "IPCC2006_PRIMAP"

table_defs = {
    1990: [[0], [1], [2], [21], [28, 29], [42]],
    1995: [[3], [4], [5], [22], [30, 31], [43]],
    2000: [[6], [7], [8], [23], [32, 33], [44]],
    2010: [[9], [10], [11], [24], [34, 35], [45]],
    2012: [[12], [13], [14], [25], [36, 37], [46]],
    2015: [[15], [16], [17], [26], [38, 39], [47]],
    2018: [[18], [19], [20], [27], [40, 41], [48]],
}

page_def_templates = {
    "24": {
        "area": ["51,745,579,87"],
        "cols": ["309,344,386,429,464,494,535"],
    },
    "odd": {  # 25, 27, 29, 31, 33, 35, 37
        "area": ["51,745,551,244", "55,231,554,118"],
        "cols": ["276,316,361,403,438,468,509", "276,319,361,407,441,472,511"],
    },
    "even": {  # 26, 28, 30, 32,34, 36
        "area": ["51,745,579,87"],
        "cols": ["304,344,386,429,464,494,535"],
    },
    "25": {  # 27, 29, 31, 33, 35, 37
        "area": ["51,745,551,244", "55,231,554,118"],
        "cols": ["276,316,361,403,438,468,509", "276,319,361,407,441,472,511"],
    },
    "26": {  # 28, 30, 32,34, 36
        "area": ["51,745,579,87"],
        "cols": ["309,344,386,429,464,494,535"],
    },
    "38": {
        "area": ["33,749,566,54"],
        "cols": ["220,243,263,283,308,336,359,415,471,493,517,546"],
    },
    "39": {
        "area": ["32,749,577,54"],
        "cols": ["224,254,275,294,320,345,367,426,482,503,525,553"],
    },
    "40": {
        "area": ["32,749,577,54"],
        "cols": ["224,245,265,287,314,338,360,420,476,496,518,546"],
    },
    "41": {  # 42
        "area": ["32,749,577,54"],
        "cols": ["220,245,265,287,314,338,360,420,476,496,518,546"],
    },
    "43": {
        "area": ["32,749,577,54"],
        "cols": ["220,245,268,287,314,338,360,420,476,496,518,546"],
    },
    "44": {
        "area": ["32,749,577,54"],
        "cols": ["220,245,268,283,314,338,360,420,476,496,518,546"],
    },
    "45": {
        "area": ["66,716,556,49"],
        "cols": ["287,362,399,441,479,515"],
    },
    "46": {
        "area": ["68,779,554,715", "68,677,554,52"],
        "cols": ["287,362,399,441,479,515", "308,387,423,453,480,510"],
    },
    "47": {
        "area": ["68,779,556,670", "67,640,555,48"],
        "cols": ["308,387,423,453,480,510", "308,387,423,453,480,510"],
    },
    "48": {
        "area": ["67,778,552,639", "67,610,553,49"],
        "cols": ["308,387,423,453,480,510", "308,387,423,453,480,510"],
    },
    "49": {
        "area": ["67,778,552,609", "67,579,553,49"],
        "cols": ["308,387,423,453,480,510", "308,387,423,453,480,510"],
    },
    "50": {
        "area": ["67,778,552,578", "67,550,553,49"],
        "cols": ["308,387,423,453,480,510", "308,387,423,453,480,510"],
    },
    "51": {
        "area": ["67,778,552,549"],
        "cols": ["308,387,423,453,480,510"],
    },
    "52": {
        "area": ["67,753,549,54"],
        "cols": ["308,387,423,453,480,510"],
    },
    "53": {
        "area": ["68,779,556,737"],
        "cols": ["308,387,423,453,480,510"],
    },
    "54": {
        "area": ["56,751,565,616", "56,587,565,449", "56,419,565,252", "56,217,565,74"],
        "cols": [
            "282,315,346,412,447,482,528",
            "282,315,346,412,447,482,528",
            "282,315,346,412,447,482,528",
            "282,315,346,412,447,482,528",
        ],
    },
    "55": {
        "area": ["56,752,565,600", "56,563,565,408", "56,369,565,216"],
        "cols": [
            "282,315,346,412,447,482,528",
            "282,315,346,412,447,482,528",
            "282,315,346,412,447,482,528",
        ],
    },
}

header_templates = {
    "24": {  # tables 0:20, 42: end
        "entity": ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "NMVOCs", "SO2"],
        "unit": ["", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg"],
        "rows": 2,
    },
    "38": {  # tables 21:27
        "entity": [
            "Catégories",
            "CO2",
            "CH4",
            "N2O",
            "HFCs",
            "PFCs",
            "SF6",
            "Autres gaz halogénés avec facteurs de conversion équivalent CO2",
            "Autres gaz halogénés sans facteurs de conversion équivalent CO2",
            "NOx",
            "CO",
            "NMVOCs",
            "SO2",
        ],
        "unit": [
            "",
            "Gg",
            "Gg",
            "Gg",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "GgCO2eq",
            "Gg",
            "Gg",
            "Gg",
            "Gg",
            "Gg",
        ],
        "rows": 7,
    },
    "45": {  # tables 28:41
        "entity": [
            "Catégories",
            "Émissions/ absorptions CO2",
            "CH4",
            "N2O",
            "NOx",
            "CO",
            "COVNM",
        ],
        "unit": ["", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg"],
        "rows": 4,
    },
    "54": {  # tables 42:
        "entity": ["Catégories", "CO2", "CH4", "N2O", "NOx", "CO", "NMVOCs", "SO2"],
        "unit": ["", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg", "Gg"],
        "rows": 3,
    },
}

fix_rows_template = {
    "24": {
        2: [
            "1.A.1.c   Transformation des combustibles solides et autres industries",
        ],
    },
    "25_1": {
        2: [
            "1.B.1.a.i.2  Emissions de gaz des couches lors des activités",
            "1.B.1.a.i.4 Combustion du méthane asséché ou",
            "1.B.1.a.ii.2  Emissions de gaz des couches lors des",
        ],
    },
    "25_2": {
        2: [
            "Émissions de CO2 imputables à la combustion de labiomasse pour",
        ],
    },
    "26": {
        2: [
            "1.A.1.c   Transformation des combustibles solides et autres industries",
            "1.A.2.i Industries extractives (à l’exclusion de l’extraction de",
        ],
    },
    "38": {
        2: [
            "2.D   Produits non énergétiques imputables aux",
            "2.F   Utilisations de produits comme substituts de",
        ],
    },
    "39": {
        2: [
            "2.D   Produits non énergétiques imputables aux combustibles",
            "2.F   Utilisations de produits comme substituts de substances",
        ],
    },
    "44": {
        -2: [
            "2  PROCÉDÉS INDUSTRIELS ET UTIL. DES PRODUITS",
        ],
        2: [
            "2.D   Produits non énergétiques imputables aux",
            "2.F   Utilisations de produits comme substituts de",
        ],
    },
}

table_reading_defs = {
    0: {
        "page": "24",
        "table": 0,
        "page_def": page_def_templates["24"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["24"],
    },
    1: {
        "page": "25",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    2: {
        "page": "25",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    3: {
        "page": "26",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    4: {
        "page": "27",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    5: {
        "page": "27",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    6: {
        "page": "28",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    7: {
        "page": "29",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    8: {
        "page": "29",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    9: {
        "page": "30",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    10: {
        "page": "31",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    11: {
        "page": "31",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    12: {
        "page": "32",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    13: {
        "page": "33",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    14: {
        "page": "33",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    15: {
        "page": "34",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    16: {
        "page": "35",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    17: {
        "page": "35",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    18: {
        "page": "36",
        "table": 0,
        "page_def": page_def_templates["even"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["26"],
    },
    19: {
        "page": "37",
        "table": 0,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_1"],
    },
    20: {
        "page": "37",
        "table": 1,
        "page_def": page_def_templates["odd"],
        "header": header_templates["24"],
        "fix_rows": fix_rows_template["25_2"],
    },
    21: {
        "page": "38",
        "table": 0,
        "page_def": page_def_templates["38"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["38"],
    },
    22: {
        "page": "39",
        "table": 0,
        "page_def": page_def_templates["39"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["39"],
    },
    23: {
        "page": "40",
        "table": 0,
        "page_def": page_def_templates["40"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["38"],
    },
    24: {
        "page": "41",
        "table": 0,
        "page_def": page_def_templates["41"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["38"],
    },
    25: {
        "page": "42",
        "table": 0,
        "page_def": page_def_templates["41"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["38"],
    },
    26: {
        "page": "43",
        "table": 0,
        "page_def": page_def_templates["43"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["38"],
    },
    27: {
        "page": "44",
        "table": 0,
        "page_def": page_def_templates["44"],
        "header": header_templates["38"],
        "fix_rows": fix_rows_template["44"],
    },
    28: {
        "page": "45",
        "table": 0,
        "page_def": page_def_templates["45"],
        "header": header_templates["45"],
    },
    29: {
        "page": "46",
        "table": 0,
        "page_def": page_def_templates["46"],
        "header": header_templates["45"],
    },
    30: {
        "page": "46",
        "table": 1,
        "page_def": page_def_templates["46"],
        "header": header_templates["45"],
    },
    31: {
        "page": "47",
        "table": 0,
        "page_def": page_def_templates["47"],
        "header": header_templates["45"],
    },
    32: {
        "page": "47",
        "table": 1,
        "page_def": page_def_templates["47"],
        "header": header_templates["45"],
    },
    33: {
        "page": "48",
        "table": 0,
        "page_def": page_def_templates["48"],
        "header": header_templates["45"],
    },
    34: {
        "page": "48",
        "table": 1,
        "page_def": page_def_templates["48"],
        "header": header_templates["45"],
    },
    35: {
        "page": "49",
        "table": 0,
        "page_def": page_def_templates["49"],
        "header": header_templates["45"],
    },
    36: {
        "page": "49",
        "table": 1,
        "page_def": page_def_templates["49"],
        "header": header_templates["45"],
    },
    37: {
        "page": "50",
        "table": 0,
        "page_def": page_def_templates["50"],
        "header": header_templates["45"],
    },
    38: {
        "page": "50",
        "table": 1,
        "page_def": page_def_templates["50"],
        "header": header_templates["45"],
    },
    39: {
        "page": "51",
        "table": 0,
        "page_def": page_def_templates["51"],
        "header": header_templates["45"],
    },
    40: {
        "page": "52",
        "table": 0,
        "page_def": page_def_templates["52"],
        "header": header_templates["45"],
    },
    41: {
        "page": "53",
        "table": 0,
        "page_def": page_def_templates["53"],
        "header": header_templates["45"],
    },
    42: {
        "page": "54",
        "table": 0,
        "page_def": page_def_templates["54"],
        "header": header_templates["54"],
    },
    43: {
        "page": "54",
        "table": 1,
        "page_def": page_def_templates["54"],
        "header": header_templates["54"],
    },
    44: {
        "page": "54",
        "table": 2,
        "page_def": page_def_templates["54"],
        "header": header_templates["54"],
    },
    45: {
        "page": "54",
        "table": 2,
        "page_def": page_def_templates["54"],
        "header": header_templates["54"],
    },
    46: {
        "page": "55",
        "table": 0,
        "page_def": page_def_templates["55"],
        "header": header_templates["54"],
    },
    47: {
        "page": "55",
        "table": 1,
        "page_def": page_def_templates["55"],
        "header": header_templates["54"],
    },
    48: {
        "page": "55",
        "table": 2,
        "page_def": page_def_templates["55"],
        "header": header_templates["54"],
    },
}


remove_per_table = [
    [
        "1.A.3.d.i di Navigation internationale (soutes internationales) (1)",
        "1.A.3.a.i ai Aviation internationale (soutes internationales) (1)",
        "1.A.5.c Opérations multilatérales (1) (2)",
    ],  # these could also be removed globally as names slightly different
    [],
    [],
    [],
    [],
    [],
]

fix_cat_values = {
    "Catégorie": "Catégories",
}

fix_cat_using_preceeding = {  # fix cat code based on cat code before
    "3.A.2.i Volaille": {"3.A.1.h Porcins": "3.A.1.i Volaille"},
}

# definitions for conversion to long format with standardized unit format
unit_row = 0
entity_row = 1
unit_entity_rows = [unit_row, entity_row]

index_cols = ["Catégories"]

# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

overlap_problems = {
    "1.A.2.i Industries extractives (à l’exclusion de l’extraction de combustibles) 113,528": [
        "1.A.2.i Industries extractives (à l’exclusion de l’extraction de combustibles)",
        "113,528",
    ],
}

## definitions part 2: conversion to PRIMAP2 interchnage format

# rows to remove
cats_remove = ["Information Items", "Memo Items (3)"]

# manual category codes
cat_codes_manual = {
    "Soutesinternationales": "M.BK",
    "Émissions de CO2 imputables à la combustion de labiomasse pour la production d’énergie": "M.BIO",
    "1.A.3.d.i Navigation internationale": "M.BK.M",
    "1.A.3.a.i Aviation internationale": "M.BK.A",
    "1.A.5.c - Opérations multilatérales": "M.MULTIOP",
}

cat_code_regexp = r"(?P<code>^[a-zA-Z0-9\.]{1,14})\s.*"

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "Mauritania-GHG-inventory",
    "provenance": "measured",
    "area": "MRT",
    "scenario": "BUR2",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "NMVOCs": "NMVOC",
        "COVNM": "NMVOC",
        "Net CO2": "CO2",
        "Émissions/ absorptions CO2": "CO2",
        "Émissions/ absorptions nettes de CO2": "CO2",
        "Autres gaz halogénés avec facteurs de conversion équivalent CO2": f"OTHERHFCS ({gwp_to_use})",
        #'Other halogenated gases without CO2 equivalent conversion factors (2)': 'OTHERHFCS',
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "HFC-23": "HFC23",
        "HFC-32": "HFC32",
        "HFC-41": "HFC41",
        "HFC-43-10mee": "HFC4310mee",
        "HFC-125": "HFC125",
        "HFC-134": "HFC134",
        "HFC-134a": "HFC134a",
        "HFC-152a": "HFC152a",
        "HFC-143": "HFC143",
        "HFC-143a": "HFC143a",
        "HFC-227ea": "HFC227ea",
        "HFC-236fa": "HFC236fa",
        "HFC-245ca": "HFC245ca",
        "c-C4F8": "cC4F8",
    },
}

coords_cols = {"category": "category", "entity": "entity", "unit": "unit"}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

filter_remove = {
    "f1": {
        "entity": ["Autres gaz halogénés sans facteurs de conversion équivalent CO2"],
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/279303",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "République Islamique de Mauritanie - RAPPORT NATIONAL DES INVENTAIRES DES GAZ A EFFET DE SERRE - RNI",
    "comment": "Read fom pdf file (Mauritania BUR 2 - NIR Annexes - May 2020.pdf) by Johannes Gütschow. ",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}

# part 3 fgases defintions
table_defs_fgases = {
    1990: [0],
    1995: [1, 2],
    2000: [3],
    2010: [4, 5],
    2012: [6],
    2015: [7, 8],
    2018: [9],
}
pages_fgases = ["92", "92", "93", "93", "93", "94", "94", "94", "95", "95"]

area_fgases = [
    "55,508,833,280",
    "55,263,833,50",
    "55,530,833,511",
    "55,491,833,264",
    "55,244,833,51",
    "55,532,833,493",
    "55,473,833,245",
    "55,224,833,53",
    "55,530,833,473",
    "55,430,833,200",
]
cols_fgases = [
    "259,300,320,345,373,391,422,444,465,486,508,534,561,585,613,642,671,693,721,748,776,805"
]

rows_to_fix_fgases = {
    2: ["2.F   Utilisations de produits comme substituts de substances"],
    -3: ["Catégories"],
}

# definitions for conversion to long format with standardized unit format
unit_row_fgases = 1
entity_row_fgases = 0
unit_entity_rows_fgases = [unit_row_fgases, entity_row_fgases]
unit_info_fgases = {
    "default_unit": "",
    "regexp_entity": r"^.*",
    "regexp_unit": None,  # temp fix until param is marked as optional in PRIMAP2
    "manual_repl_unit": {
        "Catégories": "",
        "Émissions en unité de masse d’origine (tonne)": "t",
    },
}


first_ignore_cat_fgases = "Émissions en unité équivalent CO2 (Gg Eq-CO2)"
cats_remove_fgases = [
    "Facteurs de conversion  équivalent CO2 [GWP du SAR sur 100 ans ]"
]

entities_to_remove_fgases = ["Total HFCs", "Total PFCs"]

## processing
proc_info_country = {
    "aggregate_coords": {
        "category": {
            "2.D": {
                "sources": ["2.D.1", "2.D.2", "2.D.3", "2.D.4"],
                # 'name': 'Non-Energy Products from Fuels and Solvent Use'
            },
            "2.G.1": {
                "sources": ["2.G.1.a"],
                # 'name': 'Electrical Equipment'
            },
            "2.G": {
                "sources": ["2.G.1", "2.G.2", "2.G.3", "2.G.4"],
                # 'name': 'Other Product Manufacture and Use'
            },
            "2.F": {
                "sources": ["2.F.1", "2.F.2", "2.F.3", "2.F.4", "2.F.5", "2.F.6"],
                # 'name': 'Product uses as Substitutes for Ozone Depleting Substances'
            },  # needed for fgases only
            "2.H": {
                "sources": ["2.H.1", "2.H.3"],
                # 'name': 'Other'
            },
            "2": {
                "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"],
                # 'name': 'IPPU'
            },  # needed for fgases only
            "M.3.C.1.AG": {
                "sources": ["3.C.1.c"],
                # 'name': 'Emissions from Biomass Burning (Agriculture)'
            },
            "M.3.C.AG": {
                "sources": ["M.3.C.1.AG", "3.C.3", "3.C.4"],
                # 'name': 'Aggregate sources and non-CO2 emissions sources on land (Agriculture)'
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG"],
                # 'name': 'Agriculture excluding livestock emissions'
            },
            "M.AG": {
                "sources": ["3.A", "M.AG.ELV"],
                # 'name': 'Agriculture'
            },
            "M.LULUCF": {
                "sources": ["3.B"],
                # 'name': 'Land Use, Land Use Change, and Forestry'
            },
            "3": {
                "sources": ["M.AG", "M.LULUCF"],
                # 'name': 'AFOLU'
            },
            "M.0.EL": {
                "sources": ["1", "2", "M.AG", "4"],
                # 'name': 'National Total Excluding LULUCF'
            },
            "0": {
                "sources": ["1", "2", "3", "4"],
                # 'name': 'National Total'
            },  # neede for fgases only
        },
    },
    "remove_ts": {
        "2A_NMVOC": {  # should be 0
            "category": ["2.A"],
            "entities": ["NMVOC"],
            "time": ["1990"],
        },
        "2D_NMVOC": {  # is 0 needs to be recomputed
            "category": ["2.D"],
            "entities": ["NMVOC"],
            "time": ["2012"],
        },
    },
}
