#### configuration for trend tables
import locale
gwp_to_use = 'SARGWP100'
terminology_proc = 'IPCC2006_PRIMAP'
# bunkers [0,1] need different specs
trend_table_def = {
    # only GHG read, rest dropped
    'GHG': {
        'tables': [2],
        'cols_add': {
            'unit': 'ktCO2eq',
            'category': '0',
        },
        'given_col': 'entity',
        'take_only': ['Total GHG'],
    },
    'CO2': {
        'tables': [3],
        'cols_add': {
            'unit': 'kt',
            'entity': 'CO2',
        },
        'given_col': 'category',
    },
    'CH4': {
        'tables': [5],
        'cols_add': {
            'unit': 'kt',
            'entity': 'CH4',
        },
        'given_col': 'category',
        'take_only': [
            'Total emissions', 'From fuel combustion',
            'From Industrial processes', 'From Agriculture'
        ], # ignore the waste time series as they don't cover the full sector
        # and lead to problems becaus eof the methodology chnage in the inventory
    },
    'N2O': {
        'tables': [6],
        'cols_add': {
            'unit': 'kt',
            'entity': 'N2O',
        },
        'given_col': 'category',
    },
    'FGases': {
        'tables': [7],
        'cols_add': {
            'unit': 'ktCO2eq',
            'category': '0',
        },
        'given_col': 'entity',
    },
}

#### configuration for inventory tables
inv_tab_conf = {
    'unit_row': 0,
    'entity_row': 0,
    'regex_unit': r"\((.*)\)",
    'regex_entity': r"^(.*)\s\(",
    'index_cols': 'category',
    'cat_pos': (0, 0),
    'header_long': ["category", "entity", "unit", "time", "data"],
    'header_2010': ["2010", "CO2 emissions (Gg)", "CO2 removals (Gg)",
                  "CH4 (Gg)", "N2O (Gg)", "CO (Gg)", "NOx (Gg)",
                  "NMVOCs (Gg)", "SOx (Gg)", "SF6 (CO2eq Gg)",
                  "HFCs (CO2eq Gg)", "PFCs (CO2eq Gg)"],
    'unit_repl': {
        "SF6 (CO2e Gg)": "GgCO2eq",
        "HFCs (CO2eGg)": "GgCO2eq",
        "PFCs (CO2e Gg)": "GgCO2eq",
        "SF6 (CO2eq Gg)": "GgCO2eq",
        "HFCs (CO2eq Gg)": "GgCO2eq",
        "PFCs (CO2eq Gg)": "GgCO2eq",
    },
}

inv_table_def = {
    '1996': {'tables': [1, 2]},
    '2000': {'tables': [3, 4]},
    '2005': {'tables': [5, 6]},
    '2010': {'tables': [7, 8]},
    '2015': {'tables': [9, 10, 11]},
    '2019': {'tables': [12, 13, 14]},
    '2020': {'tables': [15, 16]},
}

#### configuration for PM2 format
coords_cols = {
    "category": "category",
    "entity": "entity",
    "unit": "unit",
}

coords_terminologies = {
    "area": "ISO3",
    "category": "BURDI_ISRBUR2",
    "scenario": "PRIMAP",
}

coords_defaults = {
    "source": "ISR-GHG-Inventory",
    "provenance": "measured",
    "area": "ISR",
    "scenario": "BUR2",
}

