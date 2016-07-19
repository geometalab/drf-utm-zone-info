from rest_framework import viewsets
from rest_framework.response import Response


class UTMZoneInfoViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for posting Points and returns valid utm_zones.
    """

    def create(self, request):
        return Response(data={})
