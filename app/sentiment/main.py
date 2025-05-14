import json
import datetime
import os
from typing import Dict
from scraper import scrape_places
from sentiment_analyzer import analyze_sentiment
from geo_processor import prepare_geo_data_by_region, prepare_geo_data_by_place
from data_processor import compile_sentiment_results

def analyze_food_sentiment(food_item: str, country: str, max_places: int = 10, max_reviews: int = 5) -> Dict:
    places_data = scrape_places(food_item, country, max_places, max_reviews)
    
    if not places_data:
        print("Tidak ada data yang berhasil ditemukan.")
        return {
            "error": "Tidak ada data yang berhasil ditemukan",
            "overview": {
                "total_places": 0,
                "total_reviews": 0
            }
        }
    
    sentiment_data = analyze_sentiment(places_data)
    
    geo_data = prepare_geo_data_by_region(places_data, sentiment_data.get('regions', {}))
    geo_data_detail = prepare_geo_data_by_place(places_data, sentiment_data.get('regions', {}))
    
    results = compile_sentiment_results(
        places_data, 
        sentiment_data.get('regions', {}), 
        sentiment_data.get('review_sentiments', []),
        geo_data,
        geo_data_detail
    )
    
    results["search_info"] = {
        "food_item": food_item,
        "country": country,
        "timestamp": datetime.datetime.now().isoformat()
    }
    print("Analisis selesai!")
    return results

def save_results_to_file(results: Dict, food_item: str, country: str):
    filename = f"output/{food_item.replace(' ', '_')}_{country}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Hasil analisis disimpan ke '{filename}'")
    
if __name__ == "__main__":
    food = input("Masukkan nama makanan/minuman :") 
    country = input("Masukkan negara : ") 
    max_places = 10 
    max_reviews = 5 

    print(f"\nMenganalisis sentimen untuk '{food}' di {country}...")
    results = analyze_food_sentiment(food, country, max_places, max_reviews)
    
    output_file = f"output/{food.replace(' ', '_')}_{country}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n Hasil disimpan di: {output_file}")
    print("\n HASIL ANALISIS:")
    print(f"• Total tempat: {results['overview']['total_places']}")
    print(f"• Total ulasan: {results['overview']['total_reviews']}")
    print(f"• Sentimen: 👍 {results['overview']['sentiment_distribution']['positive']} | 👎 {results['overview']['sentiment_distribution']['negative']} | 😐 {results['overview']['sentiment_distribution']['neutral']}")
    
    if results.get('top_regions', {}).get('positive'):
        top_region = results['top_regions']['positive'][0]
        print(f"• Wilayah paling positif: {top_region['region']} ({top_region['positive_percent']}%)")