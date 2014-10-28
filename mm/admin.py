from django.contrib import admin

# Register your models here.

from mm.models import Goods,Community

class GoodsOptions(admin.ModelAdmin):
    list_display = ('id', 'name', 'groupProfile', 'community','status')

class CommunityOptions(admin.ModelAdmin):
    list_display = ('name', 'number')



admin.site.register(Community,CommunityOptions)
admin.site.register(Goods,GoodsOptions)


