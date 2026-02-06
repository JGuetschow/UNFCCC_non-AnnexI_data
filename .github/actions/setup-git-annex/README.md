[![CI Status](https://github.com/jstritch/setup-git-annex/workflows/CI/badge.svg)](https://github.com/jstritch/setup-git-annex/actions)
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R8NY1ZK)
[![Liberapay](https://liberapay.com/assets/widgets/donate.svg)](https://liberapay.com/jstritch)
[![Patreon](https://img.shields.io/badge/Patreon-F96854?style=for-the-badge&logo=patreon&logoColor=white)](https://www.patreon.com/jstritch)

# setup-git-annex

Installs git-annex on Linux, macOS, or Windows.
[git-annex](https://git-annex.branchable.com/) is an integrated alternative to storing large files in Git.

## Example

The workflow snippet shown below installs git-annex on Linux, macOS, and Windows.
Setting fail-fast to false allows other jobs in the matrix to continue if any job in the matrix fails.

Once installed, the help command is invoked to demonstrate git-annex is available from the command line.

```yaml
jobs:
  test:

    strategy:
      matrix:
        os:
          - ubuntu-latest
          - macos-latest
          - windows-latest
      fail-fast: false

    runs-on: ${{ matrix.os }}

    steps:
      - uses: actions/checkout@v4
      - uses: jstritch/setup-git-annex@v1
      - run: git annex help
```
