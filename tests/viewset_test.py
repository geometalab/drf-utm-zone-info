from unittest import mock

import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def test_posting_valid_data_returns_utm_zones(api_client, utm_zone_post_url, payload):
    expected_srid = 123456
    utm_zone_mock = mock.Mock()
    utm_zone_mock.srid = expected_srid
    with mock.patch(
            'utm_zone_info.viewsets.utm_zones_for_representing', return_value=[utm_zone_mock]):
        post_viewset_result = api_client.post(utm_zone_post_url, payload, format='json')
        expected_result = {'utm_zone_srids': [expected_srid]}
        assert post_viewset_result.json() == expected_result


@pytest.fixture
def valid_geoJSON():
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]
            ]
        ]
    }


@pytest.fixture
def payload(valid_geoJSON):
    return {
        "srid": 4326,
        'geom': valid_geoJSON,
    }


@pytest.fixture
def api_client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def utm_zone_post_url():
    return reverse('utm_zone_info:utm_zone_info-list')
