#-*- coding: UTF-8 -*-
__author__ = 'chunlei3'

from django import template
from datetime import date, timedelta,datetime
from django.utils.timezone import utc

import __builtin__
import re

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


@register.filter
def groupUrl(number,request):
    return "http://%s.5group.cn%s"  % (number,request.port)

@register.filter
def groupDate(dtime):
    now = datetime.utcnow().replace(tzinfo=utc)
    s = now - dtime
    if s.days > 0 :
        return "%s天前" % (s.days)
    elif s.seconds > 3600:
        return "%s小时前" % (s.seconds/3600)
    else:
        tmp = s.seconds/60
        if tmp ==0 :
            return "刚刚"
        else:
            return "%s分钟前" % (tmp)

