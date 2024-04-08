# primap2 format conversion
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_defaults = {
    "source": "GIN-GHG-Inventory",
    "provenance": "measured",
    "area": "GIN",
    "scenario": "BUR1",
}

coords_terminologies = {
    "area": "ISO3",
    # TODO check if this is correct
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

# gwp conversion is mentioned on page 20 in the report
gwp_to_use = "AR4GWP100"
coords_value_mapping = {
    'main' : {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            'HFCs': f"HFCS ({gwp_to_use})",
            'PFCs': f"PFCS ({gwp_to_use})",
            'SF6' : f"SF6 ({gwp_to_use})",
            'NMVOCs': 'NMVOC',
        }
    },
    'energy' : {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            'NMVOCs': 'NMVOC',
        }
    },
    'lulucf' : {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            'NMVOCs': 'NMVOC',
        }
    },
    'waste' : {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            'NMVOCs': 'NMVOC',
        }
    },
    'trend' : {
        "unit": "PRIMAP1",
        "category": "PRIMAP1",
        "entity": {
            'NMVOCs': 'NMVOC',
        }
    },
}

# TODO! Don't add MEMO if remove later
filter_remove = {
    'f_memo': {"category": "MEMO"},
}

meta_data = {
    "references": "https://unfccc.int/documents/629549",
    "rights": "", # unknown
    "contact": "daniel-busch@climate-resource.de",
    "title": "Guinea. Biennial update report (BUR). BUR1",
    "comment": "Read fom pdf by Daniel Busch",
    "institution": "UNFCCC",
}

page_def_templates = {
    '110': {
        "area": ['36,718,589,87'],
        "cols": ['290,340,368,392,425,445,465,497,535,564'],
    },
    '111': {
        "area": ['36,736,587,107'],
        "cols": ['293,335,369,399,424,445,468,497,535,565'],
    },
    '112': {
        "area": ['35,733,588,106'],
        "cols": ['293,335,369,399,424,445,468,497,535,565'],
    },
    '113': {
        "area": ['35,733,588,106'],
        "cols": ['293,335,365,399,424,445,468,497,535,565'],
    },
    '131' : {
                "area": ['36,718,590,83'],
                "cols": ['293,332,370,406,442,480,516,554'],
            },
}


# for main table
header_inventory = ['Greenhouse gas source and sink categories',
                   'CO2', 'CH4', "N2O", 'HFCs', 'PFCs', 'SF6', 'NOx', 'CO', 'NMVOCs','SO2'
                   ]

unit_inventory = ['-'] + ['Gg'] * len(header_inventory) # one extra for the category columns
unit_inventory[4] = "GgCO2eq"
unit_inventory[5] = "GgCO2eq"
unit_inventory[6] = "GgCO2eq"

# for energy tables
header_energy = ['Greenhouse gas source and sink categories',
                   'CO2', 'CH4', "N2O", 'NOx', 'CO', 'NMVOCs','SO2'
                ]
unit_energy = ['-'] + ['Gg'] * len(header_energy) # one extra for the category columns

# for lulucf tables
header_lulucf = ['Greenhouse gas source and sink categories', 'CO2', 'CH4', "N2O", 'NOx', 'CO', 'NMVOCs']
unit_lulucf = ['-'] + ['Gg'] * (len(header_lulucf) - 1)

# for waste table
header_waste = ['Greenhouse gas source and sink categories', 'CO2', 'CH4', "N2O", 'NOx', 'CO', 'NMVOCs', 'SO2']
unit_waste = ['-'] + ['Gg'] * (len(header_waste) - 1)

# for trend table (unit is always Gg for this table)
header_trend = ['data1990', 'data1995', "data2000", 'data2005', 'data2010', 'data2015', 'data2018', 'data2019']


