from flask import jsonify
from ..databases import UserDatabase


class ProfileController:
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
