import os
import json
import time

def ensure_test_dir():
    os.makedirs("output_test", exist_ok=True)

def test_scraper_module():
    try:
        from scraper import scrape_places
        
        food_item = input("Masukkan nama makanan: ") or "nasi goreng"
        country = input("Masukkan negara: ") or "Indonesia"
            
        start_time = time.time()
        places_data = scrape_places(food_item, country, max_places=5, max_reviews=10)
        elapsed_time = time.time() - start_time
        
        if places_data:
            filename = f"output_test/scraping_{food_item.replace(' ', '_')}_{country}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(places_data, f, ensure_ascii=False, indent=2)
            
        return places_data

    except Exception as e:
        print(f"Error: {e}")
        return None

def test_sentiment_analyzer(places_data):
    if not places_data:
        print("Tidak ada data untuk dianalisis")
        return None

    try:
        from sentiment_analyzer import analyze_sentiment
        
        start_time = time.time()
        sentiment_data = analyze_sentiment(places_data)
        elapsed_time = time.time() - start_time

        if sentiment_data:
            regions = sentiment_data.get('regions', {})
            filename = f"output_test/sentiment_{len(regions)}_regions.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(sentiment_data, f, ensure_ascii=False, indent=2)
            top_region = max(regions.items(), key=lambda x: x[1]['positive_percent'])
        return sentiment_data

    except Exception as e:
        print(f"Error: {e}")
        return None

def test_geo_processor(places_data, sentiment_data):
    if not places_data or not sentiment_data:
        return None, None

    try:
        from geo_processor import prepare_geo_data_by_region, prepare_geo_data_by_place
        
        region_stats = sentiment_data.get('regions', {})
        geo_data = prepare_geo_data_by_region(places_data, region_stats)
        geo_data_detail = prepare_geo_data_by_place(places_data, region_stats)
        
        with open("output_test/geo_data_region.json", 'w', encoding='utf-8') as f:
            json.dump(geo_data, f, ensure_ascii=False, indent=2)
        
        with open("output_test/geo_data_detail.json", 'w', encoding='utf-8') as f:
            json.dump(geo_data_detail, f, ensure_ascii=False, indent=2)
        
        return geo_data, geo_data_detail

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def test_data_processor(places_data, sentiment_data, geo_data, geo_data_detail):
    if not all([places_data, sentiment_data, geo_data, geo_data_detail]):
        return None

    try:
        from data_processor import compile_sentiment_results
        
        region_stats = sentiment_data.get('regions', {})
        review_sentiments = sentiment_data.get('review_sentiments', [])
        
        results = compile_sentiment_results(
            places_data, 
            region_stats, 
            review_sentiments, 
            geo_data, 
            geo_data_detail
        )
        
        filename = "output_test/final_results.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return results

    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    ensure_test_dir()
    
    places_data = test_scraper_module()
    sentiment_data = test_sentiment_analyzer(places_data)
    geo_data, geo_data_detail = test_geo_processor(places_data, sentiment_data)
    test_data_processor(places_data, sentiment_data, geo_data, geo_data_detail)
    print("Semua pengujian selesai!")

if __name__ == "__main__":
    main()