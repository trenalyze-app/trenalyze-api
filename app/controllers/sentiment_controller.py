from app.services.gemini_service import GeminiService
from collections import defaultdict, Counter
import re

class SentimentController:
    def __init__(self):
        self.gemini_service = GeminiService()
    
    def analyze_places_sentiment(self, places):
        """Analyze sentiment for all places and their reviews"""
        
        # Organize reviews by city
        city_reviews = defaultdict(list)
        city_places = defaultdict(list)
        
        for place in places:
            city = place.get('city', 'Unknown')
            city_places[city].append(place)
            
            for review in place.get('reviews', []):
                if review.get('text'):
                    city_reviews[city].append({
                        'place_name': place.get('name'),
                        'text': review.get('text'),
                        'rating': review.get('rating', 0)
                    })
        
        # Analyze sentiment for each review
        city_sentiments = defaultdict(list)
        all_sentiments = []
        review_sentiments = []
        
        for city, reviews in city_reviews.items():
            for review in reviews:
                sentiment = self.gemini_service.analyze_sentiment(review['text'])
                
                review_with_sentiment = {
                    'place_name': review['place_name'],
                    'text': review['text'],
                    'rating': review['rating'],
                    'sentiment': sentiment
                }
                
                city_sentiments[city].append(sentiment)
                all_sentiments.append(sentiment)
                review_sentiments.append(review_with_sentiment)
        
        # Calculate sentiment statistics per city
        city_stats = {}
        for city, sentiments in city_sentiments.items():
            count = Counter(sentiments)
            total = len(sentiments)
            
            if total > 0:
                city_stats[city] = {
                    'total': total,
                    'positive': count.get('positif', 0),
                    'negative': count.get('negatif', 0),
                    'neutral': count.get('netral', 0),
                    'positive_percent': round((count.get('positif', 0) / total) * 100, 1),
                    'negative_percent': round((count.get('negatif', 0) / total) * 100, 1),
                    'neutral_percent': round((count.get('netral', 0) / total) * 100, 1),
                    'dominant_sentiment': max(count.items(), key=lambda x: x[1])[0] if count else 'neutral'
                }
        
        # Find top positive and negative regions
        sentiment_ranking = sorted(
            [(city, stats) for city, stats in city_stats.items()],
            key=lambda x: x[1]['positive_percent'],
            reverse=True
        )
        
        top_positive_regions = sentiment_ranking[:5]
        top_negative_regions = sorted(
            [(city, stats) for city, stats in city_stats.items()],
            key=lambda x: x[1]['negative_percent'],
            reverse=True
        )[:5]
        
        # Find most common positive phrases
        positive_reviews = [r for r in review_sentiments if r['sentiment'] == 'positif']
        positive_reviews_sorted = sorted(positive_reviews, key=lambda x: len(x['text']))
        top_positive_phrases = positive_reviews_sorted[:5] if positive_reviews_sorted else []
        
        # Compile results
        results = {
            'overview': {
                'total_places': len(places),
                'total_reviews': sum(len(p.get('reviews', [])) for p in places),
                'total_cities': len(city_stats),
                'sentiment_distribution': {
                    'positive': all_sentiments.count('positif'),
                    'negative': all_sentiments.count('negatif'),
                    'neutral': all_sentiments.count('netral')
                }
            },
            'cities': city_stats,
            'top_regions': {
                'positive': [
                    {'city': city, 'positive_percent': stats['positive_percent']}
                    for city, stats in top_positive_regions
                ],
                'negative': [
                    {'city': city, 'negative_percent': stats['negative_percent']}
                    for city, stats in top_negative_regions
                ]
            },
            'top_phrases': [
                {
                    'text': phrase['text'],
                    'place_name': phrase['place_name'],
                    'percentage': round((all_sentiments.count('positif') / len(all_sentiments)) * 100 
                                       if len(all_sentiments) > 0 else 0, 1)
                }
                for phrase in top_positive_phrases
            ],
            'geo_data': self._prepare_geo_data(places, city_stats)
        }
        
        return results
    
    def _prepare_geo_data(self, places, city_stats):
        """Prepare geographic data for visualization"""
        geo_features = []
        
        for place in places:
            city = place.get('city', 'Unknown')
            city_sentiment = city_stats.get(city, {}).get('dominant_sentiment', 'neutral')
            sentiment_color = self._get_sentiment_color(city_sentiment)
            
            if place.get('location', {}).get('lat') and place.get('location', {}).get('lng'):
                feature = {
                    'type': 'Feature',
                    'properties': {
                        'name': place.get('name'),
                        'city': city,
                        'sentiment': city_sentiment,
                        'color': sentiment_color,
                        'rating': place.get('rating'),
                        'reviewsCount': place.get('reviewsCount')
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [place.get('location', {}).get('lng'), place.get('location', {}).get('lat')]
                    }
                }
                geo_features.append(feature)
        
        return {
            'type': 'FeatureCollection',
            'features': geo_features
        }
    
    def _get_sentiment_color(self, sentiment):
        """Get color for sentiment visualization"""
        if sentiment == 'positif':
            return 'blue'
        elif sentiment == 'negatif':
            return 'red'
        else:
            return 'gray'
