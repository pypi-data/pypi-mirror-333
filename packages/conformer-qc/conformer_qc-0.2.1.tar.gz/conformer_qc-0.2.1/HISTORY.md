<!--
Copyright 2018-2025 Fragment Contributors
SPDX-License-Identifier: Apache-2.0
-->
# Release and Feature History

## v0.2.1 (pending)

* Fixes bug in SystemRecords where noncanon matrix properties could be added to the DB
* Adds migration `migration_20250311_232937` to fix common bad matrix properties in existing projects

## v0.2.0

* Adds query and search features with the `conformer.search` module
* Improvements to PDB file reader
    * Charges are now read from PDB files
    * More metadata is saved from PDB files
* Update `visualize` package to show selections
* Bug fixes and validation for `spatial` package