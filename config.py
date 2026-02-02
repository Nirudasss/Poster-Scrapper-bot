from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


class Config:
    # ──────────────── REQUIRED (Must be set in .env) ────────────────
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DATABASE_URL = os.environ.get("DATABASE_URL")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "elitebotzking")
    OWNER_ID = int(os.environ.get("OWNER_ID", 0))

    # ──────────────── OPTIONAL LIST VALUES ────────────────
    SUDO_USERS = (
        list(map(int, os.environ.get("SUDO_USERS", "").split()))
        if os.environ.get("SUDO_USERS")
        else []
    )

    AUTH_CHATS = (
        list(map(int, os.environ.get("AUTH_CHATS", "").split()))
        if os.environ.get("AUTH_CHATS")
        else []
    )

    # ──────────────── SERVER / DEPLOYMENT ────────────────
    WEB_SERVER = os.environ.get("WEB_SERVER", "True").lower() == "true"
    PING_URL = os.environ.get("PING_URL", "")
    PING_TIME = int(os.environ.get("PING_TIME", 300))
    PORT = int(os.environ.get("PORT", 8080))

    # ──────────────── BOT SETTINGS ────────────────
    PUBLIC_MODE = os.environ.get("PUBLIC_MODE", "False").lower() == "true"
    TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")

    # ──────────────── OPTIONAL API TOKENS ────────────────
    TMDB_ACCESS_TOKEN = os.environ.get("TMDB_ACCESS_TOKEN", "")

    # ──────────────── UPSTREAM AUTO-UPDATE ────────────────
    UPSTREAM_REPO = os.environ.get(
        "UPSTREAM_REPO",
        "https://github.com/XalFH/Poster-Scraper-Bot"
    )
    UPSTREAM_BRANCH = os.environ.get("UPSTREAM_BRANCH", "main")

    # ──────────────── TEMPLATES ────────────────
    OTT_TEMPLATE = """
<b>📺 Source:</b> {source}
<b>🎬 Title:</b> {title}
<b>📅 Year:</b> {year}
<b>🎞 Type:</b> {type}

<b>🔗 Original URL:</b>
<code>{original_url}</code>

<b>🖼 Posters:</b>
{poster_lines}
""".strip()

    IMDB_TEMPLATE = """
<b>🎬 {title}</b> <i>({year})</i>

⭐ <b>Rating:</b> <code>{rating}</code>
🎭 <b>Genre:</b> {genres}
🗣 <b>Language:</b> {languages}
🌍 <b>Country:</b> {countries}
📅 <b>Release:</b> {release_date}

<b>👥 Cast:</b> {cast}
🎬 <b>Director:</b> {director}
🧠 <b>Writer:</b> {writer}

🕒 <b>Runtime:</b> {runtime}
📦 <b>Box Office:</b> {box_office}
🎥 <b>Type:</b> {kind}

<b>📝 Story:</b>
<blockquote>{plot}</blockquote>

🔗 <b>IMDb:</b> {url}
"""

    ANILIST_TEMPLATE = """
<b>🎌 {title}</b> <i>({year})</i>
<code>{romaji}</code>
{native}

🛰 <b>Status:</b> {status} • {season}
🎬 <b>Format:</b> {format}
📺 <b>Episodes:</b> {episodes} × {duration}
⭐ <b>Score:</b> <code>{score}</code>
📈 <b>Popularity:</b> {popularity}

<b>📝 Synopsis:</b>
<blockquote>{description}</blockquote>
"""

    BYPASS_TEMPLATE = """
<b>✦ Bypass Result ✦</b>

{header_block}

{meta_block}
<b>╭╴Links:</b>
{links_block}

<b>✺ Original URL:</b>
<code>{original_url}</code>
""".strip()

    POSER_TEMPLATE = """
{title}

{landscape}

• Logos PNG:
<blockquote expandable>
{logos}
</blockquote>

• Portrait Posters:
<blockquote expandable>
{posters}
</blockquote>
""".strip()
