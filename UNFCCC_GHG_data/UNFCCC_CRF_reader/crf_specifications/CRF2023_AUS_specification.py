""" CRF2023 specification for Australia.
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

CRF2023_AUS = {
    # Table1 instead of 1s1 and 1s2
    "Table1": {
        "status": "to_test",
        "table": {
            "firstrow": 8,
            "lastrow": 59,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ['Total Energy', ['1']],
            ['A. Fuel combustion activities (sectoral approach)', ['1.A']],
            ['1.A.1. Energy industries', ['1.A.1']],
            ['1.A.1.a. Public electricity and heat production', ['1.A.1.a']],
            ['1.A.1.b. Petroleum refining', ['1.A.1.b']],
            ['1.A.1.c. Manufacture of solid fuels and other energy industries', ['1.A.1.c']],
            ['1.A.2. Manufacturing industries and construction', ['1.A.2']],
            ['1.A.2.a. Iron and steel', ['1.A.2.a']],
            ['1.A.2.b. Non-ferrous metals', ['1.A.2.b']],
            ['1.A.2.c. Chemicals', ['1.A.2.c']],
            ['1.A.2.d. Pulp, paper and print', ['1.A.2.d']],
            ['1.A.2.e. Food processing, beverages and tobacco', ['1.A.2.e']],
            ['1.A.2.f. Non-metallic minerals', ['1.A.2.f']],
            ['1.A.2.g. Other', ['1.A.2.g']],
            ['1.A.3. Transport', ['1.A.3']],
            ['1.A.3.a. Domestic aviation', ['1.A.3.a']],
            ['1.A.3.b. Road transportation', ['1.A.3.b']],
            ['1.A.3.c. Railways', ['1.A.3.c']],
            ['1.A.3.d. Domestic navigation', ['1.A.3.d']],
            ['1.A.3.e. Other transportation', ['1.A.3.e']],
            ['1.A.4. Other sectors', ['1.A.4']],
            ['1.A.4.a. Commercial/institutional', ['1.A.4.a']],
            ['1.A.4.b. Residential', ['1.A.4.b']],
            ['1.A.4.c. Agriculture/forestry/fishing', ['1.A.4.c']],
            ['1.A.5. Other', ['1.A.5']],
            ['1.A.5.a. Stationary', ['1.A.5.a']],
            ['1.A.5.b. Mobile', ['1.A.5.b']],
            ['1.B. Fugitive emissions from fuels', ['1.B']],
            ['1.B.1. Solid fuels', ['1.B.1']],
            ['1.B.1.a. Coal mining and handling', ['1.B.1.a']],
            ['1.B.1.b. Solid fuel transformation', ['1.B.1.b']],
            ['1.B.1.c. Other', ['1.B.1.c']],
            ['1.B.2. Oil and natural gas and other emissions from energy production',
             ['1.B.2']],
            ['1.B.2.a. Oil', ['1.B.2.a']],
            ['1.B.2.b. Natural gas', ['1.B.2.b']],
            ['1.B.2.c. Venting and flaring', ['1.B.2.c']],
            ['1.B.2.d. Other', ['1.B.2.d']],
            ['1.C. CO2 Transport and storage', ['1.C']],
            ['1.C.1. Transport of CO2', ['1.C.1']],
            ['1.C.2. Injection and storage', ['1.C.2']],
            ['1.C.3. Other', ['1.C.3']],
            ['1.D. Memo items: (1)', ['\IGNORE']],
            ['1.D.1. International bunkers', ['M.Memo.Int']],
            ['1.D.1.a. Aviation', ['M.Memo.Int.Avi']],
            ['1.D.1.b. Navigation', ['M.Memo.Int.Mar']],
            ['1.D.2. Multilateral operations', ['M.Memo.Mult']],
            ['1.D.3. CO2 emissions from biomass', ['M.Memo.Bio']],
            ['1.D.4. CO2 captured', ['M.Memo.CO2Cap']],
            ['1.D.4.a. For domestic storage', ['M.Memo.CO2Cap.Dom']],
            ['1.D.4.b. For storage in other countries', ['M.Memo.CO2Cap.Exp']],
        ],
        "entity_mapping": {
            "NOX": "NOx",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
    "Table1.A(a)s1": {
        "status": "to_test",
        "table": {
            "firstrow": 7,
            "lastrow": 88,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2 (1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'AMOUNT CAPTURED CO2'
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A. Fuel combustion', ['1.A', 'Total'], 0],
            ['Liquid fuels', ['1.A', 'Liquid'], 1],
            ['Solid fuels', ['1.A', 'Solid'], 1],
            ['Gaseous fuels (6)', ['1.A', 'Gaseous'], 1],
            ['Other fossil fuels (7)', ['1.A', 'OtherFF'], 1],
            ['Peat (8)', ['1.A', 'Peat'], 1],
            ['Biomass (3)', ['1.A', 'Biomass'], 1],
            # 1.A.1. Energy industries
            ['1.A.1. Energy industries', ['1.A.1', 'Total'], 1],
            ['Liquid fuels', ['1.A.1', 'Liquid'], 2],
            ['Solid fuels', ['1.A.1', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.1', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.1', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.1', 'Peat'], 2],
            ['Biomass (3)', ['1.A.1', 'Biomass'], 2],
            # a. Public electricity and heat production
            ['1.A.1.a. Public electricity and heat production (9)', ['1.A.1.a',
                                                                     'Total'], 2],
            ['Liquid fuels', ['1.A.1.a', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.a', 'Solid'], 3],
            ['Gaseous fuels (6)', ['1.A.1.a', 'Gaseous'], 3],
            ['Other fossil fuels (7)', ['1.A.1.a', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.1.a', 'Peat'], 3],
            ['Biomass (3)', ['1.A.1.a', 'Biomass'], 3],
            ['Drop-down list:', ['\IGNORE', '\IGNORE'], 3],  # (empty)
            # 1.A.1.a.i Electricity Generation
            ['1.A.1.a.i Electricity Generation', ['1.A.1.a.i', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.i', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.i', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.a.i', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.a.i', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.a.i', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.a.i', 'Biomass'], 4],
            # 1.A.1.a.ii Combined heat and power generation
            ['1.A.1.a.ii Combined heat and power generation', ['1.A.1.a.ii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.ii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.ii', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.a.ii', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.a.ii', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.a.ii', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.a.ii', 'Biomass'], 4],
            # 1.A.1.a.iii heat plants
            ['1.A.1.a.iii Heat plants', ['1.A.1.a.iii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.a.iii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.a.iii', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.a.iii', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.a.iii', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.a.iii', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.a.iii', 'Biomass'], 4],
            # b. Petroleum refining
            ['1.A.1.b. Petroleum refining', ['1.A.1.b', 'Total'], 2],
            ['Liquid fuels', ['1.A.1.b', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.b', 'Solid'], 3],
            ['Gaseous fuels (6)', ['1.A.1.b', 'Gaseous'], 3],
            ['Other fossil fuels (7)', ['1.A.1.b', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.1.b', 'Peat'], 3],
            ['Biomass (3)', ['1.A.1.b', 'Biomass'], 3],
            # c. Manufacture of solid fuels and other energy industries
            ['1.A.1.c. Manufacture of solid fuels and other energy industries(8)',
             ['1.A.1.c', 'Total'], 2],
            ['Liquid fuels', ['1.A.1.c', 'Liquid'], 3],
            ['Solid fuels', ['1.A.1.c', 'Solid'], 3],
            ['Gaseous fuels (6)', ['1.A.1.c', 'Gaseous'], 3],
            ['Other fossil fuels (7)', ['1.A.1.c', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.1.c', 'Peat'], 3],
            ['Biomass (3)', ['1.A.1.c', 'Biomass'], 3],
            ['Drop-down list:', ['\IGNORE', '\IGNORE'], 3],  # (empty)
            # 1.A.1.c.i Manufacture of solid fuels
            ['1.A.1.c.i Manufacture of solid fuels', ['1.A.1.c.i', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.i', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.i', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.c.i', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.c.i', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.c.i', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.c.i', 'Biomass'], 4],
            # 1.A.1.c.ii Oil and gas extraction
            ['1.A.1.c.ii Oil and gas extraction', ['1.A.1.c.ii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.ii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.ii', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.c.ii', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.c.ii', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.c.ii', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.c.ii', 'Biomass'], 4],
            # 1.A.1.c.iii Other energy industries
            ['1.A.1.c.iii Other energy industries', ['1.A.1.c.iii', 'Total'], 3],
            ['Liquid Fuels', ['1.A.1.c.iii', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.1.c.iii', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.1.c.iii', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.1.c.iii', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.1.c.iii', 'Peat'], 4],
            ['Biomass (3)', ['1.A.1.c.iii', 'Biomass'], 4],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2 (2,3)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # to test
    "Table1.A(a)s2": {
        "status": "to_test",
        "table": {
            "firstrow": 7,
            "lastrow": 119,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2 (1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'AMOUNT CAPTURED CO2',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.2 Manufacturing industries and construction', ['1.A.2', 'Total'], 0],
            ['Liquid fuels', ['1.A.2', 'Liquid'], 1],
            ['Solid fuels', ['1.A.2', 'Solid'], 1],
            ['Gaseous fuels (6)', ['1.A.2', 'Gaseous'], 1],
            ['Other fossil fuels (7)', ['1.A.2', 'OtherFF'], 1],
            ['Peat (8)', ['1.A.2', 'Peat'], 1],
            ['Biomass (3)', ['1.A.2', 'Biomass'], 1],
            # a. Iron and Steel
            ['1.A.2.a. Iron and steel', ['1.A.2.a', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.a', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.a', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.a', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.a', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.a', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.a', 'Biomass'], 2],
            # b. non-ferrous metals
            ['1.A.2.b. Non-ferrous metals', ['1.A.2.b', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.b', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.b', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.b', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.b', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.b', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.b', 'Biomass'], 2],
            # c. Chemicals
            ['1.A.2.c. Chemicals', ['1.A.2.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.c', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.c', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.c', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.c', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.c', 'Biomass'], 2],
            # d. Pulp paper print
            ['1.A.2.d. Pulp, paper and print', ['1.A.2.d', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.d', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.d', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.d', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.d', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.d', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.d', 'Biomass'], 2],
            # e. Food processing, beverages and tobacco
            ['1.A.2.e. Food processing, beverages and tobacco', ['1.A.2.e', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.e', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.e', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.e', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.e', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.e', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.e', 'Biomass'], 2],
            # f. non-metallic minerals
            ['1.A.2.f. Non-metallic minerals', ['1.A.2.f', 'Total'], 1],
            ['Liquid fuels', ['1.A.2.f', 'Liquid'], 2],
            ['Solid fuels', ['1.A.2.f', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.2.f', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.2.f', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.2.f', 'Peat'], 2],
            ['Biomass (3)', ['1.A.2.f', 'Biomass'], 2],
            # g. other
            ['g. Other (please specify)(11)', ['1.A.2.g', 'Total'], 1],
            #1.A.2.g.i Manufacturing of machinery
            ['1.A.2.g.i Manufacturing of machinery', ['1.A.2.g.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.i', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.i', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.i', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.i', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.i', 'Biomass'], 3],
            # 1.A.2.g.ii Manufacturing of transport equipment
            ['1.A.2.g.ii Manufacturing of transport equipment', ['1.A.2.g.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.ii', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.ii', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.ii', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.ii', 'Biomass'], 3],
            # 1.A.2.g.iii Mining (excluding fuels) and quarrying
            ['1.A.2.g.iii Mining (excluding fuels) and quarrying', ['1.A.2.g.iii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.iii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.iii', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.iii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.iii', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.iii', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.iii', 'Biomass'], 3],
            # 1.A.2.g.iv Wood and wood products
            ['1.A.2.g.iv Wood and wood products', ['1.A.2.g.iv', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.iv', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.iv', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.iv', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.iv', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.iv', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.iv', 'Biomass'], 3],
            # 1.A.2.g.v Construction
            ['1.A.2.g.v Construction', ['1.A.2.g.v', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.v', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.v', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.v', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.v', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.v', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.v', 'Biomass'], 3],
            # 1.A.2.g.vi Textile and leather
            ['1.A.2.g.vi Textile and leather', ['1.A.2.g.vi', 'Total'], 2],
            ['Liquid Fuels', ['1.A.2.g.vi', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.2.g.vi', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.vi', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.vi', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.2.g.vi', 'Peat'], 3],
            ['Biomass (3)', ['1.A.2.g.vi', 'Biomass'], 3],
            # 1.A.2.g.vii Off-road vehicles and other machinery
            ['1.A.2.g.vii Off-road vehicles and other machinery', ['1.A.2.g.vii', 'Total'], 2],
            ['Gasoline', ['1.A.2.g.vii', 'Gasoline'], 3],
            ['Diesel Oil', ['1.A.2.g.vii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.2.g.vii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.2.g.vii', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 3],
            ['Gaseous Fuels (6)', ['1.A.2.g.vii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.2.g.vii', 'OtherFF'], 3],
            ['Biomass (3)', ['1.A.2.g.vii', 'Biomass'], 3],
            # 1.A.2.g.viii Other (please specify)
            ['1.A.2.g.viii Other (please specify)', ['1.A.2.g.viii', 'Total'], 2],
            ['All Other Manufacturing', ['1.A.2.g.viii.3', 'Total'], 3],
            ['Liquid Fuels', ['1.A.2.g.viii.3', 'Liquid'], 4],
            ['Solid Fuels', ['1.A.2.g.viii.3', 'Solid'], 4],
            ['Gaseous Fuels (6)', ['1.A.2.g.viii.3', 'Gaseous'], 4],
            ['Other Fossil Fuels (7)', ['1.A.2.g.viii.3', 'OtherFF'], 4],
            ['Peat (8)', ['1.A.2.g.viii.3', 'Peat'], 4],
            ['Biomass (3)', ['1.A.2.g.viii.3', 'Biomass'], 4],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2 (2,3)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # to test
    "Table1.A(a)s3": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 115,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2 (1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.3 Transport', ['1.A.3', 'Total'], 0],
            ['Liquid fuels', ['1.A.3', 'Liquid'], 1],
            ['Solid fuels', ['1.A.3', 'Solid'], 1],
            ['Gaseous fuels (6)', ['1.A.3', 'Gaseous'], 1],
            ['Other fossil fuels (7)', ['1.A.3', 'OtherFF'], 1],
            ['Biomass (3)', ['1.A.3', 'Biomass'], 1],
            # a. Domestic Aviation
            ['1.A.3.a. Domestic aviation (12)', ['1.A.3.a', 'Total'], 1],
            ['Aviation gasoline', ['1.A.3.a', 'AvGasoline'], 2],
            ['Jet kerosene', ['1.A.3.a', 'JetKerosene'], 2],
            ['Biomass', ['1.A.3.a', 'Biomass'], 2],
            # b. road Transportation
            ['b. Road transportation (13)', ['1.A.3.b', 'Total'], 1],
            ['Gasoline', ['1.A.3.b', 'Gasoline'], 2],
            ['Diesel oil', ['1.A.3.b', 'DieselOil'], 2],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b', 'LPG'], 2],
            ['Other liquid fuels (please specify)', ['1.A.3.b', 'OtherLiquid'], 2],
            ['NA', ['\IGNORE', '\IGNORE'], 3],
            ['Gaseous fuels (6)', ['1.A.3.b', 'Gaseous'], 2],
            ['Biomass (3)', ['1.A.3.b', 'Biomass'], 2],
            ['Other fossil fuels (please specify) (7)', ['1.A.3.b', 'OtherFF'], 2],
            ['Lubricants', ['1.A.3.b', 'OFFLubricants'], 3],
            # i. Cars
            ['1.A.3.b.i. Cars', ['1.A.3.b.i', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.i', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.i', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.i', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.i', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.3.b.i', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.3.b.i', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.b.i', 'OtherFF'], 3],
            ['Lubricants', ['1.A.3.b.i', 'OFFLubricants'], 4],
            # ii. Light duty trucks
            ['1.A.3.b.ii. Light duty trucks', ['1.A.3.b.ii', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.ii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.ii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.ii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.ii', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.3.b.ii', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.3.b.ii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.b.ii', 'OtherFF'], 3],
            ['Lubricants', ['1.A.3.b.ii', 'OFFLubricants'], 4],
            # iii. Heavy duty trucks and buses
            ['iii. Heavy duty trucks and buses', ['1.A.3.b.iii', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.iii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.iii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.iii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.iii', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.3.b.iii', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.3.b.iii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.b.iii', 'OtherFF'], 3],
            ['Lubricants', ['1.A.3.b.iii', 'OFFLubricants'], 4],
            # iv. Motorcycles
            ['iv. Motorcycles', ['1.A.3.b.iv', 'Total'], 2],
            ['Gasoline', ['1.A.3.b.iv', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.3.b.iv', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.iv', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.3.b.iv', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.3.b.iv', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.3.b.iv', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.b.iv', 'OtherFF'], 3],
            ['Lubricants', ['1.A.3.b.iv', 'OFFLubricants'], 4],
            # v. Other
            ['v. Other (please specify)', ['1.A.3.b.v', 'Total'], 2],
            ['NA', ['\IGNORE', '\IGNORE'], 3],
            ['Gasoline', ['1.A.3.b.v', 'Gasoline'], 4],
            ['Diesel oil', ['1.A.3.b.v', 'DieselOil'], 4],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.b.v', 'LPG'], 4],
            ['Other liquid fuels (please specify)', ['1.A.3.b.v', 'OtherLiquid'], 4],
            ['NA', ['\IGNORE', '\IGNORE'], 5],
            ['Gaseous fuels (6)', ['1.A.3.b.v', 'Gaseous'], 4],
            ['Biomass (3)', ['1.A.3.b.v', 'Biomass'], 4],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.b.v', 'OtherFF'], 4],
            ['Lubricants', ['1.A.3.b.v', 'OFFLubricants'], 5],
            # c. Railways
            ['1.A.3.c. Railways', ['1.A.3.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.3.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.3.c', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.3.c', 'Gaseous'], 2],
            ['Biomass (3)', ['1.A.3.c', 'Biomass'], 2],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.c', 'OtherFF'], 2],
            ['Lubricants', ['1.A.3.c', 'OFFLubricants'], 3],
            # d. Domestic navigation
            ['d. Domestic Navigation(10)', ['1.A.3.d', 'Total'], 1],
            ['Residual fuel oil', ['1.A.3.d', 'ResFuelOil'], 2],
            ['Gas/diesel oil', ['1.A.3.d', 'GasDieselOil'], 2],
            ['Gasoline', ['1.A.3.d', 'Gasoline'], 2],
            ['Other liquid fuels (please specify)', ['1.A.3.d', 'OtherLiquid'], 2],
            ['NA', ['\IGNORE', '\IGNORE'], 3],
            ['Gaseous fuels (6)', ['1.A.3.d', 'Gaseous'], 2],
            ['Biomass (3)', ['1.A.3.d', 'Biomass'], 2],
            ['Other fossil fuels (please specify)(7)', ['1.A.3.d', 'OtherFF'], 2],
            ['Coal', ['1.A.3.d', 'OFFCoal'], 3],
            ['Lubricants', ['1.A.3.d', 'OFFLubricants'], 3],
            # e. other transportation
            # keep details also for top category as it's present
            ['e. Other transportation (please specify)', ['1.A.3.e', 'Total'], 1],
            ['Liquid fuels', ['1.A.3.e', 'Liquid'], 2],
            ['Solid fuels', ['1.A.3.e', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.3.e', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.3.e', 'OtherFF'], 2],
            ['Biomass (3)', ['1.A.3.e', 'Biomass'], 2],
            # i. pipeline
            ['1.A.3.e.i. Pipeline transport', ['1.A.3.e.i', 'Total'], 2],
            ['Liquid fuels', ['1.A.3.e.i', 'Liquid'], 3],
            ['Solid fuels', ['1.A.3.e.i', 'Solid'], 3],
            ['Gaseous fuels (6)', ['1.A.3.e.i', 'Gaseous'], 3],
            ['Other fossil fuels (7)', ['1.A.3.e.i', 'OtherFF'], 3],
            ['Biomass (3)', ['1.A.3.e.i', 'Biomass'], 3],
            # ii other
            ['1.A.3.e.ii. Other (please specify)', ['1.A.3.e.ii', 'Total'], 2],
            ['Off-Road Vehicles', ['1.A.3.e.ii.1', 'Total'], 3],
            ['Gasoline', ['1.A.3.e.ii.1', 'Gasoline'], 4],
            ['Diesel oil', ['1.A.3.e.ii.1', 'DieselOil'], 4],
            ['Liquefied petroleum gases (LPG)', ['1.A.3.e.ii.1', 'LPG'], 4],
            ['Other liquid fuels (please specify)', ['1.A.3.e.ii.1', 'OtherLiquid'], 4],
            ['NA', ['\IGNORE', '\IGNORE'], 5],
            ['Solid Fuels', ['1.A.3.e.ii.1', 'Solid'], 4],
            ['Gaseous fuels (6)', ['1.A.3.e.ii.1', 'Gaseous'], 4],
            ['Biomass (3)', ['1.A.3.e.ii.1', 'Biomass'], 4],
            ['Other Fossil Fuels (7)', ['1.A.3.e.ii.1', 'OtherFF'], 4],
            ['Biomass (3)', ['1.A.3.e.ii.1', 'Biomass'], 4],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2 (1)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # to test
    "Table1.A(a)s4": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 118,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                'AGGREGATE ACTIVITY DATA Consumption',
                'AGGREGATE ACTIVITY DATA Consumption',
                'IMPLIED EMISSION FACTORS CO2 (1)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'AMOUNT CAPTURED CO2',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.A.4 Other sectors', ['1.A.4', 'Total'], 0],
            ['Liquid fuels', ['1.A.4', 'Liquid'], 1],
            ['Solid fuels', ['1.A.4', 'Solid'], 1],
            ['Gaseous fuels (6)', ['1.A.4', 'Gaseous'], 1],
            ['Other fossil fuels (7)', ['1.A.4', 'OtherFF'], 1],
            ['Peat (8)', ['1.A.4', 'Peat'], 1],
            ['Biomass (3)', ['1.A.4', 'Biomass'], 1],
            # a. Commercial/institutional(12)
            ['1.A.4.a. Commercial/institutional(12)', ['1.A.4.a', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.a', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.a', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.4.a', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.4.a', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.4.a', 'Peat'], 2],
            ['Biomass (3)', ['1.A.4.a', 'Biomass'], 2],
            ['Drop-down list:', ['\IGNORE', '\IGNORE'], 2],  # (empty)
            # 1.A.4.a.i Stationary combustion
            ['1.A.4.a.i Stationary combustion (14)', ['1.A.4.a.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.a.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.a.i', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.4.a.i', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.4.a.i', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.4.a.i', 'Peat'], 3],
            ['Biomass (3)', ['1.A.4.a.i', 'Biomass'], 3],
            # 1.A.4.a.ii Off-road vehicles and other machinery
            ['1.A.4.a.ii Off-road vehicles and other machinery', ['1.A.4.a.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.a.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.a.ii', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.4.a.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.4.a.ii', 'OtherFF'], 3],
            ['Biomass (3)', ['1.A.4.a.ii', 'Biomass'], 3],
            # b. Residential(13)
            ['1.A.4.b. Residential (14)', ['1.A.4.b', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.b', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.b', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.4.b', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.4.b', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.4.b', 'Peat'], 2],
            ['Biomass (3)', ['1.A.4.b', 'Biomass'], 2],
            ['Drop-down list:', ['\IGNORE', '\IGNORE'], 2],  # (empty)
            # 1.A.4.b.i Stationary combustion
            ['1.A.4.b.i Stationary combustion', ['1.A.4.b.i', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.b.i', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.b.i', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.4.b.i', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.4.b.i', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.4.b.i', 'Peat'], 3],
            ['Biomass (3)', ['1.A.4.b.i', 'Biomass'], 3],
            # 1.A.4.b.ii Off-road vehicles and other machinery
            ['1.A.4.b.ii Off-road vehicles and other machinery', ['1.A.4.b.ii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.4.b.ii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.4.b.ii', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.4.b.ii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.4.b.ii', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.4.b.ii', 'Peat'], 3],
            ['Biomass (3)', ['1.A.4.b.ii', 'Biomass'], 3],
            # c. Agriculture/forestry/fishing
            ['1.A.4.c. Agriculture/forestry/fishing', ['1.A.4.c', 'Total'], 1],
            ['Liquid fuels', ['1.A.4.c', 'Liquid'], 2],
            ['Solid fuels', ['1.A.4.c', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.4.c', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.4.c', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.4.c', 'Peat'], 2],
            ['Biomass (3)', ['1.A.4.c', 'Biomass'], 2],
            # i. Stationary
            ['1.A.4.c.i. Stationary', ['1.A.4.c.i', 'Total'], 2],
            ['Liquid fuels', ['1.A.4.c.i', 'Liquid'], 3],
            ['Solid fuels', ['1.A.4.c.i', 'Solid'], 3],
            ['Gaseous fuels (6)', ['1.A.4.c.i', 'Gaseous'], 3],
            ['Other fossil fuels (7)', ['1.A.4.c.i', 'OtherFF'], 3],
            ['Peat (8)', ['1.A.4.c.i', 'Peat'], 3],
            ['Biomass (3)', ['1.A.4.c.i', 'Biomass'], 3],
            # ii. Off-road vehicles and other machinery
            ['1.A.4.c.ii. Off-road vehicles and other machinery', ['1.A.4.c.ii', 'Total'], 2],
            ['Gasoline', ['1.A.4.c.ii', 'Gasoline'], 3],
            ['Diesel oil', ['1.A.4.c.ii', 'DieselOil'], 3],
            ['Liquefied petroleum gases (LPG)', ['1.A.4.c.ii', 'LPG'], 3],
            ['Other liquid fuels (please specify)', ['1.A.4.c.ii', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.4.c.ii', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.4.c.ii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.4.c.ii', 'OtherFF'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            # iii. Fishing
            ['iii. Fishing', ['1.A.4.c.iii', 'Total'], 2],
            ['Residual fuel oil', ['1.A.4.c.iii', 'ResFuelOil'], 3],
            ['Gas/diesel oil', ['1.A.4.c.iii', 'GasDieselOil'], 3],
            ['Gasoline', ['1.A.4.c.iii', 'Gasoline'], 3],
            ['Other liquid fuels (please specify)', ['1.A.4.c.iii', 'OtherLiquid'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            ['Gaseous fuels (6)', ['1.A.4.c.iii', 'Gaseous'], 3],
            ['Biomass (3)', ['1.A.4.c.iii', 'Biomass'], 3],
            ['Other fossil fuels (please specify)(7)', ['1.A.4.c.iii', 'OtherFF'], 3],
            ['NA', ['\IGNORE', '\IGNORE'], 4],
            # 1.A.5 Other (Not specified elsewhere)(14)
            ['1.A.5 Other (Not specified elsewhere)(15)', ['1.A.5', 'Total'], 0],
            ['Liquid fuels', ['1.A.5', 'Liquid'], 2],
            ['Solid fuels', ['1.A.5', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.5', 'Gaseous'], 2],
            ['Other fossil fuels (7)', ['1.A.5', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.5', 'Peat'], 2],
            ['Biomass (3)', ['1.A.5', 'Biomass'], 2],
            # a. Stationary (please specify)
            ['1.A.5.a. Stationary (please specify)', ['1.A.5.a', 'Total'], 1],
            ['NA', ['\IGNORE', '\IGNORE'], 2],
            ['Liquid fuels', ['1.A.5.a', 'Liquid'], 2],
            ['Solid fuels', ['1.A.5.a', 'Solid'], 2],
            ['Gaseous fuels (6)', ['1.A.5.a', 'Gaseous'], 2],
            ['Other fossil fuels(7)', ['1.A.5.a', 'OtherFF'], 2],
            ['Peat (8)', ['1.A.5.a', 'Peat'], 2],
            ['Biomass (3)', ['1.A.5.a', 'Biomass'], 2],
            # b. Mobile (please specify)
            ['1.A.5.b. Mobile (please specify)', ['1.A.5.b', 'Total'], 1],
            ['Military Transport', ['1.A.5.b.xii', 'Total'], 2],
            ['Liquid Fuels', ['1.A.5.b.xii', 'Liquid'], 3],
            ['Solid Fuels', ['1.A.5.b.xii', 'Solid'], 3],
            ['Gaseous Fuels (6)', ['1.A.5.b.xii', 'Gaseous'], 3],
            ['Other Fossil Fuels (7)', ['1.A.5.b.xii', 'OtherFF'], 3],
            ['Biomass(3)', ['1.A.5.b.xii', 'Biomass'], 3],
            # Information Item
            ['Information item: (16)', ['\IGNORE', '\IGNORE'], 0],
            ['Waste incineration with energy recovery included as:', ['\IGNORE', '\IGNORE'], 1],
            ['Biomass (3)', ['\IGNORE', '\IGNORE'], 1],
            ['Fossil fuels (7)', ['\IGNORE', '\IGNORE'], 1],
        ],
        "entity_mapping": {
            'EMISSIONS CH4': "CH4",
            'EMISSIONS CO2 (2,3)': "CO2",
            'EMISSIONS N2O': "N2O",
        },
    },  # to test
    "Table1.B.1": {
        "status": "to_test",
        "table": {
            "firstrow": 7,
            "lastrow": 32,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA Amount of fuel produced',
                'IMPLIED EMISSION FACTORS CH4 (3)',
                'IMPLIED EMISSION FACTORS CO2',
                'RECOVERY/FLARING (2) CH4',
                'RECOVERY/FLARING (2) CO2',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. B. 1. a. Coal mining and handling', ['1.B.1.a'], 0],
            ['1.B.1.a.i. Underground mines (4)', ['1.B.1.a.i'], 1],
            ['1.B.1.a.i.1. Mining activities', ['1.B.1.a.i.1'], 2],
            ['1.B.1.a.i.2. Post-mining activities', ['1.B.1.a.i.2'], 2],
            ['1.B.1.a.i.3. Abandoned underground mines', ['1.B.1.a.i.3'], 2],
            ['1.B.1.a.i.4. Flaring of drained methane or conversion of '
             'methane to CO2 (5)', ['1.B.1.a.i.4'], 2],
            ['1.B.1.a.i.5. Other (please specify)', ['1.B.1.a.i.5'], 2],
            ['NA', ['\IGNORE'], 3],
            ['1.B.1.a.ii. Surface mines (4)', ['1.B.1.a.ii'], 1],
            ['1.B.1.a.ii.1. Mining activities', ['1.B.1.a.ii.1'], 2],
            ['1.B.1.a.ii.2. Post-mining activities', ['1.B.1.a.ii.2'], 2],
            ['1.B.1.a.ii.3. Other (please specify)', ['1.B.1.a.ii.3'], 2],
            ['NA', ['\IGNORE'], 3],
            ['1. B. 1. b. Solid fuel transformation (6)', ['1.B.1.b'], 0],
            ['Drop down list:', ['\IGNORE'], 1],
            ['1.B.1.b.i. Charcoal and biochar production (7)', ['1.B.1.b.i'], 1],
            ['1.B.1.b.ii. Coke production', ['1.B.1.b.ii'], 1],
            ['1.B.1.b.iii. Coal to liquids', ['1.B.1.b.iii'], 1],
            ['1.B.1.b.iv. Gas to liquids', ['1.B.1.b.iv'], 1],
            ['1.B.1.b.v. Other (please specify)', ['1.B.1.b.v'], 1],
            ['NA', ['\IGNORE'], 2],
            ['1. B. 1. c. Other (please specify) (8)', ['1.B.1.c'], 0],
            ['NA', ['\IGNORE'], 1],
        ],
        "entity_mapping": {
            'EMISSIONS (1) CH4': 'CH4',
            'EMISSIONS (1) CO2': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
    "Table1.B.2": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 33,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA (1) Description (1)',
                'ACTIVITY DATA (1) Unit (1)',
                'ACTIVITY DATA (1) Value',
                'IMPLIED EMISSION FACTORS CO2 (3)',
                'IMPLIED EMISSION FACTORS CH4',
                'IMPLIED EMISSION FACTORS N2O',
                'RECOVERY (2) CO2',
            ],
            "stop_cats": [".", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1. B. 2. a. Oil (7)', ['1.B.2.a'], 0],
            ['1.B.2.a.i. Exploration', ['1.B.2.a.1'], 1],
            ['1.B.2.a.ii. Production and upgrading (8)', ['1.B.2.a.2'], 1],
            ['1.B.2.a.iii. Transport', ['1.B.2.a.3'], 1],
            ['1.B.2.a.iv. Refining/storage', ['1.B.2.a.4'], 1],
            ['1.B.2.a.v. Distribution of oil products', ['1.B.2.a.5'], 1],
            ['1.B.2.a.vi. Other', ['1.B.2.a.6'], 1],
            ['Drop down list:', ['\IGNORE'], 2],
            ['1.B.2.a.vi.1. Abandoned wells', ['1.B.2.a.6.1'], 2],
            ['1.B.2.a.vi.2. Other (please specify)', ['1.B.1.a.6.2'], 2],
            ['NA', ['\IGNORE'], 3],
            ['1. B. 2. b. Natural gas', ['1.B.2.b'], 0],
            ['1.B.2.b.i. Exploration', ['1.B.2.b.1'], 1],
            ['1.B.2.b.ii. Production and gathering (8)', ['1.B.2.b.2'], 1],
            ['1.B.2.b.iii. Processing', ['1.B.2.b.3'], 1],
            ['1.B.2.b.iv. Transmission and storage', ['1.B.2.b.4'], 1],
            ['1.B.2.b.v. Distribution', ['1.B.2.b.5'], 1],
            ['1.B.2.b.vi. Other', ['1.B.2.b.6'], 1],
            ['Drop down list:', ['\IGNORE'], 2],
            ['1.B.2.b.vi.1. Gas post-meter', ['1.B.2.b.6.1'], 3],
            ['1.B.2.b.vi.2. Abandoned wells', ['1.B.2.b.6.2'], 3],
            ['1.B.2.b.vi.3. Other (please specify)', ['1.B.2.b.6.3'], 3],
            ['LNG Terminals', ['1.B.2.b.6.3.a'], 4],
            ['LNG Storage', ['1.B.2.b.6.3.b'], 4],
            ['Natural Gas Storage', ['1.B.2.b.6.3.c'], 4],
            ['1. B. 2. c. Venting and flaring', ['1.B.2.c'], 0],
            ['1.B.2.c.i. Venting', ['1.B.2.c-ven'], 1],
            ['1.B.2.c.i.1. Oil', ['1.B.2.c-ven.i'], 2],
            ['1.B.2.c.i.2. Gas', ['1.B.2.c-ven.ii'], 2],
            ['1.B.2.c.i.3. Combined', ['1.B.2.c-ven.iii'], 2],
            ['1.B.2.c.ii. Flaring (9)', ['1.B.2.c-fla'], 1],
            ['1.B.2.c.ii.1. Oil', ['1.B.2.c-fla.i'], 2],
            ['1.B.2.c.ii.2. Gas', ['1.B.2.c-fla.ii'], 2],
            ['1.B.2.c.ii.3. Combined', ['1.B.2.c-fla.iii'], 2],
            ['1.B.2.d. Other (please specify) (10)', ['1.B.2.d'], 0],
            ['NA', ['\IGNORE'], 1],
        ],
        "entity_mapping": {
            'EMISSIONS CH4 (5)': 'CH4',
            'EMISSIONS CO2 (4)': 'CO2',
            'EMISSIONS N2O': 'N2O',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
    "Table1.C": {
        "status": "to_test",
        "table": {
            "firstrow": 7,
            "lastrow": 29,
            "header": ['group', 'entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                'ACTIVITY DATA CO2 transported or injected (1)',
                'IMPLIED EMISSION FACTORS CO2',
            ],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['1.C.1. Transport of CO2', ['1.C.1'], 0],
            ['1.C.1.a. Pipelines', ['1.C.1.a'], 1],
            ['1.C.1.b. Ships', ['1.C.1.b'], 1],
            ['1.C.1.c. Other', ['1.C.1.c'], 1],
            ['NA', ['\IGNORE'], 2],
            ['1.C.2. Injection and storage (3)', ['1.C.2'], 0],
            ['1.C.2.a. Injection', ['1.C.2.a'], 1],
            ['1.C.2.b. Storage', ['1.C.2.b'], 1],
            ['1.C.3. Other', ['1.C.3'], 0],
            ['NA', ['\IGNORE'], 1],
            ['Information item (4, 5, 6)', ['\IGNORE']],
            ['Total amount captured for storage (7)', ['M.Info.A.TACS']],
            ['Total amount of imports for storage (7)', ['M.Info.A.TAIS']],
            ['Total A', ['M.Info.A']],
            ['Total amount of exports for storage', ['M.Info.B.TAES']],
            ['Total amount of CO2 injected at storage sites', ['M.Info.B.TAI']],
            ['CO2 injected for operational usage (8)', ['M.Info.B.IOU']],
            ['Total leakage from transport, injection and storage', ['M.Info.B.TLTIS']],
            ['Total B', ['M.Info.B']],
            ['Difference (A-B)(6)', ['\IGNORE']],
        ],
        "entity_mapping": {
            'EMISSIONS CO2 (2)': 'CO2',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to_test
    "Table1.D": {
        "status": "TODO",
        "table": {
            "firstrow": 7,
            "lastrow": 24,
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
    "Table2(I)": {
        "status": "to_test",
        "table": {
            "firstrow": 8,
            "lastrow": 58,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ['2. Total industrial processes', ['2']],
            ['2.A. Mineral industry', ['2.A']],
            ['2.A.1. Cement production', ['2.A.1']],
            ['2.A.2. Lime production', ['2.A.2']],
            ['2.A.3. Glass production', ['2.A.3']],
            ['2.A.4. Other process uses of carbonates', ['2.A.4']],
            ['2.B. Chemical industry', ['2.B']],
            ['2.B.1. Ammonia production', ['2.B.1']],
            ['2.B.2. Nitric acid production', ['2.B.2']],
            ['2.B.3. Adipic acid production', ['2.B.3']],
            ['2.B.4. Caprolactam, glyoxal and glyoxylic acid production', ['2.B.4']],
            ['2.B.5. Carbide production', ['2.B.5']],
            ['2.B.6. Titanium dioxide production', ['2.B.6']],
            ['2.B.7. Soda ash production', ['2.B.7']],
            ['2.B.8. Petrochemical and carbon black production', ['2.B.8']],
            ['2.B.9. Fluorochemical production', ['2.B.9']],
            ['2.B.10. Other', ['2.B.10']],
            ['2.C. Metal industry', ['2.C']],
            ['2.C.1. Iron and steel production', ['2.C.1']],
            ['2.C.2. Ferroalloys production', ['2.C.2']],
            ['2.C.3. Aluminium production', ['2.C.3']],
            ['2.C.4. Magnesium production', ['2.C.4']],
            ['2.C.5. Lead production', ['2.C.5']],
            ['2.C.6. Zinc production', ['2.C.6']],
            ['2.C.7. Other', ['2.C.7']],
            ['2.D. Non-energy products from fuels and solvent use (4)', ['2.D']],
            ['2.D.1. Lubricant use', ['2.D.1']],
            ['2.D.2. Paraffin wax use', ['2.D.2']],
            ['2.D.3. Other', ['2.D.3']],
            ['2.E. Electronics industry', ['2.E']],
            ['2.E.1. Integrated circuit or semiconductor', ['2.E.1']],
            ['2.E.2. TFT flat panel display', ['2.E.2']],
            ['2.E.3. Photovoltaics', ['2.E.3']],
            ['2.E.4. Heat transfer fluid', ['2.E.4']],
            ['2.E.5. Other (as specified in table 2(II))', ['2.E.5']],
            ['2.F. Product uses as substitutes for ODS(2)', ['2.F']],
            ['2.F.1. Refrigeration and air conditioning', ['2.F.1']],
            ['2.F.2. Foam blowing agents', ['2.F.2']],
            ['2.F.3. Fire protection', ['2.F.3']],
            ['2.F.4. Aerosols', ['2.F.4']],
            ['2.F.5. Solvents', ['2.F.5']],
            ['2.F.6. Other applications', ['2.F.6']],
            ['2.G. Other product manufacture and use', ['2.G']],
            ['2.G.1. Electrical equipment', ['2.G.1']],
            ['2.G.2. SF6 and PFCs from other product use', ['2.G.2']],
            ['2.G.3. N2O from product uses', ['2.G.3']],
            ['2.G.4. Other', ['2.G.4']],
            ['2.H. Other (please specify) (5)', ['2.H']],
            ['2.H.2. Food and Beverages Industry', ['2.H.2']],
        ],
        "entity_mapping": {
            'HFCs (1)': 'HFCS (AR4GWP100)',
            'PFCs (1)': 'PFCS (AR4GWP100)',
            'Unspecified mix of HFCs and PFCs(1)': 'UnspMixOfHFCsPFCs (AR4GWP100)',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
    "Table2(II)": {
        "status": "to_test",
        "table": {
            "firstrow": 8,
            "lastrow": 37, # ignore the totals
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [".", np.nan],
            "unit_info": unit_info["fgases"],
        },
        "sector_mapping": [
            ['2. Total actual emissions of halocarbons (by chemical), SF6 and NF3',
             ['2']],
            ['2.B. Chemical industry', ['2.B']],
            ['2.B.9. Flurochemical production', ['2.B.9']],
            ['2.B.9.a. By-product emissions', ['2.B.9.a']],
            ['2.B.9.b. Fugitive emissions', ['2.B.9.b']],
            ['2.B.10. Other', ['2.B.10']],
            ['2.C. Metal industry', ['2.C']],
            ['2.C.3. Aluminium production', ['2.C.3']],
            ['2.C.4. Magnesium production', ['2.C.4']],
            ['2.C.7. Other', ['2.C.7']],
            ['2.E. Electronics industry', ['2.E']],
            ['2.E.1. Integrated circuit or semiconductor', ['2.E.1']],
            ['2.E.2. TFT flat panel display', ['2.E.2']],
            ['2.E.3. Photovoltaics', ['2.E.3']],
            ['2.E.4. Heat transfer fluid', ['2.E.4']],
            ['2.E.5. Other', ['2.E.5']],
            ['2.F. Product uses as substitutes for ODS', ['2.F']],
            ['2.F.1. Refrigeration and air conditioning', ['2.F.1']],
            ['2.F.2. Foam blowing agents', ['2.F.2']],
            ['2.F.3. Fire protection', ['2.F.3']],
            ['2.F.4. Aerosols', ['2.F.4']],
            ['2.F.5. Solvents', ['2.F.5']],
            ['2.F.6. Other applications', ['2.F.6']],
            ['2.G. Other product manufacture and use', ['2.G']],
            ['2.G.1. Electrical equipment', ['2.G.1']],
            ['2.G.2. SF6 and PFCs from other product use', ['2.G.2']],
            ['2.G.4. Other', ['2.G.4']],
            ['2.H. Other (please specify)', ['2.H']],
            ['2.H.1 Pulp and paper', ['2.H.1']],
            ['2.H.2 Food and beverages industry', ['2.H.2']],
            ['2.H.3 Other (please specify)', ['2.H.3']],
        ],
        "entity_mapping": {
            #'C3F8': 'C3F8',
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
            'Unspecified mix of HFCs (1)': 'UnspMixOfHFCs (AR4GWP100)',
            'Unspecified mix of HFCs and PFCs(1)': 'UnspMixOfHFCsPFCs (AR4GWP100)',
            'Unspecified mix of PFCs (1)': 'UnspMixOfPFCs (AR4GWP100)',
            'c-C3F6': 'cC3F6',
            'c-C4F8': 'cC4F8',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
    "Table3": {  # Agriculture summary
        "status": "to_test",
        "table": {
            "firstrow": 8,
            "lastrow": 48,
            "header": ['entity', 'unit'],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", np.nan],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ['3. Total agriculture', ['3'], 0],
            # A. Enteric fermentation
            ['3.A. Enteric fermentation', ['3.A'], 2],
            ['Option A:', ['\IGNORE'], 4],
            ['3.A.1.a Dairy cattle', ['3.A.1.Aa'], 5],
            ['3.A.1.b Non-dairy cattle', ['3.A.1.Ab'], 5],
            ['Option B (country-specific):', ['\IGNORE'], 4],
            ['3.A.1.a Other', ['3.A.1.C'], 5],
            # Other livestock
            ['3.A.2. Sheep', ['3.A.2'], 3],
            ['3.A.3. Swine', ['3.A.3'], 3],
            ['3.A.4. Other livestock', ['3.A.4'], 3],
            # Manure Management
            ['3.B. Manure management', ['3.B'], 2],
            ['3.B.1. Cattle(1)', ['3.B.1'], 3],
            ['Option A:', ['\IGNORE'], 4],
            ['3.B.1.a. Dairy cattle', ['3.B.1.Aa'], 5],
            ['3.B.1.b. Non-dairy cattle', ['3.B.1.Ab'], 5],
            ['Option B:', ['\IGNORE'], 4],
            ['3.B.1.a Other', ['3.B.1.C'], 5],
            ['2.B.2. Sheep', ['3.B.2'], 3],
            ['2.B.3. Swine', ['3.B.3'], 3],
            ['2.B.4. Other livestock', ['3.B.4'], 3],
            ['3.B.5. Indirect N2O emissions', ['3.B.5'], 3],
            ['3.C. Rice cultivation', ['3.C']],
            ['3.D. Agricultural soils(4,5)', ['3.D']],
            ['3.D.1. Direct N2O emissions from managed soils', '3.D.a']
            ['3.D.1.a. Inorganic N fertilizers', ['3.D.a.1']],
            ['3.D.1.b. Organic N fertilizers', ['3.D.a.2']],
            ['3.D.1.c. Urine and dung deposited by grazing animals', ['3.D.a.3']],
            ['3.D.1.d. Crop residues', ['3.D.a.4']],
            ['3.D.1.e. Mineralization/immobilization associated with loss/gain of '
             'soil organic matter', ['3.D.a.5']],
            ['3.D.1.f. Cultivation of organic soils (i.e. histosols)', ['3.D.a.6']],
            ['3.D.1.g. Other', ['3.D.a.7']],
            ['3.D.2. Indirect N2O Emissions from managed soils', ['3.D.b']],
            ['3.E. Prescribed burning of savannahs', ['3.E']],
            ['3.F. Field burning of agricultural residues', ['3.F']],
            ['3.G. Liming', ['3.G']],
            ['3.H. Urea application', ['3.H']],
            ['3.I. Other carbon-containing fertilizers', ['3.I']],
            ['3.J. Other (please specify)', ['3.J']],
            ['NA', ['\IGNORE']],
        ],
        "coords_defaults": {
            "class": "Total",
        },
    },  # to test
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
            ['Intermittently flooded Single aeration', ['3.C.1.a.i']],
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
            'HFCs(1)': 'HFCS (AR4GWP100)',
            'PFCs(1)': 'PFCS (AR4GWP100)',
            'Unspecified mix of HFCs and PFCs(1)': 'UnspMixOfHFCsPFCs (AR4GWP100)',
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
            'HFCs (1)': 'HFCS (AR4GWP100)',
            'PFCs(1)': 'PFCS (AR4GWP100)',
            'Unspecified mix of HFCs and PFCs(1)': 'UnspMixOfHFCsPFCs (AR4GWP100)',
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
            'HFCs(1)': 'HFCS (AR4GWP100)',
            'PFCs(1)': 'PFCS (AR4GWP100)',
            'Unspecified mix of HFCs and PFCs(1)': 'UnspMixOfHFCsPFCs (AR4GWP100)',
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
}
