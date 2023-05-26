.. currentmodule:: geocat.viz

.. _release:
Release Notes
=============

v2023.06.0 (Jun 1, 2023)
-------------------------

Function and keyword argument names have been adjusted to follow consistent formatting and style, and one bug fix.

Deprecations
^^^^^^^^^^^^
* Some functions reanmed (``findLocalExtrema`` -> ``find_local_extrema``, ``plotCLabels`` -> ``plot_contour_labels``, and ``plotELabels`` -> ``plot_extrema_labels``) and keyword arguments renamed in ``get_skewt_vars`` by `Julia Kent`_ in (:pr:`127`)

Bug Fixes
^^^^^^^^^
* Bug in ``truncate_colormap`` fixed by `Katelyn Fitzgerald`_ (:pr:`125`)

v2023.05.0 (May 4, 2023)
-------------------------

Management of this package switched to GeoCAT team members `Julia Kent`_ and `Katelyn Fitzgerald`_.

New Features
^^^^^^^^^^^^
* Pressure-height twin axis function `add_height_from_pressure_axis` by `Julia Kent`_ in (:pr:`114`)

Documentation
^^^^^^^^^^^^^
* Contributor's Guide updated by `Julia Kent`_ in (:pr:`115`)
* Documentation and Packaging Overhaul to match GeoCat-Comp style by `Julia Kent`_ in (:pr:`116`), (:pr:`121`)
* Adding examples links to all functions by `Julia Kent`_ in (:pr:`122`)

..
    Add new names and GitHub links as needed

.. _`Julia Kent`: https://github.com/jukent
.. _`Katelyn Fitzgerald`: https://github.com/kafitzgerald
