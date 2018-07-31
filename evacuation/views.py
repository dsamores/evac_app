from django.http import HttpResponse
from django.shortcuts import render

from .models import Notification


def index(request):
    return HttpResponse("Hello, world!!")


def building_map(request):
    last_notification_list = Notification.objects.order_by('-date')[:5]
    context = {'last_notification_list': last_notification_list}
    return render(request, 'evacuation/building-map.html', context)


def alerts(request):
    last_notification_list = Notification.objects.order_by('-date')[:5]
    context = {'last_notification_list': last_notification_list}
    return render(request, 'evacuation/alerts.html', context)
