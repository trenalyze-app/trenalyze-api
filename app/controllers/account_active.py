from flask import jsonify, request
from ..databases import UserDatabase, AccountActiveDatabase
from email_validator import validate_email
from ..utils import TokenWebAccountActive, TokenEmailAccountActive
import datetime
from ..task import send_email_task


class AccountActiveController:
    @staticmethod
    async def user_get_verification_email(token, timestamp):
        errors = {}
        if not isinstance(token, str):
            errors.setdefault("token", []).append("FIELD_TEXT")
        if not token or (isinstance(token, str) and token.isspace()):
            errors.setdefault("token", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (token_data := await TokenEmailAccountActive.get(token)):
            return jsonify(
                {
                    "message": "token not found",
                    "errors": {"token": ["INVALID_TOKEN"]},
                },
                404,
            )
        if not (
            account_active_data := await AccountActiveDatabase.get(
                "by_token_email_user_id", token=token, user_id=token_data["user_id"]
            )
        ):
            return (
                jsonify(
                    {
                        "message": "token not found",
                        "errors": {"token": ["INVALID_TOKEN"]},
                    }
                ),
                404,
            )
        result = await AccountActiveDatabase.update(
            "active_user_by_token_email",
            user_id=token_data["user_id"],
            token=token,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "user has been successfully activated",
                    "data": {
                        "token_email": result.token_email,
                        "token_web": result.token_web,
                        "id": result.id,
                        "created_at": result.created_at,
                        "updated_at": result.updated_at,
                        "expired_at": result.expired_at,
                    },
                    "user": {
                        "id": result.user.id,
                        "first_name": result.user.first_name,
                        "last_name": result.user.last_name,
                        "username": result.user.username,
                        "email": result.user.email,
                        "created_at": result.user.created_at,
                        "updated_at": result.user.updated_at,
                        "is_active": result.user.is_active,
                        "country": result.user.country,
                        "city": result.user.city,
                        "postal_code": result.user.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def user_get_verification_web(token):
        errors = {}
        if not isinstance(token, str):
            errors.setdefault("token", []).append("FIELD_TEXT")
        if not token or (isinstance(token, str) and token.isspace()):
            errors.setdefault("token", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (token_data := await TokenWebAccountActive.get(token)):
            return (
                jsonify(
                    {
                        "message": "token not found",
                        "errors": {"token": ["INVALID_TOKEN"]},
                    }
                ),
                404,
            )
        if not (
            account_active_data := await AccountActiveDatabase.get(
                "by_token_web_user_id", token=token, user_id=token_data["user_id"]
            )
        ):
            return (
                jsonify(
                    {
                        "message": "token not found",
                        "errors": {"token": ["INVALID_TOKEN"]},
                    }
                ),
                404,
            )
        return (
            jsonify(
                {
                    "message": "successfully obtained the information",
                    "data": {
                        "token_web": account_active_data.token_web,
                        "id": account_active_data.id,
                        "created_at": account_active_data.created_at,
                        "updated_at": account_active_data.updated_at,
                        "expired_at": account_active_data.expired_at,
                    },
                    "user": {
                        "id": account_active_data.user.id,
                        "first_name": account_active_data.user.first_name,
                        "last_name": account_active_data.user.last_name,
                        "username": account_active_data.user.username,
                        "email": account_active_data.user.email,
                        "created_at": account_active_data.user.created_at,
                        "updated_at": account_active_data.user.updated_at,
                        "is_active": account_active_data.user.is_active,
                        "country": account_active_data.user.country,
                        "city": account_active_data.user.city,
                        "postal_code": account_active_data.user.postal_code,
                    },
                }
            ),
            200,
        )

    @staticmethod
    async def user_verification(email, timestamp):
        errors = {}
        if not isinstance(email, str):
            errors.setdefault("email", []).append("FIELD_TEXT")
        if not email or (isinstance(email, str) and email.isspace()):
            errors.setdefault("email", []).append("FIELD_REQUIRED")
        try:
            valid = validate_email(email)
            email = valid.email
        except:
            errors.setdefault("email", []).append("INVALID_EMAIL")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (user_data := await UserDatabase.get("by_email", email=email)):
            return (
                jsonify(
                    {
                        "message": "email not found",
                        "errors": {"user": ["USER_NOT_FOUND"]},
                    }
                ),
                404,
            )
        if user_data.is_active:
            return (
                jsonify(
                    {
                        "message": "user has been successfully activated",
                        "errors": {"user": ["USER_ALREADY_ACTIVE"]},
                    }
                ),
                409,
            )
        expired_at = timestamp + datetime.timedelta(minutes=5)
        token_email = await TokenEmailAccountActive.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        token_web = await TokenWebAccountActive.insert(
            f"{user_data.id}", int(timestamp.timestamp())
        )
        result = await AccountActiveDatabase.insert(
            user_data.email,
            int(timestamp.timestamp()),
            int(expired_at.timestamp()),
            token_email,
            token_web,
        )
        send_email_task.apply_async(
            args=[
                "Account Active",
                [user_data.email],
                f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Reset</title>
</head>
<body>
    <p>Hello {user_data.username},</p>
    <p>Someone has requested a link to verify your account, and you can do this through the link below.</p>
    <p>
        <a href="dsadsadsa/account-active?token={token_email}">
            Click here to activate your account
        </a>
    </p>
    <p>If you didn't request this, please ignore this email.</p>
</body>
</html>
                """,
                "account active",
            ],
        )
        return (
            jsonify(
                {
                    "message": "successfully sent email verification",
                    "data": {
                        "token_email": result.token_email,
                        "token_web": result.token_web,
                        "id": result.id,
                        "created_at": result.created_at,
                        "updated_at": result.updated_at,
                        "expired_at": result.expired_at,
                    },
                    "user": {
                        "id": result.user.id,
                        "first_name": result.user.first_name,
                        "last_name": result.user.last_name,
                        "username": result.user.username,
                        "email": result.user.email,
                        "created_at": result.user.created_at,
                        "updated_at": result.user.updated_at,
                        "is_active": result.user.is_active,
                        "country": result.user.country,
                        "city": result.user.city,
                        "postal_code": result.user.postal_code,
                    },
                }
            ),
            201,
        )
