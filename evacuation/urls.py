from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map', views.building_map, name='building_map'),
    path('alerts', views.alerts, name='alerts'),
]