# app/utils/platform_scraping.py
import re
from apify_client import ApifyClient
from ..config import api_key_apify

class ApifyScraper:
    """Utility for scraping data using Apify"""
    
    @staticmethod
    def extract_city_from_address(address):
        """Extract city and province from an address string"""
        # Pattern to find city and province in Indonesian addresses
        city_pattern = r'(?:Kota|Kabupaten)\s+(\w+)'
        province_pattern = r'(?:Provinsi\s+)?([^,]+?)\s*(?:\d{5})?(?:,\s*Indonesia)?$'
        
        # Default values
        city = "Unknown"
        province = "Jawa Timur"  # Default to East Java based on sample data
        
        # Try to extract city
        city_match = re.search(city_pattern, address)
        if city_match:
            city = city_match.group(1)
        else:
            # Alternative pattern: look for "Kec." followed by district name
            district_pattern = r'Kec\.\s+(\w+)'
            district_match = re.search(district_pattern, address)
            if district_match:
                city = district_match.group(1)
        
        # Try to extract province - if "Jawa Timur" is in the address
        if "Jawa Timur" in address:
            province = "Jawa Timur"
        elif "Jawa Barat" in address:
            province = "Jawa Barat"
        elif "Jawa Tengah" in address:
            province = "Jawa Tengah"
        # More provinces can be added as needed
        
        # Try to extract province using regex as fallback
        province_match = re.search(province_pattern, address)
        if province_match:
            province = province_match.group(1)
        
        return city, province
    
    @staticmethod
    async def scrape_places(search_term, location="Indonesia", max_places=5, max_reviews=3):
        """Scrape places and their reviews based on search term and location"""
        # Initialize Apify client
        client = ApifyClient(api_key_apify)
        
        # Configure input for the Apify actor
        run_input = {
            "searchStringsArray": [search_term],
            "locationQuery": location,
            "maxCrawledPlacesPerSearch": max_places,
            "language": "id",
            "maxReviews": max_reviews,
            "scrapePlaceDetailPage": True,
        }
        
        try:
            # Run the actor and wait for results
            actor_id = "nwua9Gu5YrADL7ZDj"  # Google Maps Places Scraper
            run = client.actor(actor_id).call(run_input=run_input)
            
            # Get dataset items
            dataset_items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
            
            # Process items to extract location info
            processed_items = []
            for item in dataset_items:
                address = item.get('address', '')
                city, province = ApifyScraper.extract_city_from_address(address)
                
                processed_item = {
                    'title': item.get('title', ''),
                    'address': address,
                    'city': city,
                    'province': province,
                    'location': {
                        'lat': item.get('latitude', 0),
                        'lng': item.get('longitude', 0)
                    },
                    'totalScore': item.get('totalScore', 0),
                    'reviewsCount': item.get('reviewsCount', 0),
                    'reviews': item.get('reviews', [])
                }
                
                processed_items.append(processed_item)
            
            return processed_items
        except Exception as e:
            print(f"Error scraping data: {str(e)}")
            return []