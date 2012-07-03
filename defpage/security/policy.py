import datetime
from zope.interface import implementer
from pyramid.interfaces import IAuthenticationPolicy
from defpage.security.session import authenticated_sessions
from defpage.security.config import system_params

@implementer(IAuthenticationPolicy)
class AuthenticationPolicy(object):

    max_age = 86400

    def __init__(self):
        self.cookie_name = system_params.auth_session_cookie_name

    def _get_cookies(self, request, value):
        headers = []
        later = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(self.max_age))
        expires = later.strftime('%a, %d %b %Y %H:%M:%S GMT')
        headers.append(('Set-Cookie', '%s="%s"; Path=/; Domain=%s; Max-Age=%s; Expires=%s' %
                        (self.cookie_name,
                         value,
                         system_params.common_cookies_domain,
                         self.max_age,
                         expires)))
        return headers

    def authenticated_userid(self, request):
        session_id = request.cookies.get(self.cookie_name)
        if session_id:
            session = authenticated_sessions.get(session_id)
            if session:
                return session['user_id']

    def unauthenticated_userid(self, request):
        return None

    def effective_principals(self, request):
        return [self.authenticated_userid(request)]

    def remember(self, request, principal, email):
        session_id = authenticated_sessions.create(principal, email)
        return self._get_cookies(request, session_id)

    def forget(self, request):
        session_id = request.cookies.get(self.cookie_name)
        if session_id:
            authenticated_sessions.delete(session_id)
            return self._get_cookies(request, '')
