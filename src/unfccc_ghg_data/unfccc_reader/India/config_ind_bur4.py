"""Config for India's BUR4

Full configuration including PRIMAP2 conversion config and metadata

"""

#### configuration for trend tables
page_def_trends = {
    "139": {  # page 113: 2011-2020 trends
        "table_areas": ["49,766,544,69"],
        "flavor": "stream",
        "rows_to_fix": {
            3: [
                "2. Manufacturing Industries &",
                "2. Industrial Processes and",
                "E. Production of halocarbons",
                "E. Prescribed Burning of",
                "F. Field Burning of Agricultural",
                "C. Biological Treatment of Solid",
                "D. Incineration and Open",
            ],
            -2: ["GHG Sources and Removals"],
        },
        "entity_row": 0,
        "unit_row": 1,
    },
    "140": {  # page 114: 2011-2020 trends
        "table_areas": ["58,789,542,699"],
        "flavor": "stream",
        "rows_to_fix": {
            -2: ["GHG Sources and Removals"],
        },
        "entity_row": 0,
        "unit_row": 1,
    },
}

unit_info = {
    "unit_row": "header",
    "entity_row": "header",
    "default_unit": "Gg",
    "regexp_entity": r"^.*",
    "regexp_unit": r"^.*",
    "manual_repl_unit": {
        "CO2 emission": "Gg",
        "CO2 removal": "Gg",
        "CH4": "Gg",
        "N2O": "Gg",
        "HFC 23": "Gg",
        "CF4": "Gg",
        "C2F6": "Gg",
        "SF6": "Gg",
        "CO2 equivalent": "GgCO2eq",
    },
}

index_cols = ["Unnamed: 0"]

gwp_to_use = "SARGWP100"
cat_col_trends = "GHG Sources and Removals"

coords_terminologies = {
    "area": "ISO3",
    "category": "India2020INV",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "India-GHG-inventory ",
    "provenance": "measured",
    "area": "IND",
    "scenario": "BUR4",
}

coords_defaults_trends = {
    "source": "India-GHG-inventory ",
    "provenance": "measured",
    "area": "IND",
    "scenario": "BUR4",
    "unit": "Gg CO2 / year",
    "entity": f"KYOTOGHG ({gwp_to_use})",
}


