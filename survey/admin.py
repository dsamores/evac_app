from django.contrib import admin

from .models import Survey, Question, ChoiceGroup, Choice

admin.site.register(Survey)
admin.site.register(ChoiceGroup)
admin.site.register(Choice)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'survey', 'order')
    list_filter = ('survey__name',)

    def display_name(self, obj):
        return '%s...' % obj.text[:20]


admin.site.register(Question, QuestionAdmin)
