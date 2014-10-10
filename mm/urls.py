from django.conf.urls import patterns, url

urlpatterns = patterns('mm.views',
    url(r'^$', 'index',name='index'),
    url(r'^manage/$', 'manage',name='manage'),
    url(r'^community/add/$', 'addcommunity',name='addcommunity'),
    url(r'^community/check/$', 'checkCommunityNumber',name='checkCommunityNumber'),
    url(r'^community/id/(?P<communityId>[^/]+)/$', 'usergroup',name='usergroup'),
    url(r'^goods/add/(?P<communityId>[^/]+)/$', 'addgoods',name='addgoods'),
)