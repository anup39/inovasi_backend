import math
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Facility, Refinery, Mill, Agriplot, Tracetomill, Tracetoplantation
from .models import TestAgriplot
from .tasks import handleExampleTask
from .serializer import FileUploadSerializer, ShapeFileUploadSerializer, FacilitySerializer, MillSerializer, AgriplotSerializer, TracetoplantationSerializer, AgriplotGeojsonSerializer
from .serializer import TestAgriplotSerializer, TestAgriplotGeojsonSerializer
from django.contrib.gis.geos import Point
from rest_framework import generics, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import pandas as pd
import zipfile
import os
import glob
from django.core.exceptions import ValidationError
import geopandas as gpd
from django.contrib.gis.geos import (
    GEOSGeometry)
from .filters import TracetoplantationFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
import numpy as np
from django.db.models import F, Count, Sum, FloatField
from django.db.models.functions import Cast
from django.contrib.gis.measure import D, Distance
from django.contrib.gis.geos import GEOSGeometry, LineString, Point

# Create your views here.


def create_shapefiles_folder():
    folder_path = 'Shapefiles'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def get_zip_file_name(zip_file_path):
    file_name, file_extension = os.path.splitext(zip_file_path)

    if file_extension.lower() == '.zip':
        return file_name
    else:
        return None


def checkUploadFileValidationGlobal(shape_file):

    if not shape_file.name.endswith('.zip'):
        raise ValidationError('The file must be a ZIP archive.')
    if shape_file.name.endswith('.zip'):
        # Open the zip file
        with zipfile.ZipFile(shape_file, 'r') as zip_file:

            # Check if a file with a .shp extension exists in the zip file
            file_list = zip_file.namelist()
            shp_file = None
            for file_name in file_list:
                if file_name.endswith('.shp'):
                    shp_file = file_name
                    break

            # If a .shp file exists, open it
            if shp_file:
                with zip_file.open(shp_file) as file:
                    pass
            else:
                raise ValueError(
                    f"No .shp file found in {shape_file}")


def handleShapefileAgriplot(shapefile_obj, model, actual):
    shape_file = shapefile_obj
    print(shape_file, 'shapefile')
    actual_supplier = True
    if actual == "Yes":
        actual_supplier = True
    else:
        actual_supplier = False
    create_shapefiles_folder()
    zip_file_name = get_zip_file_name(str(shape_file))
    print(zip_file_name, "zip file name")
    with zipfile.ZipFile(shape_file, "r") as zip_ref:
        zip_ref.extractall('Shapefiles')
    # shape = glob.glob(r'{}/**/*.shp'.format(f'Shapefiles/{zip_file_name}'),
    #                   recursive=True)[0]
    # print(shape, 'shape')
    gdf = gpd.read_file('Shapefiles/Finaltest_15012024.shp')
    gdf.to_crs(epsg=4326)
    print(gdf.head(), 'gdf')
    gdf.fillna(0, inplace=True)
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))

        # Convert the geometry to EPSG 4326 (WGS84)

        if geom.geom_type == "MultiPolygon":
            for polygon in geom:
                # new_geom = Polygon(polygon.exterior)
                model.objects.create(
                    # id_mill=row['ID_Mill'],
                    # mill_name=row['Mill_Name'],
                    ownership_plot=row['Ownership'],
                    millideq=row['mill_eq_id'],
                    subsidiary=row['Subsidiary'],
                    estate=row['Estate'],
                    id_estate=row['ID_Estate'],
                    agriplot_id=row['AgriplotID'],
                    type_of_supplier=row['TypeOfSupp'],
                    village=row['Village'],
                    sub_district=row['SubDistric'],
                    district=row['District'],
                    province=row['Province'],
                    country=row['Country'],
                    planted_area=row['Planted_Ar'],
                    # year_update=row['YearUpdate'],
                    risk_assess=row['RiskAssess'],
                    ghg_luc=row['GHG_LUC'],
                    status_of_plot=row['Legal_Comp'],
                    def_free=row['Def_Free'],
                    compliance=row['Compliance'],
                    geom=polygon,
                    actual_supplier=actual_supplier
                )
        else:
            model.objects.create(
                # id_mill=row['ID_Mill'],
                # mill_name=row['Mill_Name'],
                ownership_plot=row['Ownership'],
                millideq=row['mill_eq_id'],
                subsidiary=row['Subsidiary'],
                estate=row['Estate'],
                id_estate=row['ID_Estate'],
                agriplot_id=row['AgriplotID'],
                type_of_supplier=row['TypeOfSupp'],
                village=row['Village'],
                sub_district=row['SubDistric'],
                district=row['District'],
                province=row['Province'],
                country=row['Country'],
                planted_area=row['Planted_Ar'],
                # year_update=row['YearUpdate'],
                risk_assess=row['RiskAssess'],
                ghg_luc=row['GHG_LUC'],
                status_of_plot=row['Legal_Comp'],
                def_free=row['Def_Free'],
                compliance=row['Compliance'],
                geom=geom,
                actual_supplier=actual_supplier

            )
            pass

    return bound_dict

    # return True


