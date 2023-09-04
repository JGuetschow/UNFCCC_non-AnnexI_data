import pandas as pd
gwp_to_use = "AR4GWP100"


cat_names_fix = {
    '2A3 Glass Prod.': '2A3 Glass Production',
    '2F6 Other Applications': '2F6 Other Applications (please specify)',
    '3A2 Manure Mngmt': '3A2 Manure Mngmt.',
    '3C7 Rice Cultivations': '3C7 Rice Cultivation',
}

values_replacement = {
    '': '-',
    ' ': '-',
}

cols_for_space_stripping = ["Categories"]

index_cols = ["Categories", "entity", "unit"]

# parameters part 2: conversion to interchange format
cats_remove = ['Memo items', 'Information items']

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
    "scenario": "BUR3"
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

meta_data = {
    "references": "https://unfccc.int/documents/267685",
    "rights": "",
    "contact": "mail@johannes-guetschow.de",
    "title": "Malaysia - Third Biennial Update Report to the UNFCCC",
    "comment": "Read fom pdf file by Johannes Gütschow",
    "institution": "United Nations Framework Convention on Climate Change (UNFCCC)",
}

terminology_proc = coords_terminologies["category"]

table_def_templates = {
    '184': { #184
        "area": ['54,498,793,100'],
        "cols": ['150,197,250,296,346,394,444,493,540,587,637,685,738'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel Combustion', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other emissions',
                '1C Carbon Dioxide', '2 INDUSTRIAL', '2A1 Cement',
               ],
        },
    },
    '185': { #184
        "area": ['34,504,813,99'],
        "cols": ['128,177,224,273,321,373,425,473,519,564,611,661,713,765'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other',
                '1C Carbon Dioxide', '2 INDUSTRIAL', '2A Mineral',
                '2A1 Cement', '2A2 Lime',
               ],
        },
    },
    '186': { #also 200
        "area": ['53,498,786,104'],
        "cols": ['150,197,238,296,347,396,444,489,540,587,634,686,739'],
        "rows_to_fix": {
            3: ['2A3 Glass', '2A4 Other Process', '2A5 Other (please',
                '2B Chemical', '2B1 Ammonia', '2B2 Nitric Acid',
                '2B3 Adipic Acid', '2B4 Caprolactam,', '2B5 Carbide',
                '2B6 Titanium', '2B7 Soda Ash', '2B8 Petrochemical',
                '2B10 Other (Please', '2C1 Iron and Steel', '2C2 Ferroalloys'
               ],
            2: ['2B9 Fluorochemical'],
        },
    },
    '187': { # also 201
        "area": ['39,499,807,91'],
        "cols": ['132,185,232,280,327,375,425,470,522,568,613,664,713,763'],
        "rows_to_fix": {
            3: ['2A3 Glass', '2A4 Other Process', '2A5 Other (please',
                '2B Chemical', '2B1 Ammonia', '2B2 Nitric Acid',
                '2B3 Adipic Acid', '2B5 Carbide',
                '2B6 Titanium', '2B7 Soda Ash', '2B8 Petrochemical',
                '2B10 Other (Please', '2C1 Iron and Steel', '2C2 Ferroalloys',
               ],
            2: ['2B9 Fluorochemical'],
            5: ['2B4 Caprolactam,'],
        },
    },
    '188': {
        "area": ['48,503,802,92'],
        "cols": ['146,194,245,295,346,400,452,500,549,596,642,695,746'],
        "rows_to_fix": {
            3: ['2C3 Aluminium', '2C4 Magnesium', '2C7 Other (please',
                '2D Non-Energy', '2D2 Paraffin Wax', '2D4 Other (please',
                '2E Electronics', '2E1 Integrated', '2E5 Other (please',
                '2F1 Refrigeration',
               ],
            2: ['2E2 TFT Flat Panel', '2E4 Heat Transfer'],
            5: ['2F Product Uses as'],
        },
    },
    '189': {
        "area": ['41,499,806,95'],
        "cols": ['141,184,233,282,331,376,427,472,520,567,618,665,717,760'],
        "rows_to_fix": {
            3: ['2C3 Aluminium', '2C4 Magnesium', '2C7 Other (please',
                '2D Non-Energy', '2D2 Paraffin Wax', '2D4 Other (please',
                '2E Electronics', '2E1 Integrated', '2E5 Other (please',
                '2F1 Refrigeration',
               ],
            2: ['2E2 TFT Flat Panel', '2E4 Heat Transfer'],
            5: ['2F Product Uses as'],
        },
    },
    '190': {
        "area": ['45,500,802,125'],
        "cols": ['146,193,243,295,349,400,453,501,549,595,644,696,748'],
        "rows_to_fix": {
            3: ['2F2 Foam Blowing', '2F6 Other', '2G Other Product',
                '2G2 SF6 and PFCs', '2G4 Other (Please', '2H1 Pulp and Paper',
                '2H2 Food and', '2H3 Other (please', '3 AGRICULTURE,',
               ],
            2: ['2G1 Electrical', '2G3 N2O from', '3A1 Enteric'],
        },
    },
    '191': {
        "area": ['38,498,814,120'],
        "cols": ['130,180,229,277,326,381,429,477,526,570,620,669,717,765'],
        "rows_to_fix": {
            3: ['2F2 Foam Blowing', '2F6 Other', '2G Other Product',
                '2G2 SF6 and PFCs', '2G4 Other (Please', '2H1 Pulp and Paper',
                '2H2 Food and', '2H3 Other (please', '3 AGRICULTURE,',
               ],
            2: ['2G1 Electrical', '2G3 N2O from', '3A1 Enteric'],
        },
    },
    '192': {
        "area": ['39,502,807,106'],
        "cols": ['134,193,245,296,346,400,455,507,556,602,650,701,755'],
        "rows_to_fix": {
            3: ['3C1 Emissions from', '3C4 Direct N2O', '3C5 Indirect N2O',
                '3C6 Indirect N2O', '3C8 Other (please', '3D1 Harvested Wood',
                '3D2 Other (please',
               ],
            5: ['3C Aggregate',],
        },
    },
    '193': {
        "area": ['36,508,815,119'],
        "cols": ['128,179,228,278,327,379,428,476,525,571,622,670,717,766'],
        "rows_to_fix": {
            3: ['3C1 Emissions from', '3C4 Direct N2O', '3C5 Indirect N2O',
                '3C6 Indirect N2O', '3C8 Other (please', '3D1 Harvested',
                '3D2 Other (please',
               ],
            5: ['3C Aggregate',],
        },
    },
    '194': {
        "area": ['80,502,762,151'],
        "cols": ['201,243,285,329,376,419,462,502,551,591,635,679,724'],
        "rows_to_fix": {
            3: ['4C Incineration and', '4C2 Open Burning of', '4E Other',],
            2: ['4A1 Managed Waste', '4A2 Unmanaged Waste', '4A3 Uncategorised Waste',
                '4B Biological Treatment', '4D Wastewater', '4D1 Domestic Wastewater',
                '4D2 Industrial Wastewater',
               ],
            5: ['5A Indirect N2O'],
        },
    },
    '195': {
        "area": ['78,508,765,103'],
        "cols": ['191,230,271,314,352,400,438,475,519,566,600,645,686,730'],
        "rows_to_fix": {
            3: ['4C Incineration and', '4C2 Open Burning of', '4E Other',
                '4B Biological', '4D Wastewater', '4D1 Domestic',
                '4D2 Industrial', '5B Other (please'
               ],
            2: ['4A1 Managed Waste', '4A2 Unmanaged Waste', '4A3 Uncategorised',
                '4A Solid Waste',
               ],
            5: ['5A Indirect N2O'],
        },
    },
    '196': {
        "area": ['80,502,762,151'],
        "cols": ['201,243,285,329,376,419,462,502,551,591,635,679,724'],
        "rows_to_fix": {
            3: ['International Aviation', 'International Water-borne',
                'CO2 from Biomass Burning', 'For storage in other',
                'Long-term storage of', 'Annual change in total',
                'Annual change in long-',
               ],
        },
    },
    '197': {
        "area": ['74,507,779,201'],
        "cols": ['182,226,268,311,354,398,444,482,524,565,610,654,693,733'],
        "rows_to_fix": {
            3: ['International Aviation', 'International Water-',
                'CO2 from Biomass', 'For storage in other',
                'Long-term storage of', 'Annual change in total',
                'Annual change in long-',
               ],
        },
    },
    '198': { # first CH4 table
        "area": ['54,498,793,100'],
        "cols": ['140,197,250,296,346,394,444,493,540,587,637,685,738'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel Combustion', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other emissions',
                '1C Carbon Dioxide', '2 INDUSTRIAL', '2A1 Cement',
               ],
            -3: ['2A Mineral Industry'],
        },
    },
    '199': {
        "area": ['34,506,818,97'],
        "cols": ['132,177,228,276,329,377,432,479,528,574,618,667,722,774'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other',
                '1C Carbon Dioxide', '2 INDUSTRIAL', '2A1 Cement',
                '2A Mineral', '2A2 Lime',
               ],
        },
    },
    '202': {
        "area": ['48,503,802,92'],
        "cols": ['146,194,245,295,346,400,452,500,549,596,642,695,746'],
        "rows_to_fix": {
            3: ['2C3 Aluminium', '2C7 Other (please',
                '2D Non-Energy', '2D2 Paraffin Wax', '2D4 Other (please',
                '2E Electronics', '2E1 Integrated', '2E5 Other (please',
               ],
            2: ['2C4 Magnesium', '2E2 TFT Flat Panel', '2E4 Heat Transfer',
                '2F1 Refrigeration',
               ],
            5: ['2F Product Uses as'],
        },
    },
    '203': {
        "area": ['41,499,806,95'],
        "cols": ['141,184,233,282,331,376,427,472,520,567,618,665,717,760'],
        "rows_to_fix": {
            3: ['2C3 Aluminium', '2C7 Other (please',
                '2D Non-Energy', '2D2 Paraffin Wax', '2D4 Other (please',
                '2E Electronics', '2E1 Integrated', '2E5 Other (please',
               ],
            2: ['2C4 Magnesium', '2E2 TFT Flat Panel', '2E4 Heat Transfer',
                '2F1 Refrigeration'
               ],
            5: ['2F Product Uses as'],
        },
    },
    '204': {
        "area": ['45,500,802,125'],
        "cols": ['146,193,243,295,349,400,455,501,549,595,644,696,748'],
        "rows_to_fix": {
            3: ['2F6 Other', '2G Other Product',
                '2G2 SF6 and PFCs', '2G4 Other (Please', '2H1 Pulp and Paper',
                '2H2 Food and', '2H3 Other (please', '3 AGRICULTURE,',
                '3A1 Enteric',
               ],
            2: ['2F2 Foam Blowing', '2G1 Electrical', '2G3 N2O from'],
        },
    },
    '205': {
        "area": ['38,498,814,120'],
        "cols": ['130,180,229,277,326,381,429,477,526,570,620,669,717,765'],
        "rows_to_fix": {
            3: ['2F6 Other', '2G Other Product',
                '2G2 SF6 and PFCs', '2G4 Other (Please', '2H1 Pulp and Paper',
                '2H2 Food and', '2H3 Other (please', '3 AGRICULTURE,',
                '3A1 Enteric',
               ],
            2: ['2F2 Foam Blowing', '2G1 Electrical', '2G3 N2O from'],
        },
    },
    '206': { #also 220
        "area": ['39,502,807,106'],
        "cols": ['134,193,245,296,346,400,455,507,556,602,650,701,755'],
        "rows_to_fix": {
            3: ['3C1 Emissions from', '3C4 Direct N2O', '3C5 Indirect N2O',
                '3C6 Indirect N2O', '3C8 Other (please',
                '3D2 Other (please',
               ],
            2: ['3D1 Harvested Wood',],
            5: ['3C Aggregate',],
        },
    },
    '207': { # also 221
        "area": ['36,508,815,110'],
        "cols": ['128,179,228,278,327,379,428,476,527,571,622,670,717,766'],
        "rows_to_fix": {
            3: ['3C1 Emissions from', '3C4 Direct N2O', '3C5 Indirect N2O',
                '3C6 Indirect N2O', '3C8 Other (please',
                '3D2 Other (please',
               ],
            2: ['3D1 Harvested',],
            5: ['3C Aggregate',],
        },
    },
    '208': { # also 222
        "area": ['80,502,762,151'],
        "cols": ['201,243,285,329,376,419,462,502,551,591,635,679,724'],
        "rows_to_fix": {
            3: ['4C Incineration and', '4C2 Open Burning of', '4E Other',
                '4A1 Managed Waste', '4A2 Unmanaged Waste', '4A3 Uncategorised Waste',
                '4B Biological Treatment', '4D Wastewater', '4D1 Domestic Wastewater',
                '4D2 Industrial Wastewater'
               ],
            5: ['5A Indirect N2O'],
        },
    },
    '209': { # also 223
        "area": ['78,508,765,103'],
        "cols": ['191,230,271,314,352,400,438,475,519,560,600,645,686,730'],
        "rows_to_fix": {
            3: ['4C Incineration and', '4C2 Open Burning of', '4E Other',
                '4B Biological', '4D Wastewater', '4D1 Domestic',
                '4D2 Industrial', '5B Other (please',
                '4A1 Managed Waste', '4A2 Unmanaged Waste', '4A3 Uncategorised',
                '4A Solid Waste'
               ],
            5: ['5A Indirect N2O'],
        },
    },
    '210': { # also 224
        "area": ['80,502,762,151'],
        "cols": ['201,243,285,329,376,419,462,502,551,591,635,679,724'],
        "rows_to_fix": {
            3: ['International Aviation', 'International Water-borne',
                'Long-term storage of', 'Annual change in total',
                'Annual change in long-',
               ],
            2: ['CO2 from Biomass Burning', 'For storage in other',],
        },
    },
    '211': { # also 225
        "area": ['74,507,779,201'],
        "cols": ['182,226,268,311,354,398,444,482,524,565,610,654,693,733'],
        "rows_to_fix": {
            3: ['International Aviation', 'International Water-',
                'Long-term storage of', 'Annual change in total',
                'Annual change in long-', 'CO2 from Biomass',
               ],
            2: ['For storage in other',],
        },
    },
    '212': {
        "area": ['54,498,793,100'],
        "cols": ['150,197,250,296,346,394,444,493,540,587,637,685,738'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel Combustion', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other emissions',
                '1C Carbon Dioxide', '2 INDUSTRIAL',
               ],
            2: ['2A1 Cement',],
        },
    },
    '213': {
        "area": ['34,504,813,99'],
        "cols": ['128,177,224,273,321,373,425,473,519,564,611,661,713,765'],
        "rows_to_fix": {
            3: ['Total National', '1A Fuel', '1A1 Energy', '1A2 Manufacturing',
                '1B Fugitive', '1B2 Oil and Natural', '1B3 Other',
                '1C Carbon Dioxide', '2 INDUSTRIAL', '2A Mineral',
               ],
            2: ['2A1 Cement', '2A2 Lime',],
        },
    },
    '214': {
        "area": ['47,499,801,93'],
        "cols": ['141,197,246,297,350,396,453,502,550,595,642,692,748'],
        "rows_to_fix": {
            3: ['2A5 Other (please',
                '2B Chemical', '2B1 Ammonia', '2B2 Nitric Acid',
                '2B3 Adipic Acid', '2B4 Caprolactam,', '2B5 Carbide',
                '2B6 Titanium', '2B7 Soda Ash', '2B8 Petrochemical',
                '2B10 Other (Please', '2C1 Iron and Steel', '2C2 Ferroalloys'
               ],
            2: ['2A3 Glass', '2A4 Other Process', '2B9 Fluorochemical'],
            -3: ['2C Metal Industry'],
        },
    },
    '215': {
        "area": ['39,499,807,91'],
        "cols": ['132,180,232,280,327,375,425,470,522,568,613,664,713,763'],
        "rows_to_fix": {
            3: ['2A5 Other (please',
                '2B Chemical', '2B1 Ammonia', '2B2 Nitric Acid',
                '2B3 Adipic Acid', '2B4 Caprolactam,', '2B5 Carbide',
                '2B6 Titanium Dioxide', '2B7 Soda Ash', '2B8 Petrochemical',
                '2B10 Other (Please', '2C1 Iron and Steel', '2C2 Ferroalloys'
               ],
            2: ['2A4 Other Process', '2B9 Fluorochemical'],
            -3: ['2C Metal Industry'],
        },
    },
    '216': {
        "area": ['48,503,802,92'],
        "cols": ['146,194,245,295,346,400,452,500,549,596,642,695,746'],
        "rows_to_fix": {
            3: ['2C7 Other (please', '2D Non-Energy', '2D2 Paraffin Wax',
                '2D4 Other (please', '2E Electronics', '2E1 Integrated',
                '2E5 Other (please',
               ],
            2: ['2C3 Aluminium', '2C4 Magnesium', '2E2 TFT Flat Panel',
                '2E4 Heat Transfer', '2F1 Refrigeration',
               ],
            5: ['2F Product Uses as'],
        },
    },
    '217': {
        "area": ['41,499,806,95'],
        "cols": ['141,184,233,282,331,376,427,472,520,567,618,665,717,760'],
        "rows_to_fix": {
            3: ['2C7 Other (please', '2D Non-Energy', '2D2 Paraffin Wax',
                '2D4 Other (please', '2E Electronics', '2E1 Integrated',
                '2E5 Other (please',
               ],
            2: ['2C3 Aluminium', '2C4 Magnesium', '2E2 TFT Flat Panel',
                '2E4 Heat Transfer', '2F1 Refrigeration',
               ],
            5: ['2F Product Uses as'],
        },
    },
    '218': {
        "area": ['45,500,802,125'],
        "cols": ['146,193,243,295,349,400,455,501,549,595,644,696,748'],
        "rows_to_fix": {
            3: ['2F6 Other', '2G Other Product', '2G2 SF6 and PFCs',
                '2G3 N2O from', '2H3 Other (please', '3 AGRICULTURE,',
               ],
            2: ['2F2 Foam Blowing', '2G1 Electrical', '2G4 Other (Please',
                '2H1 Pulp and Paper', '2H2 Food and', '3A1 Enteric',],
        },
    },
    '219': {
        "area": ['38,498,814,120'],
        "cols": ['130,180,229,277,326,381,429,477,526,570,620,669,717,765'],
        "rows_to_fix": {
            3: ['2F6 Other', '2G Other Product', '2G2 SF6 and PFCs',
                '2G3 N2O from', '2H3 Other (please', '3 AGRICULTURE,',
               ],
            2: ['2F2 Foam Blowing', '2G1 Electrical', '2G4 Other (Please',
                '2H1 Pulp and Paper', '2H2 Food and', '3A1 Enteric',],
        },
    },
    '226': { # also 334, 238
        "area": ['48,510,797,99'],
        "cols": ['271,310,350,393,435,475,514,557,594,640,678,719,760'],
        "rows_to_fix": {
            2: ['2B4 Caprolactam, Glyoxal and Glyoxylic Acid'],
        }
    },
    '227': { # also 331, 335, 339
        "area": ['27,510,818,99'],
        "cols": ['250,290,333,372,413,452,494,536,576,616,656,699,739,781'],
        "rows_to_fix": {
            2: ['2B4 Caprolactam, Glyoxal and Glyoxylic Acid'],
        }
    },
    '228': {
        "area": ['48,510,797,99'],
        "cols": ['271,310,350,393,435,475,514,557,594,640,678,719,760'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone'],
            2: ['2D Non-Energy Products from Fuels and Solvent'],
        },
    },
    '229': {
        "area": ['25,512,819,86'],
        "cols": ['246,291,331,370,412,454,495,536,577,619,656,699,740,777'],
        "rows_to_fix": {
            3: ['2F Product Uses as Substitutes for Ozone'],
            2: ['2D Non-Energy Products from Fuels and Solvent'],
        },
    },
    '230': {
        "area": ['48,510,797,99'],
        "cols": ['271,310,350,393,435,475,514,557,594,640,678,719,760'],
        "rows_to_fix": {
            -3: ['Total National Emissions and Removals', '2 INDUSTRIAL PROCESSES AND PRODUCT USE'],
            2: ['2B4 Caprolactam, Glyoxal and Glyoxylic Acid'],
        }
    },
    '232': { # also 236
        "area": ['48,510,797,99'],
        "cols": ['271,310,350,393,435,475,514,557,594,640,678,719,760'],
        "rows_to_fix": {
            -3: ['2G2 SF6 and PFCs from Other Product Uses',],
            2: ['2D Non-Energy Products from Fuels and Solvent',
                '2F Product Uses as Substitutes for Ozone',]
        },
    },
    '233': {
        "area": ['25,512,819,86'],
        "cols": ['246,291,331,370,412,454,495,536,577,619,656,699,740,777'],
        "rows_to_fix": {
            -5: ['2F Product Uses as Substitutes for Ozone'],
            2: ['2D Non-Energy Products from Fuels and Solvent'],
            -3: ['2G Other Product Manufacture and Use',
                 '2G2 SF6 and PFCs from Other Product Uses',]
        },
    },
    '237': {
        "area": ['25,512,819,86'],
        "cols": ['246,291,331,370,412,454,495,536,577,619,656,699,740,777'],
        "rows_to_fix": {
            2: ['2D Non-Energy Products from Fuels and Solvent',
                '2F Product Uses as Substitutes for Ozone'],
        },
    },
    '240': {
        "area": ['48,510,797,99'],
        "cols": ['271,310,350,393,435,475,514,557,594,640,678,719,760'],
        "rows_to_fix": {
            2: ['2D Non-Energy Products from Fuels and Solvent',
                '2F Product Uses as Substitutes for Ozone'],
            -3: ['2E Electronics Industry',
                 '2F1 Refrigeration and Air Conditioning',
                 '2G2 SF6 and PFCs from Other Product Uses',],
        },
    },
    '241': {
        "area": ['25,512,819,86'],
        "cols": ['246,291,331,370,412,454,495,536,577,619,656,699,740,777'],
        "rows_to_fix": {
            2: ['2D Non-Energy Products from Fuels and Solvent',
                '2F Product Uses as Substitutes for Ozone',
                '2E1 Integrated Circuit or Semiconductor',],
            -3: ['2F1 Refrigeration and Air Conditioning',
                 '2G2 SF6 and PFCs from Other Product Uses',],
        },
    },
}

