import pytest
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import pandas as pd
from packaging.version import Version
from metpy.units import units
import metpy
import metpy.calc as mpcalc
import geocat.datafiles as gdf

from geocat.viz.util import set_tick_direction_spine_visibility, add_lat_lon_gridlines, add_right_hand_axis, add_height_from_pressure_axis, add_lat_lon_ticklabels, add_major_minor_ticks, set_titles_and_labels, set_axes_limits_and_ticks, truncate_colormap, xr_add_cyclic_longitudes, set_map_boundary, find_local_extrema, plot_contour_labels, plot_extrema_labels, set_vector_density, get_skewt_vars


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_set_tick_direction_spine_visibility():
    fig, ax = plt.subplots(figsize=(6, 6))

    set_tick_direction_spine_visibility(ax,
                                        tick_direction='in',
                                        top_spine_visible=False,
                                        right_spine_visible=False)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_add_lat_lon_gridlines():
    fig = plt.figure(figsize=(10, 10))

    ax = plt.axes(projection=ccrs.NorthPolarStereo(central_longitude=10))
    ax.set_extent([4.25, 15.25, 42.25, 49.25], ccrs.PlateCarree())

    gl = add_lat_lon_gridlines(
        ax,
        color='black',
        labelsize=14,
        xlocator=np.arange(4, 18, 2),  # longitudes for gridlines
        ylocator=np.arange(43, 50))  # latitudes for gridlines
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_add_right_hand_axis():
    fig = plt.figure(figsize=(9, 10))
    ax1 = plt.gca()

    add_right_hand_axis(ax1,
                        label="Right Hand Axis",
                        ylim=(0, 13),
                        yticks=np.array([4, 8]),
                        ticklabelsize=15,
                        axislabelsize=21)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_add_height_from_pressure_axis():
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes()
    plt.yscale('log')
    ax.invert_yaxis()

    add_height_from_pressure_axis(ax, heights=[4, 8])
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_add_lat_lon_ticklabels():
    fig = plt.figure(figsize=(12, 6))

    projection = ccrs.PlateCarree()
    ax = plt.axes(projection=projection)
    ax.add_feature(cfeature.LAND, color='silver')

    add_lat_lon_ticklabels(ax)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_add_major_minor_ticks():
    fig = plt.figure(figsize=(12, 6))
    ax = plt.axes()

    add_major_minor_ticks(ax,
                          x_minor_per_major=4,
                          y_minor_per_major=5,
                          labelsize="small")
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_set_titles_and_labels():
    fig = fig, ax = plt.subplots()

    set_titles_and_labels(ax,
                          maintitle="Title",
                          maintitlefontsize=24,
                          subtitle="Subtitle",
                          xlabel="x",
                          ylabel="y",
                          labelfontsize=16)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_set_axes_limits_and_ticks():
    fig = fig, ax = plt.subplots()

    set_axes_limits_and_ticks(ax,
                              xlim=(0, 900),
                              ylim=(100, 1000),
                              xticks=range(0, 901, 100),
                              yticks=range(100, 1001, 100))
    return fig


def test_truncate_colormap():
    cmap = mpl.colormaps['terrain']
    truncated_cmap = truncate_colormap(cmap, 0.1, 0.9)

    assert isinstance(truncated_cmap, mpl.colors.LinearSegmentedColormap)
    assert truncated_cmap(0.0) == cmap(0.1)
    assert truncated_cmap(1.0) == cmap(0.9)


def test_xr_add_cyclic_longitudes_length():
    ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)
    U = ds.U

    U = xr_add_cyclic_longitudes(U, 'lon')

    cyclic_lon = [
        -180., -177.1875, -174.375, -171.5625, -168.75, -165.9375, -163.125,
        -160.3125, -157.5, -154.6875, -151.875, -149.0625, -146.25, -143.4375,
        -140.625, -137.8125, -135., -132.1875, -129.375, -126.5625, -123.75,
        -120.9375, -118.125, -115.3125, -112.5, -109.6875, -106.875, -104.0625,
        -101.25, -98.4375, -95.625, -92.8125, -90., -87.1875, -84.375, -81.5625,
        -78.75, -75.9375, -73.125, -70.3125, -67.5, -64.6875, -61.875, -59.0625,
        -56.25, -53.4375, -50.625, -47.8125, -45., -42.1875, -39.375, -36.5625,
        -33.75, -30.9375, -28.125, -25.3125, -22.5, -19.6875, -16.875, -14.0625,
        -11.25, -8.4375, -5.625, -2.8125, 0., 2.8125, 5.625, 8.4375, 11.25,
        14.0625, 16.875, 19.6875, 22.5, 25.3125, 28.125, 30.9375, 33.75,
        36.5625, 39.375, 42.1875, 45., 47.8125, 50.625, 53.4375, 56.25, 59.0625,
        61.875, 64.6875, 67.5, 70.3125, 73.125, 75.9375, 78.75, 81.5625, 84.375,
        87.1875, 90., 92.8125, 95.625, 98.4375, 101.25, 104.0625, 106.875,
        109.6875, 112.5, 115.3125, 118.125, 120.9375, 123.75, 126.5625, 129.375,
        132.1875, 135., 137.8125, 140.625, 143.4375, 146.25, 149.0625, 151.875,
        154.6875, 157.5, 160.3125, 163.125, 165.9375, 168.75, 171.5625, 174.375,
        177.1875, 180.
    ]

    assert len(U.lon) == len(cyclic_lon)


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_xr_add_cyclic_longitudes():
    ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"),
                         decode_times=False)
    pressure = ds.slp[24, :, :].astype('float64') * 0.01
    wrap_pressure = xr_add_cyclic_longitudes(pressure, "lon")

    fig = plt.figure(figsize=(8, 8))

    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    ax = plt.axes(projection=proj)
    ax.set_global()

    p = wrap_pressure.plot.contour(ax=ax,
                                   transform=ccrs.PlateCarree(),
                                   linewidths=0.5,
                                   add_labels=False)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_set_map_boundary():
    fig = plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.NorthPolarStereo())
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    set_map_boundary(ax, [-180, 180], [0, 40], south_pad=1)

    return fig