def handleShapefilePlantedOutsideLandRegistration(shapefile_obj, model):
    shape_file = shapefile_obj
    print(shape_file, 'shapefile')
    with zipfile.ZipFile(shape_file, "r") as zip_ref:
        zip_ref.extractall(str(shape_file))
    shape = glob.glob(r'{}/**/*.shp'.format(str(shape_file)),
                      recursive=True)[0]
    print(shape, 'shape')
    gdf = gpd.read_file(shape)
    print(gdf.head(), 'gdf')
    gdf.fillna(0, inplace=True)
    print(gdf.columns, "columns")
    total_bounds = gdf.total_bounds
    bound_dict = {"total_bounds": total_bounds.tolist()}
    for index, row in gdf.iterrows():
        dropped_geometry = row.drop(["geometry"])
        dropped_geometry_dict = dropped_geometry.to_dict()
        geom = GEOSGeometry(str(row["geometry"]))
        if geom.geom_type == "MultiPolygon":
            for polygon in geom:
                # new_geom = Polygon(polygon.exterior)
                model.objects.create(
                    mukim=row['Mukim'],
                    id_mukim=row['ID_Mukim'],
                    daerah=row['Daerah'],
                    id_daerah=row['ID_Daerah'],
                    negeri=row['Negeri'],
                    id_negeri=row['ID_Negeri'],
                    country=row['Country'],
                    note=row['Note'],
                    status_plot=row['Status'],
                    geom=polygon,

                )
        else:
            model.objects.create(
                mukim=row['Mukim'],
                id_mukim=row['ID_Mukim'],
                daerah=row['Daerah'],
                id_daerah=row['ID_Daerah'],
                negeri=row['Negeri'],
                id_negeri=row['ID_Negeri'],
                country=row['Country'],
                note=row['Note'],
                status_plot=row['Status'],
                geom=geom,

            )
            pass

    return bound_dict


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })


class ExampleViewSet(viewsets.ViewSet):
    def list(self, request):
        # Your logic for processing the API request
        data = {
            'message': 'Hello, API!',
            'status': 'success'
        }
        # handleExampleTask.delay()

        return Response(data)


