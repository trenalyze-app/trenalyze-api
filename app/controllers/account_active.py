from flask import jsonify, request
from ..databases import UserDatabase, AccountActiveDatabase
from email_validator import validate_email
from ..utils import TokenWebAccountActive, TokenEmailAccountActive
import datetime
from ..task import send_email_task


class AccountActiveController:
    @staticmethod
    async def user_get_verification_email(token):
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
                "by_token_email", token=token, user_id=token_data["user_id"]
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
        created_at = int(request.timestamp.timestamp())
        result = await AccountActiveDatabase.update(
            "active_user_by_token_email",
            user_id=token_data["user_id"],
            token=token,
            created_at=created_at,
        )
        return (
            jsonify(
                {
                    "message": "user has been successfully activated",
                    "data": {
                        "user_id": token_data["user_id"],
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

    @staticmethod
    async def user_verification(email):
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
        created_at = request.timestamp
        expired_at = created_at + datetime.timedelta(minutes=5)
        token_email = await TokenEmailAccountActive.insert(
            f"{user_data.id}", int(created_at.timestamp())
        )
        token_web = await TokenWebAccountActive.insert(
            f"{user_data.id}", int(created_at.timestamp())
        )
        await AccountActiveDatabase.insert(
            user_data.email,
            int(created_at.timestamp()),
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
                        "token": token_web,
                        "created_at": created_at.timestamp(),
                    },
                }
            ),
            201,
        )
