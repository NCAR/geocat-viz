import typing
import matplotlib.axes
import matplotlib.pyplot
import cartopy.mpl.geoaxes
import xarray

def add_lat_lon_ticklabels(ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxesSubplot],
                           zero_direction_label: bool = False,
                           dateline_direction_label: bool = False):
    
    """Utility function to make plots look like NCL plots by adding latitude,
    longitude tick labels.

    Parameters
    ----------
    ax: :class:`matplotlib.axes.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
            Current axes to the current figure

    zero_direction_label: :class:`bool`
        Set True to get 0 E / O W or False to get 0 only.

    dateline_direction_label: :class:`bool`
        Set True to get 180 E / 180 W or False to get 180 only.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_ce_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_ce_1.html?highlight=add_lat_lon>`_
    
    - `NCL_ce_3_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_ce_3_2.html?highlight=add_lat_lon>`_
    
    - `NCL_conOncon_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_2.html?highlight=add_lat_lon>`_
        
    """
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

    lon_formatter = LongitudeFormatter(
        zero_direction_label=zero_direction_label,
        dateline_direction_label=dateline_direction_label)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


def add_major_minor_ticks(ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxesSubplot],
                          x_minor_per_major: int = 3,
                          y_minor_per_major: int = 3,
                          basex: int = 10,
                          basey: int = 10,
                          labelsize: typing.Union[str, int] = "small",
                          linthreshx: int = 2,
                          linthreshy: int = 2):
    """Utility function to make plots look like NCL plots by adding minor and
    major tick lines.

    Parameters
    ----------
    ax: :class:`matplotlib.axes.Axes` or :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    x_minor_per_major: :class:`int`
        Number of minor ticks between adjacent major ticks on x-axis

    y_minor_per_major: :class:`int`
        Number of minor ticks between adjacent major ticks on y-axis

    basex: :class:`int`
        If the xaxis scale is logarithmic, this is the base for the logarithm. Default is base 10.

    basey: :class:`int`
        If the yaxis scale is logarithmic, this is the base for the logarithm. Default is base 10.
        
    labelsize: :class:`str` or :class:`int`
        Size of tick labels. Default is "small".

    linthreshx: :class:`int`
        An argument passed to SymmetricalLogLocator if the xaxis scale is
        `symlog`. Defines the range (-x, x), within which the plot is
        linear. This avoids having the plot go to infinity around zero.
        Defaults to 2.

    linthreshy: :class:`int`
        An argument passed to SymmetricalLogLocator if the yaxis scale is
        `symlog`. Defines the range (-x, x), within which the plot is
        linear. This avoids having the plot go to infinity around zero.
        Defaults to 2.
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_bar_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Bar/NCL_bar_2.html?highlight=add_major_minor_ticks>`_
    
    - `NCL_box_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Boxplots/NCL_box_2.html?highlight=add_major_minor_ticks>`_
    
    - `NCL_scatter_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_1.html?highlight=add_major_minor_ticks>`_
    """
    import matplotlib.ticker as tic
    import numpy as np

    ax.tick_params(labelsize=labelsize)
    ax.minorticks_on()
    if (ax.xaxis.get_scale() == 'log'):
        ax.xaxis.set_minor_locator(
            tic.LogLocator(base=basex,
                           subs=np.linspace(0, basex, x_minor_per_major + 1)))
    elif (ax.xaxis.get_scale() == 'symlog'):
        ax.xaxis.set_minor_locator(
            tic.SymmetricalLogLocator(base=basex,
                                      subs=np.linspace(0, basex,
                                                       x_minor_per_major + 1),
                                      linthresh=linthreshx))
    else:
        ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=x_minor_per_major))

    if (ax.yaxis.get_scale() == 'log'):
        ax.yaxis.set_minor_locator(
            tic.LogLocator(base=basey,
                           subs=np.linspace(0, basey, y_minor_per_major + 1)))
    elif (ax.yaxis.get_scale() == 'symlog'):
        ax.yaxis.set_minor_locator(
            tic.SymmetricalLogLocator(base=basey,
                                      subs=np.linspace(0, basey,
                                                       y_minor_per_major + 1),
                                      linthresh=linthreshy))
    else:
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


