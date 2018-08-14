from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('login', views.browser_login, name='browser_login'),
    path('register', views.register, name='register'),
    path('forget', views.forget, name='forget'),
    path('logout', views.logout_view, name='logout'),
    path('building-map', views.building_map, name='building_map'),
    path('alerts', views.alerts, name='alerts'),
    path('statements', views.statements, name='statements'),

    # web services
    path('new_user', views.new_user, name='new_user'),
    path('auto_login', views.auto_login, name='auto_login'),
    path('read_notifications', views.read_notifications, name='read_notifications'),
    path('save_interactions', views.save_interactions, name='save_interactions'),
]