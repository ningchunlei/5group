import json

from social.utils import parse_qs
from social.backends.oauth import BaseOAuth2
from social.utils import setting_name, module_member
from social.exceptions import MissingBackend
from social.strategies.utils import get_strategy
from social.backends.utils import get_backend
from django.conf import settings


class QQOAuth2(BaseOAuth2):
    name = 'qq'
    ID_KEY = 'openid'
    AUTHORIZE_URL = 'http://graph.qq.com/oauth2.0/authorize'
    ACCESS_TOKEN_URL = 'http://graph.qq.com/oauth2.0/token'
    AUTHORIZATION_URL = 'http://graph.qq.com/oauth2.0/authorize'
    OPENID_URL = 'http://graph.qq.com/oauth2.0/me'
    REDIRECT_STATE = False
    EXTRA_DATA = [
        ('nickname', 'username'),
        ('figureurl_qq_1', 'profile_image_url'),
        ('gender', 'gender')
    ]

    STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social.strategies.django_strategy.DjangoStrategy')

    Strategy = module_member(STRATEGY)

    STORAGE = getattr(settings, setting_name('STORAGE'),
                  'oauthdjango.models.DjangoStorage')

    Storage = module_member(STORAGE)

    def __init__(self, strategy=None, redirect_uri=None):
         request = None
         if strategy != None:
             redirect_uri = strategy.request.build_absolute_uri(redirect_uri)
             request = strategy.request
         super(QQOAuth2,self).__init__(QQOAuth2.Strategy(QQOAuth2.Storage(),request=request),redirect_uri)

    def get_user_details(self, response):
        return {
            'username': response.get('nickname', '')
        }

    def get_openid(self, access_token):
        response = self.request(self.OPENID_URL, params={
            'access_token': access_token
        })
        data = json.loads(response.content[10:-3])
        return data['openid']

    def user_data(self, access_token, *args, **kwargs):
        openid = self.get_openid(access_token)
        response = self.get_json(
            'http://graph.qq.com/user/get_user_info', params={
                'access_token': access_token,
                'oauth_consumer_key': self.setting('SOCIAL_AUTH_QQ_KEY'),
                'openid': openid
            }
        )
        response['openid'] = openid
        return response

    def request_access_token(self, url, data, *args, **kwargs):
        response = self.request(url, params=data, *args, **kwargs)
        return parse_qs(response.content)

