# Usage

## Overview
Introduce readers and downloaders




## Repository structure
The repository is structured by folders. Here we list the folders in order of processing.

**TODO:** update and maybe move section into individual files and just keep intros here

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (BUR), national Communications (NC), and Nationally Determined Contributions (NDC) an automatical dowloaded exists (folder UNFCCC). Within the UNFCCC folder the data is organized in a *\<country\>/\<submission\>* structure. NDC submissions are often revised. To be able to keep track of the targets and emissions inventories we store each NDC revision in a time-stamped folder. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC. The internal structure is the same as for the UNFCCC folder.
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC. As the repository is in the process of being set up, there currently is no data available.
* **extracted_data** This folder holds all extracted datasets in PRIMAP2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>_\<term\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, and *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996. As the repository is in the process of being set up, there currently is no data available.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed submissions or subsets (e.g. all first BURs) and code to generate composite datasets. Currently the only subfolder is the *UNFCCC_downloader* where code to automatically download BUR and NC submission files from the [UNFCCC website](https://www.unfccc.int) resides.
* **composite_datasets** This folder contains generated composite datasets in PRIMAP2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year). As the repository is in the process of being set up, there currently is no data available.
* **legacy_data** This folder holds all extracted datasets in PRIMAP2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>\_\<term\>\_\<extra\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996, and *\<extra\>* is a free identifier to distinguish several files for the same submission (in some cases data for e.g. fluorinated gases are in a separate file). This folder also holds data where the code or some input files are not publicly available. Our aim is to reduce data in this folder to zero and to create fully open source processes for all datasets such that they can be included in the main folder.

## Datalad etc
```{include} ../../README.md
:start-after: <!--- sec-begin-datalad -->
:end-before: <!--- sec-end-datalad -->
```

## Data storage

## UNFCCC downloader

## Individual submission reader

## CRF reader

## DI reader