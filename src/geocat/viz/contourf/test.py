import xarray as xr
import numpy as np
import cartopy.crs as ccrs

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil
from contourf import *


# # Recreated Geo-CAT Examples Plot: NCL_color_1.py

# # Open a netCDF data file using xarray default engine and load the data into xarray
# ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)

# projection = ccrs.PlateCarree()
# levels = np.arange(-16, 48, 4)

# aplot = Contour(ds.U,
#                 flevels=levels,
#                 clevels=levels,
#                 xlim=(-180, 180),
#                 ylim=(-90, 90),
#                 xticks=np.linspace(-180, 180, 13),
#                 yticks=np.linspace(-90, 90, 7),
#                 projection=projection,
#                 cmap=gvcmaps.ncl_default,
#                 maintitle="Default Color",
#                 lefttitle=ds.U.long_name,
#                 righttitle=ds.U.units,
#                 xlabel = "",
#                 ylabel = "",
#                 cbdrawedges=False
#                 )

# aplot.show()

# # Recreated Geo-CAT Examples Plot: NCL_ce_3_1.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'),
#                      decode_times=False)
# # Extract a slice of the data
# t = ds.T.isel(time=0, z_t=0).sel(lat_t=slice(-60, 30), lon_t=slice(30, 120))
# X = t.lon_t.data
# Y = t.lat_t.data

# projection = ccrs.PlateCarree()
# newcmp = gvcmaps.BlAqGrYeOrRe

# bplot = Contour(t,
#                 X = X,
#                 Y = Y,
#                 h = 7,
#                 w = 7,
#                 contour_lines = False,
#                 flevels=40,
#                 xlim=(30,120),
#                 ylim=(-60,30),
#                 xticks=np.linspace(0, 75, 3),
#                 yticks=np.linspace(-90, 90, 7),
#                 projection=projection,
#                 cmap=newcmp,
#                 cborientation="vertical",
#                 cbticks = np.arange(0, 32, 2),
#                 cbticklabels = [str(i) for i in np.arange(0, 32, 2)],
#                 cbpad = 0.05,
#                 cbshrink = 1,
#                 cbdrawedges = False,
#                 cbextend="min",
#                 maintitle="30-degree major and 10-degree minor ticks",
#                 maintitlefontsize=16,
#                 lefttitle="Potential Temperature",
#                 lefttitlefontsize=14,
#                 righttitle="Celsius",
#                 righttitlefontsize=14,
#                 xlabel="",
#                 ylabel=""    
#                 )

# bplot.show_land()

# bplot.show()


# Recreated Geo-CAT Examples Plot: NCL_conLab_4.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"), decode_times=False)
# U = ds.isel(time=1, drop=True).U

# # Reduce the dataset to something just bigger than the area we want to plot.
# # This will improve how the contour lines are labeled
# U = U.where(U.lon >= 0)
# U = U.where(U.lon <= 71)
# U = U.where(U.lat >= -33)
# U = U.where(U.lat <= 33)

# X = U.lon.data
# Y = U.lat.data

# levels = np.arange(-16, 48, 4)

# projection=ccrs.PlateCarree()
# cmap = gvcmaps.gui_default

# cplot = Contour(U,
#                 X = X,
#                 Y = Y,
#                 h = 8,
#                 w = 8,
#                 flevels=levels,
#                 clevels = levels,
#                 xlim=(0,70),
#                 ylim=(-30,30),
#                 xticks=np.linspace(0, 60, 3),
#                 yticks=np.linspace(-20, 20, 3),
#                 ticklabelfontsize = 14,
#                 projection=projection,
#                 cmap=cmap,
#                 cbticks = np.arange(-12, 44, 4),
#                 cbpad = 0.075,
#                 cbshrink = 0.8,
#                 cbticklabelsize = 14,
#                 xlabel="",
#                 ylabel="",
#                 drawcontourlabels = True,
#                 contourlabels = [(25, 28), (30, -17), (40, -21), (40, -5), (42, -13), (10, 50),
#                                  (62, -15), (65, -2)],
#                 manualcontourlabels=True,
#                 contourbackground=True
#                 )

# cplot.show_lakes(scale="110m")
# cplot.show()

# Recreated Geo-CAT Examples Plot: NCL_conLab_4.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
#                      decode_times=False)
# # Extract slice of the data
# temp = ds.TS.isel(time=43).drop_vars(names=['time'])
# # Convert from Celsius to Kelvin
# temp.data = temp.data - 273.15

# # Fix the artifact of not-shown-data around 0 and 360-degree longitudes
# temp = gvutil.xr_add_cyclic_longitudes(temp, "lon")

# X = temp.lon.data
# Y = temp.lat.data
# projection = ccrs.PlateCarree()
# levels = np.arange(-5, 35, 5)

# dplot = Contour(temp,
#                 X = X,
#                 Y = Y,
#                 h = 6,
#                 w = 12,
#                 clevels = levels,
#                 xlim=(0,70),
#                 ylim=(-30,30),
#                 lefttitlefontsize=14,
#                 righttitlefontsize=14,
#                 xticks=np.linspace(-180, 180, 13),
#                 yticks=np.linspace(-60, 60, 5),
#                 ticklabelfontsize = 12,
#                 set_extent = [-180, 180, -70, 70],
#                 projection=projection,
#                 contour_fill=False,
#                 set_coastlines = False,
#                 cbticks = np.arange(-12, 44, 4),
#                 cbpad = 0.075,
#                 cbshrink = 0.8,
#                 cbticklabelsize = 14,
#                 xlabel="",
#                 ylabel="",
#                 drawcontourlabels = True,
#                 contourlabels = np.linspace(0, 20, 3),
#                 )

# dplot.show_land(color="silver")

# dplot.ax.text(1,
#             -0.15,
#             "CONTOUR FROM -5 TO 30 BY 5",
#             horizontalalignment='right',
#             transform=dplot.ax.transAxes,
#             bbox=dict(boxstyle='square, pad=0.25',
#                       facecolor='white',
#                       edgecolor='black'))

# Recreated Geo-CAT Examples Plot: NCL_conLev_3.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get("netcdf_files/Tstorm.cdf"))

# Extract temperature data at the first timestep
T = ds.t.isel(timestep=0, drop=True)
X = T.lon.data
Y = T.lat.data
projection = ccrs.PlateCarree()
levels = np.linspace(244, 308, 17)
newcmp = 'plasma'

eplot = Contour(T,
                X = X,
                Y = Y,
                h = 8,
                w = 8,
                clevels = levels,
                xlim=(-140, -50),
                ylim=(20, 60),
                xticks=[-135, -90],
                yticks=np.arange(20, 70, 10),
                ticklabelfontsize = 10,
                projection=projection,
                cmap = newcmp,
                set_coastlines = False,
                cbticks = np.arange(248, 308, 4),
                cborientation = "vertical",
                cbpad = 0.005,
                cbticklabelsize = 11,
                maintitle = "Explanation of Python contour levels",
                xlabel="",
                ylabel=""
                )

# Create labels by colorbar
size = 8
num_lev = 16
cbticks = np.arange(248, 308, 4)
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
            text.format(cbticks[i], cbticks[i + 1]),
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