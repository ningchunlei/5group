from social.utils import setting_name, module_member
from django.conf import settings
from django.contrib.auth import logout as quit
from models import UserGroupProfile

STORAGE = getattr(settings, setting_name('STORAGE'),
                  'oauthdjango.models.DjangoStorage')

Storage = module_member(STORAGE)

class PermLookupDict(object):
    def __init__(self, user, app_label):
        self.user, self.app_label = user, app_label

    def __repr__(self):
        return str(self.user.get_all_permissions())

    def __getitem__(self, perm_name):
        return self.user.has_perm("%s.%s" % (self.app_label, perm_name))

    def __iter__(self):
        # To fix 'item in perms.someapp' and __getitem__ iteraction we need to
        # define __iter__. See #18979 for details.
        raise TypeError("PermLookupDict is not iterable.")

    def __bool__(self):
        return self.user.has_module_perms(self.app_label)

    def __nonzero__(self):      # Python 2 compatibility
        return type(self).__bool__(self)


class PermWrapper(object):
    def __init__(self, user):
        self.user = user

    def __getitem__(self, app_label):
        return PermLookupDict(self.user, app_label)

    def __iter__(self):
        # I am large, I contain multitudes.
        raise TypeError("PermWrapper is not iterable.")

    def __contains__(self, perm_name):
        """
        Lookup by "someapp" or "someapp.someperm" in perms.
        """
        if '.' not in perm_name:
            # The name refers to module.
            return bool(self[perm_name])
        app_label, perm_name = perm_name.split('.', 1)
        return self[app_label][perm_name]


def auth(request):
    """
    Returns context variables required by apps that use Django's authentication
    system.

    If there is no 'user' attribute in the request, uses AnonymousUser (from
    django.contrib.auth).
    """
    if hasattr(request, 'user') and request.session.has_key("social_auth_last_login_backend"):
        user = request.user
        socialuser = Storage.user.get_social_auth__userid(request.session["social_auth_last_login_backend"],user.id);
    else:
        socialuser = None
    return {
        'socialuser':socialuser,
    }

def userGroupProfile(request):
    groupprofiles = []
    if hasattr(request, 'user') :
        try:
            groupprofiles = UserGroupProfile.objects.select_related('community').filter(user=request.user)
        except:
             groupprofiles = []
    else:
        groupprofiles = []
    return {
     'groupprofiles':groupprofiles
    }

def logout(strategy, *args, **kwargs):
    quit(strategy.request)
