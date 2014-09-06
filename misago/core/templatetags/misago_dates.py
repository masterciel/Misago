from django import template
from django.conf import settings
from django.template.defaultfilters import date as dj_date
from django.utils import timezone


register = template.Library()


@register.filter
def compact_date(value):
    if value.year == timezone.now().year:
        return dj_date(value, settings.MISAGO_COMPACT_DATE_DAY_MONTH)
    else:
        return dj_date(value, settings.MISAGO_COMPACT_DATE_DAY_MONTH_YEAR)
