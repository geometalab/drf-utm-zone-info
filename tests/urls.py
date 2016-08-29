from django.conf.urls import url, include

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include('utm_zone_info.urls', namespace='utm_zone_info')),
    url(r'^api-without-namespace/', include('utm_zone_info.urls')),
]
