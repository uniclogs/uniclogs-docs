# Pass Calculator

A common python module for calculating orbital passes used by ULTRA and RADS.
Mostly a simple wrapper ontop of [skyfield].

## Install Dependencies

`$` `pip install -r requirements.txt`

## Build
`$` `python3 setup.py bdist_wheel`

## Installation

**Install for single-user:**

`$` `python -m pip install dist/pass_calculator-*-py3-none-any.whl`


**Install globally:**

`$` `sudo python -m pip install dist/pass_calculator-*-py3-none-any.whl`

[skyfield]:https://rhodesmill.org/skyfield/
