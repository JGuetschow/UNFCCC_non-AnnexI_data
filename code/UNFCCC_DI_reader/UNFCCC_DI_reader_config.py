di_query_filters = [
    'classifications', 'measures', 'gases',
]
# category, party are extra
# measure is preprocessed to find ids


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


