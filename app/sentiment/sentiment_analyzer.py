import os
from typing import Dict, List
from collections import defaultdict, Counter
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDXTfL66pIcMaX0MHui5wIKE4lokXVeG2Y")
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-1.5-flash")

def analyze_sentiment(places_data: List[Dict]) -> Dict:
    region_reviews = defaultdict(list)
    review_sentiments = []
    region_sentiments = defaultdict(list)
    
    for place in places_data:
        region = place.get('region', 'Unknown')
        for review in place.get('reviews', []):
            if review.get('text'):
                region_reviews[region].append({
                    'place_name': place.get('name'),
                    'text': review.get('text'),
                    'rating': review.get('rating', 0)
                })
    
    for region, reviews in region_reviews.items():
        for review in reviews:
            sentiment = _analyze_review_sentiment(review['text'])
            
            review_with_sentiment = {
                'place_name': review['place_name'],
                'text': review['text'],
                'rating': review['rating'],
                'sentiment': sentiment
            }
            
            region_sentiments[region].append(sentiment)
            review_sentiments.append(review_with_sentiment)
    
    region_stats = _calculate_region_stats(region_sentiments)
    
    results = {
        'regions': region_stats,
        'review_sentiments': review_sentiments
    }
    return results

def _analyze_review_sentiment(text: str) -> str:
    if not text or len(text.strip()) < 3:
        return "netral"
    
    prompt = f"""Analisis sentimen dari ulasan berikut ini:
"{text}"
Kembalikan salah satu dari: positif, negatif, atau netral. Jangan tambahkan teks lain."""
    
    try:
        response = MODEL.generate_content(prompt)
        sentiment = response.text.strip().lower()
        
        if sentiment not in ["positif", "negatif", "netral"]:
            return "netral"
        
        return sentiment
    except Exception as e:
        print(f"Error dalam analisis sentimen: {str(e)}")
        return "netral"

def _calculate_region_stats(region_sentiments: Dict[str, List[str]]) -> Dict[str, Dict]:
    region_stats = {}
    
    for region, sentiments in region_sentiments.items():
        count = Counter(sentiments)
        total = len(sentiments)
        
        if total > 0:
            region_stats[region] = {
                "total": total,
                "positive": count.get("positif", 0),
                "negative": count.get("negatif", 0),
                "neutral": count.get("netral", 0),
                "positive_percent": round((count.get("positif", 0) / total) * 100, 1),
                "negative_percent": round((count.get("negatif", 0) / total) * 100, 1),
                "neutral_percent": round((count.get("netral", 0) / total) * 100, 1),
                "dominant_sentiment": max(count.items(), key=lambda x: x[1])[0] if count else "netral"
            }
    
    return region_stats