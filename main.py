import os
import asyncio
from pyrogram import Client, filters

# --- RAILWAY VARIABLES ---
# Railway ki Settings > Variables mein ye teeno cheezein daalni hongi
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STRING = os.environ.get("SESSION_STRING", "")

# --- CHANNEL CONFIGURATION ---

# Jahan se episode uthana hai (Main + Testing Channel)
SOURCE_CHANNELS = [
    -1002983885867,  # Main Source
    -1003592065071   # Testing Source
]

# Jahan episode bhejna hai (Tumhare 2 channels)
TARGET_CHANNELS = [
    -1002969272951,  # Target 1
    -1003735167884   # Target 2
]

# --- FILTER LOGIC ---
# Ye words file name ya caption me hone chahiye tabhi forward hoga
REQUIRED_KEYWORDS = ["taarak", "mehta", "ooltah", "chashmah"]

print("Bot Start Ho Raha Hai... Monitoring Shuru!")

if not SESSION_STRING:
    print("Error: SESSION_STRING nahi mila! Railway Variables check karo.")

app = Client("tmkoc_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# Yahan 'filters.video' laga hai via 'AND (&)' operator.
# Iska matlab: Message Source Channel se hona chahiye AUR wo Video hona chahiye.
# Text messages yahan automatically reject ho jayenge.
@app.on_message(filters.chat(SOURCE_CHANNELS) & filters.video)
async def auto_forward(client, message):
    
    # Caption aur File Name dono check karenge
    caption = message.caption if message.caption else ""
    file_name = message.video.file_name if message.video.file_name else ""
    
    # Dono ko lowercase karke combine kar rahe hain searching ke liye
    search_text = (caption + " " + file_name).lower()
    
    # Check: Kya ye waqai TMKOC ka episode hai?
    # Logic: Kam se kam 2 keywords match hone chahiye (e.g. 'taarak' aur 'mehta')
    matches = 0
    for word in REQUIRED_KEYWORDS:
        if word in search_text:
            matches += 1
            
    if matches >= 2:
        print(f"✅ Video Found: {file_name[:20]}... Forwarding now!")
        
        for target_id in TARGET_CHANNELS:
            try:
                # copy() method use karne se 'Forwarded from' tag nahi aata
                await message.copy(chat_id=target_id)
                print(f"➡️ Sent to {target_id}")
                
                # Safety ke liye 2 second ka gap
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"❌ Error sending to {target_id}: {e}")
    else:
        # Agar video aayi par wo TMKOC nahi hai (koi aur serial ya ad)
        print(f"⚠️ Ignored Video: Keywords match nahi huye. ({file_name})")

if __name__ == "__main__":
    app.run()
