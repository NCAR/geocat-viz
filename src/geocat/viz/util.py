import warnings

import numpy as np
import typing
import math

import xarray as xr

from pint import Quantity

from sklearn.cluster import DBSCAN

import matplotlib as mpl
import matplotlib.axes
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import matplotlib.ticker as tic

import cartopy.crs as ccrs
import cartopy.util as cutil
import cartopy.mpl.geoaxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

import metpy.calc as mpcalc
from metpy.units import units

from itertools import chain


def set_tick_direction_spine_visibility(ax,
                                        tick_direction='out',
                                        top_spine_visible=True,
                                        bottom_spine_visible=True,
                                        left_spine_visible=True,
                                        right_spine_visible=True):
    """Utility function to turn off axes spines and set tickmark orientations.

    Note: This function should be called after calling add_major_minor_ticks()

    Parameters
    ----------
    ax : :class:`matplotlib.axes._subplots.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    tick_direction : str
        Tick direction. Accepted alias:

        - `in`: to put ticks inside the axes
        - `out`: to put ticks outside the axes
        - `inout`: to put ticks both in and out of the axes

    top_spine_visible : bool
        Set False to turn off top spine of the axes.

    bottom_spine_visible : bool
        Set False to turn off bottom spine of the axes.

    left_spine_visible : bool
        Set False to turn off left spine of the axes.

    right_spine_visible : bool
        Set False to turn off right spine.

    Examples
    --------
     See this example notebook: :doc:`../../examples/set_tick_direction_spine_visibility`.

     More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_box_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Boxplots/NCL_box_2.html?highlight=set_tick_direction_spine_visibility>`_
    """

    ax.tick_params(direction=tick_direction, axis='both', which='both')
    ax.spines['top'].set_visible(top_spine_visible)
    ax.spines['bottom'].set_visible(bottom_spine_visible)
    ax.spines['left'].set_visible(left_spine_visible)
    ax.spines['right'].set_visible(right_spine_visible)

    if top_spine_visible and bottom_spine_visible:
        ax.xaxis.set_ticks_position('default')
    elif bottom_spine_visible and not top_spine_visible:
        ax.xaxis.set_ticks_position('bottom')
    elif top_spine_visible and not bottom_spine_visible:
        ax.xaxis.set_ticks_position('top')
    else:
        ax.xaxis.set_ticks_position('none')

    if left_spine_visible and right_spine_visible:
        ax.yaxis.set_ticks_position('default')
    elif not right_spine_visible and left_spine_visible:
        ax.yaxis.set_ticks_position('left')
    elif not left_spine_visible and right_spine_visible:
        ax.yaxis.set_ticks_position('right')
    else:
        ax.yaxis.set_ticks_position('none')


def add_lat_lon_gridlines(ax,
                          projection=None,
                          draw_labels=True,
                          xlocator=np.arange(-180, 180, 15),
                          ylocator=np.arange(-90, 90, 15),
                          labelsize=12,
                          **kwargs):
    """Utility function that adds latitude and longtitude gridlines to the
    plot.

    Parameters
    ----------
    ax : :class:`cartopy.mpl.geoaxes.GeoAxes`
        Current axes to the current figure.

    projection : :class:`cartopy.crs.CRS`
        Defines a Cartopy Coordinate Reference System. If not given,
        defaults to ccrs.PlateCarree()

    draw_labels : bool
        Toggle whether to draw labels, default to True.

    xlocator, ylocator : :class:`numpy.ndarray`, list
        Arrays of fixed locations of the gridlines in the x and y coordinate of the given CRS.
        Default to np.arange(-180, 180, 15) and np.arange(-90, 90, 15).

    labelsize : float
        Fontsizes of label fontsizes of x and y coordinates.

    *kwargs* control line properties and are passed through to `matplotlib.collections.Collection`.

    Returns
    -------
    gl : :class:`cartopy.mpl.gridliner.Gridliner`
        A Cartopy GridLiner object.

    Examples
    --------
    See this example notebook: :doc:`../../examples/add_lat_lon_gridlines`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_native_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_native_1.html?highlight=add_lat_lon_gridlines>`_

    - `NCL_native_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_native_2.html?highlight=add_lat_lon_gridlines>`_
    """

    # Draw gridlines
    gl = ax.gridlines(crs=projection,
                      draw_labels=draw_labels,
                      x_inline=False,
                      y_inline=False,
                      **kwargs)

    gl.xlocator = tic.FixedLocator(xlocator)
    gl.ylocator = tic.FixedLocator(ylocator)
    gl.xlabel_style = {"rotation": 0, "size": labelsize}
    gl.ylabel_style = {"rotation": 0, "size": labelsize}

    return gl


