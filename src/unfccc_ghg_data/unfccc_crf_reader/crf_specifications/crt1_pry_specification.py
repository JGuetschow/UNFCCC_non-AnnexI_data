"""

CRT1 specification for Paraguay.

Some tables (agriculture) differ from the template and
need an individual specification

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

from .crt1_specification import CRT1
from .util import unit_info

gwp_to_use = "AR5GWP100"

tables_identical = [  # some might have
    "Table1",
    "Table1.A(a)s1",
    "Table1.A(a)s2",
    "Table1.A(a)s3",
    "Table1.A(a)s4",
    "Table1.B.1",
    "Table1.B.2",
    "Table1.C",
    "Table1.D",
    "Table2(I)",
    "Table2(II)",
    "Table4",
    # "Summary1",  # mixed decimal separators, can't be read
]

# table_suffixes = [
#     "_90", "_91", "_92", "_93", "_94", "_95", "_96", "_97", "_98", "_99",
#     "_00", "_01", "_02", "_03", "_04", "_05", "_06", "_07", "_08", "_09",
#     "_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", "_18", "_19",
#     "_20", "_21",
# ]
#
# tables_for_suffixes = [
#     "Table3.A", "Table3.B(a)", "Table3.B(b)", "Table3.C", "Table3.D"
# ]

CRT1_PRY = {
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
                "Documentation box:",
                '(1) "Total GHG emissions" does not include NOX, CO, NMVOC and SOX.',
            ],
            "unit_info": unit_info["industry"],
            "decimal_sep": ",",
            "thousands_sep": ".",
        },
        "sector_mapping": [
            ["3. Total agriculture", ["3"], 0],
            # A. Enteric fermentation
            ["3.A. Enteric fermentation", ["3.A"], 1],
            ["\\C!-CHL\\ 3.A.1. Cattle(3)", ["3.A.1"], 2],
            ["\\C!-CHL\\ Option A:", ["\\IGNORE"], 3],
            ["\\C-AUS\\ 3.A.1.a. Dairy cattle", ["\\IGNORE"], 4],
            ["\\C-AUS\\ 3.A.1.b. Non-dairy cattle", ["\\IGNRE"], 4],
            ["\\C!-AUS-CHL\\ 3.A.1.a. Dairy cattle", ["3.A.1.A.a"], 4],
            ["\\C!-AUS-CHL\\ 3.A.1.b. Non-dairy cattle", ["3.A.1.A.b"], 4],
            ["\\C-CHL\\ Option A:", ["\\IGNORE"], 2],  # 3.A.1 missing
            ["\\C-CHL\\ 3.A.1.a. Dairy cattle", ["3.A.1.A.a"], 3],
            ["\\C-CHL\\ 3.A.1.b. Non-dairy cattle", ["3.A.1.A.b"], 3],
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
            ["\\C-AUS-BRA-CHL-SGP\\ NA", ["\\IGNORE"], 2],
            [
                "\\C-GUY-MDV-AZE-BTN-BRN-GNB-KEN-LBN-MYS-MUS-URY-UZB-FRA\\ "
                "Other sources from agriculture (non-carbon pools) "
                "[IPCC Software 3.C.2 and 3.C.14]",
                ["3.J.2"],
                2,
            ],
            ["\\C-BLR-LTU\\ Other", ["3.J.2"], 2],
            ["\\C-DEU\\ Digestate renewable raw material (storage of N)", ["3.J.6"], 2],
            [
                "\\C-DEU\\ Digestate renewable raw material (atmospheric deposition)",
                ["3.J.7"],
                2,
            ],
            [
                "\\C-DEU\\ Digestate renewable raw material (storage of dry matter)",
                ["3.J.8"],
                2,
            ],
            ["\\C-DEU\\ 3.B NOx Emissions", ["3.J.1"], 2],
            ["\\C-AUT\\ NOx emissions from manure management", ["3.J.1"], 2],
            ["\\C-ESP\\ NOx 3B", ["3.J.1"], 2],
            ["\\C-NOR-DNK-SWE\\ NOx from manure management", ["3.J.1"], 2],
            ["\\C-IRL\\ NOx from Manure Management", ["3.J.1"], 2],
            ["\\C-COL\\ 3.B. NOx_Manure management", ["3.J.1"], 2],
            ["\\C-PRY\\ Total", ["\\IGNORE"], 2],
        ],
        "entity_mapping": {"Total GHG emissions (1)": f"KYOTOGHG ({gwp_to_use})"},
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO other agri tables
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
            "decimal_sep": ",",
            "thousands_sep": ".",
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
            [
                "CH₄ and N₂O emissions from methane flaring at waste facilities "
                "[IPCC Software 4.E]",
                ["5.E.6"],
            ],
            ["Other waste emissions [IPCC Software 4.E, SO₂ from 4.A-4.D]", ["5.E.5"]],
            ["Memo item: (3)", ["\\IGNORE"]],
            ["5.F.1. Long-term storage of C in waste disposal sites", ["M.Memo.LTSW"]],
            [
                "5.F.2. Annual change in total long-term C storage",
                ["M.Memo.ACLT"],
            ],
            [
                "5.F.3. Annual change in total long-term C storage in HWP waste (4)",
                ["M.Memo.ACLTHWP"],
            ],
        ],
        "entity_mapping": {
            # "CO2(1)": "CO2",
            "Total GHG emissions (1)": f"KYOTOGHG ({gwp_to_use})",
        },
        "coords_defaults": {
            "class": "Total",
        },
    },  # tested
    # TODO 5.A-D
}

for table in tables_identical:
    CRT1_PRY[table] = CRT1[table]
