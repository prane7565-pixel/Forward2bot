import os
import asyncio
import re
from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait

# ----------------- [ CONFIG ] -----------------
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# SOURCES
SOURCE_IDS = {-1003592065071}              # Testing
SOURCE_USERNAMES = {"tmkocepisodedaily1"}  # Public episode channel

# TARGETS
TARGET_CHANNELS = [
    "@tmkocdirect",        # Main public channel
    -1003735167884         # Database channel
]

PROMO_TEXT = "\n\n**USE THIS BOT TMKOC EPISODE:- @AutoMovie_Filter_Bot**"

# ----------------- [ CLEANER ] -----------------
def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"t\.me/\S+", "", text)

    bad_words = ["backup", "join", "link", "subscribe"]
    for word in bad_words:
        text = re.compile(re.escape(word) + r".*", re.IGNORECASE).sub("", text)

    text = re.sub(r"@\S+", "", text)
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()

# ----------------- [ APP ] -----------------
app = Client("TMKOC_Fix_Bot", API_ID, API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.video)
async def handler(client, message):
    chat = message.chat

    # ✅ 100% reliable source detection
    if chat.id not in SOURCE_IDS and (
        not chat.username or chat.username.lower() not in SOURCE_USERNAMES
    ):
        return

    try:
        cap = message.caption or ""
        fname = message.video.file_name or ""
        combined = f"{cap} {fname}".lower()

        # TMKOC detection
        if not any(x in combined for x in ["taarak", "mehta", "tmkoc", "ooltah"]):
            return

        body = clean_text(cap)
        final_text = body if body else fname
        final_caption = f"{final_text}{PROMO_TEXT}"

        print(f"🚀 Forwarding: {fname[:30]}")

        for target in TARGET_CHANNELS:
            try:
                await message.copy(chat_id=target, caption=final_caption)
                await asyncio.sleep(10)  # SAFE delay
            except FloodWait as e:
                await asyncio.sleep(e.value)

    except Exception as e:
        print(f"❌ Error: {e}")

async def start():
    await app.start()
    print("✅ BOT STARTED — FULLY STABLE MODE")
    await idle()

if __name__ == "__main__":
    app.run(start())
