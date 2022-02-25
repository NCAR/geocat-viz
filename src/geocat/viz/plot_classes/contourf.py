"""Plotting wrapper for matplotlib contourf function."""

import xarray as xr
import typing
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

from _plot_util import NCL_Plot


class Contour(NCL_Plot):
    """Create contour plot.

    Args
    ----
    data: :class:`xarray.DataArray` or :class:`numpy.ndarray`
        The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.

    type: :class:`str`
        Optional arg. Changes the type of contour figure from plotting lat vs lon. Valid inputs: press_height

    Keyword Args
    ------------
    add_colorbar: :obj:`bool` 
        Whether a colorbar is added to the figure. Default True.

    clevels: :obj:`list` or :class:`numpy.ndarray` 
        List or array of levels to be passed into matplotlib's contour function.

    cmap: :class:`cmaps.colormap.Colormap` 
        Colormap for the filled contour graph.

    contour_fill: :obj:`bool` 
            Whether filled contours will be drawn. Default True.

    contour_lines: :obj:`bool` 
        Whether contours lines will be drawn. Default True.

    contour_label_background: :obj:`bool`
        Whether a white background for the contour labels will be drawn. Default False.

    contour_label_fontsize: :obj:`int` 
        Font size of the contour line labels. Default 12.

    contour_labels :obj:`list` or :class:`numpy.ndarray` 
        List or array of labels to use for contour line labels.

    draw_contour_labels: :obj:`bool` 
        Whether add contour line labels to the figure.

    flevels: :obj:`list` or :class:`numpy.ndarray` 
        List or array of levels to be passed into matplotlib's contourf function.

    line_color: :obj:`str`
        Color of the contour line. Default "black".

    line_style :obj:`str` 
        line_style of the contour line. Default solid for positive values, dashed for negative values.

    line_width :obj:`int` 
        Width of the contour lines. Default 0.4.

    projection :obj:`str` 
        Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

    X :class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`
        The X axis data for the dataset. To be specified if not inferred correctly automatically.

    Y :class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`
        The Y axis data for the dataset. To be specified if not inferred correctly automatically.

    Return
    ------
    Contour_Object: :class:`contourf.Contour` 
        A contour plot with specified input style.
    """

    def __init__(self, *args, **kwargs):
        """Create contour figure. Generate filled contours and/or contour lines
        for figure. Add colorbar and contour labels if specified.

        Args
        ----
        data: :class:`xarray.DataArray` or :class:`numpy.ndarray`
            The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.

        Keyword Args
        ------------
        add_colorbar: :obj:`bool` 
            Whether a colorbar is added to the figure. Default True.

        cmap: :class:`cmaps.colormap.Colormap` 
            Colormap for the filled contour graph.

        contour_fill: :obj:`bool` 
                Whether filled contours will be drawn. Default True.

        contour_lines: :obj:`bool` 
            Whether contours lines will be drawn. Default True.

        contour_label_background: :obj:`bool`
            Whether a white background for the contour labels will be drawn. Default False.

        contour_label_fontsize: :obj:`int` 
            Font size of the contour line labels. Default 12.

        contour_labels :obj:`list` or :class:`numpy.ndarray` 
            List or array of labels to use for contour line labels.

        draw_contour_labels: :obj:`bool` 
            Whether add contour line labels to the figure.

        levels: :obj:`list` or :class:`numpy.ndarray` 
            List or array of levels to be passed into matplotlib's contour and/or contourf function.

        line_color: :obj:`str`
            Color of the contour line. Default "black".

        line_style :obj:`str` 
            line_style of the contour line. Default solid for positive values, dashed for negative values.

        line_width :obj:`int` 
            Width of the contour lines. Default 0.4.

        projection :obj:`str` 
            Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

        X :class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`
            The X axis data for the dataset. To be specified if not inferred correctly automatically.

        Y :class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`
            The Y axis data for the dataset. To be specified if not inferred correctly automatically.

        """

        # Valid kwargs
        valid_kwargs = {'add_colorbar', 'levels', 'cbar', 'cbdrawedges', 'cborientation', 
            'cbpad', 'cbshrink', 'cbticks', 'cbticklabels', 'cbtick_label_size', 
            'cmap', 'contour_fill', 'contour_lines', 'contour_label_background', 
            'contour_label_fontsize', 'contour_labels', 'draw_contour_labels', 
            'labelfontsize', 'lefttitle', 'lefttitlefontsize', 'levels', 
            'line_color', 'line_style', 'line_width', 'h', 'individual_cb', 
            'maintitle', 'maintitlefontsize', 'mappable', 'projection', "overlay", 
            'righttitle', 'righttitlefontsize', "set_extent", "subplot", 
            'tick_label_fontsize', 'type', 'w', 'X', "x_label_lon", 'xlabel', 'xlim', 
            "xscale", 'xticks', 'xticklabels', 'Y', "y_label_lat", 'ylabel', 
            'ylim', "yscale", 'yticks', 'yticklabels'}
        
        # Dictionary of default values
        all_kwargs = {'cmap' : 'coolwarm', 'line_color' : "black", 
            'line_width' : 0.4, 'levels' : 5, 'draw_contour_labels' : False,
            'w' : 8, 'h': 8, 'cborientation' : "horizontal",
            'cbshrink' : 0.75, 'cbpad' : 0.075, 'cbdrawedges' : True, 'projection' : ccrs.PlateCarree()}

        # Update dict to include inputted kwargs
        all_kwargs.update(kwargs)

        # Create self.kwarg for all kwargs in valid_kwargs
        self.__dict__.update((k, None) for k in valid_kwargs)
        self.__dict__.update((k, v) for k, v in all_kwargs.items() if k in valid_kwargs)

        # Read in kwargs from overlay plot
        if self.overlay is not None:
            self.__dict__.update((k,v) for k, v in kwargs.get('overlay').__dict__.items() if (k not in self.__dict__.keys() or self.__dict__[k] is None))

        # Print unused kwargs
        unused_kwargs = [unused for unused in kwargs if unused not in valid_kwargs]
        if len(unused_kwargs) > 0:
            print("--------------UNUSED KWARGS--------------" + 
                "\n".join(unused_kwargs))

        # Pull out args from data
        self.data = args[0]

        # if the type is press_height, set projection to none
        if self.type == "press_height":
            self.projection = None
        
        if self.contour_fill is False and self.add_colorbar is None:
            self.add_colorbar = False

        # If xarray file, format as Numpy array
        if isinstance(self.data, xr.DataArray):
            self.orig = self.data
            self.data = self.data.values
            if self.X is None:
                self.__dict__.update({'X' : self.orig.coords[self.orig.dims[1]]})
            if self.Y is None:
                self.__dict__.update({'Y': self.orig.coords[self.orig.dims[0]]})

        # If levels aren't specified, calculate them
        if self.levels is None:
            # take a guess at filled levels
            self._estimate_levels()

        # Check that if X is defined, Y is (and vice versa)
        if (self.X is None) ^ (self.Y is None):
            raise AttributeError("If X is defined, Y must also be defined and vice versa.")

        # Call parent class constructor
        super().__init__(self, *args, **kwargs)

        # Add filled contours and/or contour lines to figure, as specified
        self._generate_contours()

        # Set figure in NCL style
        super()._set_NCL_style(self.ax)

        # If any aspect about contour labels is specified, draw them
        if (self.draw_contour_labels is True 
            or self.contour_labels is not None
            or self.contour_label_background is not None
            or self.contour_label_fontsize is not None):
            # Try to draw contour labels on contour lines
            if hasattr(self, 'cl'):
                self._add_contour_labels(self.ax,
                                         self.cl,
                                         contour_labels=self.contour_labels,
                                         fontsize=self.contour_label_fontsize,
                                         background=self.contour_label_background)
            # If there aren't any, try to draw them on filled contours
            else:
                if self.contour_fill is not False:
                    self._add_contour_labels(self.ax,
                                             self.cf,
                                             contour_labels=self.contour_labels,
                                             fontsize=self.contour_label_fontsize,
                                             background=self.contour_label_background)

        # Call colorbar creation from parent class
        # Set colorbar if specified

        # If not a subplot and add_colorbar and contour_fill is not false, add colorbar
        if (((self.add_colorbar is not False) and
             (self.add_colorbar != 'off') and
             (kwargs.get('contour_fill') is not False) and
             (self.subplot is None)) or
                # If subplot, check if in last position in subplot and that add_colorbar is not False and plot
            ((self.add_colorbar is not False) and
             (kwargs.get('contour_fill') is not False) and
             (self.subplot[2] == self.subplot[0] * self.subplot[1]) and
             (self.add_colorbar != "off") and
             ((self.individual_cb is not True) or
              (self.overlay.individual_cb is not True)) or
             (self.individual_cb is True))):

            self._add_colorbar(mappable=self.cf)

    def _generate_contours(self, *args, **kwargs):
        """Generate filled contours and/or contour lines for figure.
        """
        if self.contour_fill is not False:
            self.cf = self.ax.contourf(self.X.data,
                                        self.Y.data,
                                        self.data,
                                        levels=self.levels,
                                        cmap=self.cmap,
                                        transform=self.projection,
                                        extent=[
                                            self.xlim[0], self.xlim[1],
                                            self.ylim[0], self.ylim[1]
                                        ])

        if self.contour_lines is not False:
            self.cl = self.ax.contour(self.X.data,
                                        self.Y.data,
                                        self.data,
                                        levels=self.levels,
                                        colors=self.line_color,
                                        alpha=0.8,
                                        linewidths=self.line_width,
                                        linestyles=self.line_style,
                                        transform=self.projection,
                                        extent=[
                                            self.xlim[0], self.xlim[1],
                                            self.ylim[0], self.ylim[1]
                                        ])

    def _add_contour_labels(self,
                            ax,
                            lines,
                            contour_labels,
                            background,
                            fontsize = 12):
        """Add contour line labels with an optional white background to the
        figure.
        
        Args
        ----
        ax: :class:`matplotlib.axes.Axes`, :class:`cartopy.mpl.geoaxes.GeoAxes`
            Axis to apply NCL style to.
            
        lines: :class:`matplotlib.contour.QuadContourSet`
            The output of matplotlib's contour/contourf function

        Keyword Args
        ------------
        contour_label_background: :obj:`bool` 
            Whether a white background for the contour labels will be drawn. Default False.

        contour_label_fontsize: :obj:`int` 
            Font size of the contour line labels. Default 12.

        contour_labels: :obj:`list` or :class:`numpy.ndarray` 
            List or array of labels to use for contour line labels.

        draw_contour_labels: :obj:`bool` 
            Whether add contour line labels to the figure.
        """
        if self.contour_label_fontsize is not None:
            fontsize = self.contour_label_fontsize

        # If level range is less than 1, set labels with smaller differences between them
        if not isinstance(self.levels,int) and (self.levels[-1] - self.levels[0]) <= 1:
            fmt = '%0.2f'
        else:
            fmt = '%d'

        # Set contour line labels based on inputted arguments
        if self.contour_labels is None:
            ax.clabel(lines,
                      fontsize=fontsize,
                      fmt=fmt,
                      inline=True,
                      colors="black")
        # If manually assigning labels, use manual kwarg
        elif isinstance(contour_labels, np.ndarray):
            ax.clabel(lines,
                    fontsize = fontsize,
                    fmt = fmt,
                    inline = True,
                    levels = contour_labels,
                    colors="black")
        else:
            ax.clabel(lines,
                    fontsize = fontsize,
                    fmt = fmt,
                    inline = True,
                    manual = contour_labels,
                    colors="black")

        # Add white background to contour line labels
        if background is True:
            [
                txt.set_bbox(dict(facecolor='white', edgecolor='none', pad=2))
                for txt in lines.labelTexts
            ]

        # if a map projection without filled contours, add RHS box label
        if self.contour_fill is False and self.type is None:
            if self.contour_labels is None:
                title = ("CONTOUR FROM " + str(self.levels[0]) + " TO " + 
                        str(self.levels[-1]) + " BY " + 
                        str((self.levels[-1]-self.levels[0])/(len(self.levels)-1)))
            else:
                title = ("CONTOUR FROM " + str(self.contour_labels[0]) + " TO " + 
                        str(self.contour_labels[-1]) + " BY " + 
                        str((self.contour_labels[-1]-self.contour_labels[0])/(len(self.contour_labels)-1)))
            
            self.ax.text(1,
                        -0.15,
                        title,
                        horizontalalignment='right',
                        transform=self.ax.transAxes,
                        bbox=dict(boxstyle='square, pad=0.25',
                        facecolor='white',
                        edgecolor='black'))

    def _estimate_levels(self):
        # TODO: flesh out
        print("estimate levels")
