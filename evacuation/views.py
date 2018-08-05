from django.shortcuts import render

from .models import Message, Notification

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.utils import timezone


def index(request):
    return render(request, 'evacuation/index.html', {})


def building_map(request):
    return render(request, 'evacuation/building-map.html', {})


def alerts(request):
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
