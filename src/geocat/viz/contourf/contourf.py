"""Plotting wrapper for matplotlib contourf function."""

import matplotlib.pyplot as plt
import xarray as xr
import warnings
import numpy as np
import cartopy.crs as ccrs

from ._plot_util import NCL_Plot


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
            self.data = self.data.values

        # Read in or calculate filled levels
        if kwargs.get('flevels') is None and kwargs.get('clevels') is None:
            # take a guess at levels
            self.flevels = self._estimate_levels()
            self.clevels = self.flevels
        # Set user input values
        if kwargs.get('flevels') is not None:
            self.flevels = kwargs.get('flevels')
        if kwargs.get('clevels') is not None:
            # take a guess at filled levels
            self.clevels = kwargs.get('clevels')
        
        # Pull out child-class specific kwargs
        if kwargs.get('cmap') is not None:
            self.cmap = kwargs.get('cmap')
        else:
            self.cmap = self._default_cmap      

        # Call parent class constructor
        NCL_Plot.__init__(self, *args, **kwargs)

        # Create plot
        if kwargs.get('contour_fill') is not False:
            self.cf = self.ax.contourf(
                self.data,
                levels=self.flevels,
                cmap=self.cmap,
                transform=self.projection,
                extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]])

        if kwargs.get('contour_lines') is not False:
            self.cl = self.ax.contour(
                self.data,
                levels=self.clevels,
                colors='black',
                alpha=0.8,
                linewidths=0.4,
                linestyles='solid',
                transform=self.projection,
                extent=[self.xlim[0], self.xlim[1], self.ylim[0], self.ylim[1]])

        self._set_NCL_style(self.ax)

        # call colorbar creation from parent class
        # set colorbar if specified
        if self.colorbar is not False and self.colorbar is not 'off' and kwargs.get('contour_fill') is not False:
            self._add_colorbar(self.cf)

    def _estimate_levels(self):
        
        # set lower, upper bounds, and stepsize
        lb = np.nanmin(self.data)
        ub = np.nanmax(self.data)
        step = np.nanstd(self.data)

        # If the dataset is smaller than integer scale, set
        # precision to get more precise lb, ub and step values
        if step < 1:
            precision = np.ceil(abs(np.log10(abs(step))))
        else:
            precision = 0
        
        step = np.true_divide(np.floor(step / 2 * 10**precision), 10**precision)
        lb = np.true_divide(np.floor(lb * 10**precision), 10**precision)
        ub = np.true_divide(np.ceil(ub * 10**precision + 1), 10**precision) + step
        
        return np.arange(lb, ub, step)
