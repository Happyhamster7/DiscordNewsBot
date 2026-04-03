import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "store.json")
MAX_ARTICLES_PER_TOPIC = 3
MAX_SEEN_ARTICLES_PER_GUILD = 200
MAX_TOPICS_PER_DIGEST = 10
SCHEDULE_HOURS = 6

EMBED_COLORS = [0x5865F2, 0x57F287, 0xFEE75C, 0xED4245, 0xEB459E]

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in .env")
if not NEWSAPI_KEY:
    raise RuntimeError("NEWSAPI_KEY is not set in .env")
