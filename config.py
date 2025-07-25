"""
config.py

This file contains API keys and configuration constants for the trading signal project. All sensitive keys should be kept secure and not shared publicly.
"""
# Telegram bot token for sending messages
BOT_TOKEN = "8160875773:AAGLDQX_FrlpeOqaUGCUXuK4BChu8-jq8-4"
# Telegram channel username or chat ID
CHANNEL_USERNAME = "-4863819718"
# OpenAI API key for generating trading signals
OPENAI_API_KEY = ""
# OpenAI API URL endpoint
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
# Binance API key (not currently used in requests, but available for future use)
BINANCE_API_KEY = "gWRFKzfQLiuPZvQvIkHimb8wBnhcXH2KUyHTvppxLg3kenHUFCcQzL060Ex123Dz"

# Prompt template for signal generation
PROMPT_TEMPLATE = """
INPUT: 
- Perp funding data: List of (coin, $ amount):
    {perp}
- Spot funding data: List of (coin, $ amount):
    {spot}
- BTC price flow table: Dict with timeframes as keys and perp/spot values:
    {btc_volume}

TASK: 
- Clean + sort data
- Format into summary blocks: BTC Flow, Top Perp, Top Spot, OI Builds, TLDR
- Output in Apple-style list (no tables), emoji where helpful

OUTPUT:
include emoji

Formatted Telegram-ready text
""" 