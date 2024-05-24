"""Read individual country submissions

The UNFCCC reader contains code to read individual country inventories,
mostly submitted by non-AnnexI countries to the UNFCCC as Biannial Update Reports (
BUR), National Communications (NC), and National Inventory Reports (NIR). Code tyo
read other official country repositories is also included here as it uses the same
setup.

The code is organized in country folders which contain scripts for each submission
and configuration files which can also be used for several submissions if the
configuration is sufficiently similar.

Data are mostly read from pdf files using camelot, but in some cases machine-readable
files like xlsx are available which we prefer over pdfs.

"""
