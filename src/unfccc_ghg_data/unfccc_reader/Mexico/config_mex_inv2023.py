"""Config for Mexico's 2023 inventory

Full configuration including PRIMAP2 conversion config and metadata

"""


gwp_to_use = "AR5GWP100"


# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

# manual category codes
cat_codes_manual = {
    "EMISIONES NETAS (Gg de CO2e)": "0",
    "1A1ci Fabricación de combustibles sólidos (coque de carbón)": "1A1ci",
    "1A1cii Otras Industrias de la energía": "1A1cii",
    "1A2ci Petroquímica": "1A2ci",
    "1A2cii Industria química": "1A2cii",
    "1A2ciii Fertilizantes": "1A2ciii",
    "1A2ei Elaboración de azúcares": "1A2ei",
    "1A2eii Elaboración de bebidas": "1A2eii",
    "1A2eiii Elaboración de productos de tabaco": "1A2eiii",
    "1A2eiiii Elaboración de cerveza": "1A2eiv",
    "1A2eiiiii Elaboración de alimentos": "1A2ev",
    "1A2mi Fabricación de vidrio y productos de vidrio": "1A2mi",
    "1A2mii Fabricación de productos de hule": "1A2mii",
    "1A2miii Otras ramas": "1A2miii",
    "1B2ai Venteo petróleo": "1B2ai",
    "1B2aii Quemado petróleo": "1B2aii",
    "1B2aiii Otras fugitivas petróleo": "1B2aiii",
    "1B2bi Venteo gas natural": "1B2bi",
    "1B2bii Quemado gas natural": "1B2bii",
    "1B2biii Otras fugitivas gas natural": "1B2biii",
    "Bunkers": "MBK",
    "Aviación internacional": "MBKA",
    "Marítimo internacional": "MBKM",
    "Emisiones de CO2 por quema de biomasa": "MBIO",
    "[3A1i] Otros (especificar)": "3A1j",
    "[3A2g] Otros (especificar)": "3A2j",
    # "Nota:": "\\IGNORE",
}

cat_code_regexp = r"^\[(?P<code>[a-zA-Z0-9]{1,6})\].*"

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
    "scenario": "INV2024",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "CO2": "CO2",
        "CH4": f"CH4 ({gwp_to_use})",
        "N2O": f"N2O ({gwp_to_use})",
        "HFC-23": f"HFC23 ({gwp_to_use})",
        "HFC-410A": f"HFC410a ({gwp_to_use})",
        "HFC-43-10mee": f"HFC4310mee ({gwp_to_use})",
        "HFC-125": f"HFC125 ({gwp_to_use})",
        "HFC-134": f"HFC134 ({gwp_to_use})",
        "HFC-134a": f"HFC134a ({gwp_to_use})",
        "HFC-404A": f"HFC404a ({gwp_to_use})",
        "HFC-407C": f"HFC407c ({gwp_to_use})",
        "HFC-245fa": f"HFC245fa ({gwp_to_use})",
        "HFC-152a": f"HFC152a ({gwp_to_use})",
        "HFC-227ea": f"HFC227ea ({gwp_to_use})",
        "HFC-236fa": f"HFC236fa ({gwp_to_use})",
        # "HFC-365mfc/227ea": f"HFC365mfc ({gwp_to_use})",
        # TODO: include in openscm units as mixture
        "HFC-365mfc": f"HFC365mfc ({gwp_to_use})",
        "HFC-507a": f"HFC507a ({gwp_to_use})",
        "HFC-32": f"HFC32 ({gwp_to_use})",
        "CF4": f"CF4 ({gwp_to_use})",
        "C2F6": f"C2F6 ({gwp_to_use})",
        "C3F8": f"C3F8 ({gwp_to_use})",
        "C4F6": f"C4F6 ({gwp_to_use})",  # not in openscm_units
        "c-C4F8": f"cC4F8 ({gwp_to_use})",
        "C5F8": f"C5F8 ({gwp_to_use})",  # not in openscm_units
        "NF3": f"NF3 ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "EMISIONES NETAS Gg en CO2e": f"KYOTOGHG ({gwp_to_use})",
        # EMISIONES (sin 3B y 3D) Gg en CO2e: ignore
        "Carbono negro (Gg)": "BC",
    },
}

filter_remove = {
    "fcat": {"category": ["Nota:", ""]},
    "fent": {"entity": ["EMISIONES (sin 3B y 3D) Gg en CO2e", "HFC-365mfc/227ea", ""]},
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/645206",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Mexico. Biennial transparency report (BTR). BTR1",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

processing_info_country = {
    # "tolerance": 0.171,  # for 2.E.1, 2.E.2
    "aggregate_coords": {
        "category": {
            "M.3.C.1.AG": {
                "sources": ["3.C.1.b", "3.C.1.c"],
                "orig_cat_name": "Aggregate Sources and Non-CO2 Emissions Sources on Land "
                "- Agriculture",
            },
            "M.3.C.1.LU": {
                "sources": ["3.C.1.a", "3.C.1.d"],
                "orig_cat_name": "Aggregate Sources and Non-CO2 Emissions Sources on Land "
                "- LULUCF",
            },
            "M.3.C.AG": {
                "sources": [
                    "M.3.C.1.AG",
                    "3.C.2",
                    "3.C.3",
                    "3.C.4",
                    "3.C.5",
                    "3.C.6",
                    "3.C.7",
                ],
                "orig_cat_name": "Aggregate Sources and Non-CO2 Emissions Sources on Land "
                "- Agriculture",
            },
            "M.3.C.LU": {
                "sources": ["M.3.C.1.LU"],
                "orig_cat_name": "Aggregate Sources and Non-CO2 Emissions Sources on Land "
                "- LULUCF",
            },
            "M.AG.ELV": {
                "sources": ["M.3.C.AG"],
                "orig_cat_name": "Agriculture excluding livestock",
            },
            "M.AG": {
                "sources": ["3.A", "M.AG.ELV"],
                "orig_cat_name": "Agriculture",
            },
            "M.LULUCF": {
                "sources": ["M.3.C.LU", "3.B", "3.D"],
                "orig_cat_name": "Land Use, Land Use Change, and Forestry",
            },
            "M.0.EL": {
                "sources": ["1", "2", "M.AG", "4"],
                "orig_cat_name": "Agriculture",
            },
            # for consistency checks
            "3": {
                "sources": ["M.AG", "M.LULUCF"],
                "orig_cat_name": "[3] Agricultura, silvicultura y otros usos de la tierra",
            },
            "0": {
                "sources": ["M.LULUCF", "M.0.EL"],
                "orig_cat_name": "Todas las emisiones y las absorciones nacionales",
            },
        }
    },
}
