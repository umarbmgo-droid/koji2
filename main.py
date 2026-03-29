import discord
from discord.ext import commands
import os
import json
import aiohttp
import asyncio
import time
from datetime import datetime, timedelta
from typing import Optional

# ===== CONFIG =====
TOKEN = os.environ.get('TOKEN')
OWNER_ID = 361069640962801664
START_TIME = time.time()
SUPPORT_SERVER = "discord.gg/ekittens"
BOT_NAME = "koji"
BOT_PFP_URL = "https://i.pinimg.com/1200x/5b/4e/28/5b4e2808b89937b39b63a89d759119bd.jpg"
BOT_BANNER_URL = "https://i.pinimg.com/originals/7f/eb/24/7feb24f573c4950b5fde5b883c731b1c.gif"

# ===== GLOBAL DATA =====
data = {
    'whitelist': [],
    'isolated': {},
    'logs_channel': {},
    'auto_react': {},
    'admins': [],
    'custom_prefix': {},
    'disabled_commands': {},
    'disabled_modules': {},
    'ignored_channels': {},
    'ignored_roles': {},
    'auto_roles': {},
    'welcome_channel': {},
    'goodbye_channel': {},
    'starboard': {},
    'reaction_roles': {},
    'economy': {},
    'warns': {},
    'mutes': {},
    'bans': {},
    'reminders': {},
    'afk': {},
    'snipe': {},
    'editsnipe': {},
    'reactionsnipe': {},
    'purgesnipe': {}
}

def load_data():
    global data
    try:
        with open('data.json', 'r') as f:
            loaded = json.load(f)
            data.update(loaded)
    except:
        pass

def save_data():
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

load_data()

# ===== BOT SETUP =====
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# Store bot functions for cogs
bot.data = data
bot.save_data = save_data
bot.owner_id = OWNER_ID
bot.get_uptime = lambda: get_uptime()
bot.is_whitelisted = lambda uid: uid in data['whitelist'] or uid == OWNER_ID
bot.get_prefix_custom = lambda guild: data['custom_prefix'].get(str(guild.id), ".") if guild else "."
bot.support_server = SUPPORT_SERVER
bot.bot_name = BOT_NAME
bot.banner_url = BOT_BANNER_URL

# ===== HELPER FUNCTIONS =====
def get_uptime():
    uptime = int(time.time() - START_TIME)
    days = uptime // 86400
    hours = (uptime % 86400) // 3600
    minutes = (uptime % 3600) // 60
    seconds = uptime % 60
    parts = []
    if days > 0: parts.append(f"{days}d")
    if hours > 0: parts.append(f"{hours}h")
    if minutes > 0: parts.append(f"{minutes}m")
    parts.append(f"{seconds}s")
    return " ".join(parts)

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

# ===== LOAD COGS =====
async def load_cogs():
    cog_files = [
        'moderation', 'economy', 'fun', 'information', 'utility',
        'snipe', 'security', 'music', 'reaction', 'server_config', 'help_commands'
    ]
    
    for cog in cog_files:
        try:
            await bot.load_extension(f'cogs.{cog}')
            print(f"✅ Loaded cog: {cog}.py")
        except Exception as e:
            print(f"❌ Failed to load cog {cog}.py: {e}")

# ===== BASIC COMMANDS (Only essential - NO HELP COMMAND) =====
@bot.command(name="test")
async def test_command(ctx):
    """Test if bot is working"""
    await ctx.send("Test command works! The bot is receiving messages!")

@bot.command(name="ping")
async def ping(ctx):
    """Check bot latency"""
    embed = discord.Embed(description=f"Pong! `{round(bot.latency * 1000)}ms`", color=0xdc143c)
    await ctx.send(embed=embed)

# ===== SLASH COMMANDS =====
@bot.tree.command(name="ping", description="Check bot latency")
async def slash_ping(interaction: discord.Interaction):
    embed = discord.Embed(description=f"Pong! `{round(bot.latency * 1000)}ms`", color=0xdc143c)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="react", description="[OWNER] Add auto-reactions to a user")
async def react_add(interaction: discord.Interaction, user: discord.Member, emoji1: str, emoji2: Optional[str] = None, emoji3: Optional[str] = None, emoji4: Optional[str] = None):
    if interaction.user.id != OWNER_ID:
        embed = discord.Embed(description="Only the owner can use this command", color=0xdc143c)
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    emojis = [e for e in [emoji1, emoji2, emoji3, emoji4] if e]
    data['auto_react'][str(user.id)] = emojis
    save_data()
    embed = discord.Embed(description=f"Now auto-reacting to {user.mention} with {' '.join(emojis)}", color=0xdc143c)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="whitelist", description="[OWNER] Whitelist a user from security features")
async def whitelist_user(interaction: discord.Interaction, user: discord.Member):
    if interaction.user.id != OWNER_ID:
        embed = discord.Embed(description="Only the owner can use this command", color=0xdc143c)
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    if user.id not in data['whitelist']:
        data['whitelist'].append(user.id)
        save_data()
        embed = discord.Embed(description=f"✅ {user.mention} has been whitelisted", color=0xdc143c)
    else:
        embed = discord.Embed(description=f"❌ {user.mention} is already whitelisted", color=0xdc143c)
    await interaction.response.send_message(embed=embed)

# ===== ON_MESSAGE =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    # AFK system
    if str(message.author.id) in data['afk']:
        del data['afk'][str(message.author.id)]
        save_data()
        await message.channel.send(f"Welcome back {message.author.mention}!")
    
    for mention in message.mentions:
        if str(mention.id) in data['afk']:
            await message.channel.send(f"{mention.name} is AFK: {data['afk'][str(mention.id)]}")
    
    # Snipe
    if message.content:
        data['snipe'][message.channel.id] = {
            'content': message.content,
            'author': message.author.name,
            'timestamp': datetime.now().isoformat()
        }
        save_data()
    
    # Auto-react
    if str(message.author.id) in data['auto_react']:
        for emoji in data['auto_react'][str(message.author.id)]:
            try:
                await message.add_reaction(emoji)
            except:
                pass
    
    await bot.process_commands(message)

# ===== ON_READY =====
@bot.event
async def on_ready():
    print("="*50)
    print(f"✅ {BOT_NAME.upper()} IS ONLINE")
    print(f"🤖 Bot ID: {bot.user.id}")
    print(f"📊 Servers: {len(bot.guilds)}")
    
    # Set Bot Avatar
    try:
        avatar_data = await download_image(BOT_PFP_URL)
        if avatar_data:
            await bot.user.edit(avatar=avatar_data)
            print(f"🖼️ Avatar set")
    except Exception as e:
        print(f"Avatar error: {e}")
    
    # Set streaming status
    await bot.change_presence(activity=discord.Streaming(
        name=SUPPORT_SERVER,
        url="https://www.twitch.tv/ekittens"
    ))
    
    # Load all cogs
    await load_cogs()
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands")
    except Exception as e:
        print(f"Failed to sync: {e}")
    
    print(f"📝 Total prefix commands: {len(bot.commands)}")
    print("="*50)

# ===== RUN BOT =====
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No token found!")
        exit(1)
    
    print(f"🚀 Starting {BOT_NAME}...")
    bot.run(TOKEN)
