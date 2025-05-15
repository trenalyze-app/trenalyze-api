from chatbot import get_market_analysis

if __name__ == "__main__":
    print("🤖 AI Market Analysis F&B Asia Pasifik")
    print("Ketik 'exit' untuk keluar.\n")

    while True:
        user_input = input("👤 Anda: ")
        if user_input.lower() == "exit":
            break
        response = get_market_analysis(user_input)
        print(f"🤖 Gemini: {response}\n")
