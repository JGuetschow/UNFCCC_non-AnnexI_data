""" CRF2022 specification.
Currently not all tables are included. Extend if you need all country
specific items in categories 2, 3.H-G, 4

tables included:
* Energy
    'Table1s1', Table1s2',
    'Table1.A(a)s1', 'Table1.A(a)s2', 'Table1.A(a)s3', 'Table1.A(a)s4',
    'Table1.B.1', 'Table1.B.2', 'Table1.C', 'Table1.D',
* Industrial processes
    'Table2(I)s1', 'Table2(I)s2',
    'Table2(II)',
* Agriculture
    'Table3s1', 'Table3s2',
    'Table3.C', 'Table3.D', 'Table3.E',
* LULUCF
    'Table4',
* Waste
    'Table5', 'Table5.A', 'Table5.B', 'Table5.C', 'Table5.D'
* Summary Tables (for "Other" and to check for consistency)

missing tables are:
* Energy
    'Table1.D'
* Industrial processes
    'Table2(I).A-Hs1', 'Table2(I).A-Hs2',
    'Table2(II)B-Hs1', 'Table2(II)B-Hs2',
* Agriculture
    'Table3.As1', 'Table3.As2' (no additional emissions data)
    'Table3.F', 'Table3.G-I',
* LULUCF
    All tables except Table4
* Waste
    All tables read

TODO:
* Add missing tables
* Add activity data

"""

import numpy as np
from .util import unit_info

# TODO: GWPs now differ by country. This has to be implemented (maybe giving
#  gwp_to_use as a parameter to the specification)
gwp_to_use = "AR5GWP100"

