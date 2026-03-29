import discord
from discord.ext import commands
import time
import asyncio
from datetime import datetime

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="afk")
    async def afk(self, ctx, *, reason: str = "AFK"):
        """Set yourself as AFK"""
        self.bot.data['afk'][str(ctx.author.id)] = reason
        self.bot.save_data()
        embed = discord.Embed(description=f"{ctx.author.mention} is now AFK: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check bot latency"""
        embed = discord.Embed(description=f"Pong! `{round(self.bot.latency * 1000)}ms`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="uptime")
    async def uptime(self, ctx):
        """Show bot uptime"""
        embed = discord.Embed(description=f"Uptime: `{self.bot.get_uptime()}`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="poll")
    async def poll(self, ctx, *, question: str):
        """Create a poll"""
        embed = discord.Embed(title="📊 Poll", description=question, color=0xdc143c)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
    
    @commands.command(name="invite")
    async def invite(self, ctx):
        """Get bot invite link"""
        embed = discord.Embed(description=f"[Invite {self.bot.user.name}](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands)", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
