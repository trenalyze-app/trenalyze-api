from flask import jsonify, request
from ..utils import GoogleTrends
from ..databases import UserDatabase
from ..task import send_email_task


class BusinessController:
    @staticmethod
    async def compare_trend_maps(topic):
        errors = {}
        if not isinstance(topic, list):
            errors.setdefault("topic", []).append("FIELD_LIST")
        if not topic:
            errors.setdefault("topic", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        user = request.user
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user["sub"])):
            return jsonify({"message": "invalid or expired token"}), 401
        topic = [i for i in topic if i]
        topic = ", ".join(topic)
        result = await GoogleTrends.get_maps(topic)
        response = {"message": "successfully obtained the information", "data": {}}
        if len(topic) > 1:
            response["data"]["compared_breakdown_by_region"] = result[
                "compared_breakdown_by_region"
            ]
        else:
            response["data"]["interest_by_region"] = result["interest_by_region"]
        return (
            jsonify(response),
            200,
        )

    @staticmethod
    async def compare_trend_chart(topic):
        errors = {}
        if not isinstance(topic, list):
            errors.setdefault("topic", []).append("FIELD_LIST")
        if not topic:
            errors.setdefault("topic", []).append("FIELD_REQUIRED")
        if errors:
            return jsonify({"errors": errors, "message": "invalid data"}), 400
        user = request.user
        if not (data_user := await UserDatabase.get("by_user_id", user_id=user["sub"])):
            return jsonify({"message": "invalid or expired token"}), 401
        topic = ", ".join(topic)
        result = await GoogleTrends.get_trends(topic)
        response = {"message": "successfully obtained the information", "data": {}}
        if "interest_over_time" not in result:
            return (
                jsonify(
                    {
                        "message": "topic not found",
                        "errors": {"topic": ["TOPIC_NOT_FOUND"]},
                    }
                ),
                404,
            )
        response["data"]["timeline_data"] = result["interest_over_time"][
            "timeline_data"
        ]
        if "averages" in result["interest_over_time"]:
            response["data"]["averages"] = result["interest_over_time"]["averages"]
        return (
            jsonify(response),
            200,
        )
