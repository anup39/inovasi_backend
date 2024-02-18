# myapp/management/commands/load_shapefile.py
import geopandas as gp
from shapely.geometry import Polygon, MultiPolygon, shape, Point
from django.core.management.base import BaseCommand
from sqlalchemy import create_engine

engine = create_engine(
    'postgresql://postgres:postgres@postgres/inovasi')


def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo


class Command(BaseCommand):
    help = 'Load shapefile into PostGIS'

    def handle(self, *args, **options):
        geodf_2d = gp.GeoDataFrame.from_file(
            'Shapefiles/Sample Agriplot ADM.shp')  # plug_in your shapefile
        # new geodf with 2D geometry series
        geodf_2d.geometry = convert_3D_2D(geodf_2d.geometry)
        geodf_2d.to_postgis('test_agriplot', engine,
                            if_exists='replace', index=True, index_label='id')
