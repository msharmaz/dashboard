from django.conf.urls import url

from . import views

app_name = 'sections'
urlpatterns = [
    url(r'^$', views.sections, name='index'),
    url(r'sections$', views.sections, name='sections'),
    url(r'^(?P<section_id>[0-9]+)/delete$', views.delete, name='delete'),
]
