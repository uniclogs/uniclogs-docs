# UniClOGS
![Build](https://github.com/oresat/uniclogs-software/workflows/Mission%20Server/badge.svg)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

![UniClOGS](https://github.com/oresat/uniclogs/raw/master/uniclogs.png "UniClOGS")

## Components
* `/stationd`: UDP Power Management Daemon
* `/cosmos`: Interface with internal UniClOGS tools and misc data pipeline utilities

## Documentation
- Install sphinx and sphinx theme: `pip install -r docs/source/requirements.txt`
- Make sphinx html:
    - `cd docs`
    - `make clean html`
