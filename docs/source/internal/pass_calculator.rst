===============
Pass Calculator
===============

A common module for RADS and ULTRA to use to calculate orbital pass for a
location on Earth. Uses Skyfield (https://rhodesmill.org/skyfield/) to
calculate passes from a TLE (two-line element) and LatLong coordinates.

.. autofunction:: pass_calculator.calculator.get_all_passes

.. autofunction:: pass_calculator.calculator.pass_overlap

.. autoclass:: pass_calculator.orbitalpass.OrbitalPass
   :members:

