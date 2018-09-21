from django.conf.urls import url

from . import views
app_name = 'professors'
urlpatterns = [
    url(r'^$', views.professors, name='index'),
    url(r'professors$', views.professors, name='professors'),
    url(r'^(?P<professor_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<professor_id>[0-9]+)/add_section$', views.add_section, name='add_section'),
    url(r'^(?P<professor_id>[0-9]+)/create_section$', views.create_section, name='create_section'),
]
