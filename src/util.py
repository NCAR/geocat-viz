"""
Utilities to help make matplotlib plots look more like NCL plots
"""
def nclize_axis(ax, minor_per_major=3):
    """
    Utility function to make plots look like NCL plots
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=minor_per_major))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=minor_per_major))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=1.5,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=5,
        width=0.75,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )

################################################

# Helper function for defining NCL-like ax
def add_lat_lon_ticklabels(ax, zero_direction_label=False, dateline_direction_label=False):
    """
    Nice latitude, longitude tick labels

    Set zero_direction_label = True to get 0 E / O W
    Set dateline_direction_label = True to get 180 E / 180 W
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(zero_direction_label=zero_direction_label,
                                       dateline_direction_label=dateline_direction_label)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

################################################

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100, name=None):
    """
    Utility function that truncates a colormap.
    Registers the new colormap by name in plt.cm, and also returns the updated map.

    Copied from  https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib
    """
    import numpy as np
    import matplotlib as mpl
    from matplotlib import cm

    if not name:
        name="trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval)
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        name=name,
        colors=cmap(np.linspace(minval, maxval, n)),
    )
    cm.register_cmap(name, new_cmap)
    return new_cmap

################################################

def make_byr_cmap():
    """
    Define the byr colormap

    Note: this will be replaced with cmaps.BlueYellowRed
    """
    from . import cmaps

    import warnings
    warnings.simplefilter('always', DeprecationWarning)
    warnings.warn('geocat.viz.util.make_byr_cmap: This function has been '
                  'deprecated, please use geocat.viz.cmaps.BlueYellowRed '
                  'instead.', DeprecationWarning, stacklevel=2)
    warnings.filters.pop(0)

    return cmaps.BlueYellowRed
