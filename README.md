# UniClOGS

[![License](https://img.shields.io/github/license/oresat/uniclogs-software)](./LICENSE)
[![Trello](https://img.shields.io/badge/trello-Backlog-blue)](https://trello.com/b/9VBVWS2I/mission-server-capstone)
[![Git Actions](https://img.shields.io/github/workflow/status/oresat/uniclogs-software/Mission%20Server)](https://github.com/oresat/uniclogs-software/actions)
[![Issues](https://img.shields.io/github/issues/oresat/uniclogs-software)](https://github.com/oresat/uniclogs-software/issues)

***

![UniClOGS Logo](https://github.com/oresat/uniclogs/raw/master/uniclogs.png "UniClOGS")

***

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
