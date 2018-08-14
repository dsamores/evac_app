from django.shortcuts import render, redirect

from .models import Notification, Interaction, Obstacle, EvacUser

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
import json
import datetime
from django.core import serializers
from django.contrib import messages


def index(request):
    if not request.user.is_authenticated:
        return redirect('browser_login')
    webpush = {'group': 'group1'}
    context = {
        'user_id': request.user.id,
        'webpush': webpush,
    }
    return render(request, 'evacuation/index.html', context)


def browser_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'evacuation/login.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.add_message(request, messages.ERROR, "Incorrect email or password")
            return render(request, 'evacuation/login.html')


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        return render(request, 'evacuation/register.html')
    else:
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            messages.add_message(request, messages.ERROR, "Email already taken")
            return render(request, 'evacuation/register.html')

        user = User.objects.create_user(email, email, password)
        user.save()

        extended_user = EvacUser(
            user=user,
            age=int(request.POST['age']),
            gender=request.POST['gender'],
            building_occupant=request.POST['building_occupant'] == 'on',
        )
        extended_user.save()

        login(request, user)
        return redirect('index')


def forget(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'evacuation/forget.html')


def logout_view(request):
    logout(request)
    return render(request, 'evacuation/logout.html')


def building_map(request):
    if not request.user.is_authenticated:
        return redirect('browser_login')
    obstacles = Obstacle.objects.filter(active=True)

    context = {
        'obstacles': serializers.serialize('json', obstacles),
    }
    return render(request, 'evacuation/building-map.html', context)


def alerts(request):
    if not request.user.is_authenticated:
        return redirect('browser_login')
    context = {}
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(
            message__active=True, user=request.user
        ).order_by('-sent_time')[:10]
        context = {
            'notifications': notifications,
        }
    return render(request, 'evacuation/alerts.html', context)


def statements(request):
    if not request.user.is_authenticated:
        return redirect('browser_login')
    return render(request, 'evacuation/statements.html')


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
