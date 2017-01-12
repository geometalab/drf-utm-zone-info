from rest_framework.reverse import reverse


def test_reverse_resolution_results_in_nice_pattern():
    expected_test_url = '/api-without-namespace/utm-zone-info/'
    assert expected_test_url == reverse('utm-zone-info')

    expected_test_url = '/api/utm-zone-info/'
    assert expected_test_url == reverse('utm_zone_info:utm-zone-info')
