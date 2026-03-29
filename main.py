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
PREFIX_DEFAULT = "."

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
bot = commands.Bot(command_prefix=None, intents=intents, help_command=None)

# ===== GLOBAL HELPER FUNCTIONS =====
def get_prefix_custom(guild):
    if guild:
        return data['custom_prefix'].get(str(guild.id), PREFIX_DEFAULT)
    return PREFIX_DEFAULT

def is_whitelisted(user_id):
    return user_id in data['whitelist'] or user_id == OWNER_ID

def is_admin(user_id):
    return user_id in data['admins'] or user_id == OWNER_ID

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

def has_higher_role(member, target_role):
    if member.guild_permissions.administrator:
        return True
    if member.id == OWNER_ID:
        return True
    return member.top_role > target_role

async def log_action(guild, action, user, moderator, reason=None, extra=None):
    channel_id = data['logs_channel'].get(str(guild.id))
    if not channel_id:
        return
    channel = guild.get_channel(channel_id)
    if not channel:
        return
    embed = discord.Embed(
        title=f"Log: {action}",
        description=f"**User:** {user.mention} (`{user.id}`)\n**Moderator:** {moderator.mention}\n**Reason:** {reason or 'N/A'}",
        color=0xdc143c
    )
    if extra:
        embed.add_field(name="Extra", value=extra, inline=False)
    embed.timestamp = datetime.now()
    await channel.send(embed=embed)

async def create_isolation_role(guild):
    role = discord.utils.get(guild.roles, name="Isolation")
    if not role:
        try:
            role = await guild.create_role(
                name="Isolation",
                permissions=discord.Permissions.none(),
                reason="Auto-created isolation role"
            )
            for channel in guild.channels:
                await channel.set_permissions(role, read_messages=False)
        except:
            pass
    return role

async def isolate_user(user, duration_minutes=0, reason="No reason provided"):
    guild = user.guild
    role = await create_isolation_role(guild)
    await user.edit(roles=[role], reason=f"Isolated: {reason}")
    if duration_minutes > 0:
        data['isolated'][str(user.id)] = {
            'guild_id': guild.id,
            'end_time': (datetime.now() + timedelta(minutes=duration_minutes)).isoformat(),
            'reason': reason
        }
        save_data()
    await log_action(guild, "Isolated", user, guild.me, reason, f"Duration: {duration_minutes} minutes")
    return role

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

# ===== IMPORT COGS =====
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load cog {filename}: {e}")

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"✅ {BOT_NAME.upper()} IS ONLINE")
    print(f"🤖 Bot ID: {bot.user.id}")
    print(f"📊 Servers: {len(bot.guilds)}")
    
    # Set Bot Avatar
    try:
        avatar_data = await download_image(BOT_PFP_URL)
        if avatar_data:
            await bot.user.edit(avatar=avatar_data)
            print(f"🖼️ Avatar set successfully")
    except Exception as e:
        print(f"❌ Error setting avatar: {e}")
    
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

tracked_actions = {}

@bot.event
async def on_member_join(member):
    if member.bot:
        if not is_whitelisted(member.id):
            await isolate_user(member, 0, "Bot detected - automatic isolation")
            await member.kick(reason="Auto-security: bot detected")
            return
    
    guild_id = str(member.guild.id)
    if guild_id in data['auto_roles']:
        for role_id in data['auto_roles'][guild_id]:
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)
    
    if guild_id in data['welcome_channel']:
        channel = member.guild.get_channel(data['welcome_channel'][guild_id])
        if channel:
            embed = discord.Embed(
                description=f"Welcome {member.mention} to {member.guild.name}!",
                color=0xdc143c
            )
            await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    guild_id = str(member.guild.id)
    if guild_id in data['goodbye_channel']:
        channel = member.guild.get_channel(data['goodbye_channel'][guild_id])
        if channel:
            embed = discord.Embed(
                description=f"{member.name} left the server.",
                color=0xdc143c
            )
            await channel.send(embed=embed)
    await log_action(member.guild, "Member Left", member, bot.user)

