# TODO: check if downscaling respects gas basket resolution for GWP transformation
# TODO: why is albania IPPU KYOTOGHG 0 in 2005

di_query_filters = [
    'classifications', 'measures', 'gases',
]
# category, party are extra
# measure is preprocessed to find ids

# the activity data and emissions factors have a structure that is incompatible
# with PRIMAP2.
# To read it into a primap2 dataframe the information in classification / measure
# has to be put into "entity" which is currently always "No gas". I's possible,
# but takes some time, so I have omitted it here
filter_activity_factors = {
    "entity": {"gas": ["No gas"]},
    "unit": {"unit": [
        'no unit', 'kg/TJ', 't/TJ', '%', 'kg/t',
        'kg/kt', 't/t', 'kg/head/year', 'kg N2O/kg N handled', 'kg N2O/kg N',
        'kg N2O-N/kg N handled', 'g/m^2', 'kg N2O-N/kg N', 'kg N2O-N/ha', 'kg/t dm',
        't CO2-C/t', 't/unit', 't C/ha', 'kg CH4/ha', 'kg CO2/ha',
        'g/kg', 'kg/kg DC',
    ]
    },
}

# regular expression to match category code in category label
cat_code_regexp = r'(?P<code>^(([0-9][A-Za-z0-9\.]{0,10}[0-9A-Za-z]))|([0-9]))[' \
                  r'\s\.].*'

gwp_to_use = 'SARGWP100'

# PRIMAP2 interchange format config
di_to_pm2if_template_nai = {
    "coords_cols": {
        "category": "category",
        "entity": "gas",
        "unit": "unit",
        "area": "party",
        "sec_cats__class": "classification",
        "sec_cats__measure": "measure",
        "data": "numberValue",
        "time": "year",
    },
    # to store the original category name as well as the one mapped to IPCC categories
    "add_coords_cols": {
        "orig_cat_name": ["category_copy", "category"],
    },
    # terminologies for different coordinates
    "coords_terminologies": {
        "area": "ISO3",
        "scenario": "Access_Date",
        "category": "BURDI",
    },
    # default values for coordinates
    "coords_defaults": {
        "provenance": "measured",
        "source": "UNFCCC",
    },
    # mapping of values e.g. gases to the primap2 format
    "coords_value_mapping": {
        "entity": {
            f"Aggregate GHGs ({gwp_to_use})": f"KYOTOGHG ({gwp_to_use})",
            f"Aggregate F-gases ({gwp_to_use})": f"FGASES ({gwp_to_use})",
            f"HFCs ({gwp_to_use})": f"HFCS ({gwp_to_use})",
            f"PFCs ({gwp_to_use})": f"PFCS ({gwp_to_use})",
            #f"SF6 ({gwp_to_use})": f"SF6 ({gwp_to_use})",
            #f"CH4 ({gwp_to_use})": f"CH4 ({gwp_to_use})",
            f"CO2 ({gwp_to_use})": "CO2",
            #f"N2O ({gwp_to_use})": f"N2O ({gwp_to_use})",
            #f"Unspecified mix of HFCs and PFCs ({gwp_to_use})":
            #    f"UnspMixOfHFCsPFCs ({gwp_to_use})",
            f"Unspecified mix of HFCs ({gwp_to_use})": f"UnspMixOfHFCs ({gwp_to_use})",
            f"Unspecified mix of PFCs ({gwp_to_use})": f"UnspMixOfPFCs ({gwp_to_use})",
            "HFC-23": "HFC23",
            "HFC-32": "HFC32",
            "HFC-41": "HFC41",
            "HFC-43-10mee": "HFC4310mee",
            "HFC-125": "HFC125",
            "HFC-134": "HFC134",
            "HFC-134a": "HFC134a",
            "HFC-143": "HFC143",
            "HFC-143a": "HFC143a",
            "HFC-152": "HFC152",
            "HFC-152a": "HFC152a",
            "HFC-161": "HFC161",
            "HFC-227ea": "HFC227ea",
            "HFC-236ea": "HFC236ea",
            "HFC-236cb": "HFC236cb",
            "HFC-236fa": "HFC236fa",
            "HFC-245ca": "HFC245ca",
            "HFC-245fa": "HFC245fa",
            "HFC-365mfc": "HFC365mfc",
            "c-C4F8": "cC4F8",
            "c-C3F6": "cC3F6",
        },
        "unit": "PRIMAP1",
        "category": {
            # NAI
            "Total GHG emissions excluding LULUCF/LUCF": "15163",
            "Total GHG emissions including LULUCF/LUCF": "24540",
            "International Bunkers": "14637",
            "Marine": "14423",
            "Aviation": "14424",
            "CO₂ Emissions from Biomass": "14638",
        }
    },
    # fill missing data from other columns (not needed here)
    "coords_value_filling": {
    },
    # remove data based on filters
    "filter_remove": {
    },
    # keep only the data defined in the filters
    "filter_keep": {
    },
    # define meta data
    "meta_data": {
        "references": "https://di.unfccc.int",
        "title": "XXXX", # to set per country
        "comment": "Data read from the UNFCCC DI flexible query interface using the API.",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "institution": "United Nations Framework Convention on Climate Change (www.unfccc.int)",
    },
    # time format used in the input data
    "time_format": "%Y",
}

