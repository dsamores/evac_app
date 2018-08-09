from django.shortcuts import render

from .models import Notification, Interaction, Obstacle

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.utils import timezone
import json
import datetime
from django.core import serializers


def index(request):
    return render(request, 'evacuation/index.html', {})


def building_map(request):
    obstacles = Obstacle.objects.filter(active=True)

    context = {
        'obstacles': serializers.serialize('json', obstacles),
    }
    return render(request, 'evacuation/building-map.html', context)


def alerts(request):
    context = {}
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            message__active=True, user=request.user
        ).order_by('-sent_time')[:10]
        context = {
            'notifications': notifications,
        }
    return render(request, 'evacuation/alerts.html', context)


def login_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)


@api_view(['POST'])
def new_user(request):
    user = User()
    user.save()
    user.username = 'anon_%d' % user.id
    user.save()
    login_user(request, user.id)
    return Response({"user_id": request.user.id})


@api_view(['POST'])
def auto_login(request):
    user_id = request.POST['user_id']
    refresh = False
    if not request.user.is_authenticated:
        login_user(request, user_id)
        refresh = True
    return Response({"user_id": request.user.id, "refresh": refresh})


@api_view(['POST'])
def read_notifications(request):
    notification_ids = request.POST.getlist('notification_ids[]')
    Notification.objects.filter(id__in=notification_ids).update(read_time=timezone.now())
    return Response({"success": True})


@api_view(['POST'])
def save_interactions(request):
    interactions_raw = json.loads(request.POST.getlist('interactions')[0])
    for interaction_raw in interactions_raw:
        assert request.user.id == int(interaction_raw['userId'])
        interaction = Interaction(
            user=request.user, type=interaction_raw['type'],
            description=interaction_raw['description'],
            page=interaction_raw['page'],
            element=interaction_raw['element'],
            time=datetime.datetime.fromtimestamp(interaction_raw['time'] / 1000.0),
        )
        interaction.save()
    return Response({"success": True})
