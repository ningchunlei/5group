from django.db import models
from django.contrib import auth
from django.conf import settings


class Community(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=100)
    service = models.IntegerField(default=0)
    code = models.CharField(max_length=100)
    number = models.CharField(max_length=100,default="",unique=True)
    time = models.DateTimeField(auto_now=True)


class UserGroupProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    community = models.ForeignKey(Community)
    nick = models.CharField(max_length=60,unique=True)
    time = models.DateTimeField(auto_now=True)

class Goods(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    link = models.CharField(max_length=100,default="")
    paylink = models.CharField(max_length=100,default="")
    offprice = models.FloatField()
    price = models.FloatField()
    groupProfile = models.ForeignKey(UserGroupProfile)
    community = models.ForeignKey(Community,default=0)
    time = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=0)

class Category(models.Model):
    name = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

class GoodsCategory(models.Model):
    product = models.ForeignKey(Goods)
    category = models.ForeignKey(Category)
    time = models.DateTimeField(auto_now=True)

class CategoryValue(models.Model):
    value = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    time = models.DateTimeField(auto_now=True)


class Orders(models.Model):
    groupProfile = models.ForeignKey(UserGroupProfile)
    goods = models.ForeignKey(Goods)
    number = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)

class OrderCategory(models.Model):
    order = models.ForeignKey(Orders)
    categoryValue = models.ForeignKey(CategoryValue)
    time = models.DateTimeField(auto_now=True)