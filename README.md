# Collaborative UNFCCC non-AnnexI dataset
This repository aims to organize a collective effort to bring GHG emissions and related data submitted by developing countries (non-AnnexI) to the UNFCCC into a standardized machine readable format. We focus on data not available through the [UNFCCC DI interface](https://di.unfccc.int/) which is mostly data submitted in IPCC 2006 categories.

The code is based on [national-inventory-submissions](https://github.com/openclimatedata/national-inventory-submisions)


**The repository is currently under initial development so a lot of things are still subject to change.**

## Description
### Repository structure
The repository is structured by folders. Here we list the folders in order of processing.

* **downloaded_data** This folder contains data downloaded from the UNFCCC website and other sources. For Biannual Update Reports (BUR), national Communications (NC), and Nationally Determined Contributions (NDC) an automatical dowloaded exists (folder UNFCCC). Within the UNFCCC folder the data is organized in a *\<country\>/\<submission\>* structure. NDC submissions are often revised. To be able to keep track of the targets and emissions inventories we store each NDC revision in a time-stamped folder. The *non-UNFCCC* folder contains official country inventories not (yet) submitted to the UNFCCC. The internal structure is the same as for the UNFCCC folder.
* **analyzed_submissions** Here we collect all files needed to extract data from submissions. Subfolders are countries (use the same names as in the *downloaded data* folder) and within the country folders each submission / report should have it's own subfolder, e.g. *Argentina/BUR1*. National Inventory Reports (NIR) are submitted together with BURs or NCs and have no individual folder but are used as additional inputs to their BUR or NC. As the repository is in the process of being set up, there currently is no data available.
* **extracted_data** This folder holds all extracted datasets in PRIMAP2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>_\<term\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, and *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996. As the repository is in the process of being set up, there currently is no data available.
* **code** Code that is used for several countries / reports, but not (yet) part of the primap2 package. This folder also contains scripts that automate data reading for all analyzed submissions or subsets (e.g. all first BURs) and code to generate composite datasets. Currently the only subfolder is the *UNFCCC_downloader* where code to automatically download BUR and NC submission files from the [UNFCCC website](https://www.unfccc.int) resides.
* **composite_datasets** This folder contains generated composite datasets in PRIMAP2 interchnage format. Each dataset has it's own subfolder which should contain a dataset name, a version, and publication date (e.g. year). As the repository is in the process of being set up, there currently is no data available.
* **legacy_data** This folder holds all extracted datasets in PRIMAP2 interchange format. The datasets are organized in country subfolders. The naming convention for the datasets is the following: *\<iso\>\_\<sub\>\_\<year\>\_\<term\>\_\<extra\>* where *\<iso\>* is the countries 3 letter iso code, *\<sub\>* is the submissions, e.g. **BUR1**, **NC5**, or **inventory2020** (for a non-UNFCCC inventory), *\<year\>* is the year of publication, *\<term\>* is the main sector terminology e.g. IPCC2006 or IPCC1996, and *\<extra\>* is a free identifier to distinguish several files for the same submission (in some cases data for e.g. fluorinated gases are in a separate file). This folder also holds data where the code or some input files are not publicly available. Our aim is to reduce data in this folder to zero and to create fully open source processes for all datasets such that they can be included in the main folder.

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
This guide is mostly targeted at contributors. If you are solely interested in using the resulting data the easiest way to get the data is to use the relases of the data on zenodo which come with a DOI and are thus citeable. If you need the most recent data and do not want to wait for the releases, you can use the setup described below.

### Clone and set up the repository
This repository is not a pure git repository. It is a datalad repository which uses git for code and other small text files and git-annex for data files and binary files (for this repository mainly pdf files). Datalad uses the concept of *siblings* which are clones of the original repository. However, only the metadata is available in all siblings, the actual data which is stored in git-annex might only be available from some siblings. Here, we have a gin repository at [gin.hemio.de](https://gin.hemio.de/jguetschow/UNFCCC_non-AnnexI_data/) which contains all metadata and data as the main sibling we're working with. It is also set up as a *common data source* which can be accessed by everyone without a github or gin.hemio.de account.

To use the repository you need to have datalad installed. To clone the repository you can use the github url, but also the gin url.

`datalad clone git@github.com:JGuetschow/UNFCCC_non-AnnexI_data.git <directory_name>`

or

`datalad clone git@gin.hemio.de:/jguetschow/UNFCCC_non-AnnexI_data.git <directory_name>`

clones the repository into the folder *\<directory_name\>*. You can also clone via `git clone`. This avoids error messages regarding git-annex. Cloning works from any sibling. If you plan to contribute to the repository you will need to push to gin and for that you need an account. Currently you cannot create an account yourself, so please contact the maintainers to obtain an account. If you are just interested in using the data you can wither clone from github, or from gin via https:

`datalad clone https://gin.hemio.de:/jguetschow/UNFCCC_non-AnnexI_data.git <directory_name>`

The data itself (meaning all binary and csv files) are not downloaded automatically. Only symlinks are created on clone. Needed files can be obtained using

`datalad get <filename>`

where \<filename\> can also be a folder to get all files within that folder. Datalad will look for a sibling that is accessible to you and provides the necessary data. In general that could also be the computer of another contributor, if that computer is accessible to you (which will normally not be the case). **NOTE: If you push to the github repository using datalad your local clone will automatically become a sibling and if your machine is accessible from the outside it will also serve data to others.**

For more detailed information on datalad we refer to the [datalad handbook](http://handbook.datalad.org/en/latest/index.html)

The code is best run in a virtual environment. All python dependencies will be automatically installed when building the virtual environment using `make venv`. If you don't want to use a virtual environment you can find the dependencies in file `code/requirements.txt`. As an external dependencies you need *firefox-geckodriver* and *git-annex \> XXX (2021 works, some 2020 versions also)*.

The code has not been tested under Windows and Mac OS.

### Update BUR, NC, and NDC submissions
The maintainers of this repository will update the list of submissions and the downloaded pdf files frequently. However, in some cases you might want to have the data early and do the download yourself. To avoid merge conflicts, please do this on a clean branch in your fork and make sure your branch is in sync with `main`.

* **BUR**: To update the list of submissions run `make update-bur` in the main project folder. This will create a new list of submissions. To actually download the files run `make download-bur`.
* **NC**: To update the list of submissions run `make update-nc` in the main project folder. This will create a new list of submissions. To actually download the files run `make download-nc`.
* **NDC**: For the NDC submissions we use the list published in [openclimatedata/ndcs](https://github.com/openclimatedata/ndcs) which receives daily updates. To  download the files run `make download-ndc`.

All download scripts create files listing the new downloads in the folder *downloaded_data/UNFCCC*. the filenames use the format *00\_new\_downloads\_\<type\>-YYYY-MM-DD.csv* where *\<type\>* is *bur*, *nc*, or *ndc*. Currently, only one file per type and day is stored, so if you run the download script more than once on a day you will overwrite your first file (likely with an empty file as you have already downloaded everything) (see also [issue #2](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/issues/2)).

All new submissions have to be added to country discussion pages (where they exist) so everyone can keep track of all submissions without having to check the data folder for updates.

### Adding new datasets
See section [Contributing] below.


## Contributing
The idea behind this data package is that several people contribute to extracting the data from pdf files such that for each user the work is less than for individual data reading and in the same time data quality improves through institutionalized data checking. You can contribute in different ways. Please also read the [Technical HowTo for contributors] at the end of this section.

### Check and propose submissions
The easiest way to contribute to the repository is via analysis of submissions for data coverage. Before selecting a submission for analysis check that it is not yet listed as analyzed in the submission overview issues.

### Organize machine readable data
We usually read the data from the pdf submissions. However, the authors of the submission of course have the data in machine readable format. It's of great help for the data reading process if the data is available in machine readable format as it minimizes errors and is just much less work compared to pdf reading. So if you have good connections to authors of country submissions or the underlying data asking them to publish the data would be of great help. Publishing the data is the optimal solution as it allows us to integrate it in this dataset. If you can obtain the data unofficially it still helps as it would allow for easy checking of results read from pdfs. Datasets created from machine readable data not publicly available can be added to the *legacy\_data* folder.

### Read data
Read data from pdfs (or machine readable format) in a reproducable way. We read data using tools like [camelot](https://github.com/atlanhq/camelot). This enables a reproducable reading process where all parameters needed (page numbers, table boundaries etc) are defined in a script that reads the data from pdf and saves it in the PRIMAP2 interchange and native format. If you want to contribute through data reading, check out the country pages in the discussion section and the issues already created for submission selected for reading. If you start data reading for a submission please leave comment in the corresponding issue and issign the issue to yourself. If there is no issue for the submission, please add it using the template (TODO create issue template). When reading the data, please consider the data requirements when reading the data.

### Review data
You can contribute also through checking data. For each submission we would like to have one person responsible for reading the data and one person responsible for checking the results for completeness and correctness. Look out for issues with the tag "Needs review".


### Issues
There always issues open regarding coding, some of them easy to resolve, some harder.

### Your ideas
Contributing is ouf course not limited to the categories above. I you have ideas for improvements just open an issue or a discussion page to discuss you idea with the community.

### Technical HowTo for contributors
As we have a datalad repository using github and gin the process of contributing code and data is a bit different from pure git repositories. As the data is only stored on gin, the gin repository is the source to start from. As gin currently has a problem with forks (the annexed data is not forked) we have to use branches for development and thus to contribute you first need to contact the maintainers to get write access to the repository. You have to clone the repository using ssh to be able to push to it. For that you first need to store your public ssh key on the gin server (settings -> SSH Keys). Once you have that create a branch and work there. When you're done create a pull request to integrate your work into the main branch. We're still testing this setup and will add more detailed information in the process.

## What data should be read
Optimally, all data that can be found in a submission should be read (emissions data, but also underlying activity data and socioeconomic data). However, it is often scattered throughout the documents and sometimes only single datapoint are available. Thus we have compiled a list of use cases and their data requirements as a basis for decisions on what to focus on. Emissions data is often presented in a similar tabular format reapeated for each year. Simetimes sectoral time series are presented in tables for individual gases. If these cases it makes sense to read all the data as the tables have to be read anyways and omitting sectoral detail does not save much time.

Activity data needed depends on use case. We have listed some use cases and their requirements below.

* **PRIMAP-hist**: currently only emissions data is needed. In the future activity data and socioeconomic data might be needed as well. For sectors and gases we refer to the data description available on [zenodo](https://zenodo.org/record/5494497):
* **FAOSTAT**: FOSTAT uses only data for the AFOLU sector (AFOLU = Agriculture, Forestry, and Other Land Use). However activity data is needed in addition to emissions data. The used sectors and variables are listed in the [FAO to UNFCCC sector mapping document](https://fenixservices.fao.org/faostat/static/documents/GT/Mapping_to_UNFCCC_IPCC.pdf)
