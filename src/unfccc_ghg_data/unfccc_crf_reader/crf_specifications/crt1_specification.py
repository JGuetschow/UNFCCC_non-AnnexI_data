"""

CRT1 specification So far based on Australia only.

Since 2023 Australia reports in the CRT (common reporting tables) format which is
similar but not identical to CRF. Some tables are different and it is more
consistent in using sector titles etc. Thus it needs a special specification.

Currently not all tables are included. Extend if you need all country
specific items in categories XXXXX

Tables included:

* **Energy:** 'Table1', 'Table1.A(a)s1', 'Table1.A(a)s2', 'Table1.A(a)s3',
  'Table1.A(a)s4', 'Table1.B.1', 'Table1.B.2', 'Table1.C',
* **Industrial processes:** 'Table2(I), 'Table2(II)',
* **Agriculture:** 'Table3', 'Table3.A', 'Table3.B(a)', 'Table3.B(b)', 'Table3.C', 'Table3.D',
* **LULUCF:**  'Table4',
* **Waste:**  'Table5',
* **Summary:** 'Summary1'

Missing tables are:

* **Energy:** 'Table1.A(b)', 'Table1.A(c)', 'Table1.A(d)', 'Table1.D'
* **Industrial processes:** 'Table2(I).A-H', 'Table2(II)B-Hs1', 'Table2(II)B-Hs2',
* **Agriculture:** 'Table3.E', 'Table3.F', 'Table3.G-I',
* **LULUCF**: All tables except Table4
* **Waste**:  'Table5.A', 'Table5.B', 'Table5.C', 'Table5.D'
* **Summary:** 'Summary2', 'Summary3', 'Flex_summary',
* **other:** 'Table6', 'Table7', 'Table8s1', 'Table8s2',
  'Table9', 'Table10s1', 'Table10s2', 'Table10s3', 'Table10s4', 'Table10s5',
  'Table10s6'



TODO:
 * Add missing tables
 * Add activity data

"""

from .util import unit_info

gwp_to_use = "AR5GWP100"

