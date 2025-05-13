from app.services.apify_service import ApifyService

class ScraperController:
    def __init__(self):
        self.apify_service = ApifyService()
    
    def scrape_places(self, food_item, country, max_places=50, max_reviews=10):
        """Scrape places data from Google Maps using Apify"""
        places = self.apify_service.scrape_places(
            search_query=food_item,
            location=country,
            max_places=max_places,
            max_reviews=max_reviews
        )
        
        # Process and clean the data
        processed_places = self._process_places(places)
        return processed_places
    
    def _process_places(self, places):
        """Process and standardize the data format"""
        processed = []
        
        for place in places:
            # Extract city/region from address
            address = place.get('address', '')
            city = self._extract_city_from_address(address, place.get('addressComponents', []))
            
            processed_place = {
                'id': place.get('placeId', ''),
                'name': place.get('title', ''),
                'address': address,
                'city': city,
                'country': self._extract_country_from_address(address, place.get('addressComponents', [])),
                'location': {
                    'lat': place.get('location', {}).get('lat'),
                    'lng': place.get('location', {}).get('lng')
                },
                'rating': place.get('totalScore'),
                'reviewsCount': place.get('reviewsCount', 0),
                'reviews': self._process_reviews(place.get('reviews', []))
            }
            processed.append(processed_place)
        
        return processed
    
    def _process_reviews(self, reviews):
        """Process and clean reviews data"""
        processed_reviews = []
        
        for review in reviews:
            if not review.get('text'):  # Skip empty reviews
                continue
                
            processed_review = {
                'author': review.get('userName', 'Unknown'),
                'rating': review.get('stars', 0),
                'text': review.get('text', '').strip(),
                'date': review.get('publishedAtDate', '')
            }
            processed_reviews.append(processed_review)
        
        return processed_reviews
    
    def _extract_city_from_address(self, address, address_components):
        """Extract city from address components or full address"""
        # First try from address components if available
        for component in address_components:
            if component.get('types') and 'locality' in component.get('types'):
                return component.get('long_name', '')
        
        # Fallback to parsing from full address
        # This is a simplified approach - in production you would use a more robust method
        address_parts = address.split(',')
        if len(address_parts) >= 3:
            # Usually the city is the third-to-last part in an address
            potential_city = address_parts[-3].strip()
            # Remove common prefixes that might indicate this is not a city
            prefixes = ['Kec.', 'Kecamatan', 'Kabupaten', 'Kota']
            for prefix in prefixes:
                if potential_city.startswith(prefix):
                    potential_city = potential_city.replace(prefix, '').strip()
            return potential_city
            
        return ""
    
    def _extract_country_from_address(self, address, address_components):
        """Extract country from address components or full address"""
        # First try from address components if available
        for component in address_components:
            if component.get('types') and 'country' in component.get('types'):
                return component.get('long_name', '')
        
        # Fallback to parsing from full address
        if address.strip().endswith('Indonesia'):
            return 'Indonesia'
            
        # You can add more countries here as needed
        return ""
