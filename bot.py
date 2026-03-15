import discord
from discord import app_commands
from discord.ext import commands
import json
import os

# --- DATABASE LOGIC ---
# This part makes sure the bot remembers your channels after a restart
def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            return json.load(f)
    return {"welcome": None, "leave": None}

def save_settings(data):
    with open("settings.json", "w") as f:
        json.dump(data, f)

class GlitchBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True 
        super().__init__(command_prefix=None, intents=intents) 
        self.server_settings = load_settings()

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Logged in as {self.user} | Memory Loaded!")

bot = GlitchBot()

# --- SLASH COMMANDS ---

@bot.tree.command(name="welcomer", description="Set the channel for welcome messages")
async def welcomer(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.server_settings["welcome"] = channel.id
    save_settings(bot.server_settings) # Save to file
    await interaction.response.send_message(f"✅ Welcome channel set to {channel.mention}", ephemeral=True)

@bot.tree.command(name="leaver", description="Set the channel for leave messages")
async def leaver(interaction: discord.Interaction, channel: discord.TextChannel):
    bot.server_settings["leave"] = channel.id
    save_settings(bot.server_settings) # Save to file
    await interaction.response.send_message(f"✅ Leave channel set to {channel.mention}", ephemeral=True)

# --- TEST COMMANDS ---

@bot.tree.command(name="welcomertest", description="Test the welcome message")
async def welcomertest(interaction: discord.Interaction):
    if not bot.server_settings["welcome"]:
        return await interaction.response.send_message("❌ Use /welcomer first!", ephemeral=True)
    await on_member_join(interaction.user)
    await interaction.response.send_message("Welcome test sent!", ephemeral=True)

@bot.tree.command(name="leavertest", description="Test the leave message")
async def leavertest(interaction: discord.Interaction):
    if not bot.server_settings["leave"]:
        return await interaction.response.send_message("❌ Use /leaver first!", ephemeral=True)
    await on_member_remove(interaction.user)
    await interaction.response.send_message("Leave test sent!", ephemeral=True)

# --- AUTO EVENTS (Avatar Based) ---

@bot.event
async def on_member_join(member):
    channel_id = bot.server_settings.get("welcome")
    if channel_id:
        channel = bot.get_channel(channel_id)
        count = len(member.guild.members)
        embed = discord.Embed(
            title="Welcome to GLITCH",
            description=f"Welcome {member.mention}!\nYou are member **#{count}**",
            color=0x00FF00 # Neon Green
        )
        embed.set_image(url=member.display_avatar.url)
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel_id = bot.server_settings.get("leave")
    if channel_id:
        channel = bot.get_channel(channel_id)
        embed = discord.Embed(
            title="A Glitch Has Been Fixed",
            description=f"**{member.name}** has left the server.",
            color=0xFF0000 # Neon Red
        )
        embed.set_image(url=member.display_avatar.url)
        await channel.send(embed=embed)

bot.run("MTQ4MjU1NzM0OTY1MzkwOTYyNQ.GbFvzf.1TJ-bF73qYoesXO2eM3YYI2xSYGBpiioWYBHSY")

