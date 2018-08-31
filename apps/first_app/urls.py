from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^dashboard/$', views.dashboard),
    url(r'^wish_item/create/$', views.create_show),
    url(r'^create/$',views.create),
    url(r'^delete/(?P<item_id>\d+)$',views.delete),
    url(r'^addw/(?P<item_id>\d+)$', views.addw),
    url(r'^removew/(?P<item_id>\d+)$', views.removew),
    url(r'^wish_items/(?P<item_id>\d+)$', views.wish_items_show),
    url(r'^logout/$', views.logout)
]