di_to_pm2if_template_ai = {
    "coords_cols": {
        "category": "category",
        "entity": "gas",
        "unit": "unit",
        "area": "party",
        "sec_cats__class": "classification",
        "sec_cats__measure": "measure",
        "data": "numberValue",
        "time": "year",
    },
    # to store the original category name as well as the one mapped to IPCC categories
    "add_coords_cols": {
        #"orig_cat_name": ["category_copy", "category"],
    },
    # terminologies for different coordinates
    "coords_terminologies": {
        "area": "ISO3",
        "scenario": "Access_Date",
        "category": "CRFDI",
    },
    # default values for coordinates
    "coords_defaults": {
        "provenance": "measured",
        "source": "UNFCCC",
    },
    # mapping of values e.g. gases to the primap2 format
    "coords_value_mapping": {
        "entity": {
            "Aggregate F-gases (AR4GWP100)": "FGASES (AR4GWP100)",
            "Aggregate GHGs (AR4GWP100)": "KYOTOGHG (AR4GWP100)",
            "HFCs (AR4GWP100)": "HFCS (AR4GWP100)",
            "PFCs (AR4GWP100)": "PFCS (AR4GWP100)",
            "Unspecified mix of HFCs and PFCs (AR4GWP100)":
                "UnspMixOfHFCsPFCs (AR4GWP100)",
            #"Unspecified mix of HFCs and PFCs":
            #    "UnspMixOfHFCsPFCs", # this is problematic, mixes should use CO2eq
            # with GWP
            "Unspecified mix of HFCs (AR4GWP100)": "UnspMixOfHFCs (AR4GWP100)",
            "Unspecified mix of PFCs (AR4GWP100)": "UnspMixOfPFCs (AR4GWP100)",
            "HFC-23": "HFC23",
            "HFC-32": "HFC32",
            "HFC-41": "HFC41",
            "HFC-43-10mee": "HFC4310mee",
            "HFC-125": "HFC125",
            "HFC-134": "HFC134",
            "HFC-134a": "HFC134a",
            "HFC-143": "HFC143",
            "HFC-143a": "HFC143a",
            "HFC-152": "HFC152",
            "HFC-152a": "HFC152a",
            "HFC-161": "HFC161",
            "HFC-227ea": "HFC227ea",
            "HFC-236ea": "HFC236ea",
            "HFC-236cb": "HFC236cb",
            "HFC-236fa": "HFC236fa",
            "HFC-245ca": "HFC245ca",
            "HFC-245fa": "HFC245fa",
            "HFC-365mfc": "HFC365mfc",
            "c-C4F8": "cC4F8",
            "c-C3F6": "cC3F6",
        },
        "unit": "PRIMAP1",
        "category": {
            'Annual Change in Total Long-term C Storage': "11024",
            'Annual Change in Total Long-term C Storage in HWP Waste': "11025",
            'HWP in SWDS': "11036",
            'International Aviation': "10357",
            'International Navigation': "8828",
            'Long-term Storage of C in Waste Disposal Sites': "temp",
            'CO₂ Emissions from Biomass': "8270",
            'International Bunkers': "8564",
            'Multilateral Operations': "8987",
            'Total Amount Captured for Storage': "11030",
            'Total Amount of CO₂ Injected at Storage Sites': "11033",
            'Total Amount of Exports for Storage': "11032",
            'Total Amount of Imports for Storage': "11031",
            'Total GHG emissions with LULUCF': "8677",
            'Total GHG emissions with LULUCF including indirect CO₂': "10480",
            'Total GHG emissions without LULUCF': "10464",
            'Total GHG emissions without LULUCF including indirect CO₂': "10479",
            'Total Leakage from Transport, Injection and Storage': "11034",
            'Waste Incineration with Energy Recovery included as Biomass': "11027",
            'Waste Incineration with Energy Recovery included as Fossil Fuels':
                "11028",
        }
    },
    # fill missing data from other columns (not needed here)
    "coords_value_filling": {
    },
    # remove data based on filters
    "filter_remove": {
        # some upsecified mixes not reported in CO2eq have tonbe removed
        "entity_wrong_unit": {
            "gas": ["Unspecified mix of HFCs and PFCs"]
        },
        # remove data that is not for a gas (partly it currently can't be read and
        # partly because the dataset is too large because of the many dimensions)
        "entity_no_gas": {
            "gas": ["No gas"]
        },
    },
    # keep only the data defined in the filters
    "filter_keep": {
        "only_emission_measures": {
            "measure": [
                'Net carbon emissions',
                'Net emissions/removals',
                'Emissions from disposal',
                'Emissions from manufacturing',
                'Emissions from stocks',
                'Indirect emissions',
                'Direct emissions per MMS',
                'Direct emissions per MMS - Anaerobic lagoon',
                'Direct emissions per MMS - Composting',
                'Direct emissions per MMS - Daily spread',
                'Direct emissions per MMS - Digesters',
                'Direct emissions per MMS - Liquid system',
                'Direct emissions per MMS - Other',
                'Direct emissions per MMS - Solid storage and dry lot',
                'Indirect N2O emissions from atmospheric deposition',
                'Indirect N2O emissions from nitrogen leaching and run-off',
                'Net emissions/removals from HWP from domestic harvest',
            ],
        },
    },
    # define meta data
    "meta_data": {
        "references": "https://di.unfccc.int",
        "title": "XXXX", # to set per country
        "comment": "Data read from the UNFCCC DI flexible query interface using the API.",
        "rights": "",
        "contact": "mail@johannes-guetschow.de",
        "institution": "United Nations Framework Convention on Climate Change (www.unfccc.int)",
    },
    # time format used in the input data
    "time_format": "%Y",
}

