import discord
from discord.ext import commands
import random
import asyncio
import time

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(description=f"Pong! `{round(self.bot.latency * 1000)}ms`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="uptime")
    async def uptime(self, ctx):
        embed = discord.Embed(description=f"Uptime: `{self.bot.get_uptime()}`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="invite")
    async def invite(self, ctx):
        embed = discord.Embed(description=f"[Invite {self.bot.user.name}](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot%20applications.commands)", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="afk")
    async def afk(self, ctx, *, reason: str = "AFK"):
        self.bot.data['afk'][str(ctx.author.id)] = {'reason': reason, 'duration': self.bot.get_uptime()}
        self.bot.save_data()
        embed = discord.Embed(description=f"✅ {ctx.author.mention} is now AFK: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="poll")
    async def poll(self, ctx, *, question: str):
        embed = discord.Embed(title="📊 Poll", description=question, color=0xdc143c)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
    
    @commands.command(name="calculate", aliases=["calc"])
    async def calculate(self, ctx, *, expression: str):
        try:
            result = eval(expression.replace("^", "**"))
            embed = discord.Embed(description=f"**{expression}** = `{result}`", color=0xdc143c)
        except:
            embed = discord.Embed(description="Invalid expression", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="translate")
    async def translate(self, ctx, lang: str, *, text: str):
        embed = discord.Embed(description=f"Translation to `{lang}`: {text}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="define")
    async def define(self, ctx, *, word: str):
        embed = discord.Embed(title=f"Definition of {word}", description="Word not found.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="choices")
    async def choices(self, ctx, *options):
        embed = discord.Embed(description=f"I choose: {random.choice(options)}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="mock")
    async def mock(self, ctx, *, text: str):
        mocked = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(text))
        embed = discord.Embed(description=mocked, color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="colour", aliases=["color"])
    async def colour(self, ctx, hex_code: str = None):
        if hex_code:
            embed = discord.Embed(color=int(hex_code.lstrip("#"), 16))
            embed.description = f"Color: {hex_code}"
        else:
            embed = discord.Embed(description="Provide a hex code: `.color #ff0000`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="hex")
    async def hex(self, ctx, color: discord.Color):
        embed = discord.Embed(description=f"Hex: {str(color)}", color=color)
        await ctx.send(embed=embed)
    
    @commands.command(name="randomhex")
    async def randomhex(self, ctx):
        random_color = random.randint(0, 0xFFFFFF)
        embed = discord.Embed(description=f"Random hex: `#{random_color:06x}`", color=random_color)
        await ctx.send(embed=embed)
    
    @commands.command(name="tts")
    async def tts(self, ctx, *, text: str):
        embed = discord.Embed(description=f"TTS: {text[:200]}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="search")
    async def search(self, ctx, *, query: str):
        embed = discord.Embed(description=f"Searching for: {query}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="emoji")
    async def emoji(self, ctx, emoji: str):
        embed = discord.Embed(description=f"Emoji: {emoji}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="sticker")
    async def sticker(self, ctx, sticker: discord.Sticker):
        embed = discord.Embed(title=sticker.name, color=0xdc143c)
        embed.set_image(url=sticker.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
