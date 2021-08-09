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
                 stdrange=(0, 1.6),
                 stdlevel=np.arange(0, 1.51, 0.25)):
        """Create base Taylor Diagram.

        Parameters
        ----------

        refstd : float
            reference standard deviation

        fig : matplotlib.figure.Figure, Optional
            Optional input figure. Default is None

        rect : int, Optional
            Optional subplot definition

        label : string, Optional
            Optional reference label string indentifier

        stdrange : Tuple, Optional
            Optional stddev axis extent

        stdlevel : list, Optional
            Optional list of tick locations for stddev axis
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as fa
        import mpl_toolkits.axisartist.grid_finder as gf

        # Pull and set optional constructor variables
        # Set figure
        if fig is None:
            fig = plt.figure(figsize=(8, 8))
        else:
            self.fig = fig

        # Reference standard deviation
        self.refstd = refstd

        # Standard deviation axis extent (in units of reference stddev)
        self.smin = stdrange[0]
        self.smax = stdrange[1]

        # Set polar transform
        tr = PolarAxes.PolarTransform()

        # Set correlation labels
        rlocs = np.concatenate((np.arange(10) / 10., [0.95, 0.99, 1]))
        tlocs = np.arccos(rlocs)  # Conversion to polar angles
        gl1 = gf.FixedLocator(tlocs)  # Positions
        tf1 = gf.DictFormatter(dict(list(zip(tlocs, list(map(str, rlocs))))))

        # Set standard deviation labels
        gl2 = gf.FixedLocator(stdlevel)

        # format each label with 2 decimal places
        format_string = list(map(lambda x: "{0:0.2f}".format(x), stdlevel))
        index = np.where(stdlevel == self.refstd)[0][0]
        format_string[index] = label
        tf2 = gf.DictFormatter(dict(list(zip(stdlevel, format_string))))

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
        ax = fa.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)

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

        # Store the reference line
        self.referenceLine = h

        # Collect sample points for latter use (e.g. legend)
        self.modelList = []

        # Set aspect ratio
        self.ax.set_aspect(1)

    def add_sample(self,
                   stddev,
                   corrcoef,
                   fontsize=14,
                   xytext=(-5, 7),
                   annotate_on=True,
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

        fontsize : float, default to 14
            Fonsize of marker labels. This argument is suplied to `matplotlib.axes.Axes.annotate` command

        xytext : (float, float), default to (-5,7)
            The position (x, y) to place the marker label at. The coordinate system is set to pixels.
            This argument is supplied to `matplotlib.axes.Axes.annotate` command.

        annotate_on : boolean, default to True
            Determine whether model labels are added

        args and kwargs are directly propagated to the `matplotlib.axes.Axes.plot` command.


        Returns
        -------
        modelset : list of Line2D
            A list of lines representing the plotted data.
        """

        # Add a set of model markers
        modelset, = self.ax.plot(
            np.arccos(corrcoef),  # theta
            stddev,  # radius
            *args,
            **kwargs)
        self.modelList.append(modelset)

        if annotate_on:
            index = 0
            color = kwargs.get('color')

            # Annotate model markers
            for std, corr in zip(stddev, corrcoef):
                index = index + 1
                text = str(index)
                self.ax.annotate(text, (np.arccos(corr), std),
                                 fontsize=fontsize,
                                 color=color,
                                 textcoords="offset pixels",
                                 xytext=xytext)
        return modelset

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

        color : str, default to "lightgray"
            Color of the gridline

        linestyle : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}, default to (0, (9,5))
            See matplotlib Linestyle examples

        linewidth : float, default to 0.5
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

        color : str, default to "lightgray"
            Color of the gridline

        linestyle : {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}, default to (0, (9,5))
            See matplotlib Linestyle examples

        linewidth : float, default to 1
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

        Returns
        -------
        None
        """
        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours.

        Parameters
        ----------

        levels : int or array-like, default to 5
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

        x_loc, y_loc : float,  default to 0.1, 0.31
            Text position

        verticalalignment : str, default to 'top'
            Vertical alignment. Options: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}

        fontsize : float, default to 13
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

        xloc : float
            x location of legend position, supplied to bbox_to_anchor()

        yloc : float, optional, default to 1.1, 0.95
            y location of legend position, upplied to bbox_to_anchor().

        loc : str, optional, default to 'upper right'
            See Matplotlib legend documentations

        fontsize : float, default to 14
            Text fontsize

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.legend` command

        Return
        ------
        None

        *kwargs* are directly propagated to the `matplotlib.pyplot.legend` command.
        """
        if kwargs.get('handles') is None:
            handles = self.modelList
        if kwargs.get('labels') is None:
            labels = [p.get_label() for p in self.modelList]

        self.ax.legend(handles,
                       labels,
                       loc=loc,
                       bbox_to_anchor=(xloc, yloc),
                       fontsize=fontsize,
                       frameon=False)

    def add_title(self, maintitle, fontsize=18, y_loc=None, **kwargs):
        """Add a main title.

        Parameters
        ----------
        maintitle : str
            Title text

        fontsize : float
            Text fontsize

        y_loc : float, default to None
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
        ticklabel_fontsize : float, default to 14
            Fontsize of all tick labels
        axislabel_fontsize : float, default to 16
            Fontsize of axis labels
        axislabel_pad : float, default to 8
            Padding between axis labels and axis

        Return
        ------
        None
        """
        self._ax.axis['top', 'right',
                      'left'].major_ticklabels.set_fontsize(ticklabel_fontsize)
        self._ax.axis['top', 'right'].label.set_fontsize(axislabel_fontsize)
        self._ax.axis['top', 'right'].label.set_pad(axislabel_pad)


