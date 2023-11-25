from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Facility, Refinery, Mill, Agriplot, Tracetomill, Tracetoplantation, PlantedOutsideLandRegistration
from .tasks import handleExampleTask
from .serializer import FileUploadSerializer, ShapeFileUploadSerializer, FacilitySerializer, MillSerializer, AgriplotSerializer, TracetoplantationSerializer
from django.contrib.gis.geos import Point
from rest_framework import generics, status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import pandas as pd
import zipfile
import glob
from django.core.exceptions import ValidationError
import geopandas as gpd
from django.contrib.gis.geos import (
    GEOSGeometry)
from .filters import TracetoplantationFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
# Create your views here.


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
    with zipfile.ZipFile(shape_file, "r") as zip_ref:
        zip_ref.extractall(str(shape_file))
    shape = glob.glob(r'{}/**/*.shp'.format(str(shape_file)),
                      recursive=True)[0]
    print(shape, 'shape')
    gdf = gpd.read_file(shape)
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
                    # ID_Mill=row['ID_Mill'],
                    # Mill_Name=row['Mill_Name'],
                    Ownership=row['Ownership'],
                    Subsidiary=row['Subsidiary'],
                    Estate=row['Estate'],
                    id_estate=row['ID_Estate'],
                    AgriplotID=row['AgriplotID'],
                    TypeOfSupp=row['TypeOfSupp'],
                    Village=row['Village'],
                    SubDistric=row['SubDistric'],
                    District=row['District'],
                    Province=row['Province'],
                    Country=row['Country'],
                    Planted_Ar=row['Planted_Ar'],
                    YearUpdate=row['YearUpdate'],
                    RiskAssess=row['RiskAssess'],
                    GHG_LUC=row['GHG_LUC'],
                    Status=row['Status'],
                    geom=polygon,
                    actual_supplier=actual_supplier
                )
        else:
            model.objects.create(
                # ID_Mill=row['ID_Mill'],
                # Mill_Name=row['Mill_Name'],
                Ownership=row['Ownership'],
                Subsidiary=row['Subsidiary'],
                Estate=row['Estate'],
                id_estate=row['ID_Estate'],
                AgriplotID=row['AgriplotID'],
                TypeOfSupp=row['TypeOfSupp'],
                Village=row['Village'],
                SubDistric=row['SubDistric'],
                District=row['District'],
                Province=row['Province'],
                Country=row['Country'],
                Planted_Ar=row['Planted_Ar'],
                YearUpdate=row['YearUpdate'],
                RiskAssess=row['RiskAssess'],
                GHG_LUC=row['GHG_LUC'],
                Status=row['Status'],
                geom=geom,
                actual_supplier=actual_supplier

            )
            pass

    return bound_dict


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
                    Mukim=row['Mukim'],
                    ID_Mukim=row['ID_Mukim'],
                    Daerah=row['Daerah'],
                    ID_Daerah=row['ID_Daerah'],
                    Negeri=row['Negeri'],
                    ID_Negeri=row['ID_Negeri'],
                    Country=row['Country'],
                    Note=row['Note'],
                    Status=row['Status'],
                    geom=polygon,

                )
        else:
            model.objects.create(
                Mukim=row['Mukim'],
                ID_Mukim=row['ID_Mukim'],
                Daerah=row['Daerah'],
                ID_Daerah=row['ID_Daerah'],
                Negeri=row['Negeri'],
                ID_Negeri=row['ID_Negeri'],
                Country=row['Country'],
                Note=row['Note'],
                Status=row['Status'],
                geom=geom,

            )
            pass

    return bound_dict


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

            return Response(data)

        if section == "facility" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Facility.objects.values(display=F('facilities_type'))
                .annotate(count=Count('facilities_type'))
                .order_by('facilities_type')
            )

            return Response(data)

        if section == "facility" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Facility.objects.values(display=F('facilites_rspo'))
                .annotate(count=Count('facilites_rspo'))
                .order_by('facilites_rspo')
            )

            return Response(data)

        if section == "refinery" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_country'))
                .annotate(count=Count('refinery_country'))
                .order_by('refinery_country')
            )

            return Response(data)

        if section == "refinery" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_type'))
                .annotate(count=Count('refinery_type'))
                .order_by('refinery_type')
            )

            return Response(data)

        if section == "refinery" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Refinery.objects.values(display=F('refinery_rspo'))
                .annotate(count=Count('refinery_rspo'))
                .order_by('refinery_rspo')
            )

            return Response(data)

        if section == "mill" and distinct == "country":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_country'))
                .annotate(count=Count('mill_country'))
                .order_by('mill_country')
            )

            return Response(data)

        if section == "mill" and distinct == "type":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_type'))
                .annotate(count=Count('mill_type'))
                .order_by('mill_type')
            )

            return Response(data)

        if section == "mill" and distinct == "rspo":
            from django.db.models import Count, F
            # Get distinct counts
            data = (
                Mill.objects.values(display=F('mill_rspo'))
                .annotate(count=Count('mill_rspo'))
                .order_by('mill_rspo')
            )

            return Response(data)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.filter(is_display=True)
    serializer_class = FacilitySerializer


