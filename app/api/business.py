from flask import Blueprint, request
from ..controllers import BusinessController
from ..utils import jwt_required

business_router = Blueprint("business_router", __name__)


@business_router.get("/trenalyze/compare/trend-chart")
@jwt_required()
async def compare_trend_chart():
    data = request.json
    topic = data.get("topic", [])
    return await BusinessController.compare_trend_chart(topic)


@business_router.get("/trenalyze/compare/maps")
@jwt_required()
async def compare_trend_maps():
    data = request.json
    topic = data.get("topic", [])
    return await BusinessController.compare_trend_maps(topic)