@bot.event
async def on_guild_channel_delete(channel):
    if not isinstance(channel, discord.TextChannel):
        return
    guild = channel.guild
    key = f"channels_{guild.id}"
    tracked_actions[key] = tracked_actions.get(key, 0) + 1
    await asyncio.sleep(5)
    if tracked_actions.get(key, 0) >= 2:
        tracked_actions[key] = 0
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_delete):
            if entry.target == channel:
                user = entry.user
                if not is_whitelisted(user.id) and not is_admin(user.id):
                    await isolate_user(user, 0, "Mass channel deletion detected")
                    await user.kick(reason="Mass channel deletion")
                    await log_action(guild, "Auto-Kicked", user, bot.user, "Mass channel deletion")
                break

@bot.event
async def on_member_ban(guild, user):
    key = f"bans_{guild.id}"
    tracked_actions[key] = tracked_actions.get(key, 0) + 1
    await asyncio.sleep(5)
    if tracked_actions.get(key, 0) >= 2:
        tracked_actions[key] = 0
        async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.ban):
            if entry.target == user:
                banner = entry.user
                if not is_whitelisted(banner.id) and not is_admin(banner.id):
                    await isolate_user(banner, 0, "Mass banning detected")
                    await banner.kick(reason="Mass banning")
                    await log_action(guild, "Auto-Kicked", banner, bot.user, "Mass banning")
                break

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if str(message.author.id) in data['afk']:
        afk_data = data['afk'][str(message.author.id)]
        del data['afk'][str(message.author.id)]
        save_data()
        embed = discord.Embed(
            description=f"Welcome back {message.author.mention}! You were AFK for {afk_data['duration']}.",
            color=0xdc143c
        )
        await message.channel.send(embed=embed, delete_after=10)
    
    for mention in message.mentions:
        if str(mention.id) in data['afk']:
            afk_data = data['afk'][str(mention.id)]
            embed = discord.Embed(
                description=f"{mention.name} is AFK: {afk_data['reason']}",
                color=0xdc143c
            )
            await message.channel.send(embed=embed, delete_after=10)
    
    if message.content:
        data['snipe'][message.channel.id] = {
            'content': message.content,
            'author': message.author.name,
            'author_id': message.author.id,
            'timestamp': datetime.now().isoformat()
        }
        save_data()
    
    if str(message.author.id) in data['auto_react']:
        for emoji in data['auto_react'][str(message.author.id)]:
            try:
                await message.add_reaction(emoji)
            except:
                pass
    
    prefix = get_prefix_custom(message.guild)
    if message.content.startswith(prefix):
        message.content = message.content[len(prefix):]
        await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    if before.content != after.content:
        data['editsnipe'][before.channel.id] = {
            'before': before.content,
            'after': after.content,
            'author': before.author.name,
            'author_id': before.author.id,
            'timestamp': datetime.now().isoformat()
        }
        save_data()

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    data['reactionsnipe'][reaction.message.channel.id] = {
        'emoji': str(reaction.emoji),
        'user': user.name,
        'user_id': user.id,
        'message': reaction.message.content,
        'timestamp': datetime.now().isoformat()
    }
    save_data()

@bot.event
async def on_bulk_message_delete(messages):
    channel = messages[0].channel
    deleted = [msg.content for msg in messages if msg.content]
    data['purgesnipe'][channel.id] = {
        'count': len(deleted),
        'messages': deleted[:10],
        'timestamp': datetime.now().isoformat()
    }
    save_data()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(description="You don't have permission to use this command.", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f"Missing argument: `{error.param.name}`", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(description=f"Invalid argument: {error}", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=5)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(description=f"Cooldown! Try again in {error.retry_after:.1f}s", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=5)
    else:
        print(f"Error: {error}")

# ===== SLASH COMMANDS =====
@bot.tree.command(name="ping", description="Check bot latency")
async def slash_ping(interaction: discord.Interaction):
    embed = discord.Embed(description=f"Pong! `{round(bot.latency * 1000)}ms`", color=0xdc143c)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="react", description="[OWNER] Add auto-reactions to a user")
async def react_add(interaction: discord.Interaction, user: discord.Member, emoji1: str, emoji2: Optional[str] = None, emoji3: Optional[str] = None, emoji4: Optional[str] = None):
    if not is_admin(interaction.user.id):
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

# ===== RUN =====
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No token found!")
        exit(1)
    
    print(f"🚀 Starting {BOT_NAME}...")
    bot.run(TOKEN)
