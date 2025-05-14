import os
import re
from typing import Dict, List, Any
from apify_client import ApifyClient

APIFY_API_KEY = os.environ.get("APIFY_API_KEY", "apify_api_3qeGEFLLY0mKbkdrKWFwc5k9hFWLKe4tac2e")

def scrape_places(food_item: str, country: str, max_places: int = 10, max_reviews: int = 5) -> List[Dict]:
    client = ApifyClient(APIFY_API_KEY)
    
    run_input = {
        "searchStringsArray": [food_item],
        "locationQuery": country,
        "maxCrawledPlacesPerSearch": max_places,
        "language": _get_language_for_country(country),
        "maxReviews": max_reviews,
        "scrapePlaceDetailPage": True,
    }
    
    try:
        run = client.actor("nwua9Gu5YrADL7ZDj").call(run_input=run_input)
        
        places = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            place = _process_place_data(item)
            places.append(place)
        
        print(f"Berhasil mengambil data {len(places)} tempat!")
        return places
        
    except Exception as e:
        print(f"Error saat scraping: {str(e)}")
        return []

def _process_place_data(item: Dict) -> Dict:
    address = item.get('address', '')
    region_info = _extract_region_from_address(address, item.get('addressComponents', []))
    
    reviews = []
    for review in item.get("reviews", []):
        if review.get("text"):
            reviews.append({
                "author": review.get("userName", "Unknown"),
                "rating": review.get("stars", 0),
                "text": (review.get("text") or "").strip()
            })
    
    place = {
        "name": item.get('title', ''),
        "address": address,
        "region": region_info["region"],
        "country": region_info["country"],
        "rating": item.get('totalScore'),
        "reviewsCount": item.get('reviewsCount', 0),
        "reviews": reviews,
        "location": {
            "lat": item.get('location', {}).get('lat'),
            "lng": item.get('location', {}).get('lng')
        }
    }
    
    return place

def _extract_region_from_address(address: str, address_components: List = None) -> Dict[str, str]:
    result = {
        "region": "Unknown",
        "country": "Unknown"
    }
    if address_components:
        for component in address_components:
            types = component.get('types', [])
            if 'administrative_area_level_1' in types:
                result["region"] = component.get('long_name', 'Unknown')
            elif 'locality' in types and result["region"] == "Unknown":
                result["region"] = component.get('long_name', 'Unknown')
            elif 'country' in types:
                result["country"] = component.get('long_name', 'Unknown')
    
    if result["region"] == "Unknown" or result["country"] == "Unknown":
        parts = [part.strip() for part in address.split(',')]
        if parts and result["country"] == "Unknown":
            last_part = parts[-1].strip()
            ap_countries = [
                "Indonesia", "Malaysia", "Singapore", "Thailand", "Vietnam", 
                "Philippines", "Japan", "South Korea", "China", "Taiwan", 
                "Australia", "New Zealand", "India"
            ]
            for country in ap_countries:
                if country.lower() in last_part.lower():
                    result["country"] = country
                    break
    
        if len(parts) > 1 and result["region"] == "Unknown":
            for part in parts:
                if "Provinsi" in part:
                    result["region"] = part.replace("Provinsi", "").strip()
                    break
                elif "Kota" in part:
                    result["region"] = part.strip()
                    break
                elif "Kabupaten" in part:
                    result["region"] = part.strip()
                    break
            
            if result["region"] == "Unknown":
                for part in parts:
                    postal_region_match = re.search(r'^\d+\s+(.+)$', part)
                    if postal_region_match:
                        result["region"] = postal_region_match.group(1).strip()
                        break
            
            if result["region"] == "Unknown" and len(parts) >= 2:
                potential_region = parts[-2].strip()
                if not re.match(r'^\d+$', potential_region):
                    result["region"] = potential_region
    
    if result["region"] != "Unknown":
        for prefix in ["Kota", "Kabupaten", "Provinsi", "Province of", "State of"]:
            if result["region"].startswith(prefix):
                result["region"] = result["region"].replace(prefix, "").strip()
    
    return result

def _get_language_for_country(country: str) -> str:
    language_map = {
        "Indonesia": "id",
        "Malaysia": "ms",
        "Singapore": "en",
        "Thailand": "th",
        "Vietnam": "vi",
        "Philippines": "en",
        "Japan": "ja",
        "South Korea": "ko",
        "China": "zh-CN",
        "Taiwan": "zh-TW",
        "India": "hi",
        "Australia": "en",
        "New Zealand": "en"
    }
    
    return language_map.get(country, "en")