import discord

from utils.core import Configuration, Database, Views
from discord import SlashCommandGroup
from discord.commands import slash_command
from discord.ext import commands


class Moderation_Module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Moderation Module Loading...")
    

    @slash_command(
        name = "modmenu",
        description = "Moderation menu to better upkeep servers."
    )
    async def modmenu(
        self,
        ctx,
        member: discord.Option(discord.Member, description = "Select a server member to target. (Target yourself to unlock utility commands)")
    ):
        user_power = ctx.author.guild_permissions.administrator
        if user_power == True:
            embed, view = await Views.Setup_ModMenu(self.bot,ctx, member, ctx.author)

            message = await ctx.respond(
                embed = embed,
                view = view
            )
        else:
            await ctx.respond("You do not have server permissions to use that command!")


    # When members join specific servers.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id
        username = member.name
        server_name = member.guild

        embed = discord.Embed(title = f"{username} Joined the server!", description = "You have been given default roles. Welcome to Dula Peep!", color=discord.Color.from_rgb(169, 128, 207))
        embed.set_thumbnail(url = member.avatar.url)
        embed.set_author(name = username, icon_url=member.avatar.url)
        #embed.set_footer(text = "", icon_url="")


        channel = 0
        if guild_id == 980656704763068466: # Dula Peep
            channel = await self.bot.fetch_channel(984278425655205888)
            default_roles = [983869009780932708, 983871181314736199, 984280405622530088]
            for role in default_roles:
                add_role = member.guild.get_role(role)
                await member.add_roles(add_role)


        if guild_id == 778162776610832384: # Maven Server
            channel = await self.bot.fetch_channel(778162776610832386)

        await channel.send(embed=embed)



def setup(bot):
    bot.add_cog(Moderation_Module(bot))