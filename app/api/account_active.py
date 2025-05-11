from flask import Blueprint, request
from ..controllers import AccountActiveController

account_active_router = Blueprint("account_active_router", __name__)


@account_active_router.post("/trenalyze/verification")
async def verification_email():
    data = request.json
    email = data.get("email", "")
    return await AccountActiveController.user_verification(email)


@account_active_router.get("/trenalyze/verification/web")
async def get_verification_web():
    args = request.args
    token = args.get("token", "")
    return await AccountActiveController.user_get_verification_web(token)


@account_active_router.get("/trenalyze/verification/email")
async def get_verification_email():
    args = request.args
    token = args.get("token", "")
    return await AccountActiveController.user_get_verification_email(token)
