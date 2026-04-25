import telebot
import requests

# --- Apnar details eikhane thakbe ---
TELEGRAM_TOKEN = '8748153358:AAEmwfgiIjllknilBaaQuV7P7ye2E4u1feA'
GROQ_API_KEY = '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'
# --------------------------------------

bot = telebot.TeleBot(TELEGRAM_TOKEN)

def get_ai_reply(user_text):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile", # Notun model bosiye dilam
        "messages": [
            {"role": "system", "content": "You are a helpful AI assistant. Reply in the same language the user uses."},
            {"role": "user", "content": user_text}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    res_data = response.json()
    
    if 'choices' in res_data:
        return res_data['choices'][0]['message']['content']
    else:
        return f"AI Error: {res_data.get('error', {}).get('message', 'Unknown Error')}"

print("Bot ekhon ready! Telegram-e message din.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        reply = get_ai_reply(message.text)
        bot.reply_to(message, reply)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "Ektu somossa hoyeche, abar try koro.")

bot.polling()