def add_right_hand_axis(ax,
                        label=None,
                        ylim=None,
                        yticks=None,
                        ticklabelsize=12,
                        labelpad=10,
                        axislabelsize=16,
                        y_minor_per_major=None):
    """Utility function that adds a right hand axis to the plot.

    Parameters
    ----------
    ax : :class:`matplotlib.axes._subplots.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    label : str
        Text to use for the right hand side label.

    ylim : tuple
        Should be given as a tuple of numeric values (left, right), where left and right are the left and right
        y-axis limits in data coordinates. Passing None for any of them leaves the limit unchanged. See Matplotlib
        documentation for further information.

    yticks : list
        List of y-axis tick locations. See Matplotlib documentation for further information.

    ticklabelsize : int
        Text font size of tick labels. A default value of 12 is used if nothing is set.

    labelpad : float
        Spacing in points from the axes bounding box. A default value of 10 is used if nothing is set.

    axislabelsize : int
        Text font size for y-axes. A default value of 16 is used if nothing is set.

    y_minor_per_major : int
            Number of minor ticks between adjacent major ticks on y-axis.

    Returns
    -------
    axRHS : :class:`matplotlib.axes._subplots.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        The created right-hand axis

    Examples
    --------
    See this example notebook: :doc:`../../examples/add_right_hand_axis`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_coneff_8.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_coneff_8.html?highlight=add_right_hand_axis>`_
    """

    axRHS = ax.twinx()
    if label is not None:
        axRHS.set_ylabel(ylabel=label,
                         labelpad=labelpad,
                         fontsize=axislabelsize)
    set_axes_limits_and_ticks(axRHS, ylim=ylim, yticks=yticks)
    axRHS.tick_params(labelsize=ticklabelsize, length=8, width=0.9)
    if y_minor_per_major is not None:
        axRHS.yaxis.set_minor_locator(tic.AutoMinorLocator(n=y_minor_per_major))
        axRHS.tick_params(length=4, width=0.4, which="minor")

    return axRHS


def add_height_from_pressure_axis(ax,
                                  heights=None,
                                  pressure_units='hPa',
                                  ticklabelsize=12,
                                  label='Height (km)',
                                  labelpad=10,
                                  axislabelsize=16):
    """Utility function that adds a right-hand Height axis to the plot, derived
    from the left-hand Pressure axis. Replicates the height-axis functionality
    in NCL's `gsn_csm_pres_hgt`method for drawing a pressure/height plot.

    Parameters
    ----------
    ax : :class:`matplotlib.axes._subplots.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    heights: :class:`numpy.ndarray`, list
        Optional array of desired height values in km.

    pressure_units :str
        Optional Pint-compliant unit string associated with the Pressure values.
        Assume to be `hPa`.

    ticklabelsize : int
        Optional text font size of tick labels. A default value of 12 is used if
        nothing is set.

    label : str
        Optional text to use for the right hand side label.

    labelpad : float
        Optional spacing in points from the axes bounding box. A default value of
        10 is used if nothing is set.

    axislabelsize : int
        Optional text font size for y-axes. A default value of 16 is used if
        nothing is set.

    Returns
    -------
    axRHS : :class:`matplotlib.axes._subplots.AxesSubplot`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        The created right-hand axis

    See ALso
    --------
    Related NCL Functions:
        `gsn_csm_pres_hgt <https://www.ncl.ucar.edu/Document/Graphics/Interfaces/gsn_csm_pres_hgt.shtml>`_,

    Examples
    --------
    See this example notebook: :doc:`../../examples/add_height_from_pressure_axis`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_conOncon_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_1.html?highlight=add_height_from_pressure_axis>`_

    - `NCL_h_lat_6.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_h_lat_6.html?highlight=add_height_from_pressure_axis>`_

    - `NCL_h_lat_7.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_h_lat_7.html?highlight=add_height_from_pressure_axis>`_
    """

    # Create the right hand axis, inheriting from the left
    axRHS = ax.twinx()

    # If height array isn't given, infer it from pressure axis
    if heights is None:
        # Calculate min and max height from pressure axis limits
        pressure_min = np.min(ax.get_ylim()) * units(pressure_units)
        height_max = mpcalc.pressure_to_height_std(pressure_min)
        pressure_max = np.max(ax.get_ylim()) * units(pressure_units)
        height_min = mpcalc.pressure_to_height_std(pressure_max)

        # Range and step values mirror NCL's `set_pres_hgt_axes` logic
        height_range = abs(height_max - height_min)
        if (height_range <= 35 * units('km')):
            step = 4
        elif (height_range <= 70 * units('km')):
            step = 7
        else:
            step = 10

        # Select heights to display as tick labels
        heights = np.arange(int(height_min.magnitude),
                            int(height_max.magnitude) + 1, step)

    # Send selected height values back to pressure to get tick locations
    pressures = mpcalc.height_to_pressure_std(
        heights * units('km')).to(pressure_units).magnitude

    # Set right-hand height axis scale to match left-hand pressure axis
    axRHS.set_yscale(ax.get_yscale())

    # Turn off minor ticks that are spaced by pressure
    axRHS.minorticks_off()

    set_axes_limits_and_ticks(axRHS,
                              ylim=ax.get_ylim(),
                              yticks=pressures,
                              yticklabels=heights)
    axRHS.tick_params(labelsize=ticklabelsize)  # manually set tick label size
    axRHS.set_ylabel(ylabel=label, labelpad=labelpad, fontsize=axislabelsize)

    return axRHS


def add_lat_lon_ticklabels(ax: typing.Union[matplotlib.axes.Axes,
                                            cartopy.mpl.geoaxes.GeoAxesSubplot],
                           zero_direction_label: bool = False,
                           dateline_direction_label: bool = False):
    """Utility function to make plots look like NCL plots by adding latitude,
    longitude tick labels.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    zero_direction_label : bool
        Set True to get 0 E / O W or False to get 0 only.

    dateline_direction_label : bool
        Set True to get 180 E / 180 W or False to get 180 only.

    Examples
    --------
    See this example notebook: :doc:`../../examples/add_lat_lon_ticklabels`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_ce_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_ce_1.html?highlight=add_lat_lon_ticklabels>`_

    - `NCL_ce_3_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_ce_3_2.html?highlight=add_lat_lon_ticklabels>`_

    - `NCL_conOncon_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_2.html?highlight=add_lat_lon_ticklabels>`_
    """

    lon_formatter = LongitudeFormatter(
        zero_direction_label=zero_direction_label,
        dateline_direction_label=dateline_direction_label)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


