import cartopy.feature as cfeature

class add_geo_features:
    
    def _init_(self, *args, **kwargs):
        
        # Add land, coastlines, or lakes if specified
        if kwargs.get('show_land') is True:
            self.show_land()

        if kwargs.get('show_coastline') is True:
            self.show_coastline()

        if kwargs.get('show_lakes') is True:
            self.show_lakes()
            
    def show_land(self, scale = "110m", color='lightgrey'):
        # Add land to figure
        self.ax.add_feature(cfeature.LAND.with_scale(scale), facecolor=color)

    def show_coastline(self, scale = "110m", lw=0.5, edgecolor="black"):
        # Add coastline to figure
        self.ax.add_feature(cfeature.COASTLINE.with_scale(scale), 
                            linewidths=lw,
                            edgecolor=edgecolor)

    def show_lakes(self, scale = "110m", lw=0.5, ec='black', fc='None'):
        # Add lakes to figure
        self.ax.add_feature(cfeature.LAKES.with_scale(scale),
                            linewidth=lw,
                            edgecolor=ec,
                            facecolor=fc)
        