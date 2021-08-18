import matplotlib.pyplot as plt
import warnings
import xarray as xr

from geocat.viz.util import set_titles_and_labels

from _set_up_fig import _fig_ax
from _add_geo_features import add_geo_features


class NCL_Plot(_fig_ax, add_geo_features):
    """Parent class to create figure, axes, set NCL style with constructors to
    add colorbar, add titles, and show plot.

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

        labelfontsize (:obj:`int`): Fontsize for x and y axis labels. Default 16.

        lefttitle (:obj:`str`): Title for top left subtitle.

        lefttitlefontsize (:obj:`int`): Font size for top left subtitle. Default 18.

        maintitle (:obj:`str`): Title of figure.

        maintitlefontsize (:obj:`int`): Font size for title of figure. Default 18.

        mappable (:class:`cartopy.mpl.contour.GeoContourSet`): The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.

        righttitle (:obj:`str`): Title for top right subtitle.

        righttitlefontsize (:obj:`int`): Font size for top right subtitle. Default 18.

        subplot (:class:`list`): List [number of rows, number of columns, position] to be passed into plt.subplot().

        ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.

        xlabel (:obj:`str`): Label for the x axis.

        ylabel (:obj:`str`): Label for the y axis.
    """

    # Constructor
    def __init__(self, *args, **kwargs):
        """Pulls kwargs for colorbar and titles. Calls _fig_ax to set up figure
        and axes, add_geo_features to add geographical features to the figure,
        and adds titles.

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

            labelfontsize (:obj:`int`): Fontsize for x and y axis labels. Default 16.

            lefttitle (:obj:`str`): Title for top left subtitle.

            lefttitlefontsize (:obj:`int`): Font size for top left subtitle. Default 18.

            maintitle (:obj:`str`): Title of figure.

            maintitlefontsize (:obj:`int`): Font size for title of figure. Default 18.

            mappable (:class:`cartopy.mpl.contour.GeoContourSet`): The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.

            righttitle (:obj:`str`): Title for top right subtitle.

            righttitlefontsize (:obj:`int`): Font size for top right subtitle. Default 18.

            ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.

            xlabel (:obj:`str`): Label for the x axis.

            ylabel (:obj:`str`): Label for the y axis.
        """

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

        # Set up figure and axes with specified format
        _fig_ax._init_(self, *args, **kwargs)

        # Add geographical features to figure
        add_geo_features._init_(self, *args, **kwargs)

        # Add titles to figure
        self.add_titles()

    def _add_colorbar(self,
                      mappable=None,
                      cborientation="horizontal",
                      cbshrink=0.75,
                      cbpad=0.11,
                      cbdrawedges=True,
                      cbticks=None,
                      cbticklabels=None,
                      cbextend="neither",
                      cbticklabelsize=None):
        """Add colorbar to figure. If figure is a subplot, uses gridspec to add
        a cax to the appropriate place on the figure.

        Kwargs:

            cbdrawedges (:obj:`bool`): Whether to draw edges on the colorbar. Default True.

            cbextend (:obj:`str`): Pointed end of the colorbar. Default "neither", which does not include pointed edges. Other options are "both" (include on both sides), "min" (include on minimum end), and "max" (include on maximum end).

            cborientation (:obj:`str`): Placement of the colorbar. Default "horizontal". Other option is "vertical".

            cbpad (:obj:`float`): Padding between colorbar and figure. Default 0.11.

            cbshrink (:obj:`float`): Percent shrinkage of colorbar. Default 0.75.

            cbticklabels (:obj:`list` or :class:`numpy.ndarray`): Labels for colorbar ticks.

            cbticklabelsize (:obj:`int`): Font size for colorbar tick labels.

            cbticks (:obj:`list` or :class:`numpy.ndarray`): Ticks for colorbar.

            mappable (:class:`cartopy.mpl.contour.GeoContourSet`): The matplotlib.cm.ScalarMappable object that the colorbar represents. Mandatory when first creating colorbar, but not for subsequent calls.
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

        if (self.cbpad is None) or (cbpad != 0.11):
            self.cbpad = cbpad

        if (self.cbdrawedges is None) or (cbdrawedges is not True):
            self.cbdrawedges = cbdrawedges

        if (cbextend != "neither") or (self.cbextend is None):
            self.cbextend = cbextend

        # If there is not a mappable, raise error
        if self.mappable is None:
            raise AttributeError(
                "Mappable must be defined when first creating colorbar.")

        # If there is no subplot, create colorbar without specifying axis
        if self.subplot is None:
            self.cbar = self.fig.colorbar(self.mappable,
                                          orientation=self.cborientation,
                                          shrink=self.cbshrink,
                                          pad=self.cbpad,
                                          drawedges=self.cbdrawedges)
        # If subplot, specify caxis as the extra subplot added during figure creation
        else:
            self.cbar = self.fig.colorbar(self.mappable,
                                          cax=self.ref_fig.axes[-1],
                                          orientation=self.cborientation,
                                          shrink=self.cbshrink,
                                          pad=self.cbpad,
                                          drawedges=self.cbdrawedges)

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
        """Add titles to figure. If inputted dataset is an xarray file (or
        netCDF converted to xarray), will attempt to pull titles and labels
        from the datafile.

        Kwargs:

            labelfontsize (:obj:`int`): Fontsize for x and y axis labels. Default 16.

            lefttitle (:obj:`str`): Title for top left subtitle.

            lefttitlefontsize (:obj:`int`): Font size for top left subtitle. Default 18.

            maintitle (:obj:`str`): Title of figure.

            maintitlefontsize (:obj:`int`): Font size for title of figure. Default 18.

            righttitle (:obj:`str`): Title for top right subtitle.

            righttitlefontsize (:obj:`int`): Font size for top right subtitle. Default 18.

            ticklabelfontsize (:obj:`int`): Font size of x and y axis ticks. Default 16.

            xlabel (:obj:`str`): Label for the x axis.

            ylabel (:obj:`str`): Label for the y axis.
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
                    if self.xlabel is None:
                        self.xlabel = self.X.long_name
                except:
                    pass

            if self.Y is not None:
                # Attempt to set y axis label if Y is specified as a kwarg
                try:
                    if self.ylabel is None:
                        self.ylabel = self.Y.long_name
                except:
                    pass

            # Loop through coordinates in xarray file to set y and x as the first two non-restricted coordinates, respectively
            for i in range(len(keys)):
                # If coordinate is first label with multiple values, set y label
                if (coordinates[keys[i - 1]].size > 1) and first:
                    try:
                        if self.ylabel is None:
                            self.ylabel = coordinates[keys[i - 1]].long_name
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
                            i += 1
                else:
                    i += 1

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
        # Try to show plot with tight_layout
        try:
            plt.tight_layout()
        except:
            pass

        self.fig.show()

    def get_mpl_obj(self):
        return self.fig
