from django.db import models
from django.contrib.auth.models import User, Group


class Survey(models.Model):
    name = models.CharField(max_length=127)
    active = models.BooleanField(default=False, blank=True)
    group_features = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='group_features')
    group_landmarks = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name='group_landmarks')

    def __str__(self):
        return self.name


class ChoiceGroup(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Choice(models.Model):
    group = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE)
    text = models.CharField(max_length=127)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '%s (%s)' % (self.text, self.group)


class Question(models.Model):
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, default=0)
    TYPE_CHOICES = (
        ('Text', 'Text'),
        ('SingleChoice', 'SingleChoice'),
        ('SingleChoiceOther', 'SingleChoiceOther'),
        ('MultipleChoice', 'MultipleChoice'),
        ('MultipleChoiceOther', 'MultipleChoiceOther'),
        ('Sketch', 'Sketch'),
    )
    type = models.CharField(
        max_length=31,
        choices=TYPE_CHOICES,
        default='Text',
    )
    choices = models.ForeignKey(ChoiceGroup, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return '(%s) %s...' % (self.survey, self.text[:20])

    def get_choices(self):
        return Choice.objects.filter(group=self.choices).order_by('order')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
