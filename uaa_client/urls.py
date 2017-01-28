from django.conf.urls import url

from . import views

app_name = 'uaa_client'

urlpatterns = [
    url(r'^callback$', views.oauth2_callback, name='callback'),
    url(r'^login$', views.login, name='login'),
]
