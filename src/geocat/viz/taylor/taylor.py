"""Taylor Diagrams."""

import numpy as np
import matplotlib.pyplot as plt


class TaylorDiagram(object):
    """Taylor Diagram.

    Taylor diagrams provide a visual framework for comparing a suite of variables from one or more test data sets to
    one or more reference data sets. Commonly, the test data sets are model experiments while the reference data set
    is a control experiment or some reference observations (eg, ECMWF Reanalyses). Generally, the plotted values are
    derived from climatological monthly, seasonal or annual means. Because the different variables (eg:
    precipitation, temperature) may have widely varying numerical values, the results are normalized by the reference
    variables. The ratio of the normalized variances indicates the relative amplitude of the model and observed
    variations.

    References
    ----------
    - https://validate-climate-model-validation.readthedocs.io/en/latest/_modules/validate/taylor.html
    - https://matplotlib.org/stable/gallery/axisartist/demo_floating_axes.html#sphx-glr-gallery-axisartist-demo-floating-axes-py
    - https://www.ncl.ucar.edu/Applications/taylor.shtml
    """

    def __init__(self,
                 refstd=1,
                 fig=None,
                 rect=111,
                 label='REF',
                 std_range=(0, 1.65),
                 std_level=np.arange(0, 1.51, 0.25)):
        """Create base Taylor Diagram.

        Parameters
        ----------
        refstd : float, optional
            reference standard deviation

        fig : matplotlib.figure.Figure, optional
            Optional input figure. Default is None

        rect : int, optional
            Optional subplot definition

        label : string, optional
            Optional reference label string indentifier

        std_range : Tuple, optional
            Optional stddev axis extent

        std_level : list, optional
            Optional list of tick locations for stddev axis
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as fa
        import mpl_toolkits.axisartist.grid_finder as gf

        # Pull and set optional constructor variables
        # Set figure
        self.fig = fig
        if fig is None:
            self.fig = plt.figure(figsize=(8, 8))

        # Reference standard deviation
        self.refstd = refstd

        # Standard deviation axis extent (in units of reference stddev)
        self.smin = std_range[0]
        self.smax = std_range[1]

        # Set polar transform
        tr = PolarAxes.PolarTransform()

        # Set correlation labels
        rlocs = np.concatenate((np.arange(10) / 10., [0.95, 0.99, 1]))
        tlocs = np.arccos(rlocs)  # Conversion to polar angles
        gl1 = gf.FixedLocator(tlocs)  # Positions
        tf1 = gf.DictFormatter(dict(list(zip(tlocs, list(map(str, rlocs))))))

        # Set standard deviation labels
        gl2 = gf.FixedLocator(std_level)

        # format each label with 2 decimal places
        format_string = list(map(lambda x: "{0:0.2f}".format(x), std_level))
        index = np.where(std_level == self.refstd)[0][0]
        format_string[index] = label
        tf2 = gf.DictFormatter(dict(list(zip(std_level, format_string))))

        # Use customized GridHelperCurveLinear to define curved axis
        ghelper = fa.GridHelperCurveLinear(
            tr,
            extremes=(
                0,
                np.pi / 2,  # 1st quadrant only
                self.smin,
                self.smax),
            grid_locator1=gl1,
            tick_formatter1=tf1,
            grid_locator2=gl2,
            tick_formatter2=tf2)

        # Create graphical axes
        ax = fa.FloatingSubplot(self.fig, rect, grid_helper=ghelper)
        self.fig.add_subplot(ax)

        # Adjust axes for Correlation
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("right")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        # Standard deviation ("X axis")
        ax.axis["left"].set_axis_direction("bottom")

        # Standard deviation ("Y axis")
        ax.axis["right"].set_axis_direction("top")
        ax.axis["right"].toggle(ticklabels=True, label=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")
        ax.axis["right"].label.set_text("Standard deviation (Normalized)")

        # Set font sizes, tick sizes, and padding
        ax.axis['top', 'right'].label.set_fontsize(18)
        ax.axis['top', 'right', 'left'].major_ticklabels.set_fontsize(16)
        ax.axis['top', 'right', 'left'].major_ticks.set_ticksize(10)
        ax.axis['top', 'right', 'left'].major_ticklabels.set_pad(8)
        ax.axis['top', 'right'].label.set_pad(6)

        # Bottom axis is not needed
        ax.axis["bottom"].set_visible(False)

        self._ax = ax  # Graphical axes
        self.ax = ax.get_aux_axes(tr)  # Polar coordinates

        # Add reference point stddev contour
        t = np.linspace(0, np.pi / 2)
        r = np.zeros_like(t) + self.refstd
        h, = self.ax.plot(t,
                          r,
                          linewidth=1,
                          linestyle=(0, (9, 5)),
                          color='black',
                          zorder=1)

        # Set aspect ratio
        self.ax.set_aspect('equal')

        # Store the reference line
        self.referenceLine = h

        # Collect sample points for latter use (e.g. legend)
        self.modelMarkerSet = []

        # Set number for models outside axes
        self.modelOutside = -1

    def add_model_set(self,
                      stddev,
                      corrcoef,
                      fontsize=14,
                      xytext=(-5, 7),
                      annotate_on=True,
                      model_outlier_on=False,
                      percent_bias_on=False,
                      bias_array=None,
                      *args,
                      **kwargs):
        """Add a model set (*stddev*, *corrcoeff*) to the Taylor diagram. NCL-
        style model markers and labels are achieved through Matplotlib markers
        and annotations. *xytext* argument can be used to adjust the
        positioning of the label relative to the markers if *annotate_on*
        argument is set to True.

        Parameters
        ----------
        stddev : array-like, list, float
            An array of vertical coordinates of the data points that denote the standard deviation

        corrcoef : array-like, list, float
            An array of horizontal coordinates of the data points that denote correlation
            Input should have the same size as *stddev*

        fontsize : float, optional, default to 14
            Fonsize of marker labels. This argument is suplied to `matplotlib.axes.Axes.annotate` command

        xytext : (float, float), optional, default to (-5,7)
            The position (x, y) to place the marker label at. The coordinate system is set to pixels.
            This argument is supplied to `matplotlib.axes.Axes.annotate` command.

        annotate_on : boolean, optional, default to True
            Determine whether model labels are added

        model_outlier_on : boolean, optional, default to False
            If True, models with negative correlations and standard deviations > TaylorDiagram.smax(default to 1.65)
            are plotted as text at the bottom of the figure; if False, all models are plotted
            according to *stddev* and *corrcoef*

        percent_bias_on : boolean, optional, default to False
            If True, model marker and marker size is plotted based on *bias_array*

        bias_array : array-like, list, float, optional, default to None
            If this is given, it is used to determine individual marker size and marker style internally.
            Input should have the same size as *stddev* and *corrcoef*

        *args* and *kwargs* are directly propagated to the `matplotlib.axes.Axes.scatter` command.


        Returns
        -------
        modelTexts, modelset : array of matplotlib.text.Annotation,
                               array of matplotlib.collections.PathCollection
            A list of text objects representing model labels, and
            a list of sets of markers representing sets of models
        """

        # Convert to np arrays and make copies
        np_std = np.array(stddev)
        np_corr = np.array(corrcoef)
        std_plot = np_std
        corr_plot = np_corr

        # Create a dictionary of key: std, value: annotated number
        stdAndNumber = dict(zip(np_std, range(1, len(np_std) + 1)))

        # If percent_bias_on is True, check inputted arguments
        if percent_bias_on:
            if bias_array is None:
                raise AttributeError(
                    "bias_array argument cannot be None if percent_bias_on is True"
                )
            if kwargs.get("s") or kwargs.get("marker"):
                raise AttributeError(
                    "Do not input s and marker arguments when percent_bias_on is True"
                )
            else:
                bias_plot = np.array(bias_array)

        # if model_outlier_on is True, split all input datasets into models
        # inside taylor diagram and outlier models
        if model_outlier_on:
            # Create a list of boolean conditions
            cond = np.logical_and(np_std <= self.smax, np_corr >= self.smin)

            std_plot = np_std[cond]
            corr_plot = np_corr[cond]
            std_outlier = np_std[np.bitwise_not(cond)]
            corr_outlier = np_corr[np.bitwise_not(cond)]
            if percent_bias_on:
                bias_plot = bias_plot[cond]
                bias_outlier = np.array(bias_array)[np.bitwise_not(cond)]

        # Add model markers inside taylor diagram
        if not percent_bias_on:
            modelset = self.ax.scatter(
                np.arccos(corr_plot),
                std_plot,  # theta, radius
                *args,
                **kwargs)
        else:
            for i in range(len(corr_plot)):
                size, marker = self._bias_to_marker_size(bias_plot[i])
                modelset = self.ax.scatter(
                    np.arccos(corr_plot)[i],  # theta
                    std_plot[i],  # radius
                    s=size,
                    marker=marker,
                    *args,
                    **kwargs)

        # grab color
        color = kwargs.get('color')
        if color is None:
            color = kwargs.get('edgecolors')
            if color is None:
                color = kwargs.get('facecolors')

        # Add modelset to modelMarkerSet for legend handles
        if not percent_bias_on:
            self.modelMarkerSet.append(modelset)
        else:
            label = kwargs.get('label')
            if percent_bias_on:
                handle = plt.scatter(1, 2, color=color, label=label)
                self.modelMarkerSet.append(handle)

        # Annotate model markers if annotate_on is True
        if annotate_on:
            # Initialize empty array that will be filled with model label text objects and returned
            modelTexts = []

            for std, corr in zip(std_plot, corr_plot):
                label = str(stdAndNumber[std])
                textObject = self.ax.annotate(label, (np.arccos(corr), std),
                                              fontsize=fontsize,
                                              color=color,
                                              textcoords="offset pixels",
                                              xytext=xytext)
                modelTexts.append(textObject)

        # Plot outlier model stats
        if model_outlier_on:
            if len(std_outlier) > 0:
                for std, corr in zip(std_outlier, corr_outlier):
                    self.modelOutside += 1  # outlier model number increases

                    # Plot markers
                    if not percent_bias_on:
                        self.ax.scatter(0.054 + self.modelOutside * 0.22,
                                        -0.105,
                                        *args,
                                        **kwargs,
                                        clip_on=False,
                                        transform=self.ax.transAxes)
                    else:
                        for i in range(len(bias_outlier)):
                            size, marker = self._bias_to_marker_size(
                                bias_outlier[i])
                            self.ax.scatter(0.054 + self.modelOutside * 0.22,
                                            -0.105,
                                            *args,
                                            **kwargs,
                                            s=size,
                                            marker=marker,
                                            clip_on=False,
                                            transform=self.ax.transAxes)
                    # Plot labels
                    textObject = self.ax.text(0.045 + self.modelOutside * 0.22,
                                              -0.08,
                                              str(stdAndNumber[std]),
                                              fontsize=fontsize,
                                              transform=self.ax.transAxes)
                    modelTexts.append(textObject)

                    # Plot std against corr in the form of fraction
                    self.ax.text(0.08 + self.modelOutside * 0.22,
                                 -0.10,
                                 r'$\frac{%.2f}{%.2f}$' % (std, corr),
                                 fontsize=17,
                                 transform=self.ax.transAxes)

        return modelTexts, modelset

    def add_xgrid(self,
                  arr,
                  color='lightgray',
                  linestyle=(0, (9, 5)),
                  linewidth=0.5,
                  **kwargs):
        """Add gridlines to the X axis (correlation) specified by array *arr*

        Parameters
        ----------
        arr : array-like, list, float
            An array of horizontal coordinates of the data points that denote correlation

        color : str, optional, default to "lightgray"
            Color of the gridline

        linestyle : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}, optional, default to (0, (9,5))
            See matplotlib Linestyle examples

        linewidth : float, optional, default to 0.5
            Set the line width in points

        kwargs are directly propagated to the `matplotlib.axes.Axes.vlines` command.

        Returns
        -------
        None
        """

        for value in arr:
            self.ax.vlines([np.arccos(value)],
                           ymin=self.smin,
                           ymax=self.smax,
                           color=color,
                           linestyle=linestyle,
                           linewidth=linewidth,
                           **kwargs)

    def add_ygrid(self,
                  arr,
                  color='lightgray',
                  linestyle=(0, (9, 5)),
                  linewidth=1,
                  **kwargs):
        """Add gridlines (radii) to the Y axis (standard deviation) specified
        by array *arr*

        Parameters
        ----------
        arr : array-like, list, float
            An array of vertical coordinates of the data points that denote standard deviation

        color : str, optional, default to "lightgray"
            Color of the gridline

        linestyle : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}, optional, default to (0, (9,5))
            See matplotlib Linestyle examples

        linewidth : float, optional, default to 1
            Set the line width in points

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.plot` command.

        Returns
        -------
        None
        """
        t = np.linspace(0, np.pi / 2)
        for value in arr:
            r = np.zeros_like(t) + value
            h, = self.ax.plot(t,
                              r,
                              color=color,
                              linestyle=linestyle,
                              linewidth=linewidth,
                              **kwargs)

    def add_grid(self, *args, **kwargs):
        """Add a grid.

        Parameters
        ----------
        *args* and *kwargs* are propagated to `matplotlib.axes.Axes.grid`
        """
        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours.

        Parameters
        ----------
        levels : int or array-like, optional, default to 5
            Determines the number and positions of the contour lines

        *args* and *kwargs* are propagated to `matplotlib.axes.Axes.contour`

        Returns
        -------
        QuadContourSet
        """
        # Return coordinate matrices from coordinate vectors
        rs, ts = np.meshgrid(np.linspace(self.smin, self.smax),
                             np.linspace(0, np.pi / 2))

        # Compute centered RMS difference
        rms = np.sqrt(self.refstd**2 + rs**2 -
                      2 * self.refstd * rs * np.cos(ts))

        # Create contour lines
        contours = self.ax.contour(ts, rs, rms, levels, **kwargs)

        return contours

    def add_model_name(self,
                       namearr,
                       x_loc=0.1,
                       y_loc=0.31,
                       verticalalignment='top',
                       fontsize=13,
                       **kwargs):
        """Add texts of model names.

        The coordinate system of the Axes(transAxes) is used for more intuitive positioning of the texts.
        (x_loc=0, y_loc=0) is bottom left of the axes, and (x_loc=1, y_loc=1) is top right of the axes.

        Parameters
        ----------
        namearr : array-like
            List of model names

        x_loc : float, optional, default to 0.1
            x component of text position

        y_loc : float, optional, default to 0.31
            y component of text position

        verticalalignment : str, optional, default to 'top'
            Vertical alignment. Options: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

        fontsize : float, optional, default to 13
            Text fontsize

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.text` command

        Return
        ------
        None
        """
        text = [str(i + 1) + ' - ' + namearr[i] for i in range(len(namearr))]
        text = '\n'.join(text)

        self.ax.text(x_loc,
                     y_loc,
                     text,
                     verticalalignment=verticalalignment,
                     fontsize=fontsize,
                     transform=self.ax.transAxes,
                     **kwargs)

    def add_bias_legend(self):
        """Add bias legend to the upper left hand corner."""
        text = "-  /  +     Bias\n"
        percent = [">20%", "10-20%", "5-10%", "1-5%", "<1%"]

        self.ax.text(0.07,
                     0.92,
                     text,
                     fontsize=11,
                     verticalalignment="top",
                     transform=self.ax.transAxes)

        y_loc = 0.87
        size = [130, 90, 50, 30, 60]
        marker1 = "v"
        marker2 = "^"
        for i in range(5):
            if i == 4:
                marker1 = "o"
                marker2 = "o"
            self.ax.scatter(0.08,
                            y_loc,
                            s=size[i],
                            marker=marker1,
                            edgecolors='black',
                            facecolors="None",
                            linewidths=0.5,
                            transform=self.ax.transAxes)
            self.ax.scatter(0.13,
                            y_loc,
                            s=size[i],
                            marker=marker2,
                            edgecolors='black',
                            facecolors="None",
                            linewidths=0.5,
                            transform=self.ax.transAxes)
            self.ax.text(0.18,
                         y_loc - 0.01,
                         percent[i],
                         fontsize=11,
                         transform=self.ax.transAxes)

            y_loc -= 0.04

    def add_legend(self,
                   xloc=1.1,
                   yloc=0.95,
                   loc="upper right",
                   fontsize=14,
                   **kwargs):
        """Add a figure legend.

        The coordinate system is Axes(transAxes).
        (x_loc=0, y_loc=0) is bottom left of the axes, and (x_loc=1, y_loc=1) is top right of the axes.

        Parameters
        ----------
        xloc : float, optional, default to 1.1
            x location of legend position, supplied to bbox_to_anchor()

        yloc : float, optional, default to 0.95
            y location of legend position, upplied to bbox_to_anchor().

        loc : str, optional, default to 'upper right'
            See Matplotlib legend documentations

        fontsize : float, optional, default to 14
            Text fontsize

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.legend` command
        *kwargs* are directly propagated to the `matplotlib.pyplot.legend` command.

        Return
        ------
        legend : matplotlib.legend.Legend
            Matplotlib legend object
        """

        if kwargs.get('handles') is None:
            handles = self.modelMarkerSet[::-1]
        if kwargs.get('labels') is None:
            labels = [p.get_label() for p in handles]

        legend = self.ax.legend(handles,
                                labels,
                                loc=loc,
                                bbox_to_anchor=(xloc, yloc),
                                fontsize=fontsize,
                                frameon=False)
        return legend

    def add_title(self, maintitle, fontsize=18, y_loc=None, **kwargs):
        """Add a main title.

        Parameters
        ----------
        maintitle : str
            Title text

        fontsize : float, optional
            Text fontsize

        y_loc : float, optional, default to None
            Vertical Axes location. 1.0 is the top.

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.set_title` command.

        Return
        ------
        None
        """

        self._ax.set_title(maintitle, fontsize=fontsize, y=y_loc, **kwargs)

    def set_fontsizes_and_pad(self,
                              ticklabel_fontsize=14,
                              axislabel_fontsize=16,
                              axislabel_pad=8):
        """Reset ticklabel and axis label fontsizes, and axis label padding.

        Parameters
        ----------
        ticklabel_fontsize : float, optional, default to 14
            Fontsize of all tick labels

        axislabel_fontsize : float, optional, default to 16
            Fontsize of axis labels

        axislabel_pad : float, optional, default to 8
            Padding between axis labels and axis

        Return
        ------
        None
        """

        self._ax.axis['top', 'right',
                      'left'].major_ticklabels.set_fontsize(ticklabel_fontsize)
        self._ax.axis['top', 'right'].label.set_fontsize(axislabel_fontsize)
        self._ax.axis['top', 'right'].label.set_pad(axislabel_pad)

    # Internal functions
    def _bias_to_marker_size(self, bias):
        """Internal helper function to return integer marker size and string
        marker symbol based on input bias.

        Parameters
        ----------
        bias : int, float
            Bais value to dictate the size of the marker size and string marker

        Returns
        -------
        marker_size, maker_symbol : int,
                                    char
            Determined size of marker in pts,
            Determined matplotlib symbol dictating symbol
        """

        ab = abs(bias)
        if ab > 20:
            marker_size = 130
        elif 10 < ab <= 20:
            marker_size = 90
        elif 5 < ab <= 10:
            marker_size = 50
        elif 1 < ab <= 5:
            marker_size = 30
        else:
            marker_size = 60

        if ab <= 1:
            marker_symbol = 'o'
        elif bias > 0:
            marker_symbol = '^'
        else:
            marker_symbol = 'v'

        return marker_size, marker_symbol
