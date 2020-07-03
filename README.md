# UniClOGS
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Foresat%2Funiclogs-software%2Fbadge%3Fref%3Dcapstone-dev&style=flat)](https://actions-badge.atrox.dev/oresat/uniclogs-software/goto?ref=capstone-dev)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![alt text](https://github.com/oresat/uniclogs/raw/master/uniclogs.png "UniClOGS")

## Components
* `/stationd`: UDP Power Management Daemon
* `/cosmos`: Interface with internal UniClOGS tools and misc data pipeline utilities

## Documentation
- Install sphinx and sphinx theme: `pip install -r docs/source/requirements.txt`
- Make sphinx html:
    - `cd docs`
    - `make clean html`
