from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from utm_zone_info.coordinate_reference_system import utm_zones_for_representing
from utm_zone_info.serializers import GeometrySerializer


@api_view(['POST'])
def utm_zone_info(request):
    """
    A simple View accepting a geometry and returning SRIDs of UTM Zones that can represent this geometry.
    """

    # only POST allowed, so no need to check for "request.method == 'POST'"
    serializer = GeometrySerializer(data=request.data)
    if serializer.is_valid():
        geometry = serializer.validated_data['geom']
        geometry.srid = serializer.validated_data['srid']
        data = dict(
            utm_zone_srids=[zone.srid for zone in utm_zones_for_representing(geometry)]
        )
        return Response(data=data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
