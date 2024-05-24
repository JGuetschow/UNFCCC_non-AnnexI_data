# Country greenhouse gas data submitted to the UNFCCC
This repository aims to organize a collective effort to bring GHG emissions and related data submitted by developing countries (non-AnnexI) to the UNFCCC into a standardized machine readable format. We focus on data not available through the [UNFCCC DI interface](https://di.unfccc.int/) which is mostly data submitted in IPCC 2006 categories.

<!--- sec-begin-description -->

Reading country greenhouse gas data submitted to the United Nations Framework Convention on Climate Change (UNFCCC)in different submissions and formats and providing it in a standadized nc and csv format compatible with primap2. Data are read using different methods from APIs, xlsx and csv files as well as pdf files.



[![CI](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/actions/workflows/ci.yaml/badge.svg?branch=main)](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/actions/workflows/ci.yaml)
[![Coverage](https://codecov.io/gh/JGuetschow/UNFCCC_non-AnnexI_data/branch/main/graph/badge.svg)](https://codecov.io/gh/JGuetschow/UNFCCC_non-AnnexI_data)
[![Docs](https://readthedocs.org/projects/unfccc-ghg-data/badge/?version=latest)](https://unfccc-ghg-data.readthedocs.io)

**PyPI :**
[![PyPI](https://img.shields.io/pypi/v/unfccc-ghg-data.svg)](https://pypi.org/project/unfccc-ghg-data/)
[![PyPI: Supported Python versions](https://img.shields.io/pypi/pyversions/unfccc-ghg-data.svg)](https://pypi.org/project/unfccc-ghg-data/)
[![PyPI install](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/actions/workflows/install.yaml/badge.svg?branch=main)](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/actions/workflows/install.yaml)

**Other info :**
[![Licence](https://img.shields.io/github/license/JGuetschow/UNFCCC_non-AnnexI_data.svg)](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/blob/main/LICENCE)
[![Last Commit](https://img.shields.io/github/last-commit/JGuetschow/UNFCCC_non-AnnexI_data.svg)](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/commits/main)
[![Contributors](https://img.shields.io/github/contributors/JGuetschow/UNFCCC_non-AnnexI_data.svg)](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/graphs/contributors)


<!--- sec-end-description -->

Full documentation can be found at:
[unfccc-ghg-data.readthedocs.io](https://unfccc-ghg-data.readthedocs.io/en/latest/).
We recommend reading the docs there because the internal documentation links
don't render correctly on GitHub's viewer.

## Installation

<!--- sec-begin-installation -->

Country greenhouse gas data submitted to the UNFCCC can be installed with pip, mamba or conda:

```bash
pip install unfccc-ghg-data
mamba install -c conda-forge unfccc-ghg-data
conda install -c conda-forge unfccc-ghg-data
```

Additional dependencies can be installed using

```bash
# To add plotting dependencies
pip install unfccc-ghg-data[plots]

# If you are installing with conda, we recommend
# installing the extras by hand because there is no stable
# solution yet (issue here: https://github.com/conda/conda/issues/7502)
```

<!--- sec-end-installation -->

### For developers

<!--- sec-begin-installation-dev -->

For development, we rely on [poetry](https://python-poetry.org) for all our
dependency management. To get started, you will need to make sure that poetry
is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

For all of work, we use our `Makefile`.
You can read the instructions out and run the commands by hand if you wish,
but we generally discourage this because it can be error prone.
In order to create your environment, run `make virtual-environment`.

If there are any issues, the messages from the `Makefile` should guide you
through. If not, please raise an issue in the
[issue tracker](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/issues).

For the rest of our developer docs, please see [](development-reference).

<!--- sec-end-installation-dev -->


TODO: old README below. reorganize into proper docs.

The code for downloading submissions is based on [national-inventory-submissions](https://github.com/openclimatedata/national-inventory-submisions)


**The repository is currently under initial development so a lot of things are still subject to change.**

## Description





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

* **BUR**: To update the list of submissions run `poetry run doit update_bur` in the main project folder. This will create a new list of submissions. To actually download the files run `poetry run doit  download_bur`.
* **NC**: To update the list of submissions run `poetry run doit update_nc` in the main project folder. This will create a new list of submissions. To actually download the files run `poetry run doit download_nc`.
* **NDC**: For the NDC submissions we use the list published in [openclimatedata/ndcs](https://github.com/openclimatedata/ndcs) which receives daily updates. To  download the files run `poetry run doit download_ndc` (currently not working due to a data format change).

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


<!--- sec-begin-datalad -->

## DataLad datasets and how to use them

This repository is a [DataLad](https://www.datalad.org/) dataset
(id: 4d062170-604c-4efd-afbf-5ce7f97e0e63). It provides
fine-grained data access down to the level of individual files, and allows for
tracking future updates. In order to use this repository for data retrieval,
[DataLad](https://www.datalad.org/) is required. It is a free and open source
command line tool, available for all major operating systems, and builds up on
Git and [git-annex](https://git-annex.branchable.com/) to allow sharing,
synchronizing, and version controlling collections of large files.

More information on how to install DataLad and
[how to install](http://handbook.datalad.org/en/latest/intro/installation.html)
it can be found in the
[DataLad Handbook](https://handbook.datalad.org/en/latest/index.html).

### Get the dataset

A DataLad dataset can be `cloned` by running

```
datalad clone <url>
```

Once a dataset is cloned, it is a light-weight directory on your local machine.
At this point, it contains only small metadata and information on the identity
of the files in the dataset, but not actual *content* of the (sometimes large)
data files.

### Retrieve dataset content

After cloning a dataset, you can retrieve file contents by running

```
datalad get <path/to/directory/or/file>
```

This command will trigger a download of the files, directories, or subdatasets
you have specified.

DataLad datasets can contain other datasets, so called *subdatasets*.  If you
clone the top-level dataset, subdatasets do not yet contain metadata and
information on the identity of files, but appear to be empty directories. In
order to retrieve file availability metadata in subdatasets, run

```
datalad get -n <path/to/subdataset>
```

Afterwards, you can browse the retrieved metadata to find out about subdataset
contents, and retrieve individual files with `datalad get`.  If you use
`datalad get <path/to/subdataset>`, all contents of the subdataset will be
downloaded at once.

### Stay up-to-date

DataLad datasets can be updated. The command `datalad update` will *fetch*
updates and store them on a different branch (by default
`remotes/origin/master`). Running

```
datalad update --merge
```

will *pull* available updates and integrate them in one go.

### Find out what has been done

DataLad datasets contain their history in the ``git log``.  By running ``git
log`` (or a tool that displays Git history) in the dataset or on specific
files, you can find out what has been done to the dataset or to individual
files by whom, and when.

<!--- sec-end-datalad -->
