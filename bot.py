import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# --- RENDER KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

keep_alive()
# -------------------------

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# --- THE CODE BOX SAY COMMAND ---
@bot.tree.command(name="say", description="Make the bot say something in a code box")
@app_commands.describe(text="The message you want to put in the box")
async def say(interaction: discord.Interaction, text: str):
    # This wraps your text in triple backticks to create the code box
    code_box_message = f"```\n{text}\n```"
    
    # We use a 'hidden' response to confirm it worked
    await interaction.response.send_message("Message sent!", ephemeral=True)
    
    # Send the code box to the channel
    await interaction.channel.send(code_box_message)

# --- TOKEN BOOT ---
token = os.environ.get('DISCORD_TOKEN')
if token:
    bot.run(token)
else:
    print("Missing DISCORD_TOKEN in Render Environment Variables!")
