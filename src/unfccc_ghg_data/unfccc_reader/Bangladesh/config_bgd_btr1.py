"""
Configuration file to read Bangladesh's BTR 1.

Overview of all available GHG tables

As the data is spread over multiple tables we collect data from small tables manually
in a xlsx file which we then read using pandas. The origin of the data points is
specified in the xls files. Additionally, we read the key category analysis (Annex-IX)
which contains detailed information for 2019 and 2022
"""

## general configuration
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
    "source": "BGD-GHG-Inventory",
    "provenance": "measured",
    "area": "BGD",
    "scenario": "BTR1",
}

gwp_to_use = "AR5GWP100"

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_info": {"category": "INFO"},
}

meta_data = {
    "references": "https://unfccc.int/documents//655314",
    "rights": "",  # unknown
    "contact": "mail@johannes-guetschow.de",
    "title": " Bangladesh. 2024 Biennial Transparency Report (BTR). BTR1. ",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

## configuration for the individual tables


## configuration for the key category analysis
page_defs = {
    "430": {
        "table_areas": ["38,746,561,76"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "431": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "432": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "433": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "434": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "435": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "436": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "437": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "438": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "439": {
        "table_areas": ["36,777,563,62"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
    "440": {
        "table_areas": ["36,777,563,691"],
        "columns": ["81,186,251,313,374,436,499"],
        "split_text": False,
        "flavor": "stream",
    },
}

### TODO


country_processing_step1 = {
    "tolerance": 0.01,
    "aggregate_cats": {
        "3.A": {"sources": ["3.A.1", "3.A.2"]},
        "M.3.C.AG": {  # "Aggregate sources and non-CO2 emissions sources on land (Agriculture)"
            "sources": [
                "3.C.3",
                "3.C.4",
                "3.C.5",
                "3.C.7",
            ]
        },
        "3.C": {"sources": ["3.C.3", "3.C.4", "3.C.5", "3.C.7"]},
        "M.AG.ELV": {
            "sources": ["M.3.C.AG", "M.3.D.AG"],
        },
        "M.AG": {"sources": ["3.A", "M.AG.ELV"]},  # agriculture
        "M.LULUCF": {"sources": ["3.B", "M.3.D.LU"]},
        "M.0.EL": {
            "sources": ["1", "2", "M.AG", "4"],
        },
        "1.B": {"sources": ["1.B.2"]},
        "4.D": {"sources": ["4.D.1", "4.D.2"]},
        "1": {"sources": ["1.A", "1.B"]},  # consistency check energy
        "2": {"sources": ["2.A", "2.B", "2.C", "2.D", "2.F"]},  # consistency check IPPU
        "3": {"sources": ["M.AG", "M.LULUCF"]},  # consistency check AFOLU
        "4": {"sources": ["4.A", "4.D"]},  # consistency check waste
        # check if typed numbers add up to the total of 1.A.2 from the main table
        "1.A.2": {
            "sources": [
                "1.A.2.a",
                "1.A.2.b",
                "1.A.2.c",
                "1.A.2.d",
                "1.A.2.e",
                "1.A.2.f",
                "1.A.2.g",
                "1.A.2.h",
                "1.A.2.i",
                "1.A.2.j",
                "1.A.2.k",
                "1.A.2.l",
                "1.A.2.m",
            ]
        },
        # check if typed numbers add up to the total of 1.A.3 from the main table
        "1.A.3": {
            "sources": [
                "1.A.3.a.ii",
                "1.A.3.b.i.2",
                "1.A.3.b.ii.2",
                "1.A.3.b.iii",
                "1.A.3.b.iv",
                "1.A.3.c",
                "1.A.3.d.ii",
            ]
        },
        # check if the typed numbers add up to the total of 1.A.4.c in the same table
        "1.A.4.c": {"sources": ["1.A.4.c.i", "1.A.4.c.iii"]},
        # check if typed numbers add up to the total of 1.A.4 from the main table
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"]},
        # check if the typed numbers add up to the total of 1.A.4.c in the same table
        "1.B.2.b.iii": {"sources": ["1.B.2.b.iii.4", "1.B.2.b.iii.5"]},
        # consistency check for 1.B.2
        "1.B.2": {"sources": ["1.B.2.b.iii"]},
    },
    # We don't have HFCs and PFCs in the report, hence basket_copy is not relevant
    # "basket_copy": {
    #     "GWPs_to_add": ["SARGWP100", "AR5GWP100", "AR6GWP100"],
    #     # "entities": ["HFCS", "PFCS"],
    #     "source_GWP": gwp_to_use,
    # },
}

# Note on downscaling: Data are always available for the same years: 2013-2019,
# so temporal downscaling does not makes sense here.
# TODO: Perhaps entity, category downscaling can be done?

gas_baskets = {
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O"],
}
