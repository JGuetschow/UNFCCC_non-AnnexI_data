"""
Configuration for Cabo Verde BUR1 (read from pdf)
"""

# reading tables on pages:
# 33/1, GHG emissions and removals by type of gas, by sector and by year
# 39, Total GHG Emissions, in CO2eq, for international bunkers, in 1995, 2000, 2005, 2010, 2015 and 2019
# 86-89, GHG emissions in 2019
# Not reading tables on pages:
# 37/38, has additional columns on PFCs, Unspecified mixture of HFCs and PFCs,
# and SF6, but they are all empty
# 32, same information as in table 33/1
# 33/2, aggregation of table 33/1
# 43, no new information here

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "CPV-GHG-Inventory",
    "provenance": "measured",
    "area": "CPV",
    "scenario": "BUR1",
}

gwp_to_use = "SARGWP100"

coords_value_mapping_main = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "HFC": f"HFCS ({gwp_to_use})",
    },
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "CO²": "CO2",
        "CH⁴": "CH4",
        "N²O": "N2O",
        "F-gases": f"FGASES ({gwp_to_use})",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    # They are all NaN and don't match a pre-defined entity
    "f_fluor": {"entity": "Other fluorinated products"},
}

meta_data = {
    "references": "https://unfccc.int/sites/default/files/resource/BUR_EN_Digital.pdf",  # TODO check other sources
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Cabo Verde. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

trend_years = ["1995", "2000", "2005", "2010", "2015", "2019"]

inv_conf_per_sector = {
    "main": {
        "page": "33",
        "skip_rows_start": 2,
        "cat_codes_manual": {
            "Energy": "1",
            "IPPU": "2",
            "Agriculture": "M.AG",
            "LULUCF": "M.LULUCF",
            "Waste": "4",
        },
        "header": ["category", "entity", *trend_years],
        "unit": ["Gg"] * 4 + ["Gg CO2eq"] + ["Gg"] * 9,
    },
    "int_bunkers": {
        "page": "39",
        "skip_rows_start": 2,
        "cat_codes_manual": {
            "Total International Bunkers": "M.BK",
            "International aviation": "M.BK.A",
            "International shipping": "M.BK.M",
        },
        "header": ["category", *trend_years],
        "unit": "Gg CO2eq",
        "drop_cols": 7,
        "entity": "KYOTOGHG (SARGWP100)",
    },
}

inv_conf = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "year": "2019",
    # TODO check again!
    # "CO2 emissions from Biomass" and "CO2 emissions from using manure as energy" are the same category
    "merge_cats": "MBIO",
}

inv_conf_main = {
    "pages": {
        "86": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "Memo items": "MEMO",
                "International bunkers": "M.BK",
                "CO² emissions from Biomass": "M.BIO",
                "CO² emissions from using manure as energy": "M.BIO",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
            # "units" : ["no unit", "Gg", "Gg", "Gg"]
        },
        "87": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O", "HFCs", "Other fluorinated products"],
            "column_names": [
                "category",
                "CO2",
                "CH4",
                "N2O",
                "HFCs",
                "Other fluorinated products",
            ],
            "cat_codes_manual": {
                "2F. Use of products as substitutes for \nsubstances that degrade the ozone layer": "2.F",
                "2B4. Production of caprolactam, \nglyoxal and glyoxylic acid": "2.B.4",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
                "HFCs": "Gg CO2eq",
            },
        },
        "88": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "3C6. Indirect emissions of N²O from manure \nmanagement": "3.C.6",
                "3C. Aggregate Sources and Sources of Non-CO²\nEmissions in the soil": "3.C",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
        },
        "89": {
            "skip_rows_start": 2,
            "entities": ["CO2", "CH4", "N2O"],
            "column_names": ["category", "CO2", "CH4", "N2O"],
            "cat_codes_manual": {
                "3C6. Indirect emissions of N²O from manure \nmanagement": "3.C.6",
                "3C. Aggregate Sources and Sources of Non-CO²\nEmissions in the soil": "3.C",
            },
            "unit_for_entity": {
                "CO2": "Gg",
                "CH4": "Gg",
                "N2O": "Gg",
            },
        },
    },
}
