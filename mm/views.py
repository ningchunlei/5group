#-*- coding: UTF-8 -*-

from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from models import Community
from django.http import HttpResponse,HttpResponseBadRequest
import json
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
# Create your views here.



def index(request):
    return render(request, 'index.html', {'request':request})

@login_required(redirect_field_name=None,login_url="/")
def manage(request):
    return render(request, 'manage.html', {'request':request})

@login_required(redirect_field_name=None,login_url="/")
@require_POST
@csrf_protect
def addcommunity(request):
    if request.POST.has_key("community") and request.POST.has_key("number") :
        rs = Community.objects.filter(name=request.POST["community"],number=request.POST["number"]).count()
        if rs > 0 :
            return HttpResponse(json.dumps({ "valid": False }))
        community = Community()
        community.user = request.user
        community.code = uuid4().hex
        community.number = request.POST["number"]
        community.name = request.POST["community"]
        community.save()
        manage(request)
    else:
        return HttpResponseBadRequest()

def checkCommunityNumber(request):
    rs = Community.objects.filter(number=request.GET["number"]).count()
    if rs > 0:
        return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')
    return HttpResponse(json.dumps({ "valid": True }),content_type='application/json; charset=utf8')