###############################################################################
# NCL taylor plots


def taylor_6():
    # https://www.ncl.ucar.edu/Applications/Images/taylor_6_3_lg.png

    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)

    # Create a list of model names
    namearr = ["SLP", "Tsfc", "Prc", "Prc 30S-30N", "LW", "SW", "U300", "Guess"]
    nModel = len(namearr)

    # Create a list of case names
    casearr = ["Case A", "Case B", "Case C", "Case D", "Case E"]
    nCase = len(casearr)

    # Create lists of colors, labels, and main titles
    colors = ["red", "blue", "green", "magenta", "orange"]
    labels = ["Case A", "Case B", "Case C", "Case D", "Case E"]
    maintitles = ["DJF", "JJA", "MAM", "SON"]

    rect = 221

    for i in range(4):
        # Generate one plot for each season + annual
        stddev = np.random.normal(1, 0.25, (nCase, nModel))
        corrcoef = np.random.uniform(0.7, 1, (nCase, nModel))

        # Create taylor diagram
        da = TaylorDiagram(fig=fig, rect=rect + i, label='REF')

        # Add models case by case
        for j in range(stddev.shape[0] - 1, -1, -1):
            da.add_sample(stddev[j],
                          corrcoef[j],
                          xytext=(-4, 5),
                          fontsize=10,
                          color=colors[j],
                          label=labels[j],
                          marker='o',
                          markersize=5,
                          linestyle='none')
        # Add legend
        da.add_legend(1.1, 1.05, fontsize=9)
        # Set fontsize and pad
        da.set_fontsizes_and_pad(11, 13, 2)
        # Add title
        da.add_title(maintitles[i], 14, 1.05)
        # Add model names
        da.add_model_name(namearr, x_loc=0.08, y_loc=0.4, fontsize=8)

    return fig


