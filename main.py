import discord
from discord.ext import commands
import os

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True  # For say/announce

bot = commands.Bot(command_prefix="!", intents=intents)

# Load slash commands to specific guild
GUILD_ID = int(os.getenv("GUILD_ID"))

@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"[✅] Logged in as {bot.user}")
    print("[⚙️] Slash commands synced.")

# Load all cogs
initial_extensions = [
    "cogs.moderation",
    "cogs.welcome",
    "cogs.utility",
    "cogs.logging_system",
    "cogs.security"
]

for ext in initial_extensions:
    try:
        bot.load_extension(ext)
        print(f"[📦] Loaded {ext}")
    except Exception as e:
        print(f"[❌] Failed to load {ext}: {e}")

# Start keep-alive server
keep_alive()

# Run the bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
