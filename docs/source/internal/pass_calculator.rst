===============
Pass Calculator
===============

A common module for RADS and ULTRA to use to calculate orbital pass for a
location on Earth. Uses Skyfield (https://rhodesmill.org/skyfield/) to
calculate passes from a TLE (two-line element) and LatLong coordinates.

.. automodule:: 
.. autofunction:: pass_calculator
.. autofunction:: pass_calculator.calculator.get_all_passes

.. autofunction:: pass_calculator.calculator.pass_overlap

.. autofunction:: pass_calculator.calculator.validate_pass

.. autoclass:: pass_calculator.orbitalpass.OrbitalPass
    :members:
    :special-members: __init__

