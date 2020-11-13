from src.commands.copypasta.controller import QuotesController
from src.commands.Blacklist.blacklistStorage import Blacklist
from classified.globals import blacklist_file_path
import time
from src.commands.Settings.controller import SettingsController

last_used_time = 0  # A global cooldown time


async def quoteMsg(message):
    """
    Used to check if the message is  copy pasta.
    Full implementation in copypasta
    :param message: Discord.py message Class
    :return: None
    """
    global last_used_time  # Init global cooldown
    # Admin has 0 cd
    if not message.author.top_role.permissions.administrator:
        # Non-Admin can't trigger during cd
        if last_used_time + 15 > time.time():
            return
    if not SettingsController(message.guild).get_setting("copypasta", "respond"):
        return
    quotesDict = QuotesController(message.guild).get_dict()  # Load the controller
    content = message.content

    if message.content in quotesDict:  # If the message is in the dict keys
        quoteData = quotesDict[content]  # Found
        if quoteData[1] == 1:  # If bits for the copypasta are set to 1 remove the trigger message
            await message.delete()
        # print(quotesController.get_dict())
        await message.channel.send(quoteData[0])  # Print the copypasta
        return


async def blacklistCheck(message):
    blacklistCtr = Blacklist(blacklist_file_path + str(message.channel.guild.id))  # Load the controller
    if blacklistCtr.userExists(message.author.id, message.channel.id):
        await message.delete()
    if blacklistCtr.exists(message.content, message.channel.id):
        await message.delete()
