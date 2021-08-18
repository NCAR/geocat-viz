import cartopy.feature as cfeature


class add_geo_features:
    """Class to add geographical features to a figure.

    Kwargs:

        show_coastline (:obj:`bool`): Whether to show coastlines in figure. Default False, unless a projection is specified.

        show_lakes (:obj:`bool`): Whether to show lakes in figure. Default False.

        show_land (:obj:`bool`): Whether to show land in figure. Default false.
    """

    def _init_(self, *args, **kwargs):
        """Add lakes, coastlines, and land, if specified.

        Kwargs:

            show_coastline (:obj:`bool`): Whether to show coastlines in figure. Default False, unless a projection is specified.

            show_lakes (:obj:`bool`): Whether to show lakes in figure. Default False.

            show_land (:obj:`bool`): Whether to show land in figure. Default false.
        """
        # Add land, coastlines, or lakes if specified
        if kwargs.get('show_land') is True:
            self.show_land()

        if kwargs.get('show_coastline') is True:
            self.show_coastline()

        if kwargs.get('show_lakes') is True:
            self.show_lakes()

    def show_land(self, scale="110m", fc='lightgrey'):
        """Add land to figure.

        Kwargs:

            fc(:obj:`str`): Facecolor of land. Default light grey.

            scale(:obj:`str`): Scale of land set. Default 110m.
        """
        # Add land to figure
        self.ax.add_feature(cfeature.LAND.with_scale(scale), facecolor=fc)

    def show_coastline(self, scale="110m", lw=0.5, ec="black"):
        """Add coastlines to figure.

        Kwargs:

            ec(:obj:`str`): Edgecolor of coastlines. Default black.

            lw(:obj:`float`): Linewidth of coastlines. Default 0.5.

            scale(:obj:`str`): Scale of coastline set. Default 110m.
        """
        # Add coastline to figure
        self.ax.add_feature(cfeature.COASTLINE.with_scale(scale),
                            linewidths=lw,
                            edgecolor=ec)

    def show_lakes(self, scale="110m", lw=0.5, ec='black', fc='None'):
        """Add lakes to figure.

        Kwargs:

            ec(:obj:`str`): Outline color of lakes. Default black.

            fc(:obj:`str`): Facecolor of lakes. Default none.

            lw(:obj:`float`): Linewidth of lake edges. Default 0.5.

            scale(:obj:`str`): Scale of lake set. Default 110m.
        """
        # Add lakes to figure
        self.ax.add_feature(cfeature.LAKES.with_scale(scale),
                            linewidth=lw,
                            edgecolor=ec,
                            facecolor=fc)
