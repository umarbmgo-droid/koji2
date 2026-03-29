import discord
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="play")
    async def play(self, ctx, *, query: str):
        embed = discord.Embed(description=f"🎵 Playing: `{query}`\n*(Full music system requires lavalink setup)*", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="playing")
    async def playing(self, ctx):
        embed = discord.Embed(description="Nothing playing.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="pause")
    async def pause(self, ctx):
        embed = discord.Embed(description="Paused.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="resume")
    async def resume(self, ctx):
        embed = discord.Embed(description="Resumed.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="queue")
    async def queue(self, ctx):
        embed = discord.Embed(title="Queue", description="Empty.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="skip")
    async def skip(self, ctx):
        embed = discord.Embed(description="Skipped.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="stop")
    async def stop(self, ctx):
        embed = discord.Embed(description="Stopped playback.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="volume")
    async def volume(self, ctx, level: int = None):
        if level:
            embed = discord.Embed(description=f"Volume set to {level}%", color=0xdc143c)
        else:
            embed = discord.Embed(description="Volume: 50%", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="loop")
    async def loop(self, ctx):
        embed = discord.Embed(description="Looping disabled.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="restart")
    async def restart(self, ctx):
        embed = discord.Embed(description="Restarted.", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
