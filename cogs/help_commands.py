import discord
from discord.ext import commands

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.get_prefix_custom = self.get_prefix_custom
        self.bot.support_server = self.support_server
        self.bot.banner_url = self.banner_url
        self.bot.bot_name = self.bot_name
    
    def get_prefix_custom(self, guild):
        return self.bot.data['custom_prefix'].get(str(guild.id), ".")
    
    @property
    def support_server(self):
        return "discord.gg/ekittens"
    
    @property
    def banner_url(self):
        return "https://i.pinimg.com/originals/7f/eb/24/7feb24f573c4950b5fde5b883c731b1c.gif"
    
    @property
    def bot_name(self):
        return "koji"
    
    class HelpDropdown(discord.ui.View):
        def __init__(self, prefix, bot):
            super().__init__(timeout=60)
            self.prefix = prefix
            self.bot = bot
        
        @discord.ui.select(
            placeholder="Select a module",
            options=[
                discord.SelectOption(label="Moderation", description="Moderate your server", emoji="🛡️"),
                discord.SelectOption(label="Economy", description="Economy system", emoji="💰"),
                discord.SelectOption(label="Fun", description="Games and interactions", emoji="🎮"),
                discord.SelectOption(label="Information", description="User and server info", emoji="📊"),
                discord.SelectOption(label="Utility", description="Conversion and tools", emoji="🔧"),
                discord.SelectOption(label="Music", description="Voice channel music", emoji="🎵"),
                discord.SelectOption(label="Snipe", description="Message sniping", emoji="🎯"),
                discord.SelectOption(label="Reaction", description="Reaction roles", emoji="😀"),
                discord.SelectOption(label="Server", description="Server configuration", emoji="⚙️"),
                discord.SelectOption(label="Security", description="Anti-nuke features", emoji="🔒"),
            ]
        )
        async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
            module = select.values[0]
            embed = await self.get_module_embed(module)
            await interaction.response.edit_message(embed=embed, view=self)
        
        async def get_module_embed(self, module):
            embed = discord.Embed(title=module, color=0xdc143c)
            commands_list = {
                "Moderation": "`kick`, `ban`, `unban`, `mute`, `unmute`, `warn`, `warns`, `clearwarns`, `purge`, `lock`, `unlock`, `slowmode`, `nickname`, `role`, `jail`, `unjail`, `softban`, `hackban`, `muteall`, `unmuteall`, `hide`, `reveal`, `cleanup`, `stripstaff`, `mutelist`, `inrole`, `drag`, `newusers`",
                "Economy": "`balance`, `daily`, `give`, `rob`, `leaderboard`, `work`, `beg`, `shop`, `buy`, `inventory`",
                "Fun": "`8ball`, `ship`, `hug`, `kiss`, `slap`, `kill`, `cat`, `dog`, `gayrate`, `insult`, `truthordare`, `tictactoe`, `rockpaperscissors`, `guess`, `chat`, `uwuify`, `marry`, `divorce`, `dadjoke`, `uselessfact`, `pp`, `autismrate`",
                "Information": "`userinfo`, `serverinfo`, `avatar`, `roleinfo`, `channelinfo`, `bots`, `boosters`, `botinfo`, `servericon`, `guildbanner`, `rolelist`, `membercount`, `firstmessage`",
                "Utility": "`ping`, `uptime`, `invite`, `afk`, `poll`, `calculate`, `translate`, `define`, `choices`, `mock`, `colour`, `hex`, `randomhex`, `tts`, `search`, `emoji`, `sticker`",
                "Music": "`play`, `playing`, `pause`, `resume`, `queue`, `skip`, `stop`, `volume`, `loop`, `restart`",
                "Snipe": "`snipe`, `editsnipe`, `reactionsnipe`, `purgesnipe`, `clearsnipe`, `cleareditsnipe`, `clearreactionsnipes`, `clearpurgesnipe`",
                "Reaction": "`autoreact`, `reactionrole`, `reactionlist`",
                "Server": "`prefix`, `autorole`, `welcome`, `goodbye`, `pin`, `unpin`, `thread`, `enablecommand`, `disablecommand`, `ignore`",
                "Security": "`isolate`, `unisolate`, `logs`, `whitelist`, `blacklist`"
            }
            embed.add_field(name="Commands", value=commands_list.get(module, "No commands"), inline=False)
            embed.add_field(name="How to use", value=f"Use `{self.prefix}help <command>` to see more command info.", inline=False)
            embed.set_footer(text=f"{self.bot.bot_name} • Commands marked with * indicate subcommands")
            return embed
    
    @commands.command(name="help")
    async def help_command(self, ctx, *, command_name: str = None):
        prefix = self.get_prefix_custom(ctx.guild)
        
        if command_name:
            embed = discord.Embed(title=command_name, color=0xdc143c)
            embed.add_field(name="Syntax", value=f"`{prefix}{command_name}`", inline=False)
            embed.add_field(name="Cooldown", value="1 per 1.0s", inline=True)
            embed.add_field(name="Module", value="Help", inline=True)
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title=f"{self.bot_name} help",
            description="Use the dropdown menu below to see commands.",
            color=0xdc143c
        )
        embed.set_image(url=self.banner_url)
        embed.add_field(name="How to use", value=f"Use `{prefix}help <command>` to see more command info.", inline=False)
        embed.add_field(name="Need support?", value=f"Join the [support server]({self.support_server}) if you're stuck.", inline=False)
        embed.add_field(name="Additional info", value="Anything in `<>` is required, `[]` is optional.\n[TOS](https://discord.com/terms) • [Privacy](https://discord.com/privacy)", inline=False)
        embed.set_footer(text=f"{len(self.bot.commands)} commands • 10 modules")
        
        view = self.HelpDropdown(prefix, self.bot)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpCommands(bot))
