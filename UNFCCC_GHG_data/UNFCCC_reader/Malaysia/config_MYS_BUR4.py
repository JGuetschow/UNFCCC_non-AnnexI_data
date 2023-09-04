import pandas as pd
gwp_to_use = "AR4GWP100"


cat_names_fix = {
    #'2A3 Glass Prod.': '2A3 Glass Production',
    #'2F6 Other Applications': '2F6 Other Applications (please specify)',
    #'3A2 Manure Mngmt': '3A2 Manure Mngmt.',
    #'3C7 Rice Cultivations': '3C7 Rice Cultivation',
}

values_replacement = {
    '': '-',
    ' ': '-',
}

cols_for_space_stripping = ["Categories"]

index_cols = ["Categories", "entity", "unit"]

# parameters part 2: conversion to interchange format
cats_remove = ['Memo items', 'Information items',  'Information items (1)']

cat_codes_manual = {
    'Annual change in long-term storage of carbon in HWP waste': 'M.LTS.AC.HWP',
    'Annual change in total long-term storage of carbon stored': 'M.LTS.AC.TOT',
    'CO2 captured': 'M.CCS',
    'CO2 from Biomass Burning for Energy Production': 'M.BIO',
    'For domestic storage': 'M.CCS.DOM',
    'For storage in other countries': 'M.CCS.OCT',
    'International Aviation (International Bunkers)': 'M.BK.A',
    'International Bunkers': 'M.BK',
    'International Water-borne Transport (International Bunkers)': 'M.BK.M',
    'Long-term storage of carbon in waste disposal sites': 'M.LTS.WASTE',
    'Multilateral Operations': 'M.MULTIOP',
    'Other (please specify)': 'M.OTHER',
    'Total National Emissions and Removals': '0',
}

cat_code_regexp = r'(?P<code>^[A-Z0-9]{1,4})\s.*'


coords_terminologies = {
    "area": "ISO3",
    "category": "IPCC2006_PRIMAP",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "MYS-GHG-inventory",
    "provenance": "measured",
    "area": "MYS",
    "scenario": "BUR4"
}

coords_value_mapping = {
}

coords_cols = {
    "category": "Categories",
    "entity": "entity",
    "unit": "unit"
}

add_coords_cols = {
    "orig_cat_name": ["orig_cat_name", "category"],
}

#filter_remove = {
#    "f1": {
#        "entity": ["CO2(grossemissions)", "CO2(removals)"],
#    },
#}

