import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="8ball")
    async def eightball(self, ctx, *, question: str):
        responses = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Very doubtful."]
        embed = discord.Embed(description=f"🎱 **Question:** {question}\n**Answer:** {random.choice(responses)}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="ship")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member = None):
        if not user2:
            user2 = ctx.author
        compatibility = random.randint(0, 100)
        bar = "❤️" * (compatibility // 10) + "🖤" * (10 - (compatibility // 10))
        embed = discord.Embed(description=f"**{user1.name}** ❤️ **{user2.name}**\nCompatibility: `{compatibility}%`\n{bar}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="hug")
    async def hug(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention} hugs {member.mention} 🤗", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="kiss")
    async def kiss(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention} kisses {member.mention} 💋", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="slap")
    async def slap(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention} slaps {member.mention} 🖐️", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="kill")
    async def kill(self, ctx, member: discord.Member):
        kills = [f"{ctx.author.mention} stabs {member.mention} with a knife!", f"{ctx.author.mention} throws {member.mention} off a cliff!", f"{ctx.author.mention} poisons {member.mention}'s drink!"]
        embed = discord.Embed(description=random.choice(kills), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="cat")
    async def cat(self, ctx):
        facts = ["Cats sleep for 70% of their lives.", "A group of cats is called a clowder.", "Cats have 32 muscles in each ear.", "A cat's purr can heal bones."]
        embed = discord.Embed(description=f"🐱 {random.choice(facts)}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="dog")
    async def dog(self, ctx):
        facts = ["Dogs' noses are wet to absorb scent chemicals.", "A dog's sense of smell is 40x better than humans.", "Dogs can understand up to 250 words.", "A Greyhound can beat a cheetah in a long race."]
        embed = discord.Embed(description=f"🐕 {random.choice(facts)}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="gayrate")
    async def gayrate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        rate = random.randint(0, 100)
        embed = discord.Embed(description=f"{member.mention} is `{rate}%` gay 🌈", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="insult")
    async def insult(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        insults = [f"{member.mention} has the personality of a burnt toast.", f"{member.mention} is proof that evolution can go backwards.", f"{member.mention}'s brain is like a browser - 20 tabs open and all frozen."]
        embed = discord.Embed(description=random.choice(insults), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="truthordare")
    async def truthordare(self, ctx, type: str):
        truth = ["What's your biggest fear?", "What's something you've never told anyone?", "What's the worst thing you've ever done?"]
        dare = ["Do 10 pushups", "Send a random message to someone", "Change your nickname to something embarrassing"]
        if type.lower() == "truth":
            embed = discord.Embed(description=f"🎲 **Truth:** {random.choice(truth)}", color=0xdc143c)
        elif type.lower() == "dare":
            embed = discord.Embed(description=f"🎲 **Dare:** {random.choice(dare)}", color=0xdc143c)
        else:
            embed = discord.Embed(description="Use `.truthordare truth` or `.truthordare dare`", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="tictactoe")
    async def tictactoe(self, ctx, opponent: discord.Member):
        embed = discord.Embed(description=f"{ctx.author.mention} challenged {opponent.mention} to Tic Tac Toe!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="rockpaperscissors", aliases=["rps"])
    async def rps(self, ctx, choice: str):
        choices = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices)
        if choice.lower() not in choices:
            embed = discord.Embed(description="Choose rock, paper, or scissors.", color=0xdc143c)
            return await ctx.send(embed=embed)
        result = "tie" if choice.lower() == bot_choice else ("win" if (choice.lower() == "rock" and bot_choice == "scissors") or (choice.lower() == "paper" and bot_choice == "rock") or (choice.lower() == "scissors" and bot_choice == "paper") else "lose")
        embed = discord.Embed(description=f"You chose {choice}, I chose {bot_choice}. You {result}!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="guess")
    async def guess(self, ctx):
        number = random.randint(1, 100)
        embed = discord.Embed(description="Guess a number between 1-100! You have 5 seconds.", color=0xdc143c)
        await ctx.send(embed=embed)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()
        try:
            msg = await self.bot.wait_for('message', timeout=5.0, check=check)
            guess_num = int(msg.content)
            result = "Correct!" if guess_num == number else f"Wrong! It was {number}"
            embed = discord.Embed(description=result, color=0xdc143c)
            await ctx.send(embed=embed)
        except asyncio.TimeoutError:
            embed = discord.Embed(description=f"Time's up! It was {number}", color=0xdc143c)
            await ctx.send(embed=embed)
    
    @commands.command(name="chat")
    async def chat(self, ctx, *, message: str):
        responses = ["Interesting.", "Tell me more.", "I see.", "That's cool!", "Hmm."]
        embed = discord.Embed(description=random.choice(responses), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="uwuify")
    async def uwuify(self, ctx, *, text: str):
        uwu = text.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
        embed = discord.Embed(description=f"uwu {uwu}", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="marry")
    async def marry(self, ctx, partner: discord.Member):
        if partner == ctx.author:
            embed = discord.Embed(description="You can't marry yourself!", color=0xdc143c)
            return await ctx.send(embed=embed)
        embed = discord.Embed(description=f"💍 {ctx.author.mention} married {partner.mention}! Congratulations!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="divorce")
    async def divorce(self, ctx):
        embed = discord.Embed(description=f"💔 {ctx.author.mention} got divorced. Sad!", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="dadjoke")
    async def dadjoke(self, ctx):
        jokes = ["Why don't scientists trust atoms? Because they make up everything!", "What do you call a fake noodle? An impasta!", "Why did the scarecrow win an award? He was outstanding in his field!"]
        embed = discord.Embed(description=random.choice(jokes), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="uselessfact")
    async def uselessfact(self, ctx):
        facts = ["A day on Venus is longer than a year on Venus.", "Honey never spoils.", "Octopuses have three hearts."]
        embed = discord.Embed(description=random.choice(facts), color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="pp")
    async def pp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        size = "=" * random.randint(1, 20)
        embed = discord.Embed(description=f"{member.name}'s pp: 8{size}D", color=0xdc143c)
        await ctx.send(embed=embed)
    
    @commands.command(name="autismrate")
    async def autismrate(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        rate = random.randint(0, 100)
        embed = discord.Embed(description=f"{member.mention} is `{rate}%` autistic", color=0xdc143c)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Fun(bot))
