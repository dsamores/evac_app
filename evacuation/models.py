from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from webpush.models import Group


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

    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)

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
        if timezone.now().date() - timedelta(days=1) == self.sent_time.date():
            return 'Yesterday %s' % self.sent_time.strftime('%I:%M %p')
        return self.sent_time.strftime('%d-%b %I:%M %p')


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=63)
    description = models.TextField(blank=True, null=True)
    page = models.CharField(max_length=127, blank=True, null=True)
    element = models.CharField(max_length=127, blank=True, null=True)
    time = models.DateTimeField()


class Obstacle(models.Model):
    name = models.CharField(max_length=63)
    place_id = models.CharField(max_length=31, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.name


class EvacUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(blank=True, null=True)
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(
        max_length=15,
        choices=GENDERS,
        blank=True, null=True
    )
    building_occupant = models.BooleanField(default=True, blank=True)
    FLOORS = (
        (0, 'Ground floor'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
    )
    floor = models.IntegerField(
        choices=FLOORS,
        blank=True, null=True
    )
    mobility_restriction = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    phone_use = models.CharField(max_length=31, blank=True, null=True)
    seen_tutorial = models.BooleanField(default=False, blank=True)
    PHONE_MAKES = (
        ('Iphone', 'Iphone'),
        ('Android', 'Android'),
        ('Other', 'Other'),
    )
    phone_make = models.CharField(
        max_length=15,
        choices=PHONE_MAKES,
        blank=True, null=True
    )


class Landmark(models.Model):
    name = models.CharField(max_length=63)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.CharField(max_length=63, blank=True, null=True)
