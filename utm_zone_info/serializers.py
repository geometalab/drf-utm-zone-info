from rest_framework import serializers
from rest_framework_gis.fields import GeometryField


class GeometrySerializer(serializers.Serializer):
    geom = GeometryField()

    def to_internal_value(self, data):
        return super(GeometrySerializer, self).to_internal_value(data)['geom']

    def to_representation(self, instance):
        return super(GeometrySerializer, self).to_representation(dict(geom=instance))
