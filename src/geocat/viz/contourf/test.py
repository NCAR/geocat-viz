import xarray as xr
import numpy as np
import cartopy.crs as ccrs
from matplotlib.ticker import ScalarFormatter
import matplotlib.pyplot as plt

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from geocat.viz import util as gvutil
from geocat.comp import eofunc_eofs, eofunc_pcs, month_to_season
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
#                       decode_times=False)
# # Extract a slice of the data
# t = ds.T.isel(time=0, z_t=0).sel(lat_t=slice(-60, 30), lon_t=slice(30, 120))
# X = t.lon_t
# Y = t.lat_t

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


# # Recreated Geo-CAT Examples Plot: NCL_conLab_4.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc"), decode_times=False)
# U = ds.isel(time=1, drop=True).U

# # Reduce the dataset to something just bigger than the area we want to plot.
# # This will improve how the contour lines are labeled
# U = U.where(U.lon >= 0)
# U = U.where(U.lon <= 71)
# U = U.where(U.lat >= -33)
# U = U.where(U.lat <= 33)

# X = U.lon
# Y = U.lat

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
#                                   (62, -15), (65, -2)],
#                 manualcontourlabels = True,
#                 contourbackground=True
#                 )

# cplot.show_lakes(scale="110m")
# cplot.show()

# # Recreated Geo-CAT Examples Plot: NCL_conLab_4.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
#                       decode_times=False)
# # Extract slice of the data
# temp = ds.TS.isel(time=43).drop_vars(names=['time'])
# # Convert from Celsius to Kelvin
# temp.data = temp.data - 273.15

# # Fix the artifact of not-shown-data around 0 and 360-degree longitudes
# temp = gvutil.xr_add_cyclic_longitudes(temp, "lon")

# X = temp.lon
# Y = temp.lat
# projection = ccrs.PlateCarree()
# levels = np.arange(-5, 35, 5)

# dplot = Contour(temp,
#                 X = X,
#                 Y = Y,
#                 h = 6,
#                 w = 12,
#                 clevels = levels,
#                 xlim=(-180,180),
#                 ylim=(-70,70),
#                 lefttitlefontsize=14,
#                 righttitlefontsize=14,
#                 xticks=np.linspace(-180, 180, 13),
#                 yticks=np.linspace(-60, 60, 5),
#                 ticklabelfontsize = 12,
#                 add_colorbar = False,
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

# dplot.show_land(fc="silver")

# dplot.ax.text(1,
#             -0.15,
#             "CONTOUR FROM -5 TO 30 BY 5",
#             horizontalalignment='right',
#             transform=dplot.ax.transAxes,
#             bbox=dict(boxstyle='square, pad=0.25',
#                       facecolor='white',
#                       edgecolor='black'))

# # Recreated Geo-CAT Examples Plot: NCL_conLev_3.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/Tstorm.cdf"))

# # Extract temperature data at the first timestep
# T = ds.t.isel(timestep=0, drop=True)
# X = T.lon
# Y = T.lat
# projection = ccrs.PlateCarree()
# levels = np.linspace(244, 308, 17)
# newcmp = 'plasma'

# eplot = Contour(T,
#                 X = X,
#                 Y = Y,
#                 h = 8,
#                 w = 8,
#                 clevels = levels,
#                 xlim=(-140, -50),
#                 ylim=(20, 60),
#                 xticks=[-135, -90],
#                 yticks=np.arange(20, 70, 10),
#                 ticklabelfontsize = 10,
#                 projection=projection,
#                 cmap = newcmp,
#                 set_coastlines = False,
#                 cbticks = np.arange(248, 308, 4),
#                 cborientation = "vertical",
#                 cbpad = 0.005,
#                 cbticklabelsize = 11,
#                 cbshrink = 1,
#                 maintitle = "Explanation of Python contour levels",
#                 xlabel="",
#                 ylabel=""
#                 )

# # Create labels by colorbar
# size = 8
# num_lev = 16
# cbticks = np.arange(248, 308, 4)
# y = 1 / num_lev / 2  # Offset from x axis in axes coordinates
# eplot.ax.text(0.949,
#         y,
#         'T < 248',
#         fontsize=size,
#         horizontalalignment='center',
#         verticalalignment='center',
#         transform=eplot.ax.transAxes,
#         bbox=dict(boxstyle='square, pad=0.25',
#                   facecolor='papayawhip',
#                   edgecolor='papayawhip'))
# text = '{} <= T < {}'
# for i in range(0, 14):
#     y = y + 1 / num_lev  # Vertical spacing between the labels
#     eplot.ax.text(0.904,
#             y,
#             text.format(cbticks[i], cbticks[i + 1]),
#             fontsize=size,
#             horizontalalignment='center',
#             verticalalignment='center',
#             transform=eplot.ax.transAxes,
#             bbox=dict(boxstyle='square, pad=0.25',
#                       facecolor='papayawhip',
#                       edgecolor='papayawhip'))

# y = y + 1 / num_lev  # Increment height once more for top label
# eplot.ax.text(0.94,
#         y,
#         'T >= 304',
#         fontsize=size,
#         horizontalalignment='center',
#         verticalalignment='center',
#         transform=eplot.ax.transAxes,
#         bbox=dict(boxstyle='square, pad=0.25',
#                   facecolor='papayawhip',
#                   edgecolor='papayawhip'))

# eplot.show()

# # Recreated Geo-CAT Examples Plot: NCL_conLev_4.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/b003_TS_200-299.nc"),
#                       decode_times=False)
# x = ds.TS

# # Apply mean reduction from coordinates as performed in NCL's dim_rmvmean_n_Wrap(x,0)
# # Apply this only to x.isel(time=0) because NCL plot plots only for time=0
# newx = x.mean('time')
# newx = x.isel(time=0) - newx

