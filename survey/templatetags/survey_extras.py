from django import template
from survey.models import Survey

register = template.Library()


@register.simple_tag
def is_survey_active(survey_name):
    survey = Survey.objects.get(name=survey_name)
    return survey.active