def add_major_minor_ticks(ax: typing.Union[matplotlib.axes.Axes,
                                           cartopy.mpl.geoaxes.GeoAxesSubplot],
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
    ax : :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    x_minor_per_major : int
        Number of minor ticks between adjacent major ticks on x-axis

    y_minor_per_major : int
        Number of minor ticks between adjacent major ticks on y-axis

    basex : int
        If the xaxis scale is logarithmic, this is the base for the logarithm. Default is base 10.

    basey : int
        If the yaxis scale is logarithmic, this is the base for the logarithm. Default is base 10.

    labelsize : str, int
        Optional text size passed to tick_params. A default value of "small" is used if nothing is set.

    linthreshx : int
        An argument passed to SymmetricalLogLocator if the xaxis scale is
        `symlog`. Defines the range (-x, x), within which the plot is
        linear. This avoids having the plot go to infinity around zero.
        Defaults to 2.

    linthreshy : int
        An argument passed to SymmetricalLogLocator if the yaxis scale is
        `symlog`. Defines the range (-x, x), within which the plot is
        linear. This avoids having the plot go to infinity around zero.
        Defaults to 2.

    Examples
    --------
    See this example notebook: :doc:`../../examples/add_major_minor_ticks`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_bar_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Bar/NCL_bar_2.html?highlight=add_major_minor_ticks>`_

    - `NCL_box_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Boxplots/NCL_box_2.html?highlight=add_major_minor_ticks>`_

    - `NCL_scatter_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Scatter/NCL_scatter_1.html?highlight=add_major_minor_ticks>`_
    """

    ax.tick_params(labelsize=labelsize)
    ax.minorticks_on()
    if ax.xaxis.get_scale() == 'log':
        ax.xaxis.set_minor_locator(
            tic.LogLocator(base=basex,
                           subs=np.linspace(0, basex, x_minor_per_major + 1)))
    elif ax.xaxis.get_scale() == 'symlog':
        ax.xaxis.set_minor_locator(
            tic.SymmetricalLogLocator(base=basex,
                                      subs=np.linspace(0, basex,
                                                       x_minor_per_major + 1),
                                      linthresh=linthreshx))
    else:
        ax.xaxis.set_minor_locator(tic.AutoMinorLocator(n=x_minor_per_major))

    if ax.yaxis.get_scale() == 'log':
        ax.yaxis.set_minor_locator(
            tic.LogLocator(base=basey,
                           subs=np.linspace(0, basey, y_minor_per_major + 1)))
    elif ax.yaxis.get_scale() == 'symlog':
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


def set_titles_and_labels(ax: typing.Union[matplotlib.axes.Axes,
                                           cartopy.mpl.geoaxes.GeoAxesSubplot],
                          maintitle: str = None,
                          maintitlefontsize: int = 18,
                          subtitle: str = None,
                          subtitlefontsize: int = 18,
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
    ax : :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    maintitle : str
        Text to use for the maintitle.

    maintitlefontsize : int
        Text font size for maintitle. A default value of 18 is used if nothing is set.

    subtitle: str
        Text to use for an optional subtitle.

    subtitlefontsize: int
        Text font size for subtitle. A default value of 18 is used if nothing is set.

    lefttitle : str
        Text to use for an optional left-aligned title, if any. For most plots, only a maintitle is enough,
        but for some plot types, a lefttitle likely with a right-aligned title, righttitle, can be used together.

    lefttitlefontsize : int
        Text font size for lefttitle. A default value of 18 is used if nothing is set.

    righttitle : str
        Text to use for an optional right-aligned title, if any. For most plots, only a maintitle is enough,
        but for some plot types, a righttitle likely with a left-aligned title, lefttitle, can be used together.

    righttitlefontsize : int
        Text font size for righttitle. A default value of 18 is used if nothing is set.

    xlabel : str
        Text for the x-axis label.

    ylabel : str
        Text for the y-axis label.

    labelfontsize : int
        Text font size for x- and y-axes. A default value of 16 is used if nothing is set.

    Notes
    -----
    If no lefttitle and righttitle is set, maintitle is placed just top to the axes as follows:

    >>>                  maintitle
    >>>  ___________________________________________
    >>> |                   Axes                    |
    >>> |                                           |


    If any of lefttitle or righttitle is set, lefttitle and righttitle are placed into a row that is just on top of
    the axes, and maintitle is placed on top of
    the row of lefttitle/righttitle as follows:

    >>>                  maintitle
    >>>  lefttitle                        righttitle
    >>>  ___________________________________________
    >>> |                   Axes                    |
    >>> |                                           |

    Be aware that the `suptitle` functionality does not always render well for Cartopy plots. If your main title appears too far above your plot, the recommended fix is to decrease the y-dimension of your figure size.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the
    `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_conOncon_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_1.html?highlight=set_titles_and_labels>`_

    - `NCL_vector_4.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_4.html?highlight=set_titles_and_labels>`_

    - `NCL_polar_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_polar_1.html?highlight=set_titles_and_labels>`_
    """

    if maintitle is not None:
        if subtitle is not None:
            fig = ax.get_figure()
            fig.suptitle(maintitle,
                         fontsize=maintitlefontsize,
                         y=1.04,
                         ha='center')
        elif lefttitle is not None or righttitle is not None:
            ax.set_title(maintitle, fontsize=maintitlefontsize + 2, y=1.12)
        else:
            ax.set_title(maintitle, fontsize=maintitlefontsize, y=1.04)

    if subtitle is not None:
        ax.set_title(subtitle, fontsize=subtitlefontsize)

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


def set_axes_limits_and_ticks(
        ax: typing.Union[matplotlib.axes.Axes,
                         cartopy.mpl.geoaxes.GeoAxesSubplot],
        xlim: tuple = None,
        ylim: tuple = None,
        xticks: list = None,
        yticks: list = None,
        xticklabels: list = None,
        yticklabels: list = None):
    """Utility function to determine axis limits, tick values and labels.

    The intent of this function is to help developers use only this convenience function instead of multiple
    matplotlib.axes.Axes functions, when applicable.

    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxesSubplot`
        Current axes to the current figure

    xlim : tuple
        Should be given as a tuple of numeric values (left, right), where left and right are the left and right
        x-axis limits in data coordinates. Passing None for any of them leaves the limit unchanged. See Matplotlib
        documentation for further information.

    ylim : tuple
        Should be given as a tuple of numeric values (left, right), where left and right are the left and right
        y-axis limits in data coordinates. Passing None for any of them leaves the limit unchanged. See Matplotlib
        documentation for further information.

    xticks : list
        List of x-axis tick locations. See Matplotlib documentation for further information.

    yticks : list
        List of y-axis tick locations. See Matplotlib documentation for further information.

    xticklabels : list
        List of string labels for x-axis ticks. See Matplotlib documentation for further information.

    yticklabels : list
        List of string labels for y-axis ticks. See Matplotlib documentation for further information.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the
    `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

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
                      n: int = 256,
                      name: str = None,
                      force: bool = True):
    """Utility function that truncates a colormap. Registers the new colormap
    by name and returns the corresponding colormap object.

    `Copied from Stack Overflow <https://stackoverflow.com/questions/18926031/how-to-extract-a-subset-of-a-colormap-as-a-new-colormap-in-matplotlib>`_

    Parameters
    ----------
    cmap : :class:`matplotlib.colors.Colormap`
        Colormap to be truncated.

    minval : int, float
        Minimum normalized value to be used for truncation of the color map.

    maxval : int, float
        Maximum normalized value to be used for truncation of the color map.

    n : int
        Number of color values in the new color map.

    name : str
        Optional name of the new color map. If not set, a new name is generated by using the name of the input
        colormap as well as min and max values.

    force : bool, default = True
        If False, a ValueError is raised if trying to overwrite an already registered name. True supports
        overwriting registered colormaps other than the builtin colormaps.


    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the
    `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_dev_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Panels/NCL_dev_2.html?highlight=truncate_colormap>`_

    - `NCL_vector_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_1.html?highlight=truncate_colormap>`_

    - `NCL_mask_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Masking/NCL_mask_1.html?highlight=truncate_colormap>`_
    """

    if not name:
        name = "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name,
                                                   a=minval,
                                                   b=maxval)
    new_cmap = mpl.colors.LinearSegmentedColormap.from_list(
        name=name, colors=cmap(np.linspace(minval, maxval)), N=n)

    try:
        mpl.colormaps.register(new_cmap, force=force)
    except AttributeError:
        mpl.cm.register_cmap(name=name, cmap=new_cmap)

    return new_cmap


def xr_add_cyclic_longitudes(da: xr.DataArray, coord: str):
    """Utility function to handle the no-shown-data artifact of 0 and
    360-degree longitudes.

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        Data array that contains one or more coordinates, strictly including the coordinate with the name
        given with the "coord" parameter.

    coord : str
        Name of the longitude coordinate within "da" data array.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the
    `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_lb_3.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_lb_3.html?highlight=xr_add_cyclic_longitudes>`_

    - `NCL_proj_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_proj_2.html?highlight=xr_add_cyclic_longitudes>`_

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=xr_add_cyclic_longitudes>`_
    """

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


def set_map_boundary(ax: matplotlib.axes.Axes,
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
    ax : :class:`matplotlib.axes.Axes`
        The axes to which the boundary will be applied.

    lon_range : tuple, list
        The two-tuple containing the start and end of the desired range of
        longitudes. The first entry must be smaller than the second entry,
        except when the region crosses the antimeridian. Both entries must
        be between [-180 , 180]. If lon_range is from -180 to 180, then a
        full circle centered on the pole with a radius from the pole to the
        lowest latitude given by lat_range will be set as the boundary.

    lat_range : tuple, list
        The two-tuple containing the start and end of the desired range of
        latitudes. The first entry must be smaller than the second entry.
        Both entries must be between [-90 , 90].

    north_pad : int
        A constant to be added to the second entry in lat_range. Use this
        if the northern edge of the plot is cut off. Defaults to 0.

    south_pad : int
        A constant to be subtracted from the first entry in lat_range. Use
        this if the southern edge of the plot is cut off. Defaults to 0.

    east_pad : int
        A constant to be added to the second entry in lon_range. Use this
        if the eastern edge of the plot is cut off. Defaults to 0.

    west_pad : int
        A constant to be subtracted from the first entry in lon_range. Use
        this if the western edge of the plot is cut off. Defaults to 0.

    res : int
        The size of the incrementation for vertices in degrees. Default is
        a vertex every one degree of longitude. A higher number results in
        a lower resolution boundary.

    Notes
    -----
    Due to the behavior of Cartopy's set_extent() function, the curved
    edges of the boundary may be flattened and cut off. To solve this, use the
    kwargs north_pad, south_pad, east_pad, and west_pad. These will modify the
    coordinates passed to set_extent(). For the Lambert Conformal and Polar
    Stereographic projections, typically only north_pad and south_pad are
    needed. If attempting to use this function for other projections
    (i.e. Orthographic) east_pad and west_pad may be needed.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the
    `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_conOncon_5.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_conOncon_5.html?highlight=set_map_boundary>`_

    - `NCL_panel_9.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Panels/NCL_panel_9.html?highlight=set_map_boundary>`_

    - `NCL_polar_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Contours/NCL_polar_1.html?highlight=set_map_boundary>`_
    """

    if lon_range[0] >= lon_range[1]:
        if not (lon_range[0] > 0 > lon_range[1]):
            raise ValueError(
                "The first longitude value must be strictly less than the second longitude value unless the region crosses over the antimeridian"
            )

    if lat_range[0] >= lat_range[1]:
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
    if lon_range[0] >= 0 >= lon_range[1]:  # Case when range crosses antimeridian
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], 180 + 1, res)] + \
                   [(lon, lat_range[0]) for lon in range(-180, lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], -180 - 1, -res)] + \
                   [(lon, lat_range[1]) for lon in range(180, lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat)
                    for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)
    elif ((lon_range[0] == 180 or lon_range[0] == -180) and
          (lon_range[1] == 180 or lon_range[1] == -180)):
        vertices = [(lon, lat_range[0]) for lon in range(0, 360 + 1, res)]
        path = mpath.Path(vertices)
    else:
        vertices = [(lon, lat_range[0]) for lon in range(lon_range[0], lon_range[1] + 1, res)] + \
                   [(lon_range[1], lat) for lat in range(lat_range[0], lat_range[1] + 1, res)] + \
                   [(lon, lat_range[1]) for lon in range(lon_range[1], lon_range[0] - 1, -res)] + \
                   [(lon_range[0], lat)
                    for lat in range(lat_range[1], lat_range[0] - 1, -res)]
        path = mpath.Path(vertices)

    proj_to_data = ccrs.PlateCarree()._as_mpl_transform(ax) - ax.transData
    ax.set_boundary(proj_to_data.transform_path(path))

    ax.set_extent([
        lon_range[0] - west_pad, lon_range[1] + east_pad,
        lat_range[0] - south_pad, lat_range[1] + north_pad
    ],
                  crs=ccrs.PlateCarree())


def findLocalExtrema(da: xr.DataArray,
                     highVal: int = 0,
                     lowVal: int = 1000,
                     eType: str = 'Low',
                     eps: float = 10) -> list:
    r""".. deprecated:: 2023.02.0 The ``findLocalExtrema`` function is deprecated due to naming conventions. Use :func:`find_local_extrema` instead.

    Utility function to find local low/high field variable coordinates on a
    contour map. To classify as a local high, the data point must be greater
    than highval, and to classify as a local low, the data point must be less
    than lowVal.

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable (ex. pressure) data values

    highVal : int
        Data value that the local high must be greater than to qualify as a "local high" location.
        Default highVal is 0.

    lowVal : int
        Data value that the local low must be less than to qualify as a "local low" location.
        Default lowVal is 1000.

    eType : str
        'Low' or 'High'
        Determines which extrema are being found- minimum or maximum, respectively.
        Default eType is 'Low'.

    eps : float
            Parameter supplied to sklearn.cluster.DBSCAN determining the maximum distance between two samples
            for one to be considered as in the neighborhood of the other.
            Default eps is 10.

    Returns
    -------
    clusterExtremas : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify local low/high locations

    Examples
    --------
    See this example notebook: :doc:`../../examples/find_local_extrema`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=findlocalextrema>`_

    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=findlocalextrema>`_
    """

    warnings.warn(
        'This function is deprecated. Call `find_local_extrema` instead.',
        PendingDeprecationWarning)

    return find_local_extrema(da, highVal, lowVal, eType, eps)


def find_local_extrema(da: xr.DataArray,
                       highVal: int = 0,
                       lowVal: int = 1000,
                       eType: str = 'Low',
                       eps: float = 10) -> list:
    """Utility function to find local low/high field variable coordinates on a
    contour map. To classify as a local high, the data point must be greater
    than highval, and to classify as a local low, the data point must be less
    than lowVal.

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable (ex. pressure) data values

    highVal : int
        Data value that the local high must be greater than to qualify as a "local high" location.
        Default highVal is 0.

    lowVal : int
        Data value that the local low must be less than to qualify as a "local low" location.
        Default lowVal is 1000.

    eType : str
        'Low' or 'High'
        Determines which extrema are being found- minimum or maximum, respectively.
        Default eType is 'Low'.

    eps : float
            Parameter supplied to sklearn.cluster.DBSCAN determining the maximum distance between two samples
            for one to be considered as in the neighborhood of the other.
            Default eps is 10.

    Returns
    -------
    clusterExtremas : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify local low/high locations

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=findlocalextrema>`_

    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=findlocalextrema>`_
    """

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
                'No local extrema with data value less than given lowval')
            return []
        if eType == 'High':
            warnings.warn(
                'No local extrema with data value greater than given highval')
            return []

    # Clean up noisy data to find actual extrema

    # Use Density-based spatial clustering of applications with noise
    # to cluster and label coordinates
    db = DBSCAN(eps=eps, min_samples=1)
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
        data_vals = []
        for coord in coordsAndLabels[key]:
            # Find pressure data at that coordinate
            cond = np.logical_and(coordarr[:, :, 0] == coord[0],
                                  coordarr[:, :, 1] == coord[1])
            x, y = np.where(cond)
            data_vals.append(da.data[x[0]][y[0]])

        # Find the index of the smallest/greatest field variable value of each cluster
        if eType == 'Low':
            index = np.argmin(np.array(data_vals))
        if eType == 'High':
            index = np.argmax(np.array(data_vals))

        # Append the coordinate corresponding to that index to the array to be returned
        clusterExtremas.append(
            (coordsAndLabels[key][index][0], coordsAndLabels[key][index][1]))

    return clusterExtremas


def plotCLabels(ax: matplotlib.axes.Axes,
                contours,
                transform: cartopy.crs.CRS,
                proj: cartopy.crs.CRS,
                clabel_locations: list = [],
                fontsize: int = 12,
                whitebbox: bool = False,
                horizontal: bool = False) -> list:
    r""".. deprecated:: 2023.02.0 The ``plotCLabels`` function is deprecated due to naming conventions. Use :func:`plot_contour_levels` instead.

    Utility function to plot contour labels by passing in a coordinate to
    the clabel function.

    This allows the user to specify the exact locations of the labels, rather than having matplotlib
    plot them automatically.


    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        Axis containing the contour set.

    contours : :class:`matplotlib.contour.QuadContourSet`
        Contour set that is being labeled.

    transform : :class:`cartopy.crs.CRS`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).

    proj : :class:`cartopy.crs.CRS`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.

    clabel_locations : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contours with regular field variable values should be plotted.

    fontsize : int
        Font size of contour labels.

    whitebbox : bool
        Setting this to "True" will cause all labels to be plotted with white backgrounds

    horizontal : bool
        Setting this to "True" will cause the contour labels to be horizontal.

    Returns
    -------
    cLabels : list
        List of text instances of all contour labels

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotCLabels>`_
    """

    warnings.warn(
        'This function is  deprecated. Call `plot_contour_labels` instead.',
        PendingDeprecationWarning)

    return plot_contour_labels(ax, contours, transform, proj, clabel_locations,
                               fontsize, whitebbox, horizontal)


def plot_contour_labels(ax: matplotlib.axes.Axes,
                        contours,
                        transform: cartopy.crs.CRS,
                        proj: cartopy.crs.CRS,
                        clabel_locations: list = [],
                        fontsize: int = 12,
                        whitebbox: bool = False,
                        horizontal: bool = False) -> list:
    """Utility function to plot contour labels by passing in a coordinate to
    the clabel function.

    This allows the user to specify the exact locations of the labels, rather than having matplotlib
    plot them automatically.


    Parameters
    ----------
    ax : :class:`matplotlib.axes.Axes`
        Axis containing the contour set.

    contours : :class:`matplotlib.contour.QuadContourSet`
        Contour set that is being labeled.

    transform : :class:`cartopy.crs.CRS`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).

    proj : :class:`cartopy.crs.CRS`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.

    clabel_locations : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contours with regular field variable values should be plotted.

    fontsize : int
        Font size of contour labels.

    whitebbox : bool
        Setting this to "True" will cause all labels to be plotted with white backgrounds

    horizontal : bool
        Setting this to "True" will cause the contour labels to be horizontal.

    Returns
    -------
    cLabels : list
        List of text instances of all contour labels

    Examples
    --------
    See this example notebook: :doc:`../../examples/plot_contour_labels`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotCLabels>`_
    """

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
                  fmt='%.0f')
        [cLabels.append(txt) for txt in contours.labelTexts]

        if horizontal is True:
            [txt.set_rotation('horizontal') for txt in contours.labelTexts]

    if whitebbox is True:
        [
            txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
            for txt in cLabels
        ]

    return cLabels


def plotELabels(da: xr.DataArray,
                transform: cartopy.crs.CRS,
                proj: cartopy.crs.CRS,
                clabel_locations: list = [],
                label: str = 'L',
                fontsize: int = 22,
                whitebbox: bool = False,
                horizontal: bool = True) -> list:
    r""".. deprecated:: 2023.02.0 The ``plotELabels`` function is deprecated due to naming conventions. Use :func:`plot_extrema_labels` instead.

    Utility function to plot high/low contour labels.

    High/Low contour labels will be plotted using text boxes for more accurate label values
    and placement.
    This function is exemplified in the python version of `sat_1_lg <https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png>`__

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable data values.

    transform : :class:`cartopy.crs.CRS`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).

    proj : :class:`cartopy.crs.CRS`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.

    clabel_locations : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contour labels should be plotted.

    label : str
        ex. 'L' or 'H'
        The data value will be plotted as a subscript of this label.

    fontsize : int
        Font size of regular contour labels.

    horizontal : bool
        Setting this to "True" will cause the contour labels to be horizontal.

    whitebbox : bool
        Setting this to "True" will cause all labels to be plotted with white backgrounds

    Returns
    -------
    extremaLabels : list
        List of text instances of all contour labels

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotELabels>`_

    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=plotELabels>`_
    """

    warnings.warn(
        'This function is deprecated. Please use `plot_extrema_labels` instead.',
        PendingDeprecationWarning)

    return plot_extrema_labels(da, transform, proj, clabel_locations, label,
                               fontsize, whitebbox, horizontal)


def plot_extrema_labels(da: xr.DataArray,
                        transform: cartopy.crs.CRS,
                        proj: cartopy.crs.CRS,
                        label_locations: list = [],
                        label: str = 'L',
                        fontsize: int = 22,
                        whitebbox: bool = False,
                        horizontal: bool = True,
                        show_warnings: bool = True) -> list:
    """Utility function to plot contour labels.

    High/Low contour labels will be plotted using text boxes for more accurate label values
    and placement.
    This function is exemplified in the python version of https://www.ncl.ucar.edu/Applications/Images/sat_1_lg.png

    Parameters
    ----------
    da : :class:`xarray.DataArray`
        Xarray data array containing the lat, lon, and field variable data values.

    transform : :class:`cartopy.crs.CRS`
        Instance of CRS that represents the source coordinate system of coordinates.
        (ex. ccrs.Geodetic()).

    proj : :class:`cartopy.crs.CRS`
        Projection 'ax' is defined by.
        This is the instance of CRS that the coordinates will be transformed to.

    label_locations : list
        List of coordinate tuples in GPS form (lon in degrees, lat in degrees)
        that specify where the contour labels should be plotted.
        Locations that cannot be translated into the provided projection will be dropped.

    label : str
        ex. 'L' or 'H'
        The data value will be plotted as a subscript of this label.

    fontsize : int
        Font size of regular contour labels.

    horizontal : bool
        Setting this to "True" will cause the contour labels to be horizontal.

    whitebbox : bool
        Setting this to "True" will cause all labels to be plotted with white backgrounds

    Returns
    -------
    extremaLabels : list
        List of text instances of all contour labels

    Examples
    --------
    See this example notebook: :doc:`../../examples/plot_extrema_labels`.

    More in-depth plotting examples that utilize this function are in the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_sat_1.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_1.html?highlight=plotELabels>`_

    - `NCL_sat_2.py <https://geocat-examples.readthedocs.io/en/latest/gallery/MapProjections/NCL_sat_2.html?highlight=plotELabels>`_
    """

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
        transform, np.array([x[0] for x in label_locations]),
        np.array([x[1] for x in label_locations]))
    transformed_locations = [(x[0], x[1]) for x in clabel_points]

    nan_indices = [
        i for i, (x, y) in enumerate(transformed_locations)
        if math.isnan(x) or math.isnan(y)
    ]
    transformed_locations = [
        loc for i, loc in enumerate(transformed_locations)
        if i not in nan_indices
    ]

    if show_warnings:
        bad_locations = [label_locations[i] for i in nan_indices]
        bad_locations_str = ", ".join([str(loc) for loc in bad_locations])
        if len(bad_locations) > 0:
            warnings.warn(
                f'The following locations could not be translated into the desired projection: {bad_locations_str}. These locations will be dropped.',
                stacklevel=2)

    for loc in range(len(transformed_locations)):

        try:
            # Find field variable data at that coordinate
            coord = label_locations[loc]
            cond = np.logical_and(coordarr[:, :, 0] == coord[0],
                                  coordarr[:, :, 1] == coord[1])
            z_loc, y_loc = np.where(cond)
            p_loc = int(round(da.data[z_loc[0]][y_loc[0]]))

            lab = plt.text(transformed_locations[loc][0],
                           transformed_locations[loc][1],
                           label + '$_{' + str(p_loc) + '}$',
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


def set_vector_density(data: xr.DataArray,
                       minDistance: int = 0) -> xr.DataArray:
    """Utility function to change density of vector plots.

    Parameters
    ----------
    data : :class:`xarray.DataArray`
        Data array that contains the vector plot latitude/longitude data.

    minDistance : int
        Value in degrees that determines the distance between the vectors.

    Returns
    -------
    ds : :class:`xarray.DataArray`
        Sliced version of the input data array.

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_vector_3.py <https://geocat-examples.readthedocs.io/en/latest/gallery/Vectors/NCL_vector_3.html?highlight=set_vector_density>`_
    """
    if minDistance <= 0:
        raise Exception('minDistance cannot be negative or zero.')
    else:
        lat_every = 1
        lon_every = 1

        # Get distance between points in latitude (y axis)
        lat = data['lat']
        latdifference = float(lat[1] - lat[0])

        # Get distance between points in longitude (x axis)
        lon = data['lon']
        londifference = float(lon[1] - lon[0])

        # Get distance between points that are diagonally adjacent
        diagDifference = math.sqrt(latdifference**2 + londifference**2)

        if diagDifference >= minDistance and latdifference >= minDistance and londifference >= minDistance:
            warnings.warn('Plot spacing is alrady greater or equal to ' +
                          str(minDistance))

        # While the difference between two vectors is smaller than minDistance, increment the value that
        # the data arrays will be sliced by
        while diagDifference < minDistance or latdifference < minDistance or londifference < minDistance:
            # Get distance between points in latitude (y axis)
            latdifference = float(lat[lat_every] - lat[0])

            # Get distance between points in longitude (x axis)
            londifference = float(lon[lon_every] - lon[0])

            # Get distance between points that are diagonally adjacent
            diagDifference = math.sqrt(latdifference**2 + londifference**2)

            lat_every += 1
            lon_every += 1

        # Slice data arrays
        ds = data.isel(lat=slice(None, None, lat_every),
                       lon=slice(None, None, lon_every))

        return ds


def get_skewt_vars(pressure: Quantity = None,
                   temperature: Quantity = None,
                   dewpoint: Quantity = None,
                   profile: Quantity = None,
                   p: Quantity = None,
                   tc: Quantity = None,
                   tdc: Quantity = None,
                   pro: Quantity = None) -> str:
    """This function processes the dataset values and returns a string element
    which can be used as a subtitle to replicate the styles of NCL Skew-T
    Diagrams.

    Parameters
    ----------
    pressure : :class:`pint.Quantity`
        Pressure level input from dataset. Renamed from deprecated kwarg `p`.
    temperature : :class:`pint.Quantity`
        Temperature for parcel from dataset. Renamed from deprecated kwarg `tc`.
    dewpoint : :class:`pint.Quantity`
        Dew point temperature for parcel from dataset. Renamed from deprecated kwarg `tdc`.
    profile : :class:`pint.Quantity`
        Parcel profile temperature converted to degC. Renamed from deprecated kwarg `pro`.
    p : :class:`pint.Quantity`
        Pressure level input from dataset.

        .. deprecated:: 2023.06.0
            In an effort to refactor the codebase to follow naming conventions,
            keyword arguments have been renamed to more meaningful values.
            ``p`` parameter has been deprecated in favor of ``pressure`.

    tc : :class:`pint.Quantity`
        Temperature for parcel from dataset.

        .. deprecated:: 2023.06.0
            In an effort to refactor the codebase to follow naming conventions,
            keyword arguments have been renamed to more meaningful values.
            ``tc`` parameter has been deprecated in favor of ``temperature``.

    tdc : :class:`pint.Quantity`
        Dew point temperature for parcel from dataset.

        .. deprecated:: 2023.06.0
            In an effort to refactor the codebase to follow naming conventions,
            keyword arguments have been renamed to more meaningful values.
            ``tdc`` parameter has been deprecated in favor of ``dewpoint``.

    pro : :class:`pint.Quantity`
        Parcel profile temperature converted to degC.

        .. deprecated:: 2023.06.0
            In an effort to refactor the codebase to follow naming conventions,
            keyword arguments have been renamed to more meaningful values.
            ``pro`` parameter has been deprecated in favor of ``profile``.

    Returns
    -------
    joined : str
        A string element with the format "Plcl=<value> Tlcl[C]=<value> Shox=<value> Pwat[cm]=<value> Cape[J]=<value>" where:
        - Cape  -  Convective Available Potential Energy [J]
        - Pwat  -  Precipitable Water [cm]
        - Shox  -  Showalter Index (stability)
        - Plcl  -  Pressure of the lifting condensation level [hPa]
        - Tlcl  -  Temperature at the lifting condensation level [C]

    See Also
    --------
    Related NCL Functions:
        `skewT_PlotData <https://www.ncl.ucar.edu/Document/Functions/Skewt_func/skewT_PlotData.shtml>`_,
        `skewt_BackGround <https://www.ncl.ucar.edu/Document/Functions/Skewt_func/skewT_BackGround.shtml>`_

    Examples
    --------
    All usage examples are within the GeoCAT-Examples Gallery. To see more usage cases, search the function on the `website <https://geocat-examples.readthedocs.io/en/latest/index.html>`_.

    - `NCL_skewt_2_2 <https://geocat-examples.readthedocs.io/en/latest/gallery/Skew-T/NCL_skewt_2_2.html?highlight=get_skewt_vars>`_
    """
    # Support for deprecating kwargs
    if p:
        pressure = p
        warnings.warn(
            'The keyword argument `p` is deprecated. Use `pressure` instead.',
            PendingDeprecationWarning)
    if tc:
        temperature = tc
        warnings.warn(
            'The keyword argument `tc` is deprecated. Use `temperature` instead.',
            PendingDeprecationWarning)
    if tdc:
        dewpoint = tdc
        warnings.warn(
            'The keyword argument `tdc` is deprecated. Use `dewpoint` instead.',
            PendingDeprecationWarning)
    if pro:
        profile = pro
        warnings.warn(
            'The keyword argument `pro` is deprecated. Use `profile` instead.',
            PendingDeprecationWarning)

    # CAPE
    cape = mpcalc.cape_cin(pressure, temperature, dewpoint, profile)
    cape = cape[0].magnitude

    # Precipitable Water
    pwat = mpcalc.precipitable_water(pressure, dewpoint)
    pwat = (pwat.magnitude / 10) * units.cm  # Convert mm to cm
    pwat = pwat.magnitude

    # Pressure and temperature of lcl
    lcl = mpcalc.lcl(pressure[0], temperature[0], dewpoint[0])
    plcl = lcl[0].magnitude
    tlcl = lcl[1].magnitude

    # Showalter index
    shox = mpcalc.showalter_index(pressure, temperature, dewpoint)
    shox = shox[0].magnitude

    # Place calculated values in iterable list
    val_list = [plcl, tlcl, shox, pwat, cape]
    val_ints = np.round(val_list).astype(int)

    # Define variable names for calculated values
    names = ['Plcl=', 'Tlcl[C]=', 'Shox=', 'Pwat[cm]=', 'Cape[J]=']

    # Combine the list of values with their corresponding labels
    lst = list(chain.from_iterable(zip(names, val_ints)))
    lst = map(str, lst)

    # Create one large string for later plotting use
    joined = ' '.join(lst)

    return joined
