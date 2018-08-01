from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default="")
    TYPE_CHOICES = (
        ('Alert', 'Alert'),
        ('Warning', 'Warning'),
        ('Info', 'Info'),
        ('Success', 'Success'),
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='Alert',
    )
    date = models.DateTimeField('date sent', auto_now_add=True)
    read = models.BooleanField(default=False)
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
        return '%s (%s)' % (self.title, self.date)