meta_data = {
    "references": "https://unfccc.int/documents/624776",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Malaysia - Fourth Biennial Update Report under the UNFCCC",
    "comment": "Read fom pdf file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}

terminology_proc = coords_terminologies["category"]

table_def_templates = {
    # CO2
    '203': {  # 203, 249
        "area": ['70,480,768,169'],
    },
    '204': {  # 204
        "area": ['70,500,763,141'],
    },
    '205': {  # 205, 209, 2014, 2018
        "area": ['70,495,763,95'],
        "rows_to_fix": {
            2: ['5A Indirect N2O emissions from the atmospheric deposition of'],
        },
    },
    '206': {  # 206
        "area": ['70,495,763,353'],
    },
    '207': {  # 207, 208, 211, 212, 213, 215, 217, 223, 227, 231,
        # 251, 257, 259, 263, 265
        "area": ['70,495,763,95'],
    },
    '216': {  #  216
        "area": ['70,500,763,95'],
    },
    # CH4
    '219': {  # 219, 255
        "area": ['70,480,768,100'],
    },
    '220': {  # 220, 224, 228
        "area": ['70,495,763,95'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '221': {  # 221
        "area": ['92,508,748,92'],
        "cols": ['298,340,380,422,462,502,542,582,622,662,702'],
        "rows_to_fix": {
            3: ['3C Aggregate sources and Non-CO2 emissions'],
            2: ['5A Indirect N2O emissions from the atmospheric'],
        },
    },
    '222': {  # 222
        "area": ['70,495,763,323'],
        "rows_to_fix": {
            2: ['Annual change in long-term storage of carbon in HWP'],
        },
    },
    '225': {  # 225
        "area": ['92,508,748,92'],
        "cols": ['311,357,400,443,486,529,572,615,658,701'],
        "rows_to_fix": {
            3: ['3C Aggregate sources and Non-CO2 emissions'],
        },
    },
    '226': {  # 226, 230
        "area": ['70,495,763,95'],
        "rows_to_fix": {
            2: ['5A Indirect N2O emissions from the atmospheric',
                'Annual change in long-term storage of carbon in HWP'],
        },
    },
    '229': {  # 229
        "area": ['114,508,725,92'],
        "cols": ['333,379,421,464,506,548,590,632,674'],
        "rows_to_fix": {
            3: ['3C Aggregate sources and Non-CO2 emissions'],
        },
    },
    # N2O
    '232': {  # 232
        "area": ['70,495,763,95'],
        "cols": ['315,366,416,466,516,566,616,666,716'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '233': {  # 233
        "area": ['70,495,763,95'],
        "rows_to_fix": {
            3: ['3C Aggregate sources and Non-CO2 emissions'],
        },
    },
    '234': {  # 234
        "area": ['70,495,763,95'],
        "rows_to_fix": {
            3: ['International Water-borne Transport (International'],
        },
    },
    '236': {  # 236
        "area": ['70,495,763,95'],
        "cols": ['298,344,392,439,487,534,580,629,675,721'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '240': {  # 240
        "area": ['70,495,763,95'],
        "cols": ['283,329,372,416,459,504,550,594,639,682,726'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    # HFCs
    '243': {  # 243
        "area": ['70,480,763,95'],
        "cols": ['408,449,489,527,567,604,644,681,721'],
    },
    '244': {  # 244
        "area": ['70,495,763,95'],
        "cols": ['408,449,489,527,567,604,644,681,721'],
    },
    '245': {  # 245, 246
        "area": ['70,495,763,95'],
        "cols": ['405,442,478,515,550,587,621,657,693,729'],
    },
    '247': {  # 247, 248
        "area": ['70,495,763,95'],
        "cols": ['384,426,459,493,531,564,597,633,666,700,735'],
    },
    # PFCs
    '250': {  # 250
        "area": ['70,495,763,95'],
        "cols": ['341,389,436,485,531,579,626,674,723'],
    },
    '252': {  # 252
        "area": ['70,495,763,95'],
        "cols": ['323,370,415,459,504,547,590,636,680,726'],
    },
    '253': {  # 253
        "area": ['70,495,763,95'],
        "cols": ['334,378,419,464,511,554,597,636,668,702,735'],
    },
    '254': {  # 254
        "area": ['70,495,763,95'],
        "cols": ['330,378,419,464,511,554,597,636,668,702,735'],
        "rows_to_fix": {
            -3: ['2F Product Uses as Substitutes for Ozone Depleting Substances'],
        },
    },
    # SF6
    '256': {  # 256
        "area": ['70,495,763,95'],
        "cols": ['382,420,462,504,546,588,630,672,714'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '258': {  # 258
        "area": ['70,495,763,95'],
        "cols": ['363,399,441,481,522,564,606,646,688,728'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '260': {  # 260
        "area": ['70,495,763,95'],
        "cols": ['346,381,419,458,498,536,576,614,652,692,732'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    # NF3
    '261': {  # 261
        "area": ['70,490,768,100'],
        "cols": ['364,412,454,496,538,581,623,667,710'],
    },
    '262': {  # 262
        "area": ['70,495,763,95'],
        "cols": ['376,420,462,504,545,591,633,676,718'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '264': {  # 264
        "area": ['70,495,763,95'],
        "cols": ['370,415,451,491,530,569,609,651,689,729'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
    '266': {  # 266
        "area": ['70,495,763,95'],
        "cols": ['355,392,430,467,505,544,580,619,656,695,732'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone Depleting'],
        },
    },
}

table_defs = {
    '203': {"template": '203', "entity": "CO2", "unit": "Gg CO2 / yr"},  # CO2
    '204': {"template": '204', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '205': {"template": '205', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '206': {"template": '206', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '207': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '208': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '209': {"template": '205', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '210': {"template": '206', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '211': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '212': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '213': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '214': {"template": '205', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '215': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '216': {"template": '216', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '217': {"template": '207', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '218': {"template": '205', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '219': {"template": '219', "entity": "CH4", "unit": "Gg CH4 / yr"},  # CH4
    '220': {"template": '220', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '221': {"template": '221', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '222': {"template": '222', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '223': {"template": '207', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '224': {"template": '220', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '225': {"template": '225', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '226': {"template": '226', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '227': {"template": '207', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '228': {"template": '220', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '229': {"template": '229', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '230': {"template": '226', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '231': {"template": '207', "entity": "N2O", "unit": "Gg N2O / yr"},  # N2O
    '232': {"template": '232', "entity": "N2O", "unit": "Gg N2O / yr"},
    '233': {"template": '233', "entity": "N2O", "unit": "Gg N2O / yr"},
    '234': {"template": '234', "entity": "N2O", "unit": "Gg N2O / yr"},
    '235': {"template": '207', "entity": "N2O", "unit": "Gg N2O / yr"},
    '236': {"template": '236', "entity": "N2O", "unit": "Gg N2O / yr"},
    '237': {"template": '233', "entity": "N2O", "unit": "Gg N2O / yr"},
    '238': {"template": '234', "entity": "N2O", "unit": "Gg N2O / yr"},
    '239': {"template": '207', "entity": "N2O", "unit": "Gg N2O / yr"},
    '240': {"template": '240', "entity": "N2O", "unit": "Gg N2O / yr"},
    '241': {"template": '233', "entity": "N2O", "unit": "Gg N2O / yr"},
    '242': {"template": '234', "entity": "N2O", "unit": "Gg N2O / yr"},
    '243': {"template": '243', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},  # HFCs
    '244': {"template": '244', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '245': {"template": '245', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '246': {"template": '245', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '247': {"template": '247', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '248': {"template": '247', "entity": f"HFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '249': {"template": '203', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},  # PFCs
    '250': {"template": '250', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '251': {"template": '207', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '252': {"template": '252', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '253': {"template": '253', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '254': {"template": '254', "entity": f"PFCS ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '255': {"template": '219', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},  # SF6
    '256': {"template": '256', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '257': {"template": '207', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '258': {"template": '258', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '259': {"template": '207', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '260': {"template": '260', "entity": f"SF6 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '261': {"template": '261', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},  # NF3
    '262': {"template": '262', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '263': {"template": '207', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '264': {"template": '264', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '265': {"template": '207', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
    '266': {"template": '266', "entity": f"NF3 ({gwp_to_use})",
            "unit": "Gg CO2 / yr"},
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
        'M.0.EL': {'sources': ['1', '2', 'M.AG', '4', '5'],
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