# Installation

This installation guide includes only the GeoCAT-viz installation instructions.
Please refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for installation of
the whole GeoCAT project.


## Installing GeoCAT-viz via Conda

The easiest way to install GeoCAT-viz is using [Conda](http://conda.pydata.org/docs/):

    conda create -n geocat -c conda-forge -c ncar geocat-viz

where "geocat" is the name of a new conda environment, which can then be
activated using:

    conda activate geocat

Please note that the use of the **conda-forge** channel is essential to guarantee
compatibility between dependency packages.

Also, note that the Conda package manager automatically installs all `required`
dependencies, meaning it is not necessary to explicitly install NumPy, Matplotlib, Cartopy,
Xarray, Scikit-learn, etc. when creating an environment.

If you are interested in learning more about how Conda environments work, please visit
the [managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
page of the Conda documentation.
