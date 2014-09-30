from django.conf.urls import include, url
from django.contrib import admin
from mm import urls as mmurls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'mmgroup.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include(mmurls)),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
]
