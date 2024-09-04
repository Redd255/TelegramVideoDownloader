
from telethon import TelegramClient, sync
import os
import re

# Your API credentials
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'
phone_number = 'YOUR_PHONE_NUMBER'

# Create a new Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Connect to the client
client.start(phone=phone_number)

# Function to extract chat username and message ID from a Telegram link
def extract_chat_and_message_id(link):
    match = re.search(r'https://t\.me/([a-zA-Z0-9_]+)/(\d+)', link)
    if match:
        chat_username = match.group(1)
        message_id = int(match.group(2))
        return chat_username, message_id
    else:
        raise ValueError("Invalid link format. Please provide a valid Telegram message link.")

# Function to download videos from a range of messages in a chat/channel
def download_videos_from_range(chat_username, start_message_id, end_message_id, download_folder):
    try:
        # Ensure the download folder exists
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for message_id in range(start_message_id, end_message_id + 1):
            # Get the message by ID
            message = client.get_messages(chat_username, ids=message_id)

            # Check if the message has a video
            if message and message.video:
                # Download the video
                file_path = client.download_media(message.media, file=download_folder)
                print(f'Downloaded: {file_path}')
            else:
                print(f"No video found in message ID: {message_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
start_link = 'https://t.me/exmpl/1725'
end_link = 'https://t.me/exmpl/1886'

# Extract chat username and message IDs from the links
chat_username, start_message_id = extract_chat_and_message_id(start_link)
_, end_message_id = extract_chat_and_message_id(end_link)

# Set the download folder
download_folder = 'folderName'

# Download videos from the specified range
download_videos_from_range(chat_username, start_message_id, end_message_id, download_folder)

# Disconnect the client
client.disconnect()
