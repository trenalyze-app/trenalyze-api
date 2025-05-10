from ..databases import UserDatabase
from flask import jsonify
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
            errors.setdefault("email", []).append("EMAIL_INVALID")
        if errors:
            return jsonify({"errors": errors}), 400
        if not (user_data := await UserDatabase.get("by_email", email=email)):
            return (
                jsonify(
                    {
                        "message": "failed login",
                        "errors": {"user": ["USER_NOT_FOUND"]},
                    }
                ),
                404,
            )
        if not bcrypt.check_password_hash(user_data[0].password, password):
            return (
                jsonify(
                    {
                        "message": "failed login",
                        "errors": {"password": ["INVALID_PASSWORD"]},
                    }
                ),
                401,
            )
        token = await AuthJwt.generate_jwt(email)
        return (
            jsonify(
                {
                    "message": "success login",
                    "data": {
                        "token": token,
                        "username": user_data[0].username,
                        "email": user_data[0].email,
                        "first_name": user_data[0].first_name,
                        "last_name": user_data[0].last_name,
                        "is_active": user_data[0].is_active,
                        "country": user_data[0].country,
                        "city": user_data[0].city,
                        "postal_code": user_data[0].postal_code,
                        "created_at": user_data[0].created_at,
                        "updated_at": user_data[0].updated_at,
                    },
                }
            ),
            200,
        )
