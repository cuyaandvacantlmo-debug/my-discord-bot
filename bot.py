import discord
from discord.ext import commands
from discord import app_commands
import os
import json
from flask import Flask
from threading import Thread

# Web Server
app = Flask('')
@app.route('/')
def home(): return "Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
keep_alive()

# Database
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

def l_box(m):
    return f"```\n{m.name} has left the server.\n```"

@bot.event
async def on_member_join(m):
    c = bot.data["welcome"].get(str(m.guild.id))
    if c:
        ch = bot.get_channel(int(c))
        if ch: await ch.send(embed=w_emb(m))

@bot.event
async def on_member_remove(m):
    c = bot.data["leave"].get(str(m.guild.id))
    if c:
        ch = bot.get_channel(int(c))
        if ch: await ch.send(l_box(m))

@bot.tree.command(name="welcomer")
async def welcomer(i, channel: discord.TextChannel):
    bot.data["welcome"][str(i.guild.id)] = channel.id
    save(bot.data)
    await i.response.send_message(f"The welcomer channel has been set to {channel.mention}", ephemeral=True)

@bot.tree.command(name="leaver")
async def leaver(i, channel: discord.TextChannel):
    bot.data["leave"][str(i.guild.id)] = channel.id
    save(bot.data)
    await i.response.send_message(f"The leaver channel has been set to {channel.mention}", ephemeral=True)

@bot.tree.command(name="say")
async def say(i, text: str):
    await i.response.send_message("Sent", ephemeral=True)
    await i.channel.send(f"```\n{text}\n```")

@bot.tree.command(name="welcomertest")
async def wtest(i):
    await i.channel.send(embed=w_emb(i.user))
    await i.response.send_message("Test sent", ephemeral=True)

@bot.tree.command(name="leavertest")
async def ltest(i):
    await i.channel.send(l_box(i.user))
    await i.response.send_message("Test sent", ephemeral=True)

# THE SCRIPT ENDS EXACTLY ON THE LINE BELOW
bot.run(os.environ.get('DISCORD_TOKEN'))