coords_value_mapping = {
    "unit": "PRIMAP1",
    "entity": {
        "CO2 equivalent": f"KYOTOGHG ({gwp_to_use})",
        "HFC 23": "HFC23",
        #'PFCs': 'PFCS (AR5GWP100)',
    },
    "category": {
        "Total Emission": "M.0.EL",
        "Net Emission": "0",
        "1. Energy": "1",
        "A. Fuel Combustion Activities": "1.A",
        "1. Energy Industries": "1.A.1",
        "a. Electricity production": "1.A.1.a.1",
        "b. Refinery": "1.A.1.b",
        "c. Manufacturing of Solid Fuel": "1.A.1.c",
        "2. Manufacturing Industries & Construction": "1.A.2",
        "a. Cement": "1.A.2.a",
        "b. Iron & steel": "1.A.2.b",  #'1.A.2.a',
        "c. Nonferrous metals": "1.A.2.c",  #'1.A.2.b',
        "d. Chemicals": "1.A.2.d",  #'1.A.2.c',
        "e Pulp & paper": "1.A.2.e",  #'1.A.2.d',
        "f. Food & beverages": "1.A.2.f",  #'1.A.2.e',
        "g. Non-metallic minerals": "1.A.2.g",
        "h. Mining & quarrying": "1.A.2.h",
        "i. Textile/leather": "1.A.2.i",
        "j. Bricks": "1.A.2.j",
        "k. Fertilizer": "1.A.2.k",
        "l. Engineering Sector": "1.A.2.l",
        "m. Nonspecific Industries": "1.A.2.m",
        "n. Glass Ceramic": "1.A.2.n",
        "3. Transport": "1.A.3",
        "a. Road transport": "1.A.3.b",
        "b. Civil Aviation": "1.A.3.a",
        "c. Railways": "1.A.3.c",
        "d. Navigation": "1.A.3.d",
        "4. Other sectors": "1.A.4",
        "a. Commercials/Institutional": "1.A.4.a",
        "b. Residential": "1.A.4.b",
        "c. Agricultural/fisheries": "1.A.4.c",
        "d. Biomass burnt for energy": "1.A.4.d",
        "B. Fugitive Emission from fuels": "1.B",
        "1 Solid fuels": "1.B.1",
        "a. Above ground mining": "1.B.1.a",
        "b. Underground mining": "1.B.1.b",
        "2 Oil and Natural gas": "1.B.2",
        "a. Oil": "1.B.2.a",
        "b. Natural gas": "1.B.2.b",
        "c. Venting and Flaring": "1.B.2.c",
        "2. Industrial Processes and Product Use": "2",
        "A. Minerals": "2.A",
        "1. Cement production": "2.A.1",
        "2. Lime production": "2.A.2",
        "3. Limestone and Dolomite Use": "2.A.3",
        "5. Glass": "2.A.5",
        "6. Ceramics": "2.A.6",
        "B. Chemicals": "2.B",
        "1 Ammonia production": "2.B.1",
        "2 Nitric acid production": "2.B.2",
        "3. Carbide production": "2.B.3",
        "4. Titanium dioxide production": "2.B.4",
        "5. Soda ash Production": "2.B.5",
        "6. Methanol production": "2.B.6",
        "7. Ethylene production": "2.B.7",
        "8. EDC & VCM production": "2.B.8",
        "9. Ethylene Oxide production": "2.B.9",
        "10. Acrylonitrile production": "2.B.10",
        "11.Carbon Black production": "2.B.11",
        "12. Caprolactam": "2.B.12",
        "C Metal Production": "2.C",
        "1. Iron & Steel production": "2.C.1",  #'2.C.1',
        "2. Ferroalloys production": "2.C.2",  #'2.C.2',
        "3. Aluminium production": "2.C.3",  #'2.C.3',
        "4. Lead production": "2.C.4",  #'',
        "5. Zinc production": "2.C.5",  #'',
        "6. Magnesium Production": "2.C.6",  #'',
        "D. Non-energy product use": "2.D",
        "1. Lubricant": "2.D.1",  #'',
        "2. Paraffin wax": "2.D.2",  #'',
        "E. Production of halocarbons and sulphur hexafluoride": "2.E",
        "F. Consumption of halocarbons and sulphur hexafluoride": "2.F",
        "H. Other": "2.H",
        "1. Pulp & paper": "2.H.1",
        "3. Agriculture": "3",
        "A. Enteric Fermentation": "3.A",
        "B. Manure Management": "3.B",
        "C. Rice Cultivation": "3.C",
        "D. Agricultural Soils": "3.D",
        "Direct N2O Emissions": "3.D.1",
        "Indirect N2O Emissions": "3.D.2",
        "F. Field Burning of Agricultural Residues": "3.F",
        "G. Harvested Wood Products": "3.G",
        "4. LULUCF": "4",
        "A. Forestland": "4.A",
        "B. Cropland": "4.B",
        "C. Grassland": "4.C",
        "D. Settlement": "4.E",  # to be consistent with trends and usual order
        "E. Wetland": "4.D",
        "F. Other land": "4.F",
        "5. Waste": "5",
        "A. Solid waste disposal on land": "5.A",
        "1. Managed Waste Disposal on Land": "5.A.1",
        "B. Waste-water handling": "5.B",
        "1. Industrial Wastewater": "5.B.1",
        "2. Domestic and Commercial wastewater": "5.B.2",
        "C. Biological Treatment of Solid Waste": "5.C",
        "D. Incineration and Open Burning of Waste": "5.D",
        "Memo Item (not accounted in total Emissions)": "IGNORE",
        "International Bunkers": "M.BK",
        "Aviation": "M.BK.A",
        "Marine": "M.BK.M",
        "CO2 from Biomass": "M.BIO",
    },
}