def set_titles_and_labels(ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxesSubplot],
                          maintitle: str = None,
                          maintitlefontsize: int = 18,
                          lefttitle: str = None,
                          lefttitlefontsize: int = 18,
                          righttitle: str = None,
                          righttitlefontsize: int = 18,
                          xlabel: str = None,
                          ylabel: str = None,
                          labelfontsize: int = 16):
    """Utility function to handle axis titles, left/right aligned titles, and
    labels as they appear in NCL plots.

    The intent of this function is to help make the plot look like an NCL plot as well as to help developers use only
    this convenience function instead of multiple matplotlib.axes.Axes functions, when applicable.

    Parameters
    ----------
    ax: :class:`matplotlib.axes.Axes` or :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    maintitle: :class:`str`
        Text to use for the maintitle.

    maintitlefontsize: :class:`int`
        Text font size for maintitle. A default value of 18 is used if nothing is set.

    lefttitle: :class:`str`
        Text to use for an optional left-aligned title, if any. For most plots, only a maintitle is enough,
        but for some plot types, a lefttitle likely with a right-aligned title, righttitle, can be used together.

    lefttitlefontsize: :class:`int`
        Text font size for lefttitle. A default value of 18 is used if nothing is set.

    righttitle: :class:`str`
        Text to use for an optional right-aligned title, if any. For most plots, only a maintitle is enough,
        but for some plot types, a righttitle likely with a left-aligned title, lefttitle, can be used together.

    righttitlefontsize: :class:`int`
        Text font size for righttitle. A default value of 18 is used if nothing is set.

    xlabel: :class:`str`
        Text for the x-axis label.

    ylabel: :class:`str`
        Text for the y-axis label.

    labelfontsize: :class:`int`
        Text font size for x- and y-axes. A default value of 16 is used if nothing is set.
        
    Notes
    -----
    If no lefttitle and righttitle is set, maintitle is placed just top to the axes as follows:

    >>>                 maintitle
    >>> ___________________________________________
    >>>|                   Axes                    |
    >>>|                                           |

    
    If any of lefttitle or righttitle is set, lefttitle and righttitle are placed into a row that is just top to the axes, and maintitle is placed to top of
    the row of lefttitle/righttitle as follows:

    >>>                 maintitle
    >>> lefttitle                        righttitle
    >>> ___________________________________________
    >>>|                   Axes                    |
    >>>|                                           |
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_conOncon_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_1.html?highlight=set_titles_and_labels>`_
    
    - `NCL_vector_4.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_4.html?highlight=set_titles_and_labels>`_
    
    - `NCL_polar_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_polar_1.html?highlight=set_titles_and_labels>`_
    """

    if maintitle is not None:
        if lefttitle is not None or righttitle is not None:
            ax.set_title(maintitle, fontsize=maintitlefontsize + 2, y=1.12)
        else:
            ax.set_title(maintitle, fontsize=maintitlefontsize, y=1.04)

    if lefttitle is not None:
        ax.set_title(lefttitle, fontsize=lefttitlefontsize, y=1.04, loc='left')

    if righttitle is not None:
        ax.set_title(righttitle,
                     fontsize=righttitlefontsize,
                     y=1.04,
                     loc='right')

    if xlabel is not None:
        ax.set_xlabel(xlabel, fontsize=labelfontsize)

    if ylabel is not None:
        ax.set_ylabel(ylabel, fontsize=labelfontsize)