class FileUploadAPIView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sheet = serializer.validated_data['sheet']
        file = serializer.validated_data['file']
        actual = serializer.validated_data['actual']

        try:
            if sheet == "Facilites":
                df = pd.read_excel(file, sheet_name=sheet)
                df.fillna(0, inplace=True)
                df['geom'] = df.apply(lambda row: Point(
                    row['facilities_long'], row['facilities_lat']), axis=1)
                facilities_data = df.to_dict(orient='records')

                # # Create Facility objects
                Facility.objects.bulk_create([Facility(
                    facilities_eq_id=data['facilities_eq_id'],
                    facilities_name=data['facilities_name'],
                    facilities_country=data['facilities_country'],
                    facilities_address=data['facilities_address'],
                    facilities_type=data['facilities_type'],
                    facilities_lat=data['facilities_lat'],
                    facilities_long=data['facilities_long'],
                    facilites_rspo=data['facilites_rspo'],
                    facilites_date_update=data['facilites_date_update'],
                    geom=data['geom'],
                    # Add other fields accordingly
                ) for data in facilities_data])

                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)
            if sheet == "Refinery":
                df = pd.read_excel(file, sheet_name=sheet)
                df.fillna(0, inplace=True)
                df['geom'] = df.apply(lambda row: Point(
                    row['refinery_long'], row['refinery_lat']), axis=1)
                refinery_data = df.to_dict(orient='records')

                # # Create Refinery objects
                Refinery.objects.bulk_create([Refinery(
                    refinery_eq_id=data['refinery_eq_id'],
                    refinery_name=data['refinery_name'],
                    refinery_country=data['refinery_country'],
                    refinery_address=data['refinery_address'],
                    refinery_type=data['refinery_type'],
                    refinery_lat=data['refinery_lat'],
                    refinery_long=data['refinery_long'],
                    refinery_rspo=data['refinery_rspo'],
                    refinery_date_update=data['refinery_date_update'],
                    geom=data['geom'],
                    # Add other fields accordingly
                ) for data in refinery_data])

                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

            if sheet == "Mill":
                df = pd.read_excel(file, sheet_name=sheet)
                df.fillna(0, inplace=True)
                df['geom'] = df.apply(lambda row: Point(
                    row['mill_long'], row['mill_lat']), axis=1)
                mill_data = df.to_dict(orient='records')

                Mill.objects.bulk_create([Mill(
                    mill_eq_id=data['mill_eq_id'],
                    mill_name=data['mill_name'],
                    mill_uml_id=data['mill_uml_id'],
                    mill_company_name=data['mill_company_name'],
                    mill_company_group_id=data['mill_company_group_id'],
                    mill_company_group=data['mill_company_group'],
                    mill_country=data['mill_country'],
                    mill_province=data['mill_province'],
                    mill_district=data['mill_district'],
                    mill_address=data['mill_address'],
                    mill_type=data['mill_type'],
                    mill_lat=data['mill_lat'],
                    mill_long=data['mill_long'],
                    mill_rspo=data['mill_rspo'],
                    mill_mspo=data['mill_mspo'],
                    mill_capacity=data['mill_capacity'],
                    mill_methane_capture=data['mill_methane_capture'],
                    mill_deforestation_risk=data['mill_deforestation_risk'],
                    mill_legal_prf_risk=data['mill_legal_prf_risk'],
                    mill_legal_production_forest=data['mill_legal_production_forest'],
                    mill_legal_conservation_area=data['mill_legal_conservation_area'],
                    mill_legal_landuse_risk=data['mill_legal_landuse_risk'],
                    mill_complex_supplybase_risk=data['mill_complex_supplybase_risk'],
                    mill_date_update=data['mill_date_update'],
                    geom=data['geom'],
                    # Add other fields accordingly
                ) for data in mill_data])

                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

            if sheet == "TTM":
                df = pd.read_excel(file, sheet_name=sheet)
                df.fillna(0, inplace=True)
                ttm_data = df.to_dict(orient='records')

                Tracetomill.objects.bulk_create([Tracetomill(
                    facility_eq_id=data['facility_eq_id'],
                    mill_eq_id=data['mill_eq_id'],
                    mill_uml_id=data['mill_uml_id'],
                    mill_name=data['mill_name'],
                    ttm_source_type=data['ttm_source_type'],
                    ttm_year_period=data['ttm_year_period'],
                    ttm_date_update=data['ttm_date_update'],
                ) for data in ttm_data])
                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

            if sheet == "TTP":
                df = pd.read_excel(file, sheet_name=sheet)
                df.fillna(0, inplace=True)
                ttp_data = df.to_dict(orient='records')

                Tracetoplantation.objects.bulk_create([Tracetoplantation(
                    mill_eq_id=data['mill_eq_id'],
                    mill_uml_id=data['mill_uml_id'],
                    mill_name=data['mill_name'],
                    agriplot_eq_id=data['agriplot_eq_id'],
                    agriplot_type=data['agriplot_type'],
                    agriplot_estate_name_id=data['agriplot_estate_name_id'],
                    agriplot_estate_name=data['agriplot_estate_name'],
                    ttp_source_type=data['ttp_source_type'],
                    ttp_year_period=data['ttp_year_period'],
                    ttp_date_update=data['ttp_date_update'],

                ) for data in ttp_data])
                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

            if sheet == "Shapefile" and actual == actual:

                checkUploadFileValidationGlobal(file)

                handleShapefileAgriplot(file, Agriplot, actual)

                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

            if sheet == "ShapefileRegistration":

                checkUploadFileValidationGlobal(file)

                handleShapefilePlantedOutsideLandRegistration(
                    file, PlantedOutsideLandRegistration)

                return Response({'message': f'{sheet} Data uploaded successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.filter(is_display=True)
    serializer_class = FacilitySerializer


class PieChartViewSet(generics.CreateAPIView):
    serializer_class = FacilitySerializer

    def get(self, request, section, distinct,  *args, **kwargs):
        if section == "facility" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Facility.objects.values(display=F('facilities_country'))
                .annotate(count=Count('facilities_country'))
                .order_by('facilities_country')
            )

            total = Facility.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "facility" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Facility.objects.values(display=F('facilities_type'))
                .annotate(count=Count('facilities_type'))
                .order_by('facilities_type')
            )

            total = Facility.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "facility" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Facility.objects.values(display=F('facilites_rspo'))
                .annotate(count=Count('facilites_rspo'))
                .order_by('facilites_rspo')
            )

            total = Facility.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "refinery" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_country'))
                .annotate(count=Count('refinery_country'))
                .order_by('refinery_country')
            )

            total = Refinery.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "refinery" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_type'))
                .annotate(count=Count('refinery_type'))
                .order_by('refinery_type')
            )

            total = Refinery.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "refinery" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_rspo'))
                .annotate(count=Count('refinery_rspo'))
                .order_by('refinery_rspo')
            )
            total = Refinery.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100
            return Response(data)

        if section == "mill" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_country'))
                .annotate(count=Count('mill_country'))
                .order_by('mill_country')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_type'))
                .annotate(count=Count('mill_type'))
                .order_by('mill_type')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_rspo'))
                .annotate(count=Count('mill_rspo'))
                .order_by('mill_rspo')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "mill_deforestation_risk":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_deforestation_risk'))
                .annotate(count=Count('mill_deforestation_risk'))
                .order_by('mill_deforestation_risk')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "mill_legal_prf_risk":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_legal_prf_risk'))
                .annotate(count=Count('mill_legal_prf_risk'))
                .order_by('mill_legal_prf_risk')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "mill_legal_landuse_risk":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_legal_landuse_risk'))
                .annotate(count=Count('mill_legal_landuse_risk'))
                .order_by('mill_legal_landuse_risk')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "mill" and distinct == "mill_complex_supplybase_risk":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_complex_supplybase_risk'))
                .annotate(count=Count('mill_complex_supplybase_risk'))
                .order_by('mill_complex_supplybase_risk')
            )

            total = Mill.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "agriplot" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                TestAgriplot.objects.values(display=F('country'))
                .annotate(count=Count('country'))
                .order_by('country')
            )

            total = TestAgriplot.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)

        if section == "agriplot" and distinct == "type_of_supplier":
            from django.db.models import Count, F
            # Get distinct counts
            plantation = self.request.query_params.get('plantation', None)
            status = self.request.query_params.get('status', None)
            mill_eq_id = self.request.query_params.get('mill_eq_id', None)
            radius = self.request.query_params.get('radius', None)

            if plantation == "actual":
                data = (
                    TestAgriplot.objects.filter(mill_eq_id=mill_eq_id, legal_comp__iexact=status).values(
                        display=F('typeofsupp'))
                    .annotate(count=Count('typeofsupp'))
                    .order_by('typeofsupp')
                )
                total = TestAgriplot.objects.filter(
                    mill_eq_id=mill_eq_id, legal_comp__iexact=status).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['area'] = np.random.randint(10)
                    item['opacity'] = opacity
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                if len(data) is 0:
                    data = [{"display": "Nodata", "count": 100,
                            "total": 0, "percentage": 100, opacity: 1}]
                return Response(data)
            else:
                # geom = GEOSGeometry(geometry_wkt)
                point = Mill.objects.get(mill_eq_id=mill_eq_id)
                data = (
                    TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                ), radius)).values(
                        display=F('typeofsupp'))
                    .annotate(count=Count('typeofsupp'))
                    .order_by('typeofsupp')
                )
                total = TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                    ), radius)).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['opacity'] = opacity
                    item['area'] = np.random.randint(10)
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                return Response(data)

        if section == "agriplot" and distinct == "def_free":
            from django.db.models import Count, F
            # Get distinct counts
            plantation = self.request.query_params.get('plantation', None)
            status = self.request.query_params.get('status', None)
            mill_eq_id = self.request.query_params.get('mill_eq_id', None)
            radius = self.request.query_params.get('radius', None)

            if plantation == "actual":
                data = (
                    TestAgriplot.objects.filter(mill_eq_id=mill_eq_id, legal_comp__iexact=status).values(
                        display=F('def_free'))
                    .annotate(count=Count('def_free'))
                    .order_by('def_free')
                )
                total = TestAgriplot.objects.filter(
                    mill_eq_id=mill_eq_id, legal_comp__iexact=status).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['area'] = np.random.randint(10)
                    item['opacity'] = opacity
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                if len(data) is 0:
                    data = [{"display": "Nodata", "count": 100,
                            "total": 0, "percentage": 100, opacity: 1}]
                return Response(data)
            else:
                # geom = GEOSGeometry(geometry_wkt)
                point = Mill.objects.get(mill_eq_id=mill_eq_id)
                data = (
                    TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                ), radius)).values(
                        display=F('def_free'))
                    .annotate(count=Count('def_free'))
                    .order_by('def_free')
                )
                total = TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                    ), radius)).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['opacity'] = opacity
                    item['area'] = np.random.randint(10)
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                return Response(data)

        if section == "agriplot" and distinct == "compliance":
            from django.db.models import Count, F
            # Get distinct counts
            plantation = self.request.query_params.get('plantation', None)
            status = self.request.query_params.get('status', None)
            mill_eq_id = self.request.query_params.get('mill_eq_id', None)
            radius = self.request.query_params.get('radius', None)

            if plantation == "actual":
                data = (
                    TestAgriplot.objects.filter(mill_eq_id=mill_eq_id, legal_comp__iexact=status).values(
                        display=F('compliance'))
                    .annotate(count=Count('compliance'))
                    .order_by('compliance')
                )
                total = TestAgriplot.objects.filter(
                    mill_eq_id=mill_eq_id, legal_comp__iexact=status).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['area'] = np.random.randint(10)
                    item['opacity'] = opacity
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                if len(data) is 0:
                    data = [{"display": "Nodata", "count": 100,
                            "total": 0, "percentage": 100, opacity: 1}]
                return Response(data)
            else:
                # geom = GEOSGeometry(geometry_wkt)
                point = Mill.objects.get(mill_eq_id=mill_eq_id)
                data = (
                    TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                ), radius)).values(
                        display=F('compliance'))
                    .annotate(count=Count('compliance'))
                    .order_by('compliance')
                )
                total = TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                    ), radius)).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['opacity'] = opacity
                    item['area'] = np.random.randint(10)
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                return Response(data)

        if section == "agriplot" and distinct == "status_of_plot":
            from django.db.models import Count, F
            # Get distinct counts
            plantation = self.request.query_params.get('plantation', None)
            status = self.request.query_params.get('status', None)
            mill_eq_id = self.request.query_params.get('mill_eq_id', None)
            radius = self.request.query_params.get('radius', None)

            if plantation == "actual":
                data = (
                    TestAgriplot.objects.filter(mill_eq_id=mill_eq_id, legal_comp__iexact=status).values(
                        display=F('legal_comp'))
                    .annotate(count=Count('legal_comp'))
                    .order_by('legal_comp')
                )
                total = TestAgriplot.objects.filter(
                    mill_eq_id=mill_eq_id, legal_comp__iexact=status).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['area'] = np.random.randint(10)
                    item['opacity'] = opacity
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                if len(data) is 0:
                    data = [{"display": "Nodata", "count": 100,
                            "total": 0, "percentage": 100, opacity: 1}]
                return Response(data)
            else:
                # geom = GEOSGeometry(geometry_wkt)
                point = Mill.objects.get(mill_eq_id=mill_eq_id)
                data = (
                    TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                ), radius)).values(
                        display=F('legal_comp'))
                    .annotate(count=Count('legal_comp'))
                    .order_by('legal_comp')
                )
                total = TestAgriplot.objects.filter(legal_comp__iexact=status, geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                                                                    ), radius)).count()
                opacity = 1
                for item in data:
                    item['total'] = total
                    item['opacity'] = opacity
                    item['area'] = np.random.randint(10)
                    item['percentage'] = (item.get('count') / total)*100
                    opacity = opacity-0.15

                return Response(data)

        if section == "agriplot" and distinct == "risk_assess":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                TestAgriplot.objects.values(display=F('riskassess'))
                .annotate(count=Count('riskassess'))
                .order_by('riskassess')
            )

            total = TestAgriplot.objects.all().count()
            for item in data:
                print(item, 'item')
                item['total'] = total
                item['percentage'] = (item.get('count') / total)*100

            return Response(data)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.filter(is_display=True)
    serializer_class = FacilitySerializer


