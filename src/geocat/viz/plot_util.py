import matplotlib
import matplotlib.pyplot as plt
import xarray as xr
import numpy
import cartopy
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
import math
import typing
from textwrap import wrap
from metpy.calc import pressure_to_height_std
from abc import ABC, abstractmethod

from .util import set_titles_and_labels
from .util import add_major_minor_ticks
from .util import set_axes_limits_and_ticks


class NCL_Plot(ABC):
    """Parent class to create figure, axes, set NCL style with constructors to
    add colorbar, add titles, and show plot.Set up figure and axes with the
    specified style. Calls _set_up_fig if there is not a figure already
    created, _set_axes to create and style the axes, and _set_lim_ticks to
    constrain the axes. Adds geographic features to figure.

    Keyword Args
    ------------
    add_colorbar: :obj:`bool`
        Whether a colorbar is added to the figure. Default True.

    coastline_on: :obj:`bool`
        Whether to show coastlines in figure. Default False, unless a projection is specified.

    cb_draw_edges: :obj:`bool`
        Whether to draw edges on the colorbar. Default True.

    cb_orientation: :obj:`str`
        Placement of the colorbar. Default "horizontal". Other option is "vertical".

    cb_pad: :obj:`float`
        Padding between colorbar and figure. Default 0.11.

    cb_shrink: :obj:`float`
        Percent shrinkage of colorbar. Default 1.0.

    cb_tick_labels: :obj:`list` or :class:`numpy.ndarray`
        Labels for colorbar ticks.

    cb_tick_label_size: :obj:`int`
        Font size for colorbar tick labels.

    cb_ticks: :obj:`list` or :class:`numpy.ndarray`
        Ticks for colorbar.

    cmap: :obj:`str` or :class:`cmaps.colormap.Colormap`
        Colormap or colormap name for figure. Default 'plasma'

    h: :obj:`float`
        Height of figure in inches. Default 8. To be passed into figsize when creating figure.

    individual_cb: :obj:`bool`
        Whether to draw individual colorbars for each subplot. Default False.

    label_font_size: :obj:`int`
        Fontsize for x and y axis labels. Default 16.

    lakes_on: :obj:`bool`
        Whether to show lakes in figure. Default False.

    land_on: :obj:`bool`
        Whether to show land in figure. Default False.

    left_title: :obj:`str`
        Title for top left subtitle.

    left_title_fontsize: :obj:`int`
        Font size for top left subtitle. Default 18.

    line_color: :obj:`str` or :class:`Sequence`
        String of color name or sequence of colors. Default 'black'.

    line_style: :obj:`str`
        Style of lines. Options: {None, 'solid', 'dashed', 'dashdot', 'dotted'}, default None.

    line_width: :obj:`float`
        Width of lines. Default 0.4.

    main_title: :obj:`str`
        Title of figure.

    main_title_fontsize: :obj:`int`
        Font size for title of figure. Default 18.

    mappable: :class:`cartopy.mpl.contour.GeoContourSet`
        The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.

    minor_per_major: obj:`list`
        Number of minor ticks per major tick [x-axis, y-axis]. Default [3, 3] unless type="press_height", then default is [3, 1].

    overlay: :class:`contourf.Contour`
        Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the overlay would be the name of the first plot.

    projection: :obj:`str`
        Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

    raxis: :obj:`bool`
        Whether to add right hand axis. Default False, unless type is 'press_height'.

    raxis_label: :obj:`str`
        Label of right hand axis

    raxis_scale: :obj:`str`
        Scale of right hand axis.

    raxis_tick_label_fontsize: :obj:`float`
        Font size of tick labels on right hand axis.

    raxis_ticks: :obj:`list` or :class:`numpy.ndarray`
        Ticks for right hand axis.

    right_title: :obj:`str`
        Title for top right subtitle.

    right_title_fontsize: :obj:`int`
        Font size for top right subtitle. Default 18.

    set_extent: :class:`list`
        Extent [xmin, xmax, ymin, ymax] of figure to be shown.

    subplot: :class:`list`
        List [number of rows, number of columns, position] to be passed into plt.subplot().

    tick_label_fontsize: :obj:`int`
        Font size of x and y axis ticks. Default 16.

    type: :obj:`str`
        Type of figure. Currently supports 'press_height' for Pressure/Height diagrams.

    X: :class:`xarray.DataArray` or :class:`numpy.ndarray`
        Data for x axis.

    w: :obj:`float`
        Weidth of the figure. Default 10. To be passed into figsize.

    xlabel: :obj:`str`
        Label for the x axis.

    xlim: :class:`list`
        List [xmin, xmax] to set the limit of the x axis.

    xscale: :obj:`str`
        Scale of x axis. Currently supports "log".

    tick_label_fontsize: :obj:`int`
        Font size of x and y axis ticks. Default 16.

    xtick_labels: :obj:`list` or :class:`numpy.ndarray`
        List or array of tick labels for the x axis.

    xticks: :obj:`list` or :class:`numpy.ndarray`
        List or array of tick values for the x axis.

    Y: :class:`xarray.DataArray` or :class:`numpy.ndarray`
        Data for y axis.

    ylabel: :obj:`str`
        Label for the y axis.

    ylim: :class:`list`
        List [ymin, ymax] to set the limit of the y axis.

    yscale: :obj:`str`
        Scale of y axis. Currently supports "log".

    ytick_labels: :obj:`list` or :class:`numpy.ndarray`
        List or array of tick labels for the y axis.

    yticks: :obj:`list` or :class:`numpy.ndarray`
        List or array of tick values for the y axis.
    """

    # Constructor
    def __init__(self, class_specific_kwargs_set: set,
                 class_specific_kwarg_defaults: dict, *args, **kwargs):
        """Sets up args and kwargs for figure. Calls _fig_ax to set up figure
        and axes, add_geo_features to add geographical features to the figure,
        and adds titles.

        Args
        ----
        class_specific_kwargs_list: :obj:`list`
            Set of valid kwargs specific to subclass, to be passed into _setup_args_kwargs

        class_specific_kwarg_defaults: :obj`dict`
            Dictionary of kwargs specific to subclass, to be passed into _setup_args_kwargs
        """
        # set up all args and kwargs
        self._setup_args_kwargs(class_specific_kwargs_set,
                                class_specific_kwarg_defaults, args, kwargs)

        # If there is a subplot, set up variables for it
        if self.subplot is not None:
            self._set_up_subplot()

        # If there is not a reference obj, create a new figure
        if self.userset_overlay is None:
            self._set_up_fig(w=self.w, h=self.h)

        # Set up axes with the specified style
        self._set_axes()

        # Add land, coastlines, or lakes if specified
        if self.land_on is True:
            self.show_land()

        if self.coastline_on is True:
            self.show_coastline()

        if self.lakes_on is True:
            self.show_lakes()

        # Set axis limits and ticks
        self._set_lim_ticks(self.ax)

        # Set up subplot colorbar axis
        if self.subplot is not None:
            self._create_subplot_cax()

        # Add titles to figure
        self.add_titles()

        # plot figure - call to child class
        self._plot()

        # Set figure in NCL style
        self._set_NCL_style(self.ax)

    @abstractmethod
    def _plot(self, *args, **kwargs):
        """Method in child class to plot figure (See contourf for example)"""
        pass

    @abstractmethod
    def _class_kwarg_handling(self, *args, **kwargs):
        """Method in child class to set class-specific args and kwargs (See
        contourf for example)"""
        pass

    def _setup_args_kwargs(self, class_specific_kwargs_set: set,
                           class_specific_kwarg_defaults: dict, args, kwargs):
        """Set up args and kwargs.

        Args
        ----
        class_specific_kwargs_set: :obj:`list`
            Set of valid kwargs specific to subclass

        class_specific_kwarg_defaults: :obj`dict`
            Dictionary of kwargs specific to subclass
        """

        # List of valid kwargs
        valid_kwargs = {
            'add_colorbar', 'coastline_on', 'cbar', 'cb_draw_edges',
            'cb_orientation', 'cb_pad', 'cb_shrink', 'cb_ticks',
            'cb_tick_labels', 'cb_tick_label_size', 'cmap', 'h',
            'individual_cb', 'label_font_size', 'lakes_on', 'land_on',
            'left_title', 'left_title_fontsize', 'line_color', 'line_style',
            'line_width', 'main_title', 'main_title_fontsize', 'mappable',
            'minor_per_major', "overlay", 'projection', 'raxis', 'raxis_label',
            'raxis_scale', 'raxis_tick_label_fontsize', 'raxis_ticks',
            'right_title', 'right_title_fontsize', "set_extent", "subplot",
            'tick_label_fontsize', 'type', 'w', 'X', 'xlabel', 'xlim', "xscale",
            'xticks', 'xtick_labels', 'Y', 'ylabel', 'ylim', "yscale", 'yticks',
            'ytick_labels'
        } | class_specific_kwargs_set

        # Dictionary of default values
        all_kwargs = {
            'cmap': 'plasma',
            'line_color': "black",
            'line_width': 0.4,
            'minor_per_major': [3, 3],
            'w': 8,
            'h': 8,
            'cb_orientation': "horizontal",
            'cb_shrink': 1.0,
            'cb_pad': 0.075,
            'cb_draw_edges': True,
            'xlim': [-180, 180],
            'ylim': [-90, 90]
        }

        overlay_keys = {}

        # add in class specific defaults
        all_kwargs.update(class_specific_kwarg_defaults)

        # Update dict to include inputted kwargs
        all_kwargs.update(kwargs)

        # Read in kwargs from overlay plot
        if kwargs.get('overlay') is not None:
            overlay_keys = kwargs.get('overlay').__dict__.keys()
            all_kwargs.update(
                (k, v)
                for k, v in kwargs.get('overlay').__dict__.items()
                if (k not in kwargs.keys()))

        # Create self.kwarg for all kwargs in valid_kwargs
        self.__dict__.update((k, None) for k in valid_kwargs)
        self.__dict__.update((k, v)
                             for k, v in all_kwargs.items()
                             if k in valid_kwargs or k in overlay_keys)

        # list of kwargs where original value set by user is needed
        user_set_kwargs = [
            'coastline_on', 'cb_shrink', 'h', 'label_font_size',
            'left_title_fontsize', 'main_title_fontsize', "overlay",
            'right_title_fontsize', 'tick_label_fontsize', 'w'
        ]

        # add user_set_kwargs with userset_ in front for user values
        self.__dict__.update(('userset_' + k, v)
                             for k, v in kwargs.items()
                             if k in user_set_kwargs)
        if self.overlay is None:
            self.__dict__.update(('userset_' + k, None)
                                 for k in user_set_kwargs
                                 if k not in kwargs.keys())

        # Print unused kwargs
        unused_kwargs = [
            unused for unused in kwargs if unused not in valid_kwargs
        ]
        if len(unused_kwargs) > 0:
            print("--------------UNUSED KWARGS--------------" +
                  "\n".join(unused_kwargs))

        # Pull out args from data
        self.data = args[0]

        # If xarray file, format as Numpy array
        if isinstance(self.data, xr.DataArray):
            self.orig = self.data
            self.data = self.data.values
            if self.X is None:
                self.__dict__.update({'X': self.orig.coords[self.orig.dims[1]]})
            if self.Y is None:
                self.__dict__.update({'Y': self.orig.coords[self.orig.dims[0]]})

        # Set up child class specific kwarg values
        self._class_kwarg_handling(args, kwargs)

    def _set_up_fig(self, w: float = None, h: float = None):
        """Create figure with subplots, if specified.

        Keyword Args
        ------------
        w: :obj:`float`
            Width of the figure. Default 10. To be passed into figsize.

        h: :obj:`float`
            Height of figure in inches. Default 8. To be passed into figsize when creating figure.
        """

        # If not a subplot, set up figure with specified width and height
        if self.subplot is None:
            self.fig = plt.figure(figsize=(w, h))

        # If a subplot, set figure and set of axes using plt.subplots and add projection if specified
        else:
            if self.projection is None:
                self.fig, self.axes = plt.subplots(
                    self.sp_rows,
                    self.sp_columns,
                    figsize=(w, h),
                    gridspec_kw=self._generate_gridspec_ratio(
                        self.sp_rows, self.sp_columns, self.cb_orientation))

            else:
                self.fig, self.axes = plt.subplots(
                    self.sp_rows,
                    self.sp_columns,
                    subplot_kw={"projection": self.projection},
                    figsize=(w, h),
                    gridspec_kw=self._generate_gridspec_ratio(
                        self.sp_rows, self.sp_columns, self.cb_orientation))

    def _generate_gridspec_ratio(self, rows: int, columns: int,
                                 cb_orientation: str):
        """Generate gridspec for subplots, with additional cax if there is a
        colorbar.

        Args
        ----
        cb_orientation: :obj:`str`
            Placement of the colorbar. Default "horizontal". Other option is "vertical".

        columns: :obj:`int`
            Number of columns in the subplot.

        rows: :obj:`int`
            Number of rows in the subplot.
        """

        height_list = [1] * rows
        width_list = [1] * columns

        if (self.add_colorbar is not False) and (self.individual_cb
                                                 is not True):
            if (cb_orientation == "horizontal") or (cb_orientation is None):
                height_list[-1] = 0.1
            elif cb_orientation == "vertical":
                width_list[-1] = 0.1

        return {'height_ratios': height_list, 'width_ratios': width_list}

    def _create_subplot_cax(self):
        """Create the colorbar subplot axis when there is a subplot with a
        colorbar."""

        # If adding a colorbar, create colorbar axis
        if (
                self.add_colorbar != 'off'
        ) and self.add_colorbar is not False and self.individual_cb is not True:

            # If a 2D subplot configuration, calculate array index from subplot position
            if self.sp_columns != 1 and self.sp_rows != 1:

                # Generate gridspec for bottom right subplot
                gs = self.axes[-1, -1].get_gridspec()

                # If a horizontal colorbar, join last row of subplots into one as the colorbar axis
                if (self.cb_orientation
                        == "horizontal") or (self.cb_orientation is None):
                    # Turn off axes in last row so they do not show under colorbar
                    for ax in self.axes[-1, :]:
                        ax.axis("off")
                    # Add a subplot that encompasses the entire last row
                    self.cax = self.fig.add_subplot(gs[-1, :])
                # If a vertical colorbar, join last column of subplots into one as the colorbar axis
                elif self.cb_orientation == "vertical":
                    # Turn off axes in last column so they do not show under colorbar
                    for ax in self.axes[:, -1]:
                        ax.axis("off")
                    # Add a subplot that encompasses the entire last column
                    self.cax = self.fig.add_subplot(gs[:, -1])
            else:
                # If not a 2D subplot, set final axis in the list of axes as the colorbar axis
                self.cax = self.axes[-1]

                # Configure axis
                self.cax.set_aspect("auto")
                self._set_lim_ticks(self.cax)

    def _set_axes(self):
        """Assign value for self.ax by either creating a new axis or
        referencing the list of axes (self.axes) generated during subplot
        creation."""

        # If there is not reference figure, either get axis from plt.subplot or create axis
        if self.overlay is None:
            if self.subplot is not None:

                # Set the axis as a axis from axes array or grid
                self.ax = self.axes[self._subplot_pos()]
            else:
                # Create axes and if there a projection, set it during creation
                if self.projection is None:
                    self.ax = plt.axes()
                else:
                    self.ax = plt.axes(projection=self.projection)
        # If there is a reference figure, get the axes from the overlayure
        else:
            if self.subplot is not None:
                # Set the axis as a axis from axes array or grid
                self.ax = self.overlay.axes[self._subplot_pos()]

        # Set the aspect to auto to correct sizing
        self.ax.set_aspect("auto")

        # Set up axes with scale if specified/needed
        if self.yscale == "log":
            self.ax.set_yscale("log")

        if self.xscale == "log":
            self.ax.set_xscale("log")

        # If there is a projection, add coastlines to the figure as long as it is not specified not to
        if self.projection is not None:
            if self.userset_coastline_on is not False:
                self.ax.coastlines(linewidths=0.5, alpha=0.6)

    def _set_NCL_style(self,
                       ax: typing.Union[matplotlib.axes.Axes,
                                        cartopy.mpl.geoaxes.GeoAxes],
                       tick_label_fontsize: int = 16):
        """Set tick label size, add minor ticks, and format axes as latitude
        and longitude.

        Args
        ----
        ax: :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxes`
            Axis to apply NCL style to.

        Keyword Args
        ------------
        tick_label_fontsize: :obj:`int`
            Font size of x and y axis ticks. Default 16.
        """
        # Set NCL-style tick marks
        if self.tick_label_fontsize is None:
            self.tick_label_fontsize = tick_label_fontsize

        # if pressure height, don't add minor ticks to y-axis
        if self.type == 'press_height':
            self.minor_per_major[1] = 1

        add_major_minor_ticks(ax,
                              labelsize=str(self.tick_label_fontsize),
                              x_minor_per_major=self.minor_per_major[0],
                              y_minor_per_major=self.minor_per_major[1])

        # if pressure height, remove right hand ticks on original axis
        if self.type == "press_height":
            self.ax.tick_params(axis='y', right=False)

        # Perform same action as add_lat_lon_ticklabels geocat-viz utility function
        if 'on' in self.X.name:
            self.ax.xaxis.set_major_formatter(LongitudeFormatter())

        if self.type is None and 'at' in self.Y.name:
            self.ax.yaxis.set_major_formatter(LatitudeFormatter())

        # if x axis is latitude, set as latitude
        if 'at' in self.X.name:
            self.ax.xaxis.set_major_formatter(LatitudeFormatter())

    def _set_lim_ticks(self, ax: typing.Union[matplotlib.axes.Axes,
                                              cartopy.mpl.geoaxes.GeoAxes]):
        """Set limits and ticks for axis.

        Args
        ----
        ax: :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxes`
            Axis to apply NCL style to.
        """
        # if there is not a projection
        if self.projection is not None:
            # Use X and Y to set x and y limits if needed
            if self.ylim is None:
                self.ylim = (round(self.Y.data[0],
                                   -1), round(self.Y.data[-1], -1))

            if self.xlim is None:
                self.xlim = (round(self.X.data[0],
                                   -1), round(self.X.data[-1], -1))

            # If x and y ticks are not specified
            if self.xticks is None:
                # if the range is greater than 45 degrees, make ticks every 30 deg
                if (self.xlim[1] - self.xlim[0]) > 45:
                    self.xticks = numpy.arange(self.xlim[0], self.xlim[1] + 30,
                                               30)
                # else, make ticks every 15 deg
                else:
                    self.xticks = numpy.arange(self.xlim[0], self.xlim[1] + 15,
                                               15)

            if self.yticks is None:
                # if the range is greater than 45 degrees, make ticks every 30 deg
                if (self.ylim[1] - self.ylim[0]) > 45:
                    self.yticks = numpy.arange(self.ylim[0], self.ylim[1] + 30,
                                               30)
                # else, make ticks every 15 deg
                else:
                    self.yticks = numpy.arange(self.ylim[0], self.ylim[1] + 15,
                                               15)

            # if there is no set width or height
            if self.userset_w is None and self.userset_h is None:
                # get the ratio of x and y limits
                if self.subplot is None:
                    ratio = (self.ylim[1] - self.ylim[0]) / (self.xlim[1] -
                                                             self.xlim[0])
                    self.w = 6 / ratio
                    self.h = 6
                else:
                    ratio = (self.ylim[1] - self.ylim[0]) / (self.xlim[1] -
                                                             self.xlim[0])
                    self.w = 6 / ratio * self.sp_columns
                    self.h = 6 * self.sp_rows
                # set figure based on ratio
                self.fig.set_size_inches(self.w, self.h)

        # If xlim/ylim is not specified, set it to the mix and max of the data
        else:
            if self.ylim is None:
                self.ylim = ax.get_ylim()[::-1]

            if self.xlim is None:
                self.xlim = ax.get_xlim()[::-1]

            # If x and y ticks are not specified, set to have 5 ticks over full range
            if self.xticks is None:
                self.xticks = numpy.linspace(self.xlim[0], self.xlim[1], 5)

            if self.yticks is None:
                self.yticks = numpy.linspace(self.ylim[0], self.ylim[1], 5)

        # Use utility function to set axis limits and ticks
        set_axes_limits_and_ticks(ax,
                                  xlim=self.xlim,
                                  ylim=self.ylim,
                                  xticks=self.xticks,
                                  yticks=self.yticks,
                                  yticklabels=self.ytick_labels,
                                  xticklabels=self.xtick_labels)

        # Add right hand axis
        if self.raxis is True or (self.type == "press_height" and
                                  self.overlay is None):
            # Calculate pressure and height
            pressure = self.orig.lev
            height = pressure_to_height_std(pressure)

            # Set up axis, with allowing for user inputs
            axRHS = ax.twinx()
            if self.raxis_scale is None:
                axRHS.set_yscale("linear")
            else:
                axRHS.set_yscale(self.raxis_scale)

            if self.raxis_label is None:
                axRHS.set_ylabel('Height (km)')
            else:
                axRHS.set_ylabel(self.raxis_label)

            if self.raxis_ticks is None:
                axRHS.set_ylim(numpy.min(height.values),
                               numpy.max(height.values))
            else:
                axRHS.set_ylim(numpy.min(self.raxis_ticks),
                               numpy.max(self.raxis_ticks))

            if self.label_font_size is not None:
                axRHS.yaxis.label.set_size(self.label_font_size)
            else:
                axRHS.yaxis.label.set_size(18)

            if self.raxis_tick_label_fontsize is None:
                axRHS.tick_params('both', labelsize=18)
            else:
                axRHS.tick_params('both',
                                  labelsize=self.raxis_tick_label_fontsize)

    def _subplot_pos(self):
        """Convert the position of a subplot to its subplot array index."""

        # If the cb_orientation is vertical, the number of rows should be used to calculate the array index.
        # Otherwise, the number of columns should be used.
        if self.cb_orientation == "vertical":
            iterate = self.sp_rows
        else:
            iterate = self.sp_columns

        # If a 2D array, find the index position
        if self.sp_columns != 1 and self.sp_rows != 1:

            # Calculate the array indices
            row_position = math.trunc((self.subplot[2] - 1) / iterate)
            pos_remain = (self.subplot[2] - 1) % iterate

            # Change the position of the index depending on the colorbar orientation
            if self.cb_orientation == "vertical":
                return pos_remain, row_position
            else:
                return row_position, pos_remain
        else:
            # If not a 2D array, return the subplot position minus 1 to account for indexing at 0
            return self.subplot[2] - 1

    def _set_up_subplot(self):
        """Find the number of rows and columns needed in the subplot, taking in
        the colorbar cax into account."""

        if self.overlay is None:
            # Set up variable for rows and columns of subplot by pulling values from subplot list
            self.sp_rows = self.subplot[0]
            self.sp_columns = self.subplot[1]

            # If there is a colorbar, add an additional row or column, depending on cb_orientation
            if (self.add_colorbar
                    is not False) and (self.add_colorbar != 'off'):
                if (self.cb_orientation is not None) and (
                        self.cb_orientation == "vertical"
                        # or self.overlay.cb_orientation == "vertical"
                ):
                    self.sp_columns += 1
                else:
                    self.sp_rows += 1

    def show_land(self, scale: str = "110m", fc: str = 'lightgrey'):
        """Add land to figure.

        Keyword Args
        ------------
        fc: :obj:`str`
            Facecolor of land. Default light grey.

        scale: :obj:`str`
            Scale of land set. Default 110m.
        """
        # Add land to figure
        self.ax.add_feature(cfeature.LAND.with_scale(scale), facecolor=fc)

    def show_coastline(self,
                       scale: str = "110m",
                       lw: float = 0.5,
                       ec: str = "black"):
        """Add coastlines to figure.

        Keyword Args
        ------------
        ec: :obj:`str`
            Edgecolor of coastlines. Default black.

        lw: :obj:`float`
            Linewidth of coastlines. Default 0.5.

        scale: :obj:`str`
            Scale of coastline set. Default 110m.
        """
        # Add coastline to figure
        self.ax.add_feature(cfeature.COASTLINE.with_scale(scale),
                            linewidths=lw,
                            edgecolor=ec)

    def show_lakes(self,
                   scale: str = "110m",
                   lw: float = 0.5,
                   ec: str = 'black',
                   fc: str = 'None'):
        """Add lakes to figure.

        Keyword Args
        ------------
        ec: :obj:`str`
            Outline color of lakes. Default black.

        fc: :obj:`str`
            Facecolor of lakes. Default none.

        lw: :obj:`float`
            Linewidth of lake edges. Default 0.5.

        scale: :obj:`str`
            Scale of lake set. Default 110m.
        """
        # Add lakes to figure
        self.ax.add_feature(cfeature.LAKES.with_scale(scale),
                            linewidth=lw,
                            edgecolor=ec,
                            facecolor=fc)

    def add_colorbar(self,
                     mappable: cartopy.mpl.contour.GeoContourSet = None,
                     cb_orientation: str = "horizontal",
                     cb_shrink: float = 1.0,
                     cb_pad: float = 0.075,
                     cb_draw_edges: bool = True,
                     cb_ticks: typing.Union[list, numpy.ndarray] = None,
                     cb_tick_labels: typing.Union[list, numpy.ndarray] = None,
                     cb_tick_label_size: int = None):
        """Add colorbar to figure. If figure is a subplot, uses gridspec to add
        a cax to the appropriate place on the figure.

        Keyword Args
        ------------
        cb_draw_edges: :obj:`bool`
            Whether to draw edges on the colorbar. Default True.

        cb_orientation: :obj:`str`
            Placement of the colorbar. Default "horizontal". Other option is "vertical".

        cb_pad: :obj:`float`
            Padding between colorbar and figure. Default 0.11.

        cb_shrink: :obj:`float`
            Percent shrinkage of colorbar. Default 1.0.

        cb_tick_labels: :obj:`list` or :class:`numpy.ndarray`
            Labels for colorbar ticks.

        cb_tick_label_size: :obj:`int`
            Font size for colorbar tick labels.

        cb_ticks: :obj:`list` or :class:`numpy.ndarray`
            Ticks for colorbar.

        mappable: :class:`cartopy.mpl.contour.GeoContourSet`
            The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
        """

        # Set values for colorbar arguments while maintaining potential previously set values
        if self.cbar is not None:
            self.cbar.remove()

        if mappable is not None:
            self.mappable = mappable

        if (self.cb_orientation is None) or (cb_orientation != "horizontal"):
            self.cb_orientation = cb_orientation

        if (self.cb_shrink is None) or (cb_shrink != 1.0):
            self.cb_shrink = cb_shrink

        if (self.cb_pad is None) or (cb_pad != 0.075):
            self.cb_pad = cb_pad

        if (self.cb_draw_edges is None) or (cb_draw_edges is not True):
            self.cb_draw_edges = cb_draw_edges

        if cb_ticks is not None:
            self.cb_ticks = cb_ticks

        if cb_tick_labels is not None:
            self.cb_tick_labels = cb_tick_labels

        if cb_tick_label_size is not None:
            self.cb_tick_label_size = cb_tick_label_size

        # If there is not a mappable, raise error
        if self.mappable is None:
            raise AttributeError(
                "Mappable must be defined when first creating colorbar.")

        # If there is no subplot, create colorbar without specifying axis
        if (self.subplot is None) or (self.individual_cb is True):
            self.cbar = self.fig.colorbar(self.mappable,
                                          ax=self.ax,
                                          orientation=self.cb_orientation,
                                          shrink=self.cb_shrink,
                                          pad=self.cb_pad,
                                          drawedges=self.cb_draw_edges)
        # If subplot, specify caxis as the extra subplot added during figure creation
        else:
            self.cbar = self.fig.colorbar(self.mappable,
                                          cax=self.cax,
                                          orientation=self.cb_orientation)

        # Set colorbar ticks as the boundaries of the cbar
        if (cb_ticks is None) and (self.cb_ticks is None):
            if isinstance(self.levels, int):
                self.cb_ticks = numpy.linspace(
                    self.cbar.get_ticks()[0],
                    self.cbar.get_ticks()[-1],
                    len(self.cbar.get_ticks()) * 2 - 1)
                self.cb_tick_labels = list(self.cb_ticks.astype(int))
            else:
                try:  # duck typing list
                    self.cb_ticks = self.levels[1:-1]
                    self.cb_tick_labels = [
                        round(num, 2) for num in self.cb_ticks
                    ]
                except:
                    self.cb_ticks = numpy.linspace(
                        self.cbar.get_ticks()[0],
                        self.cbar.get_ticks()[-1],
                        len(self.cbar.get_ticks()) * 2 - 1)[1:]
                    self.cb_tick_labels = list(self.cb_ticks.astype(int))

        # Label every boundary except the ones on the end of the colorbar
        self.cbar.set_ticks(ticks=self.cb_ticks)

        # Set colorbar tick labels
        if self.cb_tick_labels is not None:
            self.cbar.set_ticklabels(ticklabels=self.cb_tick_labels)

        # Set label size of cbar ticks
        if self.cb_tick_label_size is not None:
            self.cbar.ax.tick_params(labelsize=self.cb_tick_label_size)
        elif (self.tick_label_fontsize - 10) >= 4:
            self.cbar.ax.tick_params(labelsize=self.tick_label_fontsize - 2)

    def add_titles(self,
                   main_title: str = None,
                   main_title_fontsize: int = 18,
                   left_title: str = None,
                   left_title_fontsize: int = 18,
                   right_title: str = None,
                   right_title_fontsize: int = 18,
                   xlabel: str = None,
                   ylabel: str = None,
                   label_font_size: int = 16):
        """Add titles to figure. If inputted dataset is an xarray file (or
        netCDF converted to xarray), will attempt to pull titles and labels
        from the datafile.

        Keyword Args
        ------------
        label_font_size: :obj:`int`
            Fontsize for x and y axis labels. Default 16.

        left_title: :obj:`str`
            Title for top left subtitle.

        left_title_fontsize: :obj:`int`
            Font size for top left subtitle. Default 18.

        main_title: :obj:`str`
            Title of figure.

        main_title_fontsize: :obj:`int`
            Font size for title of figure. Default 18.

        right_title: :obj:`str`
            Title for top right subtitle.

        right_title_fontsize: :obj:`int`
            Font size for top right subtitle. Default 18.

        xlabel: :obj:`str`
            Label for the x axis.

        ylabel: :obj:`str`
            Label for the y axis.
        """

        # Update argument definitions while maintaining potential previously set values
        if main_title is not None:
            self.main_title = main_title

        if (main_title_fontsize != 18) or (self.main_title_fontsize is None):
            self.main_title_fontsize = main_title_fontsize

        if left_title is not None:
            self.left_title = left_title

        if (left_title_fontsize != 18) or (self.left_title_fontsize is None):
            self.left_title_fontsize = left_title_fontsize

        if right_title is not None:
            self.right_title = right_title

        if (right_title_fontsize != 18) or (self.right_title_fontsize is None):
            self.right_title_fontsize = right_title_fontsize

        if xlabel is not None:
            self.xlabel = xlabel

        if ylabel is not None:
            self.ylabel = ylabel

        if (label_font_size != 16) or (self.label_font_size is None):
            self.label_font_size = label_font_size

        # If xarray file, try to use labels within file
        if isinstance(self.orig, xr.core.dataarray.DataArray):
            if self.main_title is None:
                # Attempt to set title from file if title is not specified
                try:
                    self.main_title = self.orig.attrs["title"]
                except:
                    pass
            if self.left_title is None:
                # Attempt to set left title as the long name from file if left title is not specified
                try:
                    self.left_title = self.orig.attrs["long_name"]
                except:
                    pass
            if self.right_title is None:
                # Attempt to set right title as units from file if right title is not specified
                try:
                    self.right_title = self.orig.attrs["units"]
                except:
                    pass

            # Set variables to find x and y labels
            first = True
            coordinates = self.orig.coords
            keys = list(coordinates.keys())

            # Set x and y label as defined if specified
            if self.X is not None:
                # Attempt to set x axis label if X is specified as a kwarg
                try:
                    if self.xlabel is None and hasattr(
                            self.X,
                            'long_name') and "ongitude" not in self.X.long_name:
                        self.xlabel = self.X.long_name
                except:
                    pass

            if self.Y is not None:
                # Attempt to set y axis label if Y is specified as a kwarg
                try:
                    if self.ylabel is None and hasattr(
                            self.X,
                            'long_name') and "atitude" not in self.Y.long_name:
                        self.ylabel = self.Y.long_name
                except:
                    pass

            # Loop through coordinates in xarray file to set y and x as the first two non-restricted coordinates, respectively
            for i in range(len(keys)):
                # If coordinate is first label with multiple values, set y label
                if (coordinates[keys[i - 1]].size > 1) and first:
                    try:
                        if self.ylabel is None and hasattr(
                                self.X, 'long_name'
                        ) and "atitude" not in self.Y.long_name:
                            self.ylabel = coordinates[keys[i - 1]].long_name
                    except:
                        pass

                    while i < len(keys):
                        # If coordinate is second label with multiple values, set x label
                        if (coordinates[keys[i]].size > 1) and first:
                            try:
                                if self.xlabel is None and hasattr(
                                        self.X, 'long_name'
                                ) and "ongitude" not in self.X.long_name:
                                    self.xlabel = coordinates[keys[i]].long_name
                            except:
                                pass
                            first = False
                        else:
                            i += 1
                else:
                    i += 1

        # Decrease default font size if necessary and set other font sizes based on main_title_fontsize
        if self.userset_main_title_fontsize is None and self.main_title is not None:
            while (len(
                    wrap(text=self.main_title,
                         width=round(self.w / self.main_title_fontsize * 100)))
                   > 1 and self.main_title_fontsize > 12):
                self.main_title_fontsize -= 1
            if self.userset_left_title_fontsize is None:
                self.left_title_fontsize = self.main_title_fontsize - 2
            if self.userset_right_title_fontsize is None:
                self.right_title_fontsize = self.main_title_fontsize - 2
            if self.userset_label_font_size is None:
                self.label_font_size = self.main_title_fontsize - 2
            if self.userset_tick_label_fontsize is None:
                self.tick_label_fontsize = self.main_title_fontsize - 2

        # Add titles with appropriate font sizes
        set_titles_and_labels(self.ax,
                              maintitle=self.main_title,
                              maintitlefontsize=self.main_title_fontsize,
                              lefttitle=self.left_title,
                              lefttitlefontsize=self.left_title_fontsize,
                              righttitle=self.right_title,
                              righttitlefontsize=self.right_title_fontsize,
                              xlabel=self.xlabel,
                              ylabel=self.ylabel,
                              labelfontsize=self.label_font_size)

    def show(self):
        """Display the plot."""
        # Try to show plot with tight_layout
        try:
            plt.tight_layout()
        except:
            pass

        plt.show()

    def savefig(self, filepath: str):
        """Save figure."""
        # try to prevent label cutoff
        try:
            plt.tight_layout()
        except:
            pass

        plt.savefig(filepath)

    def get_mpl_obj(self):
        """Get matplotlib object."""
        return self.fig
