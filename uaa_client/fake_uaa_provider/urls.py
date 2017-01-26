from django.conf.urls import url

from . import views

app_name = 'fake_uaa_provider'

urlpatterns = [
    url(r'^oauth/authorize$', views.authorize, name='auth'),
    url(r'^oauth/token$', views.access_token, name='token'),
]
