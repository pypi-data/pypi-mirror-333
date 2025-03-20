<!--
SPDX-FileCopyrightText: Peter Pentchev <roam@ringlet.net>
SPDX-License-Identifier: BSD-2-Clause
-->

# Changelog

All notable changes to the uvoxen project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2025-03-12

### Additions

- Define configuration format 0.2:
    - add the `tool.uvoxen.build-project` boolean field for projects that are
      not really Python libraries and `uv --install-project` is irrelevant
- Add the `--diff` option to `req generate` and `tox generate` in check-only mode.
- Belatedly declare the `req-generate` feature at version 0.1.

### Fixes

- Add the version 0.1.0 changelog entry to this file.

## [0.1.0] - 2025-03-08

### Started

- First public release.

[Unreleased]: https://gitlab.com/ppentchev/uvoxen/-/compare/release%2F0.1.1...main
[0.1.1]: https://gitlab.com/ppentchev/uvoxen/-/compare/release%2F0.1.0...release%2F0.1.1
[0.1.0]: https://gitlab.com/ppentchev/uvoxen/-/tags/release%2F0.1.0
