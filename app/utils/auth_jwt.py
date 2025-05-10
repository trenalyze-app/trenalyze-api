from .. import PRIVATE_KEY
import jwt
import datetime


class AuthJwt:
    @staticmethod
    async def generate_jwt(username):
        payload = {"sub": username, "iat": datetime.datetime.utcnow()}
        token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
        return token
