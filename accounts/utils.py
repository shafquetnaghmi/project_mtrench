from datetime import datetime, timedelta
from django.conf import settings
from jwt import encode, decode

def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION),
        'iat': datetime.utcnow(),
    }
    return encode(payload, settings.SECRET_KEY, algorithm='HS256')

def decode_access_token(access_token):
    try:
        payload = decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except Exception:
        return None