coords_value_mapping_trends = {
    "unit": {
        "Gg CO2 Equivalent": "Gg CO2 / year",
    },
    "entity": {
        "CO2 equivalent": f"KYOTOGHG ({gwp_to_use})",
        "HFC 23": "HFC23",
        #'PFCs': 'PFCS (AR5GWP100)',
    },
    "category": {
        "Total (without LULUCF)": "M.0.EL",
        "Total (with LULUCF)": "0",
        "1. Energy": "1",
        "A. Fuel Combustion Activities": "1.A",
        "1. Energy Industries": "1.A.1",
        "2. Manufacturing Industries & Construction": "1.A.2",
        "3. Transport": "1.A.3",
        "4. Other sectors": "1.A.4",
        "B. Fugitive Emission from fuels": "1.B",
        "1. Solid fuels": "1.B.1",
        "2. Oil and Natural gas": "1.B.2",
        "C. CO2 Transport and Storage": "1.C",
        "2. Industrial Processes and Product Use": "2",
        "A. Mineral Industry": "2.A",
        "B. Chemical Industry": "2.B",
        "C. Metal Industry": "2.C",
        "D. Other": "2.D",
        "E. Production of halocarbons and sulphur hexafluoride": "2.E",
        "3. Agriculture": "3",
        "A. Enteric Fermentation": "3.A",
        "B. Manure Management": "3.B",
        "C. Rice Cultivation": "3.C",
        "D. Agricultural Soils": "3.D",
        "E. Prescribed Burning of Savannas": "3.E",
        "F. Field Burning of Agricultural Residues": "3.F",
        "4. LULUCF": "4",
        "A. Forestland": "4.A",
        "B. Cropland": "4.B",
        "C. Grassland": "4.C",
        "D. Wetlands": "4.D",
        "E. Settlement": "4.E",
        "F. Other Land": "4.F",
        "G. Harvested Wood Products": "4.G",
        "H. Other": "4.H",
        "5. Waste": "5",
        "A. Solid waste disposal on land": "5.A",
        "B. Waste-water handling": "5.B",
        "C. Biological Treatment of Solid Waste": "5.C",
        "D. Incineration and Open Burning of Waste": "5.D",
        "Memo Items": "IGNORE",
        "International Bunkers": "M.BK",
        "Aviation": "M.BK.A",
        "Marine": "M.BK.M",
        "CO2 from Biomass": "M.BIO",
    },
}

coords_cols = {"category": "category", "entity": "entity", "unit": "unit"}

coords_cols_trends = {
    "category": cat_col_trends,
}

add_coords_cols = {
    # "orig_cat_name": ["orig_cat_name", "category"],
}

filter_remove = {
    "f1": {
        "category": [
            "d. Biomass burnt for energy",
            "Memo Item (not accounted in total Emissions)",
        ],
    },
    # "f2": {
    #    "entity": ["HFCs", "PFCs"], # are reported in Gg without GWPs
    # },
}

filter_remove_trends = {
    "f1": {
        cat_col_trends: ["Memo Items"],
    },
}

meta_data = {
    "references": "https://https://unfccc.int/documents/645149",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "India. Biennial update report (BUR). BUR 4.",
    "comment": "Read from pdf by Johannes Gütschow.",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}


# processing
terminology_proc = "IPCC2006_PRIMAP"

