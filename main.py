import os
import asyncio
from pyrogram import Client, filters

print("Bot start hone ki koshish kar raha hai...")

# --- RAILWAY VARIABLES CHECKER ---
# Ye check karega ki aapne Railway variables sahi se daale hain ya nahi
API_ID_STR = os.environ.get("API_ID", "").strip()
API_HASH = os.environ.get("API_HASH", "").strip()
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip()

# Agar koi variable missing hai toh bot saaf error dega aur band ho jayega
if not API_ID_STR:
    print("❌ ERROR: Railway Variables mein 'API_ID' missing hai!")
    exit()
if not API_HASH:
    print("❌ ERROR: Railway Variables mein 'API_HASH' missing hai!")
    exit()
if not SESSION_STRING:
    print("❌ ERROR: Railway Variables mein 'SESSION_STRING' missing hai!")
    exit()

# API ID ko number (integer) mein convert karna zaroori hai
try:
    API_ID = int(API_ID_STR)
except ValueError:
    print("❌ ERROR: 'API_ID' mein sirf numbers hone chahiye! ABCD mat daalo.")
    exit()

# --- CHANNEL CONFIGURATION ---
SOURCE_CHANNELS = [
    -1002983885867,  # Main Source
    -1003592065071   # Testing Source
]

TARGET_CHANNELS = [
    -1002969272951,  # Target 1
    -1003735167884   # Target 2
]

REQUIRED_KEYWORDS = ["taarak", "mehta", "ooltah", "chashmah"]

print("✅ Variables mil gaye! Telegram se connect kar rahe hain...")

# Client Setup
app = Client("tmkoc_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.video)
async def auto_forward(client, message):
    
    caption = message.caption if message.caption else ""
    file_name = message.video.file_name if message.video.file_name else ""
    
    search_text = (caption + " " + file_name).lower()
    
    matches = 0
    for word in REQUIRED_KEYWORDS:
        if word in search_text:
            matches += 1
            
    if matches >= 2:
        print(f"✅ Video Found: {file_name[:20]}... Forwarding now!")
        for target_id in TARGET_CHANNELS:
            try:
                await message.copy(chat_id=target_id)
                print(f"➡️ Sent to {target_id}")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ Error sending to {target_id}: {e}")
    else:
        print(f"⚠️ Ignored: Ye TMKOC ki video nahi hai. ({file_name[:20]}...)")

if __name__ == "__main__":
    app.run()
