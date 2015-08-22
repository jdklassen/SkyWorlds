
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^build/(?P<item_name>\w*)/$', views.build, name='build'),
    url(r'^research/(?P<tech_name>\w*)/$', views.research, name='research'),
]

