"""
main.py

This is the entry point for the FastAPI application.    
It defines the API endpoint for sending trading signals to Telegram, using indicator calculation and signal generation modules. 
It also starts the background thread for periodic signal sending.
"""
import threading
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from CreateSignal import generate_chatgpt_signal_message
from telegram import post_to_telegram

app = FastAPI()

class Signal(BaseModel):
    """
    Pydantic model for the trading signal request body.

    Attributes:
        asset (str): The trading pair symbol (e.g., 'BTCUSDT').
    """
    asset: str

# --- Background Thread for Auto-Sending Signals ---
def background_signal_sender():
    """
    Periodically generates a trading signal and posts it to Telegram every 15 minutes.
    Runs in a separate daemon thread so it doesn't block the FastAPI server.
    """
    while True:
        try:
            # Generate the signal message using the CreateSignal module
            message = generate_chatgpt_signal_message()
            # Post the generated message to the configured Telegram channel
            post_to_telegram(message)
        except Exception as e:
            # Print any errors to the console for debugging
            print(f"Error sending signal: {e}")
        # Wait for 15 minutes before sending the next signal
        time.sleep(15 * 60)

def start_background_thread():
    """
    Starts the background thread for periodic signal sending.
    The thread is set as a daemon so it will not prevent program exit.
    """
    thread = threading.Thread(target=background_signal_sender, daemon=True)
    thread.start()

# Start the background thread for auto-sending signals
start_background_thread()