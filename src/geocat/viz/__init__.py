from .taylor import TaylorDiagram

from .util import (
    set_tick_direction_spine_visibility,
    add_lat_lon_gridlines,
    add_right_hand_axis,
    add_height_from_pressure_axis,
    add_lat_lon_ticklabels,
    add_major_minor_ticks,
    set_titles_and_labels,
    set_axes_limits_and_ticks,
    truncate_colormap,
    xr_add_cyclic_longitudes,
    set_map_boundary,
    findLocalExtrema,
    find_local_extrema,
    plotCLabels,
    plot_contour_labels,
    plotELabels,
    plot_extrema_labels,
    set_vector_density,
    get_skewt_vars,
)

# get version from pyproject.toml
from importlib.metadata import version as _version

try:
    __version__ = _version("geocat.viz")
except Exception:
    # Local copy or not installed with setuptools.
    # Disable minimum version checks on downstream libraries.
    __version__ = "999"
