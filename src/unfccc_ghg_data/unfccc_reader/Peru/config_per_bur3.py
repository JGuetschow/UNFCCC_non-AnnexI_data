"""Config for Peru's BUR3

Full configuration including PRIMAP2 conversion config and metadata

"""

table_def_templates = {
    "300": {  # 300
        "area": ["69,457,727,78"],
        "cols": ["288,352,391,426,458,485,519,552,587,615,643"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la fabricación",
                "Productos no energéticos de combustibles y de uso",
                "Uso de productos sustitutos de las sustancias que",
            ],
            2: [
                "1A Actividades de quema de combustible",
                "2A Industria de los minerales",
                "2B Industria química",
                "2C Industria de los metales",
                "2E Industria electrónica",
                "3A Ganado",
                "3A1 Fermentación entérica",
            ],
        },
    },
    "301": {  # 301
        "area": ["72,542,727,99"],
        "cols": ["288,352,391,426,458,485,519,552,587,615,643"],
        "rows_to_fix": {
            3: [
                "Fuentes agregadas y fuentes de emisión no CO2 de",
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo del",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
            2: [
                "3A2 Manejo del estiércol",
                "3C1 Emisiones por quema de biomasa",
                "3C3 Aplicación de urea",
                "3C7 Cultivo de arroz",
                "A Disposición de residuos sólidos",
                "B Tratamiento biológico de residuos",
                "C Incineración de residuos",
                "D Tratamiento y descarga de aguas residuales",
                "Búnker internacional",
            ],
        },
    },
    "302": {  # 302
        "area": ["72,510,727,79"],
        "cols": ["278,335,376,415,453,482,512,548,585,623,656"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la fabricación",
                "Productos no energéticos de combustibles y de",
                "Uso de productos sustitutos de las sustancias que",
                "Fuentes agregadas y fuentes de emision no CO2",
            ],
            -3: ["Total de las emisiones y remociones nacionales"],
        },
    },
    "303": {  # 303
        "area": ["72,540,727,127"],
        "cols": ["278,335,376,415,453,482,512,548,585,623,656"],
        "rows_to_fix": {
            3: [
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
            2: ["Aviación internacional"],
        },
    },
    "304": {  # 304
        "area": ["72,510,727,70"],
        "cols": ["275,332,365,408,441,470,499,533,577,620,654"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la",
                "Productos no energéticos de combustibles y de",
                "Uso de productos sustitutos de las sustancias",
                "Fuentes agregadas y fuentes de emisión no CO2",
            ],
        },
    },
    "305": {  # 305
        "area": ["72,540,727,108"],
        "cols": ["275,332,365,408,441,470,499,533,577,620,654"],
        "rows_to_fix": {
            3: [
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
        },
    },
    "306": {  # 306
        "area": ["72,510,727,70"],
        "cols": ["266,320,364,405,440,468,499,536,576,620,656"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la",
                "Productos no energéticos de combustibles y",
                "Uso de productos sustitutos de las sustancias",
                "Fuentes agregadas y fuentes de emisión no",
            ],
        },
    },
    "307": {  # 307
        "area": ["72,540,727,108"],
        "cols": ["266,320,364,405,440,468,499,536,576,620,656"],
        "rows_to_fix": {
            3: [
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA",
            ],
        },
    },
    "308": {  # 308
        "area": ["72,510,727,70"],
        "cols": ["278,329,372,406,441,470,500,536,579,621,653"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la fabricación",
                "Productos no energéticos de combustibles y de",
                "Uso de productos sustitutos de las sustancias que",
                "Fuentes agregadas y fuentes de emisión no CO2",
            ],
        },
    },
    "309": {  # 309
        "area": ["72,540,727,117"],
        "cols": ["278,329,372,406,441,470,500,536,579,621,653"],
        "rows_to_fix": {
            3: [
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo del",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
        },
    },
    "310": {  # 310
        "area": ["72,510,727,70"],
        "cols": ["279,334,379,418,453,480,505,541,582,620,654"],
        "rows_to_fix": {
            3: [
                "Industrias manufactureras y de la",
                "Emisiones fugitivas provenientes de la fabricación",
                "Productos no energéticos de combustibles y de",
                "Uso de productos sustitutos de las sustancias que",
                "Fuentes agregadas y fuentes de emisión no CO2",
            ],
        },
    },
    "311": {  # 311
        "area": ["72,540,727,110"],
        "cols": ["279,334,379,418,453,480,505,541,582,620,654"],
        "rows_to_fix": {
            3: [
                "Emisiones directas de N2O en suelos",
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
            -2: ["Emisiones de CO2 de la biomasa"],
        },
    },
    "312": {  # 312
        "area": ["72,510,727,70"],
        "cols": ["297,349,393,426,461,489,514,547,592,629,657"],
        "rows_to_fix": {
            3: [
                "Emisiones fugitivas provenientes de la fabricación de",
                "Productos no energéticos de combustibles y de uso de",
                "Uso de productos sustitutos de las sustancias que",
                "Fuentes agregadas y fuentes de emisión no CO2 de la",
            ],
        },
    },
    "313": {  # 313
        "area": ["72,540,727,90"],
        "cols": ["297,349,393,426,461,489,514,547,592,629,657"],
        "rows_to_fix": {
            3: [
                "Emisiones indirectas de N2O en suelos",
                "Emisiones indirectas de N2O por manejo del",
                "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y",
            ],
        },
    },
}

header = {
    "entity": [
        "Categorías de emisiones y sumideros de GEI",
        "Emisiones/remociones netas de CO2",
        "CH4",
        "N2O",
        "HFC",
        "PFC",
        "SF6",
        "CO",
        "NOx",
        "COVDM",
        "SOX",
        "Emisiones/remociones totales de GEI",
    ],
    "unit": [
        "",
        "Gg",
        "Gg",
        "Gg",
        "GgCO2eq",
        "GgCO2eq",
        "Gg",
        "Gg",
        "Gg",
        "Gg",
        "Gg",
        "GgCO2eq",
    ],
}

table_defs = {
    "300": {
        "templates": ["300"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2000,
        "coords_value_mapping": "default",
    },
    "301": {
        "templates": ["301"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2000,
        "coords_value_mapping": "default",
    },
    "302": {
        "templates": ["302"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2005,
        "coords_value_mapping": "default",
    },
    "303": {
        "templates": ["303"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2005,
        "coords_value_mapping": "default",
    },
    "304": {
        "templates": ["304"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2010,
        "coords_value_mapping": "default",
    },
    "305": {
        "templates": ["305"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2010,
        "coords_value_mapping": "default",
    },
    "306": {
        "templates": ["306"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2012,
        "coords_value_mapping": "default",
    },
    "307": {
        "templates": ["307"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2012,
        "coords_value_mapping": "default",
    },
    "308": {
        "templates": ["308"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2014,
        "coords_value_mapping": "default",
    },
    "309": {
        "templates": ["309"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2014,
        "coords_value_mapping": "default",
    },
    "310": {
        "templates": ["310"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2016,
        "coords_value_mapping": "default",
    },
    "311": {
        "templates": ["311"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2016,
        "coords_value_mapping": "default",
    },
    "312": {
        "templates": ["312"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2019,
        "coords_value_mapping": "default",
    },
    "313": {
        "templates": ["313"],
        "header": header,
        "drop_rows": [0, 1, 2, 3, 4],
        "category_col": "Categorías de emisiones y sumideros de GEI",
        "year": 2019,
        "coords_value_mapping": "default",
    },
}

cat_names_fix = {
    "Industrias manufactureras y de la 1A2 construcción": "1A2 Industrias manufactureras y de la construcción",  # noqa: E501
    "Emisiones fugitivas provenientes de la fabricación 1B de combustibles": "1B Emisiones fugitivas provenientes de la fabricación de combustibles", # noqa: E501
    "Emisiones fugitivas provenientes de la 1B fabricación de combustibles": "1B Emisiones fugitivas provenientes de la fabricación de combustibles", # noqa: E501
    "Emisiones fugitivas provenientes de la fabricación de 1B combustibles": "1B Emisiones fugitivas provenientes de la fabricación de combustibles", # noqa: E501
    "Productos no energéticos de combustibles y de uso 2D de solventes": "2D Productos no energéticos de combustibles y de uso de solventes", # noqa: E501
    "Productos no energéticos de combustibles y de 2D uso de solventes": "2D Productos no energéticos de combustibles y de uso de solventes", # noqa: E501
    "Uso de productos sustitutos de las sustancias que 2F agotan la capa de ozono": "2F Uso de productos sustitutos de las sustancias que agotan la capa de ozono", # noqa: E501
    "Uso de productos sustitutos de las sustancias 2F que agotan la capa de ozono": "2F Uso de productos sustitutos de las sustancias que agotan la capa de ozono", # noqa: E501
    "Fuentes agregadas y fuentes de emisión no CO2 de 3C la tierra": "3C Fuentes agregadas y fuentes de emisión no CO2 de la tierra", # noqa: E501
    "Fuentes agregadas y fuentes de emision no CO2 3C de la tierra": "3C Fuentes agregadas y fuentes de emision no CO2 de la tierra", # noqa: E501
    "Fuentes agregadas y fuentes de emisión no CO2 3C de la tierra": "3C Fuentes agregadas y fuentes de emisión no CO2 de la tierra", # noqa: E501
    "Fuentes agregadas y fuentes de emisión no 3C CO2 de la tierra": "3C Fuentes agregadas y fuentes de emisión no CO2 de la tierra", # noqa: E501
    "Fuentes agregadas y fuentes de emisión no CO2 de la 3C tierra": "3C Fuentes agregadas y fuentes de emisión no CO2 de la tierra", # noqa: E501
    "Emisiones directas de N2O en suelos 3C4 gestionados": "3C4 Emisiones directas de N2O en suelos gestionados", # noqa: E501
    "Emisiones indirectas de N2O en suelos 3C5 gestionados": "3C5 Emisiones indirectas de N2O en suelos gestionados", # noqa: E501
    "Emisiones indirectas de N2O por manejo del 3C6 estiércol": "3C6 Emisiones indirectas de N2O por manejo del estiércol", # noqa: E501
    "Emisiones indirectas de N2O por manejo 3C6 del estiércol": "3C6 Emisiones indirectas de N2O por manejo del estiércol", # noqa: E501
    "Emisiones indirectas de N2O por 3C6 manejo del estiércol": "3C6 Emisiones indirectas de N2O por manejo del estiércol", # noqa: E501
    "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y 4 SILVICULTURA": "4 USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y SILVICULTURA", # noqa: E501
    "USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA 4 Y SILVICULTURA": "4 USO DE LA TIERRA, CAMBIO DE USO DE LA TIERRA Y SILVICULTURA", # noqa: E501
}

values_replacement = {
    #    '': '-',
    " ": "",
}

gwp_to_use = "AR5GWP100"

index_cols = ["orig_cat_name"]
cols_for_space_stripping = index_cols

unit_row = "header"

## parameters part 2: conversion to PRIMAP2 interchnage format

cats_remove = ["Partidas informativas"]

cat_codes_manual = {
    "Emisiones de CO2 de la biomasa": "M.BIO",
    "Total de las emisiones y remociones nacionales": "0",
    "Búnker internacional": "M.BK",
    "Aviación internacional": "M.BK.A",
    "Transporte marítimo y fluvial internacional": "M.BK.M",
    "A Disposición de residuos sólidos": "5.A",
    "B Tratamiento biológico de residuos": "5.B",
    "C Incineración de residuos": "5.C",
    "D Tratamiento y descarga de aguas residuales": "5.D",
    "Tierras": "M.2006.3.B",
}


cat_code_regexp = r"(?P<code>^[A-Za-z0-9]{1,7})\s.*"

# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC1996_2006_PER_INV",
    "scenario": "PRIMAP",
}

coords_terminologies_2006 = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "PER-GHG-inventory ",
    "provenance": "measured",
    "area": "PER",
    "scenario": "BUR3",
}

coords_value_mapping = {
    "default": {
        "unit": "PRIMAP1",
        "entity": {
            "Emisiones/remociones netas de CO2": "CO2",
            "CH4": "CH4",
            "N2O": "N2O",
            "HFC": f"HFCS ({gwp_to_use})",
            "PFC": f"PFCS ({gwp_to_use})",
            "SF6": "SF6",
            "CO": "CO",
            "NOx": "NOX",
            "COVDM": "NMVOC",
            "SOx": "SOX",
            "Emisiones/remociones totales de GEI": f"KYOTOGHG ({gwp_to_use})",
        },
    },
}

coords_cols = {"category": "category", "entity": "entity", "unit": "unit"}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

filter_remove = {
    # "f1" :{
    #     "entity": ["HFC-125", "HFC-134a", "HFC-143a", "HFC-152a", "HFC-227ea",
    #                "HFC-23", "HFC-32", "HFC-41", "HFC-43-10mee", "PFC-116",
    #                "PFC-14", "PFC-218", "PFC-318", "NF3", "SF6"],
    #     "category": "2"
    # }
}

meta_data = {
    "references": "https://unfccc.int/documents/",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "",
    "comment": "Read fom pdf file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}


## processing
cat_conversion = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.A.5": "1.A.5",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "2": "2",
        "2.A": "2.A",
        "2.B": "2.B",
        "2.C": "2.C",
        "2.D": "2.D",
        "2.E": "2.E",
        "2.F": "2.F",
        "2.G": "2.G",
        "2.H": "2.H",
        "3": "M.AG",
        "3.A": "3.A",
        "3.A.1": "3.A.1",
        "3.A.2": "3.A.2",
        "3.C": "3.C",
        "3.C.1": "3.C.1",
        "3.C.2": "3.C.2",
        "3.C.3": "3.C.3",
        "3.C.4": "3.C.4",
        "3.C.5": "3.C.5",
        "3.C.6": "3.C.6",
        "3.C.7": "3.C.7",
        "4": "M.LULUCF",
        "M.2006.3.B": "3.B",
        "4.A": "3.B.1",
        "4.B": "3.B.2",
        "4.C": "3.B.3",
        "4.D": "3.B.4",
        "4.E": "3.B.5",
        "4.F": "3.B.6",
        "4.G": "3.D.1",
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.B",
        "5.C": "4.C",
        "5.D": "4.D",
        "M.BK": "M.BK",
        "M.BK.A": "M.BK.A",
        "M.BK.M": "M.BM.M",
        "M.BIO": "M.BIO",
    },
    "aggregate": {
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.E", "2.F", "2.G", "2.H"],
            "name": "IPPU",
        },
        "M.3.C.AG": {
            "sources": ["3.C"],
            "name": "Aggregate sources and non-CO2 emissions sources on land (Agriculture)",
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            "name": "Agriculture excluding livestock emissions",
        },
        "3.D": {"sources": ["3.D.1"], "name": "Other"},
        "3": {"sources": ["M.AG", "M.LULUCF"], "name": "AFOLU"},
    },
}

processing_info = {
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        "entities": ["HFCS", "PFCS"],
        "source_GWP": gwp_to_use,
    },
}
