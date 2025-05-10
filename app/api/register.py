from flask import Blueprint, request
from ..controllers import RegisterController

register_router = Blueprint("register_router", __name__)


@register_router.post("/trenalyze/register")
async def user_register():
    data = request.json
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")
    username = data.get("username", "")
    email = data.get("email", "")
    password = data.get("password", "")
    confirm_password = data.get("confirm_password", "")
    return await RegisterController.user_register(
        first_name, last_name, username, email, password, confirm_password
    )
