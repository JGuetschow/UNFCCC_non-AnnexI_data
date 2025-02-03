"""

CRT1 specification for Chile.

Header in Table3.B(b) differs. This is a quick fix. In the future the column matching
should be improved to allow for different column names at least for ignored columns

"""

from copy import deepcopy

from .crt1_specification import CRT1

gwp_to_use = "AR5GWP100"

CRT1_ECU = deepcopy(CRT1)
# iognore NMVOC in table 4 as it has comma as decimal sep for 2000
CRT1_ECU["Table4"]["table"]["cols_to_ignore"].append("NMVOC")
