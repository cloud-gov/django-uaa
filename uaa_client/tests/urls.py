from django.conf.urls import include, url

urlpatterns = [
    url(r'^auth/', include('uaa_client.urls')),
    url(r'^fake/', include('uaa_client.fake_uaa_provider.urls')),
]
