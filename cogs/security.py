import discord
from discord.ext import commands

class Security(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="isolate")
    @commands.has_permissions(administrator=True)
    async def isolate(self, ctx, member: discord.Member, duration: int = 0, *, reason: str = "No reason provided"):
        if self.bot.is_whitelisted(member.id):
            embed = discord.Embed(description=f"Cannot isolate whitelisted user.", color=0xdc143c)
            return await ctx.send(embed=embed)
        await self.bot.isolate_user(member, duration, reason)
        embed = discord.Embed(description=f"{member.mention} has been isolated. Reason: {reason}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unisolate")
    @commands.has_permissions(administrator=True)
    async def unisolate(self, ctx, member: discord.Member):
        isolation_role = discord.utils.get(ctx.guild.roles, name="Isolation")
        if isolation_role in member.roles:
            await member.remove_roles(isolation_role)
            embed = discord.Embed(description=f"{member.mention} has been unisolated.", color=0xdc143c)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f"{member.mention} is not isolated.", color=0xdc143c)
            await ctx.send(embed=embed)
    
    @commands.command(name="logs")
    @commands.has_permissions(administrator=True)
    async def set_logs(self, ctx, channel: discord.TextChannel):
        self.bot.data['logs_channel'][str(ctx.guild.id)] = channel.id
        self.bot.save_data()
        embed = discord.Embed(description=f"Logs channel set to {channel.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="whitelist")
    async def whitelist(self, ctx, user: discord.Member):
        if ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="Only the owner can use this command.", color=0xdc143c)
            return await ctx.send(embed=embed)
        if user.id not in self.bot.data['whitelist']:
            self.bot.data['whitelist'].append(user.id)
            self.bot.save_data()
            embed = discord.Embed(description=f"{user.mention} has been whitelisted.", color=0xdc143c)
        else:
            embed = discord.Embed(description=f"{user.mention} is already whitelisted.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="blacklist")
    async def blacklist(self, ctx, user: discord.Member):
        if ctx.author.id != self.bot.owner_id:
            embed = discord.Embed(description="Only the owner can use this command.", color=0xdc143c)
            return await ctx.send(embed=embed)
        if user.id in self.bot.data['whitelist']:
            self.bot.data['whitelist'].remove(user.id)
            self.bot.save_data()
            embed = discord.Embed(description=f"{user.mention} has been blacklisted.", color=0xdc143c)
        else:
            embed = discord.Embed(description=f"{user.mention} is not whitelisted.", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Security(bot))
