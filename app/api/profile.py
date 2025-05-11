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


@profile_router.patch("/trenalyze/profile/last/name")
@jwt_required()
async def update_last_name():
    data = request.json
    new_last_name = data.get("new_last_name", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_last_name(
        new_last_name, user["sub"], timestamp
    )


@profile_router.patch("/trenalyze/profile/username")
@jwt_required()
async def update_username():
    data = request.json
    new_username = data.get("new_username", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_username(new_username, user["sub"], timestamp)


@profile_router.patch("/trenalyze/profile/bio")
@jwt_required()
async def update_bio():
    data = request.json
    new_bio = data.get("new_bio", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_bio(new_bio, user["sub"], timestamp)


@profile_router.patch("/trenalyze/profile/country")
@jwt_required()
async def update_country():
    data = request.json
    new_country = data.get("new_country", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_country(new_country, user["sub"], timestamp)


@profile_router.patch("/trenalyze/profile/city")
@jwt_required()
async def update_city():
    data = request.json
    new_city = data.get("new_city", "")
    user = request.user
    timestamp = request.timestamp
    return await ProfileController.update_city(new_city, user["sub"], timestamp)
