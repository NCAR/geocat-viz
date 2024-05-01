import pytest
import matplotlib as mpl

from geocat.viz.util import truncate_colormap


def test_truncate_colormap():
    cmap = mpl.colormaps['terrain']
    truncated_cmap = truncate_colormap(cmap, 0.1, 0.9)

    assert isinstance(truncated_cmap, mpl.colors.LinearSegmentedColormap)
    assert truncated_cmap(0.0) == cmap(0.1)
    assert truncated_cmap(1.0) == cmap(0.9)
