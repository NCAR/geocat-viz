import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr


import geocat.viz.util as gv
import geocat.datafiles as gdf


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_set_tick_direction_spine_visibility():
    fig, ax = plt.subplots(figsize=(6, 6))

    gv.set_tick_direction_spine_visibility(ax,
                                        tick_direction='in',
                                        top_spine_visible=False,
                                        right_spine_visible=False)
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_add_lat_lon_gridlines():
    fig = plt.figure(figsize=(10, 10))

    ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=10))
    ax.set_extent([4.25, 15.25, 42.25, 49.25], ccrs.PlateCarree())

    gl = gv.add_lat_lon_gridlines(
        ax,
        color='black',
        labelsize=14,
        xlocator=np.arange(4, 18, 2),  # longitudes for gridlines
        ylocator=np.arange(43, 50))  # latitudes for gridlines
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_add_right_hand_axis():
    fig = plt.figure(figsize=(9, 10))
    ax1 = plt.gca()

    gv.add_right_hand_axis(ax1,
                        label="Right Hand Axis",
                        ylim=(0, 13),
                        yticks=np.array([4, 8]),
                        ticklabelsize=15,
                        axislabelsize=21)
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_add_height_from_pressure_axis():
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes()
    plt.yscale('log')
    ax.invert_yaxis()

    gv.add_height_from_pressure_axis(ax, heights=[4, 8])
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_add_lat_lon_ticklabels():
    fig = plt.figure(figsize=(12, 6))

    projection = ccrs.PlateCarree()
    ax = plt.axes(projection=projection)
    ax.add_feature(cfeature.LAND, color='silver')

    gv.add_lat_lon_ticklabels(ax)
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_add_major_minor_ticks():
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes()

    gv.add_major_minor_ticks(ax,
                            x_minor_per_major=4,
                            y_minor_per_major=5,
                            labelsize="small")
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_set_titles_and_labels():
    fig = fig, ax = plt.subplots()

    gv.set_titles_and_labels(ax,
                            maintitle="Title",
                            maintitlefontsize=24,
                            subtitle="Subtitle",
                            xlabel="x",
                            ylabel="y",
                            labelfontsize=16)
    return fig


@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_set_axes_limits_and_ticks():
    fig = fig, ax = plt.subplots()

    gv.set_axes_limits_and_ticks(ax,
                                xlim=(0, 900),
                                ylim=(100, 1000),
                                xticks=range(0, 901, 100),
                                yticks=range(100, 1001, 100))
    return fig


def test_truncate_colormap():
    cmap = mpl.colormaps['terrain']
    truncated_cmap = gv.truncate_colormap(cmap, 0.1, 0.9)

    assert isinstance(truncated_cmap, mpl.colors.LinearSegmentedColormap)
    assert truncated_cmap(0.0) == cmap(0.1)
    assert truncated_cmap(1.0) == cmap(0.9)


# # Need to investigate if there is simpler data out there and what assert should be equal to
#def test_xr_add_cyclic_longitudes():
#    ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)
#    U = ds.U
#
#    U = gv.xr_add_cyclic_longitudes(U, 'lon')
#    assert U.lon == 


# # Need to determine what assert should be equal to
#@pytest.mark.mpl_image_compare(tolerance=0.02,
#                               remove_text=True,
#                               style='default')
#def test_set_map_boundary():

# def test_find_local_extrema():
#    data = [[1, 4, 5, 6, 8.2],
#        [9, 8.4, 10, 10.6, 9.7],
#        [4.4, 5, 0, 6.6, 1.4],
#        [4.6, 5.2, 1.5, 7.6, 2.4]]
   
#    lmin = gv.find_local_extrema(data, eType='Low')[0]
#   lmax = gv.find_local_extrema(data, eType='High')[0]

#    assert


# # Need to make up simpler dummy data, or use data built into Xarray
# @pytest.mark.mpl_image_compare(tolerance=0.02,
#                                remove_text=True,
#                                style='default')
# def test_plot_contour_labels():
#     fig = plt.figure(figsize=(8, 8))

#     proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
#     ax = plt.axes(projection=proj)
#     ax.set_global()

#     p = wrap_pressure.plot.contour(ax=ax,
#                                 transform=ccrs.PlateCarree(),
#                                 linewidths=0.5,
#                                 cmap='black',
#                                 add_labels=False)

#     contour_label_locations = [(176.4, 34.63), (-150.46, 42.44), (-142.16, 28.5),
#                             (-92.49, 25.64), (-156.05, 84.47), (-17.83, 82.52),
#                             (-76.3, 41.99), (-48.89, 41.45), (-33.43, 37.55)]

#     gv.plot_contour_labels(ax,
#                         p,
#                         ccrs.Geodetic(),
#                         proj,
#                         clabel_locations=contour_label_locations)
#     return fig


# Need to make up extrema levels, need to take out Cartopy
@pytest.mark.mpl_image_compare(tolerance=0.02,
                               remove_text=True,
                               style='default')
def test_plot_extrema_labels():
    fig = plt.figure(figsize=(8, 8))

    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    ax = plt.axes(projection=proj)
    ax.set_global()

    lowClevels = 'a'

    # Label low and high contours
    gv.plot_extrema_labels(wrap_pressure,
                        ccrs.Geodetic(),
                        proj,
                        label_locations=lowClevels,
                        label='L',
                        show_warnings=False)
    return fig

# def test_set_vector_density():
# def test_get_skewt_vars():