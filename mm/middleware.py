__author__ = 'jack'

import re
from models import Community,UserGroupProfile
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.redirects.middleware import RedirectFallbackMiddleware

class DomainMiddleWare(object):
    def process_request(self, request):
        host = request.get_host()
        match = re.search(':\d*',host)
        if match:
            request.port = match.group()
        else:
            request.port= ""
        host = re.sub(r'\..*', '', host)
        community = Community.objects.select_related('user').filter(number=host)
        if len(community)!=0:
            community[0].user.groupProfile = UserGroupProfile.objects.get(user=community[0].user,community=community[0])
            request.community = community[0]

    def process_response(self, request, response):
        if hasattr(request,"comunity") and request.user.is_authenticated():
            cs = UserGroupProfile.objects.get(user=request.user,community=request.comunity)
            if len(cs)==0:
                return HttpResponseRedirect(redirect_to=reverse('mm:join'))

        return response



