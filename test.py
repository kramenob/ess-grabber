import requests

url = "https://api.telegram.org/6254370306:AAGVwBDZ6_FMxkCXzNrQbA6HRfVEaMNWJc8/sendMessage"

payload = {
    "text": "Required",
    "parse_mode": "Optional",
    "disable_web_page_preview": False,
    "disable_notification": False,
    "reply_to_message_id": None
}
headers = {
    "accept": "application/json",
    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)