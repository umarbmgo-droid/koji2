import discord
from discord.ext import commands
import time

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="userinfo", aliases=["ui"])
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Info", color=member.color if member.color else 0xdc143c)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Joined", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Created", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
        roles = [role.mention for role in member.roles[1:]][:5]
        embed.add_field(name=f"Roles ({len(member.roles)-1})", value=" ".join(roles) if roles else "None", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="avatar", aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar", color=0xdc143c)
        embed.set_image(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name="serverinfo", aliases=["si"])
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=guild.name, color=0xdc143c)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        embed.add_field(name="Created", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name="roleinfo")
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(title=role.name, color=role.color)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Members", value=len(role.members), inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Hoist", value=role.hoist, inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name="channelinfo")
    async def channelinfo(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(title=channel.name, color=0xdc143c)
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Category", value=channel.category.name if channel.category else "None", inline=True)
        embed.add_field(name="Created", value=channel.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Topic", value=channel.topic or "None", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="bots")
    async def bots(self, ctx):
        bots = [m.mention for m in ctx.guild.members if m.bot][:20]
        embed = discord.Embed(title=f"Bots ({len(bots)})", description=" ".join(bots), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="boosters")
    async def boosters(self, ctx):
        boosters = [m.mention for m in ctx.guild.premium_subscribers]
        embed = discord.Embed(title=f"Boosters ({len(boosters)})", description=" ".join(boosters), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="botinfo")
    async def botinfo(self, ctx):
        embed = discord.Embed(title=f"{self.bot.user.name} Info", color=0xdc143c)
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Commands", value=len(self.bot.commands), inline=True)
        embed.add_field(name="Uptime", value=self.bot.get_uptime(), inline=True)
        embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Support", value=self.bot.support_server, inline=True)
        await ctx.send(embed=embed)
    
    @commands.command(name="servericon")
    async def servericon(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}'s Icon", color=0xdc143c)
        embed.set_image(url=ctx.guild.icon.url if ctx.guild.icon else "")
        await ctx.send(embed=embed)
    
    @commands.command(name="guildbanner")
    async def guildbanner(self, ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}'s Banner", color=0xdc143c)
        embed.set_image(url=ctx.guild.banner.url if ctx.guild.banner else "")
        await ctx.send(embed=embed)
    
    @commands.command(name="rolelist")
    async def rolelist(self, ctx):
        roles = [r.mention for r in ctx.guild.roles][:20]
        embed = discord.Embed(title="Roles", description=" ".join(roles), color=0xdc143c)
        embed.set_footer(text=f"Total: {len(ctx.guild.roles)} roles")
        await ctx.send(embed=embed)
    
    @commands.command(name="membercount")
    async def membercount(self, ctx):
        embed = discord.Embed(description=f"Total Members: {ctx.guild.member_count}\nHumans: {len([m for m in ctx.guild.members if not m.bot])}\nBots: {len([m for m in ctx.guild.members if m.bot])}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="firstmessage")
    async def firstmessage(self, ctx):
        first = await ctx.channel.history(limit=1, oldest_first=True).__anext__()
        embed = discord.Embed(title="First Message", description=first.content or "[Embed]", color=0xdc143c)
        embed.set_footer(text=f"By {first.author.name} on {first.created_at.strftime('%Y-%m-%d')}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Information(bot))
