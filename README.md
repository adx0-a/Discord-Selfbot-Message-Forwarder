# Discord Message Forwarder

This script forwards messages from one Discord channel to another based on commands received in a specified channel.

## Prerequisites

- Python 3.x
- `requests` library
- `python-dotenv` library

You can install the required libraries using pip:

```
pip install requests python-dotenv
```

## Setup

1. Clone the repository or download the script.
2. Create a ⚙️ .env file in the root directory with the following content:

```
DISCORD_TOKEN=your_discord_token 
VALID_CHAT_ID=your_valid_chat_id
```

Replace your_discord_token with your Discord account token and your_valid_chat_id with the channel ID where the command will work.

To get Your Real Account Token See [that](https://stackoverflow.com/questions/67348339/any-way-to-get-my-discord-token-from-browser-dev-console)


Run the script:
```
python main.py
```

Usage
To forward messages from one channel to another, use the following command in the specified channel:

Replace from_channel_id with the ID of the channel you want to forward messages from and to_channel_id with the ID of the channel you want to forward messages to.

## License
```
This project is licensed under the MIT License. 
```