import discord
from discord.ext import commands
from discord import app_commands
import os
from flask import Flask
from threading import Thread

# --- RENDER STABILITY SYSTEM ---
# This tiny web server keeps Render from shutting down the bot.
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running!"

def run():
    # Use the port Render provides or default to 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# Start the web server
keep_alive()

# --- BOT CONFIGURATION ---
class MyBot(commands.Bot):
    def __init__(self):
        # We need these intents to see members joining and to read messages
        intents = discord.Intents.default()
        intents.members = True          
        intents.message_content = True  
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # This syncs your / commands so they appear on Discord mobile/desktop
        await self.tree.sync()
        print(f"✅ Slash commands synced for {self.user}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f"🚀 {bot.user} is online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the server"))

# --- AUTOMATIC WELCOMER ---
@bot.event
async def on_member_join(member):
    # Searches for a channel named 'welcome'
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if channel:
        embed = discord.Embed(
            title="👋 Welcome!",
            description=f"Hey {member.mention}, welcome to **{member.guild.name}**!\nYou are our **{member.guild.member_count}th** member.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"ID: {member.id}")
        await channel.send(embed=embed)

# --- AUTOMATIC LEAVER ---
@bot.event
async def on_member_remove(member):
    # Searches for a channel named 'leaves'
    channel = discord.utils.get(member.guild.text_channels, name="leaves")
    if channel:
        # Sends the leave message in a code box as requested
        leave_text = f"```\n{member.name} has left the server.\nWe now have {member.guild.member_count} members.\n```"
        await channel.send(leave_text)

# --- COMMAND: SAY (CODE BOX STYLE) ---
@bot.tree.command(name="say", description="Make the bot say something inside a code box")
@app_commands.describe(text="The message you want the bot to say")
async def say(interaction: discord.Interaction, text: str):
    # This sends an invisible confirmation to you
    await interaction.response.send_message("Message sent!", ephemeral=True)
    # This sends the message in a code block to the channel
    await interaction.channel.send(f"```\n{text}\n```")

# --- COMMAND: SETUP ---
@bot.tree.command(name="setup", description="Automatically create the welcome and leaves channels")
async def setup(interaction: discord.Interaction):
    # Defer since creating channels can take a second
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    
    status = []
    # Check/Create Welcome
    if not discord.utils.get(guild.text_channels, name="welcome"):
        await guild.create_text_channel("welcome")
        status.append("Created #welcome")
    else:
        status.append("#welcome already exists")

    # Check/Create Leaves
    if not discord.utils.get(guild.text_channels, name="leaves"):
        await guild.create_text_channel("leaves")
        status.append("Created #leaves")
    else:
        status.append("#leaves already exists")

    await interaction.followup.send("\n".join(status))

# --- BOOT THE BOT ---
# Get your token from Render Environment Variables
token = os.environ.get('DISCORD_TOKEN')

if token:
    bot.run(token)
else:
    print("❌ ERROR: No DISCORD_TOKEN found. Check your Render Environment tab!")
