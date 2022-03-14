"""Plotting wrapper for matplotlib contourf function."""

import numpy as np
import cartopy.crs as ccrs

from _plot_util import NCL_Plot


class Contour(NCL_Plot):
    """Create contour plot.

    Args
    ----
    data: :class:`xarray.DataArray` or :class:`numpy.ndarray`
        The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.

    Keyword Args
    ------------
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

    Note
    ----
    All other keyword args will be passed to NCL_Plot. To see its list of 
    keyword args, see its documentation page.

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

        Note
        ----
        All other keyword args will be passed to NCL_Plot. To see its list of 
        keyword args, see its documentation page.

        If creating a Pressure/Height figure, pressure will be converted to
        height using the U.S. standard atomsphere.

        """

        # Valid kwargs
        contour_kwargs = {'contour_fill', 'contour_lines', 'contour_label_background', 
            'contour_label_fontsize', 'contour_label_box', 'contour_labels', 
            'draw_contour_labels', 'levels'}
        
        # Dictionary of default values
        default_kwargs = {'draw_contour_labels' : False, 'projection' : ccrs.PlateCarree()}

        super().__init__(contour_kwargs, default_kwargs, *args, **kwargs)

        # If any aspect about contour labels is specified, draw them
        if (self.draw_contour_labels is True 
            or self.contour_labels is not None
            or self.contour_label_background is not None
            or self.contour_label_fontsize is not None):
            # Try to draw contour labels on contour lines
            if hasattr(self, 'cl'):
                self.add_contour_labels(ax = self.ax,
                                         lines = self.cl,
                                         contour_labels=self.contour_labels,
                                         fontsize=self.contour_label_fontsize,
                                         background=self.contour_label_background)
            # If there aren't any, try to draw them on filled contours
            else:
                if self.contour_fill is not False:
                    self.add_contour_labels(ax = self.ax,
                                             lines = self.cf,
                                             contour_labels=self.contour_labels,
                                             fontsize=self.contour_label_fontsize,
                                             background=self.contour_label_background)

        # Call colorbar creation from parent class
        # Set colorbar if specified

        # If not a subplot and add_colorbar and contour_fill is not false, add colorbar
        if (((self.add_colorbar is not False) and
             (self.add_colorbar != 'off') and
             (self.contour_fill is not False) and
             (self.subplot is None)) or
                # If subplot, check if in last position in subplot and that add_colorbar is not False and plot
            ((self.add_colorbar is not False) and
             (self.contour_fill is not False) and
             (self.subplot[2] == self.subplot[0] * self.subplot[1]) and
             (self.add_colorbar != "off") and
             ((self.individual_cb is not True) or
              (self.overlay.individual_cb is not True)) or
             (self.individual_cb is True))):

            super().add_colorbar(mappable=self.cf)


    def _class_kwarg_handling(self, *args, **kwargs):
        # if the type is press_height, set projection to none
        if self.type == "press_height":
            self.projection = None
            if self.yscale is None:
                self.yscale = "log"
            if self.ylim == [-90, 90]:
                self.ylim = (1000,10)
            if self.yticks is None:
                self.yticks = [1000, 850, 700, 500, 400, 300, 250, 150, 100, 70, 50, 30, 10]
            if self.yticklabels is None:
                self.yticklabels = [1000, 850, 700, 500, 400, 300, 250, 150, 100, 70, 50, 30, 10]
            if self.xlabel is None:
                self.xlabel = ""
            if self.ylabel is None:
                self.ylabel = str(self.orig.lev.long_name) + " [" + str(self.orig.lev.units) + "]"
            if self.overlay is None:
                if kwargs.get('xlim') is None and 'at' in self.X.name:
                    self.xlim = [-90, 90]
                elif kwargs.get('xlim') is None and 'on' in self.X.name:
                    self.xlim = [-180, 180]
        
        # if there aren't filled contours, don't draw colorbar
        if self.contour_fill is False and self.add_colorbar is None:
            self.add_colorbar = False

        # If levels aren't specified, calculate them
        if self.levels is None:
            # take a guess at filled levels
            self._estimate_levels()

    def _plot(self, *args, **kwargs):
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

    def add_contour_labels(self,
                            ax = None,
                            lines = None,
                            contour_labels = None,
                            background = None,
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
        # Set up kwargs so that function can be called outside of initial contour creation
        if ax is None:
            ax = self.ax
        
        if lines is None:
            # add contour labels to contour lines before filled contours
            if hasattr(self, 'cl'):
                lines = self.cl
            else:
                lines = self.cf
        
        if contour_labels is None:
            contour_labels = self.contour_labels

        if background is None:
            background = self.contour_label_background

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
        if ((self.contour_fill is False and self.type is None and self.contour_label_box is not False and self.overlay is None) 
            or (self.contour_label_box is True and self.overlay is None)
            or (self.contour_label_box is True and self.overlay.contour_label_box is not True)):
            if self.contour_labels is None:
                title = ("CONTOUR FROM " + str(round(lines.levels[0],1)) + " TO " + 
                        str(round(lines.levels[-1],1)) + " BY " + 
                        str(round((lines.levels[-1]-lines.levels[0])/(len(lines.levels)-1), 1)))
            else:
                title = ("CONTOUR FROM " + str(round(self.contour_labels[0],1)) + " TO " + 
                        str(round(self.contour_labels[-1],1)) + " BY " + 
                        str(round((self.contour_labels[-1]-self.contour_labels[0])/(len(self.contour_labels)-1), 1)))
            
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
