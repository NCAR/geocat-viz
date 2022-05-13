# silly import for backwards compatibility
import warnings
import cmaps

# make python show deprecation warnings
warnings.simplefilter('always', DeprecationWarning)

# deprecation warning for old-style cmaps
warnings.warn("geocat.viz.cmaps is deprecated, use cmaps instead",
              DeprecationWarning)
