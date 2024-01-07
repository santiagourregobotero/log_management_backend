from rest_framework.exceptions import AuthenticationFailed as RestAuthenticationFailed

class AuthorizationException(Exception):
    def __init__(self, message, *args):
        super().__init__(*args)
        self.message = message

    def get_message(self):
        return self.message
    

class AuthenticationFailed(RestAuthenticationFailed):
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
