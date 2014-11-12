__author__ = 'jack'

import re
from models import Community,UserGroupProfile
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render,render_to_response

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
            if hasattr(request,"user")!= None and request.user.is_authenticated():
                cs = UserGroupProfile.objects.filter(user=request.user,community=request.community)
                if len(cs)==0 and (re.search('/community/check/',request.path)==None and re.search('/community/joingroup/',request.path)==None and re.search('/community/join/',request.path)==None):
                    return HttpResponseRedirect(redirect_to=reverse("mm:joingroup"))




