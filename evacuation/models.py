from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone


class Message(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="", blank=True)
    TYPE_CHOICES = (
        ('Alert', 'Alert'),
        ('Warning', 'Warning'),
        ('Info', 'Info'),
        ('Success', 'Success'),
    )
    type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES,
        default='Alert',
    )
    date_created = models.DateTimeField('date created', auto_now_add=True)
    active = models.BooleanField(default=True, blank=True)
    sent = models.BooleanField(default=False, blank=True)

    action_text = models.CharField(max_length=255, blank=True, null=True)
    action_url = models.CharField(max_length=511, blank=True, null=True)

    ICON_CLASSES = {
        'Alert': 'fa-exclamation-circle bg-danger',
        'Warning': 'fa-warning bg-warning',
        'Info': 'fa-info-circle bg-info',
        'Success': 'fa-check bg-flat-color-5',
    }
    icon_class = ""

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        instance.icon_class = instance.ICON_CLASSES[instance.type]
        return instance

    def __str__(self):
        return '%d - %s' % (self.id, self.title)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    sent_time = models.DateTimeField('sent time', auto_now_add=True)
    read_time = models.DateTimeField('read time', blank=True, null=True)

    def format_time(self):
        if timezone.now().date() == self.sent_time.date():
            return 'Today %s' % self.sent_time.strftime('%I:%M %p')
        if timezone.now().date() - 1 == self.sent_time.date():
            return 'Yesterday %s' % self.sent_time.strftime('%I:%M %p')
        return self.sent_time.strftime('%d-%b %I:%M %p')
