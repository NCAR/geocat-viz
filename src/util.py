def add_lat_lon_ticklabels(ax, zero_direction_label=False, dateline_direction_label=False):
    """
    Utility function to make plots look like NCL plots by using latitude, longitude tick labels

    Set zero_direction_label = True to get 0 E / O W
    Set dateline_direction_label = True to get 180 E / 180 W
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(zero_direction_label=zero_direction_label,
                                       dateline_direction_label=dateline_direction_label)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

def add_major_minor_ticks(ax, x_minor_per_major=3, y_minor_per_major=3):
    """
    Utility function to make plots look like NCL plots by adding minor and major tick lines
    """
    import matplotlib.ticker as tic

    ax.tick_params(labelsize="small")
    ax.minorticks_on()
    ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=x_minor_per_major))
    ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=y_minor_per_major))

    # length and width are in points and may need to change depending on figure size etc.
    ax.tick_params(
        "both",
        length=8,
        width=0.9,
        which="major",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(
        "both",
        length=4,
        width=0.4,
        which="minor",
        bottom=True,
        top=True,
        left=True,
        right=True,
    )

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

def set_titles_and_labels(ax, suptitle=None, title=None, left=None, right=None, xlabel=None, ylabel=None):
    """
    Utility function to handle axis titles, left/right titles, and labels
    """

    # Set title, axis labels and limits, etc.

    if title is not None:
        if left is not None or right is not None:
            ax.set_title(title, fontsize=20, y=1.12)
        else:
            ax.set_title(title, fontsize=18, y=1.04)

    if left is not None:
        ax.set_title(left, fontsize=18, y=1.04, loc='left')

    if right is not None:
        ax.set_title(right, fontsize=18, y=1.04, loc='right')

    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=16)

    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=16)

def set_axes_limits_ticks(ax, xlim=None, ylim=None, xticks=None, yticks=None, xticklabels=None, yticklabels=None):

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)

    if xticks is not None:
        ax.set_xticks(xticks)

    if yticks is not None:
        ax.set_yticks(yticks)

    # Modify x-axis tick labels to be shown as North (N) - South (S) latitudinal.
    # Cartopy LatitudeFormatter could be used here, but it is not necessary (it would cost projection loading) since this is
    # only a XY-plot. Therefore, just hard-code for this case:
    ax.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'])

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

def xr_add_cyclic(da, coord):
    """
    Utility function to handle the no-shown-data artifact of 0 and 360-degree longitudes
    """

    import xarray as xr
    import cartopy.util as cutil

    cyclic_data, cyclic_coord = cutil.add_cyclic_point(da.values, coord=da[coord])

    coords = da.coords.to_dataset()
    coords[coord] = cyclic_coord
    return xr.DataArray(cyclic_data, dims=da.dims, coords=coords.coords)


###############################################################################
# Import packages
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.ticker as tic
import geocat.viz as gviz
import geocat.datafiles as gdf

###############################################################################
# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
U = ds.U

###############################################################################
# Plot
fig = plt.figure()
ax = plt.gca()

# Adjust figure size and plot parameters to get identical to original NCL plot
fig.set_size_inches((7, 6.5))

# Hard-code tic values.
ax.set_xticks(np.linspace(-90, 90, 7))
ax.set_yticks(np.linspace(-20, 50, 8))

# Modify x-axis tick labels to be shown as North (N) - South (S) latitudinal.
# Cartopy LatitudeFormatter could be used here, but it is not necessary (it would cost projection loading) since this is
# only a XY-plot. Therefore, just hard-code for this case:
ax.set_xticklabels(['90S', '60S', '30S', '0', '30N', '60N', '90N'])

# Tweak minor tic marks. Set spacing so we get nice round values.
ax.tick_params(labelsize=16)
ax.minorticks_on()
ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=3))
ax.yaxis.set_minor_locator(tic.AutoMinorLocator(n=5))
ax.tick_params('both', length=8, width=0.9, which='major', top=True, right=True)
ax.tick_params('both', length=4, width=0.4, which='minor', top=True, right=True)

# Plot data
U.isel(time=0).sel(lon=82, method='nearest').plot(x="lat", marker='', color='#C0C2EA', linewidth=1.1)
U.isel(time=0).sel(lon=-69, method='nearest').plot(x="lat", marker='', color='#E28D90', linewidth=1.1, linestyle='--', dashes=[6.5, 3.7])

# Set title, axis labels and limits, etc.
ax.set_xlim((-90,90))
ax.set_ylim((-20,50))

set_titles_and_labels(ax, title="Title Title Title Title Title Title Title Title Title ", left="Left", right="Right", xlabel="", ylabel="Zonal Wind")
set_titles_and_labels(ax, title="Title Title Title Title Title Title Title Title Title ", xlabel="", ylabel="Zonal Wind")

# Show the plot
plt.show()