import discord
from discord.ext import commands

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="snipe")
    async def snipe(self, ctx, index: int = 1):
        """Show last deleted message"""
        channel_id = ctx.channel.id
        
        # Check if there are snipes
        if channel_id not in self.bot.data['snipe']:
            embed = discord.Embed(description="No messages to snipe.", color=0xdc143c)
            return await ctx.send(embed=embed)
        
        snipes = self.bot.data['snipe'][channel_id]
        
        # If snipes is a list (multiple)
        if isinstance(snipes, list):
            if index < 1 or index > len(snipes):
                embed = discord.Embed(description=f"Only {len(snipes)} messages available.", color=0xdc143c)
                return await ctx.send(embed=embed)
            snipe = snipes[index - 1]
        else:
            # Single snipe (old format)
            snipe = snipes
        
        embed = discord.Embed(
            description=snipe['content'][:2000] if snipe['content'] else "[No text content]",
            color=0xdc143c
        )
        embed.set_author(name=snipe['author'])
        embed.set_footer(text=f"Deleted at {snipe['timestamp']}")
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Snipe(bot))