# define config dict
inv_conf = {
    'header': header_inventory,
    'unit': unit_inventory,
    'header_energy' : header_energy,
    'unit_energy' : unit_energy,
    'header_lulucf' : header_lulucf,
    'unit_lulucf' : unit_lulucf,
    'header_waste' : header_waste,
    'unit_waste' : unit_waste,
    'header_trend' : header_trend,
    'entity_row': 0,
    'unit_row': 1,
    'index_cols': "Greenhouse gas source and sink categories",
    'year': {'110' : 1990,
             '111' : 2000,
             '112' : 2010,
             '113' : 2019,
             '116' : 1990,
             '117' : 2000,
             '118' : 2010,
             '119' : 2019,
             '124' : 1990,
             '125' : 2000,
             '126' : 2010,
             '127' : 2019,
            },
    'header_long': ["orig_cat_name", "entity", "unit", "time", "data"],
    "cat_code_regexp" : r'^(?P<code>[a-zA-Z0-9\.]{1,11})[\s\.].*',
    "cat_codes_manual" : {
        'main' : {
            'Éléments pour mémoire': 'MEMO',
            'Soutes internationales': 'M.BK',
            '1.A.3.a.i - Aviation internationale (soutes internationales)': 'M.BK.A',
            '1.A.3.d.i - Navigation internationale (soutes internationales)' : 'M.BK.M',
            '1.A.5.c - Opérations multilatérales' : 'M.MULTIOP',
            'Total des émissions et absorptions nationales': "0",
            '2A5: Autre': '2A5',
        },
        'energy' : {
            'International Bunkers': 'M.BK',
            '1.A.3.a.i - Aviation internationale (soutes internationales)': 'M.BK.A',
            '1.A.3.d.i - Navigation internationale (soutes internationales)' : 'M.BK.M',
            '1.A.5.c - Opérations multilatérales' : 'M.MULTIOP',
        },
        'trend': {
            'Total des émissions et absorptions nationales' : "0",
            '2A5: Autre' : '2A5',
            'Éléments pour mémoire' : 'MEMO',
            'Soutes internationales' : 'M.BK',
            '1.A.3.a.i - Aviation internationale (soutes internationales)' : 'M.BK.A',
            '1.A.3.d.i - Navigation internationale (soutes internationales)' : 'M.BK.M',
            '1.A.5.c - Opérations multilatérales' : 'M.MULTIOP',
        },
    },
}

country_processing_step1 = {
    'aggregate_cats': {
        'M.3.C.AG': {'sources': ['3.C.1', '3.C.2', '3.C.3', '3.C.4', '3.C.5',
                                 '3.C.6', '3.C.7', '3.C.8'],
                     'name': 'Aggregate sources and non-CO2 emissions sources on land '
                             '(Agriculture)'},
        'M.3.D.AG': {'sources': ['3.D.2'],
                     'name': 'Other (Agriculture)'},
        'M.AG.ELV': {'sources': ['M.3.C.AG', 'M.3.D.AG'],
                     'name': 'Agriculture excluding livestock'},
        'M.AG': {'sources': ['3.A', 'M.AG.ELV'],
                     'name': 'Agriculture'},
        'M.3.D.LU': {'sources': ['3.D.1'],
                     'name': 'Other (LULUCF)'},
        'M.LULUCF': {'sources': ['3.B', 'M.3.D.LU'],
                     'name': 'LULUCF'},
        'M.0.EL': {'sources': ['1', '2', 'M.AG', '4'],
                     'name': 'National total emissions excluding LULUCF'},
    },
    'basket_copy': {
        'GWPs_to_add': ["SARGWP100", "AR5GWP100", "AR6GWP100"],
        'entities': ["HFCS", "PFCS"],
        'source_GWP': gwp_to_use,
    },
}

gas_baskets = {
    'FGASES (SARGWP100)': ['HFCS (SARGWP100)', 'PFCS (SARGWP100)', 'SF6', 'NF3'],
    'FGASES (AR4GWP100)': ['HFCS (AR4GWP100)', 'PFCS (AR4GWP100)', 'SF6', 'NF3'],
    'FGASES (AR5GWP100)':['HFCS (AR5GWP100)', 'PFCS (AR5GWP100)', 'SF6', 'NF3'],
    'FGASES (AR6GWP100)':['HFCS (AR6GWP100)', 'PFCS (AR6GWP100)', 'SF6', 'NF3'],
    'KYOTOGHG (SARGWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (SARGWP100)'],
    'KYOTOGHG (AR4GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR4GWP100)'],
    'KYOTOGHG (AR5GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR5GWP100)'],
    'KYOTOGHG (AR6GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR6GWP100)'],
}