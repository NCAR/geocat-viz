import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import numpy as np
import warnings
import xarray as xr
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

from geocat.viz.util import add_major_minor_ticks
from geocat.viz.util import set_titles_and_labels
from geocat.viz.util import set_axes_limits_and_ticks
from geocat.viz.util import add_lat_lon_ticklabels


class NCL_Plot:
    """Parent class to create figure, axes, set NCL style, add colorbar, add titles, and show plot.
            
            Args:
                
                data (:class:`xarray.DataArray` or :class:`numpy.ndarray`): The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.
                
            Kwargs:
                
                add_colorbar (:obj:`bool`): Whether a colorbar is added to the figure. Default True.
                
                cbdrawedges (:obj:`bool`): Whether to draw edges on the colorbar. Default True.
                
                cbextend (:obj:`str`): Pointed end of the colorbar. Default "neither", which does not include pointed edges. Other options are "both" (include on both sides), "min" (include on minimum end), and "max" (include on maximum end).
                
                cborientation (:obj:`str`): Placement of the colorbar. Default "horizontal". Other option is "vertical".
                
                cbpad (:obj:`float`): Padding between colorbar and figure. Default 0.11.
                
                cbshrink (:obj:`float`): Percent shrinkage of colorbar. Default 0.75.
                
                cbticklabels (:obj:`list` or :class:`numpy.ndarray`): Labels for colorbar ticks.
                
                cbticklabelsize (:obj:`int`): Font size for colorbar tick labels.
                
                cbticks (:obj:`list` or :class:`numpy.ndarray`): Ticks for colorbar.
                
                h (:obj:`float`): Height of figure in inches. Default 8. To be passed into figsize when creating figure.
                
                labelfontsize (:obj:`int`): Fontsize for x and y axis labels. Default 16.
                
                lefttitle (:obj:`str`): Title for top left subtitle.
                
                lefttitlefontsize (:obj:`int`): Font size for top left subtitle. Default 18.
                
                maintitle (:obj:`str`): Title of figure.
                
                maintitlefontsize (:obj:`int`): Font size for title of figure. Default 18.
                
                mappable (:class:`cartopy.mpl.contour.GeoContourSet`): The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
                
                projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_
                
                ref_fig (:class:`contourf.Contour`): Reference figure that the object will be created based on. For example, when overlaying plots or creating subplots, the ref_fig would be the name of the first plot.
                
                righttitle (:obj:`str`): Title for top right subtitle.
                
                righttitlefontsize (:obj:`int`): Font size for top right subtitle. Default 18.
                
                set_extent (:class:`list`): Extent [xmin, xmax, ymin, ymax] of figure to be shown.
                
                show_coastline (:obj:`bool`): Whether to show coastlines in figure. Default False, unless a projection is specified.
                
                show_lakes (:obj:`bool`): Whether to show lakes in figure. Default False.
                
                show_land (:obj:`bool`): Whether to show land in figure. Default false.
                
                subplot (:class:`list`): List [number of rows, number of columns, position] to be passed into plt.subplot().
                
                ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.
                
                w (:obj:`float`): Weidth of the figure. Default 10. To be passed into figsize.
                
                x_label_lon (:obj:`bool`): Format the x axis as longitude values. Default True.
                
                xlabel (:obj:`str`): Label for the x axis.
                
                xlim (:class:`list`): List [xmin, xmax] to set the limit of the x axis.
                
                xscale (:obj:`str`): Scale of x axis. Currently supports "log".
                
                xticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the x axis.
                
                xticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the x axis.
                
                y_label_lat (:obj:`bool`): Format the y axis as latitude values. Default True.
                
                ylabel (:obj:`str`): Label for the y axis.
                
                ylim (:class:`list`): List [ymin, ymax] to set the limit of the y axis.
                
                yscale (:obj:`str`): Scale of y axis. Currently supports "log".
                
                yticklabels (:obj:`list` or :class:`numpy.ndarray`): List or array of tick labels for the y axis.
    
                yticks (:obj:`list` or :class:`numpy.ndarray`): List or array of tick values for the y axis.
    
            """
    # Constructor
    def __init__(self, *args, **kwargs):
        
        # Set figure height and width defaults
        self._default_height = 8
        self._default_width = 10

        # Pull out titles and labels and their font arguments
        self.maintitle = kwargs.get('maintitle')
        self.maintitlefontsize = kwargs.get('maintitlefontsize')
        self.lefttitle = kwargs.get('lefttitle')
        self.lefttitlefontsize = kwargs.get('lefttitlefontsize')
        self.righttitle = kwargs.get('righttitle')
        self.righttitlefontsize = kwargs.get('righttitlefontsize')
        self.xlabel = kwargs.get('xlabel')
        self.ylabel = kwargs.get('ylabel')
        self.labelfontsize = kwargs.get('labelfontsize')

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

        # Pull out colorbar arguments
        self.cbar = None
        self.add_colorbar = kwargs.get('add_colorbar')
        self.mappable = kwargs.get('mappable')
        self.cborientation = kwargs.get('cborientation')
        self.cbshrink = kwargs.get('cbshrink')
        self.cbpad = kwargs.get('cbpad')
        self.cbdrawedges = kwargs.get('cbdrawedges')
        self.cbticks = kwargs.get('cbticks')
        self.cbextend = kwargs.get('cbextend')
        self.cbticklabels = kwargs.get("cbticklabels")
        self.cbticklabelsize = kwargs.get("cbticklabelsize")
        
        # Pull out x and y axis formatting arguments
        self.x_label_lon = kwargs.get("x_label_lon")
        self.y_label_lat = kwargs.get("y_label_lat")
        
        # Pull out figure size arguments
        self.h = kwargs.get('h')
        self.w = kwargs.get('w')
        
        # Pull out projection and coastline argument
        self.projection = kwargs.get('projection')
        self.set_coastlines = kwargs.get("set_coastlines")
        
        # Pull out extent of figure if specified
        self.set_extent = kwargs.get("set_extent")
        
        # Pull out reference figure argument
        self.ref_fig = kwargs.get("ref_fig")
        
        # Pull out subplot argument
        self.subplot = kwargs.get("subplot")

        # If there is no reference figure, create figure. If there is a ref_fig, set self.fig to the figure from the ref_fig
        if kwargs.get('ref_fig') is None:
            self._set_up_fig(w = self.w, h = self.h)
        else:
            self.fig = self.ref_fig.fig
        
        # If there is not reference figure, either get axis from plt.subplot or create axis
        if kwargs.get("ref_fig") is None:
            if self.subplot is not None:
                # Set the axis as the position-1 (to account for Python indexing by 0) of the position of the subplot in the set of axes from plt.subplot
                self.ax = self.axes[(self.subplot[2]-1)]
            else:
                # Create axes and if there a projection set it
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
                if self.set_coastlines is not False:
                    self.ax.coastlines(linewidths=0.5, alpha=0.6)   
        
        # Add land, coastlines, or lakes if specified
        if kwargs.get('show_land') is True:
            self.show_land()

        if kwargs.get('show_coastline') is True:
            self.show_coastline()

        if kwargs.get('show_lakes') is True:
            self.show_lakes()
            
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
        
        # Add titles to figure
        self.add_titles()
       

    def _set_up_fig(self, w=None, h=None):

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
                self.fig, self.axes = plt.subplots(self.subplot[0], 
                                                 self.subplot[1],
                                                 figsize=(w,h))
            else:
                self.fig, self.axes = plt.subplots(self.subplot[0],
                                                 self.subplot[1],
                                                 subplot_kw={"projection": self.projection},
                                                 figsize=(w,h))

    def _set_NCL_style(self, ax, ticklabelfontsize=16):
        
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
        

    def _add_colorbar(self, 
                      mappable = None, 
                      cborientation="horizontal",
                      cbshrink=0.75,
                      cbpad=0.11,
                      cbdrawedges=True,
                      cbticks=None,
                      cbticklabels=None,
                      cbextend = "neither",
                      cbticklabelsize=None):
        
        # Set values for colorbar arguments while maintaining previously set values
        if self.cbar is not None:
            self.cbar.remove()
        
        if mappable is not None:
            self.mappable = mappable
        
        if (self.cborientation is None) or (cborientation != "horizontal"):
            self.cborientation = cborientation
            
        if (self.cbshrink is None) or (cbshrink != 0.75):
            self.cbshrink = cbshrink
        
        if (self.cbpad is None) or (cbpad != 0.11):
            self.cbpad = cbpad
            
        if (self.cbdrawedges is None) or (cbdrawedges is not True):
            self.cbdrawedges = cbdrawedges
            
        if (cbextend != "neither") or (self.cbextend is None):
            self.cbextend = cbextend
            
        # If there is not a mappable, raise error
        if self.mappable is None:
            raise AttributeError("Mappable must be defined when first creating colorbar.")
        
        # If there is no subplot, create colorbar without specifying axis
        if self.subplot is None:
            self.cbar = self.fig.colorbar(self.mappable, 
                                          orientation=self.cborientation, 
                                          shrink=self.cbshrink, 
                                          pad=self.cbpad, 
                                          drawedges=self.cbdrawedges
                                          )
        # If subplot, specify axis
        else:
            self.cbar = self.fig.colorbar(self.mappable, 
                                          ax = self.ref_fig.axes,
                                          orientation=self.cborientation, 
                                          shrink=self.cbshrink, 
                                          pad=self.cbpad, 
                                          drawedges=self.cbdrawedges
                                          )
            
        # Set colorbar ticks as the boundaries of the cbar
        if (cbticks is None) and (self.cbticks is None):
            self.cbticks = self.cbar.boundaries[1:-1]

        # Label every boundary except the ones on the end of the colorbar
        self.cbar.set_ticks(ticks=self.cbticks)
        
        # Set colorbar tick labesls
        if self.cbticklabels is not None:
            self.cbar.set_ticklabels(ticklabels=self.cbticklabels)
        
        # Set label size of cbar ticks
        if self.cbticklabelsize is not None:
            self.cbar.ax.tick_params(labelsize=self.cbticklabelsize)

    def show_land(self, scale = "110m", color='lightgrey'):
        # Add land to figure
        self.ax.add_feature(cfeature.LAND.with_scale(scale), facecolor=color)

    def show_coastline(self, scale = "110m", lw=0.5, edgecolor="black"):
        # Add coastline to figure
        self.ax.add_feature(cfeature.COASTLINE.with_scale(scale), 
                            linewidths=lw,
                            edgecolor=edgecolor)

    def show_lakes(self, scale = "110m", lw=0.5, ec='black', fc='None'):
        # Add lakes to figure
        self.ax.add_feature(cfeature.LAKES.with_scale(scale),
                            linewidth=lw,
                            edgecolor=ec,
                            facecolor=fc)

    
    def add_titles(self,
                   maintitle=None, 
                   maintitlefontsize=18,
                   lefttitle=None, 
                   lefttitlefontsize=18,
                   righttitle=None, 
                   righttitlefontsize=18,
                   xlabel=None, 
                   ylabel=None,
                   labelfontsize=16):
       
        # Update argument definitions
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
                try:
                    self.maintitle = self.orig.attrs["title"]
                except:
                    pass
            if self.lefttitle is None:
                try:
                    self.lefttitle = self.orig.attrs["long_name"]
                except:
                    pass
            if self.righttitle is None:
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
                try:
                    if self.xlabel is None:
                        self.xlabel = self.X.long_name
                except:
                    pass
                
            if self.Y is not None:
                try:
                    if self.ylabel is None:
                        self.ylabel = self.Y.long_name
                except:
                    pass
                
            # Loop through coordinates in xarray file
            for i in range(len(keys)):
                # If coordinate is first label with multiple values, set y label
                if (coordinates[keys[i-1]].size > 1) and first:
                    try:
                        if self.ylabel is None:
                            self.ylabel = coordinates[keys[i-1]].long_name
                    except:
                        pass
                    
                    while i < len(keys):
                        # If coordinate is second label with multiple values, set x label
                        if (coordinates[keys[i]].size > 1) and first:
                            try:
                                if self.xlabel is None:
                                    self.xlabel = coordinates[keys[i]].long_name
                            except:
                                pass
                            first = False
                        else:
                            i +=1
                else:
                    i += 1
                
        
        # Add titles with appropriate font sizes
        set_titles_and_labels(self.ax,
                              maintitle = self.maintitle, 
                              maintitlefontsize = self.maintitlefontsize,
                              lefttitle = self.lefttitle, 
                              lefttitlefontsize = self.lefttitlefontsize,
                              righttitle = self.righttitle, 
                              righttitlefontsize = self.righttitlefontsize,
                              xlabel = self.xlabel, 
                              ylabel = self.ylabel,
                              labelfontsize = self.labelfontsize)

    def show(self):
        # Try to show plot with tight_layout
        try:
            plt.tight_layout()
        except:
            pass
        self.fig.show()

    def get_mpl_obj(self):
        return self.fig