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
            "Aggregate GHGs (SARGWP100)": "KYOTOGHG (SARGWP100)",
            "Aggregate F-gases (SARGWP100)": "FGASES (SARGWP100)",
            "HFCs (SARGWP100)": "HFCS (SARGWP100)",
            "PFCs (SARGWP100)": "PFCS (SARGWP100)",
            #"SF6 (SARGWP100)": "SF6 (SARGWP100)",
            #"CH4 (SARGWP100)": "CH4 (SARGWP100)",
            "CO2 (SARGWP100)": "CO2",
            #"N2O (SARGWP100)": "N2O (SARGWP100)",
            #"Unspecified mix of HFCs and PFCs (SARGWP100)":
            #    "UnspMixOfHFCsPFCs (SARGWP100)",
            "Unspecified mix of HFCs (SARGWP100)": "UnspMixOfHFCs (SARGWP100)",
            "Unspecified mix of PFCs (SARGWP100)": "UnspMixOfPFCs (SARGWP100)",
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
        },
    },
}

di_processing_templates = {
    # templates fro the DI processing. Most processing rules will apply to several
    # versions. So we store them here and refer to them in the processing info dict
    'BFA': {
        'DI2022-08-22': { # remove 2007, seems to have summed sectors (Agri and LULUCF)
            # and missing sectors (e.g. 1,2 for CH4, N2O)
            'remove_years': ['2007'],
        },
    },
    'BIH': {
        'DI2022-08-22': {
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
                'entities': { # 2002-2014
                    'KYOTO': {
                        'basket': 'KYOTOGHG (SARGWP100)',
                        'basket_contents': ['CH4', 'CO2', 'N2O'],
                        'sel': {'category (BURDI)':
                                    ['1' ,'1.A' ,'1.A.1', '1.A.2', '1.A.3', '1.A.4',
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
}

di_processing_info = {
    # only countries with special processing listet
    # category conversion is defined on a country group level
    # the 'default' option is used if no specific option is found such that
    # processing of new versions can be done before creating a configuration for the
    # version.
    'BFA': {
        'default': di_processing_templates['BFA']['DI2022-08-22'],
        'DI2022-08-22': di_processing_templates['BFA']['DI2022-08-22'],
    },
    'BIH': {
        'default': di_processing_templates['BIH']['DI2022-08-22'],
        'DI2022-08-22': di_processing_templates['BIH']['DI2022-08-22'],
    },
}

gas_baskets = {
    'HFCS (SARGWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152a', 'HFC227ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc',  'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee', 'OTHERHFCS (SARGWP100)'],
    'HFCS (AR4GWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152a', 'HFC227ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc',  'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee', 'Unspecified mix of HFCs (AR4GWP100)'],
    'HFCS (AR5GWP100)': ['HFC23', 'HFC32', 'HFC41', 'HFC125', 'HFC134',
                         'HFC134a', 'HFC143',  'HFC143a', 'HFC152a', 'HFC227ea',
                         'HFC236fa', 'HFC245ca', 'HFC245fa', 'HFC365mfc',  'HFC404a',
                         'HFC407c', 'HFC410a', 'HFC4310mee'],
    'PFCS (SARGWP100)': ['C3F8', 'C4F10', 'CF4', 'C2F6', 'C6F14', 'C5F12', 'cC4F8'],
    'PFCS (AR4GWP100)': ['C3F8', 'C4F10', 'CF4', 'C2F6', 'C6F14', 'C5F12', 'cC4F8',  'Unspecified mix of PFCs (AR4GWP100)'],
    'PFCS (AR5GWP100)': ['C3F8', 'C4F10', 'CF4', 'C2F6', 'C6F14', 'C5F12', 'cC4F8'],
    'FGASES (SARGWP100)': ['HFCS (SARGWP100)', 'PFCS (SARGWP100)', 'SF6', 'NF3'],
    'FGASES (AR4GWP100)': ['HFCS (AR4GWP100)', 'PFCS (AR4GWP100)', 'SF6', 'NF3'],
    'FGASES (AR5GWP100)': ['HFCS (AR5GWP100)', 'PFCS (AR5GWP100)', 'SF6', 'NF3'],
    'KYOTOGHG (SARGWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (SARGWP100)', 'PFCS (SARGWP100)'],
    'KYOTOGHG (AR4GWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (AR4GWP100)', 'PFCS (AR4GWP100)',
                             'Unspecified mix of HFCs (AR4GWP100)', 'Unspecified mix of PFCs (AR4GWP100)'],
    'KYOTOGHG (AR5GWP100)': ['CO2', 'CH4', 'N2O', 'SF6', 'NF3', 'HFCS (AR5GWP100)', 'PFCS (AR5GWP100)'],
}