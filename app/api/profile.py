from flask import Blueprint, request
from ..utils import jwt_required
from ..controllers import ProfileController

profile_router = Blueprint("profile_router", __name__)


@profile_router.patch("/trenalyze/profile/first/name")
@jwt_required()
async def update_first_name():
    data = request.json
    new_first_name = data.get("new_first_name", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_first_name(
        new_first_name, user["sub"], timestamp
    )
