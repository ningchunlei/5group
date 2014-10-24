__author__ = 'chunlei3'

import json
from mm.models import Orders,UserGroupProfile
from django.db.models.fields.related import ForeignKey

def isEmpty(params,key):
    if not params.has_key(key):
        return True
    return params[key]==""

def combination(categorys,level):
    if level >= len(categorys):
        return []
    v = categorys[level]
    ret = []
    for gv in v:
        ld = level+1
        callret = combination(categorys,ld)
        for c in callret:
            ret.append(gv.value+"-"+c)
        if len(callret)==0:
            ret.append(gv.value)
    return ret

class CountObj(object):

    def __init__(self,count):
        self.count = count;

    def inc(self):
        self.count = self.count + 1
        return self.count

    def reset(self):
        self.count = 0
        return ""

class StatisticsOrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,Orders):
            return {'id':obj.id,'number':obj.number,'groupProfile':{'nick':obj.groupProfile.nick}}







