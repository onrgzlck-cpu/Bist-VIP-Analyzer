import requests
import config

def send_telegram_message(message):
    token = config.TELEGRAM_TOKEN # Config'den okuyacak
    chat_id = config.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram mesajı gönderilemedi: {e}")
