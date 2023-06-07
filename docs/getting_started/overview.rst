.. currentmodule:: geocat.viz

.. _overview:

Overview
========
GeoCAT-viz is the visualization component of the `GeoCAT project <https://geocat.ucar.edu/>`__. It contains tools to help plot data,
including convenience and plotting functions that are used to facilitate plotting geosciences data with Matplotlib, Cartopy,
and possibly other Python ecosystem plotting packages. GeoCAT-viz allows Python users to more easily make figures
that resemeble NCL's plotting outputs, as demonstrated in the
`GeoCAT Examples gallery <https://geocat-examples.readthedocs.io/en/latest/gallery/index.html>`__,
but also offers visualization functionality that may go beyond what NCL offers.
It is a principle component of NCAR's `Pivot to Python Initiative <https://www.ncl.ucar.edu/Document/Pivot_to_Python/>`__.

Why GeoCAT-viz?
----------------
GeoCAT-viz is a geoscience visualization Python package created as part of NCAR's `Pivot to Python Initiative <https://www.ncl.ucar.edu/Document/Pivot_to_Python/>`__.
`NCL <https://www.ncl.ucar.edu/>`__, the prior language of choice for geoscience work, has been put into maintenance mode
in favor of Python. This is due to Python's easy-to-learn, open-source nature and the benefits that provides. There are
a plethora of scientific analysis packages designed for general use or for niche applications. Numerous tutorials exist
for learning Python basics and for data analysis workflows. Python also enables scalability through parallel computation
which was never possible with NCL, enabling geoscientists to tackle analysis workflows on large volumes of data.

GeoCAT-viz draws from well-established analysis packages like `Matplotlib <https://matplotlib.org/>`__, `Cartopy <https://scitools.org.uk/cartopy/docs/latest/>`__,
and `MetPy <https://unidata.github.io/MetPy/>`__ to recreate and expand upon NCL
visualization functionalities in pure Python.

One of the main concerns we heard from scientists "pivoting" from NCL to Python is that they found it harder to make
publication-ready figures in Python. The GeoCAT team was tasked with recreating the `NCL Visualization Gallery <https://www.ncl.ucar.edu/gallery.shtml>`__
in Python so that former NCL users could find 1-to-1 plotting examples from a resource they could easily navigate and pinpoint.
Our growing version of this gallery lives in the `GeoCAT Examples gallery <https://geocat-examples.readthedocs.io/en/latest/gallery/index.html>`__,
which is a separate product that the GeoCAT-viz package. However, during its creation we identified several convenience functions
that make it easier to, for example. set plotting settings such as fontsize to match the NCL style, or to create geoscience specific plots, such as skewT diagrams.
Those functions live here in GeoCAT-viz and can be used to improve or augment your Python plotting routines.

GeoCAT-viz's open-source nature allows for more community engagement than a traditional software development workflow
does. As advances are made in the realm of geoscience, new tools will be needed to analyze new datasets. We are dedicated
to addressing user needs and encourage users to submit feature requests and contributions to our GitHub as well as
participate in discussions. See our :ref:`support` page for info on how to submit bug reports, request new
features, and get involved.
