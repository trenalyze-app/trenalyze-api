from ..databases import UserDatabase
from flask import jsonify, request
from ..utils import AuthJwt
from email_validator import validate_email


class LoginController:
    @staticmethod
    async def user_login(email, password):
        from ..bcrypt import bcrypt

        errors = {}
        if not isinstance(email, str):
            errors.setdefault("email", []).append("FIELD_TEXT")
        if not email or (isinstance(email, str) and email.isspace()):
            errors.setdefault("email", []).append("FIELD_REQUIRED")
        if not isinstance(password, str):
            errors.setdefault("password", []).append("FIELD_TEXT")
        if not password or (isinstance(password, str) and password.isspace()):
            errors.setdefault("password", []).append("FIELD_REQUIRED")
        try:
            valid = validate_email(email)
            email = valid.email
        except:
            errors.setdefault("email", []).append("INVALID_EMAIL")
        if errors:
            return jsonify({"errors": errors}), 400
        if not (user_data := await UserDatabase.get("by_email", email=email)):
            return (
                jsonify(
                    {
                        "message": "failed login attempt",
                        "errors": {"user": ["USER_NOT_FOUND"]},
                    }
                ),
                404,
            )
        if not bcrypt.check_password_hash(user_data.password, password):
            return (
                jsonify(
                    {
                        "message": "failed login attempt",
                        "errors": {"password": ["INVALID_PASSWORD"]},
                    }
                ),
                401,
            )
        created_at = int(request.timestamp.timestamp())
        token = AuthJwt.generate_jwt(f"{user_data.id}", created_at)
        return (
            jsonify(
                {
                    "message": "login successful",
                    "data": {
                        "token": token,
                        "username": user_data.username,
                        "email": user_data.email,
                        "first_name": user_data.first_name,
                        "last_name": user_data.last_name,
                        "is_active": user_data.is_active,
                        "country": user_data.country,
                        "city": user_data.city,
                        "postal_code": user_data.postal_code,
                        "created_at": user_data.created_at,
                        "updated_at": user_data.updated_at,
                        "id": f"{user_data.id}",
                    },
                }
            ),
            200,
        )
