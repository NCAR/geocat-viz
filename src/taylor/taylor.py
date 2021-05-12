import numpy as np
import matplotlib.pyplot as plt

from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist import floating_axes, grid_finder


class TaylorDiagram(object):
    """Taylor diagram."""

    def __init__(self, refstd, minstd=0, maxstd=1.625, **kwargs):
        """

        Args:
            refstd : float
                reference strandard deviation

            **kwargs:
        """

        # pull out input arguments
        self.refstd = refstd
        self.minstd = minstd
        self.maxstd = maxstd

        # set up basic plot elements
        pa = PolarAxes.PolarTransform()
        self.fig = plt.figure()

        # Correlation labels
        rlocs = np.concatenate((np.arange(10) / 10., [0.95, 0.99, 1.0]))
        tlocs = np.arccos(rlocs)  # Conversion to polar angles
        gl1 = grid_finder.FixedLocator(tlocs)  # Positions
        tf1 = grid_finder.DictFormatter(
            dict(list(zip(tlocs, list(map(str, rlocs))))))

        # set up GridHelper
        gh = floating_axes.GridHelperCurveLinear(pa,
                                                 extremes=(0, np.pi / 2,
                                                           self.minstd,
                                                           self.maxstd),
                                                 grid_locator1=gl1,
                                                 tick_formatter1=tf1)

        # Set up graphical axes
        ax = floating_axes.FloatingSubplot(self.fig, 111, grid_helper=gh)

        # Put graphical axes on subplot
        self.fig.add_subplot(ax)

        # Flip all the axes around to make sense
        ax.axis["top"].set_axis_direction("bottom")  # angle axis"
        ax.axis["top"].toggle(ticklabels=True, label=True)
        ax.axis["top"].major_ticklabels.set_axis_direction("right")
        ax.axis["top"].major_ticklabels.set_visible(True)
        ax.axis["top"].minor_ticks.set_visible(True)
        ax.axis["top"].label.set_axis_direction("top")
        ax.axis["top"].label.set_text("Correlation")

        ax.axis["left"].set_axis_direction("bottom")  # x-axis

        ax.axis["right"].set_axis_direction("top")  # y-axis
        ax.axis["right"].toggle(ticklabels=True, label=True)
        ax.axis["right"].label.set_text("Standard Deviations (Normalized)")
        ax.axis["right"].major_ticklabels.set_axis_direction("left")

        ax.axis["bottom"].set_visible(False)  # Not used

        ax.axis[:].major_ticks.set_ticksize(8)
        ax.axis[:].minor_ticks.set_ticksize(4)

        # Save axes to TaylorDiagram object
        self._ax = ax  # graphical
        self.ax = ax.get_aux_axes(pa)  # polar

        plt.show()


t = TaylorDiagram(1)
