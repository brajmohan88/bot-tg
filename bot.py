import requests
import time

# ✅ बॉट API टोकन
BOT_TOKEN = "7778293612:AAEMYlLJ2WTkrgq9IeqYTiuX1U0VHKjlfMQ"
API_URL = "https://reaction.inr.workers.dev/?token={}&chat_id={}&message_id={}"

# पहले से प्रोसेस किए गए मैसेज स्टोर करने के लिए
processed_message_ids = set()

# ✅ Reaction API को कॉल करने का फंक्शन
def send_reaction(chat_id, message_id):
    if message_id in processed_message_ids:
        return  # पहले से प्रोसेस किए गए मैसेज को स्किप करें

    # सही API URL तैयार करें
    url = API_URL.format(BOT_TOKEN, chat_id, message_id)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        processed_message_ids.add(message_id)  # मैसेज ID को स्टोर करें
        print(f"✅ Reaction sent in chat {chat_id} for message ID: {message_id}")  # Debug Log
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending reaction: {e}")  # एरर लॉग करें

# ✅ नए मैसेज को प्रोसेस करने का फंक्शन
def handle_updates():
    updates_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset=-1"
    try:
        response = requests.get(updates_url, timeout=10)
        response.raise_for_status()
        updates = response.json()

        if updates["ok"]:
            for update in updates["result"]:
                message = update.get("message")
                if message:
                    message_id = message["message_id"]
                    chat_id = message["chat"]["id"]  # अब हर चैट (ग्रुप या पर्सनल) से `chat_id` लेगा

                    send_reaction(chat_id, message_id)  # ✅ अब हर चैट में ऑटोमैटिक रिएक्शन देगा

    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching updates: {e}")  # एरर लॉग करें

# ✅ बॉट को लगातार चलाने के लिए Infinite Loop
if __name__ == "__main__":
    print("🚀 Bot is running...")  # बॉट स्टार्ट होने का कंफर्मेशन
    while True:
        handle_updates()
        time.sleep(1)  # अधिक API कॉल्स से बचने के लिए 1 सेकंड की देरी
