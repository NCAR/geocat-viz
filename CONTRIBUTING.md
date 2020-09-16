Please first refer to [GeoCAT Contributor's Guide](https://geocat.ucar.edu/pages/contributing.html) for overall 
contribution guidelines (such as detailed description of GeoCAT structure, forking, repository cloning, 
branching, etc.). Once you determine that a function should be contributed under this repo, please refer to the 
following contribution guidelines:


# Adding new functions to the Geocat-viz repo

1. Please check the followings to ensure that the functionality you are about to work on has not been ported yet:
    
    - Functions implemented in `$GEOCAT_VIZ/src/util.py`,
    
    - The list of [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues) and 
    [GeoCAT-examples Issues](https://github.com/NCAR/GeoCAT-examples/issues) to see if any of 
    the existing to-do items are something you might be interested in working on,
        
        - If so, please comment (or self-assign the issue if you have permissions to do so) indicating that 
        you intend to work on it.
        
        - Otherwise, you may create and self-assign an issue under 
        [GeoCAT-viz Issues](https://github.com/NCAR/GeoCAT-viz/issues) 
        that describes need for the functionality you are planning to contribute.

2. Define a new function and implement it under the `$GEOCAT_VIZ/src/util.py`. 