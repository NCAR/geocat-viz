.. currentmodule:: geocat.viz

.. _installation:

Installation
============

This installation guide includes only the GeoCAT-viz installation and build instructions.
Please refer to the relevant project documentation for how to install other GeoCAT packages.

Installing GeoCAT-viz via Conda in a New Environment
-----------------------------------------------------

The easiest way to install GeoCAT-viz is using
`Conda <http://conda.pydata.org/docs/>`__::

    conda create -n geocat -c conda-forge geocat-viz

where ``geocat`` is the name of a new conda environment, which can then be
activated using::

    conda activate geocat

If you need to make use of other software packages, such as Jupyter
with GeoCAT-viz, you may wish to install into your ``geocat``
environment.  The following ``conda create`` command can be used to create a new
``conda`` environment that includes one of these additional commonly used Python
packages pre-installed::

    conda create -n geocat -c conda-forge geocat-viz jupyter

Alternatively, if you already created a conda environment using the first
command (without the extra packages), you can activate and install the packages
in an existing environment with the following commands::

    conda activate geocat # or whatever your environment is called
    conda install -c conda-forge jupyter

Also, note that the Conda package manager automatically installs all required dependencies,
meaning it is not necessary to explicitly install NumPy, Matplotlib, Cartopy, Xarray, Scikit-learn,
etc. when creating an environment.

If you are interested in learning more about how Conda environments work, please
visit the `managing environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
page of the Conda documentation.

Installing GeoCAT-viz in a Pre-existing Conda Environment
----------------------------------------------------------

If you started a project and later decided to use GeoCAT-viz, you will need to install it in your pre-existing environment.

1. Make sure your conda is up to date by running this command from the terminal::

        conda update conda

2. Activate the conda environment you want to add GeoCAT to. In this example, the environment is called ``geocat``::

        conda activate geocat

3. Install geocat-viz::

        conda install -c conda-forge geocat-viz

Updating GeoCAT-viz via Conda
-------------------------------

It is important to keep your version of ``geocat-viz`` up to date. This can be done as follows:

1. Make sure your Conda is up to date by running this command from the terminal::

        conda update conda

2. Activate the conda environment you want to update. In this example, the environment is called ``geocat``::

        conda activate geocat

3. Update ``geocat-viz``::

        conda update geocat-viz


Installing GeoCAT-viz via PyPi
-------------------------------
GeoCAT-viz is distributed also in PyPI; therefore, the above Conda installation instructions should, in theory,
apply to PyPI installation through using ``pip install`` commands instead of ``conda install`` wherever they occur.

Building GeoCAT-viz from source
--------------------------------

Building GeoCAT-viz from source code is a fairly straightforward task, but
doing so should not be necessary for most users. If you are interested in
building from source, the instructions below will guide you through the process.


How to create a Conda environment for building GeoCAT-viz
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The GeoCAT-viz source code includes a conda environment definition file
``build_envs/environment.yml`` that can be used to create a development environment
containing all of the packages required to build GeoCAT-viz.
The following commands will create and activate the environment::

    conda env create -f build_envs/environment.yml
    conda activate geocat_viz_build


Installing GeoCAT-viz
^^^^^^^^^^^^^^^^^^^^^^

Once the dependencies listed above are installed, you can install GeoCAT-viz
with running the following command from the root-directory::

    pip install .

For compatibility purposes, we strongly recommend using Conda to
configure your build environment as described above.
