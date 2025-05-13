from datetime import datetime
from app.utils.db_utils import get_db

class Search:
    def __init__(self, id=None, food_item=None, country=None, 
                 places_data=None, sentiment_results=None, 
                 created_at=None, updated_at=None):
        self.id = id
        self.food_item = food_item
        self.country = country
        self.places_data = places_data
        self.sentiment_results = sentiment_results
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    @classmethod
    def find_by_query(cls, food_item, country):
        """Find a search by food item and country"""
        db = get_db()
        search_data = db.searches.find_one({
            'food_item': food_item, 
            'country': country
        })
        
        if search_data:
            return cls(
                id=str(search_data['_id']),
                food_item=search_data['food_item'],
                country=search_data['country'],
                places_data=search_data['places_data'],
                sentiment_results=search_data['sentiment_results'],
                created_at=search_data['created_at'],
                updated_at=search_data['updated_at']
            )
        return None
    
    @classmethod
    def create_or_update(cls, food_item, country, places_data, sentiment_results):
        """Create or update a search record"""
        db = get_db()
        now = datetime.utcnow()
        
        search_data = {
            'food_item': food_item,
            'country': country,
            'places_data': places_data,
            'sentiment_results': sentiment_results,
            'updated_at': now
        }
        
        existing = db.searches.find_one({
            'food_item': food_item, 
            'country': country
        })
        
        if existing:
            # Update existing record
            search_data['created_at'] = existing['created_at']
            db.searches.update_one(
                {'_id': existing['_id']},
                {'$set': search_data}
            )
            search_data['_id'] = existing['_id']
        else:
            # Create new record
            search_data['created_at'] = now
            result = db.searches.insert_one(search_data)
            search_data['_id'] = result.inserted_id
        
        return cls(
            id=str(search_data['_id']),
            food_item=search_data['food_item'],
            country=search_data['country'],
            places_data=search_data['places_data'],
            sentiment_results=search_data['sentiment_results'],
            created_at=search_data['created_at'],
            updated_at=search_data['updated_at']
        )
    
    def to_dict(self):
        """Convert the object to a dictionary"""
        return {
            'id': self.id,
            'food_item': self.food_item,
            'country': self.country,
            'sentiment_results': self.sentiment_results,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
