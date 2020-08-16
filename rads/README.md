# RADS (Request Approve / Deny Service)

## Dependencies
- Install the pass calculator
- `$ pip install -r requirements.txt`

## Build pip package
`$ python3 setup.py bdist_wheel`

## Installation
`$ python3 -m pip install dist/rads*.whl` 

## Run
local:
    - `$ python3 -m rads`
pip package:
    - `$ rads`