def taylor_3():
    # https://www.ncl.ucar.edu/Applications/Images/taylor_3_lg.png

    # Case A
    CA_ratio = [1.230, 0.988, 1.092, 1.172, 1.064, 0.966, 1.079, 0.781]
    CA_cc = [0.958, 0.973, 0.740, 0.743, 0.922, 0.982, 0.952, 0.433]

    # Case B
    CB_ratio = [1.129, 0.996, 1.016, 1.134, 1.023, 0.962, 1.048, 0.852]
    CB_cc = [0.963, 0.975, 0.801, 0.814, 0.946, 0.984, 0.968, 0.647]

    # Create figure and TaylorDiagram instance
    fig = plt.figure(figsize=(8, 8))
    dia = TaylorDiagram(fig=fig, label='REF')

    # Add models to Taylor diagram
    dia.add_sample(CB_ratio,
                   CB_cc,
                   color='blue',
                   marker='o',
                   linestyle='none',
                   label='case B')

    dia.add_sample(CA_ratio,
                   CA_cc,
                   color='red',
                   marker='o',
                   linestyle='none',
                   label='case A')

    # Create model name list
    namearr = ['SLP', 'Tsfc', 'Prc', 'Prc 30S-30N', 'LW', 'SW', 'U300', 'Guess']

    # Add model name
    dia.add_model_name(namearr)

    # Add figure legend
    dia.add_legend()

    return fig


###############################################################################
def taylor_2():
    # https://www.ncl.ucar.edu/Applications/Images/taylor_2_lg.png

    # p dataset
    pstddev = [0.6, 0.5, 0.45, 0.75, 1.15]
    pcorrcoef = [0.24, 0.75, 1, 0.93, 0.37]
    # t dataset
    tstddev = [0.75, 0.64, 0.4, 0.85, 1.15]
    tcorrcoef = [0.24, 0.75, 0.47, 0.88, 0.73]

    # Create figure and TaylorDiagram instance
    fig = plt.figure(figsize=(8, 8))
    dia = TaylorDiagram(fig=fig, label='REF')

    dia.add_sample(pstddev,
                   pcorrcoef,
                   15, (-5, 10),
                   color='red',
                   marker='*',
                   markerfacecolor='none',
                   markersize=13,
                   linestyle='none')

    dia.add_sample(tstddev,
                   tcorrcoef,
                   15, (-5, 10),
                   color='blue',
                   marker='D',
                   markerfacecolor='none',
                   markersize=9,
                   linestyle='none')

    # Add RMS contours, and label them
    dia.add_contours(levels=np.arange(0, 1.1, 0.25),
                     colors='lightgrey',
                     linewidths=0.5)

    # Add y axis grid
    dia.add_ygrid(np.array([0.5, 1.5]))

    # Add x axis grid
    dia.add_xgrid(np.array([0.6, 0.9]))

    # Add figure title
    fig.suptitle("Example", size=24)

    return fig

    # p dataset
    # p_samp = [[0.60, 0.24, '1'], [0.50, 0.75, '2'], [0.45, 1.00, '3'],
    #           [0.75, 0.93, '4'], [1.15, 0.37, '5']]
    # # t dataset
    # t_samp = [[0.75, 0.24, '1'], [0.64, 0.75, '2'], [0.40, 0.47, '3'],
    #           [0.85, 0.88, '4'], [1.15, 0.73, '5']]

    # Add models to Taylor diagram
    # for i, (stddev, corrcoef, name) in enumerate(p_samp):
    # dia.add_sample(stddev,
    #                corrcoef,
    #                marker='$\genfrac{}{}{0}{}{%d}{+}$' % (i + 1),
    #                ms=25,
    #                mfc='red',
    #                mec='none',
    #                label=name)

    # Add second model data to Taylor diagram
    # for m, (stddev, corrcoef, name) in enumerate(t_samp):
    #     dia.add_sample(stddev,
    #                    corrcoef,
    #                    marker='$\genfrac{}{}{0}{}{%d}{*}$' % (m + 1),
    #                    ms=25,
    #                    mfc='blue',
    #                    mec='none',
    #                    label=name)


if __name__ == '__main__':
    taylor_2()

    plt.show()
