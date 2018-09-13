
import pandas as pd
from geojson import FeatureCollection, Feature
from collections import OrderedDict
from shapely.geometry import Polygon
from operator import itemgetter, attrgetter
import shapefile

from datapackage_utilities import building, geometry

sf = shapefile.Reader("archive/gis/exportedBoundaries_shp_levels_land_20180912_142751/Cambodia_AL2.shp")

x = pd.Series(
        OrderedDict(
            sorted([
                (rec[2], geometry._shape2poly(sh, 0.01, 1.))
                for rec, sh in zip(sf.iterRecords(), sf.iterShapes())],
            key=itemgetter(0))
        )
    )

building.write_geometries('buses.csv', x)

building.write_geometries('buses.geojson', x)
