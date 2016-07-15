import pytest
from django.contrib.gis.geos import Point
from rest_framework_gis.fields import GeoJsonDict

from utm_zone_info.serializers import GeometrySerializer


def test_serialize_point(geos_geometry, geos_geometry_representation):
    native_input = dict(geom=geos_geometry)
    representation = GeometrySerializer(native_input).data
    assert representation == geos_geometry_representation


def test_deserialize_point(geos_geometry, geos_geometry_representation):
    representation = geos_geometry_representation
    serializer = GeometrySerializer(data=representation)
    assert serializer.is_valid()
    native_output = serializer.validated_data
    assert native_output == dict(geom=geos_geometry)


@pytest.fixture
def geos_geometry():
    return Point(5, -23)


@pytest.fixture
def geos_geometry_representation():
    return {'geom': GeoJsonDict([('type', 'Point'), ('coordinates', (5.0, -23.0))])}
