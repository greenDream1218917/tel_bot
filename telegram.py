"""
telegram.py

This module provides a function to post messages to a Telegram channel using the Telegram Bot API. 
Used by the FastAPI endpoint and background thread.
"""
import requests  # For making HTTP requests to the Telegram API
from config import BOT_TOKEN, CHANNEL_USERNAME  # Import bot token and channel username from config


def post_to_telegram(message):
    """
    Sends a message to the configured Telegram channel using the Telegram Bot API.

    Parameters:
        message (str): The message text to send.

    Returns:
        Response: The response object from the requests library.

    Notes:
        - Uses HTML parse mode for message formatting.
        - If the API call fails, the response will contain error details.
    """
    # Construct the Telegram API URL for sending messages
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    # Prepare the payload with chat ID, message text, and parse mode
    payload = {
        "chat_id": CHANNEL_USERNAME,  # Channel username or ID
        "text": message,              # Message to send
        "parse_mode": "HTML"         # Use HTML formatting in the message
    }
    # Send the POST request to the Telegram API
    response = requests.post(url, data=payload)
    # Return the response object (contains status and any error info)
    return response 