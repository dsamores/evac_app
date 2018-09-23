from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, re_path
from django.shortcuts import redirect
from django.contrib import messages

from .models import Message, Notification, Obstacle, Place, EvacUser, Office, Desk
from webpush import send_group_notification
from webpush.models import PushInformation

admin.site.register(EvacUser)


@admin.register(Obstacle)
class ObstacleAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'active',
    )


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'floor',
    )


@admin.register(Desk)
class DeskAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'office',
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'display_name',
        'floor',
        'active',
        'is_landmark',
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'group',
        'date_created',
        'message_actions',
    )

    def send_all(self, request, message_id, *args, **kwargs):
        message = self.get_object(request, message_id)
        message.sent = True
        message.save()

        for push_information in PushInformation.objects.filter(group=message.group):
            notification = Notification(user=push_information.user, message=message)
            notification.save()

        url = message.action_url if message.action_url else reverse('alerts')
        url += '?from_push={}'.format(message.id)

        payload = {
            "head": message.title,
            "body": message.description,
            "url": url
        }
        send_group_notification(group_name=str(message.group), payload=payload, ttl=1000)

        messages.success(request, 'Message %s sent to all users' % message_id)
        return redirect('admin:evacuation_message_changelist')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r'^(?P<message_id>.+)/send_all/$',
                self.admin_site.admin_view(self.send_all),
                name='message-send-all',
            ),
        ]
        return custom_urls + urls

    def message_actions(self, obj):
        if obj.sent:
            return 'Already sent!'
        return format_html(
            '<a class="button" href="{}">Send all</a>',
            reverse('admin:message-send-all', args=[obj.pk])
        )
