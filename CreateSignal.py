"""
CreateSignal.py   

This module generates trading signal messages using OpenAI's API. It includes the holy_algorithm and liquidity_oscillation_engine prompt logic for signal generation. Used by the FastAPI endpoint and background thread.
"""
import requests  # For making HTTP requests to the OpenAI API
from Fetch_data.BTC_volume import get_volumes_report  # Function to get BTC volume data
from Fetch_data.perp_volume import get_perp_report    # Function to get perpetual funding data
from Fetch_data.spot_volume import get_spot_report    # Function to get spot funding data
from config import OPENAI_API_KEY, OPENAI_API_URL, PROMPT_TEMPLATE  # API key, URL, and prompt template for OpenAI


def generate_chatgpt_signal_message():
    """
    Generates a trading signal message using OpenAI's API.
    Gathers data from various sources, constructs a prompt, and sends it to OpenAI for analysis and formatting.

    Returns:
        str: The formatted trading signal message, or an error message if generation fails.
    """
    # Get BTC volume report (dict with timeframes and values)
    btc_volume = get_volumes_report()
    # Get perpetual funding data (list of coins and $ amounts)
    perp = get_perp_report()
    # Get spot funding data (list of coins and $ amounts)
    spot = get_spot_report()
    # Construct the prompt for OpenAI, including all gathered data
    prompt = PROMPT_TEMPLATE.format(perp=perp, spot=spot, btc_volume=btc_volume)
    # Set up headers for OpenAI API request
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",  # Bearer token for authentication
        "Content-Type": "application/json"            # Specify JSON content
    }
    # Prepare the data payload for the OpenAI API
    data = {
        "model": "gpt-4o-mini",  # Model to use
        "messages": [
            {"role": "system", "content": "You are a professional trading analyst specializing in technical analysis, liquidity dynamics, and algorithmic trading signals."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 250,        # Limit the response length
        "temperature": 0.7,       # Sampling temperature for creativity
        "stream": False           # No streaming
    }
    try:
        # Send the POST request to OpenAI API
        response = requests.post(OPENAI_API_URL, headers=headers, json=data)
        if response.status_code == 200:
            # Extract and return the generated message content
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            # If the API call fails, return an error message
            return "Signal generation failed."
    except Exception as e:
        # Print any exceptions for debugging and return an error message
        print(f"Error calling OpenAI API: {e}")
        return "Signal generation failed." 