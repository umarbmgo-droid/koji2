import discord
from discord.ext import commands
from datetime import timedelta
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot kick someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.kick(reason=reason)
        embed = discord.Embed(description=f"{member.mention} kicked. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot ban someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await member.ban(reason=reason)
        embed = discord.Embed(description=f"{member.mention} banned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str):
        banned_users = [entry async for entry in ctx.guild.bans()]
        for ban_entry in banned_users:
            if str(ban_entry.user) == user or str(ban_entry.user.id) == user:
                await ctx.guild.unban(ban_entry.user)
                embed = discord.Embed(description=f"{ban_entry.user.mention} unbanned.", color=0xdc143c)
                await ctx.send(embed=embed)
                return
        embed = discord.Embed(description=f"User `{user}` not found.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="mute")
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int = 5, *, reason: str = "No reason"):
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
        embed = discord.Embed(description=f"{member.mention} unmuted.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="warn")
    @commands.has_permissions(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot warn someone with higher or equal role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.data['warns']:
            self.bot.data['warns'][guild_id] = {}
        if str(member.id) not in self.bot.data['warns'][guild_id]:
            self.bot.data['warns'][guild_id][str(member.id)] = []
        
        self.bot.data['warns'][guild_id][str(member.id)].append({
            'reason': reason,
            'moderator': ctx.author.id,
            'date': discord.utils.utcnow().isoformat()
        })
        self.bot.save_data()
        
        embed = discord.Embed(description=f"{member.mention} warned. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="warns")
    @commands.has_permissions(moderate_members=True)
    async def warns(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.data['warns'] or str(member.id) not in self.bot.data['warns'][guild_id]:
            embed = discord.Embed(description=f"{member.mention} has no warnings.", color=0xdc143c)
            return await ctx.send(embed=embed)
        
        warns = self.bot.data['warns'][guild_id][str(member.id)]
        embed = discord.Embed(title=f"Warnings for {member.name}", color=0xdc143c)
        for i, warn in enumerate(warns[-5:], 1):
            embed.add_field(name=f"Warning {i}", value=f"**Reason:** {warn['reason']}\n**Mod:** <@{warn['moderator']}>", inline=False)
        embed.set_footer(text=f"Total: {len(warns)} warnings")
        await ctx.send(embed=embed)
    
    @commands.command(name="clearwarns")
    @commands.has_permissions(administrator=True)
    async def clearwarns(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        if guild_id in self.bot.data['warns'] and str(member.id) in self.bot.data['warns'][guild_id]:
            del self.bot.data['warns'][guild_id][str(member.id)]
            self.bot.save_data()
            embed = discord.Embed(description=f"Cleared all warnings for {member.mention}", color=0xdc143c)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{member.mention} has no warnings.", color=0xdc143c)
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
        embed = discord.Embed(description=f"{channel.mention} locked.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        embed = discord.Embed(description=f"{channel.mention} unlocked.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        if seconds < 0 or seconds > 21600:
            embed = discord.Embed(description="Slowmode must be 0-21600 seconds.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(description=f"Slowmode set to {seconds} seconds.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="role")
    @commands.has_permissions(manage_roles=True)
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        if role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot manage roles higher than your own.", color=0xdc143c)
            return await ctx.send(embed=embed)
        
        if role in member.roles:
            await member.remove_roles(role)
            embed = discord.Embed(description=f"Removed {role.mention} from {member.mention}", color=0xdc143c)
        else:
            await member.add_roles(role)
            embed = discord.Embed(description=f"Added {role.mention} to {member.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="nickname")
    @commands.has_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname: str = None):
        if member.top_role >= ctx.author.top_role and ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="You cannot change nickname of someone with higher role.", color=0xdc143c)
            return await ctx.send(embed=embed)
        old_name = member.display_name
        await member.edit(nick=nickname)
        embed = discord.Embed(description=f"Changed {member.mention}'s nickname from `{old_name}` to `{nickname or member.name}`", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