class MillViewSet(viewsets.ModelViewSet):
    queryset = Mill.objects.filter(is_display=True)
    serializer_class = MillSerializer


class AgriplotViewSet(viewsets.ModelViewSet):
    queryset = Agriplot.objects.filter(is_display=True)
    serializer_class = AgriplotSerializer
    filter_backends = [DjangoFilterBackend,]


class TTPViewSet(viewsets.ModelViewSet):
    queryset = Tracetoplantation.objects.filter(is_display=True)
    serializer_class = TracetoplantationSerializer
    filter_backends = [DjangoFilterBackend,]
    filterset_class = TracetoplantationFilter
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        distinct_values = queryset.values('agriplot_estate_name_id').annotate(
            count=Count('agriplot_estate_name_id')).values_list('agriplot_estate_name_id', flat=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(distinct_values)


class AgriplotResultViewSet(APIView):
    def get(self, request, *args, **kwargs):
        import json
        status = self.request.query_params.get('status', None)
        mill_eq_id = self.request.query_params.get('mill_eq_id', None)
        agriplots = TestAgriplot.objects.filter(
            legal_comp=status, mill_eq_id=mill_eq_id
        )
        serializer = TestAgriplotSerializer(agriplots, many=True)

        return Response(serializer.data)


class TableColumnViewSet(APIView):
    def get(self, request, section, *args, **kwargs):
        if section:
            if section == "mill":
                width = 250
                data = [
                    {
                        "field": "mill_eq_id",
                        "headerName": "Mill Eq Id",
                        "width": width,
                        "type": "string",
                        "editable": False,

                    },
                    {
                        "field": "mill_name",
                        "headerName": "Mill Name",
                        "width": width,
                        "type": "string",
                        "editable": False,

                    },
                    {
                        "field": "mill_company_name",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Company Name",
                    },

                    {
                        "field": "mill_company_group_id",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Company Group Id",
                    },
                    {
                        "field": "mill_company_group",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Company Group",
                    },
                    {
                        "field": "mill_country",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Country",
                    },
                    {
                        "field": "mill_province",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Province",
                    },
                    {
                        "field": "mill_district",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill District",
                    },
                    {
                        "field": "mill_address",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Address",
                    },
                    {
                        "field": "mill_type",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Type",
                    },
                    {
                        "field": "mill_lat",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Lat",
                    },
                    {
                        "field": "mill_long",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Long",
                    },
                    {
                        "field": "mill_rspo",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Rspo",
                    },
                    {
                        "field": "mill_mspo",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Mspo",
                    },
                    {
                        "field": "mill_capacity",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Capacity",
                    },
                    {
                        "field": "mill_methane_capture",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Methane Capture",
                    },
                    {
                        "field": "mill_deforestation_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Deforestation Risk",
                    },
                    {
                        "field": "mill_legal_prf_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Legal Prf Risk",
                    },
                    {
                        "field": "mill_legal_production_forest",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Legal Production Forest",
                    },
                    {
                        "field": "mill_legal_conservation_area",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Legal Conservation Area",
                    },
                    {
                        "field": "mill_legal_landuse_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Legal Landuse Risk",
                    },
                    {
                        "field": "mill_complex_supplybase_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Complex Supplybase Risk",
                    },
                    {
                        "field": "mill_date_update",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Mill Date Update",
                    },
                ]
                return Response({"columns": data})
            if section == "agriplot":
                width = 250
                data = [
                    {
                        "field": "id",
                        "headerName": "id",
                        "width": width,
                        "type": "number",
                        "editable": False,

                    },

                    {
                        "field": "ownership",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Ownership",
                    },

                    {
                        "field": "subsidiary",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Subsidiary",
                    },
                    {
                        "field": "estate",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Estate",
                    },
                    {
                        "field": "id_estate",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "ID_Estate",
                    },
                    {
                        "field": "agriplotid",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "AgriplotID",
                    },
                    {
                        "field": "typeofsupp",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "TypeOfSupp",
                    },
                    {
                        "field": "village",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Village",
                    },
                    {
                        "field": "subdistric",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "SubDistric",
                    },
                    {
                        "field": "district",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "District",
                    },
                    {
                        "field": "province",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Province",
                    },
                    {
                        "field": "country",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Country",
                    },
                    {
                        "field": "planted_ar",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Planted_Ar",
                    },
                    {
                        "field": "yearupdate",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "YearUpdate",
                    },
                    {
                        "field": "riskassess",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "RiskAssess",
                    },
                    {
                        "field": "ghg_luc",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "GHG_LUC",
                    },
                    {
                        "field": "luas",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Luas",
                    },
                    {
                        "field": "mill_eq_id",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_eq_id",
                    },
                    {
                        "field": "def_free",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Def_Free",
                    },
                    {
                        "field": "compliance",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Compliance",
                    },
                    {
                        "field": "legal_comp",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "Legal_Comp",
                    },

                ]
                return Response({"columns": data})
        return Response({"columns": []})


class AgriplotResultWKTViewSet(APIView):
    def get(self, request, *args, **kwargs):
        status = self.request.query_params.get('status', None)
        # geometry_wkt = self.request.query_params.get('geometry_wkt', None)
        mill_eq_id = self.request.query_params.get('mill_eq_id', None)
        radius = self.request.query_params.get('radius', None)
        agriplots = TestAgriplot.objects.all()
        point = Mill.objects.get(mill_eq_id=mill_eq_id)
        if status:
            agriplots = agriplots.filter(legal_comp=status)
        if radius:
            # geom = GEOSGeometry(geometry_wkt)
            agriplots = agriplots.filter(geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                              ), radius))

        serializer = TestAgriplotSerializer(agriplots, many=True)

        return Response(serializer.data)


