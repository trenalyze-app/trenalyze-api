from typing import Dict, List

def prepare_geo_data_by_region(places_data: List[Dict], region_stats: Dict) -> Dict:
    regions = {}
    
    for place in places_data:
        region = place.get('region', 'Unknown')
        country = place.get('country', 'Unknown')
        
        region_key = f"{region}, {country}"
        if region_key not in regions:
            region_stat = region_stats.get(region, {})
            dominant_sentiment = region_stat.get('dominant_sentiment', 'netral')
            
            if dominant_sentiment == 'positif':
                color = 'blue'
            elif dominant_sentiment == 'negatif':
                color = 'red'
            else:
                color = 'gray'
            
            center = [
                place.get('location', {}).get('lng', 0),
                place.get('location', {}).get('lat', 0)
            ]
       
            regions[region_key] = {
                'name': region,
                'country': country,
                'center': center,
                'places_count': 0,
                'avg_rating': 0,
                'total_rating': 0,
                'reviews_count': 0,
                'positive_count': region_stat.get('positive', 0),
                'negative_count': region_stat.get('negative', 0),
                'neutral_count': region_stat.get('neutral', 0),
                'dominant_sentiment': dominant_sentiment,
                'color': color
            }
        
        regions[region_key]['places_count'] += 1
        regions[region_key]['total_rating'] += place.get('rating', 0) or 0
        regions[region_key]['reviews_count'] += place.get('reviewsCount', 0) or 0

    for region_key, data in regions.items():
        if data['places_count'] > 0:
            data['avg_rating'] = round(data['total_rating'] / data['places_count'], 1)

    geo_features = []
    
    for region_key, data in regions.items():
        total_sentiments = data['positive_count'] + data['negative_count'] + data['neutral_count']
        positive_percent = round(data['positive_count'] / total_sentiments * 100, 1) if total_sentiments > 0 else 0
        negative_percent = round(data['negative_count'] / total_sentiments * 100, 1) if total_sentiments > 0 else 0
        
        feature = {
            'type': 'Feature',
            'properties': {
                'name': data['name'],
                'country': data['country'],
                'places_count': data['places_count'],
                'avg_rating': data['avg_rating'],
                'reviews_count': data['reviews_count'],
                'sentiment': data['dominant_sentiment'],
                'color': data['color'],
                'positive_count': data['positive_count'],
                'negative_count': data['negative_count'],
                'neutral_count': data['neutral_count'],
                'positive_percent': positive_percent,
                'negative_percent': negative_percent
            },
            'geometry': {
                'type': 'Point',
                'coordinates': data['center']
            }
        }
        geo_features.append(feature)
    
    return {
        'type': 'FeatureCollection',
        'features': geo_features
    }

def prepare_geo_data_by_place(places_data: List[Dict], region_stats: Dict) -> Dict:
    geo_features = []
    
    for place in places_data:
        region = place.get('region', 'Unknown')
        region_sentiment = region_stats.get(region, {}).get('dominant_sentiment', 'netral')
     
        if region_sentiment == 'positif':
            color = 'blue'
        elif region_sentiment == 'negatif':
            color = 'red'
        else:
            color = 'gray'
        
        if place.get('location', {}).get('lat') and place.get('location', {}).get('lng'):
            feature = {
                'type': 'Feature',
                'properties': {
                    'name': place.get('name'),
                    'region': region,
                    'country': place.get('country', 'Unknown'),
                    'sentiment': region_sentiment,
                    'color': color,
                    'rating': place.get('rating'),
                    'reviewsCount': place.get('reviewsCount', 0)
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [
                        place.get('location', {}).get('lng'),
                        place.get('location', {}).get('lat')
                    ]
                }
            }
            geo_features.append(feature)
    
    return {
        'type': 'FeatureCollection',
        'features': geo_features
    }