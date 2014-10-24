#-*- coding: UTF-8 -*-

from django.shortcuts import render,render_to_response
from django.contrib.auth.decorators import login_required
from models import Community,UserGroupProfile,Goods,GoodsCategory,Category,CategoryValue,Orders,OrderCategory
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
import json
import os
from uuid import uuid4
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.db import transaction
from utils import isEmpty,combination,CountObj
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as authLogin
import re
from django.conf import settings
import  shutil
# Create your views here.

def index(request):
    communitys = Community.objects.select_related('user').all()
    for x in communitys:
        x.user.socialUser = x.user.social_auth.model.objects.get(user=x.user)
        x.user.groupProfile = UserGroupProfile.objects.get(user=x.user,community=x)
    return render(request, 'index.html', {'request':request,'communitys':communitys})

def login(request):
    return render(request, 'login.html', {'request':request})

def userCheck(request):
    rs = User.objects.filter(username=request.GET['name']).count()
    if rs > 0 :
        return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')
    else:
        return HttpResponse(json.dumps({ "valid": True }),content_type='application/json; charset=utf8')

def userLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            authLogin(request, user)
            return HttpResponseRedirect(redirect_to=reverse("mm:manage"))
        else:
            return HttpResponseRedirect(redirect_to=reverse("mm:index"))
    else:
        return HttpResponseRedirect(redirect_to=reverse("mm:index"))

@login_required(redirect_field_name=None,login_url="/login")
def uploadImage(request):
    uploadfile  = request.FILES['file']
    print
    if uploadfile.size > settings.MAX_FILEUPLOAD_SIZE:
         return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')
    imgPattern = re.compile(r'^image/')
    imgType=re.sub(imgPattern,'',uploadfile.content_type)
    uploadfile.open()
    urlPath = "%s/%s.%s" % (request.user.id,uuid4().hex,imgType)
    try:
        os.makedirs("/www/tmp/%s" % (request.user.id))
    except:
        pass
    with open('/www/tmp/%s' % urlPath,'wb+') as ff:
        for chunk in uploadfile.chunks():
            ff.write(chunk)
    return HttpResponse(json.dumps({ "url": "/media/"+urlPath ,'valid':True}),content_type='application/json; charset=utf8')


@login_required(redirect_field_name=None,login_url="/login")
def userModify(request):
    user = User.objects.get(id=request.user.id)
    user.set_password(request.POST['passwd'])
    user.username = request.POST['name']
    user.save()
    return index(request)

@login_required(redirect_field_name=None,login_url="/login")
@transaction.atomic
def join(request,communityId):
    nick = request.POST['nick']
    code = request.POST['code']

    if Community.objects.filter(id=communityId,code=code).count()==1 and Community.objects.filter(id=communityId,user=request.user).count()==0:
        groupProfile = UserGroupProfile()
        groupProfile.user=request.user
        groupProfile.community=Community(id=communityId)
        groupProfile.nick= nick
        groupProfile.save()
        return HttpResponseRedirect(redirect_to=reverse("mm:manage"))
    return HttpResponseRedirect(redirect_to=reverse("mm:index"))


def checknick(request,communityId):
    rs = UserGroupProfile.objects.filter(community=Community(id=communityId),nick=request.GET['nick']).count()
    if rs > 0 :
        return HttpResponse(json.dumps({ "valid": False }),content_type='application/json; charset=utf8')
    else:
        return HttpResponse(json.dumps({ "valid": True }),content_type='application/json; charset=utf8')

@login_required(redirect_field_name=None,login_url="/login")
def comunityNick(request):
    nick = request.POST['nick']
    id = request.POST['communityId']
    group = UserGroupProfile.objects.filter(user=request.user,community=Community(id=id))[0]
    group.nick= nick
    group.save()
    return HttpResponse(json.dumps({ "valid": True }),content_type='application/json; charset=utf8')

@login_required(redirect_field_name=None,login_url="/login")
def register(request):
    return render(request, 'register.html', {'request':request,'panelTitle':"修改"})

@login_required(redirect_field_name=None,login_url="/login")
def registerNext(request):
    return render(request, 'register.html', {'request':request,'panelTitle':"继续完成注册"})

@login_required(redirect_field_name=None,login_url="/login")
def manage(request):
    if request.session.has_key('is_new') and request.session.pop('is_new') :
        return HttpResponseRedirect(redirect_to=reverse("mm:registerNext"))
    return render(request, 'manage.html', {'request':request})

@login_required(redirect_field_name=None,login_url="/login")
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

@login_required(redirect_field_name=None,login_url="/login")
def usergroup(request,communityId):
    community = Community.objects.get(number=communityId)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user.is_authenticated(),community=community)[0]
    doingGoods = Goods.objects.select_related('community').filter(status=0,community=community);
    historyGoods = Goods.objects.select_related('community').filter(status=1,community=community);
    return render(request, 'community.html', {'request':request,'group':group,"communityId":communityId,"doingGoods":doingGoods,"historyGoods":historyGoods})

