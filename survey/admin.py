from django.contrib import admin

from .models import Survey, Question, ChoiceGroup, Choice

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(ChoiceGroup)
admin.site.register(Choice)
