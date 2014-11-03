__author__ = 'jack'

import re
from models import Community,UserGroupProfile

class DomainMiddleWare(object):
    def process_request(self, request):
        host = request.get_host()
        host = re.sub(r':.*', '', host)
        community = Community.objects.select_related('user').filter(number=host)
        if len(community)!=0:
            community[0].user.groupProfile = UserGroupProfile.objects.get(user=community[0].user,community=community[0])
            request.community = community[0]