# # Fix the artifact of not-shown-data around 0 and 360-degree longitudes
# newx = gvutil.xr_add_cyclic_longitudes(newx, "lon")

# X = newx.lon
# Y = newx.lat
# projection = ccrs.PlateCarree()
# levels = [-12, -10, -8, -6, -4, -2, -1, 1, 2, 4, 6, 8, 10, 12]
# newcmp = gvcmaps.BlRe
# newcmp.colors[len(newcmp.colors) //
#               2] = [1, 1, 1]  # Set middle value to white to match NCL

# fplot = Contour(newx,
#                 X = X,
#                 Y = Y,
#                 h = 7.2,
#                 w = 12,
#                 clevels = levels,
#                 xlim=(-180, 180),
#                 ylim=(-90, 90),
#                 xticks=np.linspace(-180, 180, 13),
#                 yticks=np.linspace(-90, 90, 7),
#                 ticklabelfontsize = 10,
#                 projection=projection,
#                 cmap = newcmp,
#                 cbticks = levels,
#                 # cbpad = 0.005,
#                 cbticklabelsize = 11,
#                 cbshrink = 0.5,
#                 cbextend = "both",
#                 lefttitle = "Anomalies: Surface Temperature",
#                 righttitle = "K",
#                 xlabel="",
#                 ylabel=""
#                 )

# fplot.show()

# # Recreated Geo-CAT Examples Plot: NCL_conOncon_1.py

# # Open a netCDF data file using xarray default engine and load the data into xarrays
# ds = xr.open_dataset(gdf.get("netcdf_files/mxclim.nc"))
# # Extract variables
# U = ds.U[0, :, :]
# UY = U.lev
# UX = U.lat

# V = ds.V[0, :, :]
# VY = V.lev
# VX = V.lat

# levels = 16
# xlim = (-90, 90)
# ylim = (1000,10)
# xticks = np.linspace(-60, 60, 5)

# gplot = Contour(U,
#                 h = 12,
#                 w = 12,
#                 clevels = levels,
#                 xlim = xlim,
#                 ylim = ylim,
#                 yscale = "log",
#                 xticks=xticks,
#                 yticks=U["lev"],
#                 y_lat_lon = True,
#                 linecolor = "red",
#                 linewidth = 1,
#                 contour_fill = False,
#                 add_colorbar= False,
#                 maintitle="Ensemble Average 1987-89",
#                 maintitlefontsize=20,
#                 lefttitlefontsize=18,
#                 righttitlefontsize=18,
#                 ylabel= (str(U.lev.long_name) + " [" + str(U.lev.units) + "]"),
#                 xlabel = "",
#                 drawcontourlabels = True,
#                 )

# hplot = Contour(V,
#                 ref_fig = gplot,
#                 clevels = levels,
#                 xlim = xlim,
#                 ylim = ylim,
#                 yscale = "log",
#                 xticks=xticks,
#                 yticks=V["lev"],
#                 linecolor = "blue",
#                 linewidth = 1,
#                 contour_fill = False,
#                 add_colorbar= False,
#                 drawcontourlabels = True,
#                 ylabel= (str(U.lev.long_name) + " [" + str(U.lev.units) + "]"),
#                 xlabel = "",
#                 )
# hplot.ax.yaxis.set_major_formatter(ScalarFormatter())

# axRHS = gplot.ax.twinx()
# dummy = 10
# mn, mx =gplot. ax.get_ylim()
# axRHS.set_ylim(mn * dummy, mx * dummy)
# axRHS.set_ylim(axRHS.get_ylim()[::-1])
# axRHS.set_ylabel('Height (km)')
# axRHS.yaxis.label.set_size(20)
# axRHS.tick_params('both', length=20, width=2, which='major', labelsize=18)

# gplot.show()

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

xlim = (-70, 45)
ylim = (20,80)

pct = eofs.attrs['varianceFraction'].values[0] * 100

iplot = Contour(eofs.sel(eof=0),
                flevels = np.linspace(-0.08, 0.08, 9, endpoint=True),
                projection = ccrs.PlateCarree(),
                w = 6,
                h = 10.6,
                subplot = [3,1,1],
                xlim = xlim,
                ylim = ylim,
                xticks=[-60, -30, 0, 30],
                yticks=[40, 60, 80],
                ticklabelfontsize = 10,
                linewidth = 1.5,
                cmap = gvcmaps.BlWhRe,
                contour_lines = False,
                drawcontourlabels = True,
                cbextend = "both",
                xlabel = "",
                ylabel = "",
                lefttitle=f'EOF {0}',
                lefttitlefontsize=10,
                righttitle=f'{pct:.1f}%',
                righttitlefontsize=10,
                maintitle = "SLP: DJF: 1979-2003",
                maintitlefontsize = 14,
                )

for i in range(neof-1):
    eof_single = eofs.sel(eof=(i+1))
    pct = eofs.attrs['varianceFraction'].values[i] * 100
    
    jplot = Contour(eof_single,
            flevels = np.linspace(-0.08, 0.08, 9, endpoint=True),
            projection = ccrs.PlateCarree(),
            ref_fig = iplot,
            subplot = [3,1,i+2],
            xlim = xlim,
            ylim = ylim,
            xticks=[-60, -30, 0, 30],
            yticks=[40, 60, 80],
            ticklabelfontsize = 10,
            linewidth = 1.5,
            cmap = gvcmaps.BlWhRe,
            contour_lines = False,
            drawcontourlabels = True,
            cbextend = "both",
            xlabel = "",
            ylabel = "",
            lefttitle=f'EOF {i + 1}',
            lefttitlefontsize=10,
            righttitle=f'{pct:.1f}%',
            righttitlefontsize=10,
            )

iplot.show()