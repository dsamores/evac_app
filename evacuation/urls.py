from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('building-map', views.building_map, name='building_map'),
    path('alerts', views.alerts, name='alerts'),
    path('new_user', views.new_user, name='new_user'),
    path('auto_login', views.auto_login, name='auto_login'),
    path('read_notifications', views.read_notifications, name='read_notifications'),
]