coords_value_mapping = {
    "unit": "PRIMAP1",
    "category": {
        'Total national emissions and removals': '24540',
        '0': '24540', # no mapping, just for completeness
        'Total emissions and removals': '24540',
        'Total emissions': '24540',
        '1. Energy': '1',
        'A. Fuel combustion (sectoral approach)': '1.A',
        'A. From fuel combustion': '1.A',
        'From fuel combustion': '1.A',
        '1. Energy industries': '1.A.1',
        '2. Manufacturing industries and construction': '1.A.2',
        '2. Manufacturing, industries and construction': '1.A.2',
        '3. Transport': '1.A.3',
        '4. Other sectors': '1.A.4',
        '4. Other': '1.A.4',
        'Commercial, institutional residential sectors': '1.A.4.ab', # not BURDI
        'Commercial, institutional': '1.A.4.a', #not BURDI
        'residential sectors': '1.A.4.b', #not BURDI
        'Agriculture, forestry and fishing': '1.A.4.c', # not BURDI
        '5. Other (please specify)': '1.A.5',
        'B. Fugitive emissions from fuels': '1.B',
        '1. Solid fuels': '1.B.1',
        '2. Oil and natural gas': '1.B.2',
        '2. Industrial processes': '2',
        'B. industrial processes': '2',
        'From Industrial processes': '2',
        'A. Mineral products': '2.A',
        'CEMENT PRODUCTION': '2.A.1',
        'PRODUCTION OF LIME': '2.A.2',
        'SODA ASH USE': '2.A.4.b',
        'ROAD PAVING WITH ASPHALT': '2.A.6',
        'Container Glass': '2.A.7.a',
        'B. Chemical industry': '2.B',
        'NITRIC ACID PRODUCTION': '2.B.2',
        'Ethylene': '2.B.5.b',
        'PRODUCTION OF OTHER CHEMICALS': '2.B.5.g', #not BURDI
        'Sulphuric Acid': '2.B.5.f', #not BURDI
        'C. Metal production': '2.C',
        'D. Other production': '2.D',
        'E. Production of halocarbons and sulphur hexafluoride': '2.E',
        'F. Consumption of halocarbons and sulphur hexafluoride': '2.F',
        'G. Other (IPPU)': '2.G',
        '3. Solvent and other product use': '3',
        '4. Agriculture': '4',
        'From Agriculture': '4',
        'From agriculture': '4',
        'A. Enteric fermentation': '4.A',
        'B. Manure management': '4.B',
        'C. Rice cultivation': '4.C',
        'D. Agricultural soils': '4.D',
        'E. Prescribed burning of savannahs': '4.E',
        'F. Field burning of agricultural residues': '4.F',
        'G. Other (Agri)': '4.G',
        '5. Land-use change and forestry': '5',
        'C. Land-use change and forestry': '5',
        'A. Changes in forest and other woody biomass stocks': '5.A',
        '2. Changes in forest and other woody biomass stocks': '5.A',
        'B. Forest and grassland conversion': '5.B',
        'C. Abandonment of managed lands': '5.C',
        'D. CO2 emissions and removals from soil': '5.D',
        '1. CO2 emissions and removals from soil': '5.D',
        'E. Other (LULUCF)': '5.E',
        # waste in 2006 categories, not BURDI as we will lose info of we map to BURDI and back
        '6. Waste': '6',
        'A. Solid waste disposal on land': '6.A',
        'From solid waste disposal on land': '6.A',
        'B. Waste-water handling': '6X.B', # combine with 6.D
        'From waste-water treatment': '6X.B', # not BURDI
        'C. Waste incineration': '6.C',
        'D. Other (please specify)': '6X.D', # combine with 6.E
        'B. Biological Treatment of Solid Waste': '6.B', # not BURDI
        'D.Waste-water handling': '6.D', # not BURDI
        'D. Waste-water handling': '6.D', # not BURDI
        'E. Other (Waste)': '6.E', # not BURDI
        '7. Other (please specify)': '7',
        'International bunkers': '14637',
        'Aviation': '14424',
        'Marine': '14423',
        'CO2 emissions from biomass': '14638',
    },
    "entity": {
        'Total GHG': f'KYOTOGHG ({gwp_to_use})',
        'Carbon Dioxide (CO2)': 'CO2',
        'CO2': 'CO2', # no mapping, just added for completeness here
        'CO2 emissions': 'CO2 emissions', # no mapping, just added for completeness here
        'CO2 removals': 'CO2 removals', # no mapping, just added for completeness here
        'CO2 Emissions': 'CO2 emissions',
        'CO2 Removals': 'CO2 removals',
        'Methane (CH4)': 'CH4',
        'CH4': 'CH4', # no mapping, just added for completeness here
        'Nitrous Oxides (N2O)': 'N2O',
        'NO2': 'NO2', # no mapping, just added for completeness here
        'Sulfur hexafluoride (SF6)': f'SF6 ({gwp_to_use})',
        'SF6': f'SF6 ({gwp_to_use})',
        "Hydrofluorocarbons (HFC'S)": f'HFCS ({gwp_to_use})',
        "HFCs": f'HFCS ({gwp_to_use})',
        "Perfluorocarbons (PFC'S)": f'PFCS ({gwp_to_use})',
        "PFCs": f'PFCS ({gwp_to_use})',
        'NOx': 'NOX',
        'Nox': 'NOX',
        'Co': 'CO',
        'CO': 'CO', # no mapping, just added for completeness here
        'NMVOCs': 'NMVOC',
        'SOx': 'SOX', # no mapping, just added for completeness here
    },
}

