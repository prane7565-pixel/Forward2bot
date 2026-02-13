import os
import asyncio
import re  # Ye naya tool hai jo "Ep + Number" dhundega
from pyrogram import Client, filters, idle

print("Bot start hone ki koshish kar raha hai...")

# --- RAILWAY VARIABLES CHECKER ---
API_ID_STR = os.environ.get("API_ID", "").strip()
API_HASH = os.environ.get("API_HASH", "").strip()
SESSION_STRING = os.environ.get("SESSION_STRING", "").strip()

if not API_ID_STR or not API_HASH or not SESSION_STRING:
    print("❌ ERROR: Railway Variables missing hain!")
    exit()

try:
    API_ID = int(API_ID_STR)
except ValueError:
    print("❌ ERROR: 'API_ID' mein sirf numbers hone chahiye!")
    exit()

# --- CHANNEL CONFIGURATION ---
SOURCE_CHANNELS = [
    -1002983885867,  # Main Source
    -1003592065071   # Testing Source
]

TARGET_CHANNELS = [
    -1002969272951,  # Target 1
    -1003735167884   # Target 2 (Agar ye abhi bhi fail ho raha hai, toh yahan Link daal dena)
]

# Basic Keywords (Inme se koi 2 hone chahiye)
REQUIRED_KEYWORDS = ["taarak", "mehta", "ooltah", "chashmah"]

# Client Setup
app = Client("tmkoc_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.video)
async def auto_forward(client, message):
    
    caption = message.caption if message.caption else ""
    file_name = message.video.file_name if message.video.file_name else ""
    
    # Text ko lowercase karte hain check karne ke liye
    search_text = (caption + " " + file_name).lower()
    
    # STEP 1: Check Keywords ("Taarak" aur "Mehta" hai ya nahi?)
    keyword_matches = 0
    for word in REQUIRED_KEYWORDS:
        if word in search_text:
            keyword_matches += 1
            
    # STEP 2: Check Episode Number (Ep4631, Episode 123, Ep. 450 etc.)
    # Ye pattern dhundega: "ep" ya "episode" ke baad koi number
    ep_match = re.search(r"(?:ep|episode)[\s\.]*?(\d+)", search_text)
    
    # FINAL DECISION:
    # Keywords bhi match hone chahiye (>=2) AUR Episode number bhi milna chahiye
    if keyword_matches >= 2 and ep_match:
        
        episode_num = ep_match.group(1) # Episode number nikal liya
        print(f"✅ FOUND: Taarak Mehta Episode {episode_num} detected!")
        print(f"File: {file_name}")
        
        for target_id in TARGET_CHANNELS:
            try:
                await message.copy(chat_id=target_id)
                print(f"➡️ Sent to {target_id}")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ Error sending to {target_id}: {e}")
                
    else:
        # Agar Keywords mile par Episode number nahi mila, toh ignore
        if keyword_matches >= 2 and not ep_match:
            print(f"⚠️ Ignored: 'Taarak Mehta' mila par 'Ep Number' nahi mila. (File: {file_name})")
        else:
            # Agar kuch bhi match nahi hua
            pass

# --- SMART STARTUP ---
async def main():
    print("🔄 Telegram servers se connect kar rahe hain...")
    await app.start()
    print("==================================================")
    print("✅ BOT READY: Sirf 'Ep + Number' wali files forward hongi!")
    print("==================================================")
    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(main())




 
