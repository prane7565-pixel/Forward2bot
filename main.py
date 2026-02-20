import os
import asyncio
import re
from pyrogram import Client, filters, idle

# ---------- ENV ----------
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

# ---------- CHANNELS ----------
# Private channel ID sahi hai, bas ensure karein ki aapka account usme Joined hai.
SOURCE_CHANNELS = [-1002983885867, -1003592065071]
TARGET_CHANNELS = [-1002969272951, -1003735167884]

# ---------- CONFIG ----------
PROMO_TEXT = "\n\n**USE THIS BOT TMKOC EPISODE:- @AutoMovie_Filter_Bot**"

# User Session Client
app = Client(
    "tmkoc_user_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    session_string=SESSION_STRING
)

def clean_caption(caption: str) -> str:
    if not caption:
        return ""
    # Links aur @usernames hatane ke liye
    text = re.sub(r"https?://t\.me/\S+", "", caption)
    text = re.sub(r"t\.me/\S+", "", text)
    text = re.sub(r"@\S+", "", text)
    return text.strip()

# filters.video ensure karta hai ki sirf video forward ho, text nahi
@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.video)
async def auto_forward(client, message):
    try:
        caption = message.caption or ""
        file_name = (message.video.file_name if message.video else "") or ""
        
        # 1. TMKOC Detection Logic
        search_text = f"{caption} {file_name}".lower()
        keywords = ["taarak", "mehta", "tmkoc", "ooltah", "chashmah"]
        
        if not any(word in search_text for word in keywords):
            return # Agar TMKOC ka video nahi hai toh skip

        # 2. Caption Cleaning
        cleaned_text = clean_caption(caption)
        
        # 3. Fallback: Agar caption khali hai toh file_name use karein
        if not cleaned_text:
            cleaned_text = file_name if file_name else "Taarak Mehta Ka Ooltah Chashmah"

        # 4. Final Formatting with Bold Promo
        final_caption = f"{cleaned_text}{PROMO_TEXT}"

        print(f"✅ TMKOC Video Mil Gaya: {file_name}")

        for target in TARGET_CHANNELS:
            try:
                # Copy use karne se original caption hat kar naya caption lag jayega
                await message.copy(
                    chat_id=target,
                    caption=final_caption
                )
                await asyncio.sleep(2) # Flood safety
            except Exception as e:
                print(f"❌ Target {target} par bhejne mein error: {e}")
                
    except Exception as e:
        print(f"❌ Error in handler: {e}")

if __name__ == "__main__":
    print("==========================================")
    print("TMKOC USER-BOT STARTED (SESSION STRING)")
    print("==========================================")
    app.run()
    
