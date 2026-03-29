import discord
import time
from datetime import datetime, timedelta

class Helpers:
    def __init__(self, bot):
        self.bot = bot
    
    def get_uptime(self):
        uptime = int(time.time() - self.bot.start_time)
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
    
    def has_higher_role(self, member, target_role):
        if member.guild_permissions.administrator:
            return True
        if member.id == self.bot.owner_id:
            return True
        return member.top_role > target_role
    
    async def log_action(self, guild, action, user, moderator, reason=None, extra=None):
        channel_id = self.bot.data['logs_channel'].get(str(guild.id))
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
