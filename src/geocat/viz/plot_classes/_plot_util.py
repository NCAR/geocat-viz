import matplotlib
import matplotlib.pyplot as plt
import xarray as xr
import numpy
import numpy as np
import cartopy
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.feature as cfeature
import math
import typing
from textwrap import wrap
from metpy.units import units
import metpy
from metpy.calc import pressure_to_height_std, height_to_pressure_std
import pint



from geocat.viz.util import set_titles_and_labels
from geocat.viz.util import add_major_minor_ticks
from geocat.viz.util import set_axes_limits_and_ticks


class NCL_Plot():
    """Parent class to create figure, axes, set NCL style with constructors to
    add colorbar, add titles, and show plot.Set up figure and axes with the specified style. 
    Calls _set_up_fig if there is not a figure already created, _set_axes to create and style
    the axes, and _set_lim_ticks to constrain the axes. Adds geographic features
    to figure.

    Keyword Args
    ------------
    add_colorbar: :obj:`bool` 
        Whether a colorbar is added to the figure. Default True.

    cbdrawedges: :obj:`bool` 
        Whether to draw edges on the colorbar. Default True.

    cborientation: :obj:`str` 
        Placement of the colorbar. Default "horizontal". Other option is "vertical".

    cbpad: :obj:`float` 
        Padding between colorbar and figure. Default 0.11.

    cbshrink: :obj:`float` 
        Percent shrinkage of colorbar. Default 0.75.

    cbticklabels: :obj:`list` or :class:`numpy.ndarray` 
        Labels for colorbar ticks.

    cbtick_label_size: :obj:`int` 
        Font size for colorbar tick labels.

    cbticks: :obj:`list` or :class:`numpy.ndarray` 
        Ticks for colorbar.

    h: :obj:`float` 
        Height of figure in inches. Default 8. To be passed into figsize when creating figure.

    labelfontsize: :obj:`int` 
        Fontsize for x and y axis labels. Default 16.

    lefttitle: :obj:`str` 
        Title for top left subtitle.

    lefttitlefontsize: :obj:`int` 
        Font size for top left subtitle. Default 18.

    maintitle: :obj:`str` 
        Title of figure.

    maintitlefontsize: :obj:`int` 
        Font size for title of figure. Default 18.

    mappable: :class:`cartopy.mpl.contour.GeoContourSet` 
        The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
    
    projection: :obj:`str` 
        Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

    overlay: :class:`contourf.Contour` 
        Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the overlay would be the name of the first plot.

    righttitle: :obj:`str` 
        Title for top right subtitle.

    righttitlefontsize: :obj:`int` 
        Font size for top right subtitle. Default 18.
    
    set_extent: :class:`list` 
        Extent [xmin, xmax, ymin, ymax] of figure to be shown.
    
    show_coastline: :obj:`bool` 
        Whether to show coastlines in figure. Default False, unless a projection is specified.

    show_lakes: :obj:`bool` 
        Whether to show lakes in figure. Default False.

    show_land: :obj:`bool` 
        Whether to show land in figure. Default false.

    subplot: :class:`list` 
        List [number of rows, number of columns, position] to be passed into plt.subplot().

    tick_label_fontsize: :obj:`int` 
        Font size of x and y axis ticks. Default 16.
    
    w: :obj:`float` 
        Weidth of the figure. Default 10. To be passed into figsize.
    
    x_label_lon: :obj:`bool` 
        Format the x axis as longitude values. Default True.

    xlabel: :obj:`str` 
        Label for the x axis.
    
    xlim: :class:`list` 
        List [xmin, xmax] to set the limit of the x axis.

    xscale: :obj:`str` 
        Scale of x axis. Currently supports "log".

    tick_label_fontsize: :obj:`int` 
        Font size of x and y axis ticks. Default 16.

    xticklabels: :obj:`list` or :class:`numpy.ndarray` 
        List or array of tick labels for the x axis.

    xticks: :obj:`list` or :class:`numpy.ndarray` 
        List or array of tick values for the x axis.

    y_label_lat: :obj:`bool` 
        Format the y axis as latitude values. Default True.

    ylabel: :obj:`str` 
        Label for the y axis.
    
    ylim: :class:`list` 
        List [ymin, ymax] to set the limit of the y axis.

    yscale: :obj:`str` 
        Scale of y axis. Currently supports "log".

    yticklabels: :obj:`list` or :class:`numpy.ndarray` 
        List or array of tick labels for the y axis.

    yticks: :obj:`list` or :class:`numpy.ndarray` 
        List or array of tick values for the y axis.
    """

    # Constructor
    def __init__(self, *args, **kwargs):
        """Pulls kwargs for colorbar and titles. Calls _fig_ax to set up figure
        and axes, add_geo_features to add geographical features to the figure,
        and adds titles.

        Keyword Args
        ------------
        add_colorbar: :obj:`bool` 
            Whether a colorbar is added to the figure. Default True.

        cbdrawedges: :obj:`bool` 
            Whether to draw edges on the colorbar. Default True.

        cborientation: :obj:`str` 
            Placement of the colorbar. Default "horizontal". Other option is "vertical".

        cbpad: :obj:`float` 
            Padding between colorbar and figure. Default 0.11.

        cbshrink: :obj:`float` 
            Percent shrinkage of colorbar. Default 0.75.

        cbticklabels: :obj:`list` or :class:`numpy.ndarray` 
            Labels for colorbar ticks.

        cbtick_label_size: :obj:`int` 
            Font size for colorbar tick labels.

        cbticks: :obj:`list` or :class:`numpy.ndarray` 
            Ticks for colorbar.

        h: :obj:`float` 
            Height of figure in inches. Default 8. To be passed into figsize when creating figure.

        labelfontsize: :obj:`int` 
            Fontsize for x and y axis labels. Default 16.

        lefttitle: :obj:`str` 
            Title for top left subtitle.

        lefttitlefontsize: :obj:`int` 
            Font size for top left subtitle. Default 18.

        maintitle: :obj:`str` 
            Title of figure.

        maintitlefontsize: :obj:`int` 
            Font size for title of figure. Default 18.

        mappable: :class:`cartopy.mpl.contour.GeoContourSet` 
            The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
        
        projection: :obj:`str` 
            Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

        overlay: :class:`contourf.Contour` 
            Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the overlay would be the name of the first plot.

        righttitle: :obj:`str` 
            Title for top right subtitle.

        righttitlefontsize: :obj:`int` 
            Font size for top right subtitle. Default 18.
        
        set_extent: :class:`list` 
            Extent [xmin, xmax, ymin, ymax] of figure to be shown.
        
        show_coastline: :obj:`bool` 
            Whether to show coastlines in figure. Default False, unless a projection is specified.

        show_lakes: :obj:`bool` 
            Whether to show lakes in figure. Default False.

        show_land: :obj:`bool` 
            Whether to show land in figure. Default false.

        subplot: :class:`list` 
            List [number of rows, number of columns, position] to be passed into plt.subplot().

        tick_label_fontsize: :obj:`int` 
            Font size of x and y axis ticks. Default 16.
        
        w: :obj:`float` 
            Weidth of the figure. Default 10. To be passed into figsize.
        
        x_label_lon: :obj:`bool` 
            Format the x axis as longitude values. Default True.

        xlabel: :obj:`str` 
            Label for the x axis.
        
        xlim: :class:`list` 
            List [xmin, xmax] to set the limit of the x axis.

        xscale: :obj:`str` 
            Scale of x axis. Currently supports "log".

        tick_label_fontsize: :obj:`int` 
            Font size of x and y axis ticks. Default 16.

        xticklabels: :obj:`list` or :class:`numpy.ndarray` 
            List or array of tick labels for the x axis.

        xticks: :obj:`list` or :class:`numpy.ndarray` 
            List or array of tick values for the x axis.

        y_label_lat: :obj:`bool` 
            Format the y axis as latitude values. Default True.

        ylabel: :obj:`str` 
            Label for the y axis.
        
        ylim: :class:`list` 
            List [ymin, ymax] to set the limit of the y axis.

        yscale: :obj:`str` 
            Scale of y axis. Currently supports "log".

        yticklabels: :obj:`list` or :class:`numpy.ndarray` 
            List or array of tick labels for the y axis.

        yticks: :obj:`list` or :class:`numpy.ndarray` 
            List or array of tick values for the y axis.
        """

        # If there is a subplot, set up variables for it
        if self.subplot is not None:
            self._set_up_subplot()

        # If there is not a reference obj, create a new figure
        if kwargs.get('overlay') is None:
            self._set_up_fig(w=self.w, h=self.h)

        # Set up axes with the specified style
        self._set_axes()

        # Add land, coastlines, or lakes if specified
        if self.show_land is True:
            self.show_land()

        if self.show_coastline is True:
            self.show_coastline()

        if self.show_lakes is True:
            self.show_lakes()

        # Set axis limits and ticks
        self._set_lim_ticks(self.ax, kwargs)

        if self.subplot is not None:
            self._create_subplot_cax()

        # Add titles to figure
        self.add_titles()

    def _setup_args_kwargs(self, class_specific_kwargs_set : set, class_specific_kwarg_defaults : dict, *args, **kwargs):
        """Set up args and kwargs

        Args
        ----
        class_specific_kwargs_list: :obj:`list`
            Set of valid kwargs specific to subclass

        class_specific_kwarg_defaults: :obj`dict`
            Dictionary of kwargs specific to subclass
        """

        # List of valid kwargs
        valid_kwargs = {'add_colorbar', 'cbar', 'cbdrawedges', 'cborientation', 
            'cbpad', 'cbshrink', 'cbticks', 'cbticklabels', 'cbtick_label_size', 
            'cmap', 'labelfontsize', 'lefttitle', 'lefttitlefontsize', 
            'line_color', 'line_style', 'line_width', 'h', 'individual_cb', 
            'maintitle', 'maintitlefontsize', 'mappable', "overlay", 'projection',  
            'righttitle', 'righttitlefontsize', "set_extent", "subplot", 
            'tick_label_fontsize', 'type', 'w', 'X',  'xlabel', 'xlim', 
            "xscale", 'xticks', 'xticklabels', 'Y',  'ylabel', 
            'ylim', "yscale", 'yticks', 'yticklabels'} | class_specific_kwargs_set

        # Dictionary of default values
        all_kwargs = {'cmap' : 'coolwarm', 'line_color' : "black", 
            'line_width' : 0.4, 'w' : 8, 'h': 8, 'cborientation' : "horizontal",
            'cbshrink' : 0.75, 'cbpad' : 0.075, 'cbdrawedges' : True, 'xlim': [-180,180],
            'ylim': [-90,90]}

        overlay_keys = {}

        # add in class specific defaults
        all_kwargs.update(class_specific_kwarg_defaults)

        # Update dict to include inputted kwargs
        all_kwargs.update(kwargs)

        # Read in kwargs from overlay plot
        if kwargs.get('overlay') is not None:
            overlay_keys = kwargs.get('overlay').__dict__.keys()
            all_kwargs.update((k,v) for k, v in kwargs.get('overlay').__dict__.items() if (k not in kwargs.keys()))

        # Create self.kwarg for all kwargs in valid_kwargs
        self.__dict__.update((k, None) for k in valid_kwargs)
        self.__dict__.update((k, v) for k, v in all_kwargs.items() if k in valid_kwargs or k in overlay_keys)
        
        # Print unused kwargs
        unused_kwargs = [unused for unused in kwargs if unused not in valid_kwargs]
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
                self.__dict__.update({'X' : self.orig.coords[self.orig.dims[1]]})
            if self.Y is None:
                self.__dict__.update({'Y': self.orig.coords[self.orig.dims[0]]})

    def _set_up_fig(self, w: float =None, h: float =None):
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
                        self.sp_rows, self.sp_columns, self.cborientation))

            else:
                self.fig, self.axes = plt.subplots(
                    self.sp_rows,
                    self.sp_columns,
                    subplot_kw={"projection": self.projection},
                    figsize=(w, h),
                    gridspec_kw=self._generate_gridspec_ratio(
                        self.sp_rows, self.sp_columns, self.cborientation))
                    

    def _generate_gridspec_ratio(self, rows: int, columns: int, cborientation: str):
        """Generate gridspec for subplots, with additional cax if there is a
        colorbar.

        Args
        ----
        cborientation: :obj:`str` 
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
            if (cborientation == "horizontal") or (cborientation is None):
                height_list[-1] = 0.1
            elif (cborientation == "vertical"):
                width_list[-1] = 0.1

        return {'height_ratios': height_list, 'width_ratios': width_list}

    def _create_subplot_cax(self, *args, **kwargs):
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
                if (self.cborientation
                        == "horizontal") or (self.cborientation is None):
                    # Turn off axes in last row so they do not show under colorbar
                    for ax in self.axes[-1, :]:
                        ax.axis("off")
                    # Add a subplot that encompasses the entire last row
                    self.cax = self.fig.add_subplot(gs[-1, :])
                # If a vertical colorbar, join last column of subplots into one as the colorbar axis
                elif (self.cborientation == "vertical"):
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
                self._set_lim_ticks(self.cax, kwargs)

    def _set_axes(self, *args, **kwargs):
        """Assign value for self.ax by either creating a new axis or
        referencing the list of axes (self.axes) generated during subplot
        creation.
        """

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
            if kwargs.get("show_coastlines") is not False:
                self.ax.coastlines(linewidths=0.5, alpha=0.6)

    def _set_NCL_style(self, ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxes], tick_label_fontsize: int =16):
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
            
        add_major_minor_ticks(ax, labelsize=self.tick_label_fontsize)

        # if pressure height, remove right hand ticks on original axis
        if self.type == "press_height":
            self.ax.tick_params(axis='y', right=False)

        # Perform same action as add_lat_lon_ticklabels geocat-viz utility function
        if 'on' in self.X.name:
            self.ax.xaxis.set_major_formatter(LongitudeFormatter())

        if 'at' in self.X.name:
            self.ax.xaxis.set_major_formatter(LatitudeFormatter())

        # only set yaxis NCL plot if type is none
        if self.type is None and 'at' in self.Y.name:
            self.ax.yaxis.set_major_formatter(LatitudeFormatter())


    def _set_lim_ticks(self, ax: typing.Union[matplotlib.axes.Axes, cartopy.mpl.geoaxes.GeoAxes], kwargs):
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
                self.ylim = (round(self.Y.data[0], -1), round(self.Y.data[-1], -1))

            if self.xlim is None:
                self.xlim = (round(self.X.data[0], -1), round(self.X.data[-1], -1))

            # If x and y ticks are not specified
            if self.xticks is None:
                # if the range is greater than 45 degrees, make ticks every 30 deg
                if (self.xlim[1] - self.xlim[0]) > 45:
                    self.xticks = np.arange(self.xlim[0], self.xlim[1] + 30, 30)
                # else, make ticks every 15 deg
                else:
                    self.xticks = np.arange(self.xlim[0], self.xlim[1] + 15, 15)

            if self.yticks is None:
                # if the range is greater than 45 degrees, make ticks every 30 deg
                if (self.ylim[1] - self.ylim[0]) > 45:
                    self.yticks = np.arange(self.ylim[0], self.ylim[1] + 30, 30)
                # else, make ticks every 15 deg
                else:
                    self.yticks = np.arange(self.ylim[0], self.ylim[1] + 15, 15)
            
            # if there is no set width or height
            if kwargs.get('w') is None and kwargs.get('h') is None:
                # get the ratio of x and y limits
                if self.subplot is None:
                    ratio = (self.ylim[1]-self.ylim[0])/(self.xlim[1]-self.xlim[0])
                    self.w = 6/ratio
                    self.h = 6
                else:
                    ratio = (self.ylim[1]-self.ylim[0])/(self.xlim[1]-self.xlim[0])
                    self.w = 6/ratio*self.sp_columns
                    self.h = 6*self.sp_rows
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
                self.xticks = np.linspace(self.xlim[0], self.xlim[1], 5)

            if self.yticks is None:
                self.yticks = np.linspace(self.ylim[0], self.ylim[1], 5)

        
        # Use utility function to set axis limits and ticks
        set_axes_limits_and_ticks(ax,
                                  xlim=self.xlim,
                                  ylim=self.ylim,
                                  xticks=self.xticks,
                                  yticks=self.yticks,
                                  yticklabels=self.yticklabels,
                                  xticklabels=self.xticklabels)


        if self.type == "press_height" and self.overlay is None:
            pressure = self.orig.lev
            height = pressure_to_height_std(pressure)


            axRHS = ax.twinx()
            axRHS.set_yscale("linear")
            axRHS.set_ylim(np.min(height.values), np.max(height.values))
            axRHS.set_ylabel('Height (km)')
            if self.labelfontsize is not None:
                axRHS.yaxis.label.set_size(self.labelfontsize)
            else: 
                axRHS.yaxis.label.set_size(18)
            axRHS.tick_params('both', labelsize=18)
        

    def _subplot_pos(self):
        """Convert the position of a subplot to its subplot array index.
        """

        # If the cborientation is vertical, the number of rows should be used to calculate the array index. Otherwise, the number of columns should be used.
        if self.cborientation == "vertical":
            iterate = self.sp_rows
        else:
            iterate = self.sp_columns

        # If a 2D array, find the index position
        if self.sp_columns != 1 and self.sp_rows != 1:

            # Calculate the array indices
            row_position = math.trunc((self.subplot[2] - 1) / iterate)
            pos_remain = (self.subplot[2] - 1) % iterate

            # Change the position of the index depending on the colorbar orientation
            if self.cborientation == "vertical":
                return (pos_remain, row_position)
            else:
                return (row_position, pos_remain)
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

            # If there is a colorbar, add an additional row or column, depending on cborientation
            if (self.add_colorbar
                    is not False) and (self.add_colorbar != 'off'):
                if (self.cborientation is not None) and (
                        self.cborientation == "vertical"
                        # or self.overlay.cborientation == "vertical"
                        ):
                    self.sp_columns += 1
                else:
                    self.sp_rows += 1
                    
    def show_land(self, scale: str ="110m", fc: str ='lightgrey'):
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

    def show_coastline(self, scale: str ="110m", lw: float =0.5, ec: str ="black"):
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

    def show_lakes(self, scale: str ="110m", lw: float =0.5, ec: str ='black', fc: str ='None'):
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
        
    def _add_colorbar(self,
                      mappable: cartopy.mpl.contour.GeoContourSet =None,
                      cborientation: str ="horizontal",
                      cbshrink: float =0.8,
                      cbpad: float = 0.075,
                      cbdrawedges: bool =True,
                      cbticks: typing.Union[list, numpy.ndarray] =None,
                      cbticklabels: typing.Union[list, numpy.ndarray] =None,
                      cbtick_label_size: int =None,
                      **kwargs):
        """Add colorbar to figure. If figure is a subplot, uses gridspec to add
        a cax to the appropriate place on the figure.

        Keyword Args
        ------------
        cbdrawedges: :obj:`bool` 
            Whether to draw edges on the colorbar. Default True.

        cborientation: :obj:`str` 
            Placement of the colorbar. Default "horizontal". Other option is "vertical".

        cbpad: :obj:`float` 
            Padding between colorbar and figure. Default 0.11.

        cbshrink: :obj:`float` 
            Percent shrinkage of colorbar. Default 0.75.

        cbticklabels: :obj:`list` or :class:`numpy.ndarray` 
            Labels for colorbar ticks.

        cbtick_label_size: :obj:`int` 
            Font size for colorbar tick labels.

        cbticks: :obj:`list` or :class:`numpy.ndarray` 
            Ticks for colorbar.

        mappable: :class:`cartopy.mpl.contour.GeoContourSet` 
            The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
        """

        # Set values for colorbar arguments while maintaining potential previously set values
        if self.cbar is not None:
            self.cbar.remove()

        if mappable is not None:
            self.mappable = mappable

        if (self.cborientation is None) or (cborientation != "horizontal"):
            self.cborientation = cborientation

        if (self.cbshrink is None) or (cbshrink != 0.75):
            self.cbshrink = cbshrink

        if (self.cbpad is None) or (cbpad != 0.075):
            self.cbpad = cbpad

        if (self.cbdrawedges is None) or (cbdrawedges is not True):
            self.cbdrawedges = cbdrawedges

        # If there is not a mappable, raise error
        if self.mappable is None:
            raise AttributeError(
                "Mappable must be defined when first creating colorbar.")

        if kwargs.get('cbshrink') is None and self.cborientation == 'vertical':
            self.cbshrink = 1

        # If there is no subplot, create colorbar without specifying axis
        if (self.subplot is None) or (self.individual_cb is True):
            self.cbar = self.fig.colorbar(self.mappable,
                                          ax=self.ax,
                                          orientation=self.cborientation,
                                          shrink=self.cbshrink,
                                          pad=self.cbpad,
                                          drawedges=self.cbdrawedges)
        # If subplot, specify caxis as the extra subplot added during figure creation
        else:
            self.cbar = self.fig.colorbar(self.mappable,
                                          cax=self.cax,
                                          orientation=self.cborientation)

        # Set colorbar ticks as the boundaries of the cbar
        if (cbticks is None) and (self.cbticks is None):
            if (isinstance(self.levels, int)):
                self.cbticks = np.linspace(self.cbar.get_ticks()[0],
                                        self.cbar.get_ticks()[-1],
                                        len(self.cbar.get_ticks())*2 - 1)
                self.cbticklabels = list(self.cbticks.astype(int))
            else:
                try: # duck typing list
                    self.cbticks = self.levels[1:-1]
                    self.cbticklabels = [round(num,2) for num in self.cbticks]
                except:
                    self.cbticks = np.linspace(self.cbar.get_ticks()[0],
                                                self.cbar.get_ticks()[-1],
                                                len(self.cbar.get_ticks())*2 - 1)[1:]
                    self.cbticklabels = list(self.cbticks.astype(int))

        # Label every boundary except the ones on the end of the colorbar
        self.cbar.set_ticks(ticks=self.cbticks)

        # Set colorbar tick labels
        if self.cbticklabels is not None:
            self.cbar.set_ticklabels(ticklabels=self.cbticklabels)

        # Set label size of cbar ticks
        if self.cbtick_label_size is not None:
            self.cbar.ax.tick_params(labelsize=self.cbtick_label_size)
        elif (self.tick_label_fontsize - 10) >= 4:
            self.cbar.ax.tick_params(labelsize=self.tick_label_fontsize - 2)

    def add_titles(self,
                   maintitle: str =None,
                   maintitlefontsize: int =18,
                   lefttitle: str =None,
                   lefttitlefontsize: int =18,
                   righttitle: str =None,
                   righttitlefontsize: int=18,
                   xlabel: str =None,
                   ylabel: str =None,
                   labelfontsize: int =16,
                   **kwargs):
        """Add titles to figure. If inputted dataset is an xarray file (or
        netCDF converted to xarray), will attempt to pull titles and labels
        from the datafile.

        Keyword Args
        ------------
        labelfontsize: :obj:`int` 
            Fontsize for x and y axis labels. Default 16.

        lefttitle: :obj:`str` 
            Title for top left subtitle.

        lefttitlefontsize: :obj:`int` 
            Font size for top left subtitle. Default 18.

        maintitle: :obj:`str` 
            Title of figure.

        maintitlefontsize: :obj:`int` 
            Font size for title of figure. Default 18.

        righttitle: :obj:`str` 
            Title for top right subtitle.

        righttitlefontsize: :obj:`int` 
            Font size for top right subtitle. Default 18.

        tick_label_fontsize: :obj:`int` 
            Font size of x and y axis ticks. Default 16.

        xlabel: :obj:`str` 
            Label for the x axis.

        ylabel: :obj:`str` 
            Label for the y axis.
        """

        # Update argument definitions while maintaining potential previously set values
        if maintitle is not None:
            self.maintitle = maintitle

        if (maintitlefontsize != 18) or (self.maintitlefontsize is None):
            self.maintitlefontsize = maintitlefontsize

        if lefttitle is not None:
            self.lefttitle = lefttitle

        if (lefttitlefontsize != 18) or (self.lefttitlefontsize is None):
            self.lefttitlefontsize = lefttitlefontsize

        if righttitle is not None:
            self.righttitle = righttitle

        if (righttitlefontsize != 18) or (self.righttitlefontsize is None):
            self.righttitlefontsize = righttitlefontsize

        if xlabel is not None:
            self.xlabel = xlabel

        if ylabel is not None:
            self.ylabel = ylabel

        if (labelfontsize != 16) or (self.labelfontsize is None):
            self.labelfontsize = labelfontsize

        # If xarray file, try to use labels within file
        if isinstance(self.orig, xr.core.dataarray.DataArray):
            if self.maintitle is None:
                # Attempt to set title from file if title is not specified
                try:
                    self.maintitle = self.orig.attrs["title"]
                except:
                    pass
            if self.lefttitle is None:
                # Attempt to set left title as the long name from file if left title is not specified
                try:
                    self.lefttitle = self.orig.attrs["long_name"]
                except:
                    pass
            if self.righttitle is None:
                # Attempt to set right title as units from file if right title is not specified
                try:
                    self.righttitle = self.orig.attrs["units"]
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
                    if self.xlabel is None and hasattr(self.X, 'long_name') and "ongitude" not in self.X.long_name:
                        self.xlabel = self.X.long_name
                except:
                    pass

            if self.Y is not None:
                # Attempt to set y axis label if Y is specified as a kwarg
                try:
                    if self.ylabel is None and hasattr(self.X, 'long_name') and "atitude" not in self.Y.long_name:
                        self.ylabel = self.Y.long_name
                except:
                    pass

            # Loop through coordinates in xarray file to set y and x as the first two non-restricted coordinates, respectively
            for i in range(len(keys)):
                # If coordinate is first label with multiple values, set y label
                if (coordinates[keys[i - 1]].size > 1) and first:
                    try:
                        if self.ylabel is None and hasattr(self.X, 'long_name') and "atitude" not in self.Y.long_name:
                            self.ylabel = coordinates[keys[i - 1]].long_name
                    except:
                        pass

                    while i < len(keys):
                        # If coordinate is second label with multiple values, set x label
                        if (coordinates[keys[i]].size > 1) and first:
                            try:
                                if self.xlabel is None and hasattr(self.X, 'long_name') and "ongitude" not in self.X.long_name:
                                    self.xlabel = coordinates[keys[i]].long_name
                            except:
                                pass
                            first = False
                        else:
                            i += 1
                else:
                    i += 1

        # Decrease default font size if necessary and set other font sizes based on maintitlefontsize
        if kwargs.get('maintitlefontsize') is None and self.maintitle is not None:
            while (
                len(wrap(text=self.maintitle, width=round(self.w/self.maintitlefontsize*100))) > 1
                and self.maintitlefontsize > 12):
                self.maintitlefontsize -=1
            if kwargs.get('lefttitlefontsize') is None:
                self.lefttitlefontsize = self.maintitlefontsize - 2
            if kwargs.get('righttitlefontsize') is None:
                self.righttitlefontsize = self.maintitlefontsize - 2
            if kwargs.get('labelfontsize') is None:
                self.labelfontsize = self.maintitlefontsize - 2
            if kwargs.get("tick_label_fontsize") is None:
                self.tick_label_fontsize = self.maintitlefontsize -2


        # Add titles with appropriate font sizes
        set_titles_and_labels(self.ax,
                              maintitle=self.maintitle,
                              maintitlefontsize=self.maintitlefontsize,
                              lefttitle=self.lefttitle,
                              lefttitlefontsize=self.lefttitlefontsize,
                              righttitle=self.righttitle,
                              righttitlefontsize=self.righttitlefontsize,
                              xlabel=self.xlabel,
                              ylabel=self.ylabel,
                              labelfontsize=self.labelfontsize)

    def show(self):
        ''' Display the plot.

        '''
        # Try to show plot with tight_layout
        try:
            plt.tight_layout()
        except:
            pass

        plt.show()

    def get_mpl_obj(self):
        ''' Get matplotlib object.
        '''
        return self.fig
