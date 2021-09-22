"""
Commands that provide information about the server, and specific users.
"""
import discord
from discord.ext import commands
from discord.utils import escape_markdown

embed_color = 0x22C2B6  # Picked up from the Cybernetics Logo


class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        link = "https://discord.gg/KcbJYSsVvj"
        await ctx.reply(link, mention_author=False)

    @commands.command(aliases=["statistics", "stats", "severinfo"])
    async def server_info(self, ctx):
        bots_in_server = [bot for bot in ctx.guild.members if bot.bot]

        embed = discord.Embed(title=ctx.guild.name, color=embed_color).set_thumbnail(
            url=ctx.guild.icon_url
        )

        fields = {
            "Member Count": ctx.guild.member_count - len(bots_in_server),
            "Channel Count": len(ctx.guild.channels),
        }

        embed.add_field(name="Server Information", value='\n'.join([f"Member Count: {ctx.guild.member_count - len(bots_in_server)}",
            f"Channel Count: {len(ctx.guild.channels)}"]), inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["user", "userinfo"])
    async def user_info(self, ctx):

        embed_title = escape_markdown(
            f"{ctx.author.nick} ({ctx.author.name}#{ctx.author.discriminator})"
            if ctx.author.nick
            else ctx.author.name
        )
        roles = ", ".join(
            role.mention for role in ctx.author.roles[:0:-1]
        )  # 0 to remove @everyone and -1 to put in order of hierarchy

        embed = discord.Embed(title=embed_title, color=ctx.author.color).set_thumbnail(
            url=ctx.author.avatar_url
        )

        embed.add_field(
            name="**User Information**",
            value="\n".join(
                [f"Created: <t:{int(ctx.author.created_at.timestamp())}:R>", f"ID: {ctx.author.id}"]
            ), inline=False
        )

        embed.add_field(
            name="**Member Information**",
            value="\n".join(
                [f"Joined: <t:{int(ctx.author.joined_at.timestamp())}:R>", f"Roles: {roles}"]
            ), inline=False
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Info(client))
