coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# TODO: This is duplicate inormation
years_to_read = [
    "2005",
    "2006",
    "2007",
    "2008",
    "2009",
    "2010",
    "2011",
    "2012",
    "2013",
    "2014",
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
]

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
        # TODO: handle with regex
        "1.A.3.d.i - International water-borne navigation (International                      bunkers) (1)": "M.BK.M",
        "1.A.3.d.i - International water-borne navigation (International bunkers)                      (1)": "M.BK.M",
        "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
        "Total National Emissions and Removals": "0",
    },
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
        "fix_values": [
            (2, 10, "21,529"),
            (1, 12, "NMVOCs"),
            (2, 12, "0"),
        ],
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


gwp_to_use = "AR4GWP100"
coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "NMVOCs": "NMVOC",
        # "Other halogenated gases with CO2 equivalent conversion factors" : "PLACEHOLDER halo gases co2eq",
        # "Other halogenated gases without CO2 equivalent conversion factors" : "PLACEHOLDER halo gases"
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