table_defs = {
    '184': {"template": '184', "entity": "CO2", "unit": "Gg CO2 / yr"}, #CO2
    '185': {"template": '185', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '186': {"template": '186', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '187': {"template": '187', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '188': {"template": '188', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '189': {"template": '189', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '190': {"template": '190', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '191': {"template": '191', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '192': {"template": '192', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '193': {"template": '193', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '194': {"template": '194', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '195': {"template": '195', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '196': {"template": '196', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '197': {"template": '197', "entity": "CO2", "unit": "Gg CO2 / yr"},
    '198': {"template": '198', "entity": "CH4", "unit": "Gg CH4 / yr"}, #CH4
    '199': {"template": '199', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '200': {"template": '186', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '201': {"template": '187', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '202': {"template": '202', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '203': {"template": '203', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '204': {"template": '204', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '205': {"template": '205', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '206': {"template": '206', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '207': {"template": '207', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '208': {"template": '208', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '209': {"template": '209', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '210': {"template": '210', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '211': {"template": '211', "entity": "CH4", "unit": "Gg CH4 / yr"},
    '212': {"template": '212', "entity": "N2O", "unit": "Gg N2O / yr"}, #N2O
    '213': {"template": '213', "entity": "N2O", "unit": "Gg N2O / yr"},
    '214': {"template": '214', "entity": "N2O", "unit": "Gg N2O / yr"},
    '215': {"template": '215', "entity": "N2O", "unit": "Gg N2O / yr"},
    '216': {"template": '216', "entity": "N2O", "unit": "Gg N2O / yr"},
    '217': {"template": '217', "entity": "N2O", "unit": "Gg N2O / yr"},
    '218': {"template": '218', "entity": "N2O", "unit": "Gg N2O / yr"},
    '219': {"template": '219', "entity": "N2O", "unit": "Gg N2O / yr"},
    '220': {"template": '206', "entity": "N2O", "unit": "Gg N2O / yr"},
    '221': {"template": '207', "entity": "N2O", "unit": "Gg N2O / yr"},
    '222': {"template": '208', "entity": "N2O", "unit": "Gg N2O / yr"},
    '223': {"template": '209', "entity": "N2O", "unit": "Gg N2O / yr"},
    '224': {"template": '210', "entity": "N2O", "unit": "Gg N2O / yr"},
    '225': {"template": '211', "entity": "N2O", "unit": "Gg N2O / yr"},
    '226': {"template": '226', "entity": "HFCS (AR4GWP100)", "unit": "Gg CO2 / yr"}, #HFCs
    '227': {"template": '227', "entity": "HFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '228': {"template": '228', "entity": "HFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '229': {"template": '229', "entity": "HFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '230': {"template": '230', "entity": "PFCS (AR4GWP100)", "unit": "Gg CO2 / yr"}, #PFCs
    '231': {"template": '227', "entity": "PFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '232': {"template": '232', "entity": "PFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '233': {"template": '233', "entity": "PFCS (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '234': {"template": '226', "entity": "SF6 (AR4GWP100)", "unit": "Gg CO2 / yr"}, #SF6
    '235': {"template": '227', "entity": "SF6 (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '236': {"template": '232', "entity": "SF6 (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '237': {"template": '237', "entity": "SF6 (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '238': {"template": '226', "entity": "NF3 (AR4GWP100)", "unit": "Gg CO2 / yr"}, #NF3
    '239': {"template": '227', "entity": "NF3 (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '240': {"template": '240', "entity": "NF3 (AR4GWP100)", "unit": "Gg CO2 / yr"},
    '241': {"template": '241', "entity": "NF3 (AR4GWP100)", "unit": "Gg CO2 / yr"},
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