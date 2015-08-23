
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^build/(?P<item_name>\w*)/$', views.build, name='build'),
    url(r'^research/(?P<tech_name>\w*)/$', views.research, name='research'),
    url(r'^stay/$', views.stay, name='stay'),
    url(r'^travel/(?P<dx>[-0-9]*)_(?P<dy>[-0-9]*)/$', views.travel, name='travel'),

    url(r'^populate/$', views.populate, name='populate'),
    url(r'^populate/force/$', views.populate, {'forced': True}, name='populate.force'),
    url(r'^populate/(?P<x>[0-9]*)_(?P<y>[0-9]*)/(?P<p>[0-9]*)/$', views.populate, name='populate'),
    url(r'^populate/(?P<x>[0-9]*)_(?P<y>[0-9]*)/(?P<p>[0-9]*)/force/$', views.populate, {'forced': True}, name='populate.force'),
    url(r'^controls/$', views.controls, name='controls'),
]

