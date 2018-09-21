from django.conf.urls import url
from dashboard import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^signin$', views.signin),
    url(r'^sucess$', views.sucess),
    url(r'^users/new$', views.new),
    url(r'^users/register$', views.register),
    url(r'^dashboard/admin$', views.adm_db),
    url(r'^dashboard$', views.dashboard),
    url(r'^users/show/(?P<uid>\d+)$', views.show),
    url(r'^users/edit/(?P<uid>\d+)$', views.adm_edit),
    url(r'^users/edit$', views.edit),
    url(r'^users/update_info$', views.update_info),
    url(r'^users/update_pwd$', views.update_pwd),
    url(r'^users/update_desc$', views.update_desc),
    url(r'^destroy/(?P<uid>\d+)$', views.destroy),
    url(r'^delete/(?P<uid>\d+)$', views.delete),
    url(r'^post_msg$', views.post_msg),
    url(r'^post_cmt$', views.post_cmt),
    url(r'^reset$', views.reset),
    
]