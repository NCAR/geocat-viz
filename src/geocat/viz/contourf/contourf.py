"""Plotting wrapper for matplotlib contourf function."""

import matplotlib.pyplot as plt
import xarray as xr
import warnings
import numpy as np
import cartopy.crs as ccrs

from _plot_util import NCL_Plot

from geocat.viz.util import add_major_minor_ticks
from geocat.viz.util import set_titles_and_labels
from geocat.viz.util import set_axes_limits_and_ticks
from geocat.viz.util import add_lat_lon_ticklabels


class Contour(NCL_Plot):
    # child class constructor
    def __init__(self, *args, **kwargs):

        # set class defaults
        self._default_cmap = 'coolwarm'
        self._default_flevels = 5
        self._default_clevels = 7

        # Pull out args
        self.data = args[0]

        # if in xarray, format as numpy array
        if isinstance(self.data, xr.DataArray):
            self.orig = self.data
            self.data = self.data.values
            
        # Read in or calculate filled levels
        if kwargs.get('contour_fill') is not False:
            if kwargs.get('flevels') is not None:
                # levels defined by kwargs
                self.levels = kwargs.get('flevels')
            elif kwargs.get('flevels') is None:
                # take a guess at filled levels
                self._estimate_flevels
        
        if kwargs.get("X") is not None:
            self.X = kwargs.get("X")
            if kwargs.get("Y") is None:
                raise AttributeError("If X is defined, Y must also be defined.")
            
        if kwargs.get("Y") is not None:
            self.Y = kwargs.get("Y")
            if kwargs.get("X") is None:
                raise AttributeError("If Y is defined, X must also be defined.")

        # Read in or calculate contour levels
        if kwargs.get('contour_lines') is not False:
            if kwargs.get('clevels') is not None:
                # levels defined by kwargs
                self.levels = kwargs.get('clevels')
            elif kwargs.get('clevels') is None:
                # take a guess at filled levels
                self._estimate_clevels
                
        # Read in style of contour lines
        if kwargs.get("linecolor") is None:
            self.linecolor = "black"
        else:
            self.linecolor = kwargs.get("linecolor")

        if kwargs.get("linestyle") is None:
            self.linestyle = "solid"
        else:
            self.linestyle = kwargs.get("linestyle")
            
        # Pull out child-class specific kwargs
        if kwargs.get('cmap') is not None:
            self.cmap = kwargs.get('cmap')
        else:
            self.cmap = self._default_cmap
            
        # Pull out contour label specific kwargs
        if kwargs.get("drawcontourlabels") is not None:
            self.draw_contour_labels = kwargs.get("drawcontourlabels")
        else:
            self.draw_contour_labels = False
        if kwargs.get("manualcontourlabels") is not None:
            self.manualcontourlabels = kwargs.get("manualcontourlabels")
        else:
            self.manualcontourlabels = False
        
        self.contourlabels = kwargs.get("contourlabels")
        self.contourfontsize = kwargs.get("contourfontsize")
        self.contourbackground = kwargs.get("contourbackground")
            
        

        # Call parent class constructor
        NCL_Plot.__init__(self, *args, **kwargs)
        
        if (kwargs.get("projection") is not None):
            if (kwargs.get("X") is not None) and (kwargs.get("Y") is not None):
                # Create plot
                if kwargs.get('contour_fill') is not False:
                    self.cf = self.ax.contourf(self.X,
                                               self.Y,
                                               self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               transform=self.projection,
                                               extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                               extend = self.cbextend,
                                               add_colorbar = False
                                               )
        
                if kwargs.get('contour_lines') is not False:
                    self.cl = self.ax.contour(self.X,
                                               self.Y,
                                               self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=0.4,
                                              linestyles=self.linestyle,
                                              transform=self.projection,
                                              extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                              extend = self.cbextend,
                                              add_colorbar = False
                                               )
            else:
                # Create plot
                if kwargs.get('contour_fill') is not False:
                    self.cf = self.ax.contourf(self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               transform=self.projection,
                                               extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                               extend = self.cbextend,
                                               add_colorbar = False
                                               )
        
                if kwargs.get('contour_lines') is not False:
                    self.cl = self.ax.contour(self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=0.4,
                                              linestyles=self.linestyle,
                                              transform=self.projection,
                                              extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                              extend = self.cbextend,
                                              add_colorbar = False
                                               )
        else:
            if (kwargs.get("X") is not None) and (kwargs.get("Y") is not None):
                # Create plot
                if kwargs.get('contour_fill') is not False:
                    self.cf = self.ax.contourf(self.X,
                                               self.Y,
                                               self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                               extend = self.cbextend,
                                               add_colorbar = False
                                               )
        
                if kwargs.get('contour_lines') is not False:
                    self.cl = self.ax.contour(self.X,
                                               self.Y,
                                               self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=0.4,
                                              linestyles=self.linestyle,
                                              extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                              extend = self.cbextend,
                                              add_colorbar = False
                                               )
            else:
                # Create plot
                if kwargs.get('contour_fill') is not False:
                    self.cf = self.ax.contourf(self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                               extend = self.cbextend,
                                               add_colorbar = False
                                               )
        
                if kwargs.get('contour_lines') is not False:
                    self.cl = self.ax.contour(self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=0.4,
                                              linestyles=self.linestyle,
                                              extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                              extend = self.cbextend,
                                              add_colorbar = False
                                               )
        
        self._set_NCL_style(self.ax)
        
        # If contour labels are requested, set them based on label arguments provided
        if self.draw_contour_labels is True:
            try:
                self.cl
            except:
                raise AttributeError("Contour lines must be plotted to add contour labels.")
                
            if (self.contourlabels is None) and (self.manualcontourlabels is None):
                raise AttributeError("Contour labels must be defined if adding them.")
            
            if self.contourlabels is not None:
                self._add_contour_labels(self.ax, 
                                        self.cl, 
                                        contourlabels = self.contourlabels, 
                                        fontsize = self.contourfontsize,
                                        background = self.contourbackground)
            elif self.manualcontourlabels is not None:
                self._add_contour_labels(self.ax, 
                                        self.cl, 
                                        manualcontourlabels = self.manualcontourlabels, 
                                        fontsize = self.contourfontsize,
                                        background = self.contourbackground)
            else:
                raise AttributeError("Contour labels must be defined if adding them.")

        # call colorbar creation from parent class
        # set colorbar if specified
        if (self.add_colorbar is not False) and (self.add_colorbar != 'off') and (kwargs.get('contour_fill') is not False):
            self._add_colorbar(mappable=self.cf)
            
        self.add_titles()
        
    def _add_contour_labels(self, ax, lines, contourlabels = None, background=True, fontsize=12):
        if self.contourfontsize is not None:
            fontsize = self.contourfontsize
        
        if self.manualcontourlabels is False:
            ax.clabel(lines, contourlabels, fontsize=fontsize, fmt='%d', inline=True)
        elif self.manualcontourlabels is True:
            ax.clabel(lines, fontsize=fontsize, fmt='%d', inline=True, manual = contourlabels)
        else:
            raise AttributeError("Manualcontourlabels, if set, must be True or False.")
        
        if background is True:
            [
                txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
                for txt in lines.labelTexts
            ]
            
    def _estimate_flevels(self):
        # TODO: flesh out
        print("estimate flevels")

    def _estimate_clevels(self):
        # TODO: flesh out
        print("estimate clevels")
