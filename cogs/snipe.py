import discord
from discord.ext import commands

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="snipe")
    async def snipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id not in self.bot.data['snipe']:
            embed = discord.Embed(description="No messages to snipe.", color=0xdc143c)
            return await ctx.send(embed=embed)
        snipe_data = self.bot.data['snipe'][channel_id]
        embed = discord.Embed(description=f"**{snipe_data['author']}:** {snipe_data['content']}", color=0xdc143c)
        embed.set_footer(text=f"Sent at {snipe_data['timestamp']}")
        await ctx.send(embed=embed)
    
    @commands.command(name="editsnipe")
    async def editsnipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id not in self.bot.data['editsnipe']:
            embed = discord.Embed(description="No edited messages to snipe.", color=0xdc143c)
            return await ctx.send(embed=embed)
        snipe_data = self.bot.data['editsnipe'][channel_id]
        embed = discord.Embed(description=f"**{snipe_data['author']}** edited:\n**Before:** {snipe_data['before']}\n**After:** {snipe_data['after']}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="reactionsnipe")
    async def reactionsnipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id not in self.bot.data['reactionsnipe']:
            embed = discord.Embed(description="No reactions to snipe.", color=0xdc143c)
            return await ctx.send(embed=embed)
        snipe_data = self.bot.data['reactionsnipe'][channel_id]
        embed = discord.Embed(description=f"**{snipe_data['user']}** reacted with {snipe_data['emoji']} to: {snipe_data['message']}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="purgesnipe")
    async def purgesnipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id not in self.bot.data['purgesnipe']:
            embed = discord.Embed(description="No purges to snipe.", color=0xdc143c)
            return await ctx.send(embed=embed)
        snipe_data = self.bot.data['purgesnipe'][channel_id]
        messages = "\n".join(snipe_data['messages'])
        embed = discord.Embed(description=f"**{snipe_data['count']} messages purged:**\n{messages}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="clearsnipe")
    async def clearsnipe(self, ctx):
        channel_id = ctx.channel.id
        if channel_id in self.bot.data['snipe']:
            del self.bot.data['snipe'][channel_id]
            self.bot.save_data()
        embed = discord.Embed(description="Snipe data cleared.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="cleareditsnipe")
    async def cleareditsnipe(self, ctx):
        if ctx.channel.id in self.bot.data['editsnipe']:
            del self.bot.data['editsnipe'][ctx.channel.id]
            self.bot.save_data()
        embed = discord.Embed(description="Edit snipe cleared.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="clearreactionsnipes")
    async def clearreactionsnipes(self, ctx):
        if ctx.channel.id in self.bot.data['reactionsnipe']:
            del self.bot.data['reactionsnipe'][ctx.channel.id]
            self.bot.save_data()
        embed = discord.Embed(description="Reaction snipe cleared.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="clearpurgesnipe")
    async def clearpurgesnipe(self, ctx):
        if ctx.channel.id in self.bot.data['purgesnipe']:
            del self.bot.data['purgesnipe'][ctx.channel.id]
            self.bot.save_data()
        embed = discord.Embed(description="Purge snipe cleared.", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Snipe(bot))
