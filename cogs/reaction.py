import discord
from discord.ext import commands

class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="autoreact")
    @commands.has_permissions(administrator=True)
    async def autoreact(self, ctx, user: discord.Member, *emojis):
        if len(emojis) > 4:
            emojis = emojis[:4]
        self.bot.data['auto_react'][str(user.id)] = list(emojis)
        self.bot.save_data()
        embed = discord.Embed(description=f"Auto-reacting to {user.mention} with {' '.join(emojis)}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="reactionrole")
    @commands.has_permissions(administrator=True)
    async def reactionrole(self, ctx, message_id: int, emoji: str, role: discord.Role):
        embed = discord.Embed(description=f"Reaction role set: React with {emoji} to get {role.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="reactionlist")
    async def reactionlist(self, ctx):
        embed = discord.Embed(title="Reaction Roles", description="No reaction roles set.", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Reaction(bot))
