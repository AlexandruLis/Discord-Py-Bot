from discord.ext import commands
from src.commands.Reactions.controller import ReactionsController


class ReactionsCog(commands.Cog):
    """
    Bot adds a reaction if it finds a keyword in a discord message
    Bot must be in the channel with the emote !! Otherwise the bot doesn't have access to it!
    """

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def addreact(self, ctx):
        """
        Add a reaction to a keyword/keywords
        Requires admin rights to use command
        :param ctx: the full discord message from the user as a Context class from Discord.py
        :return: None
        """
        message = ctx.message
        if not message.author.top_role.permissions.administrator:
            await message.channel.send("You have no power here")
            return
        try:
            emote_data = ReactionsController(self.client, ctx.guild).add(message.content)
            if emote_data == 0:
                await message.channel.send("Emote already here")
                return
            elif emote_data == -1:
                await message.channel.send("Emote data invalid")
                return
            await message.channel.send(
                "Added {} on word(s) {}".format(self.client.get_emoji(emote_data[1]), emote_data[0]))
        except ValueError:
            await message.channel.send("Emote not recognized")

    @commands.command()
    async def rmreact(self, ctx):
        """
        Removes a reaction to a keyword/keywords
        Requires admin rights to use command
        :param ctx: the full discord message from the user as a Context class from Discord.py
        :return: None
        """
        controller = ReactionsController(self.client, ctx.guild)
        message = ctx.message
        if message.author.top_role.permissions.administrator:
            controller.remove(message.content.split()[1])
            await message.channel.send("Removed Sucessfully!")
        else:
            await message.channel.send("You have no power here")


def setup(bot):
    bot.add_cog(ReactionsCog(bot))
