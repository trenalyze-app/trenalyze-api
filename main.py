from flask import Flask
from app.api.routes.sentiment_routes import sentiment_bp
from flask_cors import CORS
import os

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Register blueprints
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
    
    # Load environment variables
    app.config['APIFY_API_KEY'] = os.environ.get('APIFY_API_KEY', 'your_apify_api_key')
    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', 'your_gemini_api_key')
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    
    @app.route('/health')
    def health_check():
        return {'status': 'ok'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 