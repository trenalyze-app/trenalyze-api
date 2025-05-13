import google.generativeai as genai
import os

class GeminiService:
    def __init__(self):
        api_key = os.environ.get('GEMINI_API_KEY', 'your_api_key_here')
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of a given text using Gemini API"""
        if not text or len(text.strip()) < 3:
            return "netral"  # Default for very short or empty text
            
        prompt = f"""Analisis sentimen dari ulasan berikut ini:
"{text}"
Kembalikan salah satu dari: positif, negatif, atau netral. Jangan tambahkan teks lain."""
        
        try:
            response = self.model.generate_content(prompt)
            sentiment = response.text.strip().lower()
            
            # Ensure we only return valid sentiment values
            if sentiment not in ["positif", "negatif", "netral"]:
                return "netral"
                
            return sentiment
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return "netral"  # Default fallback if API fails
