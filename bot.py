import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
keep_alive()

S_FILE = "settings.json"
def save(d):
    with open(S_FILE, "w") as f: json.dump(d, f)
def load():
    if os.path.exists(S_FILE):
        try:
            with open(S_FILE, "r") as f: return json.load(f)
        except: pass
    return {"welcome": {}, "leave": {}}

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)
        self.data = load()
    async def setup_hook(self): await self.tree.sync()
bot = MyBot()

def w_emb(m):
    e = discord.Embed(title="✨ Welcome!", description=f"Welcome {m.mention} to {m.guild.name}!\nMember #{m.guild.member_count}", color=0x00ff00)
    e.set_thumbnail(url=m.display_avatar.url)
    return e