def set_axes_limits_and_ticks(ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxesSubplot],
                              xlim: tuple =None,
                              ylim: tuple =None,
                              xticks: list =None,
                              yticks: list =None,
                              xticklabels: list[str] =None,
                              yticklabels: list[str] =None):
    """Utility function to determine axis limits, tick values and labels.

    The intent of this function is to help developers use only this convenience function instead of multiple
    matplotlib.axes.Axes functions, when applicable.

    Parameters
    ----------
    ax: :class:`matplotlib.axes._subplots.AxesSubplot` or :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    xlim: :class:`tuple`
        Should be given as a tuple of numeric values (left, right), where left and right are the left and right
        x-axis limits in data coordinates. Passing None for any of them leaves the limit unchanged. See Matplotlib
        documentation for further information.

    ylim: :class:`tuple`
        Should be given as a tuple of numeric values (left, right), where left and right are the left and right
        y-axis limits in data coordinates. Passing None for any of them leaves the limit unchanged. See Matplotlib
        documentation for further information.

    xticks: :class:`list`
        List of x-axis tick locations. See Matplotlib documentation for further information.

    yticks: :class:`list`
        List of y-axis tick locations. See Matplotlib documentation for further information.

    xticklabels: :class:`list[str]`
        List of string labels for x-axis ticks. See Matplotlib documentation for further information.

    yticklabels: :class:`list[str]`
        List of string labels for y-axis ticks. See Matplotlib documentation for further information.
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_bar_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Bar/NCL_bar_2.html?highlight=set_axes_limits_and_ticks>`_
    
    - `NCL_lb_5.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_lb_5.html?highlight=set_axes_limits_and_ticks>`_
    
    - `NCL_xy_4.py <https://geocat-examples.readthedocs.io/en/latest/gallery/XY/NCL_xy_4.html?highlight=set_axes_limits_and_ticks>`_
    """

    if xticks is not None:
        ax.set_xticks(xticks)

    if yticks is not None:
        ax.set_yticks(yticks)

    if xticklabels is not None:
        ax.set_xticklabels(xticklabels)

    if yticklabels is not None:
        ax.set_yticklabels(yticklabels)

    if xlim is not None:
        ax.set_xlim(xlim)

    if ylim is not None:
        ax.set_ylim(ylim)


def truncate_colormap(cmap: matplotlib.colors.Colormap, 
                      minval: typing.Union[int, float] = 0.0, 
                      maxval: typing.Union[int, float] = 1.0, 
                      n: int = 100, 
                      name: str = None):
    """Utility function that truncates a colormap. Registers the new colormap
    by name in plt.cm, and also returns the updated map.

    `Copied from Stack Overflow <https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib>`_

    Parameters
    ----------
    cmap: :class:`matplotlib.colors.Colormap`
        Colormap to be truncated.

    minval: :class:`int` or :class:`float`
        Minimum value to be used for truncation of the color map.

    maxval: :class:`int` or :class:`float`
        Maximum value to be used for truncation of the color map.

    n: :class:`int`
        Number of color values in the new color map.

    name: :class:`str`
        Optional name of the new color map. If not set, a new name is generated by using the name of the input
        colormap as well as min and max values.
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_dev_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Panels/NCL_dev_2.html?highlight=truncate_colormap>`_
    
    - `NCL_vector_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_1.html?highlight=truncate_colormap>`_
    
    - `NCL_mask_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Masking/NCL_mask_1.html?highlight=truncate_colormap>`_
    """
    import numpy as np
    import matplotlib as mpl
    from matplotlib import cm

    if not name:
        name = "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name,
                                                   a=minval,
                                                   b=maxval)
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        name=name,
        colors=cmap(np.linspace(minval, maxval, n)),
    )
    cm.register_cmap(name, new_cmap)
    return new_cmap


def xr_add_cyclic_longitudes(da: xarray.core.dataarray.DataArray, 
                             coord: str):
    """Utility function to handle the no-shown-data artifact of 0 and
    360-degree longitudes.

    Parameters
    ----------
    da: :class:`xarray.core.dataarray.DataArray`
        Data array that contains one or more coordinates, strictly including the coordinate with the name
        given with the "coord" parameter.

    coord: :class:`str`
        Name of the longitude coordinate within "da" data array.
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_lb_3.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_lb_3.html?highlight=xr_add_cyclic_longitudes>`_
    
    - `NCL_proj_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_proj_2.html?highlight=xr_add_cyclic_longitudes>`_
    
    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=xr_add_cyclic_longitudes>`_
    """

    import xarray as xr
    import cartopy.util as cutil

    cyclic_data, cyclic_coord = cutil.add_cyclic_point(da.values,
                                                       coord=da[coord])

    coords = da.coords.to_dataset()
    coords[coord] = cyclic_coord

    new_da = xr.DataArray(cyclic_data,
                          dims=da.dims,
                          coords=coords.coords,
                          attrs=da.attrs)
    new_da.encoding = da.encoding

    return new_da


