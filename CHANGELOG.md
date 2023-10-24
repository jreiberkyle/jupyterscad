# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- API documentation
- Full static typing, expanded file paths to support Path or str types.
- Full external documentation pages

### Fixed

- Grid was not aligned with origin for grid_unit != 1 (#11). Thank you @jeff-dh!
- README references to jupter_scad should be jupyterscad

## Changed

- OpenSCAD executable discovery now looks in PATH (which works for Linux) then
  in the macOS-specific install path if not found in PATH
- Rename render_stl out_file to outfile for positional arg to match other fcns

## [0.1.0] - 2023-10-01

### Added

- Changelog
- Workflows for testing PRs and publishing to testpypi/pypi and releasing

### Changed

- package files moved to src/ directory for autodetection

## [0.0.1] - 2023-09-29

### Added

- render(), render_stl() and visualize_stl()
- README.md for docs
- LICENSE and COPYING for license
