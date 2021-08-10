import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

from geocat.viz.util import add_major_minor_ticks
from geocat.viz.util import set_axes_limits_and_ticks

class _fig_ax:
    """Class to create figure and axes and set their style.
             
            Kwargs:
                
                cborientation (:obj:`str`): Placement of the colorbar. Default "horizontal". Other option is "vertical".
                
                h (:obj:`float`): Height of figure in inches. Default 8. To be passed into figsize when creating figure.
                
                projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_
                
                ref_fig (:class:`contourf.Contour`): Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the ref_fig would be the name of the first plot.
                
                set_extent (:class:`list`): Extent [xmin, xmax, ymin, ymax] of figure to be shown.
                
                subplot (:class:`list`): List [number of rows, number of columns, position] to be passed into plt.subplot().
                
                w (:obj:`float`): Weidth of the figure. Default 10. To be passed into figsize.
                
                x_label_lon (:obj:`bool`): Format the x axis as longitude values. Default True.
                
                xlim (:class:`list`): List [xmin, xmax] to set the limit of the x axis.
                
                xscale (:obj:`str`): Scale of x axis. Currently supports "log".
                
                ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.
                
                xticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the x axis.
                
                xticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the x axis.
                
                y_label_lat (:obj:`bool`): Format the y axis as latitude values. Default True.
                
                ylim (:class:`list`): List [ymin, ymax] to set the limit of the y axis.
                
                yscale (:obj:`str`): Scale of y axis. Currently supports "log".
                
                yticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the y axis.
    
                yticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the y axis.
                
    """

    def _init_(self, *args, **kwargs):
        """Set up figure and axes with the specified style. Calls _set_up_fig if there is not a figure already created, _set_axes to create and style the axes, and _set_lim_ticks to constrain the axes.
        
                Kwargs:
                    
                    cborientation (:obj:`str`): Placement of the colorbar. Default "horizontal". Other option is "vertical".
                
                    h (:obj:`float`): Height of figure in inches. Default 8. To be passed into figsize when creating figure.
                    
                    projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_
                    
                    ref_fig (:class:`contourf.Contour`): Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the ref_fig would be the name of the first plot.
                    
                    set_extent (:class:`list`): Extent [xmin, xmax, ymin, ymax] of figure to be shown.
                    
                    subplot (:class:`list`): List [number of rows, number of columns, position] to be passed into plt.subplot().
                    
                    w (:obj:`float`): Weidth of the figure. Default 10. To be passed into figsize.
                    
                    x_label_lon (:obj:`bool`): Format the x axis as longitude values. Default True.
                    
                    xlim (:class:`list`): List [xmin, xmax] to set the limit of the x axis.
                    
                    xscale (:obj:`str`): Scale of x axis. Currently supports "log".
                
                    ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.
                    
                    xticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the x axis.
                    
                    xticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the x axis.
                    
                    y_label_lat (:obj:`bool`): Format the y axis as latitude values. Default True.
                    
                    ylim (:class:`list`): List [ymin, ymax] to set the limit of the y axis.
                    
                    yscale (:obj:`str`): Scale of y axis. Currently supports "log".
                    
                    yticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the y axis.
        
                    yticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the y axis.  
        
        """
        
        # Set figure height and width defaults
        self._default_height = 8
        self._default_width = 10
        
         # Pull out figure size arguments
        self.h = kwargs.get('h')
        self.w = kwargs.get('w')
        
         # Pull out x and y axis formatting arguments
        self.x_label_lon = kwargs.get("x_label_lon")
        self.y_label_lat = kwargs.get("y_label_lat")
        
        # Pull out axes limits and scale info
        self.xlim = kwargs.get('xlim')
        self.ylim = kwargs.get('ylim')
        self.yscale = kwargs.get("yscale")
        self.xscale = kwargs.get("xscale")
        
        # Pull out tick arguments if specified
        self.xticks = kwargs.get('xticks')
        self.yticks = kwargs.get('yticks')
        self.xticklabels = kwargs.get('xticklabels')
        self.yticklabels = kwargs.get('yticklabels')
        self.ticklabelfontsize = kwargs.get("ticklabelfontsize")
        
        # Pull out extent of figure if specified
        self.set_extent = kwargs.get("set_extent")
        
         # Pull out projection and coastline argument
        self.projection = kwargs.get('projection')
        
        # Pull out reference figure argument
        self.ref_fig = kwargs.get("ref_fig")
        
        # Pull out subplot argument
        self.subplot = kwargs.get("subplot")
        
        
        
        # If there is not a reference obj, create a new figure
        if kwargs.get('ref_fig') is None:
            self._set_up_fig(w = self.w, h = self.h)
        else:
            # If there is a reference obj, assign the ref obj's figure as this obj's figure
            self.fig = self.ref_fig.fig
            
        # Set up axes with the specified style
        self._set_axes()
        
        # Set axis limits and ticks
        self._set_lim_ticks()
        
        
        
    def _set_up_fig(self, w=None, h=None):
        """ Create figure with subplots, if specified.
        
                Kwargs:
                    
                    w (:obj:`float`): Weidth of the figure. Default 10. To be passed into figsize.
                    
                    h (:obj:`float`): Height of figure in inches. Default 8. To be passed into figsize when creating figure.

        """

        # Use default figure height and width if none provided
        if h is None:
            h = self._default_height

        if w is None:
            w = self._default_width
            
        # If not a subplot, set up figure with specified width and height
        if self.subplot is None:
            self.fig = plt.figure(figsize=(w, h))
        
        
        # If a subplot, set figure and set of axes using plt.subplots and add projection if specified
        else:
            if self.projection is None:
                if self.add_colorbar is False:
                    self.fig, self.axes = plt.subplots(self.subplot[0], 
                                                     self.subplot[1],
                                                     figsize=(w,h))
                else:
                    # Create figure and axes with subplots
                    self.fig, self.axes = plt.subplots(self.subplot[0]+1, 
                                                 self.subplot[1],
                                                 figsize=(w,h),
                                                 gridspec_kw = self._generate_gridspec(self.subplot[0], self.subplot[1], self.cborientation))
        
            else:
                if self.add_colorbar is False:
                    self.fig, self.axes = plt.subplots(self.subplot[0],
                                                     self.subplot[1],
                                                     subplot_kw={"projection": self.projection},
                                                     figsize=(w,h))
                else:
                    # Create figure and axes with subplots
                    self.fig, self.axes = plt.subplots(self.subplot[0]+1, 
                                                 self.subplot[1],
                                                 figsize=(w,h),
                                                 gridspec_kw = self._generate_gridspec(self.subplot[0], self.subplot[1], self.cborientation),
                                                 subplot_kw={"projection": self.projection})
                
    def _generate_gridspec(self, rows, columns, cborientation):
        """Generate gridspec for subplots, with additional cax if there is a colorbar.
        
                Kwargs:
                    
                    cborientation (:obj:`str`): Placement of the colorbar. Default "horizontal". Other option is "vertical".
                    
                    columns (:obj:`int`): Number of columns in the subplot.
                    
                    cborientation (:obj:`string`): Number of rows in the subplot.
                    
                    rows (:obj:`int`): Number of rows in the subplot.
        
        """
            
        height_list = [1] * rows
        width_list = [1] * columns
        
        if (self.add_colorbar is not False):
            if (cborientation == "horizontal") or (cborientation is None):
                height_list.append(0.1)
            elif (cborientation == "vertical"):
                width_list.append(0.1)
        
        return {'height_ratios': height_list, 'width_ratios': width_list}
    
    def _set_axes(self, *args, **kwargs):
        """Assign value for self.ax by either creating a new axis or referencing the list of axes (self.axes) generated during subplot creation.
        
                Kwargs:
                    
                    projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_
                    
                    ref_fig (:class:`contourf.Contour`): Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the ref_fig would be the name of the first plot.
                    
                    set_extent (:class:`list`): Extent [xmin, xmax, ymin, ymax] of figure to be shown.
                    
                    xscale (:obj:`str`): Scale of x axis. Currently supports "log".
                    
                    yscale (:obj:`str`): Scale of y axis. Currently supports "log".
                    
        """
        
        # If there is not reference figure, either get axis from plt.subplot or create axis
        if self.ref_fig is None:
            if self.subplot is not None:
                # Set the axis as the position-1 (to account for Python indexing by 0) of the position of the subplot in the set of axes from plt.subplot
                self.ax = self.axes[(self.subplot[2]-1)]
            else:
                # Create axes and if there a projection, set it during creation
                if self.projection is None:
                    self.ax = plt.axes()
                else:
                    self.ax = plt.axes(projection=self.projection)
        # If there is a reference figure, get the axes from the ref_figure
        else:
            if self.subplot is not None:
                # Set the axis as the position-1 (to account for Python indexing by 0) of the position of the subplot in the set of axes from plt.subplot
                self.ax = self.ref_fig.axes[(self.subplot[2]-1)]
            else:
                # Try to set to the same axis as ref_fig, but otherwise just get the axis from the figure manually
                try:
                    self.ax = self.ref_fig.ax
                except:
                    self.ax = self.ref_fig.gca()
                    
                    
        
        # Set the aspect to auto to correct sizing
        self.ax.set_aspect("auto")
        
        # Set up axes with scale if specified
        if self.yscale == "log":
            plt.yscale("log")
            
        if self.xscale == "log":
            plt.xscale("log")
            
            
            
        # If there is a projection, add coastlines to the figure as long as it is not specified not to
        if self.projection is not None:
                if kwargs.get("show_coastlines") is not False:
                    self.ax.coastlines(linewidths=0.5, alpha=0.6)  
                    
    def _set_NCL_style(self, ax, ticklabelfontsize=16):
        """Set tick label size, add minor ticks, and format axes as latitude and longitude.
        
                Kwargs:
                    
                    ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.
                    
                    x_label_lon (:obj:`bool`): Format the x axis as longitude values. Default True.
                    
                    y_label_lat (:obj:`bool`): Format the y axis as latitude values. Default True.
                    
        """        
        # Set NCL-style tick marks
        if self.ticklabelfontsize is None:
            self.ticklabelfontsize = ticklabelfontsize
        
        add_major_minor_ticks(ax, labelsize=self.ticklabelfontsize)

        # Perform same action as add_lat_lon_ticklabels geocat-viz utility function
        # Manually set x and y axis format as lat and long unless specified not to
        if self.x_label_lon is not False:
            self.ax.xaxis.set_major_formatter(LongitudeFormatter())
        if self.y_label_lat is not False:
            self.ax.yaxis.set_major_formatter(LatitudeFormatter())
            
    def _set_lim_ticks(self):
        """Set limits and ticks for axis.
        
                Kwargs:
                
                    xlim (:class:`list`): List [xmin, xmax] to set the limit of the x axis.
                    
                    xticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the x axis.
                    
                    xticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the x axis.
                    
                    ylim (:class:`list`): List [ymin, ymax] to set the limit of the y axis.
                    
                    yticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the y axis.
        
                    yticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the y axis.  
                    
        """
         # If xlim/ylim is not specified, set it to the mix and max of the data
        if self.ylim is None:
            self.ylim = self.ax.get_ylim()[::-1]
            
        if self.xlim is None:
            self.xlim = self.ax.get_xlim()[::-1]
            
         # If x and y ticks are not specified, set to have 5 ticks over full range  
        if self.xticks is None:
            self.xticks = np.linspace(self.xlim[0], self.xlim[1], 5)
            
        if self.yticks is None:
            self.yticks = np.linspace(self.ylim[0], self.ylim[1], 5)
            
        # Use utility function to set axis limits and ticks
        set_axes_limits_and_ticks(self.ax,
                                  xlim=self.xlim,
                                  ylim=self.ylim,
                                  xticks=self.xticks,
                                  yticks=self.yticks,
                                  yticklabels = self.yticklabels,
                                  xticklabels = self.xticklabels)
        
        # TODO: check if needed
        # Set extent of figure
        if self.set_extent is not None:
            self.ax.set_extent(self.set_extent, crs=self.projection)
