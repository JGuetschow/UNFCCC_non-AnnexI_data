"""Config for Mexico's BUR3

Full configuration including PRIMAP2 conversion config and metadata

"""

import re

page_defs = {
    "81": {  # main sectors
        "camelot": {
            "table_areas": ["78,354,530,86"],
            "columns": ["245,282,316,348,382,416,450,484"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Categorías de fuentes y sumideros de GEI"],
            3: ["[1A2] Industrias manufactura y de la"],
            5: ["Todas las emisiones (sin USCUSS): [3B] Tierra,"],
        },
    },
    "82": {  # main sectors
        "camelot": {
            "table_areas": ["61,690,511,83"],
            "columns": ["228,267,299,335,367,403,436,470"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Categorías de fuentes y sumideros de GEI"],
            3: [
                "[2B8] Producción petroquímica y negro",
                "[2D] Uso de productos no energéticos",
                "[2F] Uso de productos sustitutos de las",
                "[2G] Manufactura y utilización de otros",
            ],
        },
    },
    "83": {  # main sectors
        "camelot": {
            "table_areas": ["84,689,527,95"],
            "columns": ["245,283,316,348,381,416,450,484"],
            "split_text": False,
            "flavor": "stream",
        },
        "rows_to_fix": {
            -5: ["Categorías de fuentes y sumideros de GEI"],
            3: [
                "[3C] Fuentes agregadas y fuentes de emisión no",
                "[3C1] Emisiones de GEI por quemado de",
                "[3C4] Emisiones directas de los N₂O de suelos",
                "[3C5] Emisiones indirectas de los N₂O de suelos",
                "[3C6] Emisiones indirectas de los N₂O de la",
                "[4A1] Sitios gestionados de eliminación de",
                "[4A2] Sitios no controlados de eliminación de",
                "[4A3] Tiraderos a cielo abierto para eliminación",
                "[4B] Tratamiento biológico de los residuos",
                "[4C] Incineración y quema a cielo abierto de",
                "[4C1] Incineración de residuos peligrosos",
                "[4D] Tratamiento y eliminación de aguas",
                "[4D1] Tratamiento y eliminación de aguas",
                "[4D2] Tratamiento y eliminación de aguas",
            ],
        },
    },
}

gwp_to_use = "AR5GWP100"


# units = {
#     "CO₂": "Gg",
#     "CH₄": "GgCO2eq",
#     "N₂O": "GgCO2eq",
#     "HFC": "GgCO2eq",
#     "PFC": "GgCO2eq",
#     "NF₃": "GgCO2eq",
#     "SF₆": "GgCO2eq",
#     "Emisiones Netas PCG AR5": "GgCO2eq",
# }

# manual category codes
cat_codes_manual = {
    "Todas las emisiones y las absorciones nacionales": "0",
    re.compile(r"Todas las emisiones \(sin USCUSS\).*"): "M0EL",
}

cat_code_regexp = r"^\[(?P<code>[a-zA-Z0-9]{1,3})\].*"

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "MEX-GHG-Inventory",
    "provenance": "measured",
    "area": "MEX",
    "scenario": "BTR1",
}

coords_value_mapping = {
    # "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "CH₄": f"CH4 ({gwp_to_use})",
        "CO₂": "CO2",
        "Emisiones Netas PCG AR5": "KYOTOGHG (AR5GWP100)",
        "HFC": f"HFCS ({gwp_to_use})",
        "NF₃": f"NF3 ({gwp_to_use})",
        "N₂O": f"N2O ({gwp_to_use})",
        "PFC": f"PFCS ({gwp_to_use})",
        "SF₆": f"SF6 ({gwp_to_use})",
    },
}

filter_remove = {}

filter_keep = {}

meta_data = {
    "references": "",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Mexico. Biennial update report (BUR). BUR3",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}
