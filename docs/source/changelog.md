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
