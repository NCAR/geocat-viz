# Installation

This installation guide includes only the GeoCAT-viz installation instructions.
Please refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for installation of
the whole GeoCAT project.


## Installing GeoCAT-viz via Conda

The easiest way to install GeoCAT-viz is using [Conda](http://conda.pydata.org/docs/).
If you do not have a conda environment, use:

    conda create -n geocat -c conda-forge -c ncar geocat-viz

where "geocat" is the name of a new conda environment, which can then be
activated using:

    conda activate geocat

However, if you would like to add GeoCAT-viz to your existing environment, use:

    conda install -c ncar geocat-viz

Please note that the use of the **conda-forge** channel is essential to guarantee
compatibility between dependency packages.

Also, note that the Conda package manager automatically installs all `required`
dependencies, meaning it is not necessary to explicitly install NumPy, Matplotlib, Cartopy,
Xarray, Scikit-learn, etc. when creating an environment.

If you are interested in learning more about how Conda environments work, please visit
the [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
page of the Conda documentation.


## Building GeoCAT-viz from source

Building GeoCAT-viz from source code is a fairly straightforward task, but
doing so should not be necessary for most users. If you are interested in
building GeoCAT-viz from source, you will need the following packages to be
installed.

### Required dependencies for building and testing GeoCAT-viz

- Python 3.6+
- [numpy](https://numpy.org/doc/stable/)
- [xarray](http://xarray.pydata.org/en/stable/)
- [matplotlib](https://matplotlib.org/stable/)
- [cartopy](https://scitools.org.uk/cartopy/docs/latest/)


### How to create a Conda environment for building GeoCAT-viz

The GeoCAT-viz source code includes a conda environment definition file,
`conda_environment.yml` in the root directory that can be used to create a
development environment containing all of the packages required to build GeoCAT-viz.

    conda env create -f conda_environment.yml
    conda activate geocat_viz_build

### Installing GeoCAT-viz

Once the dependencies listed above are installed, you can install GeoCAT-viz
with running the following command from the root-directory:

    pip install .

For compatibility purposes, we strongly recommend using Conda to
configure your build environment as described above.
