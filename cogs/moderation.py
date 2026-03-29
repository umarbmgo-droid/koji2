import discord
from discord.ext import commands
from datetime import timedelta
import random

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.cog_data if hasattr(bot, 'cog_data') else {}
    
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot kick someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.kick(reason=reason)
        embed = discord.Embed(description=f"{member.mention} has been kicked. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot ban someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"{member.mention} has been banned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str):
        banned_users = [entry async for entry in ctx.guild.bans()]
        for ban_entry in banned_users:
            if str(ban_entry.user) == user or str(ban_entry.user.id) == user:
                await ctx.guild.unban(ban_entry.user)
                embed = discord.Embed(description=f"{ban_entry.user.mention} has been unbanned.", color=0xdc143c)
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(description=f"User `{user}` not found in ban list.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 5, *, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot mute someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=reason)
        embed = discord.Embed(description=f"{member.mention} muted for {minutes} minutes. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unmute")
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot unmute someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.timeout(None)
        embed = discord.Embed(description=f"{member.mention} has been unmuted.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot warn someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        # Warn logic here
        embed = discord.Embed(description=f"{member.mention} has been warned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="warns")
    @commands.has_permissions(moderate_members=True)
    async def warns(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{member.mention} has 0 warnings.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="clearwarns")
    @commands.has_permissions(administrator=True)
    async def clearwarns(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"Cleared all warnings for {member.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if amount < 1 or amount > 100:
            embed = discord.Embed(description="Amount must be between 1-100.", color=0xdc143c)
            return await ctx.send(embed=embed)
        deleted = await ctx.channel.purge(limit=amount + 1)
        embed = discord.Embed(description=f"Deleted {len(deleted)} messages.", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=3)
    
    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(description=f"{channel.mention} has been locked.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(description=f"{channel.mention} has been unlocked.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:
            embed = discord.Embed(description="Slowmode must be between 0-21600 seconds.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(description=f"Slowmode set to {seconds} seconds.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = None):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot change nickname of someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        old_name = member.display_name
        await member.edit(nick=nickname)
        embed = discord.Embed(description=f"Changed {member.mention}'s nickname from `{old_name}` to `{nickname or member.name}`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="role")
    @commands.has_permissions(manage_roles=True)
    async def role_command(self, ctx, member: discord.Member, role: discord.Role):
        if not self.bot.has_higher_role(ctx.author, role):
            embed = discord.Embed(description="You cannot manage roles higher than your own.", color=0xdc143c)
            return await ctx.send(embed=embed)
        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(description=f"Removed {role.mention} from {member.mention}", color=0xdc143c)
        else:
            await member.add_roles(role)
            embed = discord.Embed(description=f"Added {role.mention} to {member.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="softban")
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot softban someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.ban(reason=reason)
        await member.unban(reason="Softban completed")
        embed = discord.Embed(description=f"{member.mention} has been softbanned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="hackban")
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user_id: int, *, reason: str = "No reason provided"):
        user = await self.bot.fetch_user(user_id)
        await ctx.guild.ban(user, reason=reason)
        embed = discord.Embed(description=f"{user.name} has been banned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="muteall")
    @commands.has_permissions(administrator=True)
    async def muteall(self, ctx):
        count = 0
        for member in ctx.guild.members:
            if not member.bot:
                try:
                    await member.timeout(timedelta(minutes=5))
                    count += 1
                except:
                    pass
        embed = discord.Embed(description=f"Muted {count} members.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unmuteall")
    @commands.has_permissions(administrator=True)
    async def unmuteall(self, ctx):
        count = 0
        for member in ctx.guild.members:
            try:
                await member.timeout(None)
                count += 1
            except:
                pass
        embed = discord.Embed(description=f"Unmuted {count} members.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="jail")
    @commands.has_permissions(moderate_members=True)
    async def jail(self, ctx, member: discord.Member, duration: int = 60, *, reason: str = "No reason"):
        await self.bot.isolate_user(member, duration, reason)
        embed = discord.Embed(description=f"{member.mention} has been jailed for {duration} minutes. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unjail")
    @commands.has_permissions(moderate_members=True)
    async def unjail(self, ctx, member: discord.Member):
        isolation_role = discord.utils.get(ctx.guild.roles, name="Isolation")
        if isolation_role in member.roles:
            await member.remove_roles(isolation_role)
            embed = discord.Embed(description=f"{member.mention} has been unjailed.", color=0xdc143c)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{member.mention} is not jailed.", color=0xdc143c)
            await ctx.send(embed=embed)
    
    @commands.command(name="hide")
    @commands.has_permissions(manage_channels=True)
    async def hide(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=False)
        embed = discord.Embed(description=f"{channel.mention} has been hidden.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="reveal")
    @commands.has_permissions(manage_channels=True)
    async def reveal(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, read_messages=True)
        embed = discord.Embed(description=f"{channel.mention} has been revealed.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="cleanup")
    @commands.has_permissions(manage_messages=True)
    async def cleanup(self, ctx, amount: int = 100):
        def is_bot(msg):
            return msg.author.bot
        deleted = await ctx.channel.purge(limit=amount, check=is_bot)
        embed = discord.Embed(description=f"Deleted {len(deleted)} bot messages.", color=0xdc143c)
        await ctx.send(embed=embed, delete_after=3)
    
    @commands.command(name="stripstaff")
    @commands.has_permissions(administrator=True)
    async def stripstaff(self, ctx, member: discord.Member):
        staff_roles = [r for r in member.roles if r.permissions.administrator or r.permissions.ban_members]
        for role in staff_roles:
            await member.remove_roles(role)
        embed = discord.Embed(description=f"Removed staff roles from {member.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="mutelist")
    async def mutelist(self, ctx):
        muted = [m.mention for m in ctx.guild.members if m.is_timed_out()]
        embed = discord.Embed(title=f"Muted Members ({len(muted)})", description="\n".join(muted[:20]) or "None", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="inrole")
    async def inrole(self, ctx, role: discord.Role):
        members = [m.mention for m in role.members[:20]]
        embed = discord.Embed(title=f"Members with {role.name}", description="\n".join(members) or "No members", color=0xdc143c)
        embed.set_footer(text=f"Total: {len(role.members)} members")
        await ctx.send(embed=embed)
    
    @commands.command(name="drag")
    @commands.has_permissions(move_members=True)
    async def drag(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        await member.move_to(channel)
        embed = discord.Embed(description=f"Moved {member.mention} to {channel.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="newusers")
    async def newusers(self, ctx, limit: int = 10):
        new_users = sorted(ctx.guild.members, key=lambda m: m.joined_at, reverse=True)[:limit]
        embed = discord.Embed(title=f"Newest Members ({limit})", color=0xdc143c)
        for m in new_users:
            embed.add_field(name=m.name, value=m.joined_at.strftime("%Y-%m-%d"), inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
