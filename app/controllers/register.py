from ..databases import UserDatabase
from flask import jsonify
from email_validator import validate_email


class RegisterController:
    @staticmethod
    async def user_register(
        first_name, last_name, username, email, password, confirm_password
    ):
        from ..bcrypt import bcrypt

        errors = {}
        if not isinstance(first_name, str):
            errors.setdefault("first_name", []).append("FIELD_TEXT")
        if not first_name or (isinstance(first_name, str) and first_name.isspace()):
            errors.setdefault("first_name", []).append("FIELD_REQUIRED")
        if not isinstance(last_name, str):
            errors.setdefault("last_name", []).append("FIELD_TEXT")
        if not last_name or (isinstance(last_name, str) and last_name.isspace()):
            errors.setdefault("last_name", []).append("FIELD_REQUIRED")
        if not isinstance(username, str):
            errors.setdefault("username", []).append("FIELD_TEXT")
        if not username or (isinstance(username, str) and username.isspace()):
            errors.setdefault("username", []).append("FIELD_REQUIRED")
        if not isinstance(email, str):
            errors.setdefault("email", []).append("FIELD_TEXT")
        if not email or (isinstance(email, str) and email.isspace()):
            errors.setdefault("email", []).append("FIELD_REQUIRED")
        if not isinstance(password, str):
            errors.setdefault("password", []).append("FIELD_TEXT")
        if not password or (isinstance(password, str) and password.isspace()):
            errors.setdefault("password", []).append("FIELD_REQUIRED")
        if not isinstance(confirm_password, str):
            errors.setdefault("confirm_password", []).append("FIELD_TEXT")
        if not confirm_password or (
            isinstance(confirm_password, str) and confirm_password.isspace()
        ):
            errors.setdefault("confirm_password", []).append("FIELD_REQUIRED")
        try:
            valid = validate_email(email)
            email = valid.email
        except:
            errors.setdefault("email", []).append("EMAIL_INVALID")
        if password != confirm_password:
            errors.setdefault("confirm_password", []).append("PASSWORD_MISMATCH")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        result_password = bcrypt.generate_password_hash(password).decode("utf-8")
        if user_data := await UserDatabase.get(
            "by_email_username", email=email, username=username
        ):
            return (
                jsonify(
                    {
                        "errors": {"user": ["USER_ALREADY_EXISTS"]},
                        "message": "user already exists",
                    }
                ),
                409,
            )
        await UserDatabase.insert(
            first_name, last_name, username, email, result_password
        )
        return jsonify({"message": "user registered successfully"})
