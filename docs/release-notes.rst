.. currentmodule:: geocat.viz

.. _release:

Release Notes
=============

v2024.1.0 (Unreleased)
-----------------------

New Features
^^^^^^^^^^^^
* Added subtitle functionality to `set_titles_and_labels()` by `Julia Kent`_ in (:pr:`185`)

Documentation
^^^^^^^^^^^^^
* Invert y-axis in ``add_height_from_pressure_axis`` example by `Katelyn FitzGerald`_ in (:pr:`173`)
* Additions to the examples gallery for ``set_titles_and_labels`` and ``set_axes_limits_and_ticks`` and updated thumbnail for ``plot_contour_labels`` by `Katelyn FitzGerald`_ in (:pr:`181`)
* Remove reference to old ncar conda channel from installation docs by `Katelyn FitzGerald`_ in (:pr:`190`)
* Additional examples published for the `TaylorDiagram` class and `get_skewt_vars()` function by `Julia Kent`_ in (:pr:`186`) and (:pr:`188`)
* `TaylorDiagram` class docstring is clarified by `Julia Kent`_ in (:pr:`182`)
* NSF NCAR branding updates by `Katelyn FitzGerald`_ in (:pr:`191`) and (:pr:`192`)

Bug Fixes
^^^^^^^^^
* Remove matplotlib version pin by `Katelyn FitzGerald`_ in (:pr:`177`)
* Fix `extlinks` for compatibility with Sphinx 6 by `Katelyn FitzGerald`_ in (:pr:`180`)

v2023.10.0 (October 3, 2023)
----------------------------
This release adds a Contributor's Guide and Code of Conduct, updates several
dependency pins, and adds Python 3.11 support while removing Python 3.8.

Bug Fixes
^^^^^^^^^
* Matplotlib pinned to <3.8 by `Katelyn FitzGerald`_ in (:pr:`161`)
* Xarray unpinned by `Katelyn FitzGerald`_ in (:pr:`159`)

New Features
^^^^^^^^^^^^
* Added Python 3.11 and removed Python 3.8 by `Katelyn FitzGerald`_ in (:pr:`162`)

Documentation
^^^^^^^^^^^^^
* Add a contributor's guide by `Katelyn FitzGerald`_ in (:pr:`166`)
* Add code of conduct by `Katelyn FitzGerald`_ in (:pr:`163`)

v2023.09.0 (September 7, 2023)
------------------------------
Bug fix in ``add_height_from_pressure_axis()`` and added example documentation.

Bug Fixes
^^^^^^^^^
* Unit and inferred height fixes in ``add_height_from_pressure_axis()``  by `Katelyn FitzGerald`_ in (:pr:`152`)

Documentation
^^^^^^^^^^^^^
* Additions to the examples gallery for ``find_local_extrema()``, ``plot_contour_labels()``, and ``plot_extrema_labels()`` by `Julia Kent`_ in (:pr:`145`)


v2023.07.0 (July 6, 2023)
-------------------------

Matplotlib unpinned and an examples gallery added.

Bug Fixes
^^^^^^^^^^^^
* Matplotlib unpinned by `Katelyn Fitzgerald`_ in (:pr:`134`)

Documentation
^^^^^^^^^^^^^
* Examples gallery with usage examples of `add_height_from_pressure_axis()`, `add_lat_lon_gridlines()`, and `add_lat_lon_ticklabels()` added by `Julia Kent`_ in (:pr:`133`)
* More examples including `set_tick_direction_spine_visibility()`, `add_right_hand_axis()`, `add_major_minor_ticks()` added by y `Julia Kent`_ in (:pr:`135`)

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