cat_conversion = {
    # ANNEXI to come (low priority as we read from CRF files)
    'BURDI_to_IPCC2006_PRIMAP': {
        'mapping': {
            '1': '1',
            '1.A': '1.A',
            '1.A.1': '1.A.1',
            '1.A.2': '1.A.2',
            '1.A.3': '1.A.3',
            '1.A.4': '1.A.4',
            '1.A.5': '1.A.5',
            '1.B': '1.B',
            '1.B.1': '1.B.1',
            '1.B.2': '1.B.2',
            '2': '2',
            '2.A': '2.A',
            '2.B': 'M.2.B_2.B',
            '2.C': '2.C',
            '2.D': 'M.2.H.1_2',
            '2.E': 'M.2.B_2.E',
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
            '6.B': '4.D',
            '6.C': '4.C',
            '6.D': '4.E',
            '24540': '0',
            '15163': 'M.0.EL',
            '14637': 'M.BK',
            '14424': 'M.BK.A',
            '14423': 'M.BK.M',
            '14638': 'M.BIO',
            '7': '5',
        }, #5.A-D ignored as not fitting 2006 cats
        'aggregate': {
            '2.B': {'sources': ['M.2.B_2.B', 'M.2.B_2.E'], 'name': 'Chemical Industry'},
            '2.H': {'sources': ['M.2.H.1_2', '2.H.3'], 'name': 'Other'},
            #'2': {'sources': ['2.A', '2.B', '2.C', '2.F', '2.H'],
            #      'name': 'Industrial Processes and Product Use'},
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
    },
}

di_processing_templates = {
    # templates fro the DI processing. Most processing rules will apply to several
    # versions. So we store them here and refer to them in the processing info dict
    # general templates
    'general': {
        'copyUnspHFCUnspPFC': {
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs", "UnspMixOfPFCs"],
                'source_GWP': gwp_to_use,
            },
        },
        'copyUnspHFC': {
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
        'copyHFCPFC': {
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["HFCS", "PFCS"],
                'source_GWP': gwp_to_use,
            },
        },
        'copyPFC': {
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["PFCS"],
                'source_GWP': gwp_to_use,
            },
        },
        'copyFGASES': {
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["FGASES"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # country templates
    #AFG: not needed (newer data in BUR1), 2005, 2013 only
    #AGO: 2000, 2005 only (external key needed for some gases / sectors)
    'ALB': {
        # 1990-2009, 1990-1999 need downscaling
        'DI2023-05-24': {
            'remove_ts': {
                '2.A_H': { # looks wrong in 2005
                    'category': ['2.A', '2.B', '2.C', '2.D', '2.G'],
                    'entities': ['CO2', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['2005'],
                },
                'Bunkers': { # Aviation and marine swapped in 2005
                    'category': ['14423', '14424'],
                    'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['2005'],
                },
                'Bunkers_CH4': { # 2005 looks all wrong (swap in activity data not
                    # result?)
                    'category': ['14423', '14424', '14637'],
                    'entities': ['CH4', f'KYOTOGHG ({gwp_to_use})', 'N2O'],
                        'time': ['2005'],
                },
            },
            'downscale': { # needed for 1990, 2000, 2005-2012
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CO2', 'N2O', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CO2', 'N2O', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F',
                                            '2.G'],
                        'entities': ['CO2', 'N2O', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                            '4.G'],
                        'entities': ['N2O', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D', '5.E'],
                        'entities': ['CO2', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C', '6.D'],
                        'entities': ['N2O', 'CH4'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                    'bunkers': {
                        'basket': '14637',
                        'basket_contents': ['14423', '14424'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                        #'skipna_evaluation_dims': None,
                        #'skipna': True,
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs", "UnspMixOfPFCs"],
                'source_GWP': gwp_to_use,
            },
        }
    },
    #AND: no data
    'ARE': { # 1990, 2000, 2005, 2014. some aggregation for fgases (pfcs) needed
        'DI2023-05-24': {
            'agg_tolerance': 0.015,
            'ignore_entities': ["NMVOC"], #errors when aggregating cats
            'aggregate_cats': {
                '2': {'sources': ['2.A', '2.B', '2.C'],
                     'name': '2.  Industrial Processes'},
                '15163': {'sources': ['1', '2', '4', '6'],
                          'name': 'Total GHG emissions excluding LULUCF/LUCF'},
                '24540': {'sources': ['1', '2', '5', '4', '6'],
                          'name': 'Total GHG emissions including LULUCF/LUCF'},
            },
        },
    },
    # ARG newer data in BUR
    # ARM 1990, 2000, 2006, 2010, no processing needed
    # ATG 1990, 2000, no processing needed
    'AZE': {
        # 1990-2013, but from different submissions and not completely consistent
        # including different sector coverage
        # for FGASES emissions are in HFCs for some years and in PFCs for others.
        # waste data has inconsistent subsectors
        'DI2023-05-24': {
            'remove_ts': {
                '1.A.1': { #contains data for all subsectors
                    'category': ['1.A.1'],
                    'entities': ['CH4', f'KYOTOGHG ({gwp_to_use})'],
                    'time': ['1990', '2000', '2005', '2006', '2007', '2008', '2009',
                             '2010', '2011', '2012'],
                },
                'pfcs': { # only HFCs in other years, likely wrong
                    'entities': [f'PFCS ({gwp_to_use})'],
                    'time': ['1991', '1992', '1993', '1994'],
                },
            },
            'downscale': { # needed for 1990, 2000, 2005-2012
                'sectors': {
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
                'entities': {
                    'FGASES': {
                        'basket': f'FGASES ({gwp_to_use})',
                        'basket_contents': [f'HFCS ({gwp_to_use})'],
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995']},
                    },
                    'HFC': {
                        'basket': f'HFCS ({gwp_to_use})',
                        'basket_contents': [f'UnspMixOfHFCs ({gwp_to_use})'],
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '2000', '2001', '2002', '2003',
                                         '2004', '2005', '2006', '2007', '2008',
                                         '2009', '2010', '2012']},
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # BDI 1998, 2005, 2010, 2015 # data coverage is a bit inconsistent
    # BEN 1995, 2000 # data coverage a bit inconsistent
    'BFA': { # 1994, 2007, 2008-2017
        'DI2023-05-24': {  # remove 2007, seems to have summed sectors (Agri and LULUCF)
            # and missing sectors (e.g. 1,2 for CH4, N2O), Agri. burning (4.E,
            # 4.F) missing for 2008-2017
            'remove_years': ['2007'],
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # BGD 1994, 2001, 2005; coverage mostly consistent but not fully
    # BHR 1994, 2000 (with some gaps in 2000)
    'BHS': { # 1990, 1994, 2000 (differing coverage, might be unusable for some sectors)
        # TODO: check e.g. 4 and 5
        'DI2023-05-24': {
            'downscale': {
                'sectors': {
                    '4': { # 1994
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.D', '4.G'],
                        'entities': ['CH4', 'CO2', f'KYOTOGHG ({gwp_to_use})'], # no N2O but
                        # CO2 is unusual
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
            },
        }
    },
    'BIH': {
        'DI2023-05-24': {
            # downscaling in two steps
            # 1990-2001 has different coverage than 2002-2012 and 2013-2014
            # do not downscale KyotoGHG for 1990-2001 as that's aggregated
            # later to avoid inconsistencies
            'downscale': {
                'sectors': {
                    '1.A_1990': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '1.B_1990': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CH4', 'CO2', 'NMVOC', 'SO2'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '2_1990': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '4_1990': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '5_1990': {
                        'basket': '5',
                        'basket_contents': ['5.A'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '6_1990': {
                        'basket': '6',
                        'basket_contents': ['6.A'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994',
                                         '1995', '1996', '1997', '1998', '1999',
                                         '2000', '2001']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
                'entities': {  # 2002-2014
                    'KYOTO': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {'category (BURDI)':
                                    ['1', '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                     '1.A.5', '1.B', '1.B.1', '1.B.2', '2', '2.A',
                                     '2.B', '2.C', '2.D', '2.E', '4', '4.A', '4.B',
                                     '4.C', '4.D', '4.E', '5', '5.A', '6', '6.A',
                                     '6.B', '6.C', '14423', '14424', '14637',
                                     '15163', '24540',
                                     ],
                                'time': ['2002', '2003', '2004', '2005', '2006',
                                         '2007', '2008', '2009', '2010', '2011',
                                         '2012', '2013', '2014'],
                                },
                    },
                },
            },
        },
    },
    'BLZ': {
        'DI2023-05-24': { # 1994, 2000, 2003, 2006, 2009 (energy sector missing in 200X)
            'remove_ts': {
                'AG_2000': { # inconsistent with other data
                    'category': ['4', '4.A', '4.B', '4.C', '4.D', '4.E', '4.F'],
                    'time': ['2000'],
                },
                'waste_1994': { # inconsistent with other data
                    'category': ['6', '6.A', '6.B'],
                    'time': ['1994'],
                },
            },
        },
    },
    # BOL 1990, 1994, 1998, 2000, 2002 (energy sectors missing for CH4, N2O), 2004 (sm),
    # BRA 1990-2016 (BUR4)
    'BRB': {
        'DI2023-05-24': {
            #'remove_years': ['1990', '1994', '1997'], # keep as 1997 needed for downscaling
            'aggregate_cats': {
                '14637': {'sources': ['14423', '14424'],
                     'name': 'International Bunkers'},
            },
            # downscaling in two steps
            # 2000 - 2012 LULUCF KYOTOGHG
            # later KYOTOGHG to gases using 1997 shares (not ideal)
            'downscale': {
                'sectors': {
                    '5_2000': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1997', '2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2009', '2010']},
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
                'entities': {  # 2000-2010 (1997 as key)
                    'KYOTO': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CO2', 'CH4', 'N2O'],
                        'sel': {'category (BURDI)':
                                    ['1', '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                     '2', '2.A', '5', '14423', '14424',
                                     '14637', '4', '4.A', '4.B', '4.D',
                                     '6', '6.A', '6.B', '15163', '24540',
                                     ],
                                'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010'],
                                },
                    },
                },
            },
        },
    }, # TODO: downscaling using external key instead of 1997
    # BRN 2010 only (though with full sectors)
    # BTN 1994, 2000, 2015. patchy coverage but no downscaling needed / possible
    # BWA 1994, 2000, 2015. inconsistent coverage
    # TODO CAF 1994, 2003-2010. 1994 has different coverage and might be inconsistent
    # CHL: more data in BUR4/5
    'CHN' :{
        'DI2023-05-24': { #1994 (gaps), 2005 (needs downscaling), 2010, 2012, 2014
            # (relatively complete and consistent)
            'remove_ts': {
                '1.A.1': { #contains data for all subsectors
                    'category': ['1.A.1'],
                    'entities': ['N2O'],
                        'time': ['1994'],
                },
            },
            'downscale': { # needed for 2005
                'sectors': {
                    '1': { # 2005
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CH4', 'CO2', 'N2O'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '1.B': { # 2005
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '1.A': { # 2005
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    # with current functionality we can't downscale 1.A further for
                    # non-CO2 as it needs several steps and CO2 is present
                    '2': { # 2005
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C'],
                        'entities': ['CO2', 'N2O'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '4': { # 2005
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '5': { # several years
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                    '6': { # 2005
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C', '6.D'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
                'entities': {
                    'HFC': {
                        'basket': f'HFCS ({gwp_to_use})',
                        'basket_contents': ['HFC125', 'HFC134a', 'HFC143a', 'HFC152a',
                                            'HFC227ea', 'HFC23', 'HFC236fa', 'HFC32',
                                            f'UnspMixOfHFCs ({gwp_to_use})'],
                        'sel': {'time': ['2005', '2010']},
                    },
                    'PFC': {
                        'basket': f'PFCS ({gwp_to_use})',
                        'basket_contents': ['C2F6', 'CF4'],
                        'sel': {'time': ['2005', '2010']},
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    'CIV' :{
        'DI2023-05-24': { #1994 (needs some downscaling), 2000
            'downscale': { # needed for 2005
                'sectors': {
                    '1.A': { # 2005
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': ['CO2', 'CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'skipna_evaluation_dims': None,
                        'skipna': True,
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["FGASES"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # CMR: 1994, 2000, not fully consistent
    # COD: 1994, 1999-2003, coverage not fully consistent, downscaling complicated
    # COG: 1994, 2000, not fully consistent
    # COK: 1994, limited coverage
    # COL: not needed, more data in BUR3, 1990, 1994, 2000, 2004,
    # COM: 1994, 2000
    # CPV: more data in NC3
    # CRI: more data in NIR
    'CUB': { # 1990, (1992, 1994, 1996, 1998 dwn needed), 2000, 2002
        'DI2023-05-24': {
            # calculate LULUCF from 0 an M.0.EL
            'subtract_cats': {
                '5': {'parent': '24540', 'subtract': ['15163'],
                      'name': '5.  Land-Use Change and Forestry'},
            },
            'downscale': { # not tested yet
                'sectors': {
                    '0': {
                        'basket': '24540',
                        'basket_contents': ['15163', '5'],
                        'entities': ['CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    'M.0.EL': {
                        'basket': '15163',
                        'basket_contents': ['1', '2', '3', '4', '6'],
                        'entities': ['CH4', 'CO2', 'N2O', 'C2F6', 'CF4', 'HFC134',
                                     'HFC23', 'SF6', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4', '1.A.5'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CH4', 'CO2', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.G'],
                        'entities': ['CH4', 'CO2', 'N2O', 'C2F6', 'CF4', 'HFC134',
                                     'HFC23', 'SF6', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NOx'],
                        'dim': 'category (BURDI)',
                    },
                '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C'],
                        'entities': ['CH4', 'CO2', 'N2O', 'CO', 'NMVOC', 'NOx', 'SO2'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
        },
    },
    # DJI: 1994, 2000
    'DMA' :{
        'DI2023-05-24': {  # 1994, 2000, (2001-2017, some dwn)
            # LULUCF has gaps, cat 0 assumes 0 for LULUCF in these years
            # we omit aerosols and ghg precusors as only so2 can be downscaled
            'downscale': {
                'sectors': {
                    '1_CH4': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1994', '2000', '2001', '2002', '2003',
                                         '2004', '2005']},
                    },
                    '1_CO2': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1994', '2000', '2001', '2002', '2003',
                                         '2004', '2005']},
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.F'],
                        'entities': ['CO2', f'HFCS ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    'bunkers': {
                        'basket': '14637',
                        'basket_contents': ['14423', '14424'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # DOM: # 1990, 1994, 1998, 2000, 2010
    # DZA: 1994, 2000
    'ECU': {
        'DI2023-05-24': { # 1990 (1994, 2000), 2010, 2012
            #omit aerosols / GHG precursosrs in downscaling
            'remove_years': ['1990'],
            'downscale': {
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.G'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E',
                                            '4.F', '4.G'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.D'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                },
                'entities': {
                    'KYOTO': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {'category (BURDI)':
                                    ['15163', '24540',
                                     '1', '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                     '1.A.5', '1.B',  '1.B.1',  '1.B.2',
                                     '2', '2.A', '2.B', '2.C', '2.D', '2.G',
                                     '4', '4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                     '4.G',
                                     '5', '5.A', '5.B', '5.C', '5.D',
                                     '6', '6.A', '6.B', '6.D', '7']}
                    },
                },
            },
        },
    },
    'EGY': {
        'DI2023-05-24': { # 1990, 2000, 2005
            #omit aerosols / GHG precursosrs in downscaling
            'remove_ts': {
                '2.G': { # all in 2.G in 1990
                        'category': ['2.G'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})', 'CO2', 'N2O'],
                    },
            },
            'downscale': {
                'sectors': {
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C'],
                        'entities': ['CO2', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # 'ERI' #1994 1995-1999 (partial coverage, KYOTOGHG and total are incomplete), 2000
    'ETH': {
        'DI2023-05-24': { # 1990-1993 (downscaling needed), 1994-2013
            'downscale': {
                # omit aerosols / ghg precursors as missing for most years
                'sectors': { # for 1990-1994
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    'bunkers': {
                        'basket': '14637',
                        'basket_contents': ['14424'],
                        'entities': ['CO2', f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                },
                'entities': {
                    'bunkers': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {'category (BURDI)': ['14637', '14424']}
                    },
                },
            },
        },
    },
    # FJI: 1994, 2000
    # FSM: 1994, 2000
    # GAB: 1994, 2000 (more data in NIR)
    # from here down aerosols and GHG precursors are always omitted in downscaling
    # GEO:
    'GEO': {
        'DI2023-05-24': { # 1990-1997, 2000, 2000-2013 (more data in NC4)
            'downscale': {
                'sectors': { # for 1991-1997
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.E', '2.F',
                                            '2.G'],
                        'entities': ['CO2', 'CH4', 'N2O', 'C2F6', 'CF4', 'HFC125',
                                     'HFC134', 'HFC134a', 'HFC32', 'SF6'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                            '4.G'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    # 5 subsectors are chaotic
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.D'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
        },
    },
    # GHA: 1990-2006
    # GIN: 1994, 2000
    # GMB: 1993, 2000
    'GMB': {
        'DI2023-05-24': { # 1993, 2000
            'remove_ts': {
                'waste': { # very high in 1994
                    'category': ['6', '6.A', '6.B'],
                    'entities': ['CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['1993'],
                },
            },
        }
    },
    'GNB': {
        'DI2023-05-24': {
            'remove_ts': {
                'energy_nonCO2': { # very high in 2006
                    'category': ['1', '1.A', '15163', '24540'],
                    'entities': ['CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['2006'],
                },
            },
        },
    },
    # GNQ: no data
    'GRD': { # 1994, limited coverage
        'DI2023-05-24': {
            'remove_ts': {
                'agri, waste': { # inconsistent with other sources
                    'category': ['4', '4.A', '4.B', '4.D', '6', '6.A',
                                 '15163', '24540'],
                    'entities': ['CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['1994'],
                },
            },
        },
    },
    # GTM: 1990, 1994, 2000, 2005,
    # GUY: 1990-2004
    # HND: 1995, 2000, 2005, 2015
    # HTI: 1994-2000
    'IDN': {
        'DI2023-05-24': { # 1990-1994, 2000
            'downscale': {
                'sectors': { # for 1990-1993
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CH4', 'CO2'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994']},
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                            '4.G'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1990', '1991', '1992', '1993', '1994']},
                    },
                },
            },
        },
    },
    'IND': {
        'DI2023-05-24': { # 1994,2000, 2010, 2016. Subsectors doffer a bit especilly
            # for 1994 and for LULUCF data
            'downscale': {
                'sectors': { # for 1994
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1994', '2000']},
                    },
                },
            },
        },
    },
    # ISR: sf6 in 2008 is very high, but it's from BUR1
    'JAM': { # 1994, 2006-2010, 2012
        'DI2023-05-24': {
            'remove_ts': {
                'agri, waste': { # inconsistent with other sources
                    'category': ['4', '4.A', '4.B', '4.D', '6', '6.A',
                                 '15163', '24540'],
                    'entities': ['CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['1994'],
                },
            },
        },
    },
    # JOR: M.AG in 2000 is very low but it's like that in NC2 and no comment on error
    # in comparison in NC3
    # 'JOR': {
    #     'DI2023-05-24': {
    #         'remove_ts': {
    #             'agri_N2O': {
    #                 'category': [''],
    #                 'entities': ['N2O'],
    #                 'time': ['2000']
    #             },
    #         },
    #     }
    # }
    'KEN': {
        'DI2023-05-24': { # 1994,1995, 2000, 2005, 2010. Subsectors doffer a bit
            # especilly for 1994
            # 1994 data is inconsistent with 1995 and following years and has
            # unrealisticly high N2O emissions from the energy sector
            'remove_years': ['1994'],
            'aggregate_cats': {
                '1.B': {'sources': ['1.B.2'],
                     'name': '1.B  Fugitive Emissions from Fuels'},
            },
        },
    },
    # KGZ: 1990-2010
    # KHM: 1994, 2000 (more data in BUR1)
    'KIR': { # 1994, (2004,2005 partial coverage), 2006-2008
        'DI2023-05-24': {
            'remove_ts': {
                'agri_n2O': { # very high compared to CH4 and total emissions
                    'category': ['4', '4.B',
                                 '15163', '24540'],
                    'entities': ['N2O', f'KYOTOGHG ({gwp_to_use})'],
                },
            },
        },
    },
    # KNA: 1994
    # KOR: 1990-2018 (more data in 2022 inventory)
    # KWT: 1994, 2016
    # LAO: 1990, 2000 (1990 data maybe inconsistent)
    # LBN: 1994, 2000, 2011-2013
    # LBR: 2000, 2014 (2000 misses some sectors, e.g. IPPU)
    # LBY: no data
    'LCA': {
        'DI2023-05-24': { #1994, 2000, 2005, 2010, sectors a bit inconsistent for 1994
            # 1994 data waste CH4
            'remove_ts': {
                'waste': { # very high in 1994
                    'category': ['6', '6.A', '6.B', '6.D'],
                    'entities': ['CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['1994'],
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # LKA: 1994, 2000. a bit inconsisten in subsectrs (all emissions in "other in
    # 1994 for some sectors)
    'LSO': {
        'DI2023-05-24': { # 1994,2000, 2000 needs downscaling
            'downscale': {
                'sectors': { # for 2000
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A'],
                        'entities': ['CH4', 'CO2', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.2', '1.A.3', '1.A.4', '1.A.5'],
                        'entities': ['CH4', 'CO2', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.D', '4.E'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
        },
    },
    'MAR': { # TODO IPPU subsectors chaotic (swap between other and metal prodction)
        'DI2023-05-24': { # 1994,2000, (2000-2006,2007 needs downscaling), 2010, 2012
            'downscale': {
                'sectors': {
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'tolerance' : 0.018, # LULUCF data inconstent in 2012
                    },
                },
                'entities': {
                    'all': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {'category (BURDI)': [
                            '1', '2', '4', '5', '6', '15163', '24540',
                            '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4',
                            '1.B', '1.B.1', '1.B.2',
                            '2.A', '2.C', '2.D',
                            '4.A', '4.B', '4.C', '4.D',
                            '5.A', '5.B',
                            '6.A', '6.B', '6.D',
                        ]}
                    },
                },
            },
        },
    },
    # MDA: 1990-2013 (more data in NIR / NC5)
    'MDG': {
        'DI2023-05-24': { # 1994,2000, 2005-2010 (2006-2010 needs downscaling)
            'downscale': {
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2005', '2006', '2007', '2008', '2009',
                                         '2010']},
                    },
                    # further downscaling is not possible in a consistent manner with
                    # current code (and not necessary for primap-hist). Using the
                    # 2005 subsector information would lead to individual gas
                    # timeseries which are inconsistent with given kyotoghg subsector
                    # timeseries while using the kyotoghg subsector information will
                    # not give individual gas subsector timeseries which add up to
                    # the individual gas main sector timeseries
                    # same for 6
                },
                'entities': {
                    'kyotoghg_4': { # in general similar problem to 1.A, but most sectors have
                        # only one gas and we need the data for PRIMAP-hist,
                        # so we have to do it anyway
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'N2O'],
                        'sel': {
                            'category (BURDI)': [
                                '4.A', '4.B', '4.C', '4.D', '4.E', '4.F'],
                            'time': [
                                '2005', '2006', '2007', '2008', '2009','2010'],
                        }
                    },
                },
            },
        },
    },
    # MDV: 1994 (only few sectors), 2011-2015
    # MEX: more data in BURs 2 and 3
    # MHL: 2000, 2005, 2010
    # MKD:
    'MKD': {
        'DI2023-05-24': {  # 1990-2009
            'downscale': {
                'entities': {
                    'FGASES': {
                        'basket': f'FGASES ({gwp_to_use})',
                        'basket_contents': [f'HFCS ({gwp_to_use})'],
                    },
                    'HFC': {
                        'basket': f'HFCS ({gwp_to_use})',
                        'basket_contents': [f'UnspMixOfHFCs ({gwp_to_use})'],
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    'MLI': {
        'DI2023-05-24': {  # 1995,2000, 2005
            'downscale': {
                'sectors': {
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['1995', '2000']},
                    },
                },
                'entities': {
                    'FGASES': {
                        'basket': f'FGASES ({gwp_to_use})',
                        'basket_contents': [f'HFCS ({gwp_to_use})'],
                    },
                    'HFC': {
                        'basket': f'HFCS ({gwp_to_use})',
                        'basket_contents': [f'UnspMixOfHFCs ({gwp_to_use})'],
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    'MMR': {
        'DI2023-05-24': {  # 2000-2005
            'downscale': {
                'sectors': {
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                },
                'entities': {
                    'kyotoghg_5': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CO2', 'CH4', 'N2O'],
                        'sel': {
                            'category (BURDI)': [
                                '5'],
                        }
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # MNE: more data in BUR3
    # MNG: 1990-1998, 2006. Some details missing in 1990-1998 but to disconnected
    # from 2006 data to use that for downscaling
    # MOZ: 1990, 1994
    # MRT: more data in BUR 1 and 2
    'MUS': {
        'DI2023-05-24': { #1995, 200-2006, 2013
            'remove_ts': {
                'waste': { # 1995 inconsistent
                    'category': ['6', '6.A', '6.B', '6.C', '6.D'],
                    'entities': ['CO2', 'CH4', 'N2O', f'KYOTOGHG ({gwp_to_use})'],
                        'time': ['1995'],
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs", "UnspMixOfPFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # MWI: 1990, 1994. inconsistency in 1.B.1: 1994: CO2, 1990: CH4
    # MYS: more data in BUR 3, 4
    # NAM: more adat in BUR 2, 3
    # NER: 1990, 2000, 2008
    # NGA: miore data in NIR
    # NIC: 1994, 2000: LU data inconsistent (5.A missing in 2000)
    # NIU: 1990, 2000, 2005-2009
    # NPL: 1994, 2000
    # NRU: 1994, 2000, 2003, 2007, 2010. Subsectors (e.g. 1.A.x) sometimes inconsistent
    # OMN: more data in BUR1
    # PAK: 1994, 2008, 2012, 2015 (very limited data)
    # PAN: more data in NIR, BUR2
    # PER: 1994, 2000, 2010, 2012
    # PNG: 1994, 2000 inconsistent sector coverage
    'PHL': {
        'DI2023-05-24': {  # 1994, 2000
            'downscale': {
                'sectors': {
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                    },
                },
                'entities': {
                    'kyotoghg_56': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'N2O'],
                        'sel': {
                            'category (BURDI)': ['6', '6.A', '6.B'],
                        }
                    },
                },
            },
        },
    },
    # PLW: 1994, 1995-1999 (partial), 2000, 2005
    # PRK: 1990, 1994, 2000, 2002
    # PRY: 1990, 1994, 2000, 2005, 2011, 2012, 2015, 2017 land use sectors not
    # consistent, more data in BUR3 but not read yet
    # PSE: 2011 only
    # QAT: 2007 only
    'RWA': {
        'DI2023-05-24': {  # 2002, 2005
            'downscale': {
                'sectors': {
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
        },
    },
    # SAU: 1990, 2000, 2010, 2012
    # SDN: 1995, 2000 subsectors inconsistent
    # SEN: 2000, 2005 subsectors inconsistent
    # SGP: 1994, 2000, 2010, 2012 for 1994 sectors a bit inconsistent
    'SLB': {
        'DI2023-05-24': {  # 1994 (energy CO2 only), 2000, 2005, 2010 (5, 10 need downscaling)
            'downscale': {
                'entities': {
                    'kyotoghg': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CO2', 'CH4', 'N2O'],
                        'sel': {
                            'category (BURDI)': [
                                '1', '1.A', '1.A.1', '1.A.3', '1.A.4',
                                '1.B', '1.B.1', '1.B.2',
                                '4', '4.A', '4.B', '4.C', '4.D',
                                '6', '6.A', '6.B',
                                '14424', '14637', '15163', '24540',
                            ],
                        }
                    },
                },
            },
        },
    },
    # SLE: no data
    # SLV: 1994, 2005 subsectors a bit inconsistent
    # SMR: 2007, 2010
    # SOM: no data
    # SSD: 2012-2015
    'STP': {
        'DI2023-05-24': {  # 1998 (dwn), 2005 (dwn), 2012:
            'downscale': {
                'entities': {
                    'kyotoghg': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CO2', 'CH4', 'N2O'],
                        'sel': {
                            'category (BURDI)': [
                                '1', '1.A', '1.A.1', '1.A.3', '1.A.4', '1.A.5',
                                '1.B',
                                '4', '4.A', '4.B', '4.D', '4.E', '4.F',
                                '5', '5.A', '5.B', '5.C', '5.D',
                                '6', '6.A', '6.B',
                                '14423', '14424', '14637', '14638', '15163', '24540',
                            ],
                        }
                    },
                },
            },
        },
    },
    # SUR: 2003
    # SYC: 1995 (partial), 2000
    # SYR: 1994-2005: external key needed
    'TCD': {
        'DI2023-05-24': {  # 1993, 1998-2003, 2010 sector coverage inconsistent
            # LULUCF data with sum errors
            'downscale': {
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A'],
                        'entities': ['CO2'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
        },
    },
    # TGO: more data in BUR / NIR, 1992-1998, 2000, 2005, 2010, 2013-2018 (
    # downscaling needed for some years, inconsistent detail)
    # THA: 1994 (2000-2013, extensive downscaling needed for 2000-2012).
    'THA': {
        'DI2023-05-24': {
            'downscale': {
                # main sectors present as KYOTOGHG sum. subsectors need to be downscaled
                # TODO: downscale CO, NOx, NMVOC, SO2 (national total present)
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '2': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E',
                                            '4.F'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C'],
                        'entities': [f'KYOTOGHG ({gwp_to_use})'],
                        'dim': 'category (BURDI)',
                        'sel': {'time': ['2000', '2001', '2002', '2003', '2004',
                                         '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013']},
                    },
                },
                'entities': {
                    'KYOTO': {
                        'basket': f'KYOTOGHG ({gwp_to_use})',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {
                            'category (BURDI)': [
                                '1', '1.A', '1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                '1.B', '1.B.1', '1.B.2',
                                '2', '2.A', '2.B', '2.C', '2.D',
                                '4', '4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                '5', '5.A', '5.B', '5.C',
                                '6', '6.A', '6.B', '6.C',
                                '15163', '24540',
                            ],
                            'time': ['2000', '2001', '2002', '2003', '2004',
                                     '2005', '2006', '2007', '2008', '2009',
                                     '2010', '2011', '2012', '2013']
                        },
                    },
                },
            },
        },
    },
    # TJK 1990-2010
    # TKM: 1994, 2000, 2004, 2010. subsectors a bit inconsistent
    # TLS: 2010, also covered by NC2, but without full detail
    # TON: 1994, 2000, 2006. subsectors a bit inconsistent
    # TTO: 1990 only
    # TUN: 1994, 2000
    # TUV: 1994, 2014, many sectors missiong / 0 (but maybe as there are no emissions)
    # TZA: 1990, 1994
    # UGA: 1994, 2000, subcategories a bit inconsistent
    'URY': {
        # remove data: CH4, 1998, 2002, 1
        'DI2023-05-24': {
            'downscale': {
                'sectors': {
                    '1': {
                        'basket': '1',
                        'basket_contents': ['1.A', '1.B'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '1.A': {
                        'basket': '1.A',
                        'basket_contents': ['1.A.1', '1.A.2', '1.A.3', '1.A.4',
                                            '1.A.5'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '1.B': {
                        'basket': '1.B',
                        'basket_contents': ['1.B.1', '1.B.2'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '2_CO2CH4N2O': {
                        'basket': '2',
                        'basket_contents': ['2.A', '2.B', '2.C', '2.D', '2.G'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '2_FGASES': {
                        'basket': '2',
                        'basket_contents': ['2.C', '2.E', '2.F'],
                        'entities': ['C2F6', 'CF4', 'HFC125', 'HFC134a', 'HFC143a',
                                     'HFC152a', 'HFC227ea', 'HFC23', 'HFC32', 'SF6'],
                        'dim': 'category (BURDI)',
                    },
                    '4': {
                        'basket': '4',
                        'basket_contents': ['4.A', '4.B', '4.C', '4.D', '4.E', '4.F',
                                            '4.G'],
                        'entities': ['CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.A', '5.B', '5.C', '5.D', '5.E'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B', '6.C', '6.D'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfPFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # UZB: 1990-2012
    # VCT: 1990, 1994, 1997, 2000, 2004. Sector coverage a bit inconsistent. 1.A.x
    # missing for CH4 but present for CO2. IPPU is 0, subsectors missing downscaling
    # doesn't wor for all 0 / Nan timeseries
    # VEN: 1999 only
    # VNM: more data in BUR3
    # VUT: more data in NC3
    # WSM: more data in NC2
    # YEM: 1995, 2000, 2010, 2012. subsectoral data a bit inconsistent, e.g. for 1.A.x
    # ZAF: 1990, 1994
    'ZMB': {
        'DI2023-05-24': {  # 1994, 2000
            'downscale': { # for 2000
                'sectors': {
                    '5': {
                        'basket': '5',
                        'basket_contents': ['5.B', '5.C'],
                        'entities': ['CO2', 'CH4', 'N2O'],
                        'dim': 'category (BURDI)',
                    },
                    '6': {
                        'basket': '6',
                        'basket_contents': ['6.A', '6.B'],
                        'entities': ['CH4'],
                        'dim': 'category (BURDI)',
                    },
                },
            },
            'basket_copy': {
                'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
                'entities': ["UnspMixOfHFCs"],
                'source_GWP': gwp_to_use,
            },
        },
    },
    # ZWE:
    'ZWE': { # 1994, 2000, 2006 consistency of sectors and coverage does not look good,
    # especially for subsectors
        'DI2023-05-24': {  # remove all years
            'remove_years': ['1994', '2000', '2006'],
        },
    },
}

di_processing_info = {
    # only countries with special processing listed
    # category conversion is defined on a country group level
    # the 'default' option is used if no specific option is found such that
    # processing of new versions can be done before creating a configuration for the
    # version.
    'ALB': {
        'default': di_processing_templates['ALB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ALB']['DI2023-05-24'],
    },
    'ARE': {
        'default': di_processing_templates['ARE']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ARE']['DI2023-05-24'],
    },
    'ARG': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'AZE': {
        'default': di_processing_templates['AZE']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['AZE']['DI2023-05-24'],
    },
    'BFA': {
        'default': di_processing_templates['BFA']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['BFA']['DI2023-05-24'],
    },
    'BHS': {
        'default': di_processing_templates['BHS']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['BHS']['DI2023-05-24'],
    },
    'BIH': {
        'default': di_processing_templates['BIH']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['BIH']['DI2023-05-24'],
    },
    'BLZ': {
        'default': di_processing_templates['BLZ']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['BLZ']['DI2023-05-24'],
    },
    'BOL': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'BRB': {
        'default': di_processing_templates['BRB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['BRB']['DI2023-05-24'],
    },
    'BRN': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'CHL': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'CHN': {
        'default': di_processing_templates['CHN']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['CHN']['DI2023-05-24'],
    },
    'CIV': {
        'default': di_processing_templates['CIV']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['CIV']['DI2023-05-24'],
    },
    'CUB': {
        'default': di_processing_templates['CUB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['CUB']['DI2023-05-24'],
    },
    'DMA': {
        'default': di_processing_templates['DMA']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['DMA']['DI2023-05-24'],
    },
    'ECU': {
        'default': di_processing_templates['ECU']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ECU']['DI2023-05-24'],
    },
    'EGY': {
        'default': di_processing_templates['EGY']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['EGY']['DI2023-05-24'],
    },
    'ETH': {
        'default': di_processing_templates['ETH']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ETH']['DI2023-05-24'],
    },
    'GEO': {
        'default': di_processing_templates['GEO']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['GEO']['DI2023-05-24'],
    },
    'GMB': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'GNB': {
        'default': di_processing_templates['GNB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['GNB']['DI2023-05-24'],
    },
    'IDN': {
        'default': di_processing_templates['IDN']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['IDN']['DI2023-05-24'],
    },
    'IND': {
        'default': di_processing_templates['IND']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['IND']['DI2023-05-24'],
    },
    'ISR': {
        'default': di_processing_templates['general']['copyHFCPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyHFCPFC'],
    },
    'JAM': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'JOR': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'KEN': {
        'default': di_processing_templates['KEN']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['KEN']['DI2023-05-24'],
    },
    'KGZ': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'KOR': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'LCA': {
        'default': di_processing_templates['LCA']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['LCA']['DI2023-05-24'],
    },
    'LKA': {
        'default': di_processing_templates['general']['copyFGASES'],
        'DI2023-05-24': di_processing_templates['general']['copyFGASES'],
    },
    'LSO': {
        'default': di_processing_templates['LSO']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['LSO']['DI2023-05-24'],
    },
    'MAR': {
        'default': di_processing_templates['MAR']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['MAR']['DI2023-05-24'],
    },
    'MDA': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'MDG': {
        'default': di_processing_templates['MDG']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['MDG']['DI2023-05-24'],
    },
    'MDV': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'MEX': {
        'default': di_processing_templates['general']['copyHFCPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyHFCPFC'],
    },
    'MHL': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'MLI': {
        'default': di_processing_templates['MLI']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['MLI']['DI2023-05-24'],
    },
    'MMR': {
        'default': di_processing_templates['MMR']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['MMR']['DI2023-05-24'],
    },
    'MNE': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'MNG': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'MOZ': {
        'default': di_processing_templates['general']['copyPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyPFC'],
    },
    'MUS': {
        'default': di_processing_templates['MUS']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['MUS']['DI2023-05-24'],
    },
    'PHL': {
        'default': di_processing_templates['PHL']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['PHL']['DI2023-05-24'],
    },
    'PRY': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'PSE': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'RWA': {
        'default': di_processing_templates['RWA']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['RWA']['DI2023-05-24'],
    },
    'SEN': {
        'default': di_processing_templates['general']['copyHFCPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyHFCPFC'],
    },
    'SGP': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'SLB': {
        'default': di_processing_templates['SLB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['SLB']['DI2023-05-24'],
    },
    'SMR': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'STP': {
        'default': di_processing_templates['STP']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['STP']['DI2023-05-24'],
    },
    'SWZ': {
        'default': di_processing_templates['general']['copyUnspHFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFC'],
    },
    'TCD': {
        'default': di_processing_templates['TCD']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['TCD']['DI2023-05-24'],
    },
    'THA': {
        'default': di_processing_templates['THA']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['THA']['DI2023-05-24'],
    },
    'URY': {
        'default': di_processing_templates['URY']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['URY']['DI2023-05-24'],
    },
    'UZB': {
        'default': di_processing_templates['general']['copyUnspHFCUnspPFC'],
        'DI2023-05-24': di_processing_templates['general']['copyUnspHFCUnspPFC'],
    },
    'ZMB': {
        'default': di_processing_templates['ZMB']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ZMB']['DI2023-05-24'],
    },
    'ZWE': {
        'default': di_processing_templates['ZWE']['DI2023-05-24'],
        'DI2023-05-24': di_processing_templates['ZWE']['DI2023-05-24'],
    },
}

basket_copy_HFCPFC = {
    'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
    'entities': ["HFCS", "PFCS"],
    'source_GWP': gwp_to_use,
},
basket_copy_unspHFCPFC = {
    'GWPs_to_add': ["AR4GWP100", "AR5GWP100", "AR6GWP100"],
    'entities': ["UnspMixOfHFCs", "UnspMixOfPFCs"],
    'source_GWP': gwp_to_use,
},



