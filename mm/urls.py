from django.conf.urls import patterns, url

urlpatterns = patterns('mm.views',
    url(r'^hello$', 'hello',name='hello'),
)