def test_find_local_extrema():
    data = [[1, 4, 5, 6, 8.2], [9, 8.4, 10, 10.6, 9.7], [4.4, 5, 0, 6.6, 1.4],
            [4.6, 5.2, 1.5, 7.6, 2.4]]
    data = xr.DataArray(data,
                        dims=["lat", "lon"],
                        coords=dict(lat=np.arange(4), lon=np.arange(5)))

    lmin = find_local_extrema(data, eType='Low')[0]

    assert lmin == (2, 2)


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_plot_contour_labels():
    ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"),
                         decode_times=False)
    pressure = ds.slp[24, :, :].astype('float64') * 0.01

    fig = plt.figure(figsize=(8, 8))

    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    ax = plt.axes(projection=proj)
    ax.set_global()

    p = pressure.plot.contour(ax=ax,
                              transform=ccrs.PlateCarree(),
                              linewidths=0.5,
                              add_labels=False)

    contour_label_locations = [
        (176.4, 34.63), (-150.46, 42.44), (-142.16, 28.5), (-92.49, 25.64),
        (-156.05, 84.47), (-17.83, 82.52), (-76.3, 41.99), (-48.89, 41.45),
        (-33.43, 37.55)
    ]

    plot_contour_labels(ax,
                        p,
                        ccrs.Geodetic(),
                        proj,
                        clabel_locations=contour_label_locations)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_plot_extrema_labels():
    ds = xr.open_dataset(gdf.get("netcdf_files/slp.1963.nc"),
                         decode_times=False)
    pressure = ds.slp[24, :, :].astype('float64') * 0.01

    fig = plt.figure(figsize=(8, 8))
    proj = ccrs.Orthographic(central_longitude=270, central_latitude=45)
    ax = plt.axes(projection=proj)
    ax.set_global()

    lowClevels = [(357.5, 75.0), (302.5, 60.0), (170.0, 52.5), (327.5, -60.0)]

    plot_extrema_labels(pressure,
                        ccrs.Geodetic(),
                        proj,
                        label_locations=lowClevels,
                        label='L',
                        show_warnings=False)
    return fig


@pytest.mark.mpl_image_compare(tolerance=2, remove_text=True, style='default')
def test_set_vector_density():
    file_in = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"))
    ds = file_in.isel(time=1, lon=slice(0, -1, 3), lat=slice(1, -1, 3))

    fig = plt.figure(figsize=(10, 5.25))
    ax = plt.axes(projection=ccrs.PlateCarree())

    z = set_vector_density(ds, 10)

    Q = plt.quiver(z['lon'],
                   z['lat'],
                   z['U'].data,
                   z['V'].data,
                   color='black',
                   zorder=1,
                   pivot="middle",
                   width=0.0007,
                   headwidth=10)
    return fig


def test_get_skewt_vars():
    ds = pd.read_csv(gdf.get('ascii_files/sounding.testdata'),
                     delimiter='\\s+',
                     header=None)

    p = ds[1].values * units.hPa
    tc = (ds[5].values + 2) * units.degC
    tdc = ds[9].values * units.degC

    tc0 = tc[0]
    tdc0 = tdc[0]
    pro = mpcalc.parcel_profile(p, tc0, tdc0)
    subtitle = get_skewt_vars(p, tc, tdc, pro)

    metpy_version = Version(metpy.__version__)
    if metpy_version < Version('1.7'):
        assert subtitle == 'Plcl= 927 Tlcl[C]= 24 Shox= 3 Pwat[cm]= 5 Cape[J]= 3135'
    else:
        assert subtitle == 'Plcl= 926 Tlcl[C]= 24 Shox= 3 Pwat[cm]= 5 Cape[J]= 3212'