def set_map_boundary(ax: matplotlib.axes,
                     lon_range: typing.Union[tuple, list],
                     lat_range: typing.Union[tuple, list],
                     north_pad: int = 0,
                     south_pad: int = 0,
                     east_pad: int = 0,
                     west_pad: int = 0,
                     res: int = 1):
    """Utility function to set the boundary of ax to a path that surrounds a
    given region specified by latitude and longitude coordinates. This boundary
    is drawn in the projection coordinates and therefore follows any curves
    created by the projection. As of now, this only works consistently for the
    Lambert Conformal Projection and North/South Polar Stereographic
    Projections.

    Parameters
    ----------
    ax: :class:`matplotlib.axes`
        The axes to which the boundary will be applied.

    lon_range: :class:`tuple` or :class:`list`
        The two-tuple containing the start and end of the desired range of
        longitudes. The first entry must be smaller than the second entry,
        except when the region crosses the antimeridian. Both entries must
        be between [-180 , 180]. If lon_range is from -180 to 180, then a
        full circle centered on the pole with a radius from the pole to the
        lowest latitude given by lat_range will be set as the boundary.

    lat_range: :class:`tuple` or :class:`list`
        The two-tuple containing the start and end of the desired range of
        latitudes. The first entry must be smaller than the second entry.
        Both entries must be between [-90 , 90].

    north_pad: :class:`int`
        A constant to be added to the second entry in lat_range. Use this
        if the northern edge of the plot is cut off. Defaults to 0.

    south_pad: :class:`int`
        A constant to be subtracted from the first entry in lat_range. Use
        this if the southern edge of the plot is cut off. Defaults to 0.

    east_pad: :class:`int`
        A constant to be added to the second entry in lon_range. Use this
        if the eastern edge of the plot is cut off. Defaults to 0.

    west_pad: :class:`int`
        A constant to be subtracted from the first entry in lon_range. Use
        this if the western edge of the plot is cut off. Defaults to 0.

    res: :class:`int`
        The size of the incrementation for vertices in degrees. Default is
        a vertex every one degree of longitude. A higher number results in
        a lower resolution boundary.
            
    Notes
    -----
    Due to the behavior of cartopy's set_extent() function, the curved
    edges of the boundary may be flattened and cut off. To solve this, use the
    kwargs north_pad, south_pad, east_pad, and west_pad. These will modify the
    coordinates passed to set_extent(). For the Lambert Conformal and Polar
    Stereographic projections, typically only north_pad and south_pad are
    needed. If attempting to use this function for other projections
    (i.e. Othographic) east_pad and west_pad may be needed.
    
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_conOncon_5.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_5.html?highlight=set_map_boundary>`_
    
    - `NCL_panel_9.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Panels/NCL_panel_9.html?highlight=set_map_boundary>`_
    
    - `NCL_polar_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_polar_1.html?highlight=set_map_boundary>`_
    """
    import cartopy.crs as ccrs
    import matplotlib.path as mpath

    if (lon_range[0] >= lon_range[1]):
        if not (lon_range[0] > 0 and lon_range[1] < 0):
            raise ValueError(
                "The first longitude value must be strictly less than the second longitude value unless the region crosses over the antimeridian"
            )

    if (lat_range[0] >= lat_range[1]):
        raise ValueError(
            "The first latitude value must be strictly less than the second latitude value"
        )

    if (lon_range[0] > 180 or lon_range[0] < -180 or lon_range[1] > 180 or
            lon_range[1] < -180):
        raise ValueError(
            "The longitudes must be within the range [-180, 180] inclusive")

    if (lat_range[0] > 90 or lat_range[0] < -90 or lat_range[1] > 90 or
            lat_range[1] < -90):
        raise ValueError(
            "The latitudes must be within the range [-90, 90] inclusive")

    # Make a boundary path in PlateCarree projection beginning in the south
    # west and continuing anticlockwise creating a point every `res` degree
    if (lon_range[0] >= 0 and
            lon_range[1] <= 0):  # Case when range crosses antimeridian
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], 180 + 1, res)] + \
                   [(lon, lat_range[0]) for lon in range(-180, lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], -180 - 1, -res)] + \
                   [(lon, lat_range[1]) for lon in range(180, lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat) for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)
    elif ((lon_range[0] == 180 or lon_range[0] == -180) and
          (lon_range[1] == 180 or lon_range[1] == -180)):
        vertices = [(lon, lat_range[0]) for lon in range(0, 360 + 1, res)]
        path = mpath.Path(vertices)
    else:
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat) for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)

    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
    ax.set_boundary(proj_to_data.transform_path(path))

    ax.set_extent([
        lon_range[0] - west_pad, lon_range[1] + east_pad,
        lat_range[0] - south_pad, lat_range[1] + north_pad
    ],
                  crs=ccrs.PlateCarree())


