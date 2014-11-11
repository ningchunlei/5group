from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('mm.views',
    url(r'^$', 'index',name='index'),
    url(r'^manage[/]*$', 'manage',name='manage'),
    url(r'^community/add[/]*$', 'addcommunity',name='addcommunity'),
    url(r'^community/check[/]*$', 'checkCommunityNumber',name='checkCommunityNumber'),
    url(r'^community/id/(?P<communityId>[^/]+)[/]*$', 'usergroup',name='usergroup'),
    url(r'^goods/add/(?P<communityId>[^/]+)[/]*$', 'addgoods',name='addgoods'),
    url(r'^goods/save[/]*$', 'savegoods',name='savegoods'),
    url(r'^goods/detail/(?P<goodsId>[^/]+)[/]*$', 'detailGoods',name='detailGoods'),
    url(r'^order/community/(?P<communityId>[^/]+)/id/(?P<goodsId>[^/]+)[/]*$', 'order',name='order'),
    url(r'^order/delete/(?P<orderId>[^/]+)[/]*$', 'deleteOrder',name='deleteOrder'),
    url(r'^order/mdelete/(?P<orderId>[^/]+)[/]*$', 'deleteOrderByAdmin',name='deleteOrderByAdmin'),
    url(r'^order/modifynum/(?P<orderId>[^/]+)[/]*$', 'modifyOrderNumber',name='modifyOrderNumber'),
    url(r'^order/statistics/(?P<goodsId>[^/]+)[/]*$', 'statisticsOrder',name='statisticsOrder'),
    url(r'^community/check/(?P<communityId>[^/]+)[/]*$', 'checknick',name='checknick'),
    url(r'^community/join/(?P<communityId>[^/]+)[/]*$', 'join',name='join'),
    url(r'^community/modify/nick[/]*$', 'comunityNick',name='comunityNick'),
    url(r'^login[/]*$', 'login',name='login'),
    url(r'^user/check[/]*$', 'userCheck',name='userCheck'),
    url(r'^user/modify[/]*$', 'userModify',name='userModify'),
    url(r'^user/register[/]*$', 'register',name='register'),
    url(r'^user/register/next[/]*$', 'registerNext',name='registerNext'),
    url(r'^user/login[/]*$', 'userLogin',name='userLogin'),
    url(r'^upload/image[/]*$', 'uploadImage',name='uploadImage'),
    url(r'^freeze/(?P<goodsId>[^/]+)[/]*$', 'freeze',name='freeze'),
    url(r'^goods/delete/(?P<goodsId>[^/]+)[/]*$', 'deleteGoods',name='deleteGoods'),
    url(r'^latest[/]*$', 'latest',name='latest'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )