# Collaborative UNFCCC non-AnnexI dataset
Currently under initial development and not meant for wider use. code is based on [national-inventory-submissions](https://github.com/openclimatedata/national-inventory-submisions)

## Description
### Structure
The repository is structured by folders

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (BUR) and national Communications (NC) an automatical dowloaded exists (folder UNFCCC). Within the UNFCCC folder the data is organized in a *\<country\>/\<submission\>* structure. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC. The internal structure is the same as for the UNFCCC folder.
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC. As the repository is in the process of being set up, there currently is no data available.
* **extracted_data** This folder holds all extracted datasets in primap2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), and *\<year\>* is the year of publication. As the repository is in the process of being set up, there currently is no data available.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed suubmissions or subsets (e.g. all first BURs) and code to generate composite datasets. Currently the only subfolder is the *UNFCCC_downloader* where code to automatically download BUR and NC submission files from the [UNFCCC website](https://www.unfccc.int) resides.
* **composite_datasets** This folder contains generated composite datasets in primap2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year). As the repository is in the process of being set up, there currently is no data available.

## Usage
This guide is for contributors. If you are solely interested in using the resulting data we refer to the relases of the data on zenodo which come with a DOI and are thus citeable.

### Clone and set up the repository
This repository is not a pure git repository. It is a datalad repository which uses git for code and other small text files and git-annex for data files and binary files (for this repository mainly pdf files). The files stored in git-annex are not part of this repository but are stored in a gin repository at [gin.hemio.de](https://gin.hemio.de/jguetschow/UNFCCC_non-AnnexI_data/).

To use the repository you need to have datalad installed.
to clone the repository you can use the github url, but also the gin url.

`datalad clone git@github.com:JGuetschow/UNFCCC_non-AnnexI_data.git <directory_name>
`
clones the repository into the folder *\<directory_name\>*. You can also clone via `git clone`. This avoids error messages regarding git-annex. Cloning works from any sibling.

The data itself (meaning all binary files) is not downloaded automatically. Only simlinks are created on clone. Needed files can be obained using

`datalad get <filename>`

where \<filename\> can also be a folder to get all files within that folder. Datalad will look for a sibling that is accessible to you and provides the necessary data. In general that could also be the computer of another contributor, if that computer is accessible to you (which will normally not be the case). **NOTE: If you push to the github repository using dtalad your local clone will automatically become a sibling and of your machine is accessible from the outside it will also serve dat

For more detailed information on datalad we refer to the [datalad handbook](http://handbook.datalad.org/en/latest/index.html)

The code is best run in a virtual environment. All python dependencies will be automatically installed when building the virtual environment using `make venv`. If you don't wat to use a virtual environment you can find the dependencies in file `code/requirements.txt`. As an external dependencies you need *firefox-geckodriver* and *git-annex \> XXX (2021 works, some 2020 versions also)*.

The code has not been tested under Windows and Mac OS.

* requirements: requirements.txt, venv, firefox-geckodriver
* explain datalad, gin

### Update BUR and NC submissions
TODO: develop a method to avoid conflicts here. e.G. only a few maintainers commit the raw data and all others use that or if they need updated raw data only use that locally.

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
