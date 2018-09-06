from django import template
from survey.models import Survey

register = template.Library()


@register.simple_tag
def is_survey_active(user):
    groups = user.groups.all()
    survey = Survey.objects.filter(group_features__in=groups, group_landmarks__in=groups, active=True)
    return True if survey else False
