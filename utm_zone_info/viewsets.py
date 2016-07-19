from rest_framework import status, viewsets
from rest_framework.response import Response

from utm_zone_info.coordinate_reference_system import utm_zones_for_representing
from utm_zone_info.serializers import GeometrySerializer


class UTMZoneInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet accepting Points and returning valid utm_zones.
    """

    serializer_class = GeometrySerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            geometry = serializer.validated_data['geom']
            if geometry.srid is None:
                geometry.srid = serializer.validated_data['srid']
            data = dict(
                utm_zone_srids=[zone.srid for zone in utm_zones_for_representing(geometry)]
            )
            return Response(data=data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
