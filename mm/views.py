#-*- coding: UTF-8 -*-

from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from models import Community,UserGroupProfile,Goods,GoodsCategory,Category,CategoryValue,Orders,OrderCategory
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import json
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.db import transaction
from utils import isEmpty,combination,CountObj
from django.core.urlresolvers import reverse
import re
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
    doingGoods = Goods.objects.select_related('community').filter(status=0,community=community);
    historyGoods = Goods.objects.select_related('community').filter(status=1,community=community);
    return render(request, 'community.html', {'request':request,'group':group,"communityId":communityId,"doingGoods":doingGoods,"historyGoods":historyGoods})

def addgoods(request,communityId):
    community = Community.objects.get(number=communityId)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=community)[0]
    return render(request, 'goods-add.html',{'request':request,'group':group,"communityId":communityId})

@transaction.atomic
def savegoods(request):
    params = request.POST;
    community = Community.objects.get(number=params["communityId"])
    group = UserGroupProfile.objects.filter(user=request.user,community=community)[0]
    goods = Goods()
    goods.name = params["name"]
    goods.image = params["image"]
    goods.groupProfile = group
    goods.link = params["link"]
    goods.price = float(params["price"])
    goods.offprice = float(params["sale"])
    goods.community = community
    goods.save()
    indexs = params.getlist("categoryIndex")
    for index in indexs:
        category = Category()
        category.name = params["categoryName"+index]
        category.save()
        cvs = params.getlist("categoryValue"+index+"[]")
        for cvp in cvs:
            cv = CategoryValue()
            cv.category = category
            cv.value = cvp
            cv.save()
        gc = GoodsCategory()
        gc.category = category
        gc.product = goods
        gc.save()
    return HttpResponseRedirect(redirect_to=reverse("mm:usergroup",args=[params["communityId"]]))

def detailGoods(request,goodsId):
    params = request.POST;
    gd = Goods.objects.select_related('community','groupProfile').filter(id=goodsId)[0]
    gdCategorys = GoodsCategory.objects.select_related('category').filter(product=gd)
    for gdc in gdCategorys:
        gdc.categoryValues = CategoryValue.objects.filter(category=gdc.category)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=gd.community)[0]
    orders = Orders.objects.select_related('goods').filter(goods=Goods(id=goodsId))
    for order in orders :
        order.categorys = OrderCategory.objects.select_related('categoryValue').filter(order=order)
    return render(request, 'detail.html',{'request':request,'group':group,'goods':gd,"categorys":gdCategorys,'orderGoods':orders})

@transaction.atomic
def order(request,communityId,goodsId):
    params = request.POST;
    gd = Goods.objects.select_related('community','groupProfile').filter(id=goodsId)[0]
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=gd.community)[0]
    order = Orders()
    order.groupProfile=group
    order.goods=Goods(id=goodsId)
    order.number=int(params["number"])
    order.save()

    gdCategorys = GoodsCategory.objects.select_related('category').filter(product=order.goods)
    for gdc in gdCategorys:
        oc = OrderCategory();
        oc.order=order
        oc.categoryValue = CategoryValue(id=int(params["ct"+str(gdc.category.id)]))
        oc.save()

    return HttpResponseRedirect(redirect_to=reverse("mm:detailGoods",args=[goodsId]))


def deleteOrder(request,orderId):
    params = request.POST;
    order = Orders.objects.get(id=orderId)
    order.delete()
    OrderCategory.objects.filter(order=Orders(id=orderId)).delete()
    return HttpResponseRedirect(redirect_to=reverse("mm:detailGoods",args=[order.goods.id]))

def statisticsOrder(request,goodsId):
    params = request.POST
    xValues=params.getlist("x")
    yValues=params.getlist("y")
    xValues=map(lambda x:int(x),xValues)
    yValues=map(lambda x:int(x),yValues)

    xValues=sorted(xValues)
    yValues=sorted(yValues)

    orders = Orders.objects.select_related('goods','groupProfile').filter(goods=Goods(id=goodsId))
    hMap = {}
    p = re.compile(r'^-')
    for order in orders :
        order.categorys = OrderCategory.objects.select_related('categoryValue').filter(order=order)
        xv = ""
        for x in xValues:
            for oc in order.categorys:
                if int(x) == oc.categoryValue.category.id:
                    xv = xv+"-"+oc.categoryValue.value
        yv= ""
        for y in yValues:
            for oc in order.categorys:
                if int(y) == oc.categoryValue.category.id:
                    yv = yv + "-" + oc.categoryValue.value

        xv = p.sub("",xv)
        yv = p.sub("",yv)
        if not hMap.has_key(yv):
            hMap.setdefault(yv,{})
        if not hMap[yv].has_key(xv):
            hMap[yv].setdefault(xv,[])
        hMap[yv][xv].append(order)

    xCategory=[]
    yCategory=[]
    gdCategorys = GoodsCategory.objects.select_related('category').filter(product=Goods(id=goodsId)).order_by('category')
    for gdc in gdCategorys:
        gdc.categoryValues = CategoryValue.objects.filter(category=gdc.category)
        if gdc.category.id in xValues:
            xCategory.append(gdc.categoryValues)
        if gdc.category.id in yValues:
            yCategory.append(gdc.categoryValues)

    xAxis = combination(xCategory,0);
    yAxis = combination(yCategory,0)

    gd = Goods.objects.get(id=goodsId)

    return render(request, 'statistics.html',{'request':request,'group':gd.groupProfile,'goods':gd,"categorys":gdCategorys,"xAxis":xAxis,"yAxis":yAxis,'x_axis':xValues,'y_axis':yValues,'hMap':hMap,'count':CountObj(0)})



