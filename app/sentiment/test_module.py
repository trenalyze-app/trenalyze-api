import os
import json
import time

def ensure_test_dir():
    os.makedirs("output_test", exist_ok=True)

def test_scraper_module():
    try:
        from scraper import scrape_places
        
        food_item = input("Masukkan nama makanan/minuman : ") or "es teh"
        country = input("Masukkan negara : ") or "indonesia"
            
        start_time = time.time()
        places_data = scrape_places(food_item, country, max_places=10, max_reviews=5)
        elapsed_time = time.time() - start_time
        
        if places_data:
            filename = f"output_test/scraping_{food_item.replace(' ', '_')}_{country}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(places_data, f, ensure_ascii=False, indent=2)
            
            print(f"\nBerhasil mengambil data {len(places_data)} tempat!")
            print(f"Data scraping disimpan di: {filename}")
            
        return places_data, food_item, country

    except Exception as e:
        print(f"Error: {e}")
        return None, None, None

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
            
            print(f"\nAnalisis sentimen selesai untuk {len(regions)} region!")
            print(f"Data sentimen disimpan di: {filename}")
            
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
        
        print("\nData geografis disimpan di:")
        print(f"- output_test/geo_data_region.json")
        print(f"- output_test/geo_data_detail.json")
        
        return geo_data, geo_data_detail

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def test_data_processor(places_data, sentiment_data, geo_data, geo_data_detail, food_item, country):
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
        
        filename = f"output_test/final_{food_item.replace(' ', '_')}_{country}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\nHasil akhir disimpan di: {filename}")
        return results

    except Exception as e:
        print(f"Error: {e}")
        return None

def display_summary(results):
    if not results:
        print("Tidak ada hasil untuk ditampilkan")
        return
    
    print("\n" + "="*50)
    print(" HASIL ANALISIS:")
    print("="*50)
    print(f"• Total tempat: {results['overview']['total_places']}")
    print(f"• Total ulasan: {results['overview']['total_reviews']}")
    
    dist = results['overview']['sentiment_distribution']
    print(f"• Sentimen: 👍 {dist['positive']} | 👎 {dist['negative']} | 😐 {dist['neutral']}")
    
    if results.get('top_regions', {}).get('positive'):
        top_region = results['top_regions']['positive'][0]
        print(f"• Wilayah paling positif: {top_region['region']} ({top_region['positive_percent']}%)")
    print("="*50 + "\n")

def main():
    ensure_test_dir()
    
    print("\n" + "="*50)
    print(" MEMULAI PENGUJIAN MODUL")
    print("="*50)
    
    places_data, food_item, country = test_scraper_module()
    sentiment_data = test_sentiment_analyzer(places_data)
    geo_data, geo_data_detail = test_geo_processor(places_data, sentiment_data)
    final_results = test_data_processor(places_data, sentiment_data, geo_data, geo_data_detail, food_item, country)
    
    display_summary(final_results)
    print("✅ Semua pengujian selesai!")

if __name__ == "__main__":
    main()