from django.conf.urls import patterns, url

urlpatterns = patterns('mm.views',
    url(r'^$', 'index',name='index'),
    url(r'^manage/$', 'manage',name='manage'),
)