from django.template import Library
import datetime

register = Library()

@register.filter(expects_localtime=True)
def parse_date(value):
    try:
        date = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
        return date
    except ValueError:
        return None

@register.filter(expects_localtime=True)
def parse_short_date(value):
    try:
        date = datetime.datetime.strptime(value, '%Y-%m-%d')
        return date
    except ValueError:
        return None
