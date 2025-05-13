# app/utils/sentiment_analysis.py
import google.generativeai as genai
from collections import defaultdict, Counter
from ..config import api_key_google_generative


class GeminiSentimentAnalyzer:
    """Utility for sentiment analysis using Google's Gemini API"""
    
    @staticmethod
    def initialize_gemini():
        """Initialize Gemini model"""
        try:
            # Configure Gemini
            genai.configure(api_key=api_key_google_generative)
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model
        except Exception as e:
            print(f"Error initializing Gemini: {str(e)}")
            return None
    
    @staticmethod
    async def analyze_text(text):
        """Analyze sentiment of a single text"""
        if not text or text.strip() == "":
            return {"sentiment": "netral", "score": 0.5}
        
        try:
            # Initialize Gemini model
            model = GeminiSentimentAnalyzer.initialize_gemini()
            if not model:
                return {"sentiment": "netral", "score": 0.5}
            
            # Create prompt for sentiment analysis
            prompt = f"""Analisis sentimen dari ulasan berikut ini:
"{text}"
Kembalikan salah satu dari: positif, negatif, atau netral. Jangan tambahkan teks lain."""
            
            # Call Gemini API
            response = model.generate_content(prompt)
            sentiment = response.text.strip().lower()
            
            # Validate response
            if sentiment not in ["positif", "negatif", "netral"]:
                sentiment = "netral"
                
            # Assign a confidence score (simplified)
            score = 0.8 if sentiment in ["positif", "negatif"] else 0.5
            
            return {"sentiment": sentiment, "score": score}
            
        except Exception as e:
            print(f"Error analyzing sentiment: {str(e)}")
            return {"sentiment": "netral", "score": 0.5}
    
    @staticmethod
    async def analyze_reviews(reviews):
        """Analyze sentiment for multiple reviews"""
        results = []
        
        for review in reviews:
            if not review.get('text'):
                # Skip empty reviews
                continue
                
            # Analyze sentiment
            sentiment_data = await GeminiSentimentAnalyzer.analyze_text(review.get('text', ''))
            
            # Add sentiment data to the review
            review_with_sentiment = {
                **review,
                'sentiment': sentiment_data['sentiment'],
                'sentiment_score': sentiment_data['score']
            }
            
            results.append(review_with_sentiment)
            
        return results
    
    @staticmethod
    async def generate_city_summary(reviews):
        """Generate sentiment summary for a city based on reviews"""
        if not reviews:
            return {
                'stats': {'total': 0, 'positif': 0, 'negatif': 0, 'netral': 0},
                'top_phrases': {'positive': [], 'negative': []}
            }
        
        # Count sentiments
        sentiments = [r.get('sentiment', 'netral') for r in reviews]
        sentiment_counter = Counter(sentiments)
        
        # Collect phrases by sentiment
        positive_phrases = [r.get('text', '').lower() for r in reviews if r.get('sentiment') == 'positif']
        negative_phrases = [r.get('text', '').lower() for r in reviews if r.get('sentiment') == 'negatif']
        
        # Find top phrases
        positive_counter = Counter(positive_phrases)
        negative_counter = Counter(negative_phrases)
        
        top_phrases = {
            'positive': [phrase for phrase, _ in positive_counter.most_common(5)],
            'negative': [phrase for phrase, _ in negative_counter.most_common(5)]
        }
        
        # Create stats summary
        stats = {
            'total': len(reviews),
            'positif': sentiment_counter.get('positif', 0),
            'negatif': sentiment_counter.get('negatif', 0),
            'netral': sentiment_counter.get('netral', 0)
        }
        
        return {
            'stats': stats,
            'top_phrases': top_phrases
        }
    
    @staticmethod
    async def extract_common_sentiments(reviews, limit=5):
        """Extract common sentiment patterns from reviews"""
        if not reviews:
            return []
            
        # Group reviews by sentiment and extract common phrases
        positive_reviews = [r for r in reviews if r.get('sentiment') == 'positif']
        negative_reviews = [r for r in reviews if r.get('sentiment') == 'negatif']
        
        # Extract top phrases (this is simplified - in a real app you'd use NLP techniques)
        top_sentiments = []
        
        # Process positive reviews
        if positive_reviews:
            positive_texts = [r.get('text', '') for r in positive_reviews]
            positive_counter = Counter(positive_texts)
            
            for text, count in positive_counter.most_common(limit):
                if text:  # Skip empty texts
                    percentage = (count / len(positive_reviews)) * 100
                    top_sentiments.append({
                        'text': text,
                        'sentiment': 'positif',
                        'percentage': round(percentage),
                        'count': count
                    })
        
        # Process negative reviews
        if negative_reviews:
            negative_texts = [r.get('text', '') for r in negative_reviews]
            negative_counter = Counter(negative_texts)
            
            for text, count in negative_counter.most_common(limit):
                if text:  # Skip empty texts
                    percentage = (count / len(negative_reviews)) * 100
                    top_sentiments.append({
                        'text': text,
                        'sentiment': 'negatif',
                        'percentage': round(percentage),
                        'count': count
                    })
        
        return sorted(top_sentiments, key=lambda x: x['count'], reverse=True)[:limit]