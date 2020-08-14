# RADS (Request Approve / Deny Service)

## Dependencies

`$` `pip install -r requirements.txt`

## Build pip package

`$` `python3 setup.py bdist_wheel`

## Installation

**Local Install:**

`$` `python -m pip install dist/rads*.whl`

**Global Install:**

`$` `sudo python -m pip install dist/rads*.whl`

## Run

**Local: (user install)**

`$` `python3 -m rads`

**Global: (global install)**

`$` `rads`
