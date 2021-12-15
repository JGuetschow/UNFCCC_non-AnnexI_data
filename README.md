# Collaborative UNFCCC non-AnnexI dataset
Currently under initial development and not meant for wider use.

## Description
### Structure
The repository is structured by folders

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (folder *BUR*) an automatical dowloaded exists. For National Communications (folder *NC*) it is under development. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC TODO: folder structure has chnaged. fix the text here
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC.
* **extracted_data** This folder holds all extracted datasets in primap2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: \<iso\>\_\<rep\>\_\<year\> where \<iso\> is the countries 3 letter iso code, \<rep\> is the repor, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), and \<year\> is the year of publication.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed suubmissions or subsets (e.g. all first BURs) and code to generate composite datasets. TODO: subfolder structure
* **composite_datasets** This folder contains generated composite datasets in primap2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year)

## Usage
This guide is for contributors. If you are solely interested in using the resulting data we refer to the relases of the data on zenodo which come with a DOI and are thus citeable.

This repository is not a pure git repository. It is a datalad repository which uses git for code and other small text files and git-annex for data files and binary files (for this repository mainly pdf files). The files stored in git-annex are not part of this repository but are stored in a gin repository at *https://gin.hemio.de/jguetschow/UNFCCC_non-AnnexI_data/*.

To use the repository you need to have datalad installed.
to clone the repository you can use the github url, but also the gin url.

`datalad clone git@github.com:JGuetschow/UNFCCC_non-AnnexI_data.git <directory_name>
`
clones the repository into the folder \<directory_name\>. You can also clone via `git clone`. This avoids error messages regarding git-annex. Cloning works from any sibling.



* requirements: requirements.txt, venv, firefox-geckodriver
* explain datalad, gin

### Update BUR and NC submissions
To update BUR and NC submissions first make sure your branch is in sync with `main` to avoid conflict when merging your branch later. To update the list of submissions run `make update-bur` in the main project folder. This will create a new list of submissions. To actually download the files run `make download-bur`  


## Contributing
The idea behind this data package is that several people contribute to extracting the data from pdf files such that for each user the work is less than for individual data reading and in the same time data quality improves through institutionalized data checking.

* use forks,
* use structure
* consider data requirements (see below)

### What data should be read

minimal requirements for use cases
* for PRIMAP-hist
* for FAOSTAT
