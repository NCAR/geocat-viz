Installation
============

Installing GeoCAT-viz via Conda
-------------------------------

The easiest way to install GeoCAT-viz is using
`Conda <http://conda.pydata.org/docs/>`_::

    conda create -n geocat -c conda-forge -c ncar geocat-viz

where "geocat" is the name of a new conda environment, which can then be
activated using::

    conda activate geocat
    
Example code provided with this documentation frequently makes use of other
software packages, such as geocat-datafiles, geocat-comp, and Jupyter, which you
may wish to install into your geocat environment. The following `conda create`
command can be used to create a new conda environment that includes some of
these additional commonly used Python packages pre-installed::

    conda create -n geocat -c conda-forge -c ncar geocat-viz geocat-comp geocat-datafiles jupyter

Alternatively, if you already created a conda environment using the first
command (without the extra packages), you can activate and install the packages
in an existing environment with the following commands::

    conda activate geocat # or whatever your environment is called
    conda install -c conda-forge geocat-comp geocat-datafiles jupyter

Please note that the use of the conda-forge channel is essential to guarantee
compatibility between dependency packages.

Also, note that the Conda package manager automatically installs all `required`
dependencies, meaning it is not necessary to explicitly install Python, NumPy, 
Matplotlib, or Xarray when creating an envionment.  Although other packages are 
often used with GeoCAT-viz, they are considered `optional` dependencies and 
must be explicitly installed.

If you are interested in learning more about how Conda environments work, please
visit the `managing environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_
page of the Conda documentation.


Building GeoCAT-viz from source
-------------------------------

Building GeoCAT-viz from source code is a fairly straightforward task, but
doing so should not be necessary for most users. If you `are` interested in
building GeoCAT-viz from source, you will need the following packages to be
installed.

Required dependencies for building GeoCAT-viz
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    - Python 3.5+
    - cartopy
    - matplotlib
    - numpy
    - xarray
    - Any C compiler (GCC, Clang, etc)


How to create a Conda environment for building GeoCAT-viz
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The GeoCAT-viz source code includes two Conda environment definition files in
the `build_envs` directory that can be used to create a development environment
containing all of the packages required to build GeoCAT-comp.  The file
`environment_Linux.yml` is intended to be used on Linux systems, while
`environment_Darwin.yml` should be used on macOS.  It is necessary to have
separate `environment_*.yml` files because Linux and macOS use different C
compilers, although the following commands should work on both Linux and macOS::

    conda env create -f build_envs/environment.yml
    conda activate geocat_viz_build


Installing GeoCAT-viz
^^^^^^^^^^^^^^^^^^^^^^

Once the dependencies listed above are installed, you can install GeoCAT-comp
with the command::

    pip install .

If you are using a conda environment as described above, this command should
work as-is.  However, if you have chosen to use a different Python binary and
have installed dependencies elsewhere, you may need to set certain environment
variables (CFLAGS, CPPFLAGS, or LDFLAGS) in order for the setup.py script to
find all of the necessary dependency packages.  Due to the potentially
complicated nature of the build process, we strongly recommend using Conda to
configure your build environment.
