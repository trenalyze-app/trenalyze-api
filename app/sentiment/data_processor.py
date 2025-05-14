from typing import Dict, List
from collections import Counter

def compile_sentiment_results(places_data: List[Dict], region_stats: Dict, 
                             review_sentiments: List[Dict], geo_data, geo_data_detail) -> Dict:
    all_sentiments = [r['sentiment'] for r in review_sentiments]
    sentiment_ranking = sorted(
        [(region, stats) for region, stats in region_stats.items()],
        key=lambda x: x[1]['positive_percent'],
        reverse=True
    )
    
    top_positive_regions = sentiment_ranking[:5] if sentiment_ranking else []
    top_negative_regions = sorted(
        [(region, stats) for region, stats in region_stats.items()],
        key=lambda x: x[1]['negative_percent'],
        reverse=True
    )[:5] if region_stats else []
    positive_reviews = [r for r in review_sentiments if r['sentiment'] == 'positif']
    positive_reviews_sorted = sorted(positive_reviews, key=lambda x: len(x['text']))
    top_positive_phrases = positive_reviews_sorted[:5] if positive_reviews_sorted else []
    
    results = {
        "overview": {
            "total_places": len(places_data),
            "total_reviews": sum(len(p.get('reviews', [])) for p in places_data),
            "total_regions": len(region_stats),
            "sentiment_distribution": {
                "positive": all_sentiments.count('positif'),
                "negative": all_sentiments.count('negatif'),
                "neutral": all_sentiments.count('netral')
            }
        },
        "regions": region_stats,
        "top_regions": {
            "positive": [
                {"region": region, "positive_percent": stats['positive_percent']}
                for region, stats in top_positive_regions
            ],
            "negative": [
                {"region": region, "negative_percent": stats['negative_percent']}
                for region, stats in top_negative_regions
            ]
        },
        "top_phrases": [
            {
                "text": phrase['text'],
                "place_name": phrase['place_name'],
                "percentage": round((all_sentiments.count('positif') / len(all_sentiments)) * 100 
                                  if len(all_sentiments) > 0 else 0, 1)
            }
            for phrase in top_positive_phrases
        ],
        "geo_data": geo_data,
        "geo_data_detail": geo_data_detail
    }
    
    return results