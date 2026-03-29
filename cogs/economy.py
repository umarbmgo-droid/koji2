import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = bot.cog_data if hasattr(bot, 'cog_data') else {}
    
    @commands.command(name="balance", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        user_id = str(member.id)
        if user_id not in self.bot.data['economy']:
            self.bot.data['economy'][user_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
            self.bot.save_data()
        embed = discord.Embed(description=f"{member.mention}'s balance: `{self.bot.data['economy'][user_id]['balance']} coins`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="daily")
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.bot.data['economy']:
            self.bot.data['economy'][user_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        last_daily = self.bot.data['economy'][user_id].get('last_daily')
        if last_daily:
            last_time = datetime.fromisoformat(last_daily)
            if datetime.now() - last_time < timedelta(days=1):
                next_time = last_time + timedelta(days=1)
                remaining = next_time - datetime.now()
                hours = remaining.seconds // 3600
                minutes = (remaining.seconds % 3600) // 60
                embed = discord.Embed(description=f"You already claimed your daily! Next in {hours}h {minutes}m", color=0xdc143c)
                return await ctx.send(embed=embed)
        reward = random.randint(100, 500)
        self.bot.data['economy'][user_id]['balance'] += reward
        self.bot.data['economy'][user_id]['last_daily'] = datetime.now().isoformat()
        self.bot.save_data()
        embed = discord.Embed(description=f"You received `{reward}` coins!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="give")
    async def give(self, ctx, member: discord.Member, amount: int):
        if amount <= 0:
            embed = discord.Embed(description="Amount must be positive.", color=0xdc143c)
            return await ctx.send(embed=embed)
        sender_id = str(ctx.author.id)
        receiver_id = str(member.id)
        if sender_id not in self.bot.data['economy']:
            self.bot.data['economy'][sender_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        if self.bot.data['economy'][sender_id]['balance'] < amount:
            embed = discord.Embed(description="You don't have enough coins!", color=0xdc143c)
            return await ctx.send(embed=embed)
        if receiver_id not in self.bot.data['economy']:
            self.bot.data['economy'][receiver_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        self.bot.data['economy'][sender_id]['balance'] -= amount
        self.bot.data['economy'][receiver_id]['balance'] += amount
        self.bot.save_data()
        embed = discord.Embed(description=f"You gave `{amount}` coins to {member.mention}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="rob")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member):
        if member == ctx.author:
            embed = discord.Embed(description="You can't rob yourself!", color=0xdc143c)
            return await ctx.send(embed=embed)
        user_id = str(ctx.author.id)
        target_id = str(member.id)
        if user_id not in self.bot.data['economy']:
            self.bot.data['economy'][user_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        if target_id not in self.bot.data['economy']:
            self.bot.data['economy'][target_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        if random.random() < 0.5:
            stolen = min(random.randint(50, 200), self.bot.data['economy'][target_id]['balance'])
            self.bot.data['economy'][user_id]['balance'] += stolen
            self.bot.data['economy'][target_id]['balance'] -= stolen
            self.bot.save_data()
            embed = discord.Embed(description=f"You robbed {member.mention} and got `{stolen}` coins!", color=0xdc143c)
        else:
            embed = discord.Embed(description=f"You failed to rob {member.mention}!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx):
        sorted_users = sorted(self.bot.data['economy'].items(), key=lambda x: x[1]['balance'], reverse=True)[:10]
        embed = discord.Embed(title="💰 Economy Leaderboard", color=0xdc143c)
        for i, (user_id, stats) in enumerate(sorted_users, 1):
            user = self.bot.get_user(int(user_id))
            name = user.name if user else f"Unknown ({user_id})"
            embed.add_field(name=f"{i}. {name}", value=f"{stats['balance']} coins", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="work")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        jobs = ["programmer", "teacher", "chef", "artist", "musician", "writer", "designer", "engineer"]
        earnings = random.randint(50, 200)
        user_id = str(ctx.author.id)
        if user_id not in self.bot.data['economy']:
            self.bot.data['economy'][user_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
        self.bot.data['economy'][user_id]['balance'] += earnings
        self.bot.save_data()
        embed = discord.Embed(description=f"You worked as a {random.choice(jobs)} and earned `{earnings}` coins!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="beg")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        if random.random() < 0.6:
            amount = random.randint(5, 50)
            user_id = str(ctx.author.id)
            if user_id not in self.bot.data['economy']:
                self.bot.data['economy'][user_id] = {'balance': 1000, 'bank': 0, 'last_daily': None}
            self.bot.data['economy'][user_id]['balance'] += amount
            self.bot.save_data()
            embed = discord.Embed(description=f"Someone gave you `{amount}` coins!", color=0xdc143c)
        else:
            embed = discord.Embed(description="You begged but got nothing...", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="shop")
    async def shop(self, ctx):
        embed = discord.Embed(title="🛒 Shop", color=0xdc143c)
        embed.add_field(name="🎁 Mystery Box", value="100 coins", inline=False)
        embed.add_field(name="💎 Diamond", value="5000 coins", inline=False)
        embed.add_field(name="📈 Stock", value="Coming soon!", inline=False)
        await ctx.send(embed=embed)
    
    @commands.command(name="buy")
    async def buy(self, ctx, item: str):
        embed = discord.Embed(description=f"Item '{item}' is not available.", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="inventory", aliases=["inv"])
    async def inventory(self, ctx):
        embed = discord.Embed(description="Your inventory is empty.", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
