#!/usr/bin/env bash
# adapted from https://github.com/pydata/xarray/blob/main/ci/install-upstream-wheels.sh

# forcibly remove packages to avoid artifacts
conda remove -y --force \
    metpy \
    numpy \
    pandas \
    pint \
    xarray \
    matplotlib \
    cartopy

# conda list
conda list

# if available install from nightly wheels
python -m pip install \
    -i https://pypi.anaconda.org/scientific-python-nightly-wheels/simple/ \
    --no-deps \
    --pre \
    --upgrade \
    matplotlib \
    numpy \
    pandas \
    xarray

# install rest from source
python -m pip install \
    git+https://github.com/SciTools/cartopy.git \
    git+https://github.com/Unidata/MetPy.git \
    git+https://github.com/hgrecco/pint.git \
