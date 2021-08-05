# https://validate-climate-model-validation.readthedocs.io/en/latest/_modules/validate/taylor.html
# https://matplotlib.org/stable/gallery/axisartist/demo_floating_axes.html#sphx-glr-gallery-axisartist-demo-floating-axes-py

"""
Taylor Diagram
==============
Functionality:
    - The constructor creates the default classic Taylor diagram
    - get_axes returns the getter for the axes
    - add_sample adds sample models to the diagram
    - add_xgrid adds gridlines to the X axis (standard deviation)
    - add_ygrid adds gridlines to the Y axis (correlation)
    - add_grid adds a complete set of gridlines
    - add_contours adds contour lines to the diagram
    - add_model_name adds texts of model names to the diagram
    - add_legend adds a figure legend
    - add_title adds a main title
    - set_fontsizes_and_pad sets the fontsizes and padding of labels and ticklabels

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

    def __init__(self, refstd=1, fig=None, rect=111, label='REF', 
                 stdrange=(0, 1.6), stdlevel=np.arange(0, 1.51, 0.25)):
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
        
        ### Extract instance variables
        # Set figure
        if fig is None:
            fig = plt.figure(figsize=(8,8))
        else:
            self.fig=fig
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
        
        # Set standard devation labels
        gl2 = gf.FixedLocator(stdlevel)
        # format each label with 2 decimal places
        format_string = list(map(lambda x: "{0:0.2f}".format(x), stdlevel))
        index = np.where(stdlevel == self.refstd)[0][0]
        format_string[index] = label
        tf2 = gf.DictFormatter(dict(list(zip(stdlevel, format_string))))
        
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
        
        # Create graphical axes
        # Note: for Matplotlib > 3.4.0, this is achieved through:
        # ax = fig.add_subplot(rect, axes_class=fa.FloatingSubplot, grid_helper=ghelper)
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
        
        # Set fonsizes, ticksizes and padding
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
        h, = self.ax.plot(t, r, 
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
        
        
    ### Create instance methods
        
    def get_axes(self):
        ''' Getter for the axes'''
        
        return self.ax
        
    def add_sample(self, stddev, corrcoef,
                   fontsize=14, xytext=(-5,7), annotate_on=True, 
                   *args, **kwargs):
        """Add sample (*stddev*,*corrcoeff*) to the Taylor diagram.
        
        *fontsize* and *xytext* are arguments supplied to 
        `matplotlib.axes.Axes.annotate` command.
        
        *args* and *kwargs* are directly propagated to the
        `matplotlib.axes.Axes.plot` command.
        """
        # Add model markers
        modelset, = self.ax.plot(np.arccos(corrcoef), # theta
                          stddev, # radius
                          *args,
                          **kwargs)
        self.modelList.append(modelset)
        
        if annotate_on:    
            index = 0
            color = kwargs.get('color')
            
            # Annotate model markers
            for std, corr in zip(stddev, corrcoef):
                index = index+1
                text = str(index)
                self.ax.annotate(text, (np.arccos(corr), std),
                                 fontsize=fontsize,
                                 color=color,
                                 textcoords="offset pixels",
                                 xytext=xytext)
        return modelset
        
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
    
    def add_model_name(self, namearr, x_loc=0.1, y_loc=0.31, 
                       verticalalignment='top', fontsize=13,
                       **kwargs):
        """Add texts of model names
        
        The coordinate system of the Axes(transAxes) is used for more intuitive positioning
        (x_loc=0, y_loc=0) is bottom left of the axes, 
        and (x_loc=1, y_loc=1) is top right of the axes.
        
        *kwargs* are directly propagated to the `matplotlib.axes.Axes.text` command.
        """
        text = [str(i+1)+' - '+namearr[i] for i in range(len(namearr))]
        text = '\n'.join(text)
        
        self.ax.text(x_loc, y_loc, text,
                     verticalalignment=verticalalignment, fontsize=fontsize,
                     transform=self.ax.transAxes,
                     **kwargs)
        
    def add_legend(self, xloc=1.1, yloc=0.95, loc="upper right",
                   fontsize=14, **kwargs):
        """Add a figure legend

        *kwargs* are directly propagated to the `matplotlib.pyplot.legend` command.
        """
        if kwargs.get('handles') == None:
            handles = self.modelList
        if kwargs.get('labels') == None:
            labels = [p.get_label() for p in self.modelList]
        
        self.ax.legend(handles, labels,
                       loc=loc,
                       bbox_to_anchor=(xloc, yloc),
                       fontsize=fontsize,
                       frameon=False)
    
    def add_title(self, maintitle, fontsize=18, y_loc=None,
                  **kwargs):
        """Add a main title

        *kwargs* are directly propagated to the `matplotlib.axes.Axes.set_title` command.
        """
        
        self._ax.set_title(maintitle, fontsize=fontsize,
                           y=y_loc, **kwargs)
        
    def set_fontsizes_and_pad(self, ticklabel_fontsize=14,
                           title_fontsize=16, pad=8):
        """Reset ticklabel and title fontsizes, and ticklabel padding
        """
        self._ax.axis['top', 'right', 'left'].major_ticklabels.set_fontsize(ticklabel_fontsize)
        self._ax.axis['top', 'right'].label.set_fontsize(title_fontsize)
        self._ax.axis['top', 'right'].label.set_pad(pad)

        


###############################################################################
# NCL taylor plots

def taylor_6():
    # https://www.ncl.ucar.edu/Applications/Images/taylor_6_3_lg.png
    
    fig = plt.figure(figsize=(12, 12))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    
    # Create a list of model names
    namearr = ["SLP","Tsfc","Prc","Prc 30S-30N","LW","SW", "U300", "Guess"]
    nModel = len(namearr)
    
    # Create a list of case names
    casearr = ["Case A", "Case B", "Case C", "Case D", "Case E"]
    nCase = len(casearr)
    
    # Create lists of colors, labels, and maintitles
    colors = ["red","blue","green","magenta","orange"]
    labels = ["Case A", "Case B","Case C","Case D","Case E"]
    maintitles = ["DJF", "JJA", "MAM", "SON"]
    
    rect = 221
    
    for i in range(4):
        # Generate one plot for each season + annual
        stddev = np.random.normal(1, 0.25, (nCase, nModel))
        corrcoef = np.random.uniform(0.7, 1, (nCase, nModel))
        
        # Create taylor diagram
        da = TaylorDiagram(fig=fig, rect=rect+i, label='REF')
        
        # Add models case by case
        for j in range(stddev.shape[0]-1, -1, -1):
            da.add_sample(stddev[j], corrcoef[j], xytext=(-4,5), fontsize=10, color=colors[j],
                          label=labels[j], marker='o', markersize=5, linestyle='none')
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
    CA_ratio= [1.230, 0.988, 1.092, 1.172, 1.064, 0.966, 1.079, 0.781]
    CA_cc = [0.958, 0.973, 0.740, 0.743, 0.922, 0.982, 0.952, 0.433]

    # Case B
    CB_ratio = [1.129, 0.996, 1.016, 1.134, 1.023, 0.962, 1.048, 0.852]
    CB_cc = [0.963, 0.975, 0.801, 0.814, 0.946, 0.984, 0.968, 0.647]

    # Create figure and TaylorDiagram instance
    fig = plt.figure(figsize=(8,8))
    dia = TaylorDiagram(fig=fig, label='REF')

    # Add models to Taylor diagram  
    dia.add_sample(CB_ratio, CB_cc, color='blue', marker='o',
                   linestyle='none', label='case B')
    
    dia.add_sample(CA_ratio, CA_cc, color='red', marker='o',
                   linestyle='none', label='case A')
    
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
    fig = plt.figure(figsize=(8,8))
    dia = TaylorDiagram(fig=fig, label='REF')
      
    dia.add_sample(pstddev, pcorrcoef, 
                   15, (-5, 10),
                   color='red', marker='*',
                   markerfacecolor='none', markersize=13,
                   linestyle='none')
    
    dia.add_sample(tstddev, tcorrcoef, 
               15, (-5, 10),
               color='blue', marker='D',
               markerfacecolor='none', markersize=9,
               linestyle='none')
        
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
    #for i, (stddev, corrcoef, name) in enumerate(p_samp):
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



###############################################################################
# Testing from the original author

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
    fig.legend(dia.modelList, [p.get_label() for p in dia.modelList],
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
    dia.modelList[0].set_color('r')  # Mark reference point as a red star

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
    fig.legend(dia.modelList, 
               [p.get_label() for p in dia.modelList],
               numpoints=1,
               prop=dict(size='small'),
               loc='upper right')
    fig.suptitle("Taylor diagram", size='x-large')  # Figure title

    return fig




if __name__ == '__main__':

    taylor_6()

    plt.show()
