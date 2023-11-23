from rest_framework import serializers
from .models import Facility, Mill, Tracetoplantation


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


class TracetoplantationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracetoplantation
        exclude = ("created_at", "is_display",
                   "is_deleted", "is_edited",)
