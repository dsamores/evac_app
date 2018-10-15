from django.urls import path

from . import views

urlpatterns = [
    path('guest', views.guest, name='survey-guest'),
    path('', views.index, name='survey-index'),
]