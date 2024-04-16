coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# define config dict
inv_conf = {
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "header": [
        "Greenhouse gas source and sink categories",
        "CO2",
        "CH4",
        "N2O",
        "HFCs",
        "PFCs",
        "SF6",
        "Other halogenated gases with CO2 equivalent conversion factors",
        "Other halogenated gases without CO2 equivalent conversion factors",
        "NOx",
        "CO",
        "NMVOCs",
        "SO2",
    ],
    "unit": [
        "-",
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
    "cat_codes_manual": {
        "Memo Items (5)": "MEMO",
        "International Bunkers": "M.BK",
        "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
        "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
        # TODO: Handle with regex instead of explicitly adding all options.
        "1.A.3.d.i - International water-borne navigation (International                      bunkers) (1)": "M.BK.M",
        "1.A.3.d.i - International water-borne navigation (International bunkers)                      (1)": "M.BK.M",
        "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
        "Total National Emissions and Removals": "0",
    },
}

inv_conf_per_year = {
    "2005": {
        "pages_to_read": ["197", "198", "199", "200"],
    },
    "2006": {
        "pages_to_read": ["201", "202", "203", "204"],
    },
    "2007": {
        "pages_to_read": ["205", "206", "207", "208"],
    },
    "2008": {
        "pages_to_read": ["209", "210", "211", "212"],
    },
    "2009": {
        "pages_to_read": ["213", "214", "215", "216"],
    },
    "2010": {
        "pages_to_read": ["221", "222", "223", "224"],
    },
    "2011": {
        "pages_to_read": ["225", "226", "227", "228"],
    },
    "2012": {
        "pages_to_read": ["229", "230", "231", "232"],
    },
    "2013": {
        "pages_to_read": ["233", "234", "235", "236"],
    },
    "2014": {
        "pages_to_read": ["237", "238", "239", "240"],
    },
    "2015": {
        "pages_to_read": ["241", "242", "243", "244"],
        # Some values move to wrong columns
        "fix_values": [
            (2, 10, "21,529"),
            (1, 12, "NMVOCs"),
            (2, 12, "0"),
        ],
        # for this table an additional column is created
        # that needs to be deleted
        "delete_columns": [11],
    },
    "2016": {
        "pages_to_read": ["245", "246", "247", "248"],
    },
    "2017": {
        "pages_to_read": ["249", "250", "251", "252"],
    },
    "2018": {
        "pages_to_read": ["253", "254", "255", "256"],
    },
    "2019": {
        "pages_to_read": ["257", "258", "259", "260"],
    },
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "BDI-GHG-Inventory",
    "provenance": "measured",
    "area": "BDI",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# Page 64: The global warming potentials (GWPs) recommended by the IPCC Fifth Assessment Report (AR5)
# and based on the annex to Decision 18/CMA.1 have been used to convert GHGs other than CO2
# into their equivalent. These GWPs provide a consistent basis for comparing the relative effect
# of emissions of all GHGs standardized over a 100-year period by converting emissions of other
# GHGs into those of CO2. The values adopted for the three direct GHGs are 1 for CO2, 28 for CH4
# and 265 for N2O.
gwp_to_use = "AR5GWP100"
coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NMVOCs": "NMVOC",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_empty": {"category": ""},
    "f1": {
        "entity": ["Other halogenated gases with CO2 equivalent conversion factors"],
    },
    "f2": {
        "entity": ["Other halogenated gases without CO2 equivalent conversion factors"],
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/611668",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Burundi. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
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
            "sources": ["1", "2", "M.AG", "4", "5"],
            "name": "National total emissions excluding LULUCF",
        },
    },
    "basket_copy": {
        "GWPs_to_add": ["SARGWP100", "AR4GWP100", "AR6GWP100"],
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
