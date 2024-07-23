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

inv_conf_main = {
    "pages": {
        "86": {"skip_rows_start": 2},
        "87": {"skip_rows_start": 2},
        "88": {"skip_rows_start": 2},
        "89": {"skip_rows_start": 2},
    },
}
