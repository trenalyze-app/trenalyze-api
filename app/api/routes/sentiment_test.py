from flask import Blueprint, jsonify

sentiment_test_bp = Blueprint('sentiment_test', __name__)

@sentiment_test_bp.route('/test', methods=['GET'])
def test_sentiment():
    """Simple test endpoint for sentiment analysis functionality"""
    return jsonify({
        "status": "success",
        "message": "Sentiment analysis API is working",
        "version": "1.0.0"
    }), 200 