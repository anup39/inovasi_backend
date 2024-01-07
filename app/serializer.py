from rest_framework import serializers
from .models import Facility, Mill, Agriplot, Tracetoplantation
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class FileUploadSerializer(serializers.Serializer):
    sheet = serializers.CharField()
    file = serializers.FileField()
    actual = serializers.CharField()


class ShapeFileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = "__all__"


class MillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mill
        exclude = ("geom", "created_at", "is_display",
                   "is_deleted", "is_edited",)


class AgriplotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agriplot
        exclude = ("created_at", "is_display",
                   "is_deleted", "is_edited", "actual_supplier")


class TracetoplantationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracetoplantation
        exclude = ("created_at", "is_display",
                   "is_deleted", "is_edited",)


# Geojson for the agriplot
class AgriplotGeojsonSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Agriplot
        geo_field = "geom"
        fields = "__all__"
