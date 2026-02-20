import os
import asyncio
import re
from pyrogram import Client, filters, idle
from pyrogram.errors import PeerIdInvalid, FloodWait

# ----------------- [ CONFIG ] -----------------
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

SOURCE_CHANNELS = [-1002983885867, -1003592065071]
TARGET_CHANNELS = [-1002969272951, -1003735167884]

PROMO_TEXT = "\n\n**USE THIS BOT TMKOC EPISODE:- @AutoMovie_Filter_Bot**"

# ----------------- [ CLEANER LOGIC ] -----------------
def clean_text(text: str) -> str:
    if not text: return ""
    
    # 1. Sabse pehle saare links udao (http aur t.me/...)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"t\.me/\S+", "", text)
    
    # 2. Backup channel, Join us, Link jaise words udao (Case insensitive)
    # Ye un lines ko uda dega jisme backup channel likha ho
    bad_words = ["backup channel", "backup", "join", "link", "channel link", "subscribe"]
    for word in bad_words:
        # Line by line check karke uda dega
        text = re.compile(re.escape(word) + r".*", re.IGNORECASE).sub("", text)

    # 3. Usernames (@bot, @channel) udao
    text = re.sub(r"@\S+", "", text)
    
    # 4. Faltu symbols aur extra spaces udao
    text = re.sub(r"[:\-👉➡📌✅]+", "", text) # Ye symbols jo aksar link ke aage hote hain
    
    # 5. Multiple empty lines ko single line mein badlo
    text = re.sub(r"\n\s*\n", "\n", text)
    
    return text.strip()

# ----------------- [ SETUP ] -----------------
app = Client("TMKOC_Fix_Bot", API_ID, API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.video)
async def main_handler(client, message):
    if message.chat.id not in SOURCE_CHANNELS:
        return

    try:
        cap = message.caption or ""
        fname = message.video.file_name or ""
        combined = f"{cap} {fname}".lower()
        
        # Detection
        if not any(x in combined for x in ["taarak", "mehta", "tmkoc", "ooltah"]):
            return

        # Yahan cleaning ho rahi hai
        cleaned_body = clean_text(cap)
        
        # Agar cleaning ke baad kuch na bache, toh filename use karo
        final_body = cleaned_body if cleaned_body else fname
        
        # Aapka Bold Promo
        final_cap = f"{final_body}{PROMO_TEXT}"

        print(f"✅ Cleaned & Forwarding: {fname[:20]}...")

        for target in TARGET_CHANNELS:
            try:
                await message.copy(chat_id=target, caption=final_cap)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ Error in {target}: {e}")

    except Exception as e:
        print(f"⚠️ Handler Error: {e}")

async def start_bot():
    await app.start()
    print("🚀 BOT STARTED & CLEANER ACTIVE!")
    await idle()

if __name__ == "__main__":
    app.run(start_bot())
    
