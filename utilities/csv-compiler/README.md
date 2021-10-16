# CSV Compiler

This is a simple tool for taking a CSV generated from [Google Spreadsheet](https://docs.google.com/spreadsheets/d/1tZBbSD7xKchf7LZwK12a4GzSHn05jnL8AcgdDFdQSok) and converting it into a YAML format suitable for a Kaitai Struct configuration. See [the CoSSI Repo](https://github.com/oresat/uniclogs-cossi/tree/master/ksy) for example and production-level structures.

***

# Usage

##### Get the help menu:

`$` `./csv-compiler --help`

# Quick Start

##### Compile the CSV with the default target of `yml`

`$` `./csv-compiler ./oresat-packet-fields.csv`
