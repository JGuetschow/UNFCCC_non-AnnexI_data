"""
Configuration file to read Saint Kitts and Nevis' BUR 1.

Tables to read:
- The sector tables in the Annex from page 149 - done
- trend tables page 111-113
- page 117
- page 118
- page 119
- page 121
- page 124

Not reading:
- page 97 - trend table with data for 2008, because it's in the trend tables from page 111
- page 113 - slice of trend table on page 111
"""

gwp_to_use = "AR5GWP100"

# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "KNA-GHG-Inventory",
    "provenance": "measured",
    "area": "KNA",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        "NMVOCs": "NMVOC",
        "HFCS": f"HFCS ({gwp_to_use})",
        "PFCS": f"PFCS ({gwp_to_use})",
        "SF6": f"SF6 ({gwp_to_use})",
        "Other halogenated gases with CO2 equivalent conversion factors (1)": f"UnspMixOfHFCs ({gwp_to_use})",
    },
}

meta_data = {
    "references": "https://unfccc.int/documents/633382",
    "rights": "",  # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Saint Kitts and Nevis. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

filter_remove = {
    "f_memo": {"category": "MEMO"},
    "f1": {
        "entity": "Other halogenated gases without CO2 equivalent conversion factors (2)"
    },
}

conf_general = {
    "cat_code_regexp": r"^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*",
}

conf_trend = {
    "overview": {
        "fix_single_value": {
            "cat": "MBIO",
            "year": "2018",
            "new_value": "0.17",
        },
        "entity": f"KYOTOGHG ({gwp_to_use})",
        "unit": "GgCO2eq",
        "replace_data_entries": {"NO,NE": "NO"},
        "cat_codes_manual": {
            "Total CO2 Eq. Emissions without  LULUCF": "M.0.EL",
            "Total CO2 Eq. Emissions with  LULUCF": "M.LULUCF",
            # "1. Energy": "1. Energy",
            "A. Fuel Combustion": "1.A",
            "1.  Energy Industries": "1.A.1",
            "2.  Man. Ind. & Constr.": "1.A.2",
            "3.  Transport": "1.A.3",
            "4.  Other Sectors": "1.A.4",
            "5.  Other": "1.A.5",
            "B. Fugitive Emissions from Fuels": "1.B",
            "1.  Solid Fuels": "1.B.1",
            "2.  Oil and Natural Gas and other…": "1.B.2",
            # "2.  Industrial Processes": "2.  Industrial Processes",
            "A.  Mineral Industry": "2.A",
            "B.  Chemical Industry": "2.B",
            "C.  Metal Industry": "2.C",
            "D.  Non-energy products": "2.D",
            "E.  Electronics industry": "2.E",
            "F.  Product uses as ODS substitutes": "2.F",
            "G.  Other product manufacture and": "2.G",
            "use  H.  Other": "2.H",
            # "3.  Agriculture": "3.  Agriculture",
            "A.  Enteric Fermentation": "3.A.1",
            "B.  Manure Management": "3.A.2",
            "C.  Rice Cultivation": "3.C.7",
            "D.  Agricultural Soils": "3.C.4",  # TODO confirm!
            "E.  Prescribed Burning of Savannahs": "3.C.1.d",  # TODO confirm!
            "F.  Field Burning of Agricultural": "3.C.1.b",  # TODO confirm!
            "Residues  G.  Liming": "3.C.2",
            "H.  Urea applications": "3.C.3",
            "I.  Other carbon-containing": "3.D",  # TODO confirm!
            "fertilisers  4. Land Use, Land-Use Change and  Forestry": "3.B",
            "A. Forest Land": "3.B.1",
            "B. Cropland": "3.B.2",
            "C. Grassland": "3.B.3",
            "D. Wetlands": "3.B.4",
            "E. Settlements": "3.B.5",
            "F. Other Land": "3.B.6",
            "G. Harvested wood products": "3.D.1",
            "H. Other": "3.D.2",
            "5. Waste": "4",
            "A.  Solid Waste Disposal": "4.A",
            "B.  Biological treatment of solid": "4.B",
            "waste  C. Incineration and open burning of": "4.C",
            "D. Waste water treatment and": "4.D",
            "discharge  E.  Other": "4.E",
            "6.  Other": "5",
            "CO2 Emissions from Biomass": "M.BIO",
        },
        "drop_cols": [
            "change to BY",
            "change to PY",
        ],
        "header": ["orig_category"],
        "years": [
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
        ],
        "extra_columns": [
            "change to BY",
            "change to PY",
        ],
        "split_values": {
            "cat": "3B2",
            "keep_value_no": 1,
        },
        "page_defs": {
            "111": {"skip_rows_start": 1},
            "112": {"skip_rows_start": 1},
            "113": {"skip_rows_start": 1},
        },
    }
}

conf = {
    "energy": {
        # TODO: List of entities are always keys of unit mapping dict
        "entities": ["CO2", "CH4", "N2O", "NOX", "CO", "NMVOCs", "SO2"],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "149": {"skip_rows_start": 2},
            "150": {"skip_rows_start": 2},
            "151": {"skip_rows_start": 2},
            "152": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOCs": "Gg",
            "SO2": "Gg",
        },
    },
    "ipuu": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "HFCS",
            "PFCS",
            "SF6",
            "Other halogenated gases with CO2 equivalent conversion factors (1)",
            "Other halogenated gases without CO2 equivalent conversion factors (2)",
            "NOX",
            "CO",
            "NMVOC",
            "SO2",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "153": {"skip_rows_start": 2},
            "154": {"skip_rows_start": 2},
            "155": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "HFCS": "GgCO2eq",
            "PFCS": "GgCO2eq",
            "SF6": "GgCO2eq",
            "Other halogenated gases with CO2 equivalent conversion factors (1)": "GgCO2eq",
            "Other halogenated gases without CO2 equivalent conversion factors (2)": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
            "SO2": "Gg",
        },
    },
    "AFOLU": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "NOX",
            "CO",
            "NMVOC",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "156": {"skip_rows_start": 3},
            "157": {"skip_rows_start": 3},
            "158": {"skip_rows_start": 3},
        },
        "replace_data_entries": {
            "NO,NA": "NO",
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
        },
    },
    "waste": {
        "entities": [
            "CO2",
            "CH4",
            "N2O",
            "NOX",
            "CO",
            "NMVOC",
            "SO2",
        ],
        "header": ["orig_category"],
        "cat_codes_manual": {
            "Information Items": "MEMO",
            "CO2 from Biomass Combustion for Energy Production": "MBIO",
        },
        "page_defs": {
            "159": {"skip_rows_start": 2},
        },
        "replace_data_entries": {
            "NO,NA": "NO",
            "NO,NE": "NO",
            "NE,NO": "NO",
            "NO,IE": "NO",
        },
        "unit_mapping": {
            "CO2": "Gg",
            "CH4": "Gg",
            "N2O": "Gg",
            "NOX": "Gg",
            "CO": "Gg",
            "NMVOC": "Gg",
            "SO2": "Gg",
        },
    },
}
