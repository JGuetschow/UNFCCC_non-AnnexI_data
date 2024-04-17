coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

inv_conf = {
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
    "cat_codes_manual": {
        # remove whitespace at start of line
        ' 2.G.2 -SF6 and PFCs from Other Product Uses' : '2.G.2 - SF6 and PFCs from Other Product Uses',
        ' 2.G.3 -N2O from Product Uses' : '2.G.3 - N2O from Product Uses',
        ' 1.C.1 -Transport of CO2' : '1.C.1 - Transport of CO2',
        " 3.C.1 -Emissions from biomass burning ": "3.C.1",
        "Memo Items (5)": "MEMO",
        "International Bunkers": "M.BK",
        "1.A.3.a.i - International Aviation (International Bunkers) (1)": "M.BK.A",
        "1.A.3.d.i - International water-borne navigation (International bunkers) (1)": "M.BK.M",
        "1.A.5.c - Multilateral Operations (1)(2)": "M.MULTIOP",
        "Total National Emissions and Removals": "0",
    },
    "header": [
        "Greenhouse gas source and sink categories",
        "CO2",
        "CH4",
        "N2O",
        "HFCs",
        "PFCs",
        "SF6",
        "other halogenated gases",
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
}

inv_conf_per_year = {
    "1990": {
        "pages_to_read": ["176", "177", "178", "179"],
        "rows_to_fix": {
            3: [
                "1.A.2 - Manufacturing Industries and",
                "2.B.4 - Caprolactam. Glyoxal and Glyoxylic Acid",
                "2.B.8 - Petrochemical and Carbon Black",
                "2.D - Non-Energy Products from Fuels and",
                "2.F - Product Uses as Substitutes for Ozone",
                "3.C - Aggregate sources and non-CO2 emissions",
                "3.C.4 - Direct N2O Emissions from managed",
                "3.C.5 - Indirect N2O Emissions from managed",
                "3.C.6 - Indirect N2O Emissions from manure",
                "5.A - Indirect N2O emissions from the atmospheric",
                "1.A.3.d.i - International water-borne navigation",
                "1.A.3.a.i - International Aviation (International",
            ],
            -2: ["3.C.1 - Emissions from biomass burning"],
            2: [" 3.C.1 -Emissions from biomass burning"],
        },
        "page_defs": {
            "176": {
                "area": ["76,501,763,83"],
                "cols": ["265,320,360,396,433,471,503,564,624,658,694,741"],
            },
            "177": {
                "area": ["68,542,762,85"],
                "cols": ["280,329,374,410,449,482,546,604,637,679,725,751"],
            },
            "178": {
                "area": ["71,543,761,81"],
                "cols": ["265, 320,361,411,447,483,546,604,621,653,719,746"],
            },
            "179": {
                "area": ["70,542,761,346"],
                "cols": ["287,328,365,410,449,482,540,600,636,675,721,750"],
            },
        },
    },
    "2020": {
        "page_defs": {
            "180": {
                "area": ["70,436,769,86"],
                "cols": ["270, 322, 367, 405, 455, 488,550,607,637,669,727,753"],
            },
            "181": {
                "area": ["68,541,768,86"],
                "cols": ["288,343,379,405,460,490,559,600,650,683,729,755"],
            },
            "182": {
                "area": ["69, 539, 771, 86"],
                "cols": ["273,331,371,425,462,491,560,615,639,671,729,755"],
            },
            "183": {
                "area": ["69, 540, 769, 373"],
                "cols": ["288, 328,363,425,459,492,560,619,650,683,731,757"],
            },
        },
        "rows_to_fix": {
            # 3: [
            #
            #
            #
            # ],
            -2: [
                "1.C.1 - Transport of CO2",
                "2.G.2 - SF6 and PFCs from Other Product Uses",
                "2.G.3 - N2O from Product Uses",
            ],
            2: [
                "2.B.8 - Petrochemical and Carbon Black",
                "2.D - Non-Energy Products from Fuels and",
                "2.F - Product Uses as Substitutes for Ozone",
                "3.C - Aggregate sources and non-CO2 emissions",
                "3.C.4 - Direct N2O Emissions from managed",
                "3.C.5 - Indirect N2O Emissions from managed",
                "3.C.6 - Indirect N2O Emissions from manure",
                "5.A - Indirect N2O emissions from the atmospheric",
                "1.A.3.d.i - International water-borne navigation",
                "1.A.3.a.i - International Aviation (International",
                "2.B.4 - Caprolactam. Glyoxal and Glyoxylic Acid",
            ],
        },
    },
}

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "MNG-GHG-Inventory",
    "provenance": "measured",
    "area": "MNG",
    "scenario": "BUR2",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# TODO
gwp_to_use = "SARGWP100"
coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "HFCs": f"HFCS ({gwp_to_use})",
        "PFCs": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "other halogenated gases": f"other halogenated gases ({gwp_to_use})",
        "NMVOCs": "NMVOC",
    },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_empty": {"category": ""},
    "f2": {
        "entity": ["Other halogenated gases without CO2 equivalent conversion factors"],
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/633382",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Mongolia. Biennial update report (BUR). BUR2",
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
        "GWPs_to_add": ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
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