# Geojson for the agriplot
class AgriplotGeoJSONAPIView(generics.ListAPIView):
    serializer_class = TestAgriplotGeojsonSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        mill_eq_id = self.request.query_params.get('mill_eq_id', None)

        queryset = TestAgriplot.objects.all()
        if status:
            queryset = queryset.filter(legal_comp=status)
        if mill_eq_id:
            queryset = queryset.filter(mill_eq_id=mill_eq_id)

        return queryset

# Geojson for the agriplot


def distance_to_decimal_degrees(distance, latitude):
    """
    Source of formulae information:
        1. https://en.wikipedia.org/wiki/Decimal_degrees
        2. http://www.movable-type.co.uk/scripts/latlong.html
    :param distance: an instance of `from django.contrib.gis.measure.Distance`
    :param latitude: y - coordinate of a point/location
    """
    lat_radians = latitude * (math.pi / 180)
    # 1 longitudinal degree at the equator equal 111,319.5m equiv to 111.32km
    return distance.m / (111_319.5 * math.cos(lat_radians))


class AgriplotGeoJSONAPIViewWKT(generics.ListAPIView):
    serializer_class = TestAgriplotGeojsonSerializer

    def get_queryset(self):
        status = self.request.query_params.get('status', None)
        geometry_wkt = self.request.query_params.get('geometry_wkt', None)
        mill_eq_id = self.request.query_params.get('mill_eq_id', None)
        radius = self.request.query_params.get('radius', None)

        queryset = TestAgriplot.objects.all()
        point = Mill.objects.get(mill_eq_id=mill_eq_id)
        print(point.geom.coords, 'coords')
        if status:
            queryset = queryset.filter(legal_comp=status)
        if radius:
            # geom = GEOSGeometry(geometry_wkt)
            queryset = queryset.filter(geom__dwithin=(Point(point.geom.coords[0], point.geom.coords[1]
                                                            ), distance_to_decimal_degrees(D(m=int(50000)), point.geom.coords[1])))

            # queryset = queryset.filter(geom__intersects=geom)
        if mill_eq_id:
            queryset = queryset.exclude(mill_eq_id=mill_eq_id)

        return queryset

    # def get(self, request, *args, **kwargs):
    #     status = self.request.query_params.get('status', None)
    #     geometry_wkt = self.request.query_params.get('geometry_wkt', None)
    #     mill_eq_id = self.request.query_params.get('mill_eq_id', None)

    #     point = Mill.objects.get(mill_eq_id=mill_eq_id)
    #     gdf = gpd.read_file('Shapefiles/Finaltest_15012024.shp')
    #     # Assuming you want to filter gdf based on queryset

    #     #    status_of_plot=row['Legal_Comp'],
    #     #             def_free=row['Def_Free'],
    #     #             compliance=row['Compliance'],
    #     # if status:
    #     #     gdf = gdf[gdf['Legal_Comp'] == status]
    #     #     print(gdf, 'gdf')
    #     # if geometry_wkt:
    #     #     # Assuming gdf has geometry column 'geometry'
    #     #     geom = GEOSGeometry(geometry_wkt)
    #     #     gdf = gdf[gdf['geometry'].apply(lambda x: geom.intersects(x))]
    #     # if mill_eq_id:
    #     #     gdf = gdf[~gdf['millideq'].isin([mill_eq_id])]

    #     geojson_data = gdf.to_crs(epsg='4326').to_json()
    #     geojson_dict = json.loads(geojson_data)

    #     return Response(geojson_dict)
