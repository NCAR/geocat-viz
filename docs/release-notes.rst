.. currentmodule:: geocat.viz

.. _release:

Release Notes
=============

vYYYY.MM.## (unreleased)
------------------------
This release...

Testing
^^^^^^^
* Manually specify contour levels in tests by `Katelyn FitzGerald`_ in (:pr:`321`)


v2025.07.0 (July 16, 2025)
--------------------------
This release includes a number of internal testing and packaging updates as well as improved Matplotlib compatibility.

Documentation
^^^^^^^^^^^^^
* Remove reference to NCAR/geocat repo from support page by `Katelyn FitzGerald`_ in (:pr:`293`)

Enhancements
^^^^^^^^^^^^
* Adapt Taylor diagram code for compatibility with Matplotlib 3.11 by `Katelyn FitzGerald`_ in (:pr:`308`, :pr:`309`)

Testing
^^^^^^^
* Add minimum dependency version testing and address minor compatibility issues with Matplotlib by `Katelyn FitzGerald`_ in (:pr:`291`)
* Move to setup-micromamba for environments in CI by `Katelyn FitzGerald`_ in (:pr:`294`)
* Adapt tests to accommodate upstream changes in MetPy for LCL and CAPE by `Katelyn FitzGerald`_ in (:pr:`299`, :pr:`300`)

Internal Changes
^^^^^^^^^^^^^^^^
* Streamlines packaging and configuration by `Katelyn FitzGerald`_ in (:pr:`311`)
* Update PyPI workflow to use build rather than setup.py by `Katelyn FitzGerald`_ in (:pr:`290`)
* Update pins for third party GitHub Actions per new guidance by `Katelyn FitzGerald`_ in (:pr:`297`)
* Transition formatting to `ruff` and `blackdoc` by `Cora Schneck`_ in (:pr:`302`)


v2025.03.0 (March 28, 2025)
---------------------------
This release adds testing infrastructure and significant test coverage, adds support and testing for Python 3.13, drops Python 3.9, and addresses some minor documentation and Matplotlib compatibility issues.

Enhancements
^^^^^^^^^^^^
* Added Python 3.13 support and testing by `Katelyn FitzGerald`_ in (:pr:`278`)

Bug Fixes
^^^^^^^^^
* Change Taylor diagram legend to be specified on the graphical axes to address legend location issues by `Katelyn FitzGerald`_ in (:pr:`274`)

Documentation
^^^^^^^^^^^^^
* Remove link to broken ``NCL_vector_5.py`` example by `Katelyn FitzGerald`_ in (:pr:`249`)
* Fix documentation theme configuration by `Katelyn FitzGerald`_ in (:pr:`253`)
* Minor updates and removal of broken link on citation page by `Katelyn FitzGerald`_ in (:pr:`260`)
* Fix broken link to Taylor Diagram documentation from usage example by `Katelyn FitzGerald`_ in (:pr:`270`)

Internal Changes
^^^^^^^^^^^^^^^^
* Update pre-commit versions and configuration by `Katelyn FitzGerald`_ in (:pr:`247`)
* Remove M1 workaround and minor CI maintenance by `Katelyn FitzGerald`_ in (:pr:`232`)
* Modify tests to avoid an Xarray bug and turn on image comparison testing by `Katelyn FitzGerald`_ in (:pr:`257`)
* Configure analytics by `Katelyn FitzGerald`_ in (:pr:`277`)
* Set ``apply_theta_transforms=False`` to adopt future behavior and silence warnings from ``matplotlib.projections.PolarAxes.PolarTransform()`` by `Katelyn FitzGerald`_ in (:pr:`279`)

Testing
^^^^^^^
* Add basic testing infrastructure by `Katelyn FitzGerald`_ and `Julia Kent`_ in (:pr:`233`)
* Add tests for ``viz.taylor`` by `Julia Kent`_ in (:pr:`234`)
* Add tests for ``viz.util`` by `Julia Kent`_ in (:pr:`239`)
* Remove duplicative macOS runner from CI and add Python 3.10 by `Katelyn FitzGerald`_ in (:pr:`240`)
* Set docs configuration to raise an error following errors in notebook builds by `Katelyn FitzGerald`_ in (:pr:`280`)
* Add upstream dev CI by `Katelyn FitzGerald`_ in (:pr:`282`)

