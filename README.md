# UniClOGS

[![License](https://img.shields.io/github/license/oresat/uniclogs-software)](./LICENSE)
[![issues](https://img.shields.io/github/issues/oresat/uniclogs-software/bug)](https://github.com/oresat/uniclogs-software/labels/bug)
[![docs](https://img.shields.io/readthedocs/uniclogs-software)](https://uniclogs-software.readthedocs.io)

***

![UniClOGS Logo](./images/gs-patch.png)

This is an umbrella repo, containing all of the various components, firmware, and software, and their respective separate repos.

Each repository is just a submodule. Checkout our [Read The Docs](https://uniclogs-software.readthedocs.io) page if you'd like a quick overview of the system as a whole. Or click on a git-submodule to follow it to its repo and it's own separate documentation, if you'd like to learn more about that particular submodule.

***

## Cloning this repo
- `git clone --recursive https://github.com/oresat/uniclogs-software`

## Project Documentation

This project uses Sphinx for documentation generation.

### Installation:
`$` `pip install -r docs/source/requirements.txt`

### Generate Docs:
`$` `cd docs`

`$` `make clean html`

### OreFLAT0

A development version of OreSAT0 is integrated into the SatNOGS network by the name `OREFLAT-0`.

A [provisional TLE](./oreflat0.tle) has been provided to mock the SatNOGS environment and provide necessary infrastructure for testing.
