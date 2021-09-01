"""Plotting wrapper for matplotlib contourf function."""

import xarray as xr

from _set_up_fig import _fig_ax
from _plot_util import NCL_Plot


class Contour(NCL_Plot):
    """Create contour plot with optional contour labels.

    Args:

        data (:class:`xarray.DataArray` or :class:`numpy.ndarray`): The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.

    Kwargs:

        add_colorbar (:obj:`bool`): Whether a colorbar is added to the figure. Default True.

        clevels (:obj:`list` or :class:`numpy.ndarray`): List or array of levels to be passed into matplotlib's contour function.

        cmap (:class:`cmaps.colormap.Colormap`): Colormap for the filled contour graph.

        contour_fill (:obj:`bool`): Whether filled contours will be drawn. Default True.

        contour_lines (:obj:`bool`): Whether contours lines will be drawn. Default True.

        contourbackground (:obj:`bool`): Whether a white background for the contour labels will be drawn. Default False.

        contourfontsize (:obj:`int`): Font size of the contour line labels. Default 12.

        contourlabels (:obj:`list` or :class:`numpy.ndarray`): List or array of labels to use for contour line labels.

        drawcontourlabels(:obj:`bool`): Whether add contour line labels to the figure.

        flevels (:obj:`list` or :class:`numpy.ndarray`): List or array of levels to be passed into matplotlib's contourf function.

        linecolor (:obj:`str`): Color of the contour line. Default "black".

        linestyle (:obj:`str`): Linestyle of the contour line. Default solid for positive values, dashed for negative values.

        linewidth (:obj:`int`): Width of the contour lines. Default 0.4.

        manualcontourlabels (:obj:`bool`): Whether contour line labels should be manually drawn. Default False.

        projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

        X (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The X axis data for the dataset. To be specified if not inferred correctly automatically.

        Y (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The Y axis data for the dataset. To be specified if not inferred correctly automatically.

    Return:
        (:class:`contourf.Contour`) A contour plot with specified input style.
    """

    def __init__(self, *args, **kwargs):
        """Create contour figure. Generate filled contours and/or contour lines
        for figure. Add colorbar and contour labels if specified.

        Args:

            data (:class:`xarray.DataArray` or :class:`numpy.ndarray`): The dataset to plot. If inputted as a Xarray file, titles and labels will be automatically inferred.

        Kwargs:

            add_colorbar (:obj:`bool`): Whether a colorbar is added to the figure. Default True.

            clevels (:obj:`list` or :class:`numpy.ndarray`): List or array of levels to be passed into matplotlib's contour function.

            cmap (:class:`cmaps.colormap.Colormap`): Colormap for the filled contour graph.

            contour_fill (:obj:`bool`): Whether filled contours will be drawn. Default True.

            contour_lines (:obj:`bool`): Whether contours lines will be drawn. Default True.

            contourbackground (:obj:`bool`): Whether a white background for the contour labels will be drawn. Default False.

            contourfontsize (:obj:`int`): Font size of the contour line labels. Default 12.

            contourlabels (:obj:`list` or :class:`numpy.ndarray`): List or array of labels to use for contour line labels.

            drawcontourlabels(:obj:`bool`): Whether add contour line labels to the figure.

            flevels (:obj:`list` or :class:`numpy.ndarray`): List or array of levels to be passed into matplotlib's contourf function.

            linecolor (:obj:`str`): Color of the contour line. Default "black".

            linestyle (:obj:`str`): Linestyle of the contour line. Default solid for positive values, dashed for negative values.

            linewidth (:obj:`int`): Width of the contour lines. Default 0.4.

            manualcontourlabels (:obj:`bool`): Whether contour line labels should be manually drawn. Default False.

            projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

            X (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The X axis data for the dataset. To be specified if not inferred correctly automatically.

            Y (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The Y axis data for the dataset. To be specified if not inferred correctly automatically.
        """

        # Set default flevels, clevels, and colormap
        self._default_cmap = 'coolwarm'
        self._default_flevels = 5
        self._default_clevels = 7

        # Pull out args from data
        self.data = args[0]

        # If xarray file, format as Numpy array
        if isinstance(self.data, xr.DataArray):
            self.orig = self.data
            self.data = self.data.values

        # Read in or calculate filled levels using built in function
        if kwargs.get('contour_fill') is not False:
            if kwargs.get('flevels') is not None:
                # levels defined by kwargs
                self.levels = kwargs.get('flevels')
            elif kwargs.get('flevels') is None:
                # take a guess at filled levels
                self._estimate_flevels()

        # Pull in X and Y axis data if specified
        if kwargs.get("X") is not None:
            self.X = kwargs.get("X")
            if kwargs.get("Y") is None:
                raise AttributeError("If X is defined, Y must also be defined.")
        else:
            self.X = kwargs.get("X")

        if kwargs.get("Y") is not None:
            self.Y = kwargs.get("Y")
            if kwargs.get("X") is None:
                raise AttributeError("If Y is defined, X must also be defined.")
        else:
            self.Y = kwargs.get("Y")

        # Pull in whether to draw filled contours and/or contour lines
        self.contour_lines = kwargs.get('contour_lines')
        self.contour_fill = kwargs.get('contour_fill')

        # Read in or calculate contour levels using built in function
        if kwargs.get('contour_lines') is not False:
            if kwargs.get('clevels') is not None:
                # levels defined by kwargs
                self.levels = kwargs.get('clevels')
            elif kwargs.get('clevels') is None:
                # take a guess at filled levels
                self._estimate_clevels()

        # Read in style of contour lines
        if kwargs.get("linecolor") is None:
            self.linecolor = "black"
        else:
            self.linecolor = kwargs.get("linecolor")

        self.linestyle = kwargs.get("linestyle")

        if kwargs.get("linewidth") is None:
            self.linewidth = 0.4
        else:
            self.linewidth = kwargs.get("linewidth")

        # Set colormap to specified or default value
        if kwargs.get('cmap') is not None:
            self.cmap = kwargs.get('cmap')
        else:
            self.cmap = self._default_cmap

        # Pull out contour line label specific kwargs
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

        # Add filled contours and/or contour lines to figure, as specified
        self._generate_contours()

        # Set figure in NCL style
        _fig_ax._set_NCL_style(self, self.ax)

        # If contour labels are requested, try to set them on contour lines. If failed, use filled contours
        if self.draw_contour_labels is True:
            try:
                self._add_contour_labels(self.ax,
                                         self.cl,
                                         contourlabels=self.contourlabels,
                                         fontsize=self.contourfontsize,
                                         background=self.contourbackground)
            except:
                if self.contour_fill is not False:
                    self._add_contour_labels(self.ax,
                                             self.cf,
                                             contourlabels=self.contourlabels,
                                             fontsize=self.contourfontsize,
                                             background=self.contourbackground)

        # Call colorbar creation from parent class
        # Set colorbar if specified

        # If not a subplot and add_colorbar and contour_fill is not false, add colorbar
        if (((self.add_colorbar is not False) and
             (self.add_colorbar != 'off') and
             (kwargs.get('contour_fill') is not False) and
             (self.subplot is None)) or
                # If subplot, check if in last position in subplot and that add_colorbar is not False and plot
            ((self.add_colorbar is not False) and
             (self.subplot[2] == self.subplot[0] * self.subplot[1]) and
             (self.add_colorbar != "off") and
             ((self.individual_cb is not True) or
              (self.ref_fig.individual_cb is not True)) or
             (self.individual_cb is True))):

            self._add_colorbar(mappable=self.cf)

    def _generate_contours(self, *args, **kwargs):
        """Generate filled contours and/or contour lines for figure.

        Kwargs:

            cmap (:class:`cmaps.colormap.Colormap`): Colormap for the filled contour graph.

            contour_fill (:obj:`bool`): Whether filled contours will be drawn. Default True.

            contour_lines (:obj:`bool`): Whether contours lines will be drawn. Default True.

            linecolor (:obj:`str`): Color of the contour line. Default "black".

            linestyle (:obj:`str`): Linestyle of the contour line. Default solid for positive values, dashed for negative values.

            linewidth (:obj:`int`): Width of the contour lines. Default 0.4.

            projection (:obj:`str`): Cartopy map projection. `See Cartopy documentation for full list. <https://scitools.org.uk/cartopy/docs/latest/crs/projections.html>`_

            X (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The X axis data for the dataset. To be specified if not inferred correctly automatically.

            Y (:class:`xarray.core.dataarray.DataArray'>` or :class:`numpy.ndarray`): The Y axis data for the dataset. To be specified if not inferred correctly automatically.
        """

        # If there is a projection and specified X and Y data, plot filled contours and contour lines unless otherwise specified
        if self.projection is not None:
            if (self.X is not None) and (self.Y is not None):
                # Create plot
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
                                               ],
                                               extend=self.cbextend)

                if self.contour_lines is not False:
                    self.cl = self.ax.contour(self.X.data,
                                              self.Y.data,
                                              self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=self.linewidth,
                                              linestyles=self.linestyle,
                                              transform=self.projection,
                                              extent=[
                                                  self.xlim[0], self.xlim[1],
                                                  self.ylim[0], self.ylim[1]
                                              ],
                                              extend=self.cbextend)
            # If there is a projection and no specified X and Y data, plot filled contours and contour lines unless otherwise specified
            else:
                # Create plot
                if self.contour_fill is not False:
                    self.cf = self.ax.contourf(self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               transform=self.projection,
                                               extent=[
                                                   self.xlim[0], self.xlim[1],
                                                   self.ylim[0], self.ylim[1]
                                               ],
                                               extend=self.cbextend)

                if self.contour_lines is not False:
                    self.cl = self.ax.contour(self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=self.linewidth,
                                              linestyles=self.linestyle,
                                              transform=self.projection,
                                              extent=[
                                                  self.xlim[0], self.xlim[1],
                                                  self.ylim[0], self.ylim[1]
                                              ],
                                              extend=self.cbextend)
        # If there is not a specified projection and specified X and Y data, plot filled contours and contour lines unless otherwise specified
        else:
            if (self.X is not None) and (self.Y is not None):
                # Create plot
                if self.contour_fill is not False:
                    self.cf = self.ax.contourf(self.X.data,
                                               self.Y.data,
                                               self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               extent=[
                                                   self.xlim[0], self.xlim[1],
                                                   self.ylim[0], self.ylim[1]
                                               ],
                                               extend=self.cbextend)

                if self.contour_lines is not False:
                    self.cl = self.ax.contour(self.X.data,
                                              self.Y.data,
                                              self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=self.linewidth,
                                              linestyles=self.linestyle,
                                              extent=[
                                                  self.xlim[0], self.xlim[1],
                                                  self.ylim[0], self.ylim[1]
                                              ],
                                              extend=self.cbextend)
            # If there is not a specified projection and no specified X and Y data, plot filled contours and contour lines unless otherwise specified
            else:
                # Create plot
                if self.contour_fill is not False:
                    self.cf = self.ax.contourf(self.data,
                                               levels=self.levels,
                                               cmap=self.cmap,
                                               extent=[
                                                   self.xlim[0], self.xlim[1],
                                                   self.ylim[0], self.ylim[1]
                                               ],
                                               extend=self.cbextend)

                if self.contour_lines is not False:
                    self.cl = self.ax.contour(self.data,
                                              levels=self.levels,
                                              colors=self.linecolor,
                                              alpha=0.8,
                                              linewidths=self.linewidth,
                                              linestyles=self.linestyle,
                                              extent=[
                                                  self.xlim[0], self.xlim[1],
                                                  self.ylim[0], self.ylim[1]
                                              ],
                                              extend=self.cbextend)

    def _add_contour_labels(self,
                            ax,
                            lines,
                            contourlabels=None,
                            background=True,
                            fontsize=12):
        """Add contour line labels with an optional white background to the
        figure.

        Kwargs:

            contourbackground (:obj:`bool`): Whether a white background for the contour labels will be drawn. Default False.

            contourfontsize (:obj:`int`): Font size of the contour line labels. Default 12.

            contourlabels (:obj:`list` or :class:`numpy.ndarray`): List or array of labels to use for contour line labels.

            drawcontourlabels(:obj:`bool`): Whether add contour line labels to the figure.

            flevels (:obj:`list` or :class:`numpy.ndarray`): List or array of levels to be passed into matplotlib's contourf function.

            manualcontourlabels (:obj:`bool`): Whether contour line labels should be manually drawn. Default False.
        """

        # Update argument definitions
        if self.contourfontsize is not None:
            fontsize = self.contourfontsize

        # If level range is less than 1, set labels with smaller differences between them
        if (self.levels[-1] - self.levels[0]) <= 1:
            fmt = '%0.2f'
        else:
            fmt = '%d'

        # Set contour line labels based on inputted arguments. Depending on which arguments are included or not, contour labels must be created differently.
        if self.contourlabels is None:
            ax.clabel(lines,
                      fontsize=fontsize,
                      fmt=fmt,
                      inline=True,
                      colors="black")
        elif self.manualcontourlabels is False:
            ax.clabel(lines,
                      contourlabels,
                      fontsize=fontsize,
                      fmt=fmt,
                      inline=True,
                      colors="black")
        elif self.manualcontourlabels is True:
            ax.clabel(lines,
                      fontsize=fontsize,
                      fmt=fmt,
                      inline=True,
                      manual=contourlabels,
                      colors="black")
        else:
            raise AttributeError(
                "Manualcontourlabels, if set, must be True or False.")

        # Add white background to contour line labels
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
