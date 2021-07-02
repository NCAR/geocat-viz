import xarray as xr
import numpy as np
import cartopy.crs as ccrs

import geocat.datafiles as gdf
from geocat.viz import cmaps as gvcmaps
from contourf import *


# Recreated Geo-CAT Examples Plot: NCL_color_1.py

# Open a netCDF data file using xarray default engine and load the data into xarray
ds = xr.open_dataset(gdf.get("netcdf_files/uv300.nc")).isel(time=1)

projection = ccrs.PlateCarree()
levels = np.arange(-16, 48, 4)

# cplot = Contour(ds.U,
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

# cplot.show()

# Recreated Geo-CAT Examples Plot: NCL_ce_3_1.py

# Open a netCDF data file using xarray default engine and load the data into xarrays
ds = xr.open_dataset(gdf.get('netcdf_files/h_avg_Y0191_D000.00.nc'),
                     decode_times=False)
# Extract a slice of the data
t = ds.T.isel(time=0, z_t=0).sel(lat_t=slice(-60, 30), lon_t=slice(30, 120))

projection = ccrs.PlateCarree()
newcmp = gvcmaps.BlAqGrYeOrRe

cplot = Contour(t,
                h = 7,
                w = 7,
                contour_lines = False,
                flevels=40,
                xlim=(30,120),
                ylim=(-60,30),
                xticks=np.linspace(-180, 180, 13),
                yticks=np.linspace(-90, 90, 7),
                projection=projection,
                cmap=newcmp,
                cborientation="vertical",
                cbticks = np.arange(0, 32, 2),
                cbticklabels = [str(i) for i in np.arange(0, 32, 2)],
                cbpad = 0.05,
                cbshrink = 1,
                cbdrawedges = False,
                cbextend="min",
                maintitle="30-degree major and 10-degree minor ticks",
                maintitlefontsize=16,
                lefttitle="Potential Temperature",
                lefttitlefontsize=14,
                righttitle="Celsius",
                righttitlefontsize=14,
                xlabel="",
                ylabel=""
                
                )
cplot.show_land()

cplot.show()

        
