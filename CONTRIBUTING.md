Please first refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for overall
contribution guidelines (such as detailed description of GeoCAT structure, forking, repository cloning,
branching, etc.). Once you determine that a function should be contributed under this repo, please refer to the
following contribution guidelines:


# Adding new utility functions to the Geocat-viz repo

1. Please check the followings to ensure that the functionality you are about to work on has not been ported yet:

    - Functions implemented in `$GEOCAT_VIZ/src/geocat/viz/util/util.py`,

    - The list of [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues) and
    [GeoCAT-examples Issues](https://github.com/NCAR/GeoCAT-examples/issues) to see if any of
    the existing to-do items are something you might be interested in working on,

        - If so, please comment (or self-assign the issue if you have permissions to do so) indicating that
        you intend to work on it.

        - Otherwise, you may create and self-assign an issue under
        [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues)
        that describes need for the functionality you are planning to contribute.

2. Define a new function and implement it under the `$GEOCAT_VIZ/src/geocat/viz/util/util.py`.

# Adding new plotting utility functionality to the Geocat-viz repo

1. Please check the followings to ensure that the functionality you are about to work on has not been ported yet:

    - Functions implemented in `$GEOCAT_VIZ/src/geocat/viz/`

    - The list of [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues) and
    [GeoCAT-examples Issues](https://github.com/NCAR/GeoCAT-examples/issues) to see if any of
    the existing to-do items are something you might be interested in working on,

        - If so, please comment (or self-assign the issue if you have permissions to do so) indicating that
        you intend to work on it.

        - Otherwise, you may create and self-assign an issue under
        [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues)
        that describes need for the functionality you are planning to contribute.

2. Determine which module is the best home for your new function.

    - If necessary, create a new `.py` module under `$GEOCAT_VIZ/src/geocat/viz/`.

    - Implement your plotting function inside the chosen module, making
    use of the pre-defined parent classes if appropriate

3. Add new modules to the namespace by adding it to `$GEOCAT_VIZ/src/geocat/viz/__init__.py`

# Adding functionality to the User API Documentation

1. Add your new function to `GEOCAT_VIZ/docs/user_api/index.rst`.

2. Ensure that the function docstring has examples linking to relevant GeoCAT-Examples scripts.
