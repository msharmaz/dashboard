from django.conf.urls import url, include
from django.contrib import admin
from .views import home, register, newpost
from django.conf import settings


urlpatterns = [
    url(r'^$', home),
    url(r'^register/', register),
    url(r'^newpost/', newpost, name='new_post'),
]