filter_remove = {
    'rem_cat': {'category': ['Memo items', 'G. Other (please specify)']},
    #'rem_ent': {'entity': ['GHG per capita', 'GHG per GDP (2015 prices)']},
}

filter_keep = {}

meta_data = {
    "references": "https://unfccc.int/documents/627150",
    "rights": "",
    "contact": "mail@johannes-guestchow.de",
    "title": "Israel. Biennial update report (BUR). BUR2",
    "comment": "Read fom pdf by Johannes Gütschow",
    "institution": "UNFCCC",
}

#### for processing
# aggregate categories
cats_to_agg = {
    '1': {'sources': ['1.A'], 'name': 'Energy'}, # for trends
    '1.A.4': {'sources': ['1.A.4.a', '1.A.4.b', '1.A.4.c', '1.A.4.ab'],
              'name': 'Other sectors'},
    '2.A.4': {'sources': ['2.A.4.b'], 'name': 'Soda Ash'},
    '2.A.7': {'sources': ['2.A.7.a'], 'name': 'Other'},
    '2.A': {'sources': ['2.A.1', '2.A.2', '2.A.4', '2.A.6', '2.A.7'], 'name': 'Mineral Products'},
    '2.B.5': {'sources': ['2.B.5.f', '2.B.5.g'], 'name': 'Other'},
    '2.B': {'sources': ['2.B.2', '2.B.5'], 'name': 'Chemical Industry'},
    '6.D': {'sources': ['6.D', '6X.B'], 'name': 'Wastewater Treatment and Discharge'},
    #'6.E': {'sources': ['6.E', '6X.D'], 'Other'}, # currently empty
}

