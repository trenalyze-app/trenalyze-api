from flask import Flask
from app.api.routes.sentiment_test import sentiment_test_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprint
app.register_blueprint(sentiment_test_bp, url_prefix='/api/sentiment')

@app.route('/health')
def health_check():
    return {'status': 'ok'}

@app.route('/')
def index():
    return {'message': 'Trenalyze API testing server is running'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 