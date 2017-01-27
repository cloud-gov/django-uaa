import django
from django.conf.urls import include, url

if django.get_version().startswith('1.8.'):
    urlpatterns = [
        url(r'^auth/', include('uaa_client.urls', namespace='uaa_client')),
        url(r'^fake/', include('uaa_client.fake_uaa_provider.urls',
                               namespace='fake_uaa_provider')),
    ]
else:
    urlpatterns = [
        url(r'^auth/', include('uaa_client.urls')),
        url(r'^fake/', include('uaa_client.fake_uaa_provider.urls')),
    ]
