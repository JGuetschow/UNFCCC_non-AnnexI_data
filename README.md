# Collaborative UNFCCC non-AnnexI dataset
Currently under initial development and not meant for wider use. code is based on [national-inventory-submissions](https://github.com/openclimatedata/national-inventory-submisions)

## Description
### Repository structure
The repository is structured by folders

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (BUR), national Communications (NC), and Nationally Determined Contributions (NDC) an automatical dowloaded exists (folder UNFCCC). Within the UNFCCC folder the data is organized in a *\<country\>/\<submission\>* structure. NDC submissions are often revised. To be able to keep track of the targets and emissions inventories we store each NDC revision in a time-stamped folder. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC. The internal structure is the same as for the UNFCCC folder.
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC. As the repository is in the process of being set up, there currently is no data available.
* **extracted_data** This folder holds all extracted datasets in primap2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>_\<term\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, and *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996. As the repository is in the process of being set up, there currently is no data available.
* **legacy_data** This folder holds all extracted datasets in primap2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>\_\<term\>\_\<extra\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996, and *\<extra\>* is a free identifier to distinguish several files for the same submission (in some cases data for e.g. fluorinated gases are in a seperate file). This folder also holds data where the code or some input files are not publicly available. Our aim is to reduce data in this folder to zero and to create fully open source processes for all datasets such that they can be included in the main folder.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed suubmissions or subsets (e.g. all first BURs) and code to generate composite datasets. Currently the only subfolder is the *UNFCCC_downloader* where code to automatically download BUR and NC submission files from the [UNFCCC website](https://www.unfccc.int) resides.
* **composite_datasets** This folder contains generated composite datasets in primap2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year). As the repository is in the process of being set up, there currently is no data available.


### Data format description (columns)

All data in this repository in the comma-separated values (CSV) files is formatted consistently with the PRIMAP2 interchange format.

The data contained in each column is as follows:

#### "source"
Name of the data source. Four country specific datasets it is `\<ISO3\>-GHG-inventory`, where `\<ISO3\>` is the ISO 3166 three-letter country code. Specifications for composite datasets including several countries will be added when the datasets are available.

#### "scenario (PRIMAP)"

The scenario specifies the submissions (e.g. BUR1, NC5, or Inventory_2021 for a non-UNFCCC inventory)

#### "provenance"
Provenance of the data. Here: "derived" as it is a composite source.

#### "country (ISO3)"
ISO 3166 three-letter country codes.

#### "entity"
Gas categories using global warming potentials (GWP) from either Second Assessment Report (SAR) or Fourth Assessment Report (AR4).

Code                     Description
----                     -----------
CH4                      Methane
CO2                      Carbon Dioxide
N2O                      Nitrous Oxide
HFCS (SARGWP100)         Hydrofluorocarbons (SAR)
HFCS (AR4GWP100)         Hydrofluorocarbons (AR4)
PFCS (SARGWP100)         Perfluorocarbons (SAR)
PFCS (AR4GWP100)         Perfluorocarbons (AR4)
SF6                      Sulfur Hexafluoride
NF3                      Nitrogen Trifluoride
FGASES (SARGWP100)       Fluorinated Gases (SAR): HFCs, PFCs, SF$_6$, NF$_3$
FGASES (AR4GWP100)       Fluorinated Gases (AR4): HFCs, PFCs, SF$_6$, NF$_3$
KYOTOGHG (SARGWP100)     Kyoto greenhouse gases (SAR)
KYOTOGHGAR4 (AR4GWP100)  Kyoto greenhouse gases (AR4)

Table: Gas categories and underlying global warming potentials


#### "unit"
Units are of the form *Gg/Mt/... \<substance\> / yr* where substance is the entity or for CO$_2$ equivalent units *Gg/Mt/... CO2 / yr*. The CO$_2$-equivalent is calculated according to the global warming potential indicated by the entity (see above).


#### "category (\<term\>)"
Categories for emission as defined in terminology \<term\>. Terminology names are those used in the [climate_categories](https://github.com/pik-primap/climate_categories) package. If the terminology name contains *\_PRIMAP* is means that some (sub)categories have been added to the official IPCC category hierarchy. Added categories outside the hierarchy begin with the prefix *M*.

#### "CategoryName"
Original name of the category as presented in the submission.

#### "CategoryNameTranslation"
Optional column. In some cases original category names have been translated to english. In this case these translations are stored in this column. 

#### Remaining columns

Years (depending on dataset)



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

### Update BUR, NC, and NDC submissions
TODO: develop a method to avoid conflicts here. e.G. only a few maintainers commit the raw data and all others use that or if they need updated raw data only use that locally.

To update BUR, NC, and NDC submissions first make sure your branch is in sync with `main` to avoid conflict when merging your branch later. To update the list of submissions run `make update-bur` in the main project folder. This will create a new list of submissions. To actually download the files run `make download-bur`  


## Contributing
The idea behind this data package is that several people contribute to extracting the data from pdf files such that for each user the work is less than for individual data reading and in the same time data quality improves through institutionalized data checking.

* use forks,
* use structure
* consider data requirements (see below)

### What data should be read

minimal requirements for use cases
* for PRIMAP-hist
* for FAOSTAT