# downscale
# 1.A.4.ab
downscaling = {
    'sectors': {
        '24540': {
            'basket': '24540',
            'basket_contents': ['2'],
            'entities': ['SF6', 'HFCS (SARGWP100)', 'PFCS (SARGWP100)'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '1.A': {
            'basket': '1.A',
            'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
            'entities': ['CO2', 'CH4', 'N2O'],
            'dim': f"category ({coords_terminologies['category']})",
            'tolerance': 0.05, # some inconsistencies (rounding?)
        },
        '1.A.4.ab': {
            'basket': '1.A.4.ab',
            'basket_contents': ['1.A.4.a', '1.A.4.b'],
            'entities': ['CO2', 'CH4', 'N2O', 'SOX', 'NOX', 'CO'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '1.A.4': {
            'basket': '1.A.4',
            'basket_contents': ['1.A.4.a', '1.A.4.b', '1.A.4.c'],
            'entities': ['CO2', 'CH4', 'N2O'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '2': {
            'basket': '2',
            'basket_contents': ['2.A', '2.B', '2.F'],
            'entities': ['CO2', 'CH4', 'N2O', 'SF6', 'PFCS (SARGWP100)', 'HFCS (SARGWP100)'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '2.A': {
            'basket': '2.A',
            'basket_contents': ['2.A.1', '2.A.2', '2.A.4', '2.A.7'],
            'entities': ['CO2', 'CH4', 'N2O'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '2.B': {
            'basket': '2.B',
            'basket_contents': ['2.B.2', '2.B.5'],
            'entities': ['CO2', 'CH4', 'N2O'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '4': {
            'basket': '4',
            'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F', '4.G'],
            'entities': ['CH4', 'N2O'],
            'dim': f"category ({coords_terminologies['category']})",
        },
        '5': {
            'basket': '5',
            'basket_contents': ['5.A', '5.D'], # the other sectors are 0
            'entities': ['CO2'],
            'dim': f"category ({coords_terminologies['category']})",
        },
    },
}

# map to IPCC2006
cat_conversion = {
    # ANNEXI to come (low priority as we read from CRF files)
    'mapping': {
        '1': '1',
        '1.A': '1.A',
        '1.A.1': '1.A.1',
        '1.A.2': '1.A.2',
        '1.A.3': '1.A.3',
        '1.A.4': '1.A.4',
        '1.A.4.a': '1.A.4.a',
        '1.A.4.b': '1.A.4.b',
        '1.A.4.c': '1.A.4.c',
        '1.A.5': '1.A.5', # currently not needed
        '1.B': '1.B', # currently not needed
        '1.B.1': '1.B.1', # currently not needed
        '1.B.2': '1.B.2', # currently not needed
        '2.A': '2.A',
        '2.A.1': '2.A.1', # cement
        '2.A.2': '2.A.2', # lime
        '2.A.4': '2.A.4.b', # soda ash
        '2.A.6': '2.A.5', # road paving with asphalt -> other
        '2.A.7.a': '2.A.3', # glass
        '2.B': 'M.2.B_2.B',
        '2.B.2': '2.B.2', # nitric acid
        '2.B.5.b': '2.B.8.b', # Ethylene
        '2.B.5.f': 'M.2.B.10.a', # sulphuric acid
        '2.B.5.g': 'M.2.B.10.b', # other chemicals
        '2.C': '2.C',
        '2.D': 'M.2.H.1_2',
        '2.E': '2.B.9',
        '2.F': '2.F',
        '2.G': '2.H.3',
        '4': 'M.AG',
        '4.A': '3.A.1',
        '4.B': '3.A.2',
        '4.C': '3.C.7',
        '4.D': 'M.3.C.45.AG',
        '4.E': '3.C.1.c',
        '4.F': '3.C.1.b',
        '4.G': '3.C.8',
        '5': 'M.LULUCF',
        '6': '4',
        '6.A': '4.A',
        '6.B': '4.B',
        '6.C': '4.C',
        '6.D': '4.D',
        '24540': '0',
        '15163': 'M.0.EL',
        '14637': 'M.BK',
        '14424': 'M.BK.A',
        '14423': 'M.BK.M',
        '14638': 'M.BIO',
        '7': '5',
    }, #5.A-D ignored as not fitting 2006 cats

    'aggregate': {
        '2.A.4': {'sources': ['2.A.4.b'], 'name': 'Other uses of soda ashes'},
        '2.B.8': {'sources': ['2.B.8.b'], 'name': 'Petrochemical and Carbon Black production'},
        '2.B.10': {'sources': ['M.2.B.10.a', 'M.2.B.10.b'], 'name': 'Other'},
        '2.B': {'sources': ['2.B.2', '2.B.8', '2.B.9', '2.B.10'], 'name': 'Chemical Industry'},
        '2.H': {'sources': ['M.2.H.1_2', '2.H.3'], 'name': 'Other'},
        '2': {'sources': ['2.A', '2.B', '2.C', '2.F', '2.H'],
              'name': 'Industrial Processes and Product Use'},
        '3.A': {'sources': ['3.A.1', '3.A.2'], 'name': 'Livestock'},
        '3.C.1': {'sources': ['3.C.1.b', '3.C.1.c'],
                     'name': 'Emissions from biomass burning'},
        'M.3.C.1.AG': {'sources': ['3.C.1.b', '3.C.1.c'],
                     'name': 'Emissions from biomass burning (Agriculture)'},
        '3.C': {'sources': ['3.C.1', 'M.3.C.45.AG', '3.C.7', '3.C.8'],
                     'name': 'Aggregate sources and non-CO2 emissions sources on land'},
        'M.3.C.AG': {'sources': ['M.3.C.1.AG', 'M.3.C.45.AG', '3.C.7', '3.C.8'],
                     'name': 'Aggregate sources and non-CO2 emissions sources on land ('
                             'Agriculture)'},
        'M.AG.ELV': {'sources': ['M.3.C.AG'], 'name': 'Agriculture excluding livestock'},
        '3': {'sources': ['M.AG', 'M.LULUCF'], 'name': 'AFOLU'},
    },
    'basket_copy': {
        'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
        'entities': ["HFCS", "PFCS"],
        'source_GWP': 'SARGWP100',
    },
}

sectors_to_save = [
    '1', '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4', '1.A.4.a', '1.A.4.b', '1.A.4.c',
    '1.A.5',
    '1.B', '1.B.1', '1.B.2',
    '2', '2.A', '2.A.1', '2.A.2', '2.A.3', '2.A.4', '2.A.5',
    '2.B', '2.B.2', '2.B.8', '2.B.9', '2.B.10', '2.C', '2.F', '2.H',
    '3', 'M.AG', '3.A', '3.A.1', '3.A.2',
    '3.C', '3.C.1', 'M.3.C.1.AG', '3.C.7', 'M.3.C.45.AG', '3.C.8', 'M.3.C.AG',
    'M.LULUCF', 'M.AG.ELV',
    '4', '4.A', '4.B', '4.C', '4.D',
    '0', 'M.0.EL', 'M.BK', 'M.BK.A', 'M.BK.M', 'M.BIO', '5']


# gas baskets
gas_baskets = {
    'FGASES (SARGWP100)': ['HFCS (SARGWP100)', 'PFCS (SARGWP100)', 'SF6', 'NF3',
                           'Unspecified mix of HFCs (SARGWP100)',
                           'Unspecified mix of PFCs (SARGWP100)'],
    'FGASES (AR4GWP100)': ['HFCS (AR4GWP100)', 'PFCS (AR4GWP100)', 'SF6', 'NF3',
                           'Unspecified mix of HFCs (AR4GWP100)',
                           'Unspecified mix of PFCs (AR4GWP100)'],
    'FGASES (AR5GWP100)':['HFCS (AR5GWP100)', 'PFCS (AR5GWP100)', 'SF6', 'NF3',
                          'Unspecified mix of HFCs (AR5GWP100)',
                          'Unspecified mix of PFCs (AR5GWP100)'
                          ],
    'FGASES (AR6GWP100)':['HFCS (AR6GWP100)', 'PFCS (AR6GWP100)', 'SF6', 'NF3',
                          'Unspecified mix of HFCs (AR6GWP100)',
                          'Unspecified mix of PFCs (AR6GWP100)'
                          ],
    'KYOTOGHG (SARGWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (SARGWP100)'],
    'KYOTOGHG (AR4GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR4GWP100)'],
    'KYOTOGHG (AR5GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR5GWP100)'],
    'KYOTOGHG (AR6GWP100)': ['CO2', 'CH4', 'N2O', 'FGASES (AR6GWP100)'],
}


#### functions
def is_int(input: str) -> bool:
    try:
        locale.atoi(input)
        return True
    except:
        return False