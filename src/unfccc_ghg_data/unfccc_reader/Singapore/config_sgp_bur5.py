table_def_templates = {
    '66_1': {  # 66
        "area": ['68,743,522,157'],
        "cols": ['224,280,319,359,399,445,481'],
        "rows_to_fix": {
            # 2: ['and Sink Categories',],
            3: ['1A2 Manufacturing Industries',
                '1B3 Other Emissions from', '1C - Carbon Dioxide Transport',
                '2 — INDUSTRIAL PROCESSES AND', '2D - Non-Energy Products from',
                '2F - Product Uses as Substitutes for',
                '2G - Other Product Manufacture'],
        },
    },
    '66_2': {  # 66
        "area": ['671,744,1117,265'],
        "cols": ['824,875,912,954,996,1040,1082'],
        "rows_to_fix": {
            3: ['3 — AGRICULTURE, FORESTRY AND', '3C - Aggregate Sources and Non-CO2',
                '4C - Incineration and Open Burning',
                '4D -  Wastewater Treatment',
                '5A - Indirect N2O emissions from the', 'CO2 from Biomass Combustion',
                ],
        },
    },
    '67_1': {  # 67
        "area": ['70,727,554,159'],
        "cols": ['207,254,291,319,356,400,442,468,503'],
        "rows_to_fix": {
            2: ['2 — INDUSTRIAL PROCESSES', '2A4 Other Process Uses',
                '2B4 Caprolactam, Glyoxal and', '2B8 Petrochemical and',
                ],
            3: ['Total National Emissions',
                ],
        },
    },
    '67_2': {  # 67
        "area": ['666,725,1150,119'],
        "cols": ['801,847,889,915,952,996,1036,1063,1098'],
        "rows_to_fix": {
            2: ['2D - Non-Energy Products from', '2G - Other Product',
                '2G2 SF6 and PFCs from', '2H2 Food and Beverages',
                ],
            3: ['Total National Emissions', '2E1 Integrated Circuit',
                '2F - Product Uses as Substitutes for', '2F1 Refrigeration and',
                ],
        },
    },
    '68_1': {  # 68
        "area": ['66,787,524,217'],
        "cols": ['205,261,315,366,415,473'],
        "rows_to_fix": {
            2: ['2 — INDUSTRIAL PROCESSES', '2A4 Other Process Uses',
                '2B4 Caprolactam, Glyoxal and', '2B8 Petrochemical and',
                ],
            3: ['Total National Emissions',
                ],
        },
    },
    '68_2': {  # 68
        "area": ['666,787,1119,180'],
        "cols": ['808,854,910,961,1017,1066'],
        "rows_to_fix": {
            2: ['2D - Non-Energy Products from',
                '2F - Product Uses as Substitutes for', '2F1 Refrigeration and Air',
                '2G2 SF6 and PFCs from Other', '2H2 Food and Beverages',
                ],
            3: ['Total National Emissions', '2E1 Integrated Circuit or',
                '2G - Other Product Manufacture',
                ],
        },
    },
    '84_1': {  # 84
        "area": ['70,667,525,112'],
        "cols": ['193,291,345,396,440,480'],
        "rows_to_fix": {},
    },
    '84_2': {  # 84
        "area": ['668,667,1115,83'],
        "cols": ['854,908,954,1001,1038,1073'],
        "rows_to_fix": { },
    },
    '85_1': {  # 85
        "area": ['70,680,531,170'],
        "cols": ['275,328,375,414,456,489'],
        "rows_to_fix": {},
    },
    '85_2': {  # 85
        "area": ['663,675,1117,175'],
        "cols": ['849,908,954,1001,1045,1073'],
        "rows_to_fix": {
            3: ['3C — Aggregate Sources and Non-CO2',
                '3C4 - Direct N2O Emissions from', '3C5 - Indirect N2O Emissions from',
                '3C6 - Indirect N2O Emissions from']
        },
    },
    '92': {  # 92
        "area": ['72,672,514,333'],
        "cols": ['228,275,319,361,398,438,489'],
        "rows_to_fix": {
            3: ['4A1 Managed Waste',
                '4A2 Unmanaged Waste', '4A3 Uncategorised Waste',
                '4C - Incineration and', '4D - Wastewater Treatment',
                '4D1 Domestic Wastewater', '4D2 Industrial Wastewater']
        },
    },
    '95_1': {  # 95
        "area": ['70,731,507,149'],
        "cols": ['233,307,375,452'],
        "drop_rows": [0, 1, 2, 3],
        "rows_to_fix": {
            3: ['Total (Net)', '1A2 Manufacturing Industries',
                '2 — INDUSTRIAL PROCESSES', '3 — AGRICULTURE, FORESTRY',
                '3C - Aggregate Sources and Non-CO2', '4C - Incineration and Open',
                'Clinical Waste', '4D - Wastewater Treatment',
                'CO2 from Biomass Combustion for']
        },
        "header": {
            'entity': ['Greenhouse Gas Source and Sink Categories',
                       'Net CO2', 'CH4', 'N2O', 'HFCs'],
            'unit': ['', 'Gg', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq'],
        },
    },
    '95_2': {  # 95
        "area": ['666,731,1103,149'],
        "cols": ['829,903,971,1048'],
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "rows_to_fix": {
            3: ['Total (Net)', '1A2 Manufacturing Industries',
                '2 — INDUSTRIAL PROCESSES', '3 — AGRICULTURE, FORESTRY',
                '3C - Aggregate Sources and Non-CO2', '4C - Incineration and Open',
                'Clinical Waste', '4D - Wastewater Treatment',
                'CO2 from Biomass Combustion for']
        },
        "header": {
            'entity': ['Greenhouse Gas Source and Sink Categories',
                       'PFCs', 'SF6', 'NF3', 'Total (Net) National Emissions'],
            'unit': ['', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq'],
        },
    },
}

table_defs = {
    '66': {
        "templates": ['66_1', '66_2'],
        # "header_rows": [0, 1],
        "header": {
            'entity': ['Greenhouse Gas Source and Sink Categories', 'Net CO2',
                       'CH4', 'N2O', 'HFCs', 'PFCs', 'SF6', 'NF3'],
            'unit': ['', 'Gg', 'Gg', 'Gg', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq', 'GgCO2eq'],
        },
        "drop_rows": [0, 1, 2, 3],
        # "drop_cols": ['NF3', 'SF6'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018",
    },
    '67': {
        "templates": ['67_1', '67_2'],
        "header": {
            'entity': ['Greenhouse Gas Source and Sink Categories', 'HFC-23', 'HFC-32',
                       'HFC-41', 'HFC-125', 'HFC-134a', 'HFC-143a', 'HFC-152a',
                       'HFC-227ea', 'HFC-43-10mee'],
            'unit': ['', 'kg', 'kg', 'kg', 'kg', 'kg', 'kg', 'kg', 'kg', 'kg'],
        },
        "drop_rows": [0, 1, 2, 3],
        # "drop_cols": ['NF3', 'SF6'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018_fgases",
    },
    '68': {
        "templates": ['68_1', '68_2'],
        "header": {
            'entity': ['Greenhouse Gas Source and Sink Categories', 'PFC-14',
                       'PFC-116', 'PFC-218', 'PFC-318', 'SF6', 'NF3'],
            'unit': ['', 'kg', 'kg', 'kg', 'kg', 'kg', 'kg'],
        },
        "drop_rows": [0, 1, 2],
         "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018_fgases",
    },
    '84': {
        "templates": ['84_1', '84_2'],
        "header": {
            'entity': ['Categories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'NMVOC'],
            'unit': ['', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg'],
        },
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "category_col": "Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018",
    },
    '85': {
        "templates": ['85_1', '85_2'],
        "header": {
            'entity': ['Categories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'NMVOC'],
            'unit': ['', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg'],
        },
        "drop_rows": [0, 1, 2, 3, 4, 5],
        "category_col": "Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018",
    },
    '92': {
        "templates": ['92'],
        "header": {
            'entity': ['Categories', 'CO2', 'CH4', 'N2O', 'NOx', 'CO', 'NMVOC', 'SO2'],
            'unit': ['', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg', 'Gg'],
        },
        "drop_rows": [0, 1, 2],
        "category_col": "Categories",
        "year": 2018,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "2018",
    },
    '95': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2016,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
    '96': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2014,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
    '97': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2012,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
    '98': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2010,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
    '99': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 2000,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
    '100': {
        "templates": ['95_1', '95_2'],
        "category_col": "Greenhouse Gas Source and Sink Categories",
        "year": 1994,
        # "unit_info": unit_info_2018,
        "coords_value_mapping": "other",
    },
}

cat_names_fix = {
    '14Ab Residential': '1A4b Residential',
}

values_replacement = {
#    '': '-',
    ' ': '',
}

gwp_to_use = "AR5GWP100"

index_cols = ["orig_cat_name"]
cols_for_space_stripping = index_cols

unit_row = "header"

## parameters part 2: conversion to PRIMAP2 interchnage format

cats_remove = ['Information items']

cat_codes_manual = {
    'CO2 from Biomass Combustion for Energy Production': 'M.BIO',
    'Total National Emissions and Removals': '0',
    'Total (Net) National Emissions': '0',
    'Clinical Waste Incineration': 'M.4.C.1',
    'Hazardous Waste Incineration': 'M.4.C.2',
    #'3 AGRICULTURE': 'M.AG',
    '3 AGRICULTURE, FORESTRY AND OTHER LAND USE': '3',
    #'3 LAND USE, LAND-USE CHANGE AND FORESTRY': 'M.LULUCF',
}


cat_code_regexp = r'(?P<code>^[A-Za-z0-9]{1,7})\s.*'

# special header as category code and name in one column
header_long = ["orig_cat_name", "entity", "unit", "time", "data"]

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP", #two extra categories
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "SGP-GHG-inventory ",
    "provenance": "measured",
    "area": "SGP",
    "scenario": "BUR5"
}

coords_value_mapping = {
    "2018": {
        "unit": "PRIMAP1",
        "entity": {
            'HFCs': f'HFCS ({gwp_to_use})',
            'PFCs': f'PFCS ({gwp_to_use})',
            'CH4': 'CH4',
            'N2O': 'N2O',
            'NF3': f'NF3 ({gwp_to_use})',
            'Net CO2': 'CO2',
            'SF6': f'SF6 ({gwp_to_use})',
            'Total (Net) National Emissions': 'KYOTOGHG (AR5GWP100)',
        },
    },
    "2018_fgases": {
        "unit": "PRIMAP1",
        "entity": {
            'HFC-125': 'HFC125',
            'HFC-134a': 'HFC134a',
            'HFC-143a': 'HFC143a',
            'HFC-152a': 'HFC152a',
            'HFC-227ea': 'HFC227ea',
            'HFC-23': 'HFC23',
            'HFC-32': 'HFC32',
            'HFC-41': 'HFC41',
            'HFC-43-10mee': 'HFC4310mee',
            'NF3': 'NF3',
            'PFC-116': 'C2F6',
            'PFC-14': 'CF4',
            'PFC-218': 'C3F8',
            'PFC-318': 'cC4F8',
            'SF6': 'SF6',
        },
    },
    "other": {
        "unit": "PRIMAP1",
        "entity": {
            'HFCs': f'HFCS ({gwp_to_use})',
            'CH4': f'CH4 ({gwp_to_use})',
            'N2O': f'N2O ({gwp_to_use})',
            'NF3': f'NF3 ({gwp_to_use})',
            'Net CO2': 'CO2',
            'PFCs': f'PFCS ({gwp_to_use})',
            'SF6': f'SF6 ({gwp_to_use})',
            'Total (Net) National Emissions': f'KYOTOGHG ({gwp_to_use})',
        },
    },
}

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit"
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

filter_remove = {
    # "f1" :{
    #     "entity": ["HFC-125", "HFC-134a", "HFC-143a", "HFC-152a", "HFC-227ea",
    #                "HFC-23", "HFC-32", "HFC-41", "HFC-43-10mee", "PFC-116",
    #                "PFC-14", "PFC-218", "PFC-318", "NF3", "SF6"],
    #     "category": "2"
    # }
}

meta_data = {
    "references": "https://unfccc.int/documents/621650",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Singapore's Fifth National Communication and Fifth Biannial Update "
             "Report",
    "comment": "Read fom pdf file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}


## processing
aggregate_sectors = {
    '2': {'sources': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F', '2.G', '2.H'],
          'name': 'IPPU'},
    'M.3.C.1.AG': {'sources': ['3.C.1.b', '3.C.1.c'], 'name': 'Emissions from Biomass Burning (Agriculture)'},
    'M.3.C.1.LU': {'sources': ['3.C.1.a', '3.C.1.d'], 'name': 'Emissions from Biomass Burning (LULUCF)'},
    'M.3.C.AG': {'sources': ['M.3.C.1.AG', '3.C.2', '3.C.3', '3.C.4', '3.C.5',
                             '3.C.6', '3.C.7', '3.C.8'],
                 'name': 'Aggregate sources and non-CO2 emissions sources on land (Agriculture)'},
    'M.AG.ELV': {'sources': ['M.3.C.AG'], 'name': 'Agriculture excluding livestock emissions'},
    'M.AG': {'sources': ['M.AG.ELV', '3.A'], 'name': 'Agriculture'},
    'M.LULUCF': {'sources': ['M.3.C.1.LU', '3.B', '3.D'],
                 'name': 'Land Use, Land Use Change, and Forestry'},
    'M.0.EL': {'sources': ['1', '2', 'M.AG', '4', '5'], 'name': 'National Total Excluding LULUCF'},
    '0': {'sources': ['1', '2', '3', '4', '5'], 'name': 'National Total'},
}


processing_info_step1 = {
    # aggregate IPPU which is missing for individual fgases so it can be used in the
    # next step (downscaling)
    'aggregate_cats': {
        '2': {'sources': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F', '2.G', '2.H'],
              'name': 'IPPU'},
    },
    'tolerance': 1, # because ch4 is inconsistent
}

processing_info_step2 =  {
    'aggregate_cats': aggregate_sectors,
    'downscale': {
        'sectors': {
            'IPPU': {
                'basket': '2',
                'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.E',
                                    '2.F', '2.G', '2.H'],
                'entities': ['CO2', 'N2O', f'PFCS ({gwp_to_use})',
                             f'HFCS ({gwp_to_use})', 'SF6', 'NF3'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            # AFOLU downscaling. Most is zero anyway
            '3C': {
                'basket': '3.C',
                'basket_contents': ['3.C.1', '3.C.2', '3.C.3', '3.C.4', '3.C.5',
                                    '3.C.6', '3.C.7', '3.C.8'],
                'entities': ['CO2', 'CH4', 'N2O'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            '3C1': {
                'basket': '3.C.1',
                'basket_contents': ['3.C.1.a', '3.C.1.b', '3.C.1.c', '3.C.1.d'],
                'entities': ['CO2', 'CH4', 'N2O'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            '3D': {
                'basket': '3.D',
                'basket_contents': ['3.D.1', '3.D.2'],
                'entities': ['CO2', 'CH4', 'N2O'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
        },
        'entities': {
            'HFCS': {
                'basket': f'HFCS ({gwp_to_use})',
                'basket_contents': ['HFC125', 'HFC134a', 'HFC143a', 'HFC23',
                                    'HFC32', 'HFC4310mee', 'HFC227ea'],
                'sel': {'category (IPCC2006_PRIMAP)':
                            ['0', '2', '2.C', '2.E',
                             '2.F', '2.G', '2.H']},
            },
            'PFCS': {
                'basket': f'PFCS ({gwp_to_use})',
                'basket_contents': ['C2F6', 'C3F8', 'CF4', 'cC4F8'],
                'sel': {'category (IPCC2006_PRIMAP)':
                            ['0', '2', '2.C', '2.E',
                             '2.F', '2.G', '2.H']},
            },
        }
    },
    'remove_ts': {
        'fgases': { # unnecessary and complicates aggregation for
            # other gases
            'category': ['5', '5.B'],
            'entities': [f'HFCS ({gwp_to_use})', f'PFCS ({gwp_to_use})', 'SF6', 'NF3'],
        },
        'CH4': { # inconsistent with IPPU sector
            'category': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F', '2.G', '2.H'],
            'entities': ['CH4'],
        },
    },
    # 'basket_copy': {
    #     'GWPs_to_add': ["SARGWP100", "AR4GWP100", "AR6GWP100"],
    #     'entities': ["HFCS", "PFCS"],
    #     'source_GWP': gwp_to_use,
    # },
}



