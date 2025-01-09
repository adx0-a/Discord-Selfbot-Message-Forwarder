import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN") # Your Account Token
VALID_CHAT_ID = os.getenv("VALID_CHAT_ID")  # Channel ID where command will works there

print("Token: ", TOKEN)
print("Valid Chat ID: ", VALID_CHAT_ID)
BASE_URL = "https://discord.com/api/v9"
limit = 100 # Message limit to fetch
HEADERS = {
    'authorization': TOKEN,
    'content-type': 'application/json',
    'origin': 'https://discord.com',
}

def forward_message(from_channel, to_channel, message_id):
    json_data = {
        'message_reference': {
            'channel_id': from_channel, #channel id to forward from
            'message_id': message_id, #message id to forward from
            'type': 1,
        },
    }
    url = f'https://discord.com/api/v9/channels/{to_channel}/messages'
    response = requests.post(url,headers=HEADERS,json=json_data)
    
    if response.status_code == 200:
        print(f"Message forwarded from channel {from_channel} to {to_channel}")
    elif response.status_code == 429:
        TimeWait = response.json()["retry_after"] + 10
        print(f"Rate limit exceeded. Waiting for {TimeWait} seconds.")
        time.sleep(TimeWait)
        forward_message(from_channel, to_channel, message_id)
    else:
        print(f"Error forwarding message: {response.status_code} - {response.text} - {url}")
        print("from_channel: ", from_channel, "to_channel: ", to_channel, "message_id: ", message_id)
        exit()

def process_command(message):
    if not message["channel_id"] == VALID_CHAT_ID:
        return

    if message["content"].startswith("/forward "):
        try:
            _, from_channel, to_channel = message["content"].split()
            print(f"Forwarding from {from_channel} to {to_channel}")
            messages = get_channel_messages(from_channel, limit)
            for msg in messages[::-1]:
                print(msg["id"])
                forward_message(from_channel, to_channel, msg["id"])
        except ValueError:
            print("Incorrect command format. Use: /forward from_channel_id to_channel_id")

def get_channel_messages(channel_id, limit):
    url = f"{BASE_URL}/channels/{channel_id}/messages?limit={limit}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching messages: {response.status_code} - {response.text}")
        return []

def check_new_messages():
    url = f"{BASE_URL}/channels/{VALID_CHAT_ID}/messages?limit=1"
    last_message_id = None

    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            messages = response.json()
            if messages and messages[0]["id"] != last_message_id:
                last_message_id = messages[0]["id"]
                process_command(messages[0])
        else:
            print(f"Error fetching new messages: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        check_new_messages()
    except KeyboardInterrupt:
        print("Program interrupted. Exiting gracefully.")
        exit()
