gwp_to_use = 'AR5GWP100'

tables_trends = {
    '70': { # GHG by main sector
        'page': '70',
        'area': ['177,430,450,142'],
        'cols': ['208,260,311,355,406'],
        'coords_defaults': {
            'unit': 'GgCO2eq',
        },
        'coords_cols': {
            "category": "Year",
            "entity": "entity",
        },
        'copy_cols': {
            # to: from
            'entity': 'Year',
        },
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'AFOLU': '3',
                'Waste': '4',
            },
            'entity': {
                'Total emissions': f'KYOTOGHG emissions ({gwp_to_use})',
                'Energy': f'KYOTOGHG ({gwp_to_use})',
                'IPPU': f'KYOTOGHG ({gwp_to_use})',
                'AFOLU': f'KYOTOGHG emissions ({gwp_to_use})',
                'Waste': f'KYOTOGHG ({gwp_to_use})',
            },
        },
        'label_rows': [0, 1, 2],
    },
    '71': { # main gases by sector
    'page': '71',
        'area': ['82,760,509,454'],
        'cols': ['124,186,249,326,388,454'],
        'coords_defaults': {
            'category': '0',
            'unit': 'GgCO2eq',
        },
        'coords_cols': {
            "entity": "Year",
        },
        'remove_cols': [],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'entity': {
                'Total GHG emissions (CO₂-eq)': f'KYOTOGHG emissions ({gwp_to_use})',
                'Removals (CO₂) (CO₂-eq)': 'CO2 removals',
                'Net emissions (CO₂-eq)': f'KYOTOGHG ({gwp_to_use})',
                'CO₂ (Gg)': 'CO2 emissions',
                'CH₄ (CO₂-eq)': f'CH4 ({gwp_to_use})',
                'N₂O (CO₂-eq)': f'N2O ({gwp_to_use})',
            },
        },
        'label_rows':  [0, 1, 2, 3, 4],
    },
    '72_1': { # CO2 by main sector
    'page': '72',
        'area': ['122,760,496,472'],
        'cols': ['159,212,265,311,355,406,456'],
        'coords_defaults': {
            #'entity': 'CO2',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
            'entity': 'entity',
        },
        'remove_cols': ['Total emissions'],
        'copy_cols': {
            # to: from
            'entity': 'Year',
        },
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total net emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'AFOLU - emissions': '3',
                'AFOLU - removals': '3',
                'Waste': '4',
            },
            'entity': {
                'Total net emissions': 'CO2',
                'Energy': 'CO2',
                'IPPU': 'CO2',
                'AFOLU - emissions': 'CO2 emissions',
                'AFOLU - removals': 'CO2 removals',
                'Waste': 'CO2',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '72_2': { # CH4 by sector
    'page': '72',
        'area': ['133,333,483,41'],
        'cols': ['172,230,280,333,384,439'],
        'coords_defaults': {
            'entity': 'CH4',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        'remove_cols': ['Total (Gg CO₂-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total': '0',
                'Energy': '1',
                'IPPU': '2',
                'AFOLU - emissions': '3',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '73': { # N2O by sector
    'page': '73',
        'area': ['155,666,643,364'],
        'cols': ['194,265,309,366,419'],
        'coords_defaults': {
            'entity': 'N2O',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        'remove_cols': ['Total emissions (Gg CO₂-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total': '0',
                'Energy': '1',
                'AFOLU': '3',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '74': { # NOx by sector
    'page': '74',
        'area': ['148,457,467,166'],
        'cols': ['190,254,304,359,421'],
        'coords_defaults': {
            'entity': 'NOX',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        #'remove_cols': [],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'AFOLU': '3',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '75': { # CO by sector
    'page': '75',
        'area': ['161,763,456,472'],
        'cols': ['199,256,307,359,410'],
        'coords_defaults': {
            'entity': 'CO',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        #'remove_cols': ['Total emissions (Gg CO2-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'AFOLU': '3',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '75_2': { # NMVOC by sector
    'page': '75',
        'area': ['177,325,441,50'],
        'cols': ['219,287,340,395'],
        'coords_defaults': {
            'entity': 'NMVOC',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        #'remove_cols': ['Total emissions (Gg CO2-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '76_1': { # NMVOC by sector
    'page': '76',
        'area': ['175,782,448,675'],
        'cols': ['216,282,340,390'],
        'coords_defaults': {
            'entity': 'NMVOC',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        #'remove_cols': ['Total emissions (Gg CO2-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'IPPU': '2',
                'Waste': '4',
            },
        },
        'label_rows':  [0, 1, 2],
    },
    '76_2': { # SO2 by sector
    'page': '76',
        'area': ['197,562,421,226'],
        'cols': ['243,331,381'],
        'coords_defaults': {
            'entity': 'SO2',
            'unit': 'Gg',
        },
        'coords_cols': {
            "category": "Year",
        },
        #'remove_cols': ['Total emissions (Gg CO2-eq)'],
        'coords_value_mapping': {
            "unit": "PRIMAP1",
            'category': {
                'Total emissions': '0',
                'Energy': '1',
                'Waste': '4',
            },
        },
        'label_rows':  [0],
    },
}

pages_inventory = {
    '78': 1,
    '79': 0,
    '80': 0,
    '81': 0,
    '82': 0,
}

year_inventory = 2017
entity_row = 1
unit_row = 0


###
index_cols = "Categories"
units_inv = {
    'Emissions (Gg)': 'Gg',
    'Emissions CO2 Equivalents (Gg)': 'GgCO2eq',
}
# special header as category UNFCCC_GHG_data and name in one column
header_long = ["category", "entity", "unit", "time", "data"]


# manual category codes
cat_codes_manual = {
    'Total National Emissions and Removals': '0',
    'International Bunkers': 'M.BK',
}

cat_code_regexp = r'(?P<code>^[a-zA-Z0-9\.]{1,9})\s.*'

coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

# add_coords_cols = {
#     "orig_cat_name": ["orig_cat_name", "category"],
# }

coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "NGA-GHG-Inventory",
    "provenance": "measured",
    "area": "NGA",
    "scenario": "BUR2",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": "PRIMAP1",
    "entity": {
        'Net CO2 (1)(2)': 'CO2',
        'CH4': "CH4",
        'N2O': "N2O",
        'HFCs': f"HFCS ({gwp_to_use})",
        'PFCs': f"PFCS ({gwp_to_use})",
        'SF6': f"SF6 ({gwp_to_use})",
        #'NOx': 'NOX',
        'CO': 'CO', # no mapping, just added for completeness here
        'NMVOCs': 'NMVOC',
        'SO2': 'SO2', # no mapping, just added for completeness here
        'Other halogenated gases with CO2 eq conversion factors (3)':
            f"UnspMixOfHFCs ({gwp_to_use})",
    },
}


filter_remove = {
    'f1': {
        'entity': ['Other halogenated gases without CO2 eq conversion factors (4)']
    },
    'f2': {
        'category': 'Memo'
    },
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/307085",
    "rights": "",
    "contact": "mail@johannes-guestchow.de",
    "title": "Nigeria. Second Biennial Update Report (BUR2) to the United Nations "
             "Framework Convention on Climate Change",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

# convert to mass units where possible
entities_to_convert_to_mass = [
    'CH4', 'N2O', 'SF6'
]

# CO2 equivalents don't make sense for these substances, so unit has to be Gg instead of Gg CO2 equivalents as indicated in the table
entities_to_fix_unit = [
    'NOx', 'CO', 'NMVOCs', 'SO2'
]

### processing

processing_info_step1 = {
    'aggregate_cats': {
        '2.F': {'sources': ['2.F.2', '2.F.6'], # all 0, but for completeness
              'name': 'Product uses as Substitutes for Ozone Depleting Substances'},
        '2': {'sources': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F', '2.G'],
              'name': 'IPPU'}, # for HFCs, PFCs, SO2, SF6, N2O (all 0)
    },
}

processing_info_step2 =  {
    'aggregate_cats': {
        'M.AG.ELV': {'sources': ['3.C'], 'name': 'Agriculture excluding livestock emissions'},
        'M.AG': {'sources': ['M.AG.ELV', '3.A'], 'name': 'Agriculture'},
        'M.LULUCF': {'sources': ['3.B', '3.D'],
                     'name': 'Land Use, Land Use Change, and Forestry'},
        'M.0.EL': {'sources': ['1', '2', 'M.AG', '4', '5'], 'name': 'National Total Excluding LULUCF'},
        '0': {'sources': ['1', '2', '3', '4', '5'], 'name': 'National Total'},
    },
    'downscale': {
        'sectors': {
            '1': {
                'basket': '1',
                'basket_contents': ['1.A', '1.B', '1.C'],
                'entities': ['CO2', 'N2O', 'CH4'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            '1.A': {
                'basket': '1.A',
                'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                'entities': ['CO2', 'N2O', 'CH4'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            '1.B': {
                'basket': '1.B',
                'basket_contents': ['1.B.1', '1.B.2', '1.B.3'],
                'entities': ['CO2', 'N2O', 'CH4'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            'IPPU': {
                'basket': '2',
                'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.E',
                                    '2.F', '2.G', '2.H'],
                'entities': ['CO2', 'N2O', 'CH4'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            '3': {
                'basket': '3',
                'basket_contents': ['3.A', '3.B', '3.C', '3.D'],
                'entities': ['CO2', 'CH4', 'N2O'],
                'dim': 'category (IPCC2006_PRIMAP)',
            },
            # '3A': {
            #     'basket': '3.A',
            #     'basket_contents': ['3.A.1', '3.A.2'],
            #     'entities': ['CH4', 'N2O'],
            #     'dim': 'category (IPCC2006_PRIMAP)',
            # },
            # '3C': {
            #     'basket': '3.C',
            #     'basket_contents': ['3.C.1', '3.C.2', '3.C.3', '3.C.4', '3.C.5',
            #                         '3.C.6', '3.C.7', '3.C.8'],
            #     'entities': ['CO2', 'CH4', 'N2O'],
            #     'dim': 'category (IPCC2006_PRIMAP)',
            # },
            # '3D': {
            #     'basket': '3.D',
            #     'basket_contents': ['3.D.1', '3.D.2'],
            #     'entities': ['CO2', 'CH4', 'N2O'],
            #     'dim': 'category (IPCC2006_PRIMAP)',
            # },
        },
    },
    'remove_ts': {
        'fgases': { # unnecessary and complicates aggregation for
            # other gases
            'category': ['5'],
            'entities': [f'HFCS ({gwp_to_use})', f'PFCS ({gwp_to_use})', 'SF6',
                         f'UnspMixOfHFCs ({gwp_to_use})'],
        },
    },
    'basket_copy': {
        'GWPs_to_add': ["SARGWP100", "AR4GWP100", "AR6GWP100"],
        'entities': ["HFCS", "PFCS", "UnspMixOfHFCs"],
        'source_GWP': gwp_to_use,
    },
}
