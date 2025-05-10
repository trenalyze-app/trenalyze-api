from flask import Blueprint, request
from ..controllers import LoginController

login_router = Blueprint("login_router", __name__)


@login_router.post("/trenalyze/login")
async def user_login():
    data = request.json
    email = data.get("email", "")
    password = data.get("password", "")
    return await LoginController.user_login(email, password)
