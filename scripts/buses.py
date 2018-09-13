
import pandas as pd
from geojson import FeatureCollection, Feature
from collections import OrderedDict
from shapely.geometry import Polygon
from operator import itemgetter, attrgetter
import shapefile

from datapackage_utilities import building, geometry

config = building.get_config()

sf = shapefile.Reader("archive/gis/exportedBoundaries_shp_levels_land_20180912_142751/Cambodia_AL2.shp")

geoms = pd.Series(
        OrderedDict(
            sorted([
                (rec[2], geometry._shape2poly(sh, 0.01, 1.))
                for rec, sh in zip(sf.iterRecords(), sf.iterShapes())],
            key=itemgetter(0))
        )
    )


buses = pd.Series(name='geometry')
buses.index.name= 'name'

config['buses'].sort()
mapper = dict(zip(config['buses'], geoms.index))
# add hubs and their geometry
for r in config['buses']:
    buses[r] = geoms[mapper[r]]

elements = pd.DataFrame(buses).drop('geometry', axis=1)
elements.loc[:, 'type'] = 'bus'
elements.loc[:, 'geometry'] = geoms.index

building.write_elements('buses.csv', elements)

building.write_geometries('buses.geojson', geoms)