class MillViewSet(viewsets.ModelViewSet):
    queryset = Mill.objects.filter(is_display=True)
    serializer_class = MillSerializer


class AgriplotViewSet(viewsets.ModelViewSet):
    queryset = Agriplot.objects.all()[:100]
    serializer_class = AgriplotSerializer


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
        estate_ids = request.GET.get('estateids')
        agriplots = Agriplot.objects.filter(
            id_estate__in=json.loads(estate_ids)
        )
        serializer = AgriplotSerializer(agriplots, many=True)

        return Response(serializer.data)


class TableColumnViewSet(APIView):
    def get(self, request, section, *args, **kwargs):
        if section:
            if section == "mill":
                width = 250
                data = [
                    {
                        "field": "mill_eq_id",
                        "headerName": "mill_eq_id",
                        "width": width,
                        "type": "string",
                        "editable": False,

                    },

                    {
                        "field": "mill_company_name",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_company_name",
                    },

                    {
                        "field": "mill_company_group_id",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_company_group_id",
                    },
                    {
                        "field": "mill_company_group",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_company_group",
                    },
                    {
                        "field": "mill_country",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_country",
                    },
                    {
                        "field": "mill_province",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_province",
                    },
                    {
                        "field": "mill_district",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_district",
                    },
                    {
                        "field": "mill_address",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_address",
                    },
                    {
                        "field": "mill_type",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_type",
                    },
                    {
                        "field": "mill_lat",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_lat",
                    },
                    {
                        "field": "mill_long",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_long",
                    },
                    {
                        "field": "mill_rspo",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_rspo",
                    },
                    {
                        "field": "mill_mspo",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_mspo",
                    },
                    {
                        "field": "mill_capacity",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_capacity",
                    },
                    {
                        "field": "mill_methane_capture",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_methane_capture",
                    },
                    {
                        "field": "mill_deforestation_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_deforestation_risk",
                    },
                    {
                        "field": "mill_legal_prf_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_legal_prf_risk",
                    },
                    {
                        "field": "mill_legal_production_forest",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_legal_production_forest",
                    },
                    {
                        "field": "mill_legal_conservation_area",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_legal_conservation_area",
                    },
                    {
                        "field": "mill_legal_landuse_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_legal_landuse_risk",
                    },
                    {
                        "field": "mill_complex_supplybase_risk",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_complex_supplybase_risk",
                    },
                    {
                        "field": "mill_date_update",
                        "type": "string",
                        "width": width,
                        "editable": False,
                        "headerName": "mill_date_update",
                    },
                ]
                return Response({"columns": data})
        return Response({"columns": []})
