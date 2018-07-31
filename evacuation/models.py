from django.db import models


class Notification(models.Model):
    text = models.TextField()
    type = models.CharField(max_length=20)
    date = models.DateTimeField('date sent')
