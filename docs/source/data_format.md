# Data format description (columns)

All data in this repository in the comma-separated values (CSV) files is formatted consistently with the PRIMAP2 interchange format. A yaml file with metadata accompanies each csv file. Datasets are also available in the native primap2 format which is based on netcdf. For a description please consult the [primap2 documentation](https://primap2.readthedocs.io/en/main/data_format_examples.html).

For the csf files the data contained in each column is as follows:

## "source"
Name of the data source. Four country specific datasets it is `\<ISO3\>-GHG-inventory`, where `\<ISO3\>` is the ISO 3166 three-letter country code. Processed submission data uses the source `BUR_NUR` so it can easily be combined into a single source for several countries. Data from the UNFCCC DI portal and CRF data use the source `UNFCCC` both for single countries and datasets for all countries or country groups.

## "scenario (\<terminology>\)"
The scenario specifies the submissions (e.g. BUR1, NC5, or Inventory_2021 for a non-UNFCCC inventory). The scenario terminology is `PRIMAP`.

For data from the UNFCCC DI interface uses the scenario is `DIYYYY-MM-DD` where `YYYY-MM-DD` is the data the DI data was accessed or processed. The terminology for DI data is `Access_Date` for raw data and `Process_Date` for processed data.

## "provenance"
Provenance of the data. "measured" for submissions and "derived" for composite sources.

## "country (ISO3)"
ISO 3166 three-letter country codes.

## "entity"
Gas categories using global warming potentials (GWP) from either Second (SAR), Fourth (AR4), Fifth (AR5), or Sixths Assessment Report (AR6).

Code                     Description
----                     -----------
CH4                      Methane
CO2                      Carbon Dioxide
N2O                      Nitrous Oxide
HFCS (SARGWP100)         Hydrofluorocarbons (SAR)
HFCS (AR4GWP100)         Hydrofluorocarbons (AR4)
HFCS (AR5GWP100)         Hydrofluorocarbons (AR5)
HFCS (AR6GWP100)         Hydrofluorocarbons (AR6)
PFCS (SARGWP100)         Perfluorocarbons (SAR)
PFCS (AR4GWP100)         Perfluorocarbons (AR4)
PFCS (AR5GWP100)         Perfluorocarbons (AR5)
PFCS (AR6GWP100)         Perfluorocarbons (AR6)
SF6                      Sulfur Hexafluoride
NF3                      Nitrogen Trifluoride
FGASES (SARGWP100)       Fluorinated Gases (SAR): HFCs, PFCs, SF$_6$, NF$_3$
FGASES (AR4GWP100)       Fluorinated Gases (AR4): HFCs, PFCs, SF$_6$, NF$_3$
FGASES (AR5GWP100)       Fluorinated Gases (AR5): HFCs, PFCs, SF$_6$, NF$_3$
FGASES (AR6GWP100)       Fluorinated Gases (AR6): HFCs, PFCs, SF$_6$, NF$_3$
KYOTOGHG (SARGWP100)     Kyoto greenhouse gases (SAR)
KYOTOGHG (AR4GWP100)     Kyoto greenhouse gases (AR4)
KYOTOGHG (AR5GWP100)     Kyoto greenhouse gases (AR5)
KYOTOGHG (AR6GWP100)     Kyoto greenhouse gases (AR6)

Table: Gas categories and underlying global warming potentials

Some datasets also contain individual fluorinated gases from the HFC and PFC baskets.


## "unit"
Units are of the form *Gg/Mt/... \<substance\> / yr* where substance is the entity or for CO$_2$ equivalent units *Gg/Mt/... CO2 / yr*. The CO$_2$-equivalent is calculated according to the global warming potential indicated by the entity (see above).


## "category (\<term\>)"
Categories for emission as defined in terminology \<term\>. Terminology names are those used in the [climate_categories](https://github.com/pik-primap/climate_categories) package. If the terminology name contains *\_PRIMAP* is means that some (sub)categories have been added to the official IPCC category hierarchy. Added categories outside the hierarchy begin with the prefix *M*.

## "CategoryName"
optional column. Original name of the category as presented in the submission.

## "CategoryNameTranslation"
Optional column. In some cases original category names have been translated to english. In this case these translations are stored in this column.

## Remaining columns

Years (depending on dataset)
