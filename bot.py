import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from flask import Flask
from threading import Thread

# --- RENDER STABILITY SYSTEM ---
app = Flask('')
@app.route('/')
def home(): return "Bot is online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()

# --- DATABASE SETTINGS ---
SETTINGS_FILE = "settings.json"
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f: json.dump(data, f)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f: return json.load(f)
        except: return {"welcome": {}, "leave": {}}
    return {"welcome": {}, "leave": {}}

# --- BOT CONFIGURATION ---
class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True          
        intents.message_content = True  
        super().__init__(command_prefix="!", intents=intents)
        self.data = load_settings()

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Commands Synced")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"🚀 {bot.user} is connected.")

def get_welcome_embed(member):
    embed = discord.Embed(title="✨ Welcome!", description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\nMember #**{member.guild.member_count}**.", color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)
    return embed

def get_leave_box(member):
    return f"
http://googleusercontent.com/immersive_entry_chip/0

**Once you save these changes, Render will automatically rebuild. Does it show "Live" in green now?**
http://googleusercontent.com/immersive_entry_chip/0
