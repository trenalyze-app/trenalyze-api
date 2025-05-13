from flask import Blueprint, request, jsonify
from app.controllers.scraper_controller import ScraperController
from app.controllers.sentiment_controller import SentimentController
from app.models.search_model import Search

sentiment_bp = Blueprint('sentiment', __name__)
scraper_controller = ScraperController()
sentiment_controller = SentimentController()

@sentiment_bp.route('/analyze', methods=['POST'])
def analyze_sentiment():
    """Endpoint to analyze sentiment for a food item in a specific country"""
    data = request.json
    food_item = data.get('foodItem')
    country = data.get('country')
    
    if not food_item or not country:
        return jsonify({"error": "Food item and country are required"}), 400
    
    # Check if we already have results in the database
    existing_search = Search.find_by_query(food_item, country)
    
    if existing_search and not data.get('refresh'):
        # Return cached results if they exist and refresh is not requested
        return jsonify(existing_search.to_dict()), 200
    
    # Perform new search and analysis
    try:
        # Step 1: Scrape data from Google Maps
        places_data = scraper_controller.scrape_places(food_item, country)
        
        # Step 2: Analyze sentiment
        sentiment_results = sentiment_controller.analyze_places_sentiment(places_data)
        
        # Step 3: Save to database
        search = Search.create_or_update(
            food_item=food_item,
            country=country,
            places_data=places_data,
            sentiment_results=sentiment_results
        )
        
        return jsonify(sentiment_results), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500 