# conversion has to be done individually for inventory and trends as they use different categories
cat_conversion_inventory = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.1.a.1": "1.A.1.a.1",
        "1.A.1.b": "1.A.1.b",
        "1.A.1.c": "1.A.1.c",
        "1.A.2": "1.A.2",
        "1.A.2.a": "M.1.A.2.f.2",  # cement
        "1.A.2.b": "1.A.2.a",  # iron and steel
        "1.A.2.c": "1.A.2.b",  # non-ferrous metals
        "1.A.2.d": "1.A.2.c",  # chemicals
        "1.A.2.e": "1.A.2.d",  # pulp, paper
        "1.A.2.f": "1.A.2.e",  # food, beverages
        "1.A.2.g": "M.1.A.2.f.1",  # non-metallic minerals
        "1.A.2.h": "1.A.2.i",  # mining quarrying
        "1.A.2.i": "1.A.2.l",  # textile, leather
        "1.A.2.j": "M.1.A.2.f.4",  # bricks
        "1.A.2.k": "M.1.A.2.m.2",  # fertilizer
        "1.A.2.l": "1.A.2.h",  # engineering (mapped to machinery)
        "1.A.2.m": "M.1.A.2.m.1",  # nonspecific industries
        "1.A.2.n": "M.1.A.2.f.3",  # glass, ceramic
        "1.A.3": "1.A.3",
        "1.A.3.a": "1.A.3.a.2",
        "1.A.3.b": "1.A.3.b",
        "1.A.3.c": "1.A.3.c",
        "1.A.3.d": "1.A.3.d.2",
        "1.A.4": "1.A.4",
        "1.A.4.a": "1.A.4.a",
        "1.A.4.b": "1.A.4.b",
        "1.A.4.c": "1.A.4.c",
        "1.A.4.d": "1.A.4.d",  # 1.A.5 might be better, but trend tables lack resolution
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.1.a": "1.B.1.a.1",
        "1.B.1.b": "1.B.1.a.2",
        "1.B.2": "1.B.2",
        #'1.B.2.a', '1.B.2.b', '1.B.2.c',
        "2": "2",
        "2.A": "2.A",
        "2.A.1": "2.A.1",  # cement
        "2.A.2": "2.A.2",  # lime
        "2.A.3": "2.A.4.d",  # limestone and dolomite use
        "2.A.5": "2.A.3",  # glass
        "2.A.6": "2.A.4.a",  # ceramics
        "2.B": "M.2.B.1-8",
        "2.B.1": "2.B.1",  # ammonia
        "2.B.2": "2.B.2",  # nitric acid
        "2.B.3": "2.B.5",  # carbide
        "2.B.4": "2.B.6",  # titanium dioxide
        "2.B.5": "2.B.7",  # soda ash
        "2.B.6": "2.B.8.a",  # methanol
        "2.B.7": "2.B.8.b",  # ethylene
        "2.B.8": "2.B.8.c",  # ethylene dichloride and vinyl chloride monomer
        "2.B.9": "2.B.8.d",  # Ethylene Oxide
        "2.B.10": "2.B.8.e",  # Acrylonitrile
        "2.B.11": "2.B.8.f",  # carbon black
        "2.B.12": "2.B.4",  # caprolactam
        "2.C": "2.C",
        "2.C.1": "2.C.1",  # '1. Iron & Steel production',
        "2.C.2": "2.C.2",  # '2. Ferroalloys production',
        "2.C.3": "2.C.3",  # '3. Aluminium production',
        "2.C.4": "2.C.5",  # '4. Lead production',
        "2.C.5": "2.C.6",  # '5. Zinc production',
        "2.C.6": "2.C.4",  # '6. Magnesium Production',
        "2.D": "2.D",
        "2.D.1": "2.D.1",  # '1. Lubricant',
        "2.D.2": "2.D.2",  # '2. Paraffin wax',
        "2.E": "2.B.9",
        "2.F": "2.F",
        "2.H": "2.H",
        "2.H.1": "2.H.1",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.C.45.AG",
        "3.D.1": "3.C.4",  # direct N2O
        "3.D.2": "3.C.5",  # indirect N2O
        "3.F": "3.C.1.b",
        "4": "M.LULUCF",
        "4.A": "3.B.1",
        "4.B": "3.B.2",
        "4.C": "3.B.3",
        "4.D": "3.B.4",
        "4.E": "3.B.5",
        "4.F": "3.B.6",
        "5": "4",
        "5.A": "4.A",
        "5.A.1": "4.A.1",
        "5.B": "4.D",
        "5.B.1": "4.D.2",
        "5.B.2": "4.D.1",
        "5.C": "4.B",
        "5.D": "4.C",
        "M.0.EL": "M.0.EL",
        "M.BK": "M.BK",
        "M.BK.A": "M.BK.A",
        "M.BK.M": "M.BK.M",
        "M.BIO": "M.BIO",
    },
    "aggregate": {
        "1.A.1.a": {
            "sources": ["1.A.1.a.1"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        "1.A.2.f": {
            "sources": ["M.1.A.2.f.1", "M.1.A.2.f.2", "M.1.A.2.f.3", "M.1.A.2.f.4"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        "1.A.2.m": {
            "sources": ["M.1.A.2.m.1", "M.1.A.2.m.2"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        "1.A.3.a": {
            "sources": ["1.A.3.a.2"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        "1.A.3.d": {
            "sources": ["1.A.3.d.2"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        # '1.A.4': {'sources': ['1.A.4.a', '1.A.4.b', '1.A.4.c'],
        #             'sel': {
        #                 'entity': ['CO2', 'CH4', 'N2O', f'KYOTOGHG']
        #             },
        #             },  # not possible as trend tables lack resolution
        "1.B.1.a": {
            "sources": ["1.B.1.a.1", "1.B.1.a.2"],
            "sel": {"entity": ["CH4", "KYOTOGHG"]},
        },
        "2.A.4": {
            "sources": ["2.A.4.a", "2.A.4.d"],
            "sel": {"entity": ["CO2", "KYOTOGHG"]},
        },
        "2.B.8": {
            "sources": [
                "2.B.8.a",
                "2.B.8.b",
                "2.B.8.c",
                "2.B.8.d",
                "2.B.8.e",
                "2.B.8.f",
            ],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        "2.B": {
            "sources": ["M.2.B.1-8", "2.B.9"],
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG", "HFC23"]},
        },
        "2.H": {
            "sources": ["2.H.1"],
            # 'sel': {
            #     'entity': ['CO2', 'CH4', 'N2O', 'KYOTOGHG', 'HFC23']
            # },
        },
        "2": {
            "sources": ["2.A", "2.B", "2.C", "2.D", "2.F", "2.H"],
            # 'sel': {
            #     'entity': ['CO2', 'CH4', 'N2O', 'KYOTOGHG', 'HFC23']
            # },
        },
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            #'name': 'Livestock'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "3.C.1": {
            "sources": ["3.C.1.b"],
            #'name': 'Emissions from biomass burning'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b"],
            #'name': 'Emissions from biomass burning (Agriculture)'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "3.C": {
            "sources": ["3.C.1", "M.3.C.45.AG", "3.C.7"],
            #'name': 'Aggregate sources and non-CO2 emissions sources on land'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "M.3.C.AG": {
            "sources": ["M.3.C.1.AG", "M.3.C.45.AG", "3.C.7"],
            #'name': 'Aggregate sources and non-CO2 emissions sources on land ('
            #        'Agriculture)'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            #'name': 'Agriculture excluding livestock'
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        # consistency check for Agriculture
        "M.AG": {
            "sources": ["M.AG.ELV", "3.A"],
            "sel": {"entity": ["CH4", "N2O", "KYOTOGHG"]},
        },
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            #'name': 'AFOLU'
            "sel": {"entity": ["CO2", "CH4", "N2O", "KYOTOGHG"]},
        },
        # consistency check on top level categories
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
        "0": {"sources": ["1", "2", "3", "4"]},
    },
}

cat_conversion_trends = {
    "mapping": {
        "0": "0",
        "1": "1",
        "1.A": "1.A",
        "1.A.1": "1.A.1",
        "1.A.2": "1.A.2",
        "1.A.3": "1.A.3",
        "1.A.4": "1.A.4",
        "1.B": "1.B",
        "1.B.1": "1.B.1",
        "1.B.2": "1.B.2",
        "1.C": "1.C",
        "2": "2",
        "2.A": "2.A",
        "2.B": "M.2.B.1-8",
        "2.C": "2.C",
        "2.D": "M.2.DH",  # sum of 2.D and 2.H
        "2.E": "2.B.9",
        "3": "M.AG",
        "3.A": "3.A.1",
        "3.B": "3.A.2",
        "3.C": "3.C.7",
        "3.D": "M.3.C.45.AG",
        "3.E": "3.C.1.c",
        "3.F": "3.C.1.b",
        "4": "M.LULUCF",
        "4.A": "3.B.1",
        "4.B": "3.B.2",
        "4.C": "3.B.3",
        "4.D": "3.B.4",
        "4.E": "3.B.5",
        "4.F": "3.B.6",
        "4.G": "3.D.1",
        "4.H": "3.D.2",
        "5": "4",
        "5.A": "4.A",
        "5.B": "4.D",
        "5.C": "4.B",
        "5.D": "4.C",
        "M.0.EL": "M.0.EL",
        "M.BK": "M.BK",
        "M.BK.A": "M.BK.A",
        "M.BK.M": "M.BK.M",
        "M.BIO": "M.BIO",
    },
    "aggregate": {
        "2.B": {"sources": ["M.2.B.1-8", "2.B.9"]},
        "3.A": {
            "sources": ["3.A.1", "3.A.2"],
            #'name': 'Livestock'
        },
        "3.B": {"sources": ["3.B.1", "3.B.2", "3.B.3", "3.B.4", "3.B.5", "3.B.6"]},
        "3.C.1": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            #'name': 'Emissions from biomass burning'
        },
        "M.3.C.1.AG": {
            "sources": ["3.C.1.b", "3.C.1.c"],
            #'name': 'Emissions from biomass burning (Agriculture)'
        },
        "3.C": {
            "sources": ["3.C.1", "M.3.C.45.AG", "3.C.7"],
            #'name': 'Aggregate sources and non-CO2 emissions sources on land'
        },
        "3.D": {"sources": ["3.D.1", "3.D.2"]},
        "M.3.C.AG": {
            "sources": ["M.3.C.1.AG", "M.3.C.45.AG", "3.C.7"],
            #'name': 'Aggregate sources and non-CO2 emissions sources on land ('
            #        'Agriculture)'
        },
        "M.AG.ELV": {
            "sources": ["M.3.C.AG"],
            #'name': 'Agriculture excluding livestock'
        },
        # AFOLU consistency check
        "M.AG": {"sources": ["M.AG.ELV", "3.A"]},
        "M.LULUCF": {"sources": ["3.B", "3.D"]},
        "3": {
            "sources": ["M.AG", "M.LULUCF"],
            #'name': 'AFOLU'
        },
        # consistency check on top level categories
        "M.0.EL": {"sources": ["1", "2", "M.AG", "4"]},
        "0": {"sources": ["1", "2", "3", "4"]},
    },
}


# gas baskets
gas_baskets = {
    "HFCS (SARGWP100)": ["HFC23"],
    "HFCS (AR4GWP100)": ["HFC23"],
    "HFCS (AR5GWP100)": ["HFC23"],
    "HFCS (AR6GWP100)": ["HFC23"],
    "PFCS (SARGWP100)": ["CF4", "C2F6"],
    "PFCS (AR4GWP100)": ["CF4", "C2F6"],
    "PFCS (AR5GWP100)": ["CF4", "C2F6"],
    "PFCS (AR6GWP100)": ["CF4", "C2F6"],
    "FGASES (SARGWP100)": ["HFCS (SARGWP100)", "PFCS (SARGWP100)", "SF6", "NF3"],
    "FGASES (AR4GWP100)": ["HFCS (AR4GWP100)", "PFCS (AR4GWP100)", "SF6", "NF3"],
    "FGASES (AR5GWP100)": ["HFCS (AR5GWP100)", "PFCS (AR5GWP100)", "SF6", "NF3"],
    "FGASES (AR6GWP100)": ["HFCS (AR6GWP100)", "PFCS (AR6GWP100)", "SF6", "NF3"],
    "KYOTOGHG (SARGWP100)": ["CO2", "CH4", "N2O", "FGASES (SARGWP100)"],
    "KYOTOGHG (AR4GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR4GWP100)"],
    "KYOTOGHG (AR5GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR5GWP100)"],
    "KYOTOGHG (AR6GWP100)": ["CO2", "CH4", "N2O", "FGASES (AR6GWP100)"],
}
