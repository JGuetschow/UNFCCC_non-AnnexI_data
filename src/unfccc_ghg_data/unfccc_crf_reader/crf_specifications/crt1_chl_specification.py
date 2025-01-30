"""

CRT1 specification for Chile.

Header in Table3.B(b) differs. This is a quick fix. In the future the column matching
should be improved to allow for different column names at least for ignored columns

"""

from copy import deepcopy

from .crt1_specification import CRT1

gwp_to_use = "AR5GWP100"

CRT1_CHL = deepcopy(CRT1)

CRT1_CHL["Table3.B(b)"]["table"]["cols_to_ignore"][
    3
] = "ACTIVITY DATA AND OTHER RELATED INFORMATION Typical animal mass (average) (kg/ animal)"
