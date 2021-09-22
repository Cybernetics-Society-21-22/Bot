import discord
from discord.ext import commands, tasks

COLOUR = 0x22C2B6  # gotten from the logo

# Commands that provide information about the server, and specific users.


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite()
        await ctx.reply(link)

    @commands.command(aliases=["statistics", "stats"])
    async def serverInfo(self, ctx):

        listOfBots = [bot.mention for bot in ctx.guild.members if bot.bot]

        embedVar = discord.Embed(
            title=ctx.guild.name, description="", color=COLOUR).set_thumbnail(url=ctx.guild.icon_url)

        embedVar.add_field(
            name="Member Count", value=ctx.guild.member_count - len(listOfBots), inline=True)

        embedVar.add_field(name="Bot Count", value=str(
            len(listOfBots)), inline=True)

        embedVar.add_field(name="Highest Role",
                           value=ctx.guild.roles[-1], inline=True)

        embedVar.add_field(name="Owner",
                           value=str(ctx.guild.owner.display_name), inline=True)

        embedVar.add_field(name="No. of Channels",
                           value=str(len(ctx.guild.voice_channels)+len(ctx.guild.text_channels)), inline=True)

        await ctx.reply(embed=embedVar)

    @commands.command(aliases=["whois", "user"])
    async def userinfo(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]

        embedVar = discord.Embed(
            title=f"User info of: {member.display_name}", description="", color=COLOUR).set_thumbnail(url=member.avatar_url)

        embedVar.add_field(name="Username", value=member)

        embedVar.add_field(name="User ID", value=member.id)

        embedVar.add_field(name="Created At", value=member.created_at.strftime(
            "%a, %d %B %Y, %I:%M %p UTC"))

        embedVar.add_field(name="Joined At", value=member.joined_at.strftime(
            "%a, %d %B %Y, %I:%M %p UTC"))

        embedVar.add_field(name=f"Roles ({len(roles)})", value=" ".join(
            [role.mention for role in roles]))

        if member.id == 659431002556596234:
            embedVar.add_field(name="Extra Info",
                               value="Coolest person to ever live and the person who made this command.", inline=False)

        await ctx.reply(embed=embedVar)


def setup(client):
    client.add_cog(Info(client))
