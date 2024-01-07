from rest_framework.authentication import (
    BaseAuthentication,
    SessionAuthentication,
    get_authorization_header,
)
from users.models import User
from .exceptions import AuthenticationFailed
import jwt

class BearerTokenAuthentication(BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise AuthenticationFailed("Invalid authentication type. Bearer token expected.")

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token)
    
    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, 'secret', algorithms="HS256")
        except:
            raise AuthenticationFailed("UnAuthorized!")
        userId = payload.get('id', None)
        try:
            user = User.objects.get(id=userId)
        except User.DoesNotExist:
            raise AuthenticationFailed("UnAuthorized!")

        return (user, token)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
