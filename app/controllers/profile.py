from flask import jsonify
from ..databases import UserDatabase
import mongoengine as me
import pycountry


class ProfileController:
    @staticmethod
    async def update_city(new_city, user_id, timestamp):
        errors = {}
        if not isinstance(new_city, str):
            errors.setdefault("new_city", []).append("FIELD_TEXT")
        if not new_city or (isinstance(new_city, str) and new_city.isspace()):
            errors.setdefault("new_city", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        result = await UserDatabase.update(
            "city_by_user_id",
            user_id=user_id,
            new_city=new_city,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "successfully updated the last name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_country(new_country, user_id, timestamp):
        errors = {}
        if not isinstance(new_country, str):
            errors.setdefault("new_country", []).append("FIELD_TEXT")
        if not new_country or (isinstance(new_country, str) and new_country.isspace()):
            errors.setdefault("new_country", []).append("FIELD_REQUIRED")
        try:
            country = pycountry.countries.lookup(new_country)
        except LookupError:
            errors.setdefault("new_country", []).append("INVALID_COUNTRY")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        result = await UserDatabase.update(
            "country_by_user_id",
            user_id=user_id,
            new_country=new_country,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "successfully updated the last name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_bio(new_bio, user_id, timestamp):
        errors = {}
        if not isinstance(new_bio, str):
            errors.setdefault("new_bio", []).append("FIELD_TEXT")
        if not new_bio or (isinstance(new_bio, str) and new_bio.isspace()):
            errors.setdefault("new_bio", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        result = await UserDatabase.update(
            "bio_by_user_id",
            user_id=user_id,
            new_bio=new_bio,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "successfully updated the last name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_username(new_username, user_id, timestamp):
        errors = {}
        if not isinstance(new_username, str):
            errors.setdefault("new_username", []).append("FIELD_TEXT")
        if not new_username or (
            isinstance(new_username, str) and new_username.isspace()
        ):
            errors.setdefault("new_username", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        try:
            result = await UserDatabase.update(
                "username_by_user_id",
                user_id=user_id,
                new_username=new_username,
                created_at=int(timestamp.timestamp()),
            )
        except me.NotUniqueError:
            return (
                jsonify(
                    {
                        "message": "username already exists",
                        "errors": {"username": ["USERNAME_ALREADY_EXISTS"]},
                    }
                ),
                409,
            )
        return (
            jsonify(
                {
                    "message": "successfully updated the last name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_last_name(new_last_name, user_id, timestamp):
        errors = {}
        if not isinstance(new_last_name, str):
            errors.setdefault("new_last_name", []).append("FIELD_TEXT")
        if not new_last_name or (
            isinstance(new_last_name, str) and new_last_name.isspace()
        ):
            errors.setdefault("new_last_name", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        result = await UserDatabase.update(
            "last_name_by_user_id",
            user_id=user_id,
            new_last_name=new_last_name,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "successfully updated the last name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )

    @staticmethod
    async def update_first_name(new_first_name, user_id, timestamp):
        errors = {}
        if not isinstance(new_first_name, str):
            errors.setdefault("new_first_name", []).append("FIELD_TEXT")
        if not new_first_name or (
            isinstance(new_first_name, str) and new_first_name.isspace()
        ):
            errors.setdefault("new_first_name", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user_id)):
            return jsonify({"message": "invalid or expired token"}), 401
        result = await UserDatabase.update(
            "first_name_by_user_id",
            user_id=user_id,
            new_first_name=new_first_name,
            created_at=int(timestamp.timestamp()),
        )
        return (
            jsonify(
                {
                    "message": "successfully updated the first name",
                    "data": {
                        "id": result.id,
                        "first_name": result.first_name,
                        "created_at": result.created_at,
                        "updated_at": int(timestamp.timestamp()),
                        "username": result.username,
                        "last_name": result.last_name,
                        "city": result.city,
                        "country": result.country,
                        "is_active": result.is_active,
                        "postal_code": result.postal_code,
                    },
                }
            ),
            201,
        )
