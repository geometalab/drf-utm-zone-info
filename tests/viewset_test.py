import pytest
from django.contrib.gis.geos import Polygon
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

import utm_zone_info


def test_posting_valid_data_returns_utm_zones(mocker, api_client, utm_zone_post_url, payload):
    utm_zone_mock = mocker.Mock()
    utm_zone_mock.srid = 123456
    mocker.patch('utm_zone_info.views.utm_zones_for_representing', return_value=[utm_zone_mock])
    post_viewset_result = api_client.post(utm_zone_post_url, payload, format='json')
    utm_zone_info.views.utm_zones_for_representing.assert_called_once_with(Polygon(*_valid_geoJSON['coordinates']))
    args, kwargs = utm_zone_info.views.utm_zones_for_representing.call_args
    assert args[0].srid == 4326
    assert post_viewset_result.status_code == status.HTTP_200_OK
    assert post_viewset_result.data == {'utm_zone_srids': [utm_zone_mock.srid]}


def test_posting_invalid_data_returns_error(api_client, utm_zone_post_url, invalid_payload):
    post_viewset_result = api_client.post(utm_zone_post_url, invalid_payload, format='json')
    assert post_viewset_result.status_code == status.HTTP_400_BAD_REQUEST


_valid_geoJSON = {
    "type": "Polygon",
    "coordinates": [
        [
            [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
        ]
    ]
}


@pytest.fixture(params=[
    dict(),
    dict(geom=''),
    dict(srid=None),
    dict(geom=None, srid=None),
    dict(geom='', srid=None),
    dict(geom=None, srid=''),
    dict(geom='', srid=4326),
    dict(geom=_valid_geoJSON, srid=''),
    dict(geom={key: value for key, value in _valid_geoJSON.items() if key != 'type'}, srid=4326),
    dict(geom={key: value for key, value in _valid_geoJSON.items() if key != 'coordinates'}, srid=4326),
])
def invalid_payload(request):
    return request.param


@pytest.fixture(params=[
    dict(geom=_valid_geoJSON, srid=4326)
])
def payload(request):
    return request.param


@pytest.fixture
def api_client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def utm_zone_post_url():
    return reverse('utm_zone_info:utm-zone-info')