CRT1 = {
    # Table1 instead of 1s1 and 1s2
    "Table1": {
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 61,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [
                "",
                "nan",
                '(1) "Total GHG emissions" does not include NOX, ' "CO, NMVOC and SOX.",
            ],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ["Total Energy", ["1"]],
            ["1.A. Fuel combustion activities (sectoral approach)", ["1.A"]],
            ["1.A.1. Energy industries", ["1.A.1"]],
            ["1.A.1.a. Public electricity and heat production", ["1.A.1.a"]],
            ["1.A.1.b. Petroleum refining", ["1.A.1.b"]],
            [
                "1.A.1.c. Manufacture of solid fuels and other energy industries",
                ["1.A.1.c"],
            ],
            ["1.A.2. Manufacturing industries and construction", ["1.A.2"]],
            ["1.A.2.a. Iron and steel", ["1.A.2.a"]],
            ["1.A.2.b. Non-ferrous metals", ["1.A.2.b"]],
            ["1.A.2.c. Chemicals", ["1.A.2.c"]],
            ["1.A.2.d. Pulp, paper and print", ["1.A.2.d"]],
            ["1.A.2.e. Food processing, beverages and tobacco", ["1.A.2.e"]],
            ["1.A.2.f. Non-metallic minerals", ["1.A.2.f"]],
            ["1.A.2.g. Other", ["1.A.2.g"]],
            ["1.A.3. Transport", ["1.A.3"]],
            ["1.A.3.a. Domestic aviation", ["1.A.3.a"]],
            ["1.A.3.b. Road transportation", ["1.A.3.b"]],
            ["1.A.3.c. Railways", ["1.A.3.c"]],
            ["1.A.3.d. Domestic navigation", ["1.A.3.d"]],
            ["1.A.3.e. Other transportation", ["1.A.3.e"]],
            ["1.A.4. Other sectors", ["1.A.4"]],
            ["1.A.4.a. Commercial/institutional", ["1.A.4.a"]],
            ["1.A.4.b. Residential", ["1.A.4.b"]],
            ["1.A.4.c. Agriculture/forestry/fishing", ["1.A.4.c"]],
            ["1.A.5. Other", ["1.A.5"]],
            ["1.A.5.a. Stationary", ["1.A.5.a"]],
            ["1.A.5.b. Mobile", ["1.A.5.b"]],
            ["1.B. Fugitive emissions from fuels", ["1.B"]],
            ["1.B.1. Solid fuels", ["1.B.1"]],
            ["1.B.1.a. Coal mining and handling", ["1.B.1.a"]],
            ["1.B.1.b. Fuel transformation", ["1.B.1.b"]],
            ["1.B.1.c. Other", ["1.B.1.c"]],
            [
                "1.B.2. Oil and natural gas and other emissions from energy production",
                ["1.B.2"],
            ],
            ["1.B.2.a. Oil", ["1.B.2.a"]],
            ["1.B.2.b. Natural gas", ["1.B.2.b"]],
            ["1.B.2.c. Venting and flaring", ["1.B.2.c"]],
            ["1.B.2.d. Other", ["1.B.2.d"]],
            ["1.C. CO2 Transport and storage", ["1.C"]],
            ["1.C.1. Transport of CO2", ["1.C.1"]],
            ["1.C.2. Injection and storage", ["1.C.2"]],
            ["1.C.3. Other", ["1.C.3"]],
            ["1.D. Memo items: (3)", ["\\IGNORE"]],
            ["1.D.1. International bunkers", ["M.Memo.Int"]],
            ["1.D.1.a. Aviation", ["M.Memo.Int.Avi"]],
            ["1.D.1.b.Navigation", ["M.Memo.Int.Mar"]],
            ["1.D.2. Multilateral operations", ["M.Memo.Mult"]],
            ["1.D.3. CO2 emissions from biomass", ["M.Memo.Bio"]],
            ["1.D.4. CO2 captured", ["M.Memo.CO2Cap"]],
            ["1.D.4.a. For domestic storage", ["M.Memo.CO2Cap.Dom"]],
            ["1.D.4.b. For storage in other countries", ["M.Memo.CO2Cap.Exp"]],
        ],
        "entity_mapping": {
            "NOX": "NOx",
            "Total GHG emissions (1)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.A(a)s1": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 88,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                "AGGREGATE ACTIVITY DATA Consumption",
                "AGGREGATE ACTIVITY DATA Consumption",
                "IMPLIED EMISSION FACTORS CO2 (1)",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
                "AMOUNT CAPTURED (4) CO2",
            ],
            "stop_cats": [
                "",
                "nan",
                "Note: Minimum level of aggregation is needed to protect "
                "confidential business and military information, where it "
                "would identify particular entity's/entities' "
                "confidential data.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.A. Fuel combustion", ["1.A", "Total"], 0],
            ["Liquid fuels", ["1.A", "Liquid"], 1],
            ["Solid fuels", ["1.A", "Solid"], 1],
            ["Gaseous fuels (6)", ["1.A", "Gaseous"], 1],
            ["Other fossil fuels (7)", ["1.A", "OtherFF"], 1],
            ["Peat (8)", ["1.A", "Peat"], 1],
            ["Biomass (3)", ["1.A", "Biomass"], 1],
            # 1.A.1. Energy industries
            ["1.A.1. Energy industries", ["1.A.1", "Total"], 1],
            ["Liquid fuels", ["1.A.1", "Liquid"], 2],
            ["Solid fuels", ["1.A.1", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.1", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.1", "OtherFF"], 2],
            ["Peat (8)", ["1.A.1", "Peat"], 2],
            ["Biomass (3)", ["1.A.1", "Biomass"], 2],
            # a. Public electricity and heat production
            [
                "1.A.1.a. Public electricity and heat production (9)",
                ["1.A.1.a", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.1.a", "Liquid"], 3],
            ["Solid fuels", ["1.A.1.a", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.1.a", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.1.a", "OtherFF"], 3],
            ["Peat (8)", ["1.A.1.a", "Peat"], 3],
            ["Biomass (3)", ["1.A.1.a", "Biomass"], 3],
            ["Drop-down list:", ["\\IGNORE", "\\IGNORE"], 3],  # (empty)
            # 1.A.1.a.i Electricity Generation
            ["1.A.1.a.i. Electricity generation", ["1.A.1.a.i", "Total"], 3],
            ["Liquid fuels", ["1.A.1.a.i", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.a.i", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.a.i", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.a.i", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.a.i", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.a.i", "Biomass"], 4],
            # 1.A.1.a.ii Combined heat and power generation
            [
                "1.A.1.a.ii. Combined heat and power generation",
                ["1.A.1.a.ii", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.1.a.ii", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.a.ii", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.a.ii", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.a.ii", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.a.ii", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.a.ii", "Biomass"], 4],
            # 1.A.1.a.iii heat plants
            ["1.A.1.a.iii. Heat plants", ["1.A.1.a.iii", "Total"], 3],
            ["Liquid fuels", ["1.A.1.a.iii", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.a.iii", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.a.iii", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.a.iii", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.a.iii", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.a.iii", "Biomass"], 4],
            # b. Petroleum refining
            ["1.A.1.b. Petroleum refining", ["1.A.1.b", "Total"], 2],
            ["Liquid fuels", ["1.A.1.b", "Liquid"], 3],
            ["Solid fuels", ["1.A.1.b", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.1.b", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.1.b", "OtherFF"], 3],
            ["Peat (8)", ["1.A.1.b", "Peat"], 3],
            ["Biomass (3)", ["1.A.1.b", "Biomass"], 3],
            # c. Manufacture of solid fuels and other energy industries
            [
                "1.A.1.c. Manufacture of solid fuels and other energy industries (10)",
                ["1.A.1.c", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.1.c", "Liquid"], 3],
            ["Solid fuels", ["1.A.1.c", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.1.c", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.1.c", "OtherFF"], 3],
            ["Peat (8)", ["1.A.1.c", "Peat"], 3],
            ["Biomass (3)", ["1.A.1.c", "Biomass"], 3],
            ["Drop-down list:", ["\\IGNORE", "\\IGNORE"], 3],  # (empty)
            # 1.A.1.c.i Manufacture of solid fuels
            ["1.A.1.c.i. Manufacture of solid fuels", ["1.A.1.c.i", "Total"], 3],
            ["Liquid fuels", ["1.A.1.c.i", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.c.i", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.c.i", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.c.i", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.c.i", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.c.i", "Biomass"], 4],
            # 1.A.1.c.ii Oil and gas extraction
            ["1.A.1.c.ii. Oil and gas extraction", ["1.A.1.c.ii", "Total"], 3],
            ["Liquid fuels", ["1.A.1.c.ii", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.c.ii", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.c.ii", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.c.ii", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.c.ii", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.c.ii", "Biomass"], 4],
            # 1.A.1.c.iii Other energy industries
            ["1.A.1.c.iii. Other energy industries", ["1.A.1.c.iii", "Total"], 3],
            ["Liquid fuels", ["1.A.1.c.iii", "Liquid"], 4],
            ["Solid fuels", ["1.A.1.c.iii", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.1.c.iii", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.1.c.iii", "OtherFF"], 4],
            ["Peat (8)", ["1.A.1.c.iii", "Peat"], 4],
            ["Biomass (3)", ["1.A.1.c.iii", "Biomass"], 4],
        ],
        "entity_mapping": {
            "EMISSIONS CH4": "CH4",
            "EMISSIONS CO2 (2,3)": "CO2",
            "EMISSIONS N2O": "N2O",
        },
    },  # tested
    "Table1.A(a)s2": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 131,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                "AGGREGATE ACTIVITY DATA Consumption",
                "AGGREGATE ACTIVITY DATA Consumption",
                "IMPLIED EMISSION FACTORS CO2 (1)",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
                "AMOUNT CAPTURED (4) CO2",
            ],
            "stop_cats": [
                "",
                "nan",
                "Note: Minimum level of aggregation is needed to protect "
                "confidential business and military information, where it "
                "would identify particular entity's/entities' confidential "
                "data.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.A.2 Manufacturing industries and construction", ["1.A.2", "Total"], 0],
            ["Liquid fuels", ["1.A.2", "Liquid"], 1],
            ["Solid fuels", ["1.A.2", "Solid"], 1],
            ["Gaseous fuels (6)", ["1.A.2", "Gaseous"], 1],
            ["Other fossil fuels (7)", ["1.A.2", "OtherFF"], 1],
            ["Peat (8)", ["1.A.2", "Peat"], 1],
            ["Biomass (3)", ["1.A.2", "Biomass"], 1],
            # a. Iron and Steel
            ["1.A.2.a. Iron and steel", ["1.A.2.a", "Total"], 1],
            ["Liquid fuels", ["1.A.2.a", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.a", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.a", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.a", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.a", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.a", "Biomass"], 2],
            # b. non-ferrous metals
            ["1.A.2.b. Non-ferrous metals", ["1.A.2.b", "Total"], 1],
            ["Liquid fuels", ["1.A.2.b", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.b", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.b", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.b", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.b", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.b", "Biomass"], 2],
            # c. Chemicals
            ["1.A.2.c. Chemicals", ["1.A.2.c", "Total"], 1],
            ["Liquid fuels", ["1.A.2.c", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.c", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.c", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.c", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.c", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.c", "Biomass"], 2],
            # d. Pulp paper print
            ["1.A.2.d. Pulp, paper and print", ["1.A.2.d", "Total"], 1],
            ["Liquid fuels", ["1.A.2.d", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.d", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.d", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.d", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.d", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.d", "Biomass"], 2],
            # e. Food processing, beverages and tobacco
            [
                "1.A.2.e. Food processing, beverages and tobacco",
                ["1.A.2.e", "Total"],
                1,
            ],
            ["Liquid fuels", ["1.A.2.e", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.e", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.e", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.e", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.e", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.e", "Biomass"], 2],
            # f. non-metallic minerals
            ["1.A.2.f. Non-metallic minerals", ["1.A.2.f", "Total"], 1],
            ["Liquid fuels", ["1.A.2.f", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.f", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.f", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.f", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.f", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.f", "Biomass"], 2],
            # g. other
            ["1.A.2.g. Other (11)", ["1.A.2.g", "Total"], 1],
            ["Liquid fuels", ["1.A.2.g", "Liquid"], 2],
            ["Solid fuels", ["1.A.2.g", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.2.g", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.2.g", "OtherFF"], 2],
            ["Peat (8)", ["1.A.2.g", "Peat"], 2],
            ["Biomass (3)", ["1.A.2.g", "Biomass"], 2],
            ["Drop-down list:", ["\\IGNORE", "\\IGNORE"], 2],
            # TODO currently different parent category strings need repetition of the
            #  full tree. Fix or make individual mappings for countries below
            # # ARG, ECU
            # ["1.A.2.g. Other (please specify)(11)", ["1.A.2.g", "Total"], 1],
            # # CHL
            # ["1.A.2.g. Other (please specify) (11)", ["1.A.2.g", "Total"], 1],
            # ["Dropdown list", ["\\IGNORE", "\\IGNORE"], 2],
            # 1.A.2.g.i Manufacturing of machinery
            ["1.A.2.g.i. Manufacturing of machinery", ["1.A.2.g.i", "Total"], 2],
            ["Liquid fuels", ["1.A.2.g.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.2.g.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.i", "Biomass"], 3],
            # 1.A.2.g.ii Manufacturing of transport equipment
            [
                "1.A.2.g.ii. Manufacturing of transport equipment",
                ["1.A.2.g.ii", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.2.g.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.2.g.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.ii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.ii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.ii", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.ii", "Biomass"], 3],
            # 1.A.2.g.iii Mining (excluding fuels) and quarrying
            [
                "1.A.2.g.iii. Mining (excluding fuels) and quarrying",
                ["1.A.2.g.iii", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.2.g.iii", "Liquid"], 3],
            ["Solid fuels", ["1.A.2.g.iii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.iii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.iii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.iii", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.iii", "Biomass"], 3],
            # 1.A.2.g.iv Wood and wood products
            ["1.A.2.g.iv. Wood and wood products", ["1.A.2.g.iv", "Total"], 2],
            ["Liquid fuels", ["1.A.2.g.iv", "Liquid"], 3],
            ["Solid Fuels", ["1.A.2.g.iv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.iv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.iv", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.iv", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.iv", "Biomass"], 3],
            # 1.A.2.g.v Construction
            ["1.A.2.g.v. Construction", ["1.A.2.g.v", "Total"], 2],
            ["Liquid fuels", ["1.A.2.g.v", "Liquid"], 3],
            ["Solid fuels", ["1.A.2.g.v", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.v", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.v", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.v", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.v", "Biomass"], 3],
            # 1.A.2.g.vi Textile and leather
            ["1.A.2.g.vi. Textile and leather", ["1.A.2.g.vi", "Total"], 2],
            ["Liquid fuels", ["1.A.2.g.vi", "Liquid"], 3],
            ["Solid fuels", ["1.A.2.g.vi", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.2.g.vi", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.vi", "OtherFF"], 3],
            ["Peat (8)", ["1.A.2.g.vi", "Peat"], 3],
            ["Biomass (3)", ["1.A.2.g.vi", "Biomass"], 3],
            # 1.A.2.g.vii Off-road vehicles and other machinery
            [
                "1.A.2.g.vii. Off-road vehicles and other machinery",
                ["1.A.2.g.vii", "Total"],
                2,
            ],
            ["Gasoline", ["1.A.2.g.vii", "Gasoline"], 3],
            ["Diesel oil", ["1.A.2.g.vii", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.2.g.vii", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.2.g.vii", "OtherLiquid"], 3],
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.e.ii]",
                ["1.A.2.g.vii", "OLOther"],
                4,
            ],
            # SGP
            ["Residual fuel oil", ["1.A.2.g.vii", "ResFuelOil"], 4],
            # CAN
            [
                "Biodiesel (5 percent fossil portion)",
                ["1.A.2.g.vii", "OLBiodieselFC"],
                4,
            ],
            ["Lubricating Oil (Two-Stroke Engines)", ["1.A.2.g.vii", "Lubricants"], 4],
            # FIN
            ["Gasoil", ["1.A.2.g.vii", "Gasoil"], 4],
            # SWE
            ["All Liquid Fuels", ["1.A.2.g.vii", "OLOther"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.vii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.2.g.vii", "OtherFF"], 3],
            ["Biomass (3)", ["1.A.2.g.vii", "Biomass"], 3],
            # 1.A.2.g.viii Other (please specify)
            ["1.A.2.g.viii. Other (please specify)", ["1.A.2.g.viii", "Total"], 2],
            ["All Other Manufacturing", ["1.A.2.g.viii.3", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.3", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.3", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.3", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.3", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.3", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.3", "Biomass"], 4],
            # GUY
            [
                "Non-specified Industry [IPCC Software 1.A.2.m]",
                ["1.A.2.g.viii.1", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # GUY, MDV
            [
                "Off-road - Manufacturing industries and construction- "
                "solid fuels [IPCC Software 1.A.3.e.ii]",
                ["1.A.2.g.viii.12", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.2.g.viii.12", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.12", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.12", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.12", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.12", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.12", "Biomass"], 4],
            # SVN
            [
                "Other manufacturing industries and construction",
                ["1.A.2.g.viii.1", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # MCO
            ["industry", ["1.A.2.g.viii.1", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # SVN
            ["Non-specified Industry", ["1.A.2.g.viii.1", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # LTU
            ["Non-specified industry", ["1.A.2.g.viii.1", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # ARG
            ["Unspecified industries", ["1.A.2.g.viii.1", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.1", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.1", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.1", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.1", "Biomass"], 4],
            # MLT
            ["All Industry", ["1.A.2.g.viii.2", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.2", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.2", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.2", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.2", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.2", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.2", "Biomass"], 4],
            # AUT
            ["Other manufacturing industries", ["1.A.2.g.viii.3", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.3", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.3", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.3", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.3", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.3", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.3", "Biomass"], 4],
            # NOR
            ["Other Manufacturing", ["1.A.2.g.viii.3", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.3", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.3", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.3", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.3", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.3", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.3", "Biomass"], 4],
            # BEL
            ["Other non-specified", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # CZE
            ["Other non_specified", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # BRA
            ["Not specified", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # GHA
            ["Non-specified sectors", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # NLD
            ["Other Industrial Sectors", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # CHN
            [
                "Manufacturing industries which separate data are not available",
                ["1.A.2.g.viii.4", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # RUS
            ["Other industries", ["1.A.2.g.viii.4", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.4", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.4", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.4", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.4", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.4", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.4", "Biomass"], 4],
            # RUS
            ["Non-CO2 emissions from BFG combustion", ["1.A.2.g.viii.5", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.5", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.5", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.5", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.5", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.5", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.5", "Biomass"], 4],
            # ESP, NZL, POL, TUR
            ["Other", ["1.A.2.g.viii.10", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.10", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.10", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.10", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.10", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.10", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.10", "Biomass"], 4],
            # HRV
            ["other", ["1.A.2.g.viii.10", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.10", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.10", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.10", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.10", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.10", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.10", "Biomass"], 4],
            # SGP
            ["Others", ["1.A.2.g.viii.10", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.10", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.10", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.10", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.10", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.10", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.10", "Biomass"], 4],
            # RUS
            ["Construction", ["1.A.2.g.viii.11", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.11", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.11", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.11", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.11", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.11", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.11", "Biomass"], 4],
            # CHE
            ["Other Boilers and Engines Industry", ["1.A.2.g.viii.9", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.9", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.9", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.9", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.9", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.9", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.9", "Biomass"], 4],
            # PRT
            ["Rubber", ["1.A.2.g.viii.6", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.6", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.6", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.6", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.6", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.6", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.6", "Biomass"], 4],
            ["Other Transformation Industry", ["1.A.2.g.viii.13", "Total"], 3],
            ["Liquid fuels", ["1.A.2.g.viii.13", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.13", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.13", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.13", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.13", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.13", "Biomass"], 4],
            # USA
            [
                "Construction, agriculture, and other non-transport vehicles",
                ["1.A.2.g.viii.11", "Total"],
                3,
            ],
            ["Liquid fuels", ["1.A.2.g.viii.11", "Liquid"], 4],
            ["Solid fuels", ["1.A.2.g.viii.11", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.2.g.viii.11", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.2.g.viii.11", "OtherFF"], 4],
            ["Peat (8)", ["1.A.2.g.viii.11", "Peat"], 4],
            ["Biomass (3)", ["1.A.2.g.viii.11", "Biomass"], 4],
            # SWE
            [
                "All stationary combustin within CRF 1.A.2.g",
                ["1.A.2.g.viii.7", "Total"],
                3,
            ],
            ["Liquid Fuels", ["1.A.2.g.viii.7", "Liquid"], 4],
            ["Solid Fuels", ["1.A.2.g.viii.7", "Solid"], 4],
            ["Gaseous Fuels", ["1.A.2.g.viii.7", "Gaseous"], 4],
            ["Other Fossil Fuels", ["1.A.2.g.viii.7", "OtherFF"], 4],
            ["Peat", ["1.A.2.g.viii.7", "Peat"], 4],
            ["Biomass", ["1.A.2.g.viii.7", "Biomass"], 4],
        ],
        "entity_mapping": {
            "EMISSIONS CH4": "CH4",
            "EMISSIONS CO2 (2,3)": "CO2",
            "EMISSIONS N2O": "N2O",
        },
    },  # tested
    "Table1.A(a)s3": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 121,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                "AGGREGATE ACTIVITY DATA Consumption",
                "AGGREGATE ACTIVITY DATA Consumption",
                "IMPLIED EMISSION FACTORS CO2 (1)",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
            ],
            "stop_cats": [
                "Note: Minimum level of aggregation is needed to protect confidential "
                "business and military information, where it would identify particular "
                "entity's/entities' confidential data."
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.A.3 Transport", ["1.A.3", "Total"], 0],
            ["Liquid fuels", ["1.A.3", "Liquid"], 1],
            ["Solid fuels", ["1.A.3", "Solid"], 1],
            ["Gaseous fuels (6)", ["1.A.3", "Gaseous"], 1],
            ["Other fossil fuels (7)", ["1.A.3", "OtherFF"], 1],
            ["Biomass (3)", ["1.A.3", "Biomass"], 1],
            # a. Domestic Aviation
            ["1.A.3.a. Domestic aviation (12)", ["1.A.3.a", "Total"], 1],
            ["Aviation gasoline", ["1.A.3.a", "AvGasoline"], 2],
            ["Jet kerosene", ["1.A.3.a", "JetKerosene"], 2],
            ["Biomass", ["1.A.3.a", "Biomass"], 2],
            # b. road Transportation
            ["1.A.3.b. Road transportation (13)", ["1.A.3.b", "Total"], 1],
            ["Gasoline", ["1.A.3.b", "Gasoline"], 2],
            ["Diesel oil", ["1.A.3.b", "DieselOil"], 2],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b", "LPG"], 2],
            ["Other liquid fuels", ["1.A.3.b", "OtherLiquid"], 2],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            ["Gaseous fuels (6)", ["1.A.3.b", "Gaseous"], 2],
            ["Biomass (3)", ["1.A.3.b", "Biomass"], 2],
            ["Other fossil fuels (7)", ["1.A.3.b", "OtherFF"], 2],
            ["Lubricants", ["1.A.3.b", "OFFLubricants"], 3],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            # i. Cars
            ["1.A.3.b.i. Cars", ["1.A.3.b.i", "Total"], 2],
            ["Gasoline", ["1.A.3.b.i", "Gasoline"], 3],
            ["Diesel oil", ["1.A.3.b.i", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.i", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.3.b.i", "OtherLiquid"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.b.i, 1.A.3.b.i.1, 1.A.3.b.i.2]",
                ["1.A.3.b.i", "OLOther"],
                4,
            ],
            # RUS
            ["Other motor fuels", ["1.A.3.b.i", "OMotorFuel"], 4],
            ["Gaseous fuels (6)", ["1.A.3.b.i", "Gaseous"], 3],
            ["Biomass (3)", ["1.A.3.b.i", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.i", "OtherFF"], 3],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.b.i, 1.A.3.b.i.1, 1.A.3.b.i.2]",
                ["1.A.3.b.i", "OFFOther"],
                4,
            ],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            ["Lubricants", ["1.A.3.b.i", "OFFLubricants"], 4],
            # AUT
            ["FAME fossil part", ["1.A.3.b.i", "OFFBiodieselFC"], 4],
            # ESP
            ["Fossil part of biodiesel", ["1.A.3.b.i", "OFFBiodieselFC"], 4],
            # SVN
            ["Fossil part of biofuel", ["1.A.3.b.i", "OFFBiofuelFC"], 4],
            # SVK
            ["Fossil part of biofuels", ["1.A.3.b.i", "OFFBiofuelFC"], 4],
            # NOR
            ["Biodiesel fossil fraction", ["1.A.3.b.i", "OFFBiodieselFC"], 4],
            # NZL
            ["Biodiesel (fossil fraction)", ["1.A.3.b.i", "OFFBiodieselFC"], 4],
            # POL
            ["Other fossil fuels", ["1.A.3.b.i", "OFFOther"], 4],
            # ii. Light duty trucks
            ["1.A.3.b.ii. Light duty trucks", ["1.A.3.b.ii", "Total"], 2],
            ["Gasoline", ["1.A.3.b.ii", "Gasoline"], 3],
            ["Diesel oil", ["1.A.3.b.ii", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.ii", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.3.b.ii", "OtherLiquid"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.b.ii, 1.A.3.b.ii.1, 1.A.3.b.ii.2]",
                ["1.A.3.b.ii", "OLOther"],
                4,
            ],
            # RUS
            ["Other motor fuels", ["1.A.3.b.ii", "OMotorFuel"], 4],
            ["Gaseous fuels (6)", ["1.A.3.b.ii", "Gaseous"], 3],
            ["Biomass (3)", ["1.A.3.b.ii", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.ii", "OtherFF"], 3],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.b.ii, 1.A.3.b.ii.1, 1.A.3.b.ii.2]",
                ["1.A.3.b.ii", "OFFOther"],
                4,
            ],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            ["Lubricants", ["1.A.3.b.ii", "OFFLubricants"], 4],
            # AUT
            ["FAME fossil part", ["1.A.3.b.ii", "OFFBiodieselFC"], 4],
            # ESP
            ["Fossil part of biodiesel", ["1.A.3.b.ii", "OFFBiodieselFC"], 4],
            # SVN
            ["Fossil part of biofuel", ["1.A.3.b.ii", "OFFBiofuelFC"], 4],
            # SVK
            ["Fossil part of biofuels", ["1.A.3.b.ii", "OFFBiofuelFC"], 4],
            # NOR
            ["Biodiesel fossil fraction", ["1.A.3.b.ii", "OFFBiodieselFC"], 4],
            # NZL
            ["Biodiesel (fossil fraction)", ["1.A.3.b.ii", "OFFBiodieselFC"], 4],
            # POL
            ["Other fossil fuels", ["1.A.3.b.ii", "OFFOther"], 4],
            # iii. Heavy duty trucks and buses
            ["1.A.3.b.iii. Heavy duty trucks and buses", ["1.A.3.b.iii", "Total"], 2],
            ["Gasoline", ["1.A.3.b.iii", "Gasoline"], 3],
            ["Diesel oil", ["1.A.3.b.iii", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.iii", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.3.b.iii", "OtherLiquid"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.b.iii]",
                ["1.A.3.b.iii", "OLOther"],
                4,
            ],
            # MCO
            ["GTL", ["1.A.3.b.iii", "GTL"], 4],
            # RUS
            ["Other motor fuels", ["1.A.3.b.iii", "OMotorFuel"], 4],
            ["Gaseous fuels (6)", ["1.A.3.b.iii", "Gaseous"], 3],
            ["Biomass (3)", ["1.A.3.b.iii", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.iii", "OtherFF"], 3],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.b.iii]",
                ["1.A.3.b.iii", "OFFOther"],
                4,
            ],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            ["Lubricants", ["1.A.3.b.iii", "OFFLubricants"], 4],
            # AUT
            ["FAME fossil part", ["1.A.3.b.iii", "OFFBiodieselFC"], 4],
            # ESP
            ["Fossil part of biodiesel", ["1.A.3.b.iii", "OFFBiodieselFC"], 4],
            # SVN
            ["Fossil part of biofuel", ["1.A.3.b.iii", "OFFBiofuelFC"], 4],
            # SVK
            ["Fossil part of biofuels", ["1.A.3.b.iii", "OFFBiofuelFC"], 4],
            # NOR
            ["Biodiesel fossil fraction", ["1.A.3.b.iii", "OFFBiodieselFC"], 4],
            # NZL
            ["Biodiesel (fossil fraction)", ["1.A.3.b.iii", "OFFBiodieselFC"], 4],
            # POL
            ["Other fossil fuels", ["1.A.3.b.iii", "OFFOther"], 4],
            # iv. Motorcycles
            ["1.A.3.b.iv. Motorcycles", ["1.A.3.b.iv", "Total"], 2],
            ["Gasoline", ["1.A.3.b.iv", "Gasoline"], 3],
            ["Diesel oil", ["1.A.3.b.iv", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.iv", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.3.b.iv", "OtherLiquid"], 3],
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.b.iv]",
                ["1.A.3.b.iv", "OLOther"],
                4,
            ],
            # ESP
            ["Lubricants (two-stroke engines)", ["1.A.3.b.iv", "Lubricants"], 4],
            # MCO
            ["Lube", ["1.A.3.b.iv", "Lubricants"], 4],
            # MLT, SVN
            ["Lubricants", ["1.A.3.b.iv", "Lubricants"], 4],
            # PRT
            ["Lubricant Oil", ["1.A.3.b.iv", "Lubricants"], 4],
            # RUS
            ["Other motor fuels", ["1.A.3.b.iv", "OMotorFuel"], 4],
            ["Gaseous fuels (6)", ["1.A.3.b.iv", "Gaseous"], 3],
            ["Biomass (3)", ["1.A.3.b.iv", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.iv", "OtherFF"], 3],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.b.iv]",
                ["1.A.3.b.iv", "OFFOther"],
                4,
            ],
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            ["Lubricants", ["1.A.3.b.iv", "OFFLubricants"], 4],
            # AUT
            ["FAME fossil part", ["1.A.3.b.iv", "OFFBiodieselFC"], 4],
            # SVN
            ["Fossil part of biofuel", ["1.A.3.b.iv", "OFFBiofuelFC"], 4],
            # SVK
            ["Fossil part of biofuels", ["1.A.3.b.iv", "OFFBiofuelFC"], 4],
            # v. Other
            ["1.A.3.b.v. Other (please specify)", ["1.A.3.b.v", "Total"], 2],
            # AUS
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            ["Gasoline", ["\\IGNORE", "Gasoline"], 4],
            ["Diesel oil", ["\\IGNORE", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["\\IGNORE", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["\\IGNORE", "OtherLiquid"], 4],
            ["NA", ["\\IGNORE", "\\IGNORE"], 5],
            ["Gaseous fuels (6)", ["\\IGNORE", "Gaseous"], 4],
            ["Biomass (3)", ["\\IGNORE", "Biomass"], 4],
            ["Other fossil fuels (please specify)(7)", ["\\IGNORE", "OtherFF"], 4],
            ["Lubricants", ["\\IGNORE", "OFFLubricants"], 5],
            # GUY, MDV
            ["Not occurring [IPCC Software]", ["\\IGNORE", "\\IGNORE"], 3],
            ["Gasoline", ["\\IGNORE", "Gasoline"], 3],
            ["Diesel oil", ["\\IGNORE", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["\\IGNORE", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["\\IGNORE", "OtherLiquid"], 3],
            ["Not occurring [IPCC Software]", ["\\IGNORE", "\\IGNORE"], 4],
            ["nan", ["\\IGNORE", "\\IGNORE"], 4],
            ["Gaseous fuels (6)", ["\\IGNORE", "Gaseous"], 3],
            ["Biomass (3)", ["\\IGNORE", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["\\IGNORE", "OtherFF"], 3],
            ["Not occurring [IPCC Software]", ["\\IGNORE", "\\IGNORE"], 4],
            ["nan", ["\\IGNORE", "\\IGNORE"], 4],
            # SGP
            ["Others", ["1.A.3.b.v.13", "total"], 3],
            ["Gasoline", ["1.A.3.b.v.13", "Gasoline"], 4],
            ["Diesel oil", ["1.A.3.b.v.13", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.v.13", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.b.v.13", "OtherLiquid"], 4],
            ["NA", ["\\IGNORE", "\\IGNORE"], 5],
            ["Gaseous fuels (6)", ["1.A.3.b.v.13", "Gaseous"], 4],
            ["Biomass (3)", ["1.A.3.b.v.13", "Biomass"], 4],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.v.13", "OtherFF"], 4],
            ["NA", ["\\IGNORE", "\\IGNORE"], 5],
            # ESP
            ["Gasoline evaporation", ["1.A.3.b.v.11", "total"], 3],
            ["Gasoline", ["1.A.3.b.v.11", "Gasoline"], 4],
            ["Diesel oil", ["1.A.3.b.v.11", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.v.11", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.b.v.11", "OtherLiquid"], 4],
            ["nan", ["\\IGNORE", "\\IGNORE"], 5],
            ["Gaseous fuels (6)", ["1.A.3.b.v.11", "Gaseous"], 4],
            ["Biomass (3)", ["1.A.3.b.v.11", "Biomass"], 4],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.v.11", "OtherFF"], 4],
            ["nan", ["\\IGNORE", "\\IGNORE"], 5],
            # SVK
            ["Urea-based catalysts", ["1.A.3.b.v.12", "total"], 3],
            ["Gasoline", ["1.A.3.b.v.12", "Gasoline"], 4],
            ["Diesel oil", ["1.A.3.b.v.12", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.b.v.12", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.b.v.12", "OtherLiquid"], 4],
            ["Gaseous fuels (6)", ["1.A.3.b.v.12", "Gaseous"], 4],
            ["Biomass (3)", ["1.A.3.b.v.12", "Biomass"], 4],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.b.v.12", "OtherFF"], 4],
            # c. Railways
            ["1.A.3.c. Railways", ["1.A.3.c", "Total"], 1],
            ["Liquid fuels", ["1.A.3.c", "Liquid"], 2],
            ["Solid fuels", ["1.A.3.c", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.3.c", "Gaseous"], 2],
            ["Biomass (3)", ["1.A.3.c", "Biomass"], 2],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.c", "OtherFF"], 2],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.c]",
                ["1.A.3.c", "OFFOther"],
                3,
            ],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            ["Lubricants", ["1.A.3.c", "OFFLubricants"], 3],
            # AUT
            ["FAME fossil part", ["1.A.3.c", "OFFBiodieselFC"], 3],
            # d. Domestic navigation
            ["1.A.3.d. Domestic Navigation (12)", ["1.A.3.d", "Total"], 1],
            ["Residual fuel oil", ["1.A.3.d", "ResFuelOil"], 2],
            ["Gas/diesel oil", ["1.A.3.d", "GasDieselOil"], 2],
            ["Gasoline", ["1.A.3.d", "Gasoline"], 2],
            ["Other liquid fuels (please specify)", ["1.A.3.d", "OtherLiquid"], 2],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.3.d.ii]",
                ["1.A.3.d", "OLOther"],
                3,
            ],
            # RUS
            ["Other motor fuels", ["1.A.3.d", "OMotorFuel"], 3],
            ["Gaseous fuels (6)", ["1.A.3.d", "Gaseous"], 2],
            ["Biomass (3)", ["1.A.3.d", "Biomass"], 2],
            ["Other fossil fuels (please specify)(7)", ["1.A.3.d", "OtherFF"], 2],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.3.d.ii]",
                ["1.A.3.d", "OFFOther"],
                3,
            ],
            ["Coal", ["1.A.3.d", "OFFCoal"], 3],
            ["Lubricants", ["1.A.3.d", "OFFLubricants"], 3],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            # AUT
            ["FAME fossil part", ["1.A.3.d", "OFFBiodieselFC"], 3],
            # e. other transportation
            # keep details also for top category as it's present
            ["1.A.3.e. Other transportation", ["1.A.3.e", "Total"], 1],
            ["Liquid fuels", ["1.A.3.e", "Liquid"], 2],
            ["Solid fuels", ["1.A.3.e", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.3.e", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.3.e", "OtherFF"], 2],
            ["Biomass (3)", ["1.A.3.e", "Biomass"], 2],
            # i. pipeline
            ["1.A.3.e.i. Pipeline transport", ["1.A.3.e.i", "Total"], 2],
            ["Liquid fuels", ["1.A.3.e.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.3.e.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.3.e.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.3.e.i", "OtherFF"], 3],
            ["Biomass (3)", ["1.A.3.e.i", "Biomass"], 3],
            # ii other
            ["1.A.3.e.ii. Other (please specify)", ["1.A.3.e.ii", "Total"], 2],
            # AUS
            ["Off-road vehicles", ["1.A.3.e.ii.1", "Total"], 3],
            ["Gasoline", ["1.A.3.e.ii.1", "Gasoline"], 4],
            ["Gas/Diesel oil", ["1.A.3.e.ii.1", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.e.ii.1", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.e.ii.1", "OtherLiquid"], 4],
            ["NA", ["\\IGNORE", "\\IGNORE"], 5],
            ["Solid fuels", ["1.A.3.e.ii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.3.e.ii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.3.e.ii.1", "OtherFF"], 4],
            ["Biomass (3)", ["1.A.3.e.ii.1", "Biomass"], 4],
            # GUY, MDV
            [
                "Other off-road transportation [IPCC Software 1.A.3.e.ii]",
                ["1.A.3.e.ii.1", "Total"],
                3,
            ],
            ["Gasoline", ["1.A.3.e.ii.1", "Gasoline"], 4],
            ["Gas/Diesel oil", ["1.A.3.e.ii.1", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.e.ii.1", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.e.ii.1", "OtherLiquid"], 4],
            [
                "Other liquid fuels [IPCC Software 1.A.3.e.ii]",
                ["1.A.3.e.ii.1", "OLOther"],
                5,
            ],
            ["nan", ["\\IGNORE", "\\IGNORE"], 5],
            ["Solid fuels", ["1.A.3.e.ii.1", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.3.e.ii.1", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.3.e.ii.1", "OtherFF"], 4],
            ["Biomass (3)", ["1.A.3.e.ii.1", "Biomass"], 4],
            # AUT
            ["Airport ground activities", ["1.A.3.e.ii.2", "Total"], 3],
            ["Gasoline", ["1.A.3.e.ii.2", "Gasoline"], 4],
            ["Gas/Diesel oil", ["1.A.3.e.ii.2", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["1.A.3.e.ii.2", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["1.A.3.e.ii.2", "OtherLiquid"], 4],
            ["Solid fuels", ["1.A.3.e.ii.2", "Solid"], 4],
            ["Gaseous fuels (6)", ["1.A.3.e.ii.2", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["1.A.3.e.ii.2", "OtherFF"], 4],
            ["Biomass (3)", ["1.A.3.e.ii.2", "Biomass"], 4],
            # SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 3],
            ["Gasoline", ["\\IGNORE", "Gasoline"], 4],
            ["Gas/Diesel oil", ["\\IGNORE", "DieselOil"], 4],
            ["Liquefied petroleum gases (LPG)", ["\\IGNORE", "LPG"], 4],
            ["Other liquid fuels (please specify)", ["\\IGNORE", "OtherLiquid"], 4],
            ["NA", ["\\IGNORE", "\\IGNORE"], 5],
            ["Solid fuels", ["\\IGNORE", "Solid"], 4],
            ["Gaseous fuels (6)", ["\\IGNORE", "Gaseous"], 4],
            ["Other fossil fuels (7)", ["\\IGNORE", "OtherFF"], 4],
            ["Biomass (3)", ["\\IGNORE", "Biomass"], 4],
        ],
        "entity_mapping": {
            "EMISSIONS CH4": "CH4",
            "EMISSIONS CO2 (2,3)": "CO2",
            "EMISSIONS N2O": "N2O",
        },
    },  # tested
    "Table1.A(a)s4": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 128,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [
                "AGGREGATE ACTIVITY DATA Consumption",
                "AGGREGATE ACTIVITY DATA Consumption",
                "IMPLIED EMISSION FACTORS CO2 (1)",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
                "AMOUNT CAPTURED (4) CO2",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) The IEFs for CO2 are estimated on the basis of gross "
                "emissions, i.e. CO2 emissions plus the absolute amount "
                "captured.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.A.4 Other sectors", ["1.A.4", "Total"], 0],
            ["Liquid fuels", ["1.A.4", "Liquid"], 1],
            ["Solid fuels", ["1.A.4", "Solid"], 1],
            ["Gaseous fuels (6)", ["1.A.4", "Gaseous"], 1],
            ["Other fossil fuels (7)", ["1.A.4", "OtherFF"], 1],
            ["Peat (8)", ["1.A.4", "Peat"], 1],
            ["Biomass(3)", ["1.A.4", "Biomass"], 1],
            # a. Commercial/institutional(12)
            ["1.A.4.a. Commercial/institutional (14)", ["1.A.4.a", "Total"], 1],
            ["Liquid fuels", ["1.A.4.a", "Liquid"], 2],
            ["Solid fuels", ["1.A.4.a", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.4.a", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.4.a", "OtherFF"], 2],
            ["Peat (8)", ["1.A.4.a", "Peat"], 2],
            ["Biomass (3)", ["1.A.4.a", "Biomass"], 2],
            ["Drop-down list:", ["\\IGNORE", "\\IGNORE"], 2],  # (empty)
            # 1.A.4.a.i Stationary combustion
            ["1.A.4.a.i. Stationary combustion", ["1.A.4.a.i", "Total"], 2],
            ["Liquid fuels", ["1.A.4.a.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.4.a.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.4.a.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.4.a.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.4.a.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.4.a.i", "Biomass"], 3],
            # 1.A.4.a.ii Off-road vehicles and other machinery
            [
                "1.A.4.a.ii. Off-road vehicles and other machinery",
                ["1.A.4.a.ii", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.4.a.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.4.a.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.4.a.ii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.4.a.ii", "OtherFF"], 3],
            ["Biomass (3)", ["1.A.4.a.ii", "Biomass"], 3],
            # b. Residential(13)
            ["1.A.4.b. Residential (14)", ["1.A.4.b", "Total"], 1],
            ["Liquid fuels", ["1.A.4.b", "Liquid"], 2],
            ["Solid fuels", ["1.A.4.b", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.4.b", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.4.b", "OtherFF"], 2],
            ["Peat (8)", ["1.A.4.b", "Peat"], 2],
            ["Biomass (3)", ["1.A.4.b", "Biomass"], 2],
            ["Drop-down list:", ["\\IGNORE", "\\IGNORE"], 2],  # (empty)
            # 1.A.4.b.i Stationary combustion
            ["1.A.4.b.i. Stationary combustion", ["1.A.4.b.i", "Total"], 2],
            ["Liquid fuels", ["1.A.4.b.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.4.b.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.4.b.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.4.b.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.4.b.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.4.b.i", "Biomass"], 3],
            # 1.A.4.b.ii Off-road vehicles and other machinery
            [
                "1.A.4.b.ii. Off-road vehicles and other machinery",
                ["1.A.4.b.ii", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.4.b.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.4.b.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.4.b.ii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.4.b.ii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.4.b.ii", "Peat"], 3],
            ["Biomass (3)", ["1.A.4.b.ii", "Biomass"], 3],
            # c. Agriculture/forestry/fishing
            ["1.A.4.c. Agriculture/forestry/fishing", ["1.A.4.c", "Total"], 1],
            ["Liquid fuels", ["1.A.4.c", "Liquid"], 2],
            ["Solid fuels", ["1.A.4.c", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.4.c", "Gaseous"], 2],
            ["Other fossil fuels (7)", ["1.A.4.c", "OtherFF"], 2],
            ["Peat (8)", ["1.A.4.c", "Peat"], 2],
            ["Biomass (3)", ["1.A.4.c", "Biomass"], 2],
            # i. Stationary
            ["1.A.4.c.i. Stationary", ["1.A.4.c.i", "Total"], 2],
            ["Liquid fuels", ["1.A.4.c.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.4.c.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.4.c.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.4.c.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.4.c.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.4.c.i", "Biomass"], 3],
            # ii. Off-road vehicles and other machinery
            [
                "1.A.4.c.ii. Off-road vehicles and other machinery",
                ["1.A.4.c.ii", "Total"],
                2,
            ],
            ["Gasoline", ["1.A.4.c.ii", "Gasoline"], 3],
            ["Diesel oil", ["1.A.4.c.ii", "DieselOil"], 3],
            ["Liquefied petroleum gases (LPG)", ["1.A.4.c.ii", "LPG"], 3],
            ["Other liquid fuels (please specify)", ["1.A.4.c.ii", "OtherLiquid"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.4.c.ii]",
                ["1.A.4.c.ii", "OLOther"],
                4,
            ],
            # RUS
            ["Other motor fuels", ["1.A.4.c.ii", "OMotorFuel"], 4],
            # NOR
            ["Heavy fuel oil", ["1.A.4.c.ii", "HeavyFuelOil"], 4],
            ["Marine gasoil", ["1.A.4.c.ii", "MarineGasoil"], 4],
            ["Gaseous fuels (6)", ["1.A.4.c.ii", "Gaseous"], 3],
            ["Biomass (3)", ["1.A.4.c.ii", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.4.c.ii", "OtherFF"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.4.c.ii]",
                ["1.A.4.c.ii", "OFFOther"],
                4,
            ],
            # AUT
            ["FAME fossil part", ["1.A.4.c.ii", "OFFBiodieselFC"], 4],
            # iii. Fishing
            ["1.A.4.c.iii. Fishing", ["1.A.4.c.iii", "Total"], 2],
            ["Residual fuel oil", ["1.A.4.c.iii", "ResFuelOil"], 3],
            ["Gas/diesel oil", ["1.A.4.c.iii", "GasDieselOil"], 3],
            ["Gasoline", ["1.A.4.c.iii", "Gasoline"], 3],
            ["Other liquid fuels (please specify)", ["1.A.4.c.iii", "OtherLiquid"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other liquid fuels [IPCC Software 1.A.4.c.iii]",
                ["1.A.4.c.iii", "OLOther"],
                4,
            ],
            # RUS
            ["Other motor fuels", ["1.A.4.c.iii", "OMotorFuel"], 4],
            ["Gaseous fuels (6)", ["1.A.4.c.iii", "Gaseous"], 3],
            ["Biomass(3)", ["1.A.4.c.iii", "Biomass"], 3],
            ["Other fossil fuels (please specify)(7)", ["1.A.4.c.iii", "OtherFF"], 3],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 4],
            # GUY, MDV
            [
                "Other fossil fuels [IPCC Software 1.A.4.c.iii]",
                ["1.A.4.c.iii", "OFFOther"],
                4,
            ],
            # 1.A.5 Other (Not specified elsewhere)(14)
            ["1.A.5 Other (Not specified elsewhere)(15)", ["1.A.5", "Total"], 0],
            ["Liquid fuels", ["1.A.5", "Liquid"], 1],
            ["Solid fuels", ["1.A.5", "Solid"], 1],
            ["Gaseous fuels (6)", ["1.A.5", "Gaseous"], 1],
            ["Other fossil fuels(7)", ["1.A.5", "OtherFF"], 1],
            ["Peat (8)", ["1.A.5", "Peat"], 1],
            ["Biomass (3)", ["1.A.5", "Biomass"], 1],
            # a. Stationary (please specify)
            ["1.A.5.a. Stationary (please specify)", ["1.A.5.a", "Total"], 1],
            # AUS, SGP
            ["NA", ["\\IGNORE", "\\IGNORE"], 2],
            ["Liquid fuels", ["1.A.5.a", "Liquid"], 2],
            ["Solid fuels", ["1.A.5.a", "Solid"], 2],
            ["Gaseous fuels (6)", ["1.A.5.a", "Gaseous"], 2],
            ["Other fossil fuels(7)", ["1.A.5.a", "OtherFF"], 2],
            ["Peat (8)", ["1.A.5.a", "Peat"], 2],
            ["Biomass (3)", ["1.A.5.a", "Biomass"], 2],
            # GUY, MDV
            ["Stationary [IPCC Software 1.A.5.a]", ["1.A.5.a.ii", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.ii", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.ii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.ii", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.ii", "Biomass"], 3],
            # SGP
            ["Military activities", ["1.A.5.a.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.i", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.i", "Biomass"], 3],
            # NOR
            ["Military", ["1.A.5.a.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.i", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.i", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.i", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.i", "Biomass"], 3],
            ["Non-fuel use", ["1.A.5.a.iii", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.iii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.iii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.iii", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.iii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.iii", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.iii", "Biomass"], 3],
            # ESP
            ["Other non-specified", ["1.A.5.a.ii", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.ii", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.ii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.ii", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.ii", "Biomass"], 3],
            # RUS, SVK
            ["Other", ["1.A.5.a.ii", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.ii", "Gaseous"], 3],
            ["Other fossil fuels(7)", ["1.A.5.a.ii", "OtherFF"], 3],
            ["Peat (8)", ["1.A.5.a.ii", "Peat"], 3],
            ["Biomass (3)", ["1.A.5.a.ii", "Biomass"], 3],
            # b. Mobile (please specify)
            ["1.A.5.b. Mobile (please specify)", ["1.A.5.b", "Total"], 1],
            # AUS
            ["Military Transport", ["1.A.5.b.xii", "Total"], 2],
            ["Liquid fuels", ["1.A.5.b.xii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.xii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.xii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.xii", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.xii", "Biomass"], 3],
            # GUY, MDV
            [
                "Other mobile (aviation) [IPCC Software 1.A.3.a.ii, 1.A.5.b.i]",
                ["1.A.5.b.vi", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.5.b.vi", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.vi", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.vi", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.vi", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.vi", "Biomass"], 3],
            [
                "Other mobile (water-borne) [IPCC Software 1.A.5.b.ii]",
                ["1.A.5.b.xiv", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.5.b.xiv", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.xiv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.xiv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.xiv", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.xiv", "Biomass"], 3],
            [
                "Other mobile (other) [IPCC Software 1.A.3.b, 1.A.4.c, 1.A.5.b.iii]",
                ["1.A.5.b.iv", "Total"],
                2,
            ],
            ["Liquid fuels", ["1.A.5.b.iv", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.iv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.iv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.iv", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.iv", "Biomass"], 3],
            # SGP
            ["Military activities", ["1.A.5.b.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.i", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.i", "Biomass"], 3],
            # AUT, NOR
            ["Military", ["1.A.5.b.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.i", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.i", "Biomass"], 3],
            # NLD
            ["Military use", ["1.A.5.b.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.i", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.i", "Biomass"], 3],
            # SVN
            ["Military use of fuel", ["1.A.5.b.i", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.i", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.i", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.i", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.i", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.i", "Biomass"], 3],
            # NOR
            ["Lubricants used in 2-stroke engines", ["1.A.5.b.vii", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.vii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.vii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.vii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.vii", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.vii", "Biomass"], 3],
            # ESP
            ["Other non-specified", ["1.A.5.a.iv", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.iv", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.iv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.iv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.a.iv", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.a.iv", "Biomass"], 3],
            # MLT
            ["Other", ["1.A.5.a.iv", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.iv", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.iv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.iv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.a.iv", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.a.iv", "Biomass"], 3],
            # RUS
            ["Other transportation", ["1.A.5.a.xv", "total"], 2],
            ["Liquid fuels", ["1.A.5.a.xv", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.a.xv", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.a.xv", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.a.xv", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.a.xv", "Biomass"], 3],
            # SVK
            ["Military use Jet Kerosene", ["1.A.5.b.ix", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.ix", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.ix", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.ix", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.ix", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.ix", "Biomass"], 3],
            ["Military Gasoline", ["1.A.5.b.x", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.x", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.x", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.x", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.x", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.x", "Biomass"], 3],
            ["Military Diesel Oil", ["1.A.5.b.xi", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.xi", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.xi", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.xi", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.xi", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.xi", "Biomass"], 3],
            # PRT
            ["Military aviation", ["1.A.5.b.ii", "total"], 2],
            ["Liquid fuels", ["1.A.5.b.ii", "Liquid"], 3],
            ["Solid fuels", ["1.A.5.b.ii", "Solid"], 3],
            ["Gaseous fuels (6)", ["1.A.5.b.ii", "Gaseous"], 3],
            ["Other fossil fuels (7)", ["1.A.5.b.ii", "OtherFF"], 3],
            ["Biomass(3)", ["1.A.5.b.ii", "Biomass"], 3],
            # Information Item
            ["Information item: (16)", ["\\IGNORE", "\\IGNORE"], 0],
            [
                "Waste incineration with energy recovery included as:",
                ["\\IGNORE", "\\IGNORE"],
                1,
            ],
            ["Biomass (3)", ["\\IGNORE", "\\IGNORE"], 1],
            ["Fossil fuels (7)", ["\\IGNORE", "\\IGNORE"], 1],
            # PRT, SVK
            ["Biomass(3)", ["\\IGNORE", "\\IGNORE"], 1],
            ["Other fossil fuels (7)", ["\\IGNORE", "\\IGNORE"], 1],
        ],
        "entity_mapping": {
            "EMISSIONS CH4": "CH4",
            "EMISSIONS CO2 (2,3)": "CO2",
            "EMISSIONS N2O": "N2O",
        },
    },  # tested
    "Table1.B.1": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 34,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA Amount of fuel produced",
                "IMPLIED EMISSION FACTORS CH4 (3)",
                "IMPLIED EMISSION FACTORS CO2",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) Final CH4 and CO2 emissions after subtracting the amounts of CH4 "
                "and CO2 utilized or recovered.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1. B. 1. a. Coal mining and handling", ["1.B.1.a"], 0],
            ["1.B.1.a.i. Underground mines (4)", ["1.B.1.a.i"], 1],
            ["1.B.1.a.i.1. Mining activities", ["1.B.1.a.i.1"], 2],
            ["1.B.1.a.i.2. Post-mining activities", ["1.B.1.a.i.2"], 2],
            [
                "1.B.1.a.i.3. Abandoned underground mines (number of mines)",
                ["1.B.1.a.i.3"],
                2,
            ],
            [
                "1.B.1.a.i.4. Flaring of drained methane or conversion of "
                "methane to CO2 (5)",
                ["1.B.1.a.i.4"],
                2,
            ],
            ["1.B.1.a.i.5. Other (please specify)", ["1.B.1.a.i.5"], 2],
            # AUS, SGP
            ["NA", ["\\IGNORE"], 3],
            # GUY, MDV
            [
                "Other Underground Coal Mines [IPCC Software 1.B.3]",
                ["1.B.1.a.i.5.a"],
                3,
            ],
            ["1.B.1.a.ii. Surface mines (4)", ["1.B.1.a.ii"], 1],
            ["1.B.1.a.ii.1. Mining activities", ["1.B.1.a.ii.1"], 2],
            ["1.B.1.a.ii.2. Post-mining activities", ["1.B.1.a.ii.2"], 2],
            ["1.B.1.a.ii.3. Other (please specify)", ["1.B.1.a.ii.3"], 2],
            # AUS, SGP
            ["NA", ["\\IGNORE"], 3],
            # GUY, MDV
            ["Other Surface Coal Mines [IPCC Software 1.B.3]", ["1.B.1.a.ii.3.a"], 3],
            ["Abandoned surface mines [IPCC Software 1.B.3]", ["1.B.1.a.ii.3.b"], 3],
            ["1. B. 1. b. Fuel transformation (6)", ["1.B.1.b"], 0],
            # AUS
            ["Drop down list:", ["\\IGNORE"], 1],
            # AUS, GUY, MDV
            ["1.B.1.b.i. Charcoal and biochar production (7)", ["1.B.1.b.i"], 1],
            ["1.B.1.b.ii. Coke production", ["1.B.1.b.ii"], 1],
            ["1.B.1.b.iii. Coal to liquids", ["1.B.1.b.iii"], 1],
            ["1.B.1.b.iv. Gas to liquids", ["1.B.1.b.iv"], 1],
            ["1.B.1.b.v. Other (please specify)", ["1.B.1.b.v"], 1],
            # AUS
            ["NA", ["\\IGNORE"], 2],
            # GUY, MDV
            [
                "GHG emissions from other gasification [IPCC Software 1.B.1.c.iv]",
                ["1.B.1.b.v.i"],
                2,
            ],
            ["Other fuel transformation [IPCC Software 1.B.3]", ["1.B.1.b.v.ii"], 2],
            # SGP
            ["Gasification transformation", ["1.B.1.b.v.i"], 1],
            # NOR
            ["Solid Fuel transformation", ["1.B.1.b.v.iii"], 1],
            ["1. B. 1. c. Other (please specify) (8)", ["1.B.1.c"], 0],
            # AUS, SGP
            ["NA", ["\\IGNORE"], 1],
            # GUY, MDV
            [
                "Uncontrolled combustion and burning of coal dumps "
                "[IPCC Software 1.B.1.b]",
                ["1.B.1.c.ii"],
                1,
            ],
            ["Other solid fuels [IPCC Software 1.B.3]", ["1.B.1.c.v"], 1],
            # JPN
            ["Uncontrolled combustion", ["1.B.1.c.ii"], 1],
            # POL
            ["Emisson from coke oven gas subsystem", ["1.B.1.c.iv"], 1],
            # SVN
            ["SO2 scrubbing", ["1.B.1.c.iii"], 1],
            # SVK
            ["CO2 emissions from Charcoal and biochar", ["1.B.1.c.vi"], 1],
        ],
        "entity_mapping": {
            "EMISSIONS (1) CH4": "CH4 emissions",  # this is necessary because there
            # is an error in the table and the CH4 emissions don't have the removals
            # subtracted which would be correct according to the footnotes
            # TODO: check!!!
            "EMISSIONS (1) CO2": "CO2",  #  emissions",
            "RECOVERY/FLARING (2) CH4": "CH4 removals",
            "RECOVERY/FLARING (2) CO2": "CO2 removals",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.B.2": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 45,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA (1) Description (1)",
                "ACTIVITY DATA (1) Unit (1)",
                "ACTIVITY DATA (1) Value",
                "IMPLIED EMISSION FACTORS CO2 (3)",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
            ],
            "stop_cats": [
                ".",
                "nan",
                "(1) Specify the AD used. Specify the unit of the AD in energy or "
                "volume units (e.g. PJ, 106 m3 and 106 bbl/year).",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.B.2.a. Oil (7)", ["1.B.2.a"], 0],
            ["1.B.2.a.i. Exploration", ["1.B.2.a.i"], 1],
            ["1.B.2.a.ii. Production and upgrading (8)", ["1.B.2.a.ii"], 1],
            ["1.B.2.a.iii. Transport", ["1.B.2.a.iii"], 1],
            ["1.B.2.a.iv. Refining/storage", ["1.B.2.a.iv"], 1],
            ["1.B.2.a.v. Distribution of oil products", ["1.B.2.a.v"], 1],
            ["1.B.2.a.vi. Other", ["1.B.2.a.vi"], 1],
            # AUS
            ["Drop down list:", ["\\IGNORE"], 2],
            # AUS, GUY, MDV
            ["1.B.2.a.vi.1. Abandoned wells", ["1.B.2.a.vi.1"], 2],
            ["1.B.2.a.vi.2. Other (please specify)", ["1.B.2.a.vi.2"], 2],
            # AUS, SGP
            ["NA", ["\\IGNORE"], 3],
            # GUY, MDV
            [
                "Other fugitive from oil industry [IPCC Software 1.B.2.a.iii.6]",
                ["1.B.2.a.vi.2.a"],
                3,
            ],
            # JPN
            ["Accidents", ["1.B.2.a.vi.2.b"], 3],
            # RUS
            ["Gas condensate transported", ["1.B.2.a.vi.2.c"], 3],
            ["1.B.2.b. Natural gas", ["1.B.2.b"], 0],
            ["1.B.2.b.i. Exploration", ["1.B.2.b.i"], 1],
            ["1.B.2.b.ii. Production and gathering (8)", ["1.B.2.b.ii"], 1],
            ["1.B.2.b.iii. Processing", ["1.B.2.b.iii"], 1],
            ["1.B.2.b.iv. Transmission and storage", ["1.B.2.b.iv"], 1],
            ["1.B.2.b.v. Distribution", ["1.B.2.b.v"], 1],
            ["1.B.2.b.vi. Other", ["1.B.2.b.vi"], 1],
            # AUS
            ["Drop down list:", ["\\IGNORE"], 2],
            # AUS (no other), GUY, MDV, SGP, JPN (no other), NOR (othe ronly)
            ["1.B.2.b.vi.1. Gas post-meter", ["1.B.2.b.vi.1"], 2],
            ["1.B.2.b.vi.2. Abandoned wells", ["1.B.2.b.vi.2"], 2],
            ["1.B.2.b.vi.3. Other (please specify)", ["1.B.2.b.vi.3"], 2],
            # # AUS
            # ["LNG Terminals", ["1.B.2.b.vi.3.a"], 3],
            # ["LNG Storage", ["1.B.2.b.vi.3.b"], 3],
            # ["Natural Gas Storage", ["1.B.2.b.vi.3.c"], 3],
            # GUY, MDV
            [
                "Other fugitive from natural gas industry [IPCC Software 1.B.2.b.iii.6]",
                ["1.B.2.b.vi.3.d"],
                3,
            ],
            # SGP
            ["NA", ["\\IGNORE"], 3],
            # NOR
            ["Other", ["1.B.2.b.vi.3.d"], 3],
            # SVK
            ["Storage of gas", ["1.B.2.b.vi.3.e"], 3],
            ["1.B.2.c. Venting and flaring", ["1.B.2.c"], 0],
            ["1.B.2.c.i. Venting", ["1.B.2.c-ven"], 1],
            ["1.B.2.c.i.1. Oil", ["1.B.2.c-ven.i"], 2],
            ["1.B.2.c.i.2. Gas", ["1.B.2.c-ven.ii"], 2],
            ["1.B.2.c.i.3. Combined", ["1.B.2.c-ven.iii"], 2],
            ["1.B.2.c.ii. Flaring (9)", ["1.B.2.c-fla"], 1],
            ["1.B.2.c.ii.1. Oil", ["1.B.2.c-fla.i"], 2],
            ["1.B.2.c.ii.2. Gas", ["1.B.2.c-fla.ii"], 2],
            ["1.B.2.c.ii.3. Combined", ["1.B.2.c-fla.iii"], 2],
            ["1.B.2.d. Other (please specify) (10)", ["1.B.2.d"], 0],
            # AUS, SGP
            ["NA", ["\\IGNORE"], 1],
            # GUY, MDV
            [
                "N2O emissions from Oil and Natural Gas Systems [IPCC Software 1.B.2]",
                ["1.B.2.d.xii"],
                1,
            ],
            [
                "N2O emissions from other Energy Production [IPCC Software 1.B.3]",
                ["1.B.2.d.xiii"],
                1,
            ],
            ["Geotherm", ["1.B.2.d.ii"], 1],  # ITA
            ["Geothermal generation", ["1.B.2.d.ii"], 1],  # JPN
            ["Geothermal", ["1.B.2.d.ii"], 1],  # (DEU, PRT,) NZL
            ["Flaring in refineries", ["1.B.2.d.v"], 1],  # ITA
            # RUS (also included in 1.B.2.a.vi.2, double counting)
            ["Gas condensate transported", ["1.B.2.d.xii"], 1],
        ],
        "entity_mapping": {
            "EMISSIONS CH4 (5)": "CH4",
            "EMISSIONS CO2 (4)": "CO2",  # "CO2 emissions",
            "EMISSIONS N2O": "N2O",
            "RECOVERY (2) CO2": "CO2 removals",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.C": {
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 29,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA CO2 transported or injected (1)",
                "IMPLIED EMISSION FACTORS CO2",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) Excluding recycled CO2 for enhanced recovery.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["1.C.1. Transport of CO2", ["1.C.1"], 0],
            ["1.C.1.a. Pipelines", ["1.C.1.a"], 1],
            ["1.C.1.b. Ships", ["1.C.1.b"], 1],
            ["1.C.1.c. Other (please specify)", ["1.C.1.c"], 1],
            # AUS
            ["NA", ["\\IGNORE"], 2],
            # GUY, MDV
            ["Other [IPCC Software 1.C.1.c]", ["1.C.1.c.i"], 2],
            # ESP
            ["Other", ["1.C.1.c.i"], 2],
            ["1.C.2. Injection and storage (3)", ["1.C.2"], 0],
            ["1.C.2.a. Injection", ["1.C.2.a"], 1],
            ["1.C.2.b. Storage", ["1.C.2.b"], 1],
            ["1.C.3. Other (please specify)", ["1.C.3"], 0],
            # AUS
            ["NA", ["\\IGNORE"], 1],
            # GUY, MDV
            ["Other [IPCC Software 1.C.3]", ["1.C.3.i"], 1],
            # ESP
            ["Other", ["1.C.3.i"], 1],
            ["Information item (kt CO2) (4, 5, 6)", ["\\IGNORE"], 0],
            ["Total amount captured for storage (7)", ["M.Info.A.TACS"], 1],
            ["Total amount of imports for storage (7)", ["M.Info.A.TAIS"], 1],
            ["Total A", ["M.Info.A"], 1],
            ["Total amount of exports for storage", ["M.Info.B.TAES"], 1],
            ["Total amount of CO2 injected at storage sites", ["M.Info.B.TAI"], 1],
            ["CO2 injected for operational usage (8)", ["M.Info.B.IOU"], 1],
            [
                "Total leakage from transport, injection and storage",
                ["M.Info.B.TLTIS"],
                1,
            ],
            ["Total B", ["M.Info.B"], 1],
            ["Difference (A-B)(6)", ["\\IGNORE"], 1],
        ],
        "entity_mapping": {
            "EMISSIONS CO2 (2)": "CO2",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table1.D": {
        "status": "TODO",
        "table": {
            "firstrow": 7,
            "lastrow": 24,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category", "class"],
            "cols_to_ignore": [],
            "stop_cats": ["", "nan"],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table2(I)": {
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 66,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [
                "",
                "nan",
                "(1) Emissions of HFCs, PFCs, unspecified mix of HFCs and PFCs, and "
                "other F-gases are to be expressed in CO2 eq. Data on disaggregated "
                "emissions of HFCs and PFCs are to be provided in table 2(II).",
            ],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ["2. Total industrial processes", ["2"], 0],
            ["2.A. Mineral industry", ["2.A"], 1],
            ["2.A.1. Cement production", ["2.A.1"], 2],
            ["2.A.2. Lime production", ["2.A.2"], 2],
            ["2.A.3. Glass production", ["2.A.3"], 2],
            ["2.A.4. Other process uses of carbonates", ["2.A.4"], 2],
            ["2.B. Chemical industry", ["2.B"], 1],
            ["2.B.1. Ammonia production", ["2.B.1"], 2],
            ["2.B.2. Nitric acid production", ["2.B.2"], 2],
            ["2.B.3. Adipic acid production", ["2.B.3"], 2],
            ["2.B.4. Caprolactam, glyoxal and glyoxylic acid production", ["2.B.4"], 2],
            ["2.B.5. Carbide production", ["2.B.5"], 2],
            ["2.B.6. Titanium dioxide production", ["2.B.6"], 2],
            ["2.B.7. Soda ash production", ["2.B.7"], 2],
            ["2.B.8. Petrochemical and carbon black production", ["2.B.8"], 2],
            ["2.B.9. Fluorochemical production", ["2.B.9"], 2],
            ["2.B.10. Other", ["2.B.10"], 2],
            ["2.C. Metal industry", ["2.C"], 1],
            ["2.C.1. Iron and steel production", ["2.C.1"], 2],
            ["2.C.2. Ferroalloys production", ["2.C.2"], 2],
            ["2.C.3. Aluminium production", ["2.C.3"], 2],
            ["2.C.4. Magnesium production", ["2.C.4"], 2],
            ["2.C.5. Lead production", ["2.C.5"], 2],
            ["2.C.6. Zinc production", ["2.C.6"], 2],
            ["2.C.7. Other", ["2.C.7"], 2],
            ["2.D. Non-energy products from fuels and solvent use (4)", ["2.D"], 1],
            ["2.D.1. Lubricant use", ["2.D.1"], 2],
            ["2.D.2. Paraffin wax use", ["2.D.2"], 2],
            ["2.D.3. Other", ["2.D.3"], 2],
            ["2.E. Electronics industry", ["2.E"], 1],
            ["2.E.1. Integrated circuit or semiconductor", ["2.E.1"], 2],
            ["2.E.2. TFT flat panel display", ["2.E.2"], 2],
            ["2.E.3. Photovoltaics", ["2.E.3"], 2],
            ["2.E.4. Heat transfer fluid", ["2.E.4"], 2],
            ["2.E.5. Other", ["2.E.5"], 2],
            ["2.F. Product uses as substitutes for ODS", ["2.F"], 1],
            ["2.F.1. Refrigeration and air conditioning", ["2.F.1"], 2],
            ["2.F.2. Foam blowing agents", ["2.F.2"], 2],
            ["2.F.3. Fire protection", ["2.F.3"], 2],
            ["2.F.4. Aerosols", ["2.F.4"], 2],
            ["2.F.5. Solvents", ["2.F.5"], 2],
            ["2.F.6. Other applications", ["2.F.6"], 2],
            ["2.G. Other product manufacture and use", ["2.G"], 1],
            ["2.G.1. Electrical equipment", ["2.G.1"], 2],
            ["2.G.2. SF6 and PFCs from other product use", ["2.G.2"], 2],
            ["2.G.3. N2O from product uses", ["2.G.3"], 2],
            ["2.G.4. Other", ["2.G.4"], 2],
            # most countries
            ["2.H. Other (5)", ["2.H"], 1],
            ["2.H.1. Pulp and paper", ["2.H.1"], 2],
            ["2.H.2. Food and beverages industry", ["2.H.2"], 2],
            ["2.H.3. Other (please specify)", ["2.H.3"], 2],
            # GUY, MDV
            [
                "Other industrial processes and product use [IPCC Software]",
                ["2.H.3.a"],
                3,
            ],
            # SGP
            ["Other processes", ["2.H.3.a"], 3],
            # ESP
            ["Soda ash production (CO emissions)", ["2.H.3.d"], 3],
            ["Glass production (NMVOC emissions)", ["2.H.3.e"], 3],
            ["Tobacco", ["2.H.3.b"], 3],
            ["Fireworks", ["2.H.3.c"], 3],
            ["Titanium dioxide production (NOX and SO2 emissions)", ["2.H.3.f"], 3],
            ["Flaring in iron and steel producion (N2O emissions)", ["2.H.3.g"], 3],
            # JPN
            ["Emissions from Imported Carbonated Gas", ["2.H.3.h"], 3],
            ["Utilization of Carbonated Gas", ["2.H.3.i"], 3],
            # NZL
            ["Fibreboard production", ["2.H.3.j"], 3],
            ["Particleboard Production", ["2.H.3.k"], 3],
            # NOR
            ["Ore mines", ["2.H.3.l"], 3],
            # PRT
            ["Carbon electrodes consumption", ["2.H.3.l"], 3],
            ["Chipboard production", ["2.H.3.k"], 3],
            # CHE
            ["Blasting and shooting", ["2.H.3.m"], 3],
            # AUS
            ["2.H. Other (please specify) (5)", ["2.H"], 1],
            ["2.H.2. Food and Beverages Industry", ["2.H.2"], 2],
        ],
        "entity_mapping": {
            "HFCs (1)": f"HFCS ({gwp_to_use})",
            "PFCs (1)": f"PFCS ({gwp_to_use})",
            "Unspecified mix of HFCs and PFCs (1)": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
            "Total GHG emissions (2)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table2(II)": {
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 37,  # ignore the totals
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [".", "nan", "", "Total emissions (3)"],
            "unit_info": unit_info["fgases"],
        },
        "sector_mapping": [
            [
                "2. Total actual emissions of halocarbons (by chemical), SF6 and NF3",
                ["2"],
            ],
            ["2.B. Chemical industry", ["2.B"]],
            ["2.B.9. Fluorochemical production", ["2.B.9"]],
            ["2.B.9.a. By-product emissions", ["2.B.9.a"]],
            ["2.B.9.b. Fugitive emissions", ["2.B.9.b"]],
            ["2.B.10. Other", ["2.B.10"]],
            ["2.C. Metal industry", ["2.C"]],
            ["2.C.3. Aluminium production", ["2.C.3"]],
            ["2.C.4. Magnesium production", ["2.C.4"]],
            ["2.C.7. Other", ["2.C.7"]],
            ["2.E. Electronics industry", ["2.E"]],
            ["2.E.1. Integrated circuit or semiconductor", ["2.E.1"]],
            ["2.E.2. TFT flat panel display", ["2.E.2"]],
            ["2.E.3. Photovoltaics", ["2.E.3"]],
            ["2.E.4. Heat transfer fluid", ["2.E.4"]],
            ["2.E.5. Other", ["2.E.5"]],
            ["2.F. Product uses as substitutes for ODS", ["2.F"]],
            ["2.F.1. Refrigeration and air conditioning", ["2.F.1"]],
            ["2.F.2. Foam blowing agents", ["2.F.2"]],
            ["2.F.3. Fire protection", ["2.F.3"]],
            ["2.F.4. Aerosols", ["2.F.4"]],
            ["2.F.5. Solvents", ["2.F.5"]],
            ["2.F.6. Other applications", ["2.F.6"]],
            ["2.G. Other product manufacture and use", ["2.G"]],
            ["2.G.1. Electrical equipment", ["2.G.1"]],
            ["2.G.2. SF6 and PFCs from other product use", ["2.G.2"]],
            ["2.G.4. Other", ["2.G.4"]],
            ["2.H. Other", ["2.H"]],
            ["2.H.1 Pulp and paper", ["2.H.1"]],
            ["2.H.2 Food and beverages industry", ["2.H.2"]],
            ["2.H.3 Other (please specify)", ["2.H.3"]],
        ],
        "entity_mapping": {
            #'C3F8': 'C3F8',
            #'C10F18' 'C2F6' 'C4F10' 'C5F12' 'C6F14' 'CF4'
            "HFC-125": "HFC125",
            "HFC-134": "HFC134",
            "HFC-134a": "HFC134a",
            "HFC-143": "HFC143",
            "HFC-143a": "HFC143a",
            "HFC-152": "HFC152",
            "HFC-152a": "HFC152a",
            "HFC-161": "HFC161",
            "HFC-227ea": "HFC227ea",
            "HFC-23": "HFC23",
            "HFC-236cb": "HFC236cb",
            "HFC-236ea": "HFC236ea",
            "HFC-236fa": "HFC236fa",
            "HFC-245ca": "HFC245ca",
            "HFC-245fa": "HFC245fa",
            "HFC-32": "HFC32",
            "HFC-365mfc": "HFC365mfc",
            "HFC-41": "HFC41",
            "HFC-43-10mee": "HFC4310mee",
            "Unspecified mix of HFCs (1)": f"UnspMixOfHFCs ({gwp_to_use})",
            "Unspecified mix of HFCs and PFCs(1)": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
            "Unspecified mix of PFCs (1)": f"UnspMixOfPFCs ({gwp_to_use})",
            "c-C3F6": "cC3F6",
            "c-C4F8": "cC4F8",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3": {  # Agriculture summary
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 48,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [
                "",
                "nan",
                '(1) "Total GHG emissions" does not include NOX, CO, NMVOC and SOX.',
            ],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ["3. Total agriculture", ["3"], 0],
            # A. Enteric fermentation
            ["3.A. Enteric fermentation", ["3.A"], 1],
            ["3.A.1. Cattle(3)", ["3.A.1"], 2],
            ["Option A:", ["\\IGNORE"], 3],
            ["\\C-AUS\\ 3.A.1.a. Dairy cattle", ["\\IGNORE"], 4],
            ["\\C-AUS\\ 3.A.1.b. Non-dairy cattle", ["\\IGNRE"], 4],
            ["\\C!-AUS\\ 3.A.1.a. Dairy cattle", ["3.A.1.A.a"], 4],
            ["\\C!-AUS\\ 3.A.1.b. Non-dairy cattle", ["3.A.1.A.b"], 4],
            ["Option B (country-specific):", ["\\IGNORE"], 3],
            ["3.A.1.a. Other", ["3.A.1.B"], 4],
            ["3.A.1.a.i. Mature dairy cattle", ["3.A.1.B.a"], 5],
            ["3.A.1.a.ii. Other mature cattle", ["3.A.1.B.b"], 5],
            ["3.A.1.a.iii. Growing cattle", ["3.A.1.B.c"], 5],
            ["3.A.1.a.iv. Other (please specify)", ["3.A.1.B.d"], 5],
            # Other livestock
            ["3.A.2. Sheep", ["3.A.2"], 2],
            ["3.A.3. Swine", ["3.A.3"], 2],
            ["3.A.4. Other livestock", ["3.A.4"], 2],
            # Manure Management
            ["3.B. Manure management", ["3.B"], 1],
            ["3.B.1. Cattle(3)", ["3.B.1"], 2],
            ["Option A:", ["\\IGNORE"], 3],
            ["\\C-AUS\\ 3.B.1.a. Dairy cattle", ["\\IGNORE"], 4],
            ["\\C-AUS\\ 3.B.1.b. Non-dairy cattle", ["\\IGNORE"], 4],
            ["\\C!-AUS\\ 3.B.1.a. Dairy cattle", ["3.B.1.A.a"], 4],
            ["\\C!-AUS\\ 3.B.1.b. Non-dairy cattle", ["3.B.1.A.b"], 4],
            ["Option B (country-specific):", ["\\IGNORE"], 3],
            ["3.B.1.a. Other", ["3.B.1.B"], 4],
            ["3.B.1.a.i. Mature dairy cattle", ["3.B.1.B.a"], 5],
            ["3.B.1.a.ii. Other mature cattle", ["3.B.1.B.b"], 5],
            ["3.B.1.a.iii. Growing cattle", ["3.B.1.B.c"], 5],
            ["3.B.1.a.iv. Other (please specify)", ["3.B.1.B.d"], 5],
            ["3.B.2. Sheep", ["3.B.2"], 2],
            ["3.B.3. Swine", ["3.B.3"], 2],
            ["3.B.4. Other livestock", ["3.B.4"], 2],
            ["3.B.5. Indirect N2O emissions", ["3.B.5"], 2],
            ["3.C. Rice cultivation", ["3.C"], 1],
            ["3.D. Agricultural soils(4,5)", ["3.D"], 1],
            ["3.D.1. Direct N2O emissions from managed soils", ["3.D.a"], 2],
            ["3.D.1.a. Inorganic N fertilizers", ["3.D.a.1"], 3],
            ["3.D.1.b. Organic N fertilizers", ["3.D.a.2"], 3],
            ["3.D.1.c. Urine and dung deposited by grazing animals", ["3.D.a.3"], 3],
            ["3.D.1.d. Crop residues", ["3.D.a.4"], 3],
            [
                "3.D.1.e. Mineralization/immobilization associated with loss/gain of "
                "soil organic matter",
                ["3.D.a.5"],
                3,
            ],
            ["3.D.1.f. Cultivation of organic soils (i.e. histosols)", ["3.D.a.6"], 3],
            ["3.D.1.g. Other", ["3.D.a.7"], 3],
            ["3.D.2. Indirect N2O Emissions from managed soils", ["3.D.b"], 2],
            ["3.E. Prescribed burning of savannahs", ["3.E"], 1],
            ["3.F. Field burning of agricultural residues", ["3.F"], 1],
            ["3.G. Liming", ["3.G"], 1],
            ["3.H. Urea application", ["3.H"], 1],
            ["3.I. Other carbon-containing fertilizers", ["3.I"], 1],
            ["3.J. Other (please specify)", ["3.J"], 1],
            # AUS
            ["NA", ["\\IGNORE"], 2],
            # GUY, MDV
            [
                "Other sources from agriculture (non-carbon pools) "
                "[IPCC Software 3.C.2 and 3.C.14]",
                ["3.J.2"],
                2,
            ],
            # AUT
            ["NOx emissions from manure management", ["3.J.1"], 2],
            # ESP
            ["NOx 3B", ["3.J.1"], 2],
            # NOR
            ["NOx from manure management", ["3.J.1"], 2],
        ],
        "entity_mapping": {"Total GHG emissions (1)": f"KYOTOGHG ({gwp_to_use})"},
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.A": {  # Enteric fermentation
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 45,
            "header": ["entity", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Population size (1)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Average gross energy intake (GE)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Average CH4 conversion rate (Ym) (2)",
                "IMPLIED EMISSION FACTORS CH4",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) Parties are encouraged to provide detailed livestock population "
                "data by animal type and region, if available, in NID, and provide in "
                "the documentation box below a reference to the relevant section. Parties "
                "should use the same animal population statistics to estimate CH4 emissions "
                "from enteric fermentation, CH4 and N2O emissions from manure management, "
                "direct N2O emissions from soil and N2O emissions associated with manure "
                "production, as well as emissions from use of manure as fuel, and "
                "sewage-related emissions reported under the waste sector.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.A.1. Cattle", ["3.A.1"], 0],
            ["Option A:", ["\\IGNORE"], 1],
            # AUS
            ["\\C-AUS\\ 3.A.1.a. Dairy cattle", ["\\IGNORE"], 2],
            ["\\C-AUS\\ 3.A.1.b. Non-dairy cattle", ["\\IGNORE"], 2],
            # other countries
            ["\\C!-AUS\\ 3.A.1.a. Dairy cattle", ["3.A.1.A.a"], 2],
            ["\\C!-AUS\\ 3.A.1.b. Non-dairy cattle", ["3.A.1.A.b"], 2],
            ["Option B (country-specific): (3)", ["\\IGNORE"], 1],
            ["3.A.1.a. Other", ["3.A.1.B"], 2],
            ["Drop-down list:", ["\\IGNORE"], 3],
            ["3.A.1.a.i. Mature dairy cattle", ["3.A.1.B.a"], 3],
            ["3.A.1.a.ii. Other mature cattle", ["3.A.1.B.b"], 3],
            ["3.A.1.a.iii. Growing cattle", ["3.A.1.B.c"], 3],
            ["3.A.1.a.iv. Other (please specify)", ["3.A.1.B.d"], 3],
            # AUS
            ["\\C-AUS\\ Dairy Cattle", ["3.A.1.B.d.AUS-i"], 4],
            ["\\C-AUS\\ Beef Cattle - Pasture", ["3.A.1.B.d.AUS-ii"], 4],
            ["\\C-AUS\\ Beef Cattle - Feedlot", ["3.A.1.C.d.AUS-iii"], 4],
            # MLT
            ["\\C-MLT\\ Bulls", ["3.A.1.B.d.MLT-i"], 4],
            ["\\C-MLT\\ Calves", ["3.A.1.B.d.MLT-ii"], 4],
            # POL
            ["\\C-POL\\ Bulls (older than 2 years)", ["3.A.1.B.d.POL-i"], 4],
            [
                "\\C-POL\\ Non-dairy Heifers (older than 2 years)",
                ["3.A.1.B.d.POL-ii"],
                4,
            ],
            [
                "\\C-POL\\ Non-dairy Young Cattle (younger than 1 year)",
                ["3.A.1.C.d.POL-iii"],
                4,
            ],
            ["\\C-POL\\ Non-dairy Young Cattle (1-2 years)", ["3.A.1.C.d.POL-iv"], 4],
            ["\\C-POL\\ Dairy Cattle", ["3.A.1.C.d.POL-v"], 4],
            ["\\C-POL\\ Non-dairy Cattle", ["3.A.1.C.d.POL-vi"], 4],
            # SVN
            ["\\C-SVN\\ Non-dairy cattle", ["3.A.1.B.d.SVN-i"], 4],
            ["\\C-SVN\\ Other cows", ["3.A.1.B.d.SVN-ii"], 4],
            ["3.A.2. Sheep", ["3.A.2"], 0],
            ["3.A.2.a. Other (please specify)", ["3.A.2.a"], 1],
            # AUS, ITA
            ["Sheep", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Sheep (2)", ["\\IGNORE"], 2],
            # NLD
            ["Sheep (8)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All sheep [IPCC Software 3.A.1.c]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # MLT
            ["\\C-MLT\\ Growing Lambs", ["3.A.2.a.MLT-i"], 2],
            ["\\C-MLT\\ Other Mature Ewes", ["3.A.2.a.MLT-ii"], 2],
            ["\\C-MLT\\ Mature Ewes", ["3.A.2.a.MLT-iii"], 2],
            # SVK
            ["\\C-SVK\\ Mature ewes", ["3.A.2.a.SVK-i"], 2],
            ["\\C-SVK\\ Growing lambs", ["3.A.2.a.SVK-ii"], 2],
            ["\\C-SVK\\ Other mature sheeps", ["3.A.2.a.SVK-iii"], 2],
            # TUR
            ["\\C-TUR\\ Domestic sheep", ["3.A.2.a.TUR-i"], 2],
            ["\\C-TUR\\ Merino sheep", ["3.A.2.a.TUR-ii"], 2],
            ["3.A.3. Swine", ["3.A.3"], 0],
            ["3.A.3.a. Other (please specify)", ["3.A.3.a"], 1],
            # AUS, ITA
            ["Swine", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Swine (3)", ["\\IGNORE"], 2],
            # NLD
            ["Swine (7)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All swine [IPCC Software 3.A.1.h]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # ESP
            ["\\C-ESP\\ White swine (finishing/fattening pigs)", ["3.A.3.a.ESP-i"], 2],
            ["\\C-ESP\\ White swine (sows)", ["3.A.3.a.ESP-ii"], 2],
            [
                "\\C-ESP\\ Iberian swine (finishing/fattening pigs)",
                ["3.A.3.a.ESP-iii"],
                2,
            ],
            ["\\C-ESP\\ Iberian swine (sows)", ["3.A.3.a.ESP-iv"], 2],
            # MLT
            ["\\C-MLT\\ Breeding boars", ["3.A.3.a.MLT-i"], 2],
            ["\\C-MLT\\ Breeding females - gilts", ["3.A.3.a.MLT-ii"], 2],
            ["\\C-MLT\\ Breeding female - sows", ["3.A.3.a.MLT-iii"], 2],
            ["\\C-MLT\\ Fattening pigs more than 50kg", ["3.A.3.a.MLT-iv"], 2],
            ["\\C-MLT\\ Young pigs 20-50kg", ["3.A.3.a.MLT-v"], 2],
            ["\\C-MLT\\ Piglets less than 20kg", ["3.A.3.a.MLT-vi"], 2],
            # SVK
            ["\\C-SVK\\ Breeding swine", ["3.A.3.a.SVK-i"], 2],
            ["\\C-SVK\\ Market swine", ["3.A.3.a.SVK-ii"], 2],
            # NZL
            ["\\C-NZL\\ Pigs", ["\\IGNORE"], 2],
            # most countries
            ["3.A.4. Other livestock(4)", ["3.A.4"], 0],
            ["3.A.4.a. Buffalo", ["3.A.4.a"], 1],
            ["3.A.4.b. Camels", ["3.A.4.b"], 1],
            ["3.A.4.c. Deer", ["3.A.4.c"], 1],
            ["3.A.4.d. Goats", ["3.A.4.d"], 1],
            ["3.A.4.e. Horses", ["3.A.4.e"], 1],
            ["3.A.4.f. Mules and asses", ["3.A.4.f"], 1],
            ["3.A.4.g. Poultry", ["3.A.4.g"], 1],
            ["3.A.4.h. Other", ["3.A.4.h"], 1],
            ["3.A.4.h.i. Rabbit", ["3.A.4.h.i"], 2],
            ["3.A.4.h.ii. Reindeer", ["3.A.4.h.ii"], 2],
            ["3.A.4.h.iii. Ostrich", ["3.A.4.h.iii"], 2],
            ["3.A.4.h.iv. Fur-bearing animals (5)", ["3.A.4.h.iv"], 2],
            ["3.A.4.h.v. Other (please specify)", ["3.A.4.h.v"], 2],
            # GUY
            ["Alpacas [IPCC Software 3.A.1.j]", ["3.A.4.h.v.1"], 3],
            ["Llamas [IPCC Software 3.A.1.j]", ["3.A.4.h.v.2"], 3],
            ["All other species [IPCC Software 3.A.1.j]", ["3.A.4.h.v.10"], 3],
            # SGP
            ["Quail", ["3.A.4.h.v.3"], 3],
            # ESP
            ["Ducks and other poultry", ["3.A.4.h.v.4"], 3],
            ["Turkeys", ["3.A.4.h.v.5"], 3],
            ["Broilers", ["3.A.4.h.v.6"], 3],
            # CHE
            ["Livestock outside agriculture", ["3.A.4.h.v.11"], 3],
            # AUS
            ["3.A.4. Other livestock (4)", ["3.A.4"], 0],
            ["Drop down list:", ["\\IGNORE"], 1],
            ["3.A.4.a. Buffalo", ["3.A.4.a"], 1],
            ["3.A.4.b. Camels", ["3.A.4.b"], 1],
            ["3.A.4.c. Deer", ["3.A.4.c"], 1],
            ["3.A.4.d. Goats", ["3.A.4.d"], 1],
            ["3.A.4.e. Horses", ["3.A.4.e"], 1],
            ["3.A.4.f. Mules and asses", ["3.A.4.f"], 1],
            ["3.A.4.g. Poultry", ["3.A.4.g"], 1],
            ["3.A.4.h. Other", ["3.A.4.h"], 1],
            ["Drop-down list:", ["\\IGNORE"], 2],
            ["3.A.4.h.i. Rabbit", ["3.A.4.h.i"], 2],
            ["3.A.4.h.ii. Reindeer", ["3.A.4.h.ii"], 2],
            ["3.A.4.h.iii. Ostrich", ["3.A.4.h.iii"], 2],
            ["3.A.4.h.iv. Fur-bearing animals (5)", ["3.A.4.h.iv"], 2],
            ["3.A.4.h.v. Other (please specify)", ["3.A.4.h.v"], 2],
            ["Alpacas", ["3.A.4.h.v.i"], 3],
        ],
        "entity_mapping": {"EMISSIONS CH4": "CH4"},
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.B(a)": {  # Manure management CH4
        "status": "tested",
        "table": {
            "firstrow": 6,
            "lastrow": 45,
            "header": ["entity", "entity", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Population size",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Allocation by climate region (1) Cool",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Allocation by climate region (1) Temperate",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Allocation by climate region (1) Warm",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Typical animal mass (average) Warm",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION VS(2) daily excretion (average) Warm",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION CH4 producing potential (Bo) (2) (average) Warm",
                "IMPLIED EMISSION FACTORS CH4 producing potential (Bo) (2) (average) CH4",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) Climate regions are defined in terms of annual average temperature as "
                "follows: cool = less than 15 °C; temperate = 15–25 °C inclusive; and warm "  # noqa: RUF001
                "= higher than 25 °C (see table 10.17, chap. 10, vol. 4 of the 2006 IPCC "
                "Guidelines).",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.B.1. Cattle", ["3.B.1"], 0],
            ["Option A:", ["\\IGNORE"], 1],
            # AUS
            ["\\C-AUS\\ 3.B.1.a. Dairy cattle", ["\\IGNORE"], 2],
            ["\\C-AUS\\ 3.B.1.b. Non-dairy cattle", ["\\IGNORE"], 2],
            # other countries
            ["\\C!-AUS\\ 3.B.1.a. Dairy cattle", ["3.B.1.A.a"], 2],
            ["\\C!-AUS\\ 3.B.1.b. Non-dairy cattle", ["3.B.1.A.b"], 2],
            ["Option B (country-specific): (3)", ["\\IGNORE"], 1],
            ["3.B.1.a. Other", ["3.B.1.B"], 2],
            ["Drop down list:", ["\\IGNORE"], 3],
            ["3.B.1.a.i. Mature dairy cattle", ["3.B.1.B.a"], 3],
            ["3.B.1.a.ii. Other mature cattle", ["3.B.1.B.b"], 3],
            ["3.B.1.a.iii. Growing cattle", ["3.B.1.B.c"], 3],
            ["3.B.1.a.iv. Other (please specify)", ["3.B.1.B.d"], 3],
            # AUS
            ["\\C-AUS\\ Dairy Cattle", ["3.B.1.B.d.AUS-i"], 4],
            ["\\C-AUS\\ Beef Cattle - Pasture", ["3.B.1.B.d.AUS-ii"], 4],
            ["\\C-AUS\\ Beef Cattle - Feedlot", ["3.B.1.C.d.AUS-iii"], 4],
            # MLT
            ["\\C-MLT\\ Bulls", ["3.B.1.B.d.MLT-i"], 4],
            ["\\C-MLT\\ Calves", ["3.B.1.B.d.MLT-ii"], 4],
            # POL
            ["\\C-POL\\ Bulls (older than 2 years)", ["3.B.1.B.d.POL-i"], 4],
            [
                "\\C-POL\\ Non-dairy Heifers (older than 2 years)",
                ["3.B.1.B.d.POL-ii"],
                4,
            ],
            [
                "\\C-POL\\ Non-dairy Young Cattle (younger than 1 year)",
                ["3.B.1.C.d.POL-iii"],
                4,
            ],
            ["\\C-POL\\ Non-dairy Young Cattle (1-2 years)", ["3.B.1.C.d.POL-iv"], 4],
            ["\\C-POL\\ Dairy Cattle", ["3.B.1.C.d.POL-v"], 4],
            ["\\C-POL\\ Non-dairy Cattle", ["3.B.1.C.d.POL-vi"], 4],
            # SVN
            ["\\C-SVN\\ Non-dairy cattle", ["3.B.1.B.d.SVN-i"], 4],
            ["\\C-SVN\\ Other cows", ["3.B.1.B.d.SVN-ii"], 4],
            ["3.B.2. Sheep", ["3.B.2"], 0],
            ["3.B.2.a. Other (please specify)", ["3.B.2.a"], 1],
            # AUS, ITA
            ["Sheep", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Sheep (2)", ["\\IGNORE"], 2],
            # NLD
            ["Sheep (8)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All sheep [IPCC Software 3.A.2.c]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # MLT
            ["\\C-MLT\\ Growing Lambs", ["3.B.2.a.MLT-i"], 2],
            ["\\C-MLT\\ Other Mature Ewes", ["3.B.2.a.MLT-ii"], 2],
            ["\\C-MLT\\ Mature Ewes", ["3.B.2.a.MLT-iii"], 2],
            # SVK
            ["\\C-SVK\\ Mature ewes", ["3.A.2.a.SVK-i"], 2],
            ["\\C-SVK\\ Growing lambs", ["3.A.2.a.SVK-ii"], 2],
            ["\\C-SVK\\ Other mature sheeps", ["3.A.2.a.SVK-iii"], 2],
            # TUR
            ["\\C-TUR\\ Domestic sheep", ["3.B.2.a.TUR-i"], 2],
            ["\\C-TUR\\ Merino sheep", ["3.B.2.a.TUR-ii"], 2],
            ["3.B.3. Swine", ["3.B.3"], 0],
            ["3.B.3.a. Other (please specify)", ["3.B.3.a"], 1],
            # AUS, ITA
            ["Swine", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Swine (3)", ["\\IGNORE"], 2],
            # NLD
            ["Swine (7)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All swine [IPCC Software 3.A.2.h]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # ESP
            ["\\C-ESP\\ White swine (finishing/fattening pigs)", ["3.B.3.a.ESP-i"], 2],
            ["\\C-ESP\\ White swine (sows)", ["3.B.3.a.ESP-ii"], 2],
            [
                "\\C-ESP\\ Iberian swine (finishing/fattening pigs)",
                ["3.B.3.a.ESP-iii"],
                2,
            ],
            ["\\C-ESP\\ Iberian swine (sows)", ["3.B.3.a.ESP-iv"], 2],
            # MLT
            ["\\C-MLT\\ Breeding boars", ["3.B.3.a.MLT-i"], 2],
            ["\\C-MLT\\ Breeding females - gilts", ["3.B.3.a.MLT-ii"], 2],
            ["\\C-MLT\\ Breeding female - sows", ["3.B.3.a.MLT-iii"], 2],
            ["\\C-MLT\\ Fattening pigs more than 50kg", ["3.B.3.a.MLT-iv"], 2],
            ["\\C-MLT\\ Young pigs 20-50kg", ["3.B.3.a.MLT-v"], 2],
            ["\\C-MLT\\ Piglets less than 20kg", ["3.B.3.a.MLT-vi"], 2],
            # SVK
            ["\\C-SVK\\ Breeding swine", ["3.A.3.a.SVK-i"], 2],
            ["\\C-SVK\\ Market swine", ["3.A.3.a.SVK-ii"], 2],
            # NZL
            ["\\C-NZL\\ Pigs", ["\\IGNORE"], 2],
            # most countries
            ["3.B.4. Other livestock (4)", ["3.B.4"], 0],
            ["Drop-down list:", ["\\IGNORE"], 1],  # AUS
            ["3.B.4.a. Buffalo", ["3.B.4.a"], 1],
            ["3.B.4.b. Camels", ["3.B.4.b"], 1],
            ["3.B.4.c. Deer", ["3.B.4.c"], 1],
            ["3.B.4.d. Goats", ["3.B.4.d"], 1],
            ["3.B.4.e. Horses", ["3.B.4.e"], 1],
            ["3.B.4.f. Mules and Asses", ["3.B.4.f"], 1],
            ["3.B.4.g. Poultry", ["3.B.4.g"], 1],
            ["3.B.4.h. Other", ["3.B.4.h"], 1],
            ["Drop-down list:", ["\\IGNORE"], 2],
            ["3.B.4.h.i. Rabbit", ["3.B.4.h.i"], 2],
            ["3.B.4.h.ii. Reindeer", ["3.B.4.h.ii"], 2],
            ["3.B.4.h.iii. Ostrich", ["3.B.4.h.iii"], 2],
            ["3.B.4.h.iv. Fur-bearing animals (5)", ["3.B.4.h.iv"], 2],
            ["3.B.4.h.v. Other (please specify)", ["3.B.4.h.v"], 2],
            # GUY
            ["Alpacas [IPCC Software 3.A.2.j]", ["3.B.4.h.v.1"], 3],
            ["Llamas [IPCC Software 3.A.2.j]", ["3.B.4.h.v.2"], 3],
            ["All other species [IPCC Software 3.A.2.j]", ["3.B.4.h.v.10"], 3],
            # SGP
            ["Quail", ["3.B.4.h.v.3"], 3],
            # ESP
            ["Ducks and other poultry", ["3.B.4.h.v.4"], 3],
            ["Turkeys", ["3.B.4.h.v.5"], 3],
            ["Broilers", ["3.B.4.h.v.6"], 3],
            # AUS
            ["Alpacas", ["3.B.4.h.v.i"], 3],
            # CHE
            ["Livestock outside agriculture", ["3.A.4.h.v.11"], 3],
        ],
        "entity_mapping": {
            "EMISSIONS CH4 producing potential (Bo) (2) (average) CH4": "CH4"
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.B(b)": {  # Manure management N2O
        "status": "tested",
        "table": {
            "firstrow": 5,
            "lastrow": 46,  # don't read indirect emissions as we have them from
            # Table3 and reading them makes the specification very complicated
            "header": ["entity", "entity", "entity", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Population size (1000s)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion rate "
                "(kg N/ head/yr)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Typical animal mass "
                "(average) (kg/ head)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Anaerobic lagoon",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Liquid system",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Daily spread",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Solid storage",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Pit storage",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Dry lot",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Deep bedding",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Pasture range and paddock (1)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Composting",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Digesters",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Burned for fuel or as waste (2)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen excretion per "
                "manure management system (MMS) (kg N/yr) Other (3)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Total N excreted Other (3)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Total N volatilised as "
                "NH3, NOX and N2 (4)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION N lost through leaching "
                "and run-off",
                "IMPLIED EMISSION FACTORS Emission factor per animals Direct and run-off",
                "IMPLIED EMISSION FACTORS Emission factor per animals Indirect "
                "Atmospheric deposition",
                "IMPLIED EMISSION FACTORS Emission factor per animals Indirect "
                "Nitrogen leaching and run-off",
                "EMISSIONS N2O Indirect Atmospheric deposition",
                "EMISSIONS N2O Indirect Nitrogen leaching and run-off",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) Direct and indirect N2O emissions associated with the manure "
                "deposited on agricultural soils or pasture, range and paddock systems "
                "are included under N2O emissions from managed soils (see table "
                "3(III).D-E).",
                "3.B.5. Indirect N2O emissions",
                "Total N handled per MMS (kg N/year)",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.B.1. Cattle", ["3.B.1"], 0],
            ["Option A:", ["\\IGNORE"], 1],
            # AUS
            ["\\C-AUS\\ 3.B.1.a. Dairy cattle", ["\\IGNORE"], 2],
            ["\\C-AUS\\ 3.B.1.b. Non-dairy cattle", ["\\IGNORE"], 2],
            # other countries
            ["\\C!-AUS\\ 3.B.1.a. Dairy cattle", ["3.B.1.A.a"], 2],
            ["\\C!-AUS\\ 3.B.1.b. Non-dairy cattle", ["3.B.1.A.b"], 2],
            ["Option B (country-specific): (5)", ["\\IGNORE"], 1],
            ["3.B.1.a. Other", ["3.B.1.B"], 2],
            ["Drop-down list", ["\\IGNORE"], 3],
            ["3.B.1.a.i. Mature dairy cattle", ["3.B.1.B.a"], 3],
            ["3.B.1.a.ii. Other mature cattle", ["3.B.1.B.b"], 3],
            ["3.B.1.a.iii. Growing cattle", ["3.B.1.B.c"], 3],
            ["3.B.1.a.iv. Other (please specify)", ["3.B.1.B.d"], 3],
            # AUS
            ["\\C-AUS\\ Dairy Cattle", ["3.B.1.B.d.AUS-i"], 4],
            ["\\C-AUS\\ Beef Cattle - Pasture", ["3.B.1.B.d.AUS-ii"], 4],
            ["\\C-AUS\\ Beef Cattle - Feedlot", ["3.B.1.C.d.AUS-iii"], 4],
            # MLT
            ["\\C-MLT\\ Bulls", ["3.B.1.B.d.MLT-i"], 4],
            ["\\C-MLT\\ Calves", ["3.B.1.B.d.MLT-ii"], 4],
            # POL
            ["\\C-POL\\ Bulls (older than 2 years)", ["3.B.1.B.d.POL-i"], 4],
            [
                "\\C-POL\\ Non-dairy Heifers (older than 2 years)",
                ["3.B.1.B.d.POL-ii"],
                4,
            ],
            [
                "\\C-POL\\ Non-dairy Young Cattle (younger than 1 year)",
                ["3.B.1.C.d.POL-iii"],
                4,
            ],
            ["\\C-POL\\ Non-dairy Young Cattle (1-2 years)", ["3.B.1.C.d.POL-iv"], 4],
            ["\\C-POL\\ Dairy Cattle", ["3.B.1.C.d.POL-v"], 4],
            ["\\C-POL\\ Non-dairy Cattle", ["3.B.1.C.d.POL-vi"], 4],
            # SVN
            ["\\C-SVN\\ Non-dairy cattle", ["3.B.1.B.d.SVN-i"], 4],
            ["\\C-SVN\\ Other cows", ["3.B.1.B.d.SVN-ii"], 4],
            ["3.B.2. Sheep", ["3.B.2"], 0],
            ["3.B.2.a. Other (please specify)", ["3.B.2.a"], 1],
            # AUS, ITA
            ["Sheep", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Sheep (3)", ["\\IGNORE"], 2],
            # NLD
            ["Sheep (8)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All sheep [IPCC Software 3.A.2.c]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # MLT
            ["\\C-MLT\\ Growing Lambs", ["3.B.2.a.MLT-i"], 2],
            ["\\C-MLT\\ Other Mature Ewes", ["3.B.2.a.MLT-ii"], 2],
            ["\\C-MLT\\ Mature Ewes", ["3.B.2.a.MLT-iii"], 2],
            # SVK
            ["\\C-SVK\\ Mature ewes", ["3.B.2.a.SVK-i"], 2],
            ["\\C-SVK\\ Growing lambs", ["3.B.2.a.SVK-ii"], 2],
            ["\\C-SVK\\ Other mature sheeps", ["3.B.2.a.SVK-iii"], 2],
            # TUR
            ["\\C-TUR\\ Domestic sheep", ["3.B.2.a.TUR-i"], 2],
            ["\\C-TUR\\ Merino sheep", ["3.B.2.a.TUR-ii"], 2],
            ["3.B.3. Swine", ["3.B.3"], 0],
            ["3.B.3.a. Other (please specify)", ["3.B.3.a"], 1],
            # AUS, ITA
            ["Swine", ["\\IGNORE"], 2],
            # ITA, NLD
            ["Swine (2)", ["\\IGNORE"], 2],
            # NLD
            ["Swine (7)", ["\\IGNORE"], 2],
            # GUY, MDV
            ["All swine [IPCC Software 3.A.2.h]", ["\\IGNORE"], 2],
            # SGP
            ["NA", ["\\IGNORE"], 2],
            # ESP
            ["\\C-ESP\\ White swine (finishing/fattening pigs)", ["3.B.3.a.ESP-i"], 2],
            ["\\C-ESP\\ White swine (sows)", ["3.B.3.a.ESP-ii"], 2],
            [
                "\\C-ESP\\ Iberian swine (finishing/fattening pigs)",
                ["3.B.3.a.ESP-iii"],
                2,
            ],
            ["\\C-ESP\\ Iberian swine (sows)", ["3.B.3.a.ESP-iv"], 2],
            # MLT
            ["\\C-MLT\\ Breeding boars", ["3.B.3.a.MLT-i"], 2],
            ["\\C-MLT\\ Breeding females - gilts", ["3.B.3.a.MLT-ii"], 2],
            ["\\C-MLT\\ Breeding female - sows", ["3.B.3.a.MLT-iii"], 2],
            ["\\C-MLT\\ Fattening pigs more than 50kg", ["3.B.3.a.MLT-iv"], 2],
            ["\\C-MLT\\ Young pigs 20-50kg", ["3.B.3.a.MLT-v"], 2],
            ["\\C-MLT\\ Piglets less than 20kg", ["3.B.3.a.MLT-vi"], 2],
            # SVK
            ["\\C-SVK\\ Breeding swine", ["3.B.3.a.SVK-i"], 2],
            ["\\C-SVK\\ Market swine", ["3.B.3.a.SVK-ii"], 2],
            # NZL
            ["\\C-NZL\\ Pigs", ["\\IGNORE"], 2],
            ["3.B.4. Other livestock (6)", ["3.B.4"], 0],
            ["Drop-down list", ["\\IGNORE"], 1],  # AUS
            ["3.B.4.a. Buffalo", ["3.B.4.a"], 1],
            ["3.B.4.b. Camels", ["3.B.4.b"], 1],
            ["3.B.4.c. Deer", ["3.B.4.c"], 1],
            ["3.B.4.d. Goats", ["3.B.4.d"], 1],
            ["3.B.4.e. Horses", ["3.B.4.e"], 1],
            ["3.B.4.f. Mules and asses", ["3.B.4.f"], 1],
            ["3.B.4.g. Poultry", ["3.B.4.g"], 1],
            ["3.B.4.h. Other", ["3.B.4.h"], 1],
            ["Drop-down list:", ["\\IGNORE"], 2],  # AUS
            ["3.B.4.h.i. Rabbit", ["3.B.4.h.i"], 2],
            ["3.B.4.h.ii. Reindeer", ["3.B.4.h.ii"], 2],
            ["3.B.4.h.iii. Ostrich", ["3.B.4.h.iii"], 2],
            ["3.B.4.h.iv Fur-bearing animals (7)", ["3.B.4.h.iv"], 2],
            ["3.B.4.h.v. Other (please specify)", ["3.B.4.h.v"], 2],
            # GUY
            ["Alpacas [IPCC Software 3.A.2.j]", ["3.B.4.h.v.1"], 3],
            ["Llamas [IPCC Software 3.A.2.j]", ["3.B.4.h.v.2"], 3],
            ["All other species [IPCC Software 3.A.2.j]", ["3.B.4.h.v.10"], 3],
            # SGP
            ["Quail", ["3.B.4.h.v.3"], 3],
            # ESP
            ["Ducks and other poultry", ["3.B.4.h.v.4"], 3],
            ["Turkeys", ["3.B.4.h.v.5"], 3],
            ["Broilers", ["3.B.4.h.v.6"], 3],
            # AUS
            ["Alpacas", ["3.B.4.h.v.i"], 3],
            # CHE
            ["Livestock outside agriculture", ["3.B.4.h.v.11"], 3],
        ],
        "entity_mapping": {
            "EMISSIONS N2O Direct Nitrogen leaching and run-off": "N2O",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO: tables 3.A and 3.B for livestock details as they are not contained in table3
    "Table3.C": {  # rice cultivation details
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 25,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Harvested area (2)",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Organic amendments added (3)",
                "IMPLIED EMISSION FACTOR (1) CH4",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) The IEF implicitly takes account of all relevant corrections for "
                "continuously flooded fields without organic amendments, the correction"
                " for organic amendments and the effect of different soil "
                "characteristics, if considered in the calculation of CH4 emissions.",
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.C.1. Irrigated", ["3.C.1"]],
            ["3.C.1.a. Continuously flooded", ["3.C.1.a"]],
            ["3.C.1.b. Intermittently flooded", ["3.C.1.b"]],
            ["3.C.1.b.i. Single aeration", ["3.C.1.b.i"]],
            ["3.C.1.b.ii.Multiple aeration", ["3.C.1.b.ii"]],
            ["3.C.2. Rain-fed", ["3.C.2"]],
            ["3.C.2.a. Flood-prone", ["3.C.2.a"]],
            ["3.C.2.b. Drought-prone", ["3.C.2.b"]],
            ["3.C.3. Deep water", ["3.C.3"]],
            ["3.C.3.a. Water depth 50–100 cm", ["3.C.3.a"]],  # noqa: RUF001
            ["3.C.3.b. Water depth > 100 cm", ["3.C.3.b"]],
            ["3.C.4. Other (please specify)", ["3.C.4"]],
            # AUS
            ["NA", ["\\IGNORE"]],
            # GUY, MDV
            ["Other rice ecosystems [IPCC Software 3.C.7]", ["\\IGNORE"]],
            # ignore as just for comparison
            ["Upland rice(4)", ["\\IGNORE"]],
            ["Total(4)", ["\\IGNORE"]],
        ],
        "entity_mapping": {
            "EMISSIONS CH4": "CH4",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.D": {  # direct and indirect N2O from soils
        "status": "tested",
        "table": {
            "firstrow": 7,
            "lastrow": 24,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Description",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Value",
                "IMPLIED EMISSION FACTORS Value",
                # "Fraction (a) FracGASF",
                # "Description Fraction of synthetic fertilizer N applied to soils that "
                # "volatilises as NH3 and NOX",
                # "Value 0.11",
            ],
            "stop_cats": [
                "",
                "nan",
                "(1) To convert from N2O–N to N2O emissions, multiply by 44/28.",  # noqa: RUF001
            ],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.D.1. Direct N2O emissions from managed soils", ["3.D.a"]],
            ["3.D.1.a. Inorganic N fertilizers (3)", ["3.D.a.1"]],
            ["3.D.1.b. Organic N fertilizers (3)", ["3.D.a.2"]],
            ["3.D.1.b.i. Animal manure applied to soils", ["3.D.a.2.a"]],
            ["3.D.1.b.ii. Sewage sludge applied to soils", ["3.D.a.2.b"]],
            ["3.D.1.b.iii. Other organic fertilizers applied to soils", ["3.D.a.2.c"]],
            ["3.D.1.c. Urine and dung deposited by grazing animals", ["3.D.a.3"]],
            ["3.D.1.d. Crop residues", ["3.D.a.4"]],
            [
                "3.D.1.e. Mineralization/immobilization associated with loss/gain of "
                "soil organic matter (4,5)",
                ["3.D.a.5"],
            ],
            ["3.D.1.f. Cultivation of organic soils (i.e. histosols) (2)", ["3.D.a.6"]],
            ["3.D.1.g. Other", ["3.D.a.7"]],
            ["3.D.2. Indirect N2O Emissions from managed soils", ["3.D.b"]],
            ["3.D.2.a. Atmospheric deposition (6)", ["3.D.b.1"]],
            ["3.D.2.b. Nitrogen leaching and run-off", ["3.D.b.2"]],
        ],
        "entity_mapping": {
            "EMISSIONS N2O": "N2O",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    "Table3.E": {  # savanna burning details
        "status": "TODO",  # actually done but empty and crashes
        "table": {
            "firstrow": 7,
            "lastrow": 13,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Area of savannah burned",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Average above-ground biomass density",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Biomass burned",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Fraction of savannah "
                "burned",
                "ACTIVITY DATA AND OTHER RELATED INFORMATION Nitrogen fraction in biomass",
                "IMPLIED EMISSION FACTORS CH4",
                "IMPLIED EMISSION FACTORS N2O",
            ],
            "stop_cats": ["", ".", "nan"],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [
            ["3.E.1. Forest land (specify ecological zone) (2)", ["3.E.1"], 0],
            ["NA", ["\\IGNORE"], 1],
            ["3.E.2. Grassland (specify ecological zone) (2)", ["3.E.2"], 0],
            ["NA", ["\\IGNORE"], 1],
        ],
        "entity_mapping": {
            "EMISSIONS (2) CH4": "CH4",
            "EMISSIONS (2) N2O": "N2O",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table3.F": {  # field burning details
        "status": "TODO",
        "table": {
            "firstrow": 7,
            "lastrow": 29,
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", "nan"],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [],
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
            "header": ["group", "entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", "nan"],
            "unit_info": unit_info["default"],
        },
        "sector_mapping": [],
        "entity_mapping": [],
        "coords_defaults": {
            "class": "Total",
        },
    },  # TODO
    "Table4": {  # LULUCF overview
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 33,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": ["", ".", "nan"],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ["4. Total LULUCF", ["4"]],
            ["4.A. Forest land", ["4.A"]],
            ["4.A.1. Forest land remaining forest land", ["4.A.1"]],
            ["4.A.2. Land converted to forest land", ["4.A.2"]],
            ["4.B. Cropland", ["4.B"]],
            ["4.B.1. Cropland remaining cropland", ["4.B.1"]],
            ["4.B.2. Land converted to cropland", ["4.B.2"]],
            ["4.C. Grassland", ["4.C"]],
            ["4.C.1. Grassland remaining grassland", ["4.C.1"]],
            ["4.C.2. Land converted to grassland", ["4.C.2"]],
            ["4.D. Wetlands (5)", ["4.D"]],
            ["4.D.1. Wetlands remaining wetlands", ["4.D.1"]],
            ["4.D.2. Land converted to wetlands", ["4.D.2"]],
            ["4.E. Settlements", ["4.E"]],
            ["4.E.1. Settlements remaining settlements", ["4.E.1"]],
            ["4.E.2. Land converted to settlements", ["4.E.2"]],
            ["4.F. Other land (6)", ["4.F"]],
            ["4.F.1. Other land remaining other land", ["4.F.1"]],
            ["4.F.2. Land converted to other land", ["4.F.2"]],
            ["4.G. Harvested wood products (7)", ["4.G"]],
            ["4.H. Other (please specify)", ["4.H"]],
            ["Land converted to Settlement", ["4.H.1"]],
            ["Aquaculture", ["4.H.10"]],
            ["Seagrass", ["4.H.11"]],
            # GUY, MDV
            ["N2O emissions from aquaculture [IPCC Software 3.C.12]", ["4.H.6"]],
            ["Other emissions from LULUCF [IPCC Software 3.D.2]", ["4.H.9"]],
            # SGP, NZL
            ["Other", ["4.H.9"]],
            # JPN
            ["Concrete using Biochar", ["4.H.10"]],
            # currently ignoring memo item
        ],
        "entity_mapping": {
            "CH4(2)": "CH4",
            "N2O(2)": "N2O",
            "Net CO2 emissions/removals (1,2)": "CO2",
            "Total GHG emissions/removals (3)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO: all other LULUCF tables
    "Table5": {  # Waste overview
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 31,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [
                "",
                "nan",
                '(1) "Total GHG emissions" does not include NOX, CO, NMVOC and SOX.',
            ],
            "unit_info": unit_info["industry"],
        },
        "sector_mapping": [
            ["5. Total waste", ["5"]],
            ["5.A. Solid waste disposal", ["5.A"]],
            ["5.A.1. Managed waste disposal sites", ["5.A.1"]],
            ["5.A.2. Unmanaged waste disposal sites", ["5.A.2"]],
            ["5.A.3. Uncategorized waste disposal sites", ["5.A.3"]],
            ["5.B. Biological treatment of solid waste", ["5.B"]],
            ["5.B.1. Composting", ["5.B.1"]],
            ["5.B.2. Anaerobic digestion at biogas facilities", ["5.B.2"]],
            ["5.C. Incineration and open burning of waste", ["5.C"]],
            ["5.C.1. Waste incineration", ["5.C.1"]],
            ["5.C.2. Open burning of waste", ["5.C.2"]],
            ["5.D. Wastewater treatment and discharge", ["5.D"]],
            ["5.D.1. Domestic wastewater", ["5.D.1"]],
            ["5.D.2. Industrial wastewater", ["5.D.2"]],
            ["5.D.3. Other", ["5.D.3"]],
            ["5.E. Other (please specify)", ["5.E"]],
            ["Accidential fires at Solid Waste Disposal Sites", ["5.E.9"]],
            # GUY, MDV
            [
                "CH₄ and N₂O emissions from methane flaring at waste facilities "
                "[IPCC Software 4.E]",
                ["5.E.6"],
            ],
            ["Other waste emissions [IPCC Software 4.E, SO₂ from 4.A-4.D]", ["5.E.5"]],
            # SGP
            ["NA", ["\\IGNORE"]],
            # CHE
            ["Car shredding", ["5.E.10"]],
            # ESP
            ["Accidental combustion", ["5.E.3"]],
            ["Sludge spreading", ["5.E.7"]],
            # JPN
            ["Decomposition of fossil-fuel derived surfactants", ["5.E.4"]],
            # PRT
            ["Biogas burning without energy recovery", ["5.E.6"]],
            ["Memo item: (3)", ["\\IGNORE"]],
            ["5.F.1. Long-term storage of C in waste disposal sites", ["M.Memo.LTSW"]],
            ["5.F.2. Annual change in total long-term C storage", ["M.Memo.ACLT"]],
            [
                "5.F.3. Annual change in total long-term C storage in HWP waste (4)",
                ["M.Memo.ACLTHWP"],
            ],
        ],
        "entity_mapping": {
            "CO2(1)": "CO2",
            "Total GHG emissions (1)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO 5.A-D
    "Summary1": {  # Summary 1
        "status": "tested",
        "table": {
            "firstrow": 8,
            "lastrow": 71,
            "header": ["entity", "unit"],
            "col_for_categories": "GREENHOUSE GAS SOURCE AND SINK CATEGORIES",
            "categories": ["category"],
            "cols_to_ignore": [],
            "stop_cats": [
                "(1) The emissions of HFCs, PFCs, unspecified mix of HFCs and PFCs and "
                "other F-gases are to be expressed as CO2 eq. emissions. Data on "
                "disaggregated emissions of HFCs and PFCs are to be provided in "
                "table 2(II) of this common reporting format."
            ],
            "unit_info": unit_info["summary"],
        },
        "sector_mapping": [
            ["Total national emissions and removals", ["0"]],
            ["1. Energy", ["1"]],
            ["1.A. Fuel combustion", ["1.A"]],
            ["1.A.1. Energy industries", ["1.A.1"]],
            ["1.A.2. Manufacturing industries and construction", ["1.A.2"]],
            ["1.A.3. Transport", ["1.A.3"]],
            ["1.A.4. Other sectors", ["1.A.4"]],
            ["1.A.5. Other", ["1.A.5"]],
            ["1.B. Fugitive emissions from fuels", ["1.B"]],
            ["1.B.1. Solid fuels", ["1.B.1"]],
            [
                "1.B.2. Oil and natural gas and other emissions from energy production",
                ["1.B.2"],
            ],
            ["1.C. CO2 Transport and storage", ["1.C"]],
            ["2. Industrial processes and product use", ["2"]],
            ["2.A. Mineral industry", ["2.A"]],
            ["2.B. Chemical industry", ["2.B"]],
            ["2.C. Metal industry", ["2.C"]],
            ["2.D. Non-energy products from fuels and solvent use", ["2.D"]],
            ["2.E. Electronic industry", ["2.E"]],
            ["2.F. Product uses as substitutes for ODS", ["2.F"]],
            ["2.G. Other product manufacture and use", ["2.G"]],
            ["2.H. Other (4)", ["2.H"]],
            ["3. Agriculture", ["3"]],
            ["3.A. Enteric fermentation", ["3.A"]],
            ["3.B. Manure management", ["3.B"]],
            ["3.C. Rice cultivation", ["3.C"]],
            ["3.D. Agricultural soils", ["3.D"]],
            ["3.E. Prescribed burning of savannahs", ["3.E"]],
            ["3.F. Field burning of agricultural residues", ["3.F"]],
            ["3.G. Liming", ["3.G"]],
            ["3.H. Urea application", ["3.H"]],
            ["3.I. Other carbon-containing fertilizers", ["3.I"]],
            ["3.J. Other", ["3.J"]],
            ["4. Land use, land-use change and forestry (5)", ["4"]],
            ["4.A. Forest land (5)", ["4.A"]],
            ["4.B. Cropland (5)", ["4.B"]],
            ["4.C. Grassland (5)", ["4.C"]],
            ["4.D. Wetlands (5)", ["4.D"]],
            ["4.E. Settlements (5)", ["4.E"]],
            ["4.F. Other land (5)", ["4.F"]],
            ["4.G. Harvested wood products (5)", ["4.G"]],
            ["4.H. Other (5)", ["4.H"]],
            ["5. Waste", ["5"]],
            ["5.A. Solid waste disposal (6)", ["5.A"]],
            ["5.B. Biological treatment of solid waste", ["5.B"]],
            ["5.C. Incineration and open burning of waste (6)", ["5.C"]],
            ["5.D. Wastewater treatment and discharge", ["5.D"]],
            ["5.E. Other (6)", ["5.E"]],
            ["6. Other (please specify) (7)", ["6"]],
            # GUY, MDV
            ["Other sources of emissions/removals [IPCC Software 5.C]", ["6.A"]],
            # CHE
            ["Other non-specified", ["6.A"]],
            # JPN
            ["Smoking", ["6.B"]],
            # NZL
            ["\\C-NZL\\ 6. Tokelau_1. Energy", ["6.NZL-A"]],
            [
                "\\C-NZL\\ 6. Tokelau_2. Industrial Processes and Product Use",
                ["6.NZL-B"],
            ],
            ["\\C-NZL\\ 6. Tokelau_3. Agriculture", ["6.NZL-C"]],
            ["\\C-NZL\\ 6. Tokelau_5. Waste", ["6.NZL-D"]],
            # AUS
            ["NA", ["\\IGNORE"]],
            ["", ["\\IGNORE"]],
            ["nan", ["\\IGNORE"]],
            ["Memo items: (8)", ["\\IGNORE"]],
            ["1.D.1. International bunkers", ["M.Memo.Int"]],
            ["1.D.1.a. Aviation", ["M.Memo.Int.Avi"]],
            ["1.D.1.b. Navigation", ["M.Memo.Int.Mar"]],
            ["1.D.2. Multilateral operations", ["M.Memo.Mult"]],
            ["1.D.3. CO2 emissions from biomass", ["M.Memo.Bio"]],
            ["1.D.4. CO2 captured", ["M.Memo.CO2Cap"]],
            ["5.F.1. Long-term storage of C in waste disposal sites", ["M.Memo.LTSW"]],
            ["Indirect N2O", ["M.Memo.IndN2O"]],
            ["Indirect CO2", ["M.Memo.IndCO2"]],
        ],
        "entity_mapping": {
            "NOX": "NOx",
            "Net CO2 emissions/ removals": "CO2",
            "HFCs (1)": f"HFCS ({gwp_to_use})",
            "PFCs (1)": f"PFCS ({gwp_to_use})",
            "Unspecified mix of HFCs and PFCs (1)": f"UnspMixOfHFCsPFCs ({gwp_to_use})",
            "Total GHG emissions/removals (2)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
}
