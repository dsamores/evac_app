from django.contrib import admin

from .models import Survey, Question, ChoiceGroup, Choice

admin.site.register(Survey)
admin.site.register(ChoiceGroup)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'survey', 'order', 'type')
    list_filter = ('survey__name',)

    def display_name(self, obj):
        return '%s%s' % (obj.text[:30], '...' if len(obj.text) > 30 else '')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'group', 'order')
    list_filter = ('group__name',)

    def display_name(self, obj):
        return '%s%s' % (obj.text[:30], '...' if len(obj.text) > 30 else '')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
