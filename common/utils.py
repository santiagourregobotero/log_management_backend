from rest_framework.response import Response
from rest_framework import status
from .exceptions import AuthorizationException
import jwt

def format_serializer_errors(serializer_errors):
    error_list = []
    for field, messages in serializer_errors.items():
        for message in messages:
            error_list.append(f"{field}: {message}")
    if len(error_list) == 1:
        return {"msg": error_list[0]}
    else:
        return {"msg": error_list}


def validate_auth_header(auth_header):
    header_parts = auth_header.split(' ') if auth_header else []

    auth_type = header_parts[0] if len(header_parts) > 0 else ''
    token = header_parts[1] if len(header_parts) > 1 else ''

    if auth_type.lower() != 'bearer':
        raise AuthorizationException("Invalid authentication type. Bearer token expected.")

    if not token:
        raise AuthorizationException("UnAuthorized!")
    
    try:
        payload = jwt.decode(token, 'secret', algorithms="HS256")
        return payload
    except:
        raise AuthorizationException("UnAuthorized!")


def convert_ft_to_ftin_txt(height):
    parts = height.split("/")
    ft = float(parts[0]) if len(parts) > 0 else 0
    inch = float(parts[1]) if len(parts) > 1 else 0
    return f"{ft:.0f} feet {inch:.0f} inch"

def convert_cm_to_ft_in(approx_height):
    if approx_height is None:
        return '-'
    ft = int(approx_height/30.48)
    inch = (approx_height/30.48 - int(approx_height/30.48)) * 12
    return f"{ft:.0f} feet {inch:.0f} inch"
