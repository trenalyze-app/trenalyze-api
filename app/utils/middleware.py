from functools import wraps
from flask import request, jsonify
from ..utils import AuthJwt
import asyncio
from ..models import UserModel


def jwt_required():
    def decorator(f):
        async def async_handler(*args, **kwargs):
            result = _verify_jwt()
            if isinstance(result, tuple):
                return result
            request.user = result
            return await f(*args, **kwargs)

        def sync_handler(*args, **kwargs):
            result = _verify_jwt()
            if isinstance(result, tuple):
                return result
            request.user = result
            return f(*args, **kwargs)

        @wraps(f)
        def _verify_jwt():
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return jsonify({"message": "missing authorization header"}), 401

            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({"message": "invalid authorization header"}), 401

            token = parts[1]
            payload = AuthJwt.verify_token(token)
            if payload is None:
                return jsonify({"message": "invalid or expired token"}), 401

            user_id = payload.get("sub")
            if not user_id:
                return jsonify({"message": "invalid or expired token"}), 401

            if not (user_data := UserModel.objects(id=user_id).first()):
                return jsonify({"message": "invalid or expired token"}), 401

            if not user_data.is_active:
                return jsonify({"message": "user is not active"}), 401

            return payload

        if asyncio.iscoroutinefunction(f):
            return wraps(f)(async_handler)
        else:
            return wraps(f)(sync_handler)

    return decorator