def findLocalExtrema(da: xarray.DataArray, 
                     highVal: int = 0, 
                     lowVal:int = 1000, 
                     eType: str = 'Low') -> list:
    """Utility function to find local low/high field variable coordinates on a
    contour map. To classify as a local high, the data point must be greater
    than highVal, and to classify as a local low, the data point must be less
    than lowVal.

    Parameters
    ----------
    da: :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable (ex. pressure) data values
    
    highVal: :class:`int`
        Data value that the local high must be greater than to qualify as a "local high" location.
        Default highVal is 0.
    
    lowVal: :class:`int`
        Data value that the local low must be less than to qualify as a "local low" location.
        Default lowVal is 1000.
    
    eType: :class:`str`
        'Low' or 'High'
        Determines which extrema are being found- minimum or maximum, respectively.
        Default eType is 'Low'.
        
    Returns
    -------
    clusterExtremas: :class:`list`
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify local low/high locations
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=findlocalextrema>`_
    
    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=findlocalextrema>`_
    """

    import numpy as np
    from sklearn.cluster import DBSCAN
    import warnings

    # Create a 2D array of coordinates in the same shape as the field variable data
    # so each coordinate is easily mappable to a data value
    # ex:
    # (1, 1), (2, 1), (3, 1)
    # (1, 2)................
    # (1, 3)................
    lons, lats = np.meshgrid(np.array(da.lon), np.array(da.lat))
    coordarr = np.dstack((lons, lats))

    # Find all zeroes that also qualify as low or high values
    extremacoords = []

    if eType == 'Low':
        coordlist = np.argwhere(da.data < lowVal)
        extremacoords = [tuple(coordarr[x[0]][x[1]]) for x in coordlist]
    if eType == 'High':
        coordlist = np.argwhere(da.data > highVal)
        extremacoords = [tuple(coordarr[x[0]][x[1]]) for x in coordlist]

    if extremacoords == []:
        if eType == 'Low':
            warnings.warn(
                'No local extrema with data value less than given lowVal')
            return []
        if eType == 'High':
            warnings.warn(
                'No local extrema with data value greater than given highVal')
            return []

    # Clean up noisy data to find actual extrema

    # Use Density-based spatial clustering of applications with noise
    # to cluster and label coordinates
    db = DBSCAN(eps=10, min_samples=1)
    new = db.fit(extremacoords)
    labels = new.labels_

    # Create an dictionary of values with key being coordinate
    # and value being cluster label.
    coordsAndLabels = {label: [] for label in labels}
    for label, coord in zip(labels, extremacoords):
        coordsAndLabels[label].append(coord)

    # Initialize array of coordinates to be returned
    clusterExtremas = []

    # Iterate through the coordinates in each cluster
    for key in coordsAndLabels:

        # Create array to hold all the field variable values for that cluster
        datavals = []
        for coord in coordsAndLabels[key]:
            # Find pressure data at that coordinate
            cond = np.logical_and(coordarr[:, :, 0] == coord[0],
                                  coordarr[:, :, 1] == coord[1])
            x, y = np.where(cond)
            datavals.append(da.data[x[0]][y[0]])

        # Find the index of the smallest/greatest field variable value of each cluster
        if eType == 'Low':
            index = np.argmin(np.array(datavals))
        if eType == 'High':
            index = np.argmax(np.array(datavals))

        # Append the coordinate corresponding to that index to the array to be returned
        clusterExtremas.append(
            (coordsAndLabels[key][index][0], coordsAndLabels[key][index][1]))

    return clusterExtremas


