import os
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY", "")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
DEV_GUILD_ID = os.getenv("DEV_GUILD_ID")

ENABLE_NEWSAPI  = bool(NEWSAPI_KEY)
ENABLE_RSS      = True
ENABLE_GUARDIAN = bool(GUARDIAN_API_KEY)
ENABLE_GNEWS    = bool(GNEWS_API_KEY)
ENABLE_REDDIT   = True

STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "store.json")
MAX_ARTICLES_PER_TOPIC = 3
MAX_SEEN_ARTICLES_PER_GUILD = 200
MAX_TOPICS_PER_DIGEST = 10
DIGEST_TIME = datetime.time(hour=11, minute=0, tzinfo=ZoneInfo("Australia/Sydney"))

EMBED_COLORS = [0x5865F2, 0x57F287, 0xFEE75C, 0xED4245, 0xEB459E]

# Video generation (opt-in — validated at command time, not startup)
ANTHROPIC_API_KEY     = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY    = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID   = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
BACKGROUND_VIDEOS_DIR = os.getenv("BACKGROUND_VIDEOS_DIR", "./background_videos")
OUTPUT_VIDEOS_DIR     = os.getenv("OUTPUT_VIDEOS_DIR", "./output_videos")

if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set in .env")
if not NEWSAPI_KEY:
    print("[config] NEWSAPI_KEY not set — NewsAPI source will be disabled")