@login_required(redirect_field_name=None,login_url="/login")
def addgoods(request,communityId):
    community = Community.objects.get(number=communityId)
    group = UserGroupProfile.objects.select_related('community').filter(user=request.user,community=community)[0]
    return render(request, 'goods-add.html',{'request':request,'group':group,"communityId":communityId})

@login_required(redirect_field_name=None,login_url="/login")
@transaction.atomic
def savegoods(request):
    params = request.POST;
    community = Community.objects.get(number=params["communityId"])
    group = UserGroupProfile.objects.filter(user=request.user,community=community)[0]
    goods = Goods()
    goods.name = params["name"]
    img = re.compile(r'^/media').sub("/image",params["image"])
    fimg = re.compile(r'^/media').sub("",params["image"])
    goods.image = img
    goods.groupProfile = group
    goods.link = params["link"]
    goods.price = float(params["price"])
    goods.offprice = float(params["sale"])
    goods.desc = params['desc']
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
    if re.search('^http://',params["image"]) == None:
        try:
            os.mkdir("")
        except:
            pass
        shutil.move("/www/tmp/"+fimg,"/www/image/"+str(request.user.uid))
    return HttpResponseRedirect(redirect_to=reverse("mm:usergroup",args=[params["communityId"]]))

@login_required(redirect_field_name=None,login_url="/login")
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

@login_required(redirect_field_name=None,login_url="/login")
@transaction.atomic
def order(request,communityId,goodsId):
    params = request.POST;
    gd = Goods.objects.select_related('community','groupProfile').filter(id=goodsId)[0]
    if gd.status == 1 :
        return HttpResponseRedirect(redirect_to=reverse("mm:detailGoods",args=[goodsId]))
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

@login_required(redirect_field_name=None,login_url="/login")
def deleteOrder(request,orderId):
    params = request.POST;
    order = Orders.objects.get(id=orderId)
    if order.goods.status == 1 :
        return HttpResponseRedirect(redirect_to=reverse("mm:detailGoods",args=[order.goods.id]))
    if request.user.id != order.groupProfile.user.id:
         return HttpResponseRedirect(redirect_to=reverse("mm:index"))
    order.delete()
    OrderCategory.objects.filter(order=Orders(id=orderId)).delete()
    return HttpResponseRedirect(redirect_to=reverse("mm:detailGoods",args=[order.goods.id]))

@login_required(redirect_field_name=None,login_url="/login")
def deleteOrderByAdmin(request,orderId):
    order = Orders.objects.get(id=orderId)
    if not (order.goods.community.user.id == request.user.id or order.goods.groupProfile.user.id == request.user.id):
         return HttpResponseRedirect(redirect_to=reverse("mm:index"))
    order.delete()
    OrderCategory.objects.filter(order=Orders(id=orderId)).delete()
    return HttpResponseRedirect(redirect_to=reverse("mm:statisticsOrder",args=[order.goods.id]))


@login_required(redirect_field_name=None,login_url="/login")
def statisticsOrder(request,goodsId):
    params = request.POST
    xValues=params.getlist("x")
    yValues=params.getlist("y")
    if len(xValues)==0:
        xValues = request.session.get("goods_"+str(goodsId),([],[]))[0]
    if len(yValues)==0:
        yValues = request.session.get("goods_"+str(goodsId),([],[]))[1]
    if len(xValues)!=0  or len(yValues)!=0:
        request.session["goods_"+str(goodsId)]=(xValues,yValues)
        request.session.modified = True

    xValues=map(lambda x:int(x),xValues)
    yValues=map(lambda x:int(x),yValues)

    xValues=sorted(xValues)
    yValues=sorted(yValues)

    gd = Goods.objects.get(id=goodsId)
    group = UserGroupProfile.objects.get(user=request.user,community=gd.community)

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

    orderPeople = {}
    for order in orders:
        id = order.groupProfile.user.id
        if not orderPeople.has_key(id):
            orderPeople.setdefault(id,[])
        orderPeople[id].append(order)

    return render(request, 'statistics.html',{'request':request,'group':group,'goods':gd,"categorys":gdCategorys,"xAxis":xAxis,"yAxis":yAxis,'x_axis':xValues,'y_axis':yValues,'hMap':hMap,'count':CountObj(0),'orderByPeople':orderPeople.values()})

@login_required(redirect_field_name=None,login_url="/login")
def modifyOrderNumber(request,orderId):
    order = Orders.objects.get(id=orderId)

    if not (order.goods.community.user.id == request.user.id or order.goods.groupProfile.user.id == request.user.id):
         return HttpResponseRedirect(redirect_to=reverse("mm:index"))
    order.number = request.POST["n"]
    order.save()
    return HttpResponseRedirect(redirect_to=reverse("mm:statisticsOrder",args=[order.goods.id]))


@login_required(redirect_field_name=None,login_url="/login")
def freeze(request,goodsId):
    gd = Goods.objects.get(id=goodsId)
    if gd.community.user.id == request.user.id or gd.groupProfile.user.id == request.user.id:
        gd.status=1
        gd.save()
    return HttpResponseRedirect(redirect_to=reverse("mm:usergroup",args=[gd.community.number]))

def latest(request):
    gd = Goods.objects.all().order_by('time')
    return render(request, 'latest.html', {'request':request,"goods":gd})