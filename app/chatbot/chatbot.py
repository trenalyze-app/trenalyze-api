from prompt import SYSTEM_PROMPT
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

def format_prompt(user_input):
    
    return f"{SYSTEM_PROMPT.strip()}\n\nPertanyaan Pengguna: {user_input}"

def get_market_analysis(user_input):
    prompt = format_prompt(user_input)
    response = model.generate_content(prompt)
    return response.text
