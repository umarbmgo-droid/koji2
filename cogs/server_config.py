import discord
from discord.ext import commands

class ServerConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, new_prefix: str = None):
        if not new_prefix:
            prefix = self.bot.get_prefix_custom(ctx.guild)
            embed = discord.Embed(description=f"Current prefix: `{prefix}`", color=0xdc143c)
            return await ctx.send(embed=embed)
        self.bot.data['custom_prefix'][str(ctx.guild.id)] = new_prefix
        self.bot.save_data()
        embed = discord.Embed(description=f"Prefix changed to `{new_prefix}`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="autorole")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx, role: discord.Role):
        guild_id = str(ctx.guild.id)
        if guild_id not in self.bot.data['auto_roles']:
            self.bot.data['auto_roles'][guild_id] = []
        if role.id not in self.bot.data['auto_roles'][guild_id]:
            self.bot.data['auto_roles'][guild_id].append(role.id)
            self.bot.save_data()
            embed = discord.Embed(description=f"Auto-role set to {role.mention}", color=0xdc143c)
        else:
            self.bot.data['auto_roles'][guild_id].remove(role.id)
            self.bot.save_data()
            embed = discord.Embed(description=f"Auto-role removed: {role.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="welcome")
    @commands.has_permissions(administrator=True)
    async def welcome(self, ctx, channel: discord.TextChannel = None):
        if channel:
            self.bot.data['welcome_channel'][str(ctx.guild.id)] = channel.id
            embed = discord.Embed(description=f"Welcome channel set to {channel.mention}", color=0xdc143c)
        else:
            if str(ctx.guild.id) in self.bot.data['welcome_channel']:
                del self.bot.data['welcome_channel'][str(ctx.guild.id)]
                embed = discord.Embed(description="Welcome channel disabled", color=0xdc143c)
            else:
                embed = discord.Embed(description="Welcome channel not set", color=0xdc143c)
        self.bot.save_data()
        await ctx.send(embed=embed)
    
    @commands.command(name="goodbye")
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx, channel: discord.TextChannel = None):
        if channel:
            self.bot.data['goodbye_channel'][str(ctx.guild.id)] = channel.id
            embed = discord.Embed(description=f"Goodbye channel set to {channel.mention}", color=0xdc143c)
        else:
            if str(ctx.guild.id) in self.bot.data['goodbye_channel']:
                del self.bot.data['goodbye_channel'][str(ctx.guild.id)]
                embed = discord.Embed(description="Goodbye channel disabled", color=0xdc143c)
            else:
                embed = discord.Embed(description="Goodbye channel not set", color=0xdc143c)
        self.bot.save_data()
        await ctx.send(embed=embed)
    
    @commands.command(name="pin")
    @commands.has_permissions(manage_messages=True)
    async def pin(self, ctx, message_id: int):
        try:
            msg = await ctx.channel.fetch_message(message_id)
            await msg.pin()
            embed = discord.Embed(description=f"Pinned message from {msg.author.name}", color=0xdc143c)
        except:
            embed = discord.Embed(description="Message not found.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="unpin")
    @commands.has_permissions(manage_messages=True)
    async def unpin(self, ctx, message_id: int):
        try:
            pins = await ctx.channel.pins()
            for pin in pins:
                if pin.id == message_id:
                    await pin.unpin()
                    embed = discord.Embed(description="Unpinned message", color=0xdc143c)
                    break
            else:
                embed = discord.Embed(description="Message not pinned.", color=0xdc143c)
        except:
            embed = discord.Embed(description="Error unpinning.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="thread")
    @commands.has_permissions(manage_threads=True)
    async def thread(self, ctx, name: str):
        thread = await ctx.channel.create_thread(name=name, type=discord.ChannelType.public_thread)
        embed = discord.Embed(description=f"Thread created: {thread.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="enablecommand")
    @commands.has_permissions(administrator=True)
    async def enablecommand(self, ctx, command_name: str):
        embed = discord.Embed(description=f"Command `{command_name}` enabled", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="disablecommand")
    @commands.has_permissions(administrator=True)
    async def disablecommand(self, ctx, command_name: str):
        embed = discord.Embed(description=f"Command `{command_name}` disabled", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="ignore")
    @commands.has_permissions(administrator=True)
    async def ignore(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        embed = discord.Embed(description=f"Ignoring commands in {channel.mention}", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerConfig(bot))
