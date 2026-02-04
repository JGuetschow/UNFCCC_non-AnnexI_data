"""

CRT1 specification for Peru.

Table 1.A(a)s3 is named Table 1.A(a)3, so it is renamed from the general specification

"""

from copy import deepcopy

from .crt1_specification import CRT1

gwp_to_use = "AR5GWP100"

tables_identical = [  # some might have
    "Table1",
    "Table1.A(a)s1",
    "Table1.A(a)s2",
    # "Table1.A(a)s3",  # has to be renamed
    "Table1.A(a)s4",
    "Table1.B.1",
    "Table1.B.2",
    "Table1.C",
    "Table1.D",
    "Table2(I)",
    "Table2(II)",
    "Table3",
    "Table3.A",
    "Table3.B(a)",
    "Table3.B(b)",
    "Table3.C",
    "Table3.D",
    "Table3.E",
    "Table3.F",
    "Table3.G-I",
    "Table4",
    "Table5",
    "Summary1",  # mixed decimal separators, can't be read
]

CRT1_PER = {"Table 1.A(a)3": deepcopy(CRT1["Table1.A(a)s3"])}
CRT1_PER["Table 1.A(a)3"]["table"]["firstrow"] = 5
CRT1_PER["Table 1.A(a)3"]["table"]["firstrow_fallback"] = 6

for table in tables_identical:
    CRT1_PER[table] = CRT1[table]
