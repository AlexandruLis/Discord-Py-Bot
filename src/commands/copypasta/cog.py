from discord.ext import commands
from src.commands.copypasta.controller import QuotesController
from src.core.Validation import validateAdmin


class QuotesCog(commands.Cog):

    def __init__(self, bot):
        self.client = bot

    @commands.command(pass_context=True)
    async def addQ(self, ctx, key, quote, bits, *args):
        """
        Add quote, args: key, quote, bits
        :param ctx: Context class from Discord.py
        :return: None
        """
        if not await validateAdmin(ctx.message):
            return
        quotesController = QuotesController(ctx.guild)  # Create the controller object for the specific guild

        status = quotesController.add(key, quote, bits)
        if status == -1:  # Invalid quote length
            await ctx.channel.send("Error: limit is 3-100 characters")
        elif status == 0:  # There's already a key with that value
            await ctx.channel.send("Error: Quote already exists")
        else:  # Successfully added
            await ctx.channel.send("Success!")
        return

    @commands.command(pass_context=True)
    async def rmQh(self, ctx, quote, *args):
        """
        Remove quote by message
        :param ctx:
        :return:
        """
        controller = QuotesController(ctx.guild)  # Create a controller
        message = ctx.message  # Obtain the message class
        # Check permissions
        if message.author.top_role.permissions.administrator:
            status = controller.removeByQuote(quote)
            if status == 1:  # Successfully removed
                await message.channel.send("Removed!")
            elif status == -1:  # Not found in the dictionary
                await message.channel.send("Not found")
            elif status == 0:  # Unexpected text
                await message.channel.send("Bad input")
            return
        else:  # User doesn't have the rights
            await message.channel.send("You have no power here")

    @commands.command(pass_context=True)
    async def rmQ(self, ctx, key, *args):
        """
        Remove quote
        :param ctx: Context class from Discord.py
        :return: None
        """
        quotesController = QuotesController(ctx.guild)  # Create a controller
        if not await validateAdmin(ctx.message):
            return

        status = quotesController.remove(key)  # Run the remove command with the message text
        if status == 1:  # Successfully removed
            await ctx.channel.send("Removed!")
        elif status == -1:  # Not found in the dictionary
            await ctx.channel.send("Not found")
        elif status == 0:  # Unexpected text
            await ctx.channel.send("Bad input")
        return

    @commands.command(pass_context=True)
    async def upQbits(self, ctx, key, bits):
        """
        Changes if the trigger messages gets delete
        :param ctx: Discord.py Context
        :return: None
        """
        if not await validateAdmin(ctx.message):
            return

        result = QuotesController(ctx.guild).set_bits(key, bits)
        if result:
            await ctx.channel.send("Successfully Updated!")
            return
        await ctx.channel.send("Key not found!")


# Setup
def setup(bot):
    bot.add_cog(QuotesCog(bot))
