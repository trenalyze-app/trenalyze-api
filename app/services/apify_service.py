from apify_client import ApifyClient
import os

class ApifyService:
    def __init__(self):
        self.client = ApifyClient(os.environ.get('APIFY_API_KEY', 'your_api_key_here'))
    
    def scrape_places(self, search_query, location, max_places=50, max_reviews=10):
        """Scrape places from Google Maps using Apify"""
        run_input = {
            "searchStringsArray": [search_query],
            "locationQuery": location,
            "maxCrawledPlacesPerSearch": max_places,
            "language": self._get_language_for_location(location),
            "maxReviews": max_reviews,
            "scrapePlaceDetailPage": True,
        }
        
        # Run the actor and wait for it to finish
        run = self.client.actor("nwua9Gu5YrADL7ZDj").call(run_input=run_input)
        
        # Get results from the dataset
        items = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            items.append(item)
        
        return items
    
    def _get_language_for_location(self, location):
        """Get appropriate language code for the location"""
        # Map countries to language codes
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
        
        return language_map.get(location, "en")
