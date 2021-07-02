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
        if kwargs.get('flevels') != 'auto':
            # levels defined by kwargs
            self.levels = kwargs.get('flevels')
        elif kwargs.get('flevels') is not None:
            # take a guess at filled levels
            self._estimate_flevels

        # Read in or calculate contour levels
        if kwargs.get('clevels') != 'auto':
            # levels defined by kwargs
            self.levels = kwargs.get('clevels')
        elif kwargs.get('clevels') is not None:
            # take a guess at filled levels
            self._estimate_clevels

        # Pull out child-class specific kwargs
        if kwargs.get('cmap') is not None:
            self.cmap = kwargs.get('cmap')
        else:
            self.cmap = self._default_cmap

        # Call parent class constructor
        NCL_Plot.__init__(self, *args, **kwargs)

        # Create plot
        if kwargs.get('contour_fill') is not False:
            self.cf = self.ax.contourf(self.data,
                                       levels=self.levels,
                                       cmap=self.cmap,
                                       transform=self.projection,
                                       extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                       extend = self.cbextend
                                       )

        if kwargs.get('contour_lines') is not False:
            self.cl = self.ax.contour(self.data,
                                      levels=self.levels,
                                      colors='black',
                                      alpha=0.8,
                                      linewidths=0.4,
                                      linestyles='solid',
                                      transform=self.projection,
                                      extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]],
                                      extend = self.cbextend
                                       )

        self._set_NCL_style(self.ax)

        # call colorbar creation from parent class
        # set colorbar if specified
        if (self.colorbar is not False) and (self.colorbar != 'off'):
            self._add_colorbar(mappable=self.cf)
            
        self.add_titles()
            
    def _estimate_flevels(self):
        # TODO: flesh out
        print("estimate flevels")

    def _estimate_clevels(self):
        # TODO: flesh out
        print("estimate clevels")
