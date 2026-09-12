import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', None)
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', None)

DEBUG_MODE = os.getenv('DEBUG_MODE', 'False').lower() == 'true'

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    if DEBUG_MODE:
        print("⚠️  Telegram credentials not configured.")
        print("   Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")
        print("   See README_UPDATED.md for setup instructions.")
