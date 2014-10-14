from django.conf.urls import patterns, url

urlpatterns = patterns('mm.views',
    url(r'^$', 'index',name='index'),
    url(r'^manage/$', 'manage',name='manage'),
    url(r'^community/add/$', 'addcommunity',name='addcommunity'),
    url(r'^community/check/$', 'checkCommunityNumber',name='checkCommunityNumber'),
    url(r'^community/id/(?P<communityId>[^/]+)/$', 'usergroup',name='usergroup'),
    url(r'^goods/add/(?P<communityId>[^/]+)/$', 'addgoods',name='addgoods'),
    url(r'^goods/save/$', 'savegoods',name='savegoods'),
    url(r'^goods/detail/(?P<goodsId>[^/]+)/$', 'detailGoods',name='detailGoods'),
    url(r'^order/community/(?P<communityId>[^/]+)/id/(?P<goodsId>[^/]+)/$', 'order',name='order'),
    url(r'^order/delete/(?P<orderId>[^/]+)/$', 'deleteOrder',name='deleteOrder'),
    url(r'^order/delete/(?P<orderId>[^/]+)/$', 'deleteOrder',name='deleteOrder'),
    url(r'^order/statistics/(?P<goodsId>[^/]+)/$', 'statisticsOrder',name='statisticsOrder'),
)