import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import numpy as np
import warnings

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

        # TODO: address all input arguments and run checks
        # Pull out title arguments
        self.maintitle = kwargs.get('maintitle')
        self.lefttitle = kwargs.get('lefttitle')
        self.righttitle = kwargs.get('righttitle')

        # Pull out axes info
        self.xlim = kwargs.get('xlim')
        self.ylim = kwargs.get('ylim')

        # Make sure x and y limits specified (for now)
        #TODO: make x and y limits self-determinable somehow
        if self.xlim is None or self.ylim is None:
            raise AttributeError(
                "For now, xlim and ylim must be specified as kwargs")

        # Pull out tick arguments if specified
        self.xticks = kwargs.get('xticks')
        self.yticks = kwargs.get('yticks')

        # Pull out axes label arguments
        self.xlabel = kwargs.get('xlabel')
        self.ylabel = kwargs.get('ylabel')

        # pull out colorbar arguments
        self.colorbar = kwargs.get('colorbar')

        # Set up figure
        self._set_up_fig()

        # Set up axes with projection if specified
        if kwargs.get('projection') is not None:
            self.projection = kwargs.get('projection')
            self.ax = plt.axes(projection=self.projection)
            self.ax.coastlines(linewidths=0.5, alpha=0.6)
        else:
            self.ax = plt.axes()

        # TODO: un-hardcode
        set_axes_limits_and_ticks(self.ax,
                                  xlim=self.xlim,
                                  ylim=self.ylim,
                                  xticks=self.xticks,
                                  yticks=self.yticks)

        # Set specified features
        if kwargs.get('show_land') is True:
            self.show_land()

        if kwargs.get('show_coastline') is True:
            self.show_coastline()

        if kwargs.get('show_lakes') is True:
            self.show_lakes()

    def _set_up_fig(self, w=None, h=None):

        # Use default figure height and width if none provided
        if h is None:
            h = self._default_height

        if w is None:
            w = self._default_width

        self.fig = plt.figure(figsize=(w, h))

    def _set_NCL_style(self, ax, fontsize=18, subfontsize=18, labelfontsize=16):
        # Set NCL-style tick marks
        # TODO: switch from using geocat-viz to using a geocat-lynx specific tick function
        add_major_minor_ticks(ax, labelsize=10)

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

        # format axes as lat lon
        add_lat_lon_ticklabels(self.ax)

    def _add_colorbar(self, mappable):
        self.cbar = self.fig.colorbar(mappable,
                                      orientation="horizontal",
                                      shrink=0.75,
                                      pad=0.11,
                                      drawedges=True)

        # label every boundary except the ones on the end of the colorbar
        self.cbar.set_ticks(ticks=self.cbar.boundaries[1:-1])

    def show_land(self, color='lightgrey'):
        self.ax.add_feature(cfeature.LAND, facecolor=color)

    def show_coastline(self, lw=0.5):
        self.ax.add_feature(cfeature.COASTLINE, linewidths=lw)

    def show_lakes(self, lw=0.5, ec='black', fc='None'):
        self.ax.add_feature(cfeature.LAKES,
                            linewidth=lw,
                            edgecolor=ec,
                            facecolor=fc)

    # TODO: allow changes in font size from external call
    def add_titles(self,
                   maintitle=None,
                   lefttitle=None,
                   righttitle=None,
                   xlabel=None,
                   ylabel=None):
        set_titles_and_labels(self.ax, maintitle, lefttitle, righttitle, xlabel,
                              ylabel)

        # update object definitions
        if maintitle is not None:
            self.maintitle = maintitle

        if lefttitle is not None:
            self.lefttitle = lefttitle

        if righttitle is not None:
            self.righttitle = righttitle

        if xlabel is not None:
            self.xlabel = xlabel

        if ylabel is not None:
            self.ylabel = ylabel

    def show(self):
        plt.show()

    def get_mpl_obj(self):
        return self.fig
