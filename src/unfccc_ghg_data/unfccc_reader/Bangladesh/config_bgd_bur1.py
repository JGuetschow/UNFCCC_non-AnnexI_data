"""
Configuration file to read Bangladesh's BUR 1.

# Overview of all available GHG tables

# not reading:
# table 7, page 70 - already in main table in annex
# table 8, page 71 - only four new data points for 2012
# figure 22, page 83 - this is a summary of all energy tables
# figure 23 - image of summary of IPUU, data are available as tables in same
# chapter
# table 27 - rice cultivation available - in main tables
# table 28 - N2O from fertilizers - in main tables
# table 29 - indirect N2O from fertilizer - in main table
# table 31 - enteric CH4 by livestock - low priority
# table 32 - manure CH4 by livestock - low priority
# table 37 - already in main tables in annex
# table 19-23, ammonia-urea, cement, glass, lubricants, steel mills
# 2013-2019 on pages 86-88 - already in main table

# reading:
# table 16, page 78 - 2013-2019 by industry sub-sectors - typed
# table 17, page 79 - 2013-2019 transportation - typed
# table 18, page 80 - residential 2013-2019 commercial sector  - typed
# table 19, page 80 - agriculture energy use 2013-2019 - typed
# figure 20, page 81 - gas leakage 2013-2019 - typed


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
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f_info": {"category": "INFO"},
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
        # TODO The manual codes can be summarised for all years
        "cat_codes_manual": {
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
    "2015": {
        "page_defs": {
            "211": {
                "area": ["75,712,550,88"],
                "cols": ["375,444,498"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "212": {
                "area": ["64,711,524,90"],
                "cols": ["369,436,492"],
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
                "a-co2 emission from soil",
                "c-co2 emission due to fuel wood removal for consumption",
            ],
            2: [
                # "B-Methane emission from domestic waste wate"r" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
        # These three categories only appear in 2015 and are all zero
        "categories_to_drop": [
            "a-co2 emission from soil",
            "c-co2 emission due to fuel wood removal for consumption",
            "B-conversion of forest land to other land use",
        ],
    },
    "2016": {
        "page_defs": {
            "213": {
                "area": ["73,712,544,77"],
                "cols": ["373,444,498"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "214": {
                "area": ["66,711,533,143"],
                "cols": ["359,435,492"],
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
    "2017": {
        "page_defs": {
            "215": {
                "area": ["74,715,543,80"],
                "cols": ["382,444,497"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "216": {
                "area": ["64,720,530,158"],
                "cols": ["380,433,490"],
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "2 a. 1-cement Production": "2.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2a3 Glass Production": "2.A.3",
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
    "2018": {
        "page_defs": {
            "217": {
                "area": ["75,713,542,91"],
                "cols": ["378,446,499"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "218": {
                "area": ["63,714,528,154"],
                "cols": ["374,438,491"],
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
    "2019": {
        "page_defs": {
            "219": {
                "area": ["75,713,542,91"],
                "cols": ["378,446,499"],
                "skip_rows_start": 9,
                "skip_rows_end": 0,
            },
            "220": {
                "area": ["63,714,524,139"],
                "cols": ["374,438,491"],
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
                # "B-Methane emission from domestic waste water" and
                # "c-nitrous oxide emission from domestic waste water" are the same category
                # and should be merged
                "B-Methane emission from domestic waste water",
                # "Total Manure ch4 emissions" and
                # "Total Direct n2o emissions from manure system" are the same category
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
            "1-A - Fuel Combustion Activities_Energy Industries": "1.A",
            "1 - a1- electricity Generation": "1.A.1",
            "1.a2- Manufacturing industries and construction": "1.A.2",
            "1.a3-Transport": "1.A.3",
            "1.a4-other sectors": "1.A.4",
            "2 a. 1-cement Production": "2.A.1",
            "2a3 Glass Production": "2.A.3",
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
            "Memo Items (5)": "MEMO",
            "Information Items": "INFO",
            "International Bunkers": "M.BK",
            "a-international aviation (international Bunkers)": "M.BK.A",
            "B-international Water-borne navigation (international Bunkers)": "M.BK.M",
            "CO2 from Biomass burning for Energy purpose": "M.BIO",
        },
        "merge_cats": "3C5",
        "categories_to_drop": ["in eq. Million Tons"],
    },
}

# needed for the pandas wide_to_long function
wide_to_long_col_replace = {
    "2013": "data2013",
    "2014": "data2014",
    "2015": "data2015",
    "2016": "data2016",
    "2017": "data2017",
    "2018": "data2018",
    "2019": "data2019",
}

manually_typed = {
    "figure_16": {
        # TODO Conflicting entities in figure: CO2e or CO2?
        # It says CO2 and gG more often, so I'm going with CO2
        "unit": "Gg",
        "entity": "CO2",
        "data": {
            "category": [
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
            ],
            "2013": [
                709,
                6,
                796,
                421,
                553,
                12174,
                1,
                1,
                0,
                4,
                5,
                4885,
                1280,
            ],
            "2014": [
                706,
                0,
                636,
                409,
                515,
                13896,
                0,
                0,
                0,
                0,
                203,
                4793,
                1276,
            ],
            "2015": [
                778,
                0,
                545,
                458,
                532,
                13660,
                0,
                0,
                0,
                0,
                195,
                5180,
                1799,
            ],
            "2016": [
                830,
                0,
                445,
                473,
                527,
                15771,
                0,
                0,
                0,
                0,
                118,
                5375,
                1700,
            ],
            "2017": [
                883,
                0,
                344,
                492,
                522,
                15141,
                0,
                0,
                0,
                0,
                179,
                5294,
                1546,
            ],
            "2018": [
                943,
                0,
                247,
                519,
                519,
                15949,
                0,
                0,
                0,
                0,
                193,
                5810,
                1764,
            ],
            "2019": [
                988,
                0,
                123,
                527,
                516,
                16091,
                0,
                0,
                0,
                0,
                216,
                5935,
                2492,
            ],
        },
    },
    "figure_17": {
        # TODO Conflicting entities in figure: CO2e or CO2?
        # This category should mainly be combustion emissions -> CO2
        "entity": "CO2",
        "unit": "Gg",
        "data": {
            "category": [
                "1.A.3.a.ii",
                "1.A.3.b.i.2",
                "1.A.3.b.ii.2",
                "1.A.3.b.iii",
                "1.A.3.b.iv",
                "1.A.3.c",
                "1.A.3.d.ii",
            ],
            "2013": [
                694,
                1450,
                1215,
                8960,
                979,
                115,
                162,
            ],
            "2014": [
                704,
                1485,
                914,
                8126,
                934,
                113,
                196,
            ],
            "2015": [
                738,
                1708,
                1135,
                9082,
                1030,
                117,
                208,
            ],
            "2016": [
                757,
                1710,
                1030,
                8504,
                1089,
                115,
                350,
            ],
            "2017": [
                822,
                1962,
                1298,
                10201,
                1136,
                156,
                289,
            ],
            "2018": [
                890,
                2019,
                1410,
                10320,
                1152,
                140,
                332,
            ],
            "2019": [
                938,
                2440,
                1985,
                12682,
                1232,
                168,
                401,
            ],
        },
    },
    "figure_18": {
        # TODO Conflicting entities in figure: CO2e or CO2?
        "entity": "CO2",
        "unit": "Gg",
        "data": {
            "category": ["1.A.4.a", "1.A.4.b"],
            "2013": [1871, 6703],
            "2014": [1619, 6960],
            "2015": [1522, 8573],
            "2016": [1260, 9755],
            "2017": [981, 9702],
            "2018": [833, 11355],
            "2019": [835, 12317],
        },
    },
    "figure_19": {
        # TODO Conflicting entities in figure: CO2e or CO2?
        "unit": "Gg",
        "entity": "CO2",
        "data": {
            "category": ["1.A.4.c.i", "1.A.4.c.iii", "1.A.4.c"],
            "2013": [2692, 5, 2697],
            "2014": [2804, 5, 2809],
            "2015": [2977, 6, 2983],
            "2016": [3035, 6, 3040],
            "2017": [2903, 6, 2909],
            "2018": [3496, 6, 3502],
            "2019": [3446, 6, 3452],
        },
    },
    "figure_20": {
        "unit": "Gg",
        "entity": "CO2",
        "data": {
            "category": ["1.B.2.b.iii.4", "1.B.2.b.iii.5", "1.B.2.b.iii"],
            "2013": [896, 8440, 9336],
            "2014": [896, 8440, 9336],
            "2015": [896, 8440, 9336],
            "2016": [896, 8440, 9336],
            "2017": [896, 6429, 7325],
            "2018": [896, 6429, 7325],
            "2019": [896, 4289, 5185],
        },
    },
}

# correct values that are obviously wrong in the tables
values_to_correct = [
    # the sum of 1.A sub-categories does not match the value of 1.A
    ("1.A", "CH4", "2014", 110),
    ("1.A", "CO2", "2014", 77373),
    ("1", "N2O", "2014", 3.8),
    # For the sum for CO2 in category 3 they forgot to add 3.B
    ("3", "CO2", "2013", 8140),
    ("3", "CO2", "2014", 8923),
    ("3", "CO2", "2015", 9791),
    ("3", "CO2", "2016", 10518),
    ("3", "CO2", "2017", 11359),
    ("3", "CO2", "2018", 11993),
    ("3", "CO2", "2019", 12640),
]

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
        # There is no data for 3.D
        # "M.3.D.AG": {"sources": ["3.D.2"], "name": "Other (Agriculture)"},
        # "M.3.D.AG" is empty, so I'm not sure we need it
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
        # check if the typed numbers add up to the total of 1.A.4.c in the same table
        "1.A.4.c": {"sources": ["1.A.4.c.i", "1.A.4.c.iii"]},
        # check if typed numbers add up to the total of 1.A.4 from the main table
        "1.A.4": {"sources": ["1.A.4.a", "1.A.4.b", "1.A.4.c"]},
        # check if the typed numbers add up to the total of 1.A.4.c in the same table
        "1.B.2.b.iii": {"sources": ["1.B.2.b.iii.4", "1.B.2.b.iii.5"]},
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
