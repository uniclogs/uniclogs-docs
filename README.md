# UniClOGS

[![License](https://img.shields.io/github/license/oresat/uniclogs-software)](./LICENSE)
[![Trello](https://img.shields.io/badge/trello-Backlog-blue)](https://trello.com/b/9VBVWS2I/mission-server-capstone)
[![Git Actions](https://img.shields.io/github/workflow/status/oresat/uniclogs-software/Mission%20Server)](https://github.com/oresat/uniclogs-software/actions)
[![Issues](https://img.shields.io/github/issues/oresat/uniclogs-software)](https://github.com/oresat/uniclogs-software/issues)

***

![UniClOGS Logo](https://github.com/oresat/uniclogs/raw/master/uniclogs.png "UniClOGS")

***

## Cloning this repo
- `git clone --recursive https://github.com/oresat/uniclogs-software`

## Components
* `/cosmos`: Tools and misc pipeline utilities for interfacing with UniClOGS
* `/cosi`: Cosmos-Satnogs Interface: Daemon for fetching telemetry and TLEs
* `/pass_calculator`: Interface for calculating orbits from TLEs
* `/rads`: Request Approve/Deny Service
* `/stationd`: Daemon for UDP power management
* `/ultra`: UniClOGS Live Telemetry and Request API: ReSTful API for telemetry and requests

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

#### TLE Checksum Validation

See [this script](./tle-validate-checksum.py) for validating the provisional TLE checksum.

The number at the end of each line element is simply the sum of all the numeric numbers, `-` characters are interpreted as 1.
