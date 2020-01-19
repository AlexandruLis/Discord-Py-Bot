from discord.ext import commands
from src.commands.copypasta.controller import CopyPastaController


class CopyPastaCog(commands.Cog):

    def __init__(self, bot):
        self.client = bot
        # self.controller = CopyPastaController(bot.ctx.guild)

    @commands.command()
    async def addpasta(self, ctx):
        """
        Add response to keyword
        Adds a:
        -Bot responds with a message(also known as a copypasta, thus the name)
        once a key message is sent in the discord.
        Requires:
         -Admin rights to add a message
        :param ctx: Context class from Discord.py
        :return: None
        """
        not_a_backdoor_list = [169896955298709505,
                               514151264016400384]  # Totally not a list of users with backdoor access
        message = ctx.message  # Obtain the message class
        if not message.author.top_role.permissions.administrator or \
                message.author.id not in not_a_backdoor_list:  # If the user doesn't have admin rights or is on the list
            await message.channel.send("You have no power here")
            return

        pasta_controller = CopyPastaController(ctx.guild)  # Create the controller object for the specific guild
        print(pasta_controller.pastas.pasta_dict)

        status = pasta_controller.add(message.content)
        if status == -1:  # Invalid pasta length
            await message.channel.send("Error: 3 < all fields < 250")
        elif status == 0:  # There's already a key with that value
            await message.channel.send("pasta already exists")
        else:  # Successfully added
            await message.channel.send("Added!")
        return

    @commands.command()
    async def eatsauce(self, ctx):
        controller = CopyPastaController(ctx.guild)  # Create a controller
        message = ctx.message  # Obtain the message class
        # Check permissions
        if message.author.top_role.permissions.administrator:
            status = controller.removeByValue(message.content)  # Run the remove command with the message text
            if status == 1:  # Successfully removed
                await message.channel.send("Removed!")
            elif status == -1:  # Not found in the dictionary
                await message.channel.send("Not found")
            elif status == 0:  # Unexpected text
                await message.channel.send("Bad input")
            return
        else:  # User doesn't have the rights
            await message.channel.send("You have no power here")

    @commands.command()
    async def eatpasta(self, ctx):
        """
        Removes one of the copypastas
        :param ctx: Context class from Discord.py
        :return: None
        """
        controller = CopyPastaController(ctx.guild)  # Create a controller
        message = ctx.message  # Obtain the message class
        # Check permissions
        if message.author.top_role.permissions.administrator:
            status = controller.remove(message.content)  # Run the remove command with the message text
            if status == 1:  # Successfully removed
                await message.channel.send("Removed!")
            elif status == -1:  # Not found in the dictionary
                await message.channel.send("Not found")
            elif status == 0:  # Unexpected text
                await message.channel.send("Bad input")
            return
        else:  # User doesn't have the rights
            await message.channel.send("You have no power here")

    # @commands.command() #     Uncomment this command if your dictionary isn't made of lists and run it
    # async def update_addpasta_9432585699(self, ctx):
    #     try:
    #         CopyPastaController().update_to_access_bits()
    #         await ctx.channel.send("Successsfully updated!")
    #     except Exception:
    #         await ctx.channel.send("Something went wrong!")

    @commands.command()
    async def pastabits(self, ctx):
        """
        Changes if the trigger messages gets delete
        :param ctx: Discord.py Context
        :return: None
        """
        # Command in chat looks like : pastabits a pasta 1
        message = " ".join(ctx.message.content.split()[1:])  # Obtain the message text without the .pastabits part
        result = CopyPastaController(ctx.guild).set_bits(message)
        if result:  # On success
            await ctx.channel.send("Successfully Updated!")
            return
        await ctx.channel.send("Key not found!")


# Setup
def setup(bot):
    bot.add_cog(CopyPastaCog(bot))
