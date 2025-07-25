# Elite Trading Signal Bot

This project is a FastAPI-based application that generates trading signals using OpenAI's API and posts them to a Telegram channel every 15 minutes. It also provides an API endpoint for sending trading signals manually.

## Features
- **Automated Trading Signals:** Generates and posts formatted trading signals to Telegram every 15 minutes.
- **OpenAI Integration:** Uses GPT-4 to analyze and summarize market data.
- **FastAPI Server:** Provides an API endpoint for manual signal posting (extendable).

## Project Structure
- `main.py` — FastAPI app entry point, background thread for auto-sending signals.
- `CreateSignal.py` — Gathers market data, generates signal messages using OpenAI.
- `telegram.py` — Sends messages to Telegram via the Bot API.
- `BTC_volume.py`, `perp_volume.py`, `spot_volume.py` — Data source modules for market data.
- `config.py` — Stores API keys and configuration constants.
- `requirements.txt` — Python dependencies.

## How to Run (Step by Step)

### 1. Install Python (if not already installed)
Make sure you have Python 3.7 or higher installed. You can check your version with:
```bash
python --version
```
If you need to install Python, download it from [python.org](https://www.python.org/downloads/).

### 2. Install Dependencies
Install all required Python packages using pip:
```bash
pip install -r requirements.txt
```

### 3. Configure API Keys
Edit the `config.py` file and set your credentials:
```python
BOT_TOKEN = "<your-telegram-bot-token>"
CHANNEL_USERNAME = "<your-channel-username-or-id>"
OPENAI_API_KEY = "<your-openai-api-key>"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
# (Optional) BINANCE_API_KEY = "<your-binance-api-key>"
```
**Important:** Keep this file secure and do not share it publicly!

### 4. Run the Application
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
- Every 15 minutes, a trading signal will be generated and posted to your Telegram channel automatically.

### 5. (Optional) Test the API Endpoint
You can access the interactive API docs at:
```
```
From here, you can test any available endpoints.

---

## About the Prompt Value

The content and structure of the trading signal sent to OpenAI is controlled by the `PROMPT_TEMPLATE` variable in `config.py`.

- **Purpose:** This template defines how your market data is presented to the AI and what kind of summary or formatting you want in the response.
- **Customization:** You can edit the `PROMPT_TEMPLATE` string in `config.py` to change the instructions, formatting style, or output requirements for the generated signal. The template uses Python's `.format()` placeholders: `{perp}`, `{spot}`, and `{btc_volume}` will be replaced with live data at runtime.
- **Example:**
```python
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
```
- **Tip:** Adjust the instructions or formatting in this template to get different styles or details in your Telegram signals.

---

## Customization
- **Signal Logic:** Edit `CreateSignal.py` to change how signals are generated or formatted.
- **Data Sources:** Update or extend `BTC_volume.py`, `perp_volume.py`, and `spot_volume.py` to use your preferred data sources.
- **API Endpoints:** Add more endpoints to `main.py` as needed.

## Dependencies
- fastapi
- uvicorn
- requests

## Security Note
- Never commit your real API keys to public repositories.
- Use environment variables or a secrets manager for production deployments.

## License
This project is for educational and demonstration purposes. Please review and adapt for your own use case. 
