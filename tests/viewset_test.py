import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


def test_posting_valid_data_returns_utm_zones(post_viewset_result):
    assert post_viewset_result.status_code == 200
    assert post_viewset_result.data == {}


@pytest.fixture
def api_client():
    return APIClient(enforce_csrf_checks=True)


@pytest.fixture
def utm_zone_post_url():
    return reverse('utm_zone_info:utm_zone_info-list')


@pytest.fixture
def post_viewset_result(api_client, utm_zone_post_url):
    return api_client.post(utm_zone_post_url, {}, format='json')
