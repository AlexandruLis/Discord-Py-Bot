from discord.ext import commands
from src.commands.Youtube.youtube import YouTube


class YoutubeCog(commands.Cog):
    """
    Searches youtube for a topic
    """

    def __init__(self, bot):
        """
        :param bot: commands.Bot from discord.ext
        """
        self.client = bot

    @commands.command()
    async def yt(self, ctx):
        """
        First result from youtube
        :param ctx: the full discord message from the user as a Context class from Discord.py
        :return:
        """
        search = " ".join(ctx.message.content.split()[1:])
        await ctx.message.channel.send(YouTube().find_first(search))

    @commands.command()
    async def ryt(self, ctx):
        """
        Random result from search
        :param ctx: the full discord message from the user as a Context class from Discord.py
        :return:
        """
        message = ctx.message
        search = " ".join(ctx.message.content.split()[1:])
        await message.channel.send(YouTube().rand_find(search))


def setup(bot):
    bot.add_cog(YoutubeCog(bot))
