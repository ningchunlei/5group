#-*- coding: UTF-8 -*-

from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from models import Community,UserGroupProfile,Goods,GoodsCategory,Category,CategoryValue
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import json
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.db import transaction
from utils import isEmpty
# Create your views here.



def index(request):
    return render(request, 'index.html', {'request':request})

@login_required(redirect_field_name=None,login_url="/")
def manage(request):
    return render(request, 'manage.html', {'request':request})

@login_required(redirect_field_name=None,login_url="/")
@require_POST
@csrf_protect
@transaction.atomic
def addcommunity(request):
    if not isEmpty(request.POST,"community") and not isEmpty(request.POST,"number") and not isEmpty(request.POST,"nick") :
        rs = Community.objects.filter(name=request.POST["community"],number=request.POST["number"]).count()
        if rs > 0 :
            return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')

        community = Community()
        community.user = request.user
        community.code = uuid4().hex
        community.number = request.POST["number"]
        community.name = request.POST["community"]
        community.save()

        groupProfile = UserGroupProfile()
        groupProfile.user=request.user
        groupProfile.community=community
        groupProfile.nick= request.POST["nick"]
        groupProfile.save()
        return HttpResponseRedirect(redirect_to="/manage")
    else:
        return HttpResponseBadRequest()

def checkCommunityNumber(request):
    rs = Community.objects.filter(number=request.GET["number"]).count()
    if rs > 0:
        return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')
    return HttpResponse(json.dumps({ "valid": True }),content_type='application/json; charset=utf8')

def usergroup(request,communityId):
    community = Community.objects.get(number=communityId)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=community)[0]
    return render(request, 'community.html', {'request':request,'group':group})

def addgoods(request,communityId):
    community = Community.objects.get(number=communityId)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=community)[0]
    return render(request, 'goods-add.html',{'request':request,'group':group})

def savegoods(request):
    params = request.POST;
    goods = Goods()



