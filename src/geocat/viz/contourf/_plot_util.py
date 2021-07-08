import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import numpy as np
import warnings
import xarray as xr

from geocat.viz.util import add_major_minor_ticks
from geocat.viz.util import set_titles_and_labels
from geocat.viz.util import set_axes_limits_and_ticks
from geocat.viz.util import add_lat_lon_ticklabels


class NCL_Plot:

    # Constructor
    def __init__(self, *args, **kwargs):
        # Set class defaults
        self._default_height = 8
        self._default_width = 10

        # Pull out title and title font arguments
        self.maintitle = kwargs.get('maintitle')
        self.maintitlefontsize = kwargs.get('maintitlefontsize')
        self.lefttitle = kwargs.get('lefttitle')
        self.lefttitlefontsize = kwargs.get('lefttitlefontsize')
        self.righttitle = kwargs.get('righttitle')
        self.righttitlefontsize = kwargs.get('righttitlefontsize')

        # Pull out axes limits info
        self.xlim = kwargs.get('xlim')
        self.ylim = kwargs.get('ylim')
        self.yscale = kwargs.get("yscale")
        self.xscale = kwargs.get("xscale")

        # Pull out tick arguments if specified
        self.xticks = kwargs.get('xticks')
        self.yticks = kwargs.get('yticks')

        # Pull out axes label arguments
        self.xlabel = kwargs.get('xlabel')
        self.ylabel = kwargs.get('ylabel')
        self.labelfontsize = kwargs.get('labelfontsize')
        self.ticklabelfontsize = kwargs.get("ticklabelfontsize")

        # pull out colorbar arguments
        self.cbar = None
        self.add_colorbar = kwargs.get('add_colorbar')
        self.mappable = kwargs.get('mappable')
        self.cborientation = kwargs.get('cborientation')
        self.cbshrink = kwargs.get('cbshrink')
        self.cbpad = kwargs.get('cbpad')
        self.cbdrawedges = kwargs.get('cbdrawedges')
        self.cbticks = kwargs.get('cbticks')
        self.cbextend = kwargs.get('cbextend')
        
        # Pull out figure size arguments
        self.h = kwargs.get('h')
        self.w = kwargs.get('w')

        # Set up figure
        self._set_up_fig(w = self.w, h = self.h)
        
        self.set_coastlines = kwargs.get("set_coastlines")

        # Set up axes with projection if specified
        self.ax = kwargs.get("ax")
        
        if self.ax is None:
            if kwargs.get('projection') is not None:
                self.projection = kwargs.get('projection')
                self.ax = plt.axes(projection=self.projection)
                if self.set_coastlines is not False:
                    self.ax.coastlines(linewidths=0.5, alpha=0.6)
                self.ax.set_aspect("auto")
            else:
                self.ax = plt.axes()
                self.ax.set_aspect("auto")
            
        # Set up axes with scale if specified
        if self.yscale == "log":
            plt.yscale("log")
        if self.xscale == "log":
            plt.xscale("log")
        
        # Set specified features
        if kwargs.get('show_land') is True:
            self.show_land()

        if kwargs.get('show_coastline') is True:
            self.show_coastline()

        if kwargs.get('show_lakes') is True:
            self.show_lakes()
            
        self.set_extent = kwargs.get("set_extent")
            
        # If xlim/ylim is not specified, set it to the mix and max of the data
        if self.ylim is None:
            self.ylim = self.ax.get_ylim()[::-1]
            
        if self.xlim is None:
            self.ylim = self.ax.get_xlim()[::-1]
            
         # If x and y ticks are not specified, set to have 4 ticks over full range  
        if self.xticks is None:
            self.xticks = np.linspace(0, self.xlim[1], 4)
            
        if self.yticks is None:
            self.yticks = np.linspace(0, self.ylim[1], 4)
            
        # Use utility function ot set limits and ticks
        set_axes_limits_and_ticks(self.ax,
                                  xlim=self.xlim,
                                  ylim=self.ylim,
                                  xticks=self.xticks,
                                  yticks=self.yticks)
        
        # Set extent of figure
        if self.set_extent is not None:
            self.ax.set_extent(self.set_extent, crs=self.projection)

    def _set_up_fig(self, w=None, h=None):

        # Use default figure height and width if none provided
        if h is None:
            h = self._default_height

        if w is None:
            w = self._default_width

        self.fig = plt.figure(figsize=(w, h))

    def _set_NCL_style(self, ax, fontsize=18, subfontsize=18, ticklabelfontsize=16, labelfontsize=16):
        # Set NCL-style tick marks
        if self.ticklabelfontsize is None:
            self.ticklabelfontsize = ticklabelfontsize
        add_major_minor_ticks(ax, labelsize=self.ticklabelfontsize)

        # Set NLC-style titles set from from initialization call (based on geocat-viz function)
        if self.maintitle is not None:
            if self.lefttitle is not None or self.righttitle is not None:
                plt.title(self.maintitle, fontsize=fontsize + 2, y=1.12)
            else:
                plt.title(self.maintitle, fontsize=fontsize, y=1.04)
        
        if self.lefttitle is not None:
            plt.title(self.lefttitle, fontsize=subfontsize, y=1.04, loc='left')

        if self.righttitle is not None:
            plt.title(self.righttitle,
                      fontsize=subfontsize,
                      y=1.04,
                      loc='right')

        if self.xlabel is not None:
            plt.xlabel(self.xlabel, fontsize=labelfontsize)

        if self.ylabel is not None:
            plt.ylabel(self.ylabel, fontsize=labelfontsize)

        # format axes as lat, lon
        add_lat_lon_ticklabels(self.ax)

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
        # Set values for colorbar while maintaining previously set values
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
            
        if self.mappable is None:
            raise AttributeError("Mappable must be defined when first creating colorbar.")
        
        # Create colorbar
        self.cbar = self.fig.colorbar(self.mappable, 
                                      orientation=self.cborientation, 
                                      shrink=self.cbshrink, 
                                      pad=self.cbpad, 
                                      drawedges=self.cbdrawedges
                                      )
        
        # Set colorbar ticks
        if (cbticks is None) and (self.cbticks is None):
            self.cbticks = self.cbar.boundaries[1:-1]

        # Label every boundary except the ones on the end of the colorbar
        self.cbar.set_ticks(ticks=self.cbticks)
        
        # Set colorbar tick labesls
        if cbticklabels is not None:
            self.cbticklabels = cbticklabels
            
            self.cbar.set_ticklabels(ticklabels=self.cbticklabels)
        
        # Set labelsize
        if cbticklabelsize is not None:
            self.cbticklabelsize = cbticklabelsize
            self.cbar.ax.tick_params(labelsize=self.cbticklabelsize)

    def show_land(self, scale = "110m", color='lightgrey'):
        self.ax.add_feature(cfeature.LAND.with_scale(scale), facecolor=color)

    def show_coastline(self, scale = "110m", lw=0.5, edgecolor="black"):
        self.ax.add_feature(cfeature.COASTLINE.with_scale(scale), 
                            linewidths=lw,
                            edgecolor=edgecolor)

    def show_lakes(self, scale = "110m", lw=0.5, ec='black', fc='None'):
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
       
        # Update object definitions
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

            
        # If xarray file, use labels within file
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
                
            # Set variables for x and y labels
            first = True    
            coordinates = self.orig.coords
            keys = list(coordinates.keys())
            
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
        plt.tight_layout()
        plt.show()

    def get_mpl_obj(self):
        return self.fig