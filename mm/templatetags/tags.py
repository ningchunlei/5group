__author__ = 'chunlei3'

from django import template
from datetime import date, timedelta
import __builtin__

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary == None:
        return None
    if not dictionary.has_key(key):
        return None
    return dictionary.get(key)

@register.filter
def item_in(array, key):
    return key in array

@register.filter
def inc(count):
    return count+1


@register.filter
def orderlen(obj):
    if obj == None :
        return 0
    count = 0;
    for x in obj:
        count = count + x.number
    return count

@register.filter
def totalPrice(obj):
    if obj == None :
        return 0
    count = 0.0;
    for x in obj:
        count = count + x.goods.offprice*x.number
    return count

@register.filter
def nick(obj):
    if obj == None  or len(obj)==0:
        return ""
    return obj[0].groupProfile.nick