CRF2023 = {
    "Table1s1": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 26,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['Total Energy', ['1']],
            ['A. Fuel combustion activities (sectoral approach)', ['1.A']],
            ['1. Energy industries', ['1.A.1']],
            ['a. Public electricity and heat production', ['1.A.1.a']],
            ['b. Petroleum refining', ['1.A.1.b']],
            ['c. Manufacture of solid fuels and other energy industries', ['1.A.1.c']],
            ['2. Manufacturing industries and construction', ['1.A.2']],
            ['a. Iron and steel', ['1.A.2.a']],
            ['b. Non-ferrous metals', ['1.A.2.b']],
            ['c. Chemicals', ['1.A.2.c']],
            ['d. Pulp, paper and print', ['1.A.2.d']],
            ['e. Food processing, beverages and tobacco', ['1.A.2.e']],
            ['f. Non-metallic minerals', ['1.A.2.f']],
            ['g. Other (please specify)', ['1.A.2.g']],
            ['3. Transport', ['1.A.3']],
            ['a. Domestic aviation', ['1.A.3.a']],
            ['b. Road transportation', ['1.A.3.b']],
            ['c. Railways', ['1.A.3.c']],
            ['d. Domestic navigation', ['1.A.3.d']],
            ['e. Other transportation', ['1.A.3.e']],
        ],
        "entity_mapping": {
            "NOX": "NOx",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1s2": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 36,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['4. Other sectors', ['1.A.4']],
            ['a. Commercial/institutional', ['1.A.4.a']],
            ['b. Residential', ['1.A.4.b']],
            ['c. Agriculture/forestry/fishing', ['1.A.4.c']],
            ['5. Other (as specified in table 1.A(a) sheet 4)', ['1.A.5']],
            ['a. Stationary', ['1.A.5.a']],
            ['b. Mobile', ['1.A.5.b']],
            ['B. Fugitive emissions from fuels', ['1.B']],
            ['1. Solid fuels', ['1.B.1']],
            ['a. Coal mining and handling', ['1.B.1.a']],
            ['b. Solid fuel transformation', ['1.B.1.b']],
            ['c. Other (as specified in table 1.B.1)', ['1.B.1.c']],
            ['2. Oil and natural gas and other emissions from energy production', ['1.B.2']],
            ['a. Oil', ['1.B.2.a']],
            ['b. Natural gas', ['1.B.2.b']],
            ['c. Venting and flaring', ['1.B.2.c']],
            ['d. Other (as specified in table 1.B.2)', ['1.B.2.d']],
            ['C. CO2 Transport and storage', ['1.C']],
            ['1. Transport of CO2', ['1.C.1']],
            ['2. Injection and storage', ['1.C.2']],
            ['3. Other', ['1.C.3']],
            ['Memo items: (1)', ['\IGNORE']],
            ['International bunkers', ['M.Memo.Int']],
            ['Aviation', ['M.Memo.Int.Avi']],
            ['Navigation', ['M.Memo.Int.Mar']],
            ['Multilateral operations', ['M.Memo.Mult']],
            ['CO2 emissions from biomass', ['M.Memo.Bio']],
            ['CO2 captured', ['M.Memo.CO2Cap']],
            ['For domestic storage', ['M.Memo.CO2Cap.Dom']],
            ['For storage in other countries', ['M.Memo.CO2Cap.Exp']],
        ],
        "entity_mapping": {
            "NOX": "NOx",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.A(a)s1": {
        "status": "tested",
        "table": {
            "firstrow": 6,
            "lastrow": 104,  # template, countries report less
            # check the resulting data as the templates have nan rows
            # which would stop the reading process (actual reported
            # data does not seem to have the nan rows)
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2(1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'EMISSIONS CO2 Amount captured'
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A. Fuel combustion', ['1.A', 'Total'], 0],
            ['Liquid fuels', ['1.A', 'Liquid'], 1],
            ['Solid fuels', ['1.A', 'Solid'], 1],
            ['Gaseous fuels', ['1.A', 'Gaseous'], 1],
            ['Other fossil fuels(4)', ['1.A', 'OtherFF'], 1],
            ['Peat(5)', ['1.A', 'Peat'], 1],
            ['Biomass(6)', ['1.A', 'Biomass'], 1],
            # 1.A.1. Energy industries
            ['1.A.1. Energy industries', ['1.A.1', 'Total'], 1],
            ['Liquid fuels', ['1.A.1', 'Liquid'], 2],
            ['Solid fuels', ['1.A.1', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.1', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.1', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.1', 'Peat'], 2],
            ['Biomass(6)', ['1.A.1', 'Biomass'], 2],
            # a. Public electricity and heat production
            ['a. Public electricity and heat production(7)', ['1.A.1.a', 'Total'], 2],
            ['Liquid fuels', ['1.A.1.a', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.a', 'Solid'], 3],
            ['Gaseous fuels', ['1.A.1.a', 'Gaseous'], 3],
            ['Other fossil fuels(4)', ['1.A.1.a', 'OtherFF'], 3],
            ['Peat(5)', ['1.A.1.a', 'Peat'], 3],
            ['Biomass(6)', ['1.A.1.a', 'Biomass'], 3],
            # 1.A.1.a.i Electricity Generation
            ['1.A.1.a.i Electricity Generation', ['1.A.1.a.i', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.i', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.i', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.a.i', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.i', 'OtherFF'], 4],
            ['Peat', ['1.A.1.a.i', 'Peat'], 4],
            ['Biomass', ['1.A.1.a.i', 'Biomass'], 4],
            # 1.A.1.a.ii Combined heat and power generation
            ['1.A.1.a.ii Combined heat and power generation', ['1.A.1.a.ii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.ii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.ii', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.a.ii', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.ii', 'OtherFF'], 4],
            ['Peat', ['1.A.1.a.ii', 'Peat'], 4],
            ['Biomass', ['1.A.1.a.ii', 'Biomass'], 4],
            # 1.A.1.a.iii heat plants
            ['1.A.1.a.iii Heat plants', ['1.A.1.a.iii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.iii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.iii', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.a.iii', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.iii', 'OtherFF'], 4],
            ['Peat', ['1.A.1.a.iii', 'Peat'], 4],
            ['Biomass', ['1.A.1.a.iii', 'Biomass'], 4],
            # 1.A.1.a.iv Other (please specify)
            ['1.A.1.a.iv Other (please specify)', ['1.A.1.a.iv', 'Total'], 3],
            # AUT
            ['Total Public Electricity and Heat Production', ['1.A.1.a.iv.4', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.a.iv.4', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.a.iv.4', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.a.iv.4', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.a.iv.4', 'OtherFF'], 5],
            ['Peat', ['1.A.1.a.iv.4', 'Peat'], 5],
            ['Biomass', ['1.A.1.a.iv.4', 'Biomass'], 5],
            # DEU
            ['1.A.1.a Public Electricity and Heat Production', ['1.A.1.a.iv.4', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.a.iv.4', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.a.iv.4', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.a.iv.4', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.a.iv.4', 'OtherFF'], 5],
            ['Peat', ['1.A.1.a.iv.4', 'Peat'], 5],
            ['Biomass', ['1.A.1.a.iv.4', 'Biomass'], 5],
            # ESP
            ['Other', ['1.A.1.a.iv.3', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.a.iv.3', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.a.iv.3', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.a.iv.3', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.a.iv.3', 'OtherFF'], 5],
            ['Peat', ['1.A.1.a.iv.3', 'Peat'], 5],
            ['Biomass', ['1.A.1.a.iv.3', 'Biomass'], 5],
            # SVK
            ['Methane Cogeneration (Mining)', ['1.A.1.a.iv.1', 'Total'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.iv.1', 'OtherFF'], 5],
            ['Municipal Solid Waste Incineration (Energy use)', ['1.A.1.a.iv.2', 'Total'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.iv.2', 'OtherFF'], 5],
            ['Biomass', ['1.A.1.a.iv.2', 'Biomass'], 5],
            # CHE
            ['Municipal and special waste incineration plants', ['1.A.1.a.iv.2', 'Total'], 4],
            ['Other Fossil Fuels', ['1.A.1.a.iv.2', 'OtherFF'], 5],
            ['Biomass', ['1.A.1.a.iv.2', 'Biomass'], 5],
            # b. Petroleum refining
            ['b. Petroleum refining', ['1.A.1.b', 'Total'], 2],
            ['Liquid fuels', ['1.A.1.b', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.b', 'Solid'], 3],
            ['Gaseous fuels', ['1.A.1.b', 'Gaseous'], 3],
            ['Other fossil fuels(4)', ['1.A.1.b', 'OtherFF'], 3],
            ['Peat(5)', ['1.A.1.b', 'Peat'], 3],
            ['Biomass(6)', ['1.A.1.b', 'Biomass'], 3],
            # c. Manufacture of solid fuels and other energy industries
            ['c. Manufacture of solid fuels and other energy industries(8)', ['1.A.1.c', 'Total'], 2],
            ['Liquid fuels', ['1.A.1.c', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.c', 'Solid'], 3],
            ['Gaseous fuels', ['1.A.1.c', 'Gaseous'], 3],
            ['Other fossil fuels(4)', ['1.A.1.c', 'OtherFF'], 3],
            ['Peat(5)', ['1.A.1.c', 'Peat'], 3],
            ['Biomass(6)', ['1.A.1.c', 'Biomass'], 3],
            # 1.A.1.c.i Manufacture of solid fuels
            ['1.A.1.c.i Manufacture of solid fuels', ['1.A.1.c.i', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.i', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.i', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.c.i', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.c.i', 'OtherFF'], 4],
            ['Peat', ['1.A.1.c.i', 'Peat'], 4],
            ['Biomass', ['1.A.1.c.i', 'Biomass'], 4],
            # 1.A.1.c.ii Oil and gas extraction
            ['1.A.1.c.ii Oil and gas extraction', ['1.A.1.c.ii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.ii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.ii', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.c.ii', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.c.ii', 'OtherFF'], 4],
            ['Peat', ['1.A.1.c.ii', 'Peat'], 4],
            ['Biomass', ['1.A.1.c.ii', 'Biomass'], 4],
            # 1.A.1.c.iii Other energy industries
            ['1.A.1.c.iii Other energy industries', ['1.A.1.c.iii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.iii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.iii', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.1.c.iii', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.1.c.iii', 'OtherFF'], 4],
            ['Peat', ['1.A.1.c.iii', 'Peat'], 4],
            ['Biomass', ['1.A.1.c.iii', 'Biomass'], 4],
            # 1.A.1.c.iv Other (please specify)
            ['1.A.1.c.iv Other (please specify)', ['1.A.1.c.iv', 'Total'], 3],
            # DEU
            ['1.A.1.c Manufacture of Solid Fuels and Other Energy Industries', ['1.A.1.c.iv.2', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.c.iv.2', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.c.iv.2', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.c.iv.2', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.c.iv.2', 'OtherFF'], 5],
            ['Peat', ['1.A.1.c.iv.2', 'Peat'], 5],
            ['Biomass', ['1.A.1.c.iv.2', 'Biomass'], 5],
            # ESP
            ['Other', ['1.A.1.c.iv.3', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.c.iv.3', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.c.iv.3', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.c.iv.3', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.c.iv.3', 'OtherFF'], 5],
            ['Peat', ['1.A.1.c.iv.3', 'Peat'], 5],
            ['Biomass', ['1.A.1.c.iv.3', 'Biomass'], 5],
            # CYP
            ['Charcoal Production', ['1.A.1.c.iv.1', 'Total'], 4],
            ['Liquid Fuels', ['1.A.1.c.iv.1', 'Liquid'], 5],
            ['Solid Fuels', ['1.A.1.c.iv.1', 'Solid'], 5],
            ['Gaseous Fuels', ['1.A.1.c.iv.1', 'Gaseous'], 5],
            ['Other Fossil Fuels', ['1.A.1.c.iv.1', 'OtherFF'], 5],
            ['Peat', ['1.A.1.c.iv.1', 'Peat'], 5],
            ['Biomass', ['1.A.1.c.iv.1', 'Biomass'], 5],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2(2)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # tested
    "Table1.A(a)s2": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 114,  # template, countries report less
            # check the resulting data as the templates have nan rows
            # which would stop the reading process (actual reported
            # data does not seem to have the nan rows)
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2(1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'EMISSIONS CO2 Amount captured',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.2 Manufacturing industries and construction', ['1.A.2', 'Total'], 0],
            ['Liquid fuels', ['1.A.2', 'Liquid'], 1],
            ['Solid fuels', ['1.A.2', 'Solid'], 1],
            ['Gaseous fuels', ['1.A.2', 'Gaseous'], 1],
            ['Other fossil fuels(4)', ['1.A.2', 'OtherFF'], 1],
            ['Peat(5)', ['1.A.2', 'Peat'], 1],
            ['Biomass(6)', ['1.A.2', 'Biomass'], 1],
            # a. Iron and Steel
            ['a. Iron and steel', ['1.A.2.a', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.a', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.a', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.a', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.a', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.a', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.a', 'Biomass'], 2],
            # b. non-ferrous metals
            ['b. Non-ferrous metals', ['1.A.2.b', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.b', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.b', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.b', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.b', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.b', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.b', 'Biomass'], 2],
            # c. Chemicals
            ['c. Chemicals', ['1.A.2.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.c', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.c', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.c', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.c', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.c', 'Biomass'], 2],
            # d. Pulp paper print
            ['d. Pulp, paper and print', ['1.A.2.d', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.d', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.d', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.d', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.d', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.d', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.d', 'Biomass'], 2],
            # e. Food processing, beverages and tobacco
            ['e. Food processing, beverages and tobacco', ['1.A.2.e', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.e', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.e', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.e', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.e', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.e', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.e', 'Biomass'], 2],
            # f. non-metallic minerals
            ['f. Non-metallic minerals', ['1.A.2.f', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.f', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.f', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.2.f', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.2.f', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.2.f', 'Peat'], 2],
            ['Biomass(6)', ['1.A.2.f', 'Biomass'], 2],
            # g. other
            ['g. Other (please specify)(9)', ['1.A.2.g', 'Total'], 1],
            #1.A.2.g.i Manufacturing of machinery
            ['1.A.2.g.i Manufacturing of machinery', ['1.A.2.g.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.i', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.i', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.i', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.i', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.i', 'Biomass'], 3],
            # 1.A.2.g.ii Manufacturing of transport equipment
            ['1.A.2.g.ii Manufacturing of transport equipment', ['1.A.2.g.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.ii', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.ii', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.ii', 'Biomass'], 3],
            # 1.A.2.g.iii Mining (excluding fuels) and quarrying
            ['1.A.2.g.iii Mining (excluding fuels) and quarrying', ['1.A.2.g.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.iii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.iii', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.iii', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.iii', 'Biomass'], 3],
            # 1.A.2.g.iv Wood and wood products
            ['1.A.2.g.iv Wood and wood products', ['1.A.2.g.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.iv', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.iv', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.iv', 'Biomass'], 3],
            # 1.A.2.g.v Construction
            ['1.A.2.g.v Construction', ['1.A.2.g.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.v', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.v', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.v', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.v', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.v', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.v', 'Biomass'], 3],
            # 1.A.2.g.vi Textile and leather
            ['1.A.2.g.vi Textile and leather', ['1.A.2.g.vi', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.vi', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.vi', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.vi', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.vi', 'OtherFF'], 3],
            ['Peat', ['1.A.2.g.vi', 'Peat'], 3],
            ['Biomass', ['1.A.2.g.vi', 'Biomass'], 3],
            # 1.A.2.g.vii Off-road vehicles and other machinery
            ['1.A.2.g.vii Off-road vehicles and other machinery', ['1.A.2.g.vii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.vii', 'Liquid'], 3],
            ['Gaseous Fuels', ['1.A.2.g.vii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.2.g.vii', 'OtherFF'], 3],
            ['Biomass', ['1.A.2.g.vii', 'Biomass'], 3],
            # 1.A.2.g.viii Other (please specify)
            ['1.A.2.g.viii Other (please specify)', ['1.A.2.g.viii', 'Total'], 2],
            # DKE
            ['Construction', ['\IGNORE', '\IGNORE'], 3],  # (empty)
            ['Mining', ['\IGNORE', '\IGNORE'], 3],  # (empty)
            # DNK, DKE, USA, CZE
            ['Other non-specified', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            #SVK, CYP
            ['Non-specified Industry', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            #BEL
            ['Other non specified', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            #PRT, LTU
            ['Non-specified industry', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            # MLT
            ['Undefined Industry', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            # TUR
            ['Other unspecified', ['1.A.2.g.viii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.1', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.1', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.1', 'Biomass'], 4],
            # DKE
            ['Textile', ['\IGNORE', '\IGNORE'], 3],  # (empty)
            # DNK, DNM, FIN, DKE
            ['Other manufacturing industries', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.3', 'Biomass'], 4],
            # CAN
            ['Other Manufacturing', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.3', 'Biomass'], 4],
            # AUT, LUX
            ['Other Manufacturing Industries', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.3', 'Biomass'], 4],
            # NOR
            ['Other manufacturing', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.3', 'Biomass'], 4],
            # AUS
            ['All Other Manufacturing', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.3', 'Biomass'], 4],
            # NLD
            ['Other Industrial Sectors', ['1.A.2.g.viii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.4', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.4', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.4', 'Biomass'], 4],
            # GBR, GBK
            ['Other industry (not specified above)', ['1.A.2.g.viii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.4', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.4', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.4', 'Biomass'], 4],
            # UKR
            ['Oter Industries', ['1.A.2.g.viii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.4', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.4', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.4', 'Biomass'], 4],
            # RUS
            ['Other industries', ['1.A.2.g.viii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.4', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.4', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.4', 'Biomass'], 4],
            # RUS
            ['Non-CO2 emissions from BFG combustion', ['1.A.2.g.viii.5', 'Total'], 3],
            ['Solid Fuels', ['1.A.2.g.viii.5', 'Solid'], 4],
            # BLR, DNK, ESP, LVA, NZL, POL, ROU, SVN,
            ['Other', ['1.A.2.g.viii.10', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.10', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.10', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.10', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.10', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.10', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.10', 'Biomass'], 4],
            # BLR
            ['Manufacture and construction Aggregated', ['1.A.2.g.viii.2', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.2', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.2', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.2', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.2', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.2', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.2', 'Biomass'], 4],
            # HRV
            ['Other Industry', ['1.A.2.g.viii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.4', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.4', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.4', 'Biomass'], 4],
            # HRV
            ['1A2 Total for 1990 to 2000', ['1.A.2.g.viii.2', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.2', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.2', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.2', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.2', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.2', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.2', 'Biomass'], 4],
            # MLT
            ['All Industry', ['1.A.2.g.viii.2', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.2', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.2', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.2', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.2', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.2', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.2', 'Biomass'], 4],
            # PRT
            ['Rubber', ['1.A.2.g.viii.6', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.6', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.6', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.6', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.6', 'OtherFF'], 4],
            ['Biomass', ['1.A.2.g.viii.6', 'Biomass'], 4],
            # SWE
            ['All stationary combustin within CRF 1.A.2.g', ['1.A.2.g.viii.7', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.7', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.7', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.7', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.7', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.7', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.7', 'Biomass'], 4],
            # IRL
            ['Other stationary combustion', ['1.A.2.g.viii.8', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.8', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.8', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.8', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.8', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.8', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.8', 'Biomass'], 4],
            # HUN
            ['Other Stationary Combustion', ['1.A.2.g.viii.8', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.8', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.8', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.8', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.8', 'OtherFF'], 4],
            ['Peat', ['1.A.2.g.viii.8', 'Peat'], 4],
            ['Biomass', ['1.A.2.g.viii.8', 'Biomass'], 4],
            # CHE
            ['Other Boilers and Engines Industry', ['1.A.2.g.viii.9', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.9', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.9', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.2.g.viii.9', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.2.g.viii.9', 'OtherFF'], 4],
            ['Biomass', ['1.A.2.g.viii.9', 'Biomass'], 4],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2(2)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # tested
    "Table1.A(a)s3": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 115,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2(1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
            ],
            "stop_cats": ["Note: All footnotes for this table are given at the end of the table on sheet 4.", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.3 Transport', ['1.A.3', 'Total'], 0],
            ['Liquid fuels', ['1.A.3', 'Liquid'], 1],
            ['Solid fuels', ['1.A.3', 'Solid'], 1],
            ['Gaseous fuels', ['1.A.3', 'Gaseous'], 1],
            ['Other fossil fuels(4)', ['1.A.3', 'OtherFF'], 1],
            ['Biomass(6)', ['1.A.3', 'Biomass'], 1],
            # a. Domestic Aviation
            ['a. Domestic aviation(10)', ['1.A.3.a', 'Total'], 1],
            ['Aviation gasoline', ['1.A.3.a', 'AvGasoline'], 2],
            ['Jet kerosene', ['1.A.3.a', 'JetKerosene'], 2],
            ['Biomass', ['1.A.3.a', 'Biomass'], 2],
            # b. road Transportation
            ['b. Road transportation(11)', ['1.A.3.b', 'Total'], 1],
            ['Gasoline', ['1.A.3.b', 'Gasoline'], 2],
            ['Diesel oil', ['1.A.3.b', 'DieselOil'], 2],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b', 'LPG'], 2],
            ['Other liquid fuels (please specify)', ['1.A.3.b', 'OtherLiquid'], 2],
            ['Gaseous fuels', ['1.A.3.b', 'Gaseous'], 2],
            ['Biomass(6)', ['1.A.3.b', 'Biomass'], 2],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.b', 'OtherFF'], 2],
            # i. Cars
            ['i. Cars', ['1.A.3.b.i', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.i', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.i', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.i', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.i', 'OtherLiquid'], 3],
            ['Kerosene', ['1.A.3.b.i', 'Kerosene'], 4],  # UKR (and probably others)
            ['Lubricants', ['1.A.3.b.i', 'Lubricants'], 4],  # UKR, JPN
            ['Lubricant oil', ['1.A.3.b.i', 'Lubricants'], 4],  # PRT
            ['Biodiesel (5 percent fossil portion)', ['1.A.3.b.i', 'OLBiodieselFC'], 4],  # CAN
            ['Fossil part of biodiesel', ['1.A.3.b.i', 'OLBiodieselFC'], 4],  # LTU
            ['Other', ['1.A.3.b.i', 'OLOther'], 4],  # UKR, MLT
            ['Other Liquid Fuels', ['1.A.3.b.i', 'OLOther'], 4],  # CYP
            ['Other non-specified', ['1.A.3.b.i', 'OLOther'], 4],  # SWE new in 2023
            ['Other motor fuels', ['1.A.3.b.i', 'OMotorFuels'], 4],  # RUS
            ['Lubricants in 2-stroke engines', ['1.A.3.b.i', 'Lubricants'], 4],  # HUN
            ['LNG', ['1.A.3.b.i', 'LNG'], 4],  ## USA
            ['Gaseous fuels', ['1.A.3.b.i', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.3.b.i', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.b.i', 'OtherFF'], 3],
            ['Other Fossil Fuels', ['1.A.3.b.i', 'OFFOther'], 4],  # CYP, POL
            ['Biodiesel (fossil component)', ['1.A.3.b.i', 'OFFBiodieselFC'], 4],  # LUX
            ['Biodiesel fossil fraction', ['1.A.3.b.i', 'OFFBiodieselFC'], 4],  # NOR
            ['Biodiesel (fossil fraction)', ['1.A.3.b.i', 'OFFBiodieselFC'], 4],  # NZL
            ['Fossil part of biodiesel or biogasoline', ['1.A.3.b.i', 'OFFBiofuelFC'], 4],  # PRT
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.b.i', 'OFFBiofuelFC'], 4],  # SWE
            ['fossil part of biofuels', ['1.A.3.b.i', 'OFFBiofuelFC'], 4],  # CZE
            ['fossil part of biodiesel', ['1.A.3.b.i', 'OFFBiodieselFC'], 4],  # DKE, DNK, HRV
            ['Fossil part of biodiesel', ['1.A.3.b.i', 'OFFBiodieselFC'], 4],  # DNM, BEL, HUN, LVA, ESP
            ['Fossil part of biogasoline', ['1.A.3.b.i', 'OFFBiogasolineFC'], 4],  # BEL
            ['Natural Gas', ['1.A.3.b.i', 'OFFNaturalGas'], 4],  # USA
            ['Fossil part of biofuel', ['1.A.3.b.i', 'OFFBiofuelFC'], 4],  # IRL
            ['Other', ['1.A.3.b.i', 'OFFOther'], 4],  # MLT
            # ii. Light duty trucks
            ['ii. Light duty trucks', ['1.A.3.b.ii', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.ii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.ii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.ii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.ii', 'OtherLiquid'], 3],
            ['Kerosene', ['1.A.3.b.ii', 'Kerosene'], 4],  # UKR (and probably others)
            ['Lubricants', ['1.A.3.b.ii', 'Lubricants'], 4],  # UKR, JPN
            ['Lubricant Oil', ['1.A.3.b.ii', 'Lubricants'], 4],  # PRT
            ['Biodiesel (5 percent fossil portion)', ['1.A.3.b.ii', 'OLBiodieselFC'], 4],  # CAN
            ['Other', ['1.A.3.b.ii', 'OLOther'], 4],  # UKR (and probably others)
            ['Other Liquid Fuels', ['1.A.3.b.ii', 'OLOther'], 4],  # CYP
            ['Other non-specified', ['1.A.3.b.ii', 'OLOther'], 4],  # SWE new in 2023
            ['Other motor fuels', ['1.A.3.b.ii', 'OMotorFuels'], 4],  # RUS
            ['LNG', ['1.A.3.b.ii', 'LNG'], 4],  ## USA
            ['Gaseous fuels', ['1.A.3.b.ii', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.3.b.ii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.b.ii', 'OtherFF'], 3],
            ['Other Fossil Fuels', ['1.A.3.b.ii', 'OFFOther'], 4],  # CYP, POL
            ['Biodiesel (fossil component)', ['1.A.3.b.ii', 'OFFBiodieselFC'], 4],  # LUX
            ['Biodiesel fossil fraction', ['1.A.3.b.ii', 'OFFBiodieselFC'], 4],  # NOR
            ['Biodiesel (fossil fraction)', ['1.A.3.b.ii', 'OFFBiodieselFC'], 4],  # NZL
            ['Fossil part of biodiesel or biogasoline', ['1.A.3.b.ii', 'OFFBiofuelFC'], 4],  # PRT
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.b.ii', 'OFFBiofuelFC'], 4],  # SWE
            ['fossil part of biofuels', ['1.A.3.b.ii', 'OFFBiofuelFC'], 4],  # CZE
            ['fossil part of biodiesel', ['1.A.3.b.ii', 'OFFBiodieselFC'], 4],  # DKE, DNK, HRV
            ['Fossil part of biodiesel', ['1.A.3.b.ii', 'OFFBiodieselFC'], 4],  # DNM, BEL, HUN, LVA, ESP
            ['Fossil part of biogasoline', ['1.A.3.b.ii', 'OFFBiogasolineFC'], 4],  # BEL
            ['Fossil part of biofuel', ['1.A.3.b.ii', 'OFFBiofuelFC'], 4],  # IRL
            # iii. Heavy duty trucks and buses
            ['iii. Heavy duty trucks and buses', ['1.A.3.b.iii', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.iii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.iii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.iii', 'LPG'], 3],
            ['Other liquid fFuels (please specify)', ['1.A.3.b.iii', 'OtherLiquid'], 3],
            ['Kerosene', ['1.A.3.b.iii', 'Kerosene'], 4],  # UKR (and probably others)
            ['Lubricants', ['1.A.3.b.iii', 'Lubricants'], 4],  # UKR, JPN
            ['Lubricant Oil', ['1.A.3.b.iii', 'Lubricants'], 4],  # PRT
            ['Biodiesel (5 percent fossil portion)', ['1.A.3.b.iii', 'OLBiodieselFC'], 4],  # CAN
            ['Other', ['1.A.3.b.iii', 'OLOther'], 4],  # UKR (and probably others)
            ['Other Liquid Fuels', ['1.A.3.b.iii', 'OLOther'], 4],  # CYP
            ['Other non-specified', ['1.A.3.b.iii', 'OLOther'], 4],  # SWE new in 2023
            ['Other motor fuels', ['1.A.3.b.iii', 'OMotorFuels'], 4],  # RUS
            ['LNG', ['1.A.3.b.iii', 'LNG'], 4],  # USA
            ['GTL', ['1.A.3.b.iii', 'GTL'], 4],  # MCO, new in 2022
            ['Gaseous fuels', ['1.A.3.b.iii', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.3.b.iii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.b.iii', 'OtherFF'], 3],
            ['Other Fossil Fuels', ['1.A.3.b.iii', 'OFFOther'], 4],  # CYP, POL
            ['Biodiesel (fossil component)', ['1.A.3.b.iii', 'OFFBiodieselFC'], 4],  # LUX
            ['Biodiesel fossil fraction', ['1.A.3.b.iii', 'OFFBiodieselFC'], 4],  # NOR
            ['Biodiesel (fossil fraction)', ['1.A.3.b.iii', 'OFFBiodieselFC'], 4],  # NZL
            ['Fossil part of biodiesel or biogasoline', ['1.A.3.b.iii', 'OFFBiofuelFC'], 4],  # PRT
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.b.iii', 'OFFBiofuelFC'], 4],  # SWE
            ['fossil part of biofuels', ['1.A.3.b.iii', 'OFFBiofuelFC'], 4],  # CZE
            ['fossil part of biodiesel', ['1.A.3.b.iii', 'OFFBiodieselFC'], 4],  # DKE, DNK, HRV
            ['Fossil part of biodiesel', ['1.A.3.b.iii', 'OFFBiodieselFC'], 4],  # DNM, BEL, HUN. LVA, ESP
            ['Fossil part of biogasoline', ['1.A.3.b.iii', 'OFFBiogasolineFC'], 4],  # BEL
            ['Fossil part of biofuel', ['1.A.3.b.iii', 'OFFBiofuelFC'], 4],  # IRL
            # iv. Motorcycles
            ['iv. Motorcycles', ['1.A.3.b.iv', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.iv', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.iv', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.iv', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.iv', 'OtherLiquid'], 3],
            ['Kerosene', ['1.A.3.b.iv', 'Kerosene'], 4],  # UKR (and probably others)
            ['Lubricants', ['1.A.3.b.iv', 'Lubricants'], 4],  # UKR, JPN, HRV
            ['Lubricant Oil', ['1.A.3.b.iv', 'Lubricants'], 4],  # PRT
            ['Other', ['1.A.3.b.iv', 'OLOther'], 4],  # UKR (and probably others)
            ['Other Liquid Fuels', ['1.A.3.b.iv', 'OLOther'], 4],  # CYP
            ['Other non-specified', ['1.A.3.b.iv', 'OLOther'], 4],  # SWE new in 2023
            ['Lube', ['1.A.3.b.iv', 'Lubricants'], 4],  # MCO
            ['Lubricants in 2-stroke engines', ['1.A.3.b.iv', 'Lubricants'], 4],  # HUN
            ['Lubricants (two-stroke engines)', ['1.A.3.b.iv', 'Lubricants'], 4],  # ESP
            ['lubricants', ['1.A.3.b.iv', 'Lubricants'], 4],  # SVN
            ['Gaseous fuels', ['1.A.3.b.iv', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.3.b.iv', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.b.iv', 'OtherFF'], 3],
            ['Other Fossil Fuels', ['1.A.3.b.iv', 'OFFOther'], 4],  # CYP
            ['Fossil part of biodiesel or biogasoline', ['1.A.3.b.iv', 'OFFBiofuelFC'], 4],  # PRT
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.b.iv', 'OFFBiofuelFC'], 4],  # SWE
            ['fossil part of biofuels', ['1.A.3.b.iv', 'OFFBiofuelFC'], 4],  # CZE
            ['Fossil part of biodiesel', ['1.A.3.b.iv', 'OFFBiodieselFC'], 4],  # BEL
            ['Fossil part of biogasoline', ['1.A.3.b.iv', 'OFFBiogasolineFC'], 4],  # BEL
            ['Fossil part of biodiese', ['1.A.3.b.iv', 'OFFBiodieselFC'], 4],  # LVA
            ['Fossil part of biofuel', ['1.A.3.b.iv', 'OFFBiofuelFC'], 4],  # IRL
            ['fossil part of biodiesel', ['1.A.3.b.iv', 'OFFBiofuelFC'], 4],  # HRV
            # v. Other
            ['v. Other (please specify)', ['1.A.3.b.v', 'Total'], 2],
            # TUR
            ['Road total', ['1.A.3.b.v.1', 'Total'], 3],
            ['Gasoline', ['1.A.3.b.v.1', 'Gasoline'], 4],
            ['Diesel Oil', ['1.A.3.b.v.1', 'DieselOil'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.1', 'LPG'], 4],
            ['Gaseous Fuels', ['1.A.3.b.v.1', 'Gaseous'], 4],
            ['Biomass', ['1.A.3.b.v.1', 'Biomass'], 4],
            # CYP
            ['Buses', ['1.A.3.b.v.2', 'Total'], 3],
            ['Gasoline', ['1.A.3.b.v.2', 'Gasoline'], 4],
            ['Diesel Oil', ['1.A.3.b.v.2', 'DieselOil'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.2', 'LPG'], 4],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.2', 'OtherLiquid'], 4],
            ['Gaseous Fuels', ['1.A.3.b.v.2', 'Gaseous'], 4],
            ['Biomass', ['1.A.3.b.v.2', 'Biomass'], 4],
            ['Other Fossil Fuels (please specify)', ['1.A.3.b.v.2', 'OtherFF'], 4],
            # GBK, GBR
            ['All vehicles - biofuel use', ['1.A.3.b.v.3', 'Total'], 3],
            ['Biomass', ['1.A.3.b.v.3', 'Biomass'], 4],
            ['All vehicles - LPG use', ['1.A.3.b.v.4', 'Total'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.4', 'LPG'], 4],
            ['All vehicles - biofuel use (fossil component)', ['1.A.3.b.v.5', 'Total'], 4],
            ['Other Fossil Fuels (please specify)', ['1.A.3.b.v.5', 'OtherFF'], 4],
            # CAN
            ['Propane and Natural Gas Vehicles', ['1.A.3.b.v.6', 'Total'], 3],
            ['Gasoline', ['1.A.3.b.v.6', 'Gasoline'], 4],
            ['Diesel Oil', ['1.A.3.b.v.6', 'DieselOil'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.6', 'LPG'], 4],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.6', 'OtherLiquid'], 4],
            ['Gaseous Fuels', ['1.A.3.b.v.6', 'Gaseous'], 4],
            ['Biomass', ['1.A.3.b.v.6', 'Biomass'], 4],
            ['Other Fossil Fuels (please specify)', ['1.A.3.b.v.6', 'OtherFF'], 4],
            # BEL
            ['Lubricant Two-Stroke Engines', ['1.A.3.b.v.7', 'Lubricants'], 3],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.7', 'OtherLiquid'], 4],
            # ROU
            ['Gaseous Fuels', ['1.A.3.b.v.8', 'Total'], 3],
            ['Gaseous Fuels', ['1.A.3.b.v.8', 'Gaseous'], 4],
            ['Other Liquid Fuels', ['1.A.3.b.v.9', 'Total'], 3],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.9', 'OtherLiquid'], 4],
            ['Other Kerosene', ['1.A.3.b.v.9', 'Kerosene'], 5],
            ['Heating and Other Gasoil', ['1.A.3.b.v.9', 'HeatingGasoil'], 5],
            ['Biomass', ['1.A.3.b.v.10', 'Total'], 3],
            ['Biomass', ['1.A.3.b.v.10', 'Biomass'], 4],
            # DEU
            ['CO2 from lubricant co-incineration in 2-stroke road vehicles', ['1.A.3.b.v.7', 'Total'], 3],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.7', 'OtherLiquid'], 4],
            ['lubricant used in 2-stroke mix', ['1.A.3.b.v.7', 'Lubricants'], 5],
            # USA
            ['Evaporative Emissions', ['1.A.3.b.v.11', 'Total'], 3],
            ['Gasoline', ['1.A.3.b.v.11', 'Gasoline'], 4],
            ['Diesel Oil', ['1.A.3.b.v.11', 'DieselOil'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.11', 'LPG'], 4],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.11', 'OtherLiquid'], 4],
            ['Gaseous Fuels', ['1.A.3.b.v.11', 'Gaseous'], 4],
            ['Biomass', ['1.A.3.b.v.11', 'Biomass'], 4],
            ['Other Fossil Fuels (please specify)', ['1.A.3.b.v.11', 'OtherFF'], 4],
            # SVK
            ['Urea-based catalysts', ['1.A.3.b.v.12', 'Total'], 3],
            ['Diesel Oil', ['1.A.3.b.v.12', 'DieselOil'], 4],
            # ESP
            ['Other non-specified', ['1.A.3.b.v.13', 'Total'], 3],
            ['Gasoline', ['1.A.3.b.v.13', 'Gasoline'], 4],
            ['Diesel Oil', ['1.A.3.b.v.13', 'DieselOil'], 4],
            ['Liquefied Petroleum Gases (LPG)', ['1.A.3.b.v.13', 'LPG'], 4],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.13', 'OtherLiquid'], 4],
            ['Gaseous Fuels', ['1.A.3.b.v.13', 'Gaseous'], 4],
            ['Biomass', ['1.A.3.b.v.13', 'Biomass'], 4],
            ['Other Fossil Fuels (please specify)', ['1.A.3.b.v.13', 'OtherFF'], 4],
            # BGR
            ['Urea', ['1.A.3.b.v.12', 'Total'], 3],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.12', 'OtherLiquid'], 4],
            ['Lubricants', ['1.A.3.b.v.7', 'Total'], 3],
            ['Other Liquid Fuels (please specify)', ['1.A.3.b.v.7', 'OtherLiquid'], 4],
            # c. Railways
            ['c. Railways', ['1.A.3.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.3.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.3.c', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.3.c', 'Gaseous'], 2],
            ['Biomass(6)', ['1.A.3.c', 'Biomass'], 2],
            ['Other fossil fuels (please specify)', ['1.A.3.c', 'OtherFF'], 2],
            ['Biodiesel (fossil component)', ['1.A.3.c', 'OFFBiodieselFC'], 3],  # LUX
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.c', 'OFFBiodieselFC'], 3],  # SWE
            ['Fossil part of biodiesel', ['1.A.3.c', 'OFFBiodieselFC'], 3],  # LVA, new in 2022
            ['Other fossil fuels', ['1.A.3.c', 'OFFOther'], 3],  # ROU, new in 2022
            # d. Domestic navigation
            ['d. Domestic Navigation(10)', ['1.A.3.d', 'Total'], 1],
            ['Residual fuel oil', ['1.A.3.d', 'ResFuelOil'], 2],
            ['Gas/diesel oil', ['1.A.3.d', 'GasDieselOil'], 2],
            ['Gasoline', ['1.A.3.d', 'Gasoline'], 2],
            ['Other liquid fuels (please specify)', ['1.A.3.d', 'OtherLiquid'], 2],
            ['Lubricants', ['1.A.3.d', 'Lubricants'], 3],  # UKR, JPN
            ['Biodiesel (5 percent fossil portion)', ['1.A.3.d', 'OLBiodieselFC'], 3],  # CAN
            ['Light Fuel Oil', ['1.A.3.d', 'LightFuelOil'], 3],  # CAN
            ['Kerosene and stove oil', ['1.A.3.d', 'KeroseStoveOil'], 3],  # CAN
            ['Kerosene', ['1.A.3.d', 'Kerosene'], 3],  # DKE, DNK
            ['Natural Gas Liquids', ['1.A.3.d', 'NGL'], 3],  # DKE, DNK
            ['Fossil part of biodiesel', ['1.A.3.d', 'OLBiodieselFC'], 3],  # LTU
            ['Other non-specified', ['1.A.3.d', 'OLOther'], 3],  # SWE
            ['Other motor fuels', ['1.A.3.d', 'OMotorFuels'], 3],  # RUS
            ['Fuel oil A', ['1.A.3.d', 'FuelOilA'], 3],  # JPN
            ['Fuel oil B', ['1.A.3.d', 'FuelOilB'], 3],  # JPN
            ['Fuel oil C', ['1.A.3.d', 'FuelOilC'], 3],  # JPN
            ['Diesel Oil', ['1.A.3.d', 'OLDiesel'], 3],  # FIN
            ['Other Liquid Fuels', ['1.A.3.d', 'OLOther'], 3],  # ROU, new in 2022
            ['Heating and Other Gasoil', ['1.A.3.d', 'OLHeatingOtherGasoil'], 3],
            # ROU, new in 2023
            ['Liquified Petroleum Gas', ['1.A.3.d', 'OLLPG'], 3],  # ROU, new in 2023
            ['Gaseous fuels', ['1.A.3.d', 'Gaseous'], 2],
            ['Biomass(6)', ['1.A.3.d', 'Biomass'], 2],
            ['Other fossil fuels (please specify)(4)', ['1.A.3.d', 'OtherFF'], 2],
            ['Liquified natural gas', ['1.A.3.d', 'LNG'], 3],  # DKE, DNK, DNM
            ['Biodiesel (fossil component)', ['1.A.3.d', 'OFFBiodieselFC'], 3],  # LUX
            ['Coal', ['1.A.3.d', 'OFFCoal'], 3],  # NZL, NDL
            ['fossil part of biodiesel', ['1.A.3.d', 'OFFBiodieselFC'], 3],  # AUT
            ['Fossil part of biodiesel and biogasoline', ['1.A.3.d', 'OFFBioGasDieselFC'], 3],  # SWE
            ['Solid Fuels', ['1.A.3.d', 'OFFSolid'], 3],  # AUS
            ['Other Fossil Fuels', ['1.A.3.d', 'OFFOther'], 3],  # ROU, new in 2022
            # e. other transportation
            # keep details also for top category as it's present
            ['e. Other transportation (please specify)', ['1.A.3.e', 'Total'], 1],
            ['Liquid fuels', ['1.A.3.e', 'Liquid'], 2],
            ['Solid fuels', ['1.A.3.e', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.3.e', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.3.e', 'OtherFF'], 2],
            ['Biomass(6)', ['1.A.3.e', 'Biomass'], 2],
            # i. pipeline
            ['i. Pipeline transport', ['1.A.3.e.i', 'Total'], 2],
            ['Liquid fuels', ['1.A.3.e.i', 'Liquid'], 3],
            ['Solid fuels', ['1.A.3.e.i', 'Solid'], 3],
            ['Gaseous fuels', ['1.A.3.e.i', 'Gaseous'], 3],
            ['Other fossil fuels(4)', ['1.A.3.e.i', 'OtherFF'], 3],
            ['Biomass(6)', ['1.A.3.e.i', 'Biomass'], 3],
            # ii other
            ['ii. Other (please specify)', ['1.A.3.e.ii', 'Total'], 2],
            # UKR, SWE
            ['Off-road vehicles and other machinery', ['1.A.3.e.ii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.1', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.1', 'Biomass'], 4],
            # GBR, GBK
            ['Aircraft support vehicles', ['1.A.3.e.ii.2', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.2', 'Liquid'], 4],
            # CAN
            ['Off Road', ['1.A.3.e.ii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.1', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.1', 'Biomass'], 4],
            # LTU
            ['Off-road transport', ['1.A.3.e.ii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.1', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.1', 'Biomass'], 4],
            # BEL
            ['Other non-specified', ['1.A.3.e.ii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.3', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.3', 'Biomass'], 4],
            # AUS
            ['Off-Road Vehicles', ['1.A.3.e.ii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.1', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.1', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.1', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.1', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.1', 'Biomass'], 4],
            # USA
            ['Non-Transportation Mobile', ['1.A.3.e.ii.4', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.4', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.4', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.4', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.4', 'Biomass'], 4],
            # AUT (new in 2022)
            ['Airport ground activities', ['1.A.3.e.ii.2', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.4', 'Liquid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.4', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.4', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.4', 'Biomass'], 4],
            # ROU, new in 2022
            ['Other', ['1.A.3.e.ii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.3.e.ii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.3.e.ii.3', 'Solid'], 4],
            ['Gaseous Fuels', ['1.A.3.e.ii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels', ['1.A.3.e.ii.3', 'OtherFF'], 4],
            ['Biomass', ['1.A.3.e.ii.3', 'Biomass'], 4],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2(2)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # tested
    "Table1.A(a)s4": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 127,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2(1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'EMISSIONS CO2 Amount captured',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.4 Other sectors', ['1.A.4', 'Total'], 0],
            ['Liquid fuels', ['1.A.4', 'Liquid'], 1],
            ['Solid fuels', ['1.A.4', 'Solid'], 1],
            ['Gaseous fuels', ['1.A.4', 'Gaseous'], 1],
            ['Other fossil fuels(4)', ['1.A.4', 'OtherFF'], 1],
            ['Peat(5)', ['1.A.4', 'Peat'], 1],
            ['Biomass(6)', ['1.A.4', 'Biomass'], 1],
            # a. Commercial/institutional(12)
            ['a. Commercial/institutional(12)', ['1.A.4.a', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.a', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.a', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.4.a', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.4.a', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.4.a', 'Peat'], 2],
            ['Biomass(6)', ['1.A.4.a', 'Biomass'], 2],
            # 1.A.4.a.i Stationary combustion
            ['1.A.4.a.i Stationary combustion', ['1.A.4.a.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.a.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.a.i', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.a.i', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.a.i', 'OtherFF'], 3],
            ['Peat', ['1.A.4.a.i', 'Peat'], 3],
            ['Biomass', ['1.A.4.a.i', 'Biomass'], 3],
            # 1.A.4.a.ii Off-road vehicles and other machinery
            ['1.A.4.a.ii Off-road vehicles and other machinery', ['1.A.4.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.a.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.4.a.ii', 'Biomass'], 3],
            # 1.A.4.a.iii Other (please specify)
            ['1.A.4.a.iii Other (please specify)', ['1.A.4.a.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.a.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.a.iii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.a.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.a.iii', 'OtherFF'], 3],
            ['Peat', ['1.A.4.a.iii', 'Peat'], 3],
            ['Biomass', ['1.A.4.a.iii', 'Biomass'], 3],
            # b. Residential(13)
            ['b. Residential(13)', ['1.A.4.b', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.b', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.b', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.4.b', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.4.b', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.4.b', 'Peat'], 2],
            ['Biomass(6)', ['1.A.4.b', 'Biomass'], 2],
            # 1.A.4.b.i Stationary combustion
            ['1.A.4.b.i Stationary combustion', ['1.A.4.b.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.b.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.b.i', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.b.i', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.b.i', 'OtherFF'], 3],
            ['Peat', ['1.A.4.b.i', 'Peat'], 3],
            ['Biomass', ['1.A.4.b.i', 'Biomass'], 3],
            # 1.A.4.b.ii Off-road vehicles and other machinery
            ['1.A.4.b.ii Off-road vehicles and other machinery', ['1.A.4.b.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.b.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.b.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.b.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.b.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.4.b.ii', 'Biomass'], 3],
            # 1.A.4.b.iii Other (please specify)
            ['1.A.4.b.iii Other (please specify)', ['1.A.4.b.iii', 'Total'], 2],
            # CYP, USA
            ['Residential', ['1.A.4.b.iii.1', 'Total'], 3],
            ['Liquid Fuels', ['1.A.4.b.iii.1', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.b.iii.1', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.4.b.iii.1', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.4.b.iii.1', 'OtherFF'], 3],
            ['Peat', ['1.A.4.b.iii.1', 'Peat'], 3],
            ['Biomass', ['1.A.4.b.iii.1', 'Biomass'], 3],
            # c. Agriculture/forestry/fishing
            ['c. Agriculture/forestry/fishing', ['1.A.4.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.c', 'Solid'], 2],
            ['Gaseous fuels', ['1.A.4.c', 'Gaseous'], 2],
            ['Other fossil fuels(4)', ['1.A.4.c', 'OtherFF'], 2],
            ['Peat(5)', ['1.A.4.c', 'Peat'], 2],
            ['Biomass(6)', ['1.A.4.c', 'Biomass'], 2],
            # i. Stationary
            ['i. Stationary', ['1.A.4.c.i', 'Total'], 2],
            ['Liquid fuels', ['1.A.4.c.i', 'Liquid'], 3],
            ['Solid fuels', ['1.A.4.c.i', 'Solid'], 3],
            ['Gaseous fuels', ['1.A.4.c.i', 'Gaseous'], 3],
            ['Other fossil fuels(4)', ['1.A.4.c.i', 'OtherFF'], 3],
            ['Peat(5)', ['1.A.4.c.i', 'Peat'], 3],
            ['Biomass(6)', ['1.A.4.c.i', 'Biomass'], 3],
            # ii. Off-road vehicles and other machinery
            ['ii. Off-road vehicles and other machinery', ['1.A.4.c.ii', 'Total'], 2],
            ['Gasoline', ['1.A.4.c.ii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.4.c.ii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.4.c.ii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.4.c.ii', 'OtherLiquid'], 3],
            ['Other Kerosene', ['1.A.4.c.ii', 'Kerosene'], 4],  # HRV
            ['Lubricants', ['1.A.4.c.ii', 'Lubricants'], 4],  # HRV
            ['Gasoil', ['1.A.4.c.ii', 'Gasoil'], 4],  # FIN
            ['Marine gasoil', ['1.A.4.c.ii', 'MarineGasoil'], 4],  # NOR
            ['heavy fuel oil', ['1.A.4.c.ii', 'HeavyFuelOil'], 4],  # NOR
            ['Other motor fuels', ['1.A.4.c.ii', 'OMotorFuels'], 4],  # RUS
            ['Biodiesel (5 percent fossil portion)', ['1.A.4.c.ii', 'OLBiodieselFC'], 4],  # CAN
            ['Lubricating Oil (Two-Stroke Engines)', ['1.A.4.c.ii', 'Lubricants'], 4],
            # CAN new in 2023
            ['Gaseous fuels', ['1.A.4.c.ii', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.4.c.ii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.4.c.ii', 'OtherFF'], 3],
            ['fossil part of biodiesel', ['1.A.4.c.ii', 'OFFBiodieselFC'], 4],
            ['Fossil part of biodiesel and biogasoline', ['1.A.4.c.ii', 'OFFBiofuelFC'], 4],
            ['Biodiesel (fossil component)', ['1.A.4.c.ii', 'OFFBiodieselFC'], 4], # LUX
            ['Alkylate Gasoline', ['1.A.4.c.ii', 'OFFAlkylateGasoline'], 4], # LIE
            # iii. Fishing
            ['iii. Fishing', ['1.A.4.c.iii', 'Total'], 2],
            ['Residual fuel oil', ['1.A.4.c.iii', 'ResFuelOil'], 3],
            ['Gas/diesel oil', ['1.A.4.c.iii', 'GasDieselOil'], 3],
            ['Gasoline', ['1.A.4.c.iii', 'Gasoline'], 3],
            ['Other liquid fuels (please specify)', ['1.A.4.c.iii', 'OtherLiquid'], 3],
            ['Biodiesel (5 percent fossil portion)', ['1.A.4.c.iii', 'OLBiodieselFC'], 4],  # CAN
            ['Gaseous fuels', ['1.A.4.c.iii', 'Gaseous'], 3],
            ['Biomass(6)', ['1.A.4.c.iii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(4)', ['1.A.4.c.iii', 'OtherFF'], 3],
            ['Fossil part of biodiesel and biogasoline', ['1.A.4.c.iii', 'OFFBiofuelFC'], 3],
            # 1.A.5 Other (Not specified elsewhere)(14)
            ['1.A.5 Other (Not specified elsewhere)(14)', ['1.A.5', 'Total'], 0],
            # a. Stationary (please specify)
            ['a. Stationary (please specify)', ['1.A.5.a', 'Total'], 1],
            # temp
            ['Liquid Fuels', ['1.A.5.a', 'Liquid'], 2],
            ['Solid Fuels', ['1.A.5.a', 'Solid'], 2],
            ['Gaseous Fuels', ['1.A.5.a', 'Gaseous'], 2],
            ['Other Fossil Fuels', ['1.A.5.a', 'OtherFF'], 2],
            ['Peat', ['1.A.5.a', 'Peat'], 2],
            ['Biomass', ['1.A.5.a', 'Biomass'], 2],
            # temp
            # GBK, GBR
            ['Military fuel use', ['1.A.5.a.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.i', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.i', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.i', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.i', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.i', 'Biomass'], 3],
            # TUR
            ['Liquid fuels', ['1.A.5.a', 'Liquid'], 2],
            # ESP, FIN, SWE
            ['Other non-specified', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.ii', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # ROU, SVK, RUS
            ['Other', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.ii', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # FRA, FRK
            ['Other not specified', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.ii', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # CYP
            ['Other (not specified elsewhere)', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.ii', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # NOR, HUN
            ['Military', ['1.A.5.a.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.i', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.i', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.i', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.i', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.i', 'Biomass'], 3],
            ['Non-fuel Use', ['1.A.5.a.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.iii', 'Liquid'], 3],
            # DNM, DKE, DNK
            ['Other stationary combustion', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # LUX
            ['Stationary', ['1.A.5.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.a.ii', 'Biomass'], 3],
            # USA
            ['Incineration of Waste', ['1.A.5.a.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.iv', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.iv', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.iv', 'Biomass'], 3],
            ['U.S. Territories', ['1.A.5.a.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.v', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.v', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.v', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.v', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.v', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.v', 'Biomass'], 3],
            ['Non Energy Use', ['1.A.5.a.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.a.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.a.iii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.a.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.a.iii', 'OtherFF'], 3],
            ['Peat', ['1.A.5.a.iii', 'Peat'], 3],
            ['Biomass', ['1.A.5.a.iii', 'Biomass'], 3],
            # b. Mobile (please specify)
            ['b. Mobile (please specify)', ['1.A.5.b', 'Total'], 1],
            # temp
            ['Liquid Fuels', ['1.A.5.b', 'Liquid'], 2],
            ['Solid Fuels', ['1.A.5.b', 'Solid'], 2],
            ['Gaseous Fuels', ['1.A.5.b', 'Gaseous'], 2],
            ['Other Fossil Fuels', ['1.A.5.b', 'OtherFF'], 2],
            ['Biomass', ['1.A.5.b', 'Biomass'], 2],
            # temp
            # GBK, GBR
            ['Military aviation and naval shipping', ['1.A.5.b.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.i', 'Liquid'], 3],
            # HRV
            ['Military aviation component', ['1.A.5.b.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.ii', 'Biomass'], 3],
            ['Military water-borne component', ['1.A.5.b.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.iii', 'Biomass'], 3],
            # ESP, FIN
            ['Other non-specified', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Peat', ['1.A.5.b.iv', 'Peat'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # NLD, DKE, DNM, DNK, SWE, UKR
            ['Military use', ['1.A.5.b.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.v', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.v', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.v', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.v', 'OtherFF'], 3],
            ['Peat', ['1.A.5.b.v', 'Peat'], 3],
            ['Biomass', ['1.A.5.b.v', 'Biomass'], 3],
            # AUT, NOR, USA, CHE, HUN, LTU
            ['Military', ['1.A.5.b.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.v', 'Liquid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.v', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.v', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.v', 'Biomass'], 3],
            # PRT
            ['Military Aviation', ['1.A.5.b.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.ii', 'Liquid'], 3],
            # ROU, MLT
            ['Other', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Peat', ['1.A.5.b.iv', 'Peat'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # FRA, FRK
            ['Other not specified', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Peat', ['1.A.5.b.iv', 'Peat'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # CYP
            ['1A5b i Mobile (aviation component)', ['1.A.5.b.vi', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.vi', 'Liquid'], 3],
            # GBK, GBR
            ['Lubricants used in 2-stroke engines', ['1.A.5.b.vii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.vii', 'Liquid'], 3],
            # DNM, DKE, DNK
            ['Recreational crafts', ['1.A.5.b.viii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.viii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.viii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.viii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.viii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.viii', 'Biomass'], 3],
            # SVK
            ['Military use Jet Kerosene', ['1.A.5.b.ix', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.ix', 'Liquid'], 3],
            ['Military Gasoline', ['1.A.5.b.x', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.x', 'Liquid'], 3],
            ['Biomass', ['1.A.5.b.ix', 'Biomass'], 3],
            ['Military Diesel Oil', ['1.A.5.b.xi', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.xi', 'Liquid'], 3],
            ['Biomass', ['1.A.5.b.xi', 'Biomass'], 3],
            # BEL
            ['Military Use', ['1.A.5.b.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.v', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.v', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.v', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.v', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.v', 'Biomass'], 3],
            # AUS
            ['Military Transport', ['1.A.5.b.xii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.xii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.xii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.xii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.xii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.xii', 'Biomass'], 3],
            # CZE
            ['Agriculture and Forestry and Fishing', ['1.A.5.b.xiii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.xiii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.xiii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.xiii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.xiii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.xiii', 'Biomass'], 3],
            ['Other mobile sources not included elsewhere', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # SVN
            ['Military use of fuels', ['1.A.5.b.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.v', 'Liquid'], 3],
            # LUX
            ['Unspecified Mobile', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # LVA
            ['Mobile', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iv', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iv', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.iv', 'Biomass'], 3],
            # CAN
            ['Domestic Military (Aviation)', ['1.A.5.b.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.ii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.ii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.ii', 'Biomass'], 3],
            ['Military Water-borne Navigation', ['1.A.5.b.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.iii', 'Solid'], 3],
            ['Gaseous Fuels', ['1.A.5.b.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels', ['1.A.5.b.iii', 'OtherFF'], 3],
            ['Biomass', ['1.A.5.b.iii', 'Biomass'], 3],
            # CZE, new in 2022
            ['i. Mobile (aviation component)', ['1.A.5.b.vi', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.vi', 'Liquid'], 3],
            ['iii. Mobile (other)', ['1.A.5.b.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.iv', 'Liquid'], 3],
            # Information Item
            ['Information item:(15)', ['\IGNORE', '\IGNORE'], 0],
            ['Waste incineration with energy recovery included as:', ['\IGNORE', '\IGNORE'], 1],
            ['Biomass(6)', ['\IGNORE', '\IGNORE'], 1],
            ['Fossil fuels(4)', ['\IGNORE', '\IGNORE'], 1],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2(2)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # tested
    "Table1.B.1": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 19,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA Amount of fuel produced',
                'IMPLIED EMISSION FACTORS CH4(1)',
                'IMPLIED EMISSION FACTORS CO2',
                'EMISSIONS CH4 Recovery/Flaring(2)',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. B. 1. a. Coal mining and handling', ['1.B.1.a'], 0],
            ['i. Underground mines(4)', ['1.B.1.a.i'], 1],
            ['Mining activities', ['1.B.1.a.i.1'], 2],
            ['Post-mining activities', ['1.B.1.a.i.2'], 2],
            ['Abandoned underground mines', ['1.B.1.a.i.3'], 2],
            ['ii. Surface mines(4)', ['1.B.1.a.ii'], 1],
            ['Mining activities', ['1.B.1.a.ii.1'], 2],
            ['Post-mining activities', ['1.B.1.a.ii.2'], 2],
            ['1. B. 1. b. Solid fuel transformation(5)', ['1.B.1.b'], 0],
            ['1. B. 1. c. Other (please specify)(6)', ['1.B.1.c'], 0],
            ['Flaring', ['1.B.1.c.i'], 1],  # UKR, AUS
            ['Flaring of gas', ['1.B.1.c.i'], 1],  # SWE
            ['Coal Dumps', ['1.B.1.c.ii'], 1],  # JPN
            ['Uncontrolled combustion and burning coal dumps', ['1.B.1.c.ii'], 1],
            # JPN since 2023
            ['SO2 scrubbing', ['1.B.1.c.iii'], 1],  # SVN
            ['Flaring of coke oven gas', ['1.B.1.c.iv'], 1],  # KAZ
            ['Emisson from Coke Oven Gas Subsystem', ['1.B.1.c.iv'], 1],  # POL
            ['Other', ['1.B.1.c.v'], 1],  # ROU, new in 2022
        ],
        "entity_mapping": {
            'EMISSIONS CH4 Emissions(3)': 'CH4',
            'EMISSIONS CO2 Emissions': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.B.2": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 33,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA(1) Description(1)',
                'ACTIVITY DATA(1) Unit(1)',
                'ACTIVITY DATA(1) Value',
                'IMPLIED EMISSION FACTORS CO2(2)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'EMISSIONS CO2 Amount captured',
            ],
            "stop_cats": [".", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. B. 2. a. Oil(6)', ['1.B.2.a'], 0],
            ['1. Exploration', ['1.B.2.a.1'], 1],
            ['2. Production(7)', ['1.B.2.a.2'], 1],
            ['3. Transport', ['1.B.2.a.3'], 1],
            ['4. Refining/storage', ['1.B.2.a.4'], 1],
            ['5. Distribution of oil products', ['1.B.2.a.5'], 1],
            ['6. Other', ['1.B.2.a.6'], 1],
            ['1. B. 2. b. Natural gas', ['1.B.2.b'], 0],
            ['1. Exploration', ['1.B.2.b.1'], 1],
            ['2. Production(7)', ['1.B.2.b.2'], 1],
            ['3. Processing', ['1.B.2.b.3'], 1],
            ['4. Transmission and storage', ['1.B.2.b.4'], 1],
            ['5. Distribution', ['1.B.2.b.5'], 1],
            ['6. Other', ['1.B.2.b.6'], 1],
            ['1. B. 2. c. Venting and flaring', ['1.B.2.c'], 0],
            ['Venting', ['1.B.2.c-ven'], 1],
            ['i. Oil', ['1.B.2.c-ven.i'], 2],
            ['ii. Gas', ['1.B.2.c-ven.ii'], 2],
            ['iii. Combined', ['1.B.2.c-ven.iii'], 2],
            ['Flaring(8)', ['1.B.2.c-fla'], 1],
            ['i. Oil', ['1.B.2.c-fla.i'], 2],
            ['ii. Gas', ['1.B.2.c-fla.ii'], 2],
            ['iii. Combined', ['1.B.2.c-fla.iii'], 2],
            ['1.B.2.d. Other (please specify)(9)', ['1.B.2.d'], 0],
            ['Groundwater extraction and CO2 mining', ['1.B.2.d.i'], 1],  # HUN
            ['Geothermal', ['1.B.2.d.ii'], 1],  # NOR, DEU, PRT, NZL
            ['Geothermal Energy', ['1.B.2.d.ii'], 1],  # ISL
            ['Geothermal Generation', ['1.B.2.d.ii'], 1],  # JPN
            ['Geotherm', ['1.B.2.d.ii'], 1],  # ITA
            ['City Gas Production', ['1.B.2.d.iii'], 1],  # PRT
            ['Other', ['1.B.2.d.iv'], 1],  # UKR, ROU
            ['Other non-specified', ['1.B.2.d.iv'], 1],  # SWE
            ['Flaring in refineries', ['1.B.2.d.v'], 1],  # ITA
            ['LPG transport', ['1.B.2.d.vi'], 1],  # GRC
            ['Distribution of town gas', ['1.B.2.d.vii'], 1],  # FIN
            ['Petrol distribution', ['1.B.2.d.viii'], 1],  # IRL
            ['Natural Gas Transport', ['1.B.2.d.ix'], 1],  # BLR
            ['Natural gas exploration - N2O emissions', ['1.B.2.d.x'], 1],  # GBR, GBK
            ['flue gas desulfurisation', ['1.B.2.d.xi'], 1],  # GBR, GBK, new in 2022
        ],
        "entity_mapping": {
            'EMISSIONS CH4 (4) Amount captured': 'CH4',
            'EMISSIONS CO2 Emissions(3)': 'CO2',
            'EMISSIONS N2O Amount captured': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.C": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 24,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA CO2 transported or injected(1)',
                'IMPLIED EMISSION FACTORS CO2',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Transport of CO2', ['1.C.1']],
            ['a. Pipelines', ['1.C.1.a']],
            ['b. Ships', ['1.C.1.b']],
            ['c. Other', ['1.C.1.c']],
            ['2. Injection and storage(3)', ['1.C.2']],
            ['a. Injection', ['1.C.2.a']],
            ['b. Storage', ['1.C.2.b']],
            ['3. Other', ['1.C.3']],
            ['Information item(4, 5)', ['\IGNORE']],
            ['Total amount captured for storage', ['M.Info.A.TACS']],
            ['Total amount of imports for storage', ['M.Info.A.TAIS']],
            ['Total A', ['M.Info.A']],
            ['Total amount of exports for storage', ['M.Info.B.TAES']],
            ['Total amount of CO2 injected at storage sites', ['M.Info.B.TAI']],
            ['Total leakage from transport, injection and storage', ['M.Info.B.TLTIS']],
            ['Total B', ['M.Info.B']],
            ['Difference (A-B)(6)', ['\IGNORE']],
        ],
        "entity_mapping": {
            'EMISSIONS CO2(2)': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.D": {
        "status": "TODO",
        "table": {
            "firstrow": 5,
            "lastrow": 20,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [

        ],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table2(I)s1": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 31,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ['Total industrial processes', ['2']],
            ['A. Mineral industry', ['2.A']],
            ['1. Cement production', ['2.A.1']],
            ['2. Lime production', ['2.A.2']],
            ['3. Glass production', ['2.A.3']],
            ['4. Other process uses of carbonates', ['2.A.4']],
            ['B. Chemical industry', ['2.B']],
            ['1. Ammonia production', ['2.B.1']],
            ['2. Nitric acid production', ['2.B.2']],
            ['3. Adipic acid production', ['2.B.3']],
            ['4. Caprolactam, glyoxal and glyoxylic acid production', ['2.B.4']],
            ['5. Carbide production', ['2.B.5']],
            ['6. Titanium dioxide production', ['2.B.6']],
            ['7. Soda ash production', ['2.B.7']],
            ['8. Petrochemical and carbon black production', ['2.B.8']],
            ['9. Fluorochemical production', ['2.B.9']],
            ['10. Other (as specified in table 2(I).A-H)', ['2.B.10']],
            ['C. Metal industry', ['2.C']],
            ['1. Iron and steel production', ['2.C.1']],
            ['2. Ferroalloys production', ['2.C.2']],
            ['3. Aluminium production', ['2.C.3']],
            ['4. Magnesium production', ['2.C.4']],
            ['5. Lead production', ['2.C.5']],
            ['6. Zinc production', ['2.C.6']],
            ['7. Other (as specified in table 2(I).A-H)', ['2.C.7']],
        ],
        "entity_mapping": {
            'HFCs(1)': f'HFCS ({gwp_to_use})',
            'PFCs(1)': f'PFCS ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table2(I)s2": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 29,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ['D. Non-energy products from fuels and solvent use', ['2.D']],
            ['1. Lubricant use', ['2.D.1']],
            ['2. Paraffin wax use', ['2.D.2']],
            ['3. Other', ['2.D.3']],
            ['E. Electronics industry', ['2.E']],
            ['1. Integrated circuit or semiconductor', ['2.E.1']],
            ['2. TFT flat panel display', ['2.E.2']],
            ['3. Photovoltaics', ['2.E.3']],
            ['4. Heat transfer fluid', ['2.E.4']],
            ['5. Other (as specified in table 2(II))', ['2.E.5']],
            ['F. Product uses as substitutes for ODS(2)', ['2.F']],
            ['1. Refrigeration and air conditioning', ['2.F.1']],
            ['2. Foam blowing agents', ['2.F.2']],
            ['3. Fire protection', ['2.F.3']],
            ['4. Aerosols', ['2.F.4']],
            ['5. Solvents', ['2.F.5']],
            ['6. Other applications', ['2.F.6']],
            ['G. Other product manufacture and use', ['2.G']],
            ['1. Electrical equipment', ['2.G.1']],
            ['2. SF6 and PFCs from other product use', ['2.G.2']],
            ['3. N2O from product uses', ['2.G.3']],
            ['4. Other', ['2.G.4']],
            ['H. Other (as specified in tables 2(I).A-H and 2(II))(3)', ['2.H']],
        ],
        "entity_mapping": {
            'HFCs(1)': f'HFCS ({gwp_to_use})',
            'PFCs(1)': f'PFCS ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table2(I).A-Hs1": {
        "status": "TODO",
        "table": {
            "firstrow": 5,
            "lastrow": 40,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [

        ],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table2(I).A-Hs2": {
        "status": "TODO",
        "table": {
            "firstrow": 5,
            "lastrow": 36,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [

        ],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table2(II)": {
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 38,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [".", np.nan],
            "unit_info": unit_info["fgases"],
        },
        "sector_mapping": [
            ['Total actual emissions of halocarbons (by chemical) and SF6', ['2']],
            ['B. Chemical industry', ['2.B']],
            ['9. Flurochemical production', ['2.B.9']],
            ['By-product emissions', ['2.B.9.a']],
            ['Fugitive emissions', ['2.B.9.b']],
            ['10. Other', ['2.B.10']],
            ['C. Metal industry', ['2.C']],
            ['3. Aluminium production', ['2.C.3']],
            ['4. Magnesium production', ['2.C.4']],
            ['7. Other', ['2.C.7']],
            ['E. Electronics industry', ['2.E']],
            ['1. Integrated circuit or semiconductor', ['2.E.1']],
            ['2. TFT flat panel display', ['2.E.2']],
            ['3. Photovoltaics', ['2.E.3']],
            ['4. Heat transfer fluid', ['2.E.4']],
            ['5. Other (as specified in table 2(II))', ['2.E.5']],
            ['F. Product uses as substitutes for ODS(2)', ['2.F']],
            ['1. Refrigeration and air conditioning', ['2.F.1']],
            ['2. Foam blowing agents', ['2.F.2']],
            ['3. Fire protection', ['2.F.3']],
            ['4. Aerosols', ['2.F.4']],
            ['5. Solvents', ['2.F.5']],
            ['6. Other applications', ['2.F.6']],
            ['G. Other product manufacture and use', ['2.G']],
            ['1. Electrical equipment', ['2.G.1']],
            ['2. SF6 and PFCs from other product use', ['2.G.2']],
            ['4. Other', ['2.G.4']],
            ['H. Other (please specify)', ['2.H']],
            ['2.H.1 Pulp and paper', ['2.H.1']],
            ['2.H.2 Food and beverages industry', ['2.H.2']],
            ['2.H.3 Other (please specify)', ['2.H.3']],
        ],
        "entity_mapping": {
            'C 3F8': 'C3F8',
            #'C10F18' 'C2F6' 'C4F10' 'C5F12' 'C6F14' 'CF4'
            'HFC-125': 'HFC125',
            'HFC-134': 'HFC134',
            'HFC-134a': 'HFC134a',
            'HFC-143': 'HFC143',
            'HFC-143a': 'HFC143a',
            'HFC-152': 'HFC152',
            'HFC-152a': 'HFC152a',
            'HFC-161': 'HFC161',
            'HFC-227ea': 'HFC227ea',
            'HFC-23': 'HFC23',
            'HFC-236cb': 'HFC236cb',
            'HFC-236ea': 'HFC236ea',
            'HFC-236fa': 'HFC236fa',
            'HFC-245ca': 'HFC245ca',
            'HFC-245fa': 'HFC245fa',
            'HFC-32': 'HFC32',
            'HFC-365mfc': 'HFC365mfc',
            'HFC-41': 'HFC41',
            'HFC-43-10mee': 'HFC4310mee',
            'Unspecified mix of HFCs (1)': f'UnspMixOfHFCs ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
            'Unspecified mix of PFCs (1)': f'UnspMixOfPFCs ({gwp_to_use})',
            'c-C3F6': 'cC3F6',
            'c-C4F8': 'cC4F8',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3s1": {  # Agriculture summary sheet 1
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 75,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['3. Total agriculture', ['3'], 0],
            # I. Livestock
            ['I. Livestock', ['M.3.LV'], 1],
            # A. Enteric fermentation
            ['A. Enteric fermentation', ['3.A'], 2],
            ['1. Cattle(1)', ['3.A.1'], 3],
            ['Option A:', ['\IGNORE'], 4],
            ['Dairy cattle', ['3.A.1.Aa'], 5],
            ['Non-dairy cattle', ['3.A.1.Ab'], 5],
            ['Option B:', ['\IGNORE'], 4],
            ['Mature dairy cattle', ['3.A.1.Ba'], 5],
            ['Other mature cattle', ['3.A.1.Bb'], 5],
            ['Growing cattle', ['3.A.1.Bc'], 5],
            ['Option C (country-specific):', ['\IGNORE'], 4],
            # all countries not specified explcitly
            ['\C!-AUS-MLT-LUX-POL-SVN-USA\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            # Australia
            ['\C-AUS\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-AUS\ Dairy Cattle', ['3.A.1.C-AUS-a'], 6],
            ['\C-AUS\ Beef Cattle - Pasture', ['3.A.1.C-AUS-b'], 6],
            ['\C-AUS\ Beef Cattle - Feedlot', ['3.A.1.C-AUS-c'], 6],
            # malta
            ['\C-MLT\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-MLT\ dairy cows', ['3.A.1.C-MLT-a'], 6],
            ['\C-MLT\ non-lactating cows', ['3.A.1.C-MLT-b'], 6],
            ['\C-MLT\ bulls', ['3.A.1.C-MLT-c'], 6],
            ['\C-MLT\ calves', ['3.A.1.C-MLT-d'], 6],
            ['\C-MLT\ growing cattle 1-2 years', ['3.A.1.C-MLT-e'], 6],
            # Luxembourg
            ['\C-LUX\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-LUX\ Bulls', ['3.A.1.C-LUX-a'], 6],
            ['\C-LUX\ Calves', ['3.A.1.C-LUX-b'], 6],
            ['\C-LUX\ Young Cattle', ['3.A.1.C-LUX-c'], 6],
            ['\C-LUX\ Suckler Cows', ['3.A.1.C-LUX-d'], 6],
            ['\C-LUX\ Bulls under 2 years', ['3.A.1.C-LUX-e'], 6],
            ['\C-LUX\ Dairy Cows', ['3.A.1.C-LUX-f'], 6],
            # Poland
            ['\C-POL\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-POL\ Bulls (older than 2 years)', ['3.A.1.C-POL-a'], 6],
            ['\C-POL\ Non-dairy Heifers (older than 2 years)', ['3.A.1.C-POL-b'], 6],
            ['\C-POL\ Non-dairy Young Cattle (younger than 1 year)', ['3.A.1.C-POL-c'], 6],
            ['\C-POL\ Dairy Cattle', ['3.A.1.C-POL-d'], 6],
            ['\C-POL\ Non-dairy Young Cattle (1-2 years)', ['3.A.1.C-POL-e'], 6],
            # Slovenia
            ['\C-SVN\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-SVN\ Dairy cows', ['3.A.1.C-SVN-a'], 6],
            ['\C-SVN\ Non-dairy cattle', ['3.A.1.C-SVN-b'], 6],
            ['\C-SVN\ Other cows', ['3.A.1.C-SVN-c'], 6],
            # USA
            ['\C-USA\ Other (as specified in table 3(I).A)', ['3.A.1.C'], 5],
            ['\C-USA\ Steer Stocker', ['3.A.1.C-USA-a'], 6],
            ['\C-USA\ Heifer Stocker', ['3.A.1.C-USA-b'], 6],
            ['\C-USA\ Beef Cows', ['3.A.1.C-USA-c'], 6],
            ['\C-USA\ Dairy Replacements', ['3.A.1.C-USA-d'], 6],
            ['\C-USA\ Beef Replacements', ['3.A.1.C-USA-e'], 6],
            ['\C-USA\ Steer Feedlot', ['3.A.1.C-USA-f'], 6],
            ['\C-USA\ Heifer Feedlot', ['3.A.1.C-USA-g'], 6],
            ['\C-USA\ Bulls', ['3.A.1.C-USA-h'], 6],
            ['\C-USA\ Dairy Cows', ['3.A.1.C-USA-i'], 6],
            ['\C-USA\ Beef Calves', ['3.A.1.C-USA-j'], 6],
            ['\C-USA\ Dairy Calves', ['3.A.1.C-USA-k'], 6],
            # Other livestock
            ['2. Sheep', ['3.A.2'], 3],
            ['3. Swine', ['3.A.3'], 3],
            ['4. Other livestock', ['3.A.4'], 3],
            ['Buffalo', ['3.A.4.a'], 4],
            ['Camels', ['3.A.4.b'], 4],
            ['Deer', ['3.A.4.c'], 4],
            ['Goats', ['3.A.4.d'], 4],
            ['Horses', ['3.A.4.e'], 4],
            ['Mules and Asses', ['3.A.4.f'], 4],
            ['Poultry', ['3.A.4.g'], 4],
            ['Other (please specify)', ['3.A.4.h'], 4],
            ['Rabbit', ['3.A.4.h.i'], 5],
            ['Reindeer', ['3.A.4.h.ii'], 5],
            ['Ostrich', ['3.A.4.h.iii'], 5],
            ['Fur-bearing Animals', ['3.A.4.h.iv'], 5],
            ['Other', ['3.A.4.h.v'], 5],
            # Manure Management
            ['B. Manure management', ['3.B'], 2],
            ['1. Cattle(1)', ['3.B.1'], 3],
            ['Option A:', ['\IGNORE'], 4],
            ['Dairy cattle', ['3.B.1.Aa'], 5],
            ['Non-dairy cattle', ['3.B.1.Ab'], 5],
            ['Option B:', ['\IGNORE'], 4],
            ['Mature dairy cattle', ['3.B.1.Ba'], 5],
            ['Other mature cattle', ['3.B.1.Bb'], 5],
            ['Growing cattle', ['3.B.1.Bc'], 5],
            ['Option C (country-specific):', ['\IGNORE'], 4],
            # all countries not specified explicitly
            ['\C!-AUS-MLT-LUX-POL-SVN-USA\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            # Australia
            ['\C-AUS\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-AUS\ Dairy Cattle', ['3.B.1.C-AUS-a'], 6],
            ['\C-AUS\ Beef Cattle - Pasture', ['3.B.1.C-AUS-b'], 6],
            ['\C-AUS\ Beef Cattle - Feedlot', ['3.B.1.C-AUS-c'], 6],
            # Malta
            ['\C-MLT\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-MLT\ dairy cows', ['3.B.1.C-MLT-a'], 6],
            ['\C-MLT\ non-lactating cows', ['3.B.1.C-MLT-b'], 6],
            ['\C-MLT\ bulls', ['3.B.1.C-MLT-c'], 6],
            ['\C-MLT\ calves', ['3.B.1.C-MLT-d'], 6],
            ['\C-MLT\ growing cattle 1-2 years', ['3.B.1.C-MLT-e'], 6],
            # Luxembourg
            ['\C-LUX\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-LUX\ Bulls', ['3.B.1.C-LUX-a'], 6],
            ['\C-LUX\ Calves', ['3.B.1.C-LUX-b'], 6],
            ['\C-LUX\ Young Cattle', ['3.B.1.C-LUX-c'], 6],
            ['\C-LUX\ Suckler Cows', ['3.B.1.C-LUX-d'], 6],
            ['\C-LUX\ Bulls under 2 years', ['3.B.1.C-LUX-e'], 6],
            ['\C-LUX\ Dairy Cows', ['3.B.1.C-LUX-f'], 6],
            # Poland
            ['\C-POL\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-POL\ Non-dairy Cattle', ['3.B.1.C-POL-a'], 6],
            ['\C-POL\ Dairy Cattle', ['3.B.1.C-POL-b'], 6],
            # Slovenia
            ['\C-SVN\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-SVN\ Dairy cows', ['3.B.1.C-SVN-a'], 6],
            ['\C-SVN\ Non-dairy cattle', ['3.B.1.C-SVN-b'], 6],
            ['\C-SVN\ Other cows', ['3.B.1.C-SVN-c'], 6],
            # USA
            ['\C-USA\ Other (as specified in table 3(I).B)', ['3.B.1.C'], 5],
            ['\C-USA\ Dairy Cattle', ['\IGNORE'], 6],
            ['\C-USA\ Non-Dairy Cattle', ['\IGNORE'], 6],
            ['\C-USA\ Steer Stocker', ['3.B.1.C-USA-a'], 6],
            ['\C-USA\ Heifer Stocker', ['3.B.1.C-USA-b'], 6],
            ['\C-USA\ Beef Cows', ['3.B.1.C-USA-c'], 6],
            ['\C-USA\ Dairy Replacements', ['3.B.1.C-USA-d'], 6],
            ['\C-USA\ Beef Replacements', ['3.B.1.C-USA-e'], 6],
            ['\C-USA\ Steer Feedlot', ['3.B.1.C-USA-f'], 6],
            ['\C-USA\ Heifer Feedlot', ['3.B.1.C-USA-g'], 6],
            ['\C-USA\ Bulls', ['3.B.1.C-USA-h'], 6],
            ['\C-USA\ Dairy Cows', ['3.B.1.C-USA-i'], 6],
            ['\C-USA\ Beef Calves', ['3.B.1.C-USA-j'], 6],
            ['\C-USA\ Dairy Calves', ['3.B.1.C-USA-k'], 6],
            # other animals
            ['2. Sheep', ['3.B.2'], 3],
            ['3. Swine', ['3.B.3'], 3],
            ['4. Other livestock', ['3.B.4'], 3],
            ['Buffalo', ['3.B.4.a'], 4],
            ['Camels', ['3.B.4.b'], 4],
            ['Deer', ['3.B.4.c'], 4],
            ['Goats', ['3.B.4.d'], 4],
            ['Horses', ['3.B.4.e'], 4],
            ['Mules and Asses', ['3.B.4.f'], 4],
            ['Poultry', ['3.B.4.g'], 4],
            ['Other (please specify)', ['3.B.4.h'], 4],
            ['Rabbit', ['3.B.4.h.i'], 5],
            ['Reindeer', ['3.B.4.h.ii'], 5],
            ['Ostrich', ['3.B.4.h.iii'], 5],
            ['Fur-bearing Animals', ['3.B.4.h.iv'], 5],
            ['Other', ['3.B.4.h.v'], 5],
            ['5. Indirect N2O emissions', ['3.B.5'], 3],
        ],
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3s2": {  # Agriculture summary sheet 2
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 18,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [".", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['C. Rice cultivation', ['3.C']],
            ['D. Agricultural soils(2) (3) (4)', ['3.D']],
            ['E. Prescribed burning of savannahs', ['3.E']],
            ['E. Prescribed burning of savannas', ['3.E']],
            ['F. Field burning of agricultural residues', ['3.F']],
            ['G. Liming', ['3.G']],
            ['H. Urea application', ['3.H']],
            ['I. Other carbon-containing fertilizers', ['3.I']],
            ['J. Other (please specify)', ['3.J']],
            ['NOx from Manure Management', ['3.J.1']],
            ['3.B NOx Emissions', ['3.J.1']],
            ['NOx from 3B', ['3.J.1']],
            ['NOX emissions from manure management', ['3.J.1']],
            ['NOx from manure management', ['3.J.1']],
            ['Other', ['3.J.2']],
            ['Other UK emissions', ['3.J.2']],
            ['Other non-specified', ['3.J.2']],
            ['OTs and CDs - Livestock', ['3.J.3']],
            ['OTs and CDs - soils', ['3.J.4']],
            ['OTs and CDs - other', ['3.J.5']],
            ['Digestate renewable raw material (storage of N)', ['3.J.6']],
            ['Digestate renewable raw material (atmospheric deposition)', ['3.J.7']],
            ['Digestate renewable raw material (storage of dry matter)', ['3.J.8']],
            ['NOx from Livestock', ['3.J.9']],
        ],
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.C": {  # rice cultivation details
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 21,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Harvested area(2)',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Organic amendments added(3)',
                'IMPLIED EMISSION FACTOR (1) CH4',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Irrigated', ['3.C.1']],
            ['Continuously flooded', ['3.C.1.a']],
            ['Intermittently flooded Single aeration', ['3.C.1.b.i']],
            ['Intermittently flooded Multiple aeration', ['3.C.1.b.ii']],
            ['2. Rainfed', ['3.C.2']],
            ['Flood prone', ['3.C.2.a']],
            ['Drought prone', ['3.C.2.b']],
            ['3. Deep water', ['3.C.3']],
            ['Water depth 50–100 cm', ['3.C.3.a']],
            ['Water depth > 100 cm', ['3.C.3.b']],
            ['4. Other (please specify)', ['3.C.4']],
            ['Non-specified', ['3.C.4.a']],  # EST
            ['Other', ['3.C.4.a']],  # DEU
            ['other', ['3.C.4.a']],  # LVA
            ['Other cultivation', ['3.C.4.a']],  # CZE
            ['Upland rice(4)', ['\IGNORE']],
            ['Total(4)', ['\IGNORE']],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': 'CH4',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.D": {  # direct and indirect N2O from soils
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 21,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Description",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Value",
                "IMPLIED EMISSION FACTORS Value",
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['a. Direct N2O emissions from managed soils', ['3.D.a']],
            ['1. Inorganic N fertilizers(3)', ['3.D.a.1']],
            ['2. Organic N fertilizers(3)', ['3.D.a.2']],
            ['a. Animal manure applied to soils', ['3.D.a.2.a']],
            ['b. Sewage sludge applied to soils', ['3.D.a.2.b']],
            ['c. Other organic fertilizers applied to soils', ['3.D.a.2.c']],
            ['3. Urine and dung deposited by grazing animals', ['3.D.a.3']],
            ['4. Crop residues', ['3.D.a.4']],
            ['5. Mineralization/immobilization associated with loss/gain of soil organic matter (4)(5)', ['3.D.a.5']],
            ['6. Cultivation of organic soils (i.e. histosols)(2)', ['3.D.a.6']],
            ['7. Other', ['3.D.a.7']],
            ['b. Indirect N2O Emissions from managed soils', ['3.D.b']],
            ['1. Atmospheric deposition(6)', ['3.D.b.1']],
            ['2. Nitrogen leaching and run-off', ['3.D.b.2']],
        ],
        "entity_mapping": {
            'EMISSIONS N2O': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.E": {  # savanna burning details
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 14,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Area of savanna burned',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Average above-ground biomass density',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Biomass burned',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Fraction of savanna burned',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen fraction in biomass',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
            ],
            "stop_cats": ["", ".", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['Forest land (specify ecological zone)(1)', ['3.E.1'], 0],
            ['Savanna Grassland', ['3.E.1.b'], 1],  # AUS
            ['Savanna Woodland', ['3.E.1.a'], 1],  # AUS
            ['Forest land', ['3.E.1.a'], 1],  # SWE, CHE, CZE, HRV
            ['Luxembourg', ['3.E.1.c'], 1],  # LUX
            ['Other non-specified', ['3.E.1.d'], 1],  # EST
            ['All', ['3.E.1.d'], 1],  # DNK, DNM, DKE
            ['Unspecified', ['3.E.1.d'], 1],  # DEU
            ['forest land', ['3.E.1.a'], 1],  # MLT
            ['Zone', ['3.E.1.d'], 1],  # LVA
            ['Grassland (specify ecological zone)(1)', ['3.E.2'], 0],
            ['Savanna Woodland', ['3.E.2.a'], 1],  # AUS
            ['Savanna Grassland', ['3.E.2.b'], 1],  # AUS
            ['Temperate Grassland', ['3.E.2.c'], 1],  # AUS
            ['Grassland', ['3.E.2.d'], 1],  # SWE, CHE, CZE, HRV
            ['Luxembourg', ['3.E.2.e'], 1],  # LUX
            ['Other non-specified', ['3.E.2.f'], 1],  # EST
            ['All', ['3.E.2.f'], 1],  # DNK, DNM, DKE
            ['Unspecified', ['3.E.2.f'], 1],  # DEU
            ['Tussock', ['3.E.2.g'], 1],  # NZL
            ['grassland', ['3.E.2.d'], 1],  # MLT
            ['Zone_', ['3.E.2.f'], 1],  # LVA
        ],
        "entity_mapping": {
            'EMISSIONS (2) CH4': 'CH4',
            'EMISSIONS (2) N2O': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.F": {  # field burning details
        "status": "TODO",
        "table": {
            "firstrow": 5,
            "lastrow": 30,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [

        ],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table3.G-I": {  # liming, urea, carbon containing fertilizer
        "status": "TODO",
        "table": {
            "firstrow": 5,
            "lastrow": 13,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [

        ],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table4": {  # LULUCF overview
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 29,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", ".", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['4. Total LULUCF', ['4']],
            ['A. Forest land', ['4.A']],
            ['1. Forest land remaining forest land', ['4.A.1']],
            ['2. Land converted to forest land', ['4.A.2']],
            ['B. Cropland', ['4.B']],
            ['1. Cropland remaining cropland', ['4.B.1']],
            ['2. Land converted to cropland', ['4.B.2']],
            ['C. Grassland', ['4.C']],
            ['1. Grassland remaining grassland', ['4.C.1']],
            ['2. Land converted to grassland', ['4.C.2']],
            ['D. Wetlands(3)', ['4.D']],
            ['1. Wetlands remaining wetlands', ['4.D.1']],
            ['2. Land converted to wetlands', ['4.D.2']],
            ['E. Settlements', ['4.E']],
            ['1. Settlements remaining settlements', ['4.E.1']],
            ['2. Land converted to settlements', ['4.E.2']],
            ['F. Other land (4)', ['4.F']],
            ['1. Other land remaining other land', ['4.F.1']],
            ['2. Land converted to other land', ['4.F.2']],
            ['G. Harvested wood products (5)', ['4.G']],
            ['H. Other (please specify)', ['4.H']],
            ['Land converted to Settlement', ['4.H.1']],
            ['Reservoir of Petit-Saut in French Guiana', ['4.H.5']],
            ['Biogenic NMVOCs from managed forest', ['4.H.4']],
            ['All other', ['4.H.9']],
            ['Luxembourg', ['4.H.8']],
            ['Settlements Remaining Settlements', ['4.H.2']],
            ['4.E Settlements', ['4.H.2']],
            ['4.C Grassland', ['4.H.3']],
            ['Settlements', ['4.H.2']],
            ['Other', ['4.H.9']],
            ['N2O Emissions from Aquaculture Use', ['4.H.6']],
            ['CH4 from artificial water bodies', ['4.H.7']],
        ],
        "entity_mapping": {
            'CH4(2)': 'CH4',
            'N2O(2)': 'N2O',
            'Net CO2 emissions/removals(1), (2)': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO: all other LULUCF tables
    "Table5": {  # Waste overview
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 27,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['Total waste', ['5']],
            ['A. Solid waste disposal', ['5.A']],
            ['1. Managed waste disposal sites', ['5.A.1']],
            ['2. Unmanaged waste disposal sites', ['5.A.2']],
            ['3. Uncategorized waste disposal sites', ['5.A.3']],
            ['B. Biological treatment of solid waste', ['5.B']],
            ['1. Composting', ['5.B.1']],
            ['2. Anaerobic digestion at biogas facilities', ['5.B.2']],
            ['C. Incineration and open burning of waste', ['5.C']],
            ['1. Waste incineration', ['5.C.1']],
            ['2. Open burning of waste', ['5.C.2']],
            ['D. Wastewater treatment and discharge', ['5.D']],
            ['1. Domestic wastewater', ['5.D.1']],
            ['2. Industrial wastewater', ['5.D.2']],
            ['3. Other (as specified in table 5.D)', ['5.D.3']],
            ['E. Other (please specify)', ['5.E']],
            ['Other', ['5.E.5']],  # EST, NOR
            ['Recycling activities', ['5.E.1']],  # NLD
            ['Mechanical-Biological Treatment MBT', ['5.E.2']],  # DEU
            ['Accidental fires', ['5.E.3']],  # DEU, DKE, DNK, DNM
            ['Decomposition of Petroleum-Derived Surfactants', ['5.E.4']],  # JPN
            ['Decomposition of Fossil-fuel Derived Surfactants', ['5.E.4']],
            # JPN since 2023
            ['Other non-specified', ['5.E.5']],  # USA
            ['Biogas burning without energy recovery', ['5.E.6']],  # PRT
            ['Sludge spreading', ['5.E.7']],  # ESP
            ['Accidental combustion', ['5.E.3']],  # ESP
            ['Other waste', ['5.E.5']],  # CZE
            ['5.E.1 Industrial Wastewater', ['5.E.8']],  # CAN, new in 2022
            ['Accidental Fires at SWDS', ['5.E.9']],  # AUS, new in 2022
            ['Memo item:(2)', ['\IGNORE']],
            ['Long-term storage of C in waste disposal sites', ['M.Memo.LTSW']],
            ['Annual change in total long-term C storage', ['M.Memo.ACLT']],
            ['Annual change in total long-term C storage in HWP waste(3)', ['M.Memo.ACLTHWP']],
        ],
        "entity_mapping": {
            'CO2(1)': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested; memo items not read because of empty lines
    "Table5.A": {  # solid waste disposal
        "status": "tested",
        "table": {
            "firstrow": 6,
            "lastrow": 15,
            "header": ['group', 'group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA AND OTHER RELATED INFORMATION SINK CATEGORIES Annual waste at the SWDS',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION SINK CATEGORIES MCF',
                'ACTIVITY DATA AND OTHER RELATED INFORMATION SINK CATEGORIES DOCf',
                'IMPLIED EMISSION FACTOR SINK CATEGORIES CH4(1)',
                'IMPLIED EMISSION FACTOR SINK CATEGORIES CO2',
                'EMISSIONS SINK CATEGORIES CH4 Amount of CH4 flared',
                'EMISSIONS SINK CATEGORIES CH4 Amount of CH4 for energy recovery(3)',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Managed waste disposal sites', ['5.A.1']],
            ['a. Anaerobic', ['5.A.1.a']],
            ['b. Semi-aerobic', ['5.A.1.b']],
            ['2. Unmanaged waste disposal sites', ['5.A.2']],
            ['3. Uncategorized waste disposal sites', ['5.A.3']],
        ],
        "entity_mapping": {
            'EMISSIONS SINK CATEGORIES CH4 Emissions(2)': 'CH4',
            'EMISSIONS SINK CATEGORIES CO2(4) Amount of CH4 for energy recovery(3)': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table5.B": {  # Biological treatment of solid waste
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 16,
            "header": ['group', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA AND OTHER RELATED INFORMATION Annual waste amount treated',
                'IMPLIED EMISSION FACTOR CH4(1)',
                'IMPLIED EMISSION FACTOR N2O',
                'EMISSIONS CH4 Amount of CH4 flared',
                'EMISSIONS CH4 Amount of CH4 for energy recovery(3)',
            ],
            "stop_cats": [".", "", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Composting', ['5.B.1'], 0],
            ['Municipal solid waste', ['5.B.1.a'], 1],
            ['Other (please specify)(4)', ['5.B.1.b'], 1],
            ['Organic wastes households', ['5.B.1.b.i'], 2],  # NLD
            ['Organic wastes from gardens and horticulture', ['5.B.1.b.ii'], 2],  # NLD
            ['Food and garden waste', ['5.B.1.b.ii'], 2],  # DNM, DNK, DKE
            ['Industrial Solid Waste', ['5.B.1.b.iii'], 2],  # POL
            ['Home composting', ['5.B.1.b.iv'], 2],  # NOR
            ['Mixed waste', ['5.B.1.b.v'], 2],  # LTU
            ['Other waste', ['5.B.1.b.v'], 2],  # SWE
            ['Sludge', ['5.B.1.b.vi'], 2],  # HUN, EST
            ['Textile', ['5.B.1.b.vii'], 2],  # EST
            ['Wood', ['5.B.1.b.viii'], 2],  # EST
            ['Organic', ['5.B.1.b.ix'], 2],  # EST
            ['Paper', ['5.B.1.b.x'], 2],  # EST
            ['Other_SW', ['5.B.1.b.v'], 2],  # CZE
            ['MBA treated MSW', ['5.B.1.b.xi'], 2],  # LUX
            ['Specific Agricultural and Industrial Waste', ['5.B.1.b.xii'], 2],  # UKR
            ['Industrial solid waste and constr. waste', ['5.B.1.b.xiii'], 2],  # FIN
            ['Municipal sludge', ['5.B.1.b.xiv'], 2],  # FIN
            ['Industrial sludge', ['5.B.1.b.xv'], 2],  # FIN
            ['Open air composting', ['5.B.1.b.xvi'], 2],  # LIE
            ['Industrial Waste', ['5.B.1.b.xvii'], 2],  # JPN
            ['Human Waste and Johkasou sludge', ['5.B.1.b.xviii'], 2],  # JPN
            ['2. Anaerobic digestion at biogas facilities(3)', ['5.B.2'], 0],
            ['Municipal solid waste', ['5.B.2.a'], 1],
            ['Other (please specify)(4)', ['5.B.2.b'], 1],
            ['Organic wastes households', ['5.B.2.b.i'], 2],  # NLD
            ['Organic wastes from gardens and horticulture', ['5.B.2.b.ii'], 2],  # NLD
            ['Animal manure and other organic waste', ['5.B.2.b.iii'], 2],  # DNM, DNK, DKE
            ['sewage sludge', ['5.B.2.b.iv'], 2],  # LTU
            ['Other waste', ['5.B.2.b.v'], 2],  # SWE
            ['Agricultural biogas facilities', ['5.B.2.b.vi'], 2],  # CHE
            ['Other biogases from anaerobic fermentation', ['5.B.2.b.vii'], 2],  # HUN
            ['Sludge', ['5.B.2.b.iv'], 2],  # EST
            ['Anaerobic Digestion On-Farm and at Wastewater Treatment Facilities', ['5.B.2.b.viii'], 2],  # USA
            ['Other_AD', ['5.B.2.b.v'], 2],  # CZE
            ['Biogenic waste incl. wastes from Agriculture (manure)', ['5.B.2.b.ix'], 2],  # LUX
            ['Industrial solid waste and constr. waste', ['5.B.2.b.x'], 2],  # FIN
            ['Municipal sludge', ['5.B.2.b.xi'], 2],  # FIN
            ['Industrial sludge', ['5.B.2.b.xii'], 2],  # FIN
            ['Livestock manure co-digested', ['5.B.2.b.xiii'], 2],  # DEU, new in 2022
            ['Waste water', ['5.B.2.b.xiv'], 2],  # NOR, new in 2022
        ],
        "entity_mapping": {
            'EMISSIONS CH4 Emissions(2)': 'CH4',
            'EMISSIONS N2O Amount of CH4 for energy recovery(3)': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table5.C": {  # Waste incineration and open burning
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 38,
            "header": ['group', 'group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA Amount of wastes (incinerated/open burned)',
                'IMPLIED EMISSION FACTOR Amount of wastes (incinerated/open burned) CO2',
                'IMPLIED EMISSION FACTOR Amount of wastes (incinerated/open burned) CH4',
                'IMPLIED EMISSION FACTOR Amount of wastes (incinerated/open burned) N2O',
            ],
            "stop_cats": [".", "", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Waste Incineration', ['5.C.1'], 0],
            ['Biogenic (1)', ['5.C.1.a'], 1],
            ['Municipal solid waste', ['5.C.1.a.i'], 2],
            ['Other (please specify)(2)', ['5.C.1.a.ii'], 2],
            ['Industrial Solid Wastes', ['5.C.1.a.ii.1'], 3],
            ['Hazardous Waste', ['5.C.1.a.ii.2'], 3],
            ['Clinical Waste', ['5.C.1.a.ii.3'], 3],
            ['Sewage Sludge', ['5.C.1.a.ii.4'], 3],
            ['Other (please specify)', ['5.C.1.a.ii.5'], 3],
            ['Animal cremations', ['5.C.1.a.ii.5.a'], 4],  # DKE, DNK, DNM
            ['Human cremations', ['5.C.1.a.ii.5.b'], 4],  # DKE, DNK, DNM
            ['Cremation', ['5.C.1.a.ii.5.c'], 4],  # CHE, NOR, FRA, FRK
            ['cremation', ['5.C.1.a.ii.5.c'], 4],  # DEU
            ['Industrial waste', ['5.C.1.a.ii.5.d'], 4],  # NOR
            ['Biogenic other waste', ['5.C.1.a.ii.5.e'], 4],  # EST
            ['Biogenic waste other than Municipal Solid Waste', ['5.C.1.a.ii.5.e'], 4],  # ROU
            ['Sludge', ['5.C.1.a.ii.5.f'], 4],  # JPN
            ['Non-fossile liquid waste', ['5.C.1.a.ii.5.g'], 4],  # JPN
            ['Non-biogenic', ['5.C.1.b'], 1],
            ['Municipal solid waste', ['5.C.1.b.i'], 2],
            ['Other (please specify)(3)', ['5.C.1.b.ii'], 2],
            ['Industrial Solid Wastes', ['5.C.1.b.ii.1'], 3],
            ['Hazardous Waste', ['5.C.1.b.ii.2'], 3],
            ['Clinical Waste', ['5.C.1.b.ii.3'], 3],
            ['Sewage Sludge', ['5.C.1.b.ii.4'], 3],
            ['Fossil liquid waste', ['5.C.1.b.ii.5'], 3],
            ['Other (please specify)', ['5.C.1.b.ii.6'], 3],
            ['Quarantine and other waste', ['5.C.1.b.ii.6.a'], 4],  # NZL
            ['Industrial waste', ['5.C.1.b.ii.6.b'], 4],  # CHE
            ['Chemical waste', ['5.C.1.b.ii.6.c'], 4],  # GBR, GBK
            ['Flaring in the chemical industry', ['5.C.1.a.ii.6.d'], 4],  # BEL
            ['Sludge', ['5.C.1.a.ii.6.e'], 4],  # JPN
            ['Solvents', ['5.C.1.a.ii.6.f'], 4],  # GRC, AUS
            ['2. Open burning of waste', ['5.C.2'], 0],
            ['Biogenic (1)', ['5.C.2.a'], 1],
            ['Municipal solid waste', ['5.C.2.a.i'], 2],
            ['Other (please specify)', ['5.C.2.a.ii'], 2],
            ['agricultural waste', ['5.C.2.a.ii.1'], 3],  # ITA
            ['Agricultural residues', ['5.C.2.a.ii.1'], 3],  # ESP
            ['Agriculture residues', ['5.C.2.a.ii.1'], 3],  # PRT new in 2023
            ['Natural residues', ['5.C.2.a.ii.2'], 3],  # CHE
            ['Wood waste', ['5.C.2.a.ii.3'], 3],  # GBR, GBK
            ['Bonfires etc.', ['5.C.2.a.ii.4'], 3],  # DEU
            ['Bonfires', ['5.C.2.a.ii.4'], 3],  # NLD, ISL
            ['Other', ['5.C.2.a.ii.5'], 3],  # EST
            ['Other waste', ['5.C.2.a.ii.5'], 3],  # CZE
            ['Waste', ['5.C.2.a.ii.5'], 3],  # GBR new in 2023
            ['Industrial Solid Waste', ['5.C.2.a.ii.6'], 3],  # JPN
            ['Vine', ['5.C.2.a.ii.7'], 3], # AUT new in 2023
            ['Non-biogenic', ['5.C.2.b'], 1],
            ['Municipal solid waste', ['5.C.2.b.i'], 2],
            ['Other (please specify)', ['5.C.2.b.ii'], 2],
            ['Rural waste', ['5.C.2.b.ii.1'], 3],  # NZL
            ['Accidental fires (vehicles)', ['5.C.2.b.ii.2'], 3],  # GBR, GBK
            ['Accidental fires (buildings)', ['5.C.2.b.ii.3'], 3],  # GBR, GBK
            ['Bonfires', ['5.C.2.b.ii.4'], 3],  # ISL
            ['Other', ['5.C.2.b.ii.5'], 3],  # EST
            ['Other waste', ['5.C.2.b.ii.5'], 3],  # CZE
            ['Waste', ['5.C.2.b.ii.5'], 3],  # GBR new in 2023
            ['Industrial Solid Waste', ['5.C.2.b.ii.6'], 3],  # JPN
        ],
        "entity_mapping": {
            'EMISSIONS Amount of wastes (incinerated/open burned) CH4': 'CH4',
            'EMISSIONS Amount of wastes (incinerated/open burned) CO2': 'CO2',
            'EMISSIONS Amount of wastes (incinerated/open burned) N2O': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table5.D": {  # Waste incineration and open burning
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 13,
            "header": ['group', 'entity', 'entity', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA AND RELATED INFORMATION Total organic product',
                'ACTIVITY DATA AND RELATED INFORMATION Sludge removed(1)',
                'ACTIVITY DATA AND RELATED INFORMATION Sludge removed(1) N in effluent',
                'IMPLIED EMISSION FACTOR CH4(2) N in effluent',
                'IMPLIED EMISSION FACTOR N2O(3) N in effluent',
                'EMISSIONS CH4 Amount of CH4 flared',
                'EMISSIONS CH4 Amount of CH4 for Energy Recovery(5)',
            ],
            "stop_cats": [".", "", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. Domestic wastewater', ['5.D.1']],
            ['2. Industrial wastewater', ['5.D.2']],
            ['3. Other (please specify)', ['5.D.3']],
            ['Other', ['5.D.3.a']],  # EST
            ['Septic tanks', ['5.D.3.b']],  # NLD
            ['Wastewater Effluent', ['5.D.3.c']],  # NLD
            ['Fish farming', ['5.D.3.d']],  # FIN
            ['Uncategorized wastewater', ['5.D.3.a']],  # CZE
        ],
        "entity_mapping": {
            'EMISSIONS CH4 Emissions(4)': 'CH4',
            'EMISSIONS N2O(3) Amount of CH4 for Energy Recovery(5)': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Summary1.As1": {  # Summary 1, sheet 1
        "status": "tested",
         "table": {
            "firstrow": 5,
            "lastrow": 28,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["summary"],
        },
        "sector_mapping": [
            ['Total national emissions and removals', ['0']],
            ['1. Energy', ['1']],
            ['A. Fuel combustion Reference approach(2)', ['1.A-ref']],
            ['Sectoral approach(2)', ['1.A']],
            ['1. Energy industries', ['1.A.1']],
            ['2. Manufacturing industries and construction', ['1.A.2']],
            ['3. Transport', ['1.A.3']],
            ['4. Other sectors', ['1.A.4']],
            ['5. Other', ['1.A.5']],
            ['B. Fugitive emissions from fuels', ['1.B']],
            ['1. Solid fuels', ['1.B.1']],
            ['2. Oil and natural gas and other emissions from energy production',
             ['1.B.2']],
            ['C. CO2 Transport and storage', ['1.C']],
            ['2. Industrial processes and product use', ['2']],
            ['A. Mineral industry', ['2.A']],
            ['B. Chemical industry', ['2.B']],
            ['C. Metal industry', ['2.C']],
            ['D. Non-energy products from fuels and solvent use', ['2.D']],
            ['E. Electronic industry', ['2.E']],
            ['F. Product uses as substitutes for ODS', ['2.F']],
            ['G. Other product manufacture and use', ['2.G']],
            ['H. Other(3)', ['2.H']],
        ],
        "entity_mapping": {
            'NOX': 'NOx',
            'Net CO2 emissions/removals': 'CO2',
            'HFCs(1)': f'HFCS ({gwp_to_use})',
            'PFCs(1)': f'PFCS ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Summary1.As2": {  # Summary 1, sheet 2
        "status": "tested",
         "table": {
            "firstrow": 5,
            "lastrow": 34,
            "header": ['entity', 'entity', 'unit'],
            "header_fill": [True, False, True],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["summary"],
        },
        "sector_mapping": [
            ['3. Agriculture', ['3']],
            ['A. Enteric fermentation', ['3.A']],
            ['B. Manure management', ['3.B']],
            ['C. Rice cultivation', ['3.C']],
            ['D. Agricultural soils', ['3.D']],
            ['E. Prescribed burning of savannas', ['3.E']],
            ['F. Field burning of agricultural residues', ['3.F']],
            ['G. Liming', ['3.G']],
            ['H. Urea application', ['3.H']],
            ['I. Other carbon-contining fertilizers', ['3.I']],
            ['J. Other', ['3.J']],
            ['4. Land use, land-use change and forestry (4)', ['4']],
            ['A. Forest land (4)', ['4.A']],
            ['B. Cropland (4)', ['4.B']],
            ['C. Grassland (4)', ['4.C']],
            ['D. Wetlands (4)', ['4.D']],
            ['E. Settlements (4)', ['4.E']],
            ['F. Other land (4)', ['4.F']],
            ['G. Harvested wood products', ['4.G']],
            ['H. Other (4)', ['4.H']],
            ['5. Waste', ['5']],
            ['A. Solid waste disposal (5)', ['5.A']],
            ['B. Biological treatment of solid waste (5)', ['5.B']],
            ['C. Incineration and open burning of waste (5)', ['5.C']],
            ['D. Wastewater treatment and discharge', ['5.D']],
            ['E. Other (5)', ['5.E']],
            ['6. Other (please specify)(6)', ['6']],
        ],
        "entity_mapping": {
            'NOX': 'NOx',
            'Net CO2 emissions/removals': 'CO2',
            'HFCs (1)': f'HFCS ({gwp_to_use})',
            'PFCs(1)': f'PFCS ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Summary1.As3": {  # Summary 1, sheet 3
        "status": "tested",
         "table": {
            "firstrow": 5,
            "lastrow": 17,
            "header": ['entity', 'entity', 'unit'],
            "header_fill": [True, False, True],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["summary"],
        },
        "sector_mapping": [
            ['Memo items:(7)', ['\IGNORE']],
            ['International bunkers', ['M.Memo.Int']],
            ['Aviation', ['M.Memo.Int.Avi']],
            ['Navigation', ['M.Memo.Int.Mar']],
            ['Multilateral operations', ['M.Memo.Mult']],
            ['CO2 emissions from biomass', ['M.Memo.Bio']],
            ['CO2 captured', ['M.Memo.CO2Cap']],
            ['Long-term storage of C in waste disposal sites', ['M.Memo.LTSW']],
            ['Indirect N2O', ['M.Memo.IndN2O']],
            ['Indirect CO2', ['M.Memo.IndCO2']],
        ],
        "entity_mapping": {
            'NOX': 'NOx',
            'Net CO2 emissions/removals': 'CO2',
            'HFCs(1)': f'HFCS ({gwp_to_use})',
            'PFCs(1)': f'PFCS ({gwp_to_use})',
            'Unspecified mix of HFCs and PFCs(1)': f'UnspMixOfHFCsPFCs ({gwp_to_use})',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
}
