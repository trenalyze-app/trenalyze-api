from ..databases import UserDatabase, AccountActiveDatabase
from flask import jsonify, request
from ..utils import AuthJwt, TokenEmailAccountActive, TokenWebAccountActive, SendEmail
from email_validator import validate_email
import datetime


class LoginController:
    @staticmethod
    async def user_login(email, password, timestamp):
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
        if not user_data.is_active:
            expired_at = timestamp + datetime.timedelta(minutes=5)
            token_email = await TokenEmailAccountActive.insert(
                f"{user_data.id}", int(timestamp.timestamp())
            )
            token_web = await TokenWebAccountActive.insert(
                f"{user_data.id}", int(timestamp.timestamp())
            )
            await AccountActiveDatabase.insert(
                user_data.email,
                int(timestamp.timestamp()),
                int(expired_at.timestamp()),
                token_email,
                token_web,
            )
            SendEmail.send_email_verification(user_data, token_email)
            return (
                jsonify(
                    {
                        "message": "failed login attempt",
                        "errors": {"user": ["USER_INACTIVE"]},
                        "user": {
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
                        "token": None,
                    }
                ),
                403,
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
                    "user": {
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
                    "token": {"web_token": None, "access_token": token},
                }
            ),
            200,
        )
