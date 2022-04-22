import xarray as xr

import geocat.datafiles as gdf
from geocat.viz import util as gvutil
from geocat.comp import eofunc_eofs, eofunc_pcs, month_to_season
from contourf import *

#Recreated Geo-CAT Examples Plot: NCL_color_1.py

# Open a netCDF data file using xarray default engine and load the data into xarray
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)

aplot = Contour(ds.U, main_title="Default Color")

aplot.show()

# Recreated Geo-CAT Examples Plot: NCL_ce_3_1.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'),
                     decode_times=False)
# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0).sel(lat_t=slice(-60, 30), lon_t=slice(30, 120))

bplot = Contour(
    t,
    contour_lines=False,
    xlim=(30, 120),
    ylim=(-60, 30),
    cb_orientation="vertical",
    cb_draw_edges=False,  #
    main_title="30-degree major and 10-degree minor ticks")

bplot.show_land()

bplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conLab_4.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"), decode_times=False)
U = ds.isel(time=1, drop=True).U

# Reduce the dataset to something just bigger than the area we want to plot.
# This will improve how the contour lines are labeled
U = U.where(U.lon >= 0)
U = U.where(U.lon <= 71)
U = U.where(U.lat >= -33)
U = U.where(U.lat <= 33)

cplot = Contour(U, xlim=(0, 70), ylim=(-30, 30), contour_label_background=True)

cplot.show_lakes(scale="110m")
cplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conLev_1.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
                     decode_times=False)
# Extract slice of the data
temp = ds.TS.isel(time=43).drop_vars(names=['time'])
# Convert from Celsius to Kelvin
temp.data = temp.data - 273.15

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
temp = gvutil.xr_add_cyclic_longitudes(temp, "lon")

dplot = Contour(temp,
                ylim=(-70, 70),
                contour_fill=False,
                contour_labels=np.linspace(8, 38, 4))

dplot.show_land(fc="silver")

dplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conOncon_1.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/mxclim.nc"))
# Extract variables
U = ds.U[0, :, :]

V = ds.V[0, :, :]

gplot = Contour(
    U,
    type="press_height",
    line_color="red",
    line_width=1,
    contour_fill=False,
    main_title="Ensemble Average 1987-89",
    draw_contour_labels=True,
    contour_label_box=True,  #
)

hplot = Contour(
    V,
    overlay=gplot,
    line_color="blue",
    line_width=1,
)

gplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conLev_3.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/Tstorm.cdf"))

# Extract temperature data at the first timestep
T = ds.t.isel(timestep=0, drop=True)
levels = np.linspace(244, 308, 17)

eplot = Contour(
    T,
    levels=levels,
    xlim=(-140, -50),
    ylim=(20, 60),
    cb_orientation="vertical",
    cb_pad=0.005,
    main_title="Explanation of Python contour levels",
)

# Create labels by colorbar
size = 8
num_lev = 16
cb_ticks = np.arange(248, 308, 4)
y = 1 / num_lev / 2  # Offset from x axis in axes coordinates
eplot.ax.text(0.949,
              y,
              'T < 248',
              fontsize=size,
              horizontalalignment='center',
              verticalalignment='center',
              transform=eplot.ax.transAxes,
              bbox=dict(boxstyle='square, pad=0.25',
                        facecolor='papayawhip',
                        edgecolor='papayawhip'))
text = '{} <= T < {}'
for i in range(0, 14):
    y = y + 1 / num_lev  # Vertical spacing between the labels
    eplot.ax.text(0.904,
                  y,
                  text.format(cb_ticks[i], cb_ticks[i + 1]),
                  fontsize=size,
                  horizontalalignment='center',
                  verticalalignment='center',
                  transform=eplot.ax.transAxes,
                  bbox=dict(boxstyle='square, pad=0.25',
                            facecolor='papayawhip',
                            edgecolor='papayawhip'))

y = y + 1 / num_lev  # Increment height once more for top label
eplot.ax.text(0.94,
              y,
              'T >= 304',
              fontsize=size,
              horizontalalignment='center',
              verticalalignment='center',
              transform=eplot.ax.transAxes,
              bbox=dict(boxstyle='square, pad=0.25',
                        facecolor='papayawhip',
                        edgecolor='papayawhip'))

eplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conLev_4.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
                     decode_times=False)
x = ds.TS

# Apply mean reduction from coordinates as performed in NCL's dim_rmvmean_n_Wrap(x,0)
# Apply this only to x.isel(time=0) because NCL plot plots only for time=0
newx = x.mean('time')
newx = x.isel(time=0) - newx

# Fix the artifact of not-shown-data around 0 and 360-degree longitudes
newx = gvutil.xr_add_cyclic_longitudes(newx, "lon")

fplot = Contour(
    newx,
    left_title="Anomalies: Surface Temperature",
)

fplot.show()

# Recreated Geo-CAT Examples Plot:NCL_eof_1_1.py

# In order to specify region of the globe, time span, etc.
latS = 25.
latN = 80.
lonL = -70.
lonR = 40.

yearStart = 1979
yearEnd = 2003

neof = 3  # number of EOFs

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/slp.mon.mean.nc'))

# To facilitate data subsetting

ds["lon"] = ((ds["lon"] + 180) % 360) - 180

# Sort longitudes, so that subset operations end up being simpler.
ds = ds.sortby("lon")

# To facilitate data subsetting

ds = ds.sortby("lat", ascending=True)

startDate = f'{yearStart}-01-01'
endDate = f'{yearEnd}-12-31'

ds = ds.sel(time=slice(startDate, endDate))

# Choose the winter season (December-January-February)
season = "DJF"
SLP = month_to_season(ds, season)

clat = SLP['lat'].astype(np.float64)
clat = np.sqrt(np.cos(np.deg2rad(clat)))

# Xarray will apply latitude-based weights to all longitudes and timesteps automatically.
# This is called "broadcasting".

wSLP = SLP
wSLP['slp'] = SLP['slp'] * clat

# For now, metadata for slp must be copied over explicitly; it is not preserved by binary operators like multiplication.
wSLP['slp'].attrs = ds['slp'].attrs
wSLP['slp'].attrs['long_name'] = 'Wgt: ' + wSLP['slp'].attrs['long_name']

xw = wSLP.sel(lat=slice(latS, latN), lon=slice(lonL, lonR))

# Transpose data to have 'time' in the first dimension
# as `eofunc` functions expects so for xarray inputs for now
xw_slp = xw["slp"].transpose('time', 'lat', 'lon')

eofs = eofunc_eofs(xw_slp, neofs=neof, meta=True)

pcs = eofunc_pcs(xw_slp, npcs=neof, meta=True)

# Change the sign of the second EOF and its time-series for
# consistent visualization purposes. See this explanation:
# https://www.ncl.ucar.edu/Support/talk_archives/2009/2015.html
# about that EOF signs are arbitrary and do not change the physical
# interpretation.
eofs[1, :, :] = eofs[1, :, :] * (-1)
pcs[1, :] = pcs[1, :] * (-1)

# Sum spatial weights over the area used.
nLon = xw.sizes["lon"]

# Bump the upper value of the slice, so that latitude values equal to latN are included.
clat_subset = clat.sel(lat=slice(latS, latN + 0.01))
weightTotal = clat_subset.sum() * nLon
pcs = pcs / weightTotal

pct = eofs.attrs['varianceFraction'].values[0] * 100

iplot = Contour(
    eofs.sel(eof=0),
    subplot=[3, 1, 1],
    xlim=(-70, 45),
    ylim=(20, 80),
    contour_lines=False,
    draw_contour_labels=True,
    left_title=f'EOF {0}',
    right_title=f'{pct:.1f}%',
    main_title="SLP: DJF: 1979-2003",
)

for i in range(neof - 1):
    eof_single = eofs.sel(eof=(i + 1))
    pct = eofs.attrs['varianceFraction'].values[i] * 100

    jplot = Contour(
        eof_single,
        overlay=iplot,
        subplot=[3, 1, i + 2],
        left_title=f'EOF {i + 1}',
        right_title=f'{pct:.1f}%',
    )

iplot.show()
