
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^build/(?P<item_name>\w*)/$', views.build, name='build'),
    url(r'^research/(?P<tech_name>\w*)/$', views.research, name='research'),
    url(r'^stay/$', views.stay, name='stay'),
    url(r'^travel/(?P<dx>[-0-9]*)_(?P<dy>[-0-9]*)/$', views.travel, name='travel'),
]

