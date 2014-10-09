__author__ = 'chunlei3'

from django import template
from datetime import date, timedelta

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