def plotCLabels(ax: matplotlib.pyplot.axis,
                contours: cartopy.mpl.contour.GeoContourSet,
                transform: cartopy._crs,
                proj: cartopy.crs,
                clabel_locations: list = [],
                fontsize: int = 12,
                whitebbox: bool = False,
                horizontal: bool = False) -> list:
    """Utility function to plot contour labels by passing in a coordinate to
    the clabel function.

    This allows the user to specify the exact locations of the labels, rather than having matplotlib
    plot them automatically.
    This function is exemplified in the python version of https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
    
    Parameters
    ----------
    ax: :class:`matplotlib.pyplot.axis`
        Axis containing the contour set.
    
    contours: :class:`cartopy.mpl.contour.GeoContourSet`
        Contour set that is being labeled.
    
    transform: :class:`cartopy._crs`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).
    
    proj: :class:`cartopy.crs`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.
    
    clabel:_locations :class:`list`
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contours with regular field variable values should be plotted.
    
    fontsize: :class:`int`
        Font size of contour labels.
    
    whitebbox: :class:`bool`
        Setting this to "True" will cause all labels to be plotted with white backgrounds
    
    horizontal: :class:`bool`
        Setting this to "True" will cause the contour labels to be horizontal.
    
    Returns
    -------
    cLabels: :class:`list`
        List of text instances of all contour labels
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotclabels>`_
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Initialize empty array that will be filled with contour label text objects and returned
    cLabels = []

    # Plot any regular contour levels
    if clabel_locations != []:
        clevelpoints = proj.transform_points(
            transform, np.array([x[0] for x in clabel_locations]),
            np.array([x[1] for x in clabel_locations]))
        transformed_locations = [(x[0], x[1]) for x in clevelpoints]
        ax.clabel(contours,
                  manual=transformed_locations,
                  inline=True,
                  fontsize=fontsize,
                  colors='black',
                  fmt="%.0f")
        [cLabels.append(txt) for txt in contours.labelTexts]

        if horizontal is True:
            [txt.set_rotation('horizontal') for txt in contours.labelTexts]

    if whitebbox is True:
        [
            txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
            for txt in cLabels
        ]

    return cLabels


def plotELabels(da: xarray.DataArray,
                transform: cartopy._crs,
                proj: cartopy.crs,
                clabel_locations: list = [],
                label: str = 'L',
                fontsize: int = 22,
                whitebbox: bool = False,
                horizontal: bool = True) -> list:
    """Utility function to plot contour labels.

    High/Low contour labels will be plotted using text boxes for more accurate label values
    and placement.
    This function is exemplified in the python version of https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png
    
    Parameters
    ----------
    da: :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable data values.
    
    transform: :class:`cartopy._crs`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).
    
    proj: :class:`cartopy.crs`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.
    
    clabel_locations: :class:`list`
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contour labels should be plotted.
    
    label: :class:`str`
        ex. 'L' or 'H'
        The data value will be plotted as a subscript of this label.
    
    fontsize: :class:`int`
        Font size of regular contour labels.
    
    horizontal: :class:`bool`
        Setting this to "True" will cause the contour labels to be horizontal.
    
    whitebbox: :class:`bool`
        Setting this to "True" will cause all labels to be plotted with white backgrounds
    
    Returns
    -------
    extremaLabels: :class:`list`
        List of text instances of all contour labels
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotELabels>`_
    
    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=plotELabels>`_
    """

    import numpy as np
    import matplotlib.pyplot as plt

    # Create array of coordinates in the same shape as field variable data
    # so each coordinate can be easily mapped to its data value.
    # ex:
    # (1, 1), (2, 1), (3, 1)
    # (1, 2)................
    # (1, 3)................
    lons, lats = np.meshgrid(np.array(da.lon), np.array(da.lat))
    coordarr = np.dstack((lons, lats))

    # Initialize empty array that will be filled with contour label text objects and returned
    extremaLabels = []

    # Plot any low contour levels
    clabel_points = proj.transform_points(
        transform, np.array([x[0] for x in clabel_locations]),
        np.array([x[1] for x in clabel_locations]))
    transformed_locations = [(x[0], x[1]) for x in clabel_points]

    for x in range(len(transformed_locations)):

        try:
            # Find field variable data at that coordinate
            coord = clabel_locations[x]
            cond = np.logical_and(coordarr[:, :, 0] == coord[0],
                                  coordarr[:, :, 1] == coord[1])
            z, y = np.where(cond)
            p = int(round(da.data[z[0]][y[0]]))

            lab = plt.text(transformed_locations[x][0],
                           transformed_locations[x][1],
                           label + "$_{" + str(p) + "}$",
                           fontsize=fontsize,
                           horizontalalignment='center',
                           verticalalignment='center')

            if horizontal is True:
                lab.set_rotation('horizontal')

            extremaLabels.append(lab)

        except Exception as E:
            print(E)
            continue

    if whitebbox is True:
        [
            txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
            for txt in extremaLabels
        ]

    return extremaLabels


def set_vector_density(data: xarray.core.dataarray.DataArray, 
                       minDistance: int = 0) -> xarray.core.dataarray.DataArray:
    """Utility function to change density of vector plots.

    Parameters
    ----------
    data: :class:`xarray.core.dataarray.DataArray`
        Data array that contains the vector plot latitude/longitude data.
    
    minDistance: :class:`int`
        Value in degrees that determines the distance between the vectors.
    
    Returns
    -------
    ds: :class:`xarray.core.dataarray.DataArray`
        Sliced version of the input data array.
        
    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.
    
    - `NCL_vector_3.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_3.html?highlight=set_vector_density>`_
    """
    import math
    import warnings

    if minDistance <= 0:
        raise Exception("minDistance cannot be negative or zero.")
    else:
        lat_every = 1
        lon_every = 1

        # Get distance between points in latitude (y axis)
        lat = data['lat']
        latdifference = (float)(lat[1] - lat[0])

        # Get distance between points in longitude (x axis)
        lon = data['lon']
        londifference = (float)(lon[1] - lon[0])

        # Get distance between points that are diagonally adjacent
        diagDifference = math.sqrt(latdifference**2 + londifference**2)

        # Initialize ds
        ds = data

        if diagDifference >= minDistance and latdifference >= minDistance and londifference >= minDistance:
            warnings.warn('Plot spacing is alrady greater or equal to ' +
                          (str)(minDistance))

        # While the difference between two vectors is smaller than minDistance, increment the value that
        # the data arrays will be sliced by
        while diagDifference < minDistance or latdifference < minDistance or londifference < minDistance:

            # Get distance between points in latitude (y axis)
            latdifference = (float)(lat[lat_every] - lat[0])

            # Get distance between points in longitude (x axis)
            londifference = (float)(lon[lon_every] - lon[0])

            # Get distance between points that are diagonally adjacent
            diagDifference = math.sqrt(latdifference**2 + londifference**2)

            lat_every += 1
            lon_every += 1

        # Slice data arrays
        ds = data.isel(lat=slice(None, None, lat_every),
                       lon=slice(None, None, lon_every))

        return ds
