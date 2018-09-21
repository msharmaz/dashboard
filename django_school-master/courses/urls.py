from django.conf.urls import url

from . import views

app_name = 'courses'
urlpatterns = [
    url(r'^$', views.courses, name='index'),
    url(r'courses$', views.courses, name='courses'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
]
