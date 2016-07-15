from django.contrib.gis.geos import Point
from rest_framework_gis.fields import GeoJsonDict

from utm_zone_info.serializers import GeometrySerializer


def test_serialize_point():
    p = Point(5, -23)
    native_input = dict(geom=p)
    representation = GeometrySerializer(native_input).data
    assert representation == {'geom': GeoJsonDict([('type', 'Point'), ('coordinates', (5.0, -23.0))])}


def test_deserialize_point():
    representation = {'geom': GeoJsonDict([('type', 'Point'), ('coordinates', (5.0, -23.0))])}
    serializer = GeometrySerializer(data=representation)
    assert serializer.is_valid()
    native_output = serializer.validated_data
    assert native_output == dict(geom=Point(5, -23))
