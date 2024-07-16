"""
Configuration file to read Bangladesh's BUR 1.
"""

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
    "scenario": "BUR2",
}

gwp_to_use = "AR4GWP100"

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    # "entity": {
    #     "HFCs": f"HFCS ({gwp_to_use})",
    #     "PFCs": f"PFCS ({gwp_to_use})",
    #     "SF6": f"SF6 ({gwp_to_use})",
    #     "other halogenated gases": f"other halogenated gases ({gwp_to_use})",
    #     "NMVOCs": "NMVOC",
    # },
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_info": {"category": "INFO"},
    # "f2": {
    #     "entity": ["Other halogenated gases without CO2 equivalent conversion factors"],
    # },
}

meta_data = {
    "references": "https://unfccc.int/documents/634149",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Bangladesh. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

inv_conf = {
    "entity_row": 0,
    "unit_row": 1,
    "index_cols": "Greenhouse gas source and sink categories",
    "header_long": ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
}
inv_conf_per_year = {
    "2013": {
        "page_defs": {
            "207": {
                "area": ["60,630,534,79"],
                "cols": ["387,444,495"],
                "skip_rows_start": 0,
                "skip_rows_end": 0,
            },
            "208": {
                "area": ["63,720,527,120"],
                "cols": ["380,437,491"],
                "skip_rows_start": 8,
                "skip_rows_end": 4,
            },
        },
        "rows_to_fix": {
            3: [
                "3 - GHG Emissions Agriculture, Livestock & Forest and Other Land -Use"
            ],
            2: [
                # B-Methane emission from domestic waste water and
                # c-nitrous oxide emission from domestic waste water are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # Total Manure ch4 emissions and
                # Total Direct n2o emissions from manure system are the same category
                # and should be merged
                "Total Manure ch4 emissions",
            ],
            -2: [
                "ch4 emission from rice field",
                "indirect nitrous oxide (n2o) from n based fertilizer",
                "Direct nitrous oxide (n2o) emissions from fertilizer application",
                "Total enteric ch4 emissions",
                "Total Manure ch4 emissions",
                "Total Direct n2o emissions from manure system",
                "Total indirect n2o emissions - Volatilization",
                "Total indirect n2o emissions - leaching/Runoff",
                "CO2 from Biomass burning for Energy purpose",
            ],
        },
        "header": [
            "Greenhouse gas source and sink categories",
            "CO2",
            "CH4",
            "N2O",
        ],
        "unit": [
            "-",
            "Gg",
            "Gg",
            "Gg",
        ],
        "skip_rows": 6,
        "cat_codes_manual": {
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "2 a. 1-cement Production": "2.A.1",
            "2 B. 1 - ammonia Production": "2.B.1",
            "2 C-Metal Industry": "2.C",
            "2 c. 1 iron and steel Production": "2.C.1",
            "2. D - Non-Energy Products from Fuels and Solvent Use": "2.D",
            "2D 1-lubricant Use": "2.D.1",
            "ch4 emission from rice field": "3.C.7",
            "indirect nitrous oxide (n2o) from n based fertilizer": "3.C.5",
            "Direct nitrous oxide (n2o) emissions from fertilizer application": "3.C.4",
            "Direct carbon Dioxide emissions from urea fertilizer": "3.C.3",
            "Total enteric ch4 emissions": "3.A.1",
            "Total Manure ch4 emissions Total Direct n2o emissions from manure system": "3.A.2",
            "Total indirect n2o emissions -Volatilization": "3.C.5",
            "Total indirect n2o emissions -leaching/Runoff": "3.C.5",
            "4 a-solid Waste Disposal": "4.A",
            "B-Methane emission from domestic waste water c-nitrous oxide emission from domestic waste water": "4.D.1",
            "D- Metahne emission from industrial waste water": "4.D.2",
            "Memo items (5)": "MEMO",
            "Information Items": "INFO",
            "international Bunkers": "M.BK",
            "a-international aviation (international Bunkers)": "M.BK.A",
            "B-international Water-borne navigation (international Bunkers)": "M.BK.M",
            "CO2 from Biomass burning for Energy purpose": "M.BIO",
        },
        "merge_cats": "3C5",
    },
    "2014": {
        "page_defs": {
            "209": {
                "area": ["74,715,542,78"],
                "cols": ["380,441,498"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "210": {
                "area": ["64,715,529,196"],
                "cols": ["380,435,491"],
                "skip_rows_start": 8,
                "skip_rows_end": 4,
            },
        },
        "rows_to_fix": {
            3: ["3 - GHG Emissions Agriculture, Livestock & Forest and Other"],
            -2: [
                "ch4 emission from rice field",
                "indirect nitrous oxide (n2o) from n based fertilizer",
                "Direct nitrous oxide (n2o) emissions from fertilizer application",
                "Total enteric ch4 emissions",
                "Total Manure ch4 emissions",
                "Total Direct n2o emissions from manure system",
                "Total indirect n2o emissions - Volatilization",
                "Total indirect n2o emissions - leaching/Runoff",
                "CO2 from Biomass burning for Energy purpose",
            ],
            2: [
                # B-Methane emission from domestic waste water and
                # c-nitrous oxide emission from domestic waste water are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # Total Manure ch4 emissions and
                # Total Direct n2o emissions from manure system are the same category
                # and should be merged
                "Total Manure ch4 emissions",
            ],
        },
        "header": [
            "Greenhouse gas source and sink categories",
            "CO2",
            "CH4",
            "N2O",
        ],
        "unit": [
            "-",
            "Gg",
            "Gg",
            "Gg",
        ],
        "skip_rows": 0,
        "cat_codes_manual": {
            "1-a - Fuel combustion activities_energy industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "2 a. 1-cement Production": "2.A.1",
            "2 B. 1 - ammonia Production": "2.B.1",
            "2 C-Metal Industry": "2.C",
            "2 c. 1 iron and steel Production": "2.C.1",
            "2. D - Non-Energy Products from Fuels and Solvent Use": "2.D",
            "2D 1-lubricant Use": "2.D.1",
            "ch4 emission from rice field": "3.C.7",
            "indirect nitrous oxide (n2o) from n based fertilizer": "3.C.5",
            "Direct nitrous oxide (n2o) emissions from fertilizer application": "3.C.4",
            "Direct carbon Dioxide emissions from urea fertilizer": "3.C.3",
            "Total enteric ch4 emissions": "3.A.1",
            "Total Manure ch4 emissions Total Direct n2o emissions from manure system": "3.A.2",
            "Total indirect n2o emissions -Volatilization": "3.C.5",
            "Total indirect n2o emissions -leaching/Runoff": "3.C.5",
            "4 a-solid Waste Disposal": "4.A",
            "B-Methane emission from domestic waste water c-nitrous oxide emission from domestic waste water": "4.D.1",
            "D- Metahne emission from industrial waste water": "4.D.2",
            "Memo items (5)": "MEMO",
            "Information Items": "INFO",
            "international Bunkers": "M.BK",
            "a-international aviation (international Bunkers)": "M.BK.A",
            "B-international Water-borne navigation (international Bunkers)": "M.BK.M",
            "CO2 from Biomass burning for Energy purpose": "M.BIO",
        },
        "merge_cats": "3C5",
    },
}
