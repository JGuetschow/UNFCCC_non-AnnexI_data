# Collaborative UNFCCC non-AnnexI dataset

## Description
### Structure
The repository is structured by folders

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (folder *BUR*) an automatical dowloaded exists. For National Communications (folder *NC*) it is under development. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC.
* **extracted_data** This folder holds all extracted datasets in primap2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: \<iso\>\_\<rep\>\_\<year\> where \<iso\> is the countries 3 letter iso code, \<rep\> is the repor, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), and \<year\> is the year of publication.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed suubmissions or subsets (e.g. all first BURs) and code to generate composite datasets. TODO: subfolder structure
* **composite_datasets** This folder contains generated composite datasets in primap2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year)

## Usage

## Contributing

### What data should be read

minimal requirements for use cases
* for PRIMAP-hist
* for FAOSTAT
