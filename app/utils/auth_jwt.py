from .. import PRIVATE_KEY, PUBLIC_KEY
import jwt
import datetime


class AuthJwt:
    @staticmethod
    def generate_jwt(user_id, created_at):
        payload = {
            "sub": user_id,
            "iat": created_at,
        }
        token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
        return token

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
