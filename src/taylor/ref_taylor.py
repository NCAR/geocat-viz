# https://validate-climate-model-validation.readthedocs.io/en/latest/_modules/validate/taylor.html
# https://matplotlib.org/stable/gallery/axisartist/demo_floating_axes.html#sphx-glr-gallery-axisartist-demo-floating-axes-py

"""
Taylor Diagram
==============
Functionality:
    - The constructor creates the default classic Taylor diagram
    - add_xgrid adds gridlines to the X axis (standard deviation)
    - add_ygrid adds gridlines to the Y axis (correlation)
    - add_sample adds sample models to the diagram
    - add_grid adds a complete set of gridlines
    - add_contours adds contour lines to the diagram

"""

import numpy as np
import matplotlib.pyplot as plt
from taylor_statistics import taylor_stats

class TaylorDiagram(object):
    """Taylor diagram.

    Plot model standard deviation and correlation to reference (data)
    sample in a single-quadrant polar plot, with r=stddev and
    theta=arccos(correlation).
    """

    def __init__(self, refstd=1, fig=None, rect=111, label='_', stdrange=(0, 1.6)):
        """Set up Taylor diagram axes, i.e. single quadrant polar plot, using
        `mpl_toolkits.axisartist.floating_axes`.

        Parameters:

        * refstd: reference standard deviation to be compared to
        * fig: input Figure or None
        * rect: subplot definition
        * label: reference label
        * srange: stddev axis extension, in units of *refstd*
        """

        from matplotlib.projections import PolarAxes
        import mpl_toolkits.axisartist.floating_axes as fa
        import mpl_toolkits.axisartist.grid_finder as gf

        # Reference standard deviation
        self.refstd = refstd
        
        # Set polar transform
        tr = PolarAxes.PolarTransform()

        # Set correlation labels
        rlocs = np.concatenate((np.arange(10) / 10., [0.95, 0.99, 1]))
        tlocs = np.arccos(rlocs)  # Conversion to polar angles
        gl1 = gf.FixedLocator(tlocs)  # Positions
        tf1 = gf.DictFormatter(dict(list(zip(tlocs, list(map(str, rlocs))))))
        
        # Standard devation labels
        stdlocs = np.arange(0, 1.51, 0.25)
        gl2 = gf.FixedLocator(stdlocs)
        format_string = list(map(str, stdlocs))
        index = np.where(stdlocs == self.refstd)[0][0]
        format_string[index] = 'REF'
        tf2 = gf.DictFormatter(dict(list(zip(stdlocs, format_string))))
        
        # Standard deviation axis extent (in units of reference stddev)
        self.smin = stdrange[0]
        self.smax = stdrange[1]
        
        # Use customized gridhelper to define a curvilinear coordinate
        ghelper = fa.GridHelperCurveLinear(
            tr,
            extremes=(
                0,
                np.pi / 2,  # 1st quadrant
                self.smin,
                self.smax),
            grid_locator1=gl1,
            tick_formatter1=tf1,
            grid_locator2=gl2,
            tick_formatter2=tf2)

        if fig is None:
            fig = plt.figure(figsize=(8,8))

        ax = fa.FloatingSubplot(fig, rect, grid_helper=ghelper)
        fig.add_subplot(ax)

        # Adjust axes for Correlation
        ax.axis["top"].set_axis_direction("bottom")  # "Angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("right")
        #ax.axis["top"].minor_ticklabels.set_axis_direction("top")
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        # Standard deviation ("X axis")
        ax.axis["left"].set_axis_direction("bottom")
        
        # Standard deviation ("Y axis")
        ax.axis["right"].set_axis_direction("top")
        ax.axis["right"].toggle(ticklabels=True, label=True)
        ax.axis["right"].major_ticklabels.set_axis_direction("left")
        ax.axis["right"].label.set_text("Standard deviation (Normalized)")
        
        # Set fonsizes, ticksizes and padding
        ax.axis['top', 'right'].label.set_fontsize(18)
        ax.axis['top', 'right', 'left'].major_ticklabels.set_fontsize(16)
        ax.axis['top', 'right', 'left'].major_ticks.set_ticksize(10)
        ax.axis['top', 'right', 'left'].major_ticklabels.set_pad(8)
        
        # Bottom axis is not needed
        ax.axis["bottom"].set_visible(False)

        self._ax = ax  # Graphical axes
        self.ax = ax.get_aux_axes(tr)  # Polar coordinates

        # Add reference point stddev contour
        t = np.linspace(0, np.pi / 2)
        r = np.zeros_like(t) + self.refstd
        h, = self.ax.plot(t, r, 
                          linewidth=1,
                          linestyle=(0, (9, 5)),
                          color='black',
                          zorder=1)
        
        # Store the reference line
        self.referenceLine = h

        # Collect sample points for latter use (e.g. legend)
        self.samplePoints = []
        
        # Set aspect ratio
        self.ax.set_aspect(1)
        
    def add_xgrid(self, arr, *args, **kwargs):
        """Add gridlines (radii) to the X axis (standard deviation)
        specified by array *arr*

        *args* and *kwargs* are directly propagated to the
        `matplotlib.axes.Axes.vlines` command.
        """
        for value in arr:                
            self.ax.vlines([np.arccos(value)], 
                           ymin=self.smin, ymax=self.smax,
                           *args, **kwargs)
        
    def add_ygrid(self, arr, *args, **kwargs):
        """Add gridlines (radii) to the Y axis (standard deviation)
        specified by array *arr*

        *args* and *kwargs* are directly propagated to the
        `matplotlib.axes.Axes.plot` command.
        """
        
        t = np.linspace(0, np.pi / 2)
        for value in arr:
            r = np.zeros_like(t) + value
            h, = self.ax.plot(t, r,
                              *args, **kwargs,
                              zorder=1)
            
    def add_sample(self, stddev, corrcoef, *args, **kwargs):
        """Add sample (*stddev*,*corrcoeff*) to the Taylor diagram.

        *args* and *kwargs* are directly propagated to the
        `matplotlib.axes.Axes.plot` command.
        """
        l, = self.ax.plot(np.arccos(corrcoef), # theta
                          stddev, # radius
                          *args,
                          **kwargs)
        self.samplePoints.append(l)

        return l

    def add_grid(self, *args, **kwargs):
        """Add a grid.
        
        """     
        self._ax.grid(*args, **kwargs)

    def add_contours(self, levels=5, **kwargs):
        """Add constant centered RMS difference contours, defined by.

        *levels*.
        
        *kwargs* are directly propagated to the `matplotlib.axes.Axes.contour` command.
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


###############################################################################
# Testing

def taylor_3():
    # Case A
    CA_ratio= [1.230, 0.988, 1.092, 1.172, 1.064, 0.966, 1.079, 0.781]
    CA_cc = [0.958, 0.973, 0.740, 0.743, 0.922, 0.982, 0.952, 0.433]

    # Case B
    CB_ratio = [1.129, 0.996, 1.016, 1.134, 1.023, 0.962, 1.048, 0.852]
    CB_cc = [0.963, 0.975, 0.801, 0.814, 0.946, 0.984, 0.968, 0.647]

    # Create figure and TaylorDiagram instance
    fig = plt.figure(figsize=(8,8))
    stdref = 1
    dia = TaylorDiagram(stdref, fig=fig, label='REF')

    # Add models to Taylor diagram
    for i, (stddev, corrcoef, name) in zip(CA_ratio, CA_cc):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$\genfrac{}{}{0}{}{%d}{+}$' % (i + 1),
                       ms=25,
                       mfc='red',
                       mec='none',
                       label=name)

    # Add second model data to Taylor diagram
    for m, (stddev, corrcoef, name) in enumerate(t_samp):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$\genfrac{}{}{0}{}{%d}{*}$' % (m + 1),
                       ms=25,
                       mfc='blue',
                       mec='none',
                       label=name)
        
    # Add RMS contours, and label them
    dia.add_contours(levels=np.arange(0, 1.1, 0.25), colors='lightgrey', linewidths=0.5)
    
    # Add y axis grid
    dia.add_ygrid(np.array([0.5, 1.5]),
                  color="lightgray",
                  linestyle=(0, (9,5)),
                  linewidth=1)
    
    # Add x axis grid
    dia.add_xgrid(np.array([0.6, 0.9]), 
                  color='lightgray', linestyle=(0, (9,5)),
                  lw=0.5)
    
    return fig





###############################################################################
def taylor_2():
    # p dataset
    p_samp = [[0.60, 0.24, '1'], [0.50, 0.75, '2'], [0.45, 1.00, '3'],
              [0.75, 0.93, '4'], [1.15, 0.37, '5']]
    # t dataset
    t_samp = [[0.75, 0.24, '1'], [0.64, 0.75, '2'], [0.40, 0.47, '3'],
              [0.85, 0.88, '4'], [1.15, 0.73, '5']]

    # Create figure and TaylorDiagram instance
    fig = plt.figure(figsize=(8,8))
    stdref = 1
    dia = TaylorDiagram(stdref, fig=fig, label='REF')

    # Add models to Taylor diagram
    for i, (stddev, corrcoef, name) in enumerate(p_samp):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$\genfrac{}{}{0}{}{%d}{+}$' % (i + 1),
                       ms=25,
                       mfc='red',
                       mec='none',
                       label=name)

    # Add second model data to Taylor diagram
    for m, (stddev, corrcoef, name) in enumerate(t_samp):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$\genfrac{}{}{0}{}{%d}{*}$' % (m + 1),
                       ms=25,
                       mfc='blue',
                       mec='none',
                       label=name)
        
    # Add RMS contours, and label them
    dia.add_contours(levels=np.arange(0, 1.1, 0.25), colors='lightgrey', linewidths=0.5)
    
    # Add y axis grid
    dia.add_ygrid(np.array([0.5, 1.5]),
                  color="lightgray",
                  linestyle=(0, (9,5)),
                  linewidth=1)
    
    # Add x axis grid
    dia.add_xgrid(np.array([0.6, 0.9]), 
                  color='lightgray', linestyle=(0, (9,5)),
                  lw=0.5)
    
    return fig











###############################################################################
def test1():
    """Display a Taylor diagram in a separate axis."""

    # Reference dataset
    x = np.linspace(0, 4 * np.pi, 100)
    data = np.sin(x)
    refstd = data.std(ddof=1)  # Reference standard deviation

    # Generate models
    m1 = data + 0.2 * np.random.randn(len(x))  # Model 1
    m2 = 0.8 * data + .1 * np.random.randn(len(x))  # Model 2
    m3 = np.sin(x - np.pi / 10)  # Model 3

    # Compute stddev and correlation coefficient of models
    samples = np.array(
        [[m.std(ddof=1), np.corrcoef(data, m)[0, 1]] for m in (m1, m2, m3)])

    fig = plt.figure(figsize=(10, 4))
    ax1 = fig.add_subplot(1, 2, 1, xlabel='X', ylabel='Y')

    # Taylor diagram
    dia = TaylorDiagram(refstd, fig=fig, rect=122, label="Reference")

    colors = plt.matplotlib.cm.jet(np.linspace(0, 1, len(samples)))
    ax1.plot(x, data, 'ko', label='Data')
    for i, m in enumerate([m1, m2, m3]):
        ax1.plot(x, m, c=colors[i], label='Model %d' % (i + 1))
    ax1.legend(numpoints=1, prop=dict(size='small'), loc='best')

    # Add the models to Taylor diagram
    for i, (stddev, corrcoef) in enumerate(samples):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$%d$' % (i + 1),
                       ms=10,
                       ls='',
                       mfc=colors[i],
                       mec=colors[i],
                       label="Model %d" % (i + 1))

    # Add grid
    dia.add_grid()

    # Add RMS contours, and label them
    contours = dia.add_contours(colors='0.5')
    plt.clabel(contours, inline=1, fontsize=10)

    # Add a figure legend
    fig.legend(dia.samplePoints, [p.get_label() for p in dia.samplePoints],
               numpoints=1,
               prop=dict(size='small'),
               loc='upper right')

    return fig


def test2():
    """Climatology-oriented example (after iteration w/ Michael A.

    Rawlins).
    """

    # Reference std
    stdref = 48.491

    # Samples std,rho,name
    samples = [[25.939, 0.385, "Model A"], [29.593, 0.509, "Model B"],
               [33.125, 0.585, "Model C"], [29.593, 0.509, "Model D"],
               [71.215, 0.473, "Model E"], [27.062, 0.360, "Model F"],
               [38.449, 0.342, "Model G"], [35.807, 0.609, "Model H"],
               [17.831, 0.360, "Model I"]]

    fig = plt.figure()

    dia = TaylorDiagram(stdref, fig=fig, label='Reference')
    dia.samplePoints[0].set_color('r')  # Mark reference point as a red star

    # Add models to Taylor diagram
    for i, (stddev, corrcoef, name) in enumerate(samples):
        dia.add_sample(stddev,
                       corrcoef,
                       marker='$%d$' % (i + 1),
                       ms=10,
                       ls='',
                       mfc='k',
                       mec='k',
                       label=name)

    # Add RMS contours, and label them
    contours = dia.add_contours(levels=5, colors='0.5')  # 5 levels in grey
    plt.clabel(contours, inline=1, fontsize=10, fmt='%.1f')

    # Add a figure legend and title
    fig.legend(dia.samplePoints, 
               [p.get_label() for p in dia.samplePoints],
               numpoints=1,
               prop=dict(size='small'),
               loc='upper right')
    fig.suptitle("Taylor diagram", size='x-large')  # Figure title

    return fig




if __name__ == '__main__':

    test2()

    plt.show()
