from django.shortcuts import render

from .models import Notification

from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


def index(request):
    last_notification_list = Notification.objects.order_by('-date')[:5]
    context = {'last_notification_list': last_notification_list}
    return render(request, 'evacuation/index.html', context)


def building_map(request):
    last_notification_list = Notification.objects.order_by('-date')[:5]
    context = {'last_notification_list': last_notification_list}
    return render(request, 'evacuation/building-map.html', context)


def alerts(request):
    unread_notifications = Notification.objects.filter(read=False).order_by('-date')
    read_notifications = Notification.objects.filter(read=True).order_by('-date')[:5]
    context = {
        'unread_notifications': unread_notifications,
        'read_notifications': read_notifications,
    }
    return render(request, 'evacuation/alerts.html', context)


@api_view(['POST'])
def new_user(request):
    user = User()
    user.save()
    user.username = 'anon_%d' % user.id
    user.save()
    return Response({"user_id": user.id})