Maintenance
^^^^^^^^^^^
* Require ``matplotlib-base`` instead of ``matplotlib`` and minor dependency cleanup by `Katelyn FitzGerald`_ in (:pr:`284`)


v2024.03.0 (March 26, 2024)
---------------------------
This release deprecates ``TaylorDiagram`` method names ``add_xgrid()`` and
``add_ygrid()`` in favor of the more descriptive ``add_corr_grid()`` and ``add_std_grid()``.

Documentation
^^^^^^^^^^^^^
* Document known issue with `suptitle` argument of  ``set_titles_and_labels`` and Cartopy plots by `Julia Kent`_ in (:pr:`219`)

Deprecations
^^^^^^^^^^
* Pending deprecation warnings added for ``TaylorDiagram`` methods ``add_xgrid`` and ``add_ygrid`` which are changing to the new ``add_corr_grid`` and ``add_std_grid`` by `Julia Kent`_ in (:pr:`219`)

v2024.02.1 (February 28, 2024)
------------------------------
This release changes to implicit namespace packaging and addresses a bug in the Taylor diagram functionality when disabling ``annotate_on``.

Bug Fixes
^^^^^^^^^
* Fix Taylor diagram issue when disabling ``annotate_on`` by `Simon Rosanka`_ in (:pr:`207`)

Internal Changes
^^^^^^^^^^^^^^^^
* Switch to PyPI Trusted Publishing by `Orhan Eroglu`_ in (:pr:`208`)
* Add ``linkcheck_ignore`` to ``docs/conf.py`` to address erroneous failures and add CI badge to README by `Katelyn FitzGerald`_ in (:pr:`218`)
* Convert to implicit namespace packaging set up by `Anissa Zacharias`_ in (:pr:`220`)

v2024.02.0 (February 6, 2024)
-----------------------------
This release adds a new subtitle functionality to ``set_titles_and_labels`` and
includes a number of new usage examples and documentation updates. It also adds
support for Python 3.12 and removes a matplotlib version pin.

New Features
^^^^^^^^^^^^
* Added subtitle functionality to ``set_titles_and_labels()`` by `Julia Kent`_ in (:pr:`185`)
* Added Python 3.12 support and testing for Windows and M1 by `Katelyn FitzGerald`_ in (:pr:`194`)

Documentation
^^^^^^^^^^^^^
* Invert y-axis in ``add_height_from_pressure_axis`` example by `Katelyn FitzGerald`_ in (:pr:`173`)
* Additions to the examples gallery for ``set_titles_and_labels`` and ``set_axes_limits_and_ticks`` and updated thumbnail for ``plot_contour_labels`` by `Katelyn FitzGerald`_ in (:pr:`181`)
* Remove reference to old ncar conda channel from installation docs by `Katelyn FitzGerald`_ in (:pr:`190`)
* Additional examples published for the ``TaylorDiagram`` class and ``get_skewt_vars()`` function by `Julia Kent`_ in (:pr:`186`) and (:pr:`188`)
* ``TaylorDiagram`` class docstring is clarified by `Julia Kent`_ in (:pr:`182`)
* NSF NCAR branding updates by `Katelyn FitzGerald`_ in (:pr:`191`) and (:pr:`192`)

Bug Fixes
^^^^^^^^^
* Remove matplotlib version pin by `Katelyn FitzGerald`_ in (:pr:`177`)
* Fix ``extlinks`` for compatibility with Sphinx 6 by `Katelyn FitzGerald`_ in (:pr:`180`)

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
* Some functions renamed (``findLocalExtrema`` -> ``find_local_extrema``, ``plotCLabels`` -> ``plot_contour_labels``, and ``plotELabels`` -> ``plot_extrema_labels``) and keyword arguments renamed in ``get_skewt_vars`` by `Julia Kent`_ in (:pr:`127`)

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
.. _`Simon Rosanka`: https://github.com/srosanka
.. _`Orhan Eroglu`: https://github.com/erogluorhan
.. _`Anissa Zacharias`: https://github.com/anissa111
.. _`Cora Schneck`: https://github.com/cyschneck
