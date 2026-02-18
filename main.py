import os
import asyncio
import re
from pyrogram import Client, filters, idle

print("TMKOC FINAL BOT starting...")

# ---------- ENV (Railway Safe) ----------
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# ---------- CHANNELS ----------
SOURCE_CHANNELS = [
    -1002983885867,   # Main source
    -1003592065071    # Testing source
]

TARGET_CHANNELS = [
    -1002969272951,
    -1003735167884
]

# ---------- CLIENT ----------
app = Client(
    "tmkoc_bot_final",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

# ---------- REGEX ----------
EP_REGEX = re.compile(r"(?:ep|episode)[\s\.\-_]*?(\d+)", re.IGNORECASE)

# ---------- CLEANER ----------
def remove_backup_links(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"https?://t\.me/\S+", "", text)
    text = re.sub(r"t\.me/\S+", "", text)
    text = re.sub(r"backup\s*channel\s*[-:]*", "", text, flags=re.I)
    return text.strip()

# ---------- HANDLER ----------
@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.video)
async def auto_forward(client, message):

    caption = message.caption or ""
    filename = message.video.file_name or ""

    combined_text = f"{caption} {filename}".lower()

    # Must contain TMKOC identity
    if not ("taarak" in combined_text and "mehta" in combined_text):
        return

    ep_match = EP_REGEX.search(combined_text)
    if not ep_match:
        return

    episode_number = ep_match.group(1)

    # FINAL CLEAN CAPTION (ALWAYS SAME FORMAT)
    final_caption = (
        "Taarak Mehta Ka Ooltah Chashmah\n"
        f"Episode {episode_number}"
    )

    print(f"✅ Forwarding Episode {episode_number}")

    for target in TARGET_CHANNELS:
        try:
            await message.copy(
                chat_id=target,
                caption=final_caption
            )
            await asyncio.sleep(2)  # flood safety
        except Exception as e:
            print(f"❌ Error sending to {target}: {e}")

# ---------- START ----------
async def main():
    await app.start()
    print("================================================")
    print("✅ TMKOC FINAL BOT READY (NO CRASH MODE)")
    print("================================================")
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())





 
