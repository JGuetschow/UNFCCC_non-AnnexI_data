# Changelog

Versions follow [Semantic Versioning](https://semver.org/) (`<major>.<minor>.<patch>`).

Backward incompatible (breaking) changes will only be introduced in major versions
with advance notice in the **Deprecations** section of releases.


<!--
You should *NOT* be adding new changelog entries to this file, this
file is managed by towncrier. See changelog/README.md.

You *may* edit previous changelogs to fix problems like typo corrections or such.
To add a new changelog entry, please see
https://pip.pypa.io/en/latest/development/contributing/#news-entries,
noting that we use the `changelog` directory instead of news, md instead
of rst and use slightly different categories.
-->

<!-- towncrier release notes start -->

## unfccc-ghg-data 1.1.0 (2026-09-28)

### Improvements

- Added category for data updates in towncrier configuration. ([#155](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/155))
- Allow for `sel` in `basket_copy` in the `process_data_for_country` function
  Small changes to country list (add Taiwan and make `additional_territories` visible) ([#168](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/168))

### Bug Fixes

- Fixed bug in unfccc update functions (old downloads were not saved when running with `only_new` parameter) ([#147](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/147))
- Fixed a bug in `get_info_from_crf_filename`. Now version info in CRF files is checked for the correct format so files are detected correctly. ([#168](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/168))

### Improved Documentation

- Updated docs with new data reading scripts ([#168](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/168))
- regenerated docs ([#179](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/179))

### Data Update

- * Update submission lists
  * read KOR and TWN 2025 inventories
  * Read CRT1 for KOR, MNG, TUR, ROU, ZWE

  ([#146](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/146))
- Updated specifications and read data for CRTAI 2026. Countries Australia, Austria, Belgium, Bulgaria, Belarus, Canada, SwitzerlandCyprus, Czechia, Germany, Denmark, Spain, Estonia, Finland, France, United Kingdom, Greece, Croatia, Hungary, Ireland, Iceland, Italy, Japan, Liechtenstein, Lithuania, Luxembourg, Latvia, Monaco, Malta, Netherlands,  New Zealand, Portugal, Roumania, Slovakia, Slovenia, Turkey, Ukraine. ([#155](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/155))
- Read CRT data from India's BTR1 and Honduras' BTR1
  Read Bangladesh BTR1 data from pdf
  Read USA data from non-official inventory
  Read Tuvalu's and Zambia's BTR1 from CRT files ([#168](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/168))
- Added first BTR2 submissions (Australia, Austria, Belgium, Belarus, Canada, Switzerland,
  Cyprus, Czechia, Denmark, Spain, Estonia, Finland, France, United Kingdom, Greece,
  Croatia, Hungary, Ireland, Iceland, Italy, Japan, Kazakhstan, Liechtenstein, Lithuania,
  Luxembourg, Latvia, Netherlands, Norway, New Zealand, Poland, Romania , Slovakia, Slovenia,
  Sweden, Turkey, Ukraine).
  Most BTR2 submissions are identical to the 2026 National Inventory Submissions. ([#173](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/173))
- Mexico 2026 Inventory
  Indonesia NC4
  Bosnia and Herzegovina BTR1
  Democratic Republic of the Congo BUR1
  Botswana BTR/CRT1
  Liberia BTR/CRT1
  Seychelles BTR/CRT1
  Dominican Republic BTR/CRT1
  Qatar BTR/CRT1
  Kyrgyzstan BTR/CRT1
  re-read USA 2026 inventory
  Re-read Korea 2025 inventory
  re-read Bangladesh BTR1
  re-read Saint Kitts and Nevis BUR1 ([#179](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/179))
- Data for Russia; updates for Croatia, Iceland, Japan, Switzerland; re-uploads (same version number) for Canada, Czechia, Finland, Portugal ([#180](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/180))
- Added BTR/CRT2 data for Colombia and Croatia.
  Updated BTR2 and CRTAI2026 submission lists ([#187](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/187))


## unfccc-ghg-data 1.0.0 (2026-04-28)

### Features

- Add BTR data submitted in CRT format for several countries ([#141](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/141))
- New semi-automatic release process. ([#161](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/161))

### Improvements

- Update CRT reading functions with better debug output and some flexibility improvements for special cases ([#141](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/141))
- * Now use python 3.12
  * Update packages
  * Fix CI including downloading of data files using datalad

  ([#142](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/142))
- * Update submission lists
  * read KOR and TWN 2025 inventories
  * Read CRT1 for KOR, MNG, TUR, ROU, ZWE

  ([#146](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/146))
- * Read IRQ BUR1
  * Code to read Democratic Republic of the Congo BUR1 (partial as inconsistent)

  ([#147](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/147))
- * Add CRT AI 2026 specifications
  * Read CRT AI 2026 for Poland, Norway, Sweden

  ([#153](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/153))

### Bug Fixes

- All exceptions are now logged in CRF/CRT reading functions. closes #124 ([#141](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/141))
- Fixed typo in `release.yaml`
  Updated github actions to latest versions ([#162](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/162))
- Fixed a wrong reference to uv in `release.yaml` ([#163](https://github.com/JGuetschow/UNFCCC_non-AnnexI_data/pulls/163))
