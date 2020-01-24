from discord.ext import commands
import discord
from classified.bot_token.token import bot_token
from src.commands.copypasta.EventFunction import copypasta_on_msg, blacklistCheck
from src.commands.Reactions.EventFunction import react_to_msg
from src.commands.Google.eventFunction import translate
from src.commands.Settings.controller import SettingsController

command_dictionary = ""
client = commands.Bot(command_prefix=".")


def get_setting_commands():
    command_dict = {}
    for cog in client.cogs:
        shortened = str(cog).replace("Cog", "").lower()
        command_dict[shortened] = []
        for command in client.get_cog(cog).get_commands():
            command_dict[shortened].append(str(command))
    return command_dict


@client.event
async def on_ready():
    """
    Runs when bot starts / connects to Discord
    :return: None
    """
    print('We have logged in as {0.user}'.format(client))
    global command_dictionary
    command_dictionary = get_setting_commands()


@client.event
async def on_disconnect():
    """
    Runs when bot gets shut down
    :return: None
    """
    print("Bot has logged off")


def is_enabled(message):
    command = message.content.split()[0][1:]
    command_module = ""
    for module in command_dictionary:
        if command in command_dictionary[module]:
            # print("here")
            command_module = module
    # print(command)
    # print(command_module)
    try:
        return SettingsController(message.guild).get_setting(command_module, command)
    except KeyError:
        return True


@client.event
@commands.cooldown(1, 2)
async def on_message(message):
    """
    Discord.py function. On message sent in any discord channel/server
    :param message: Message object from Discord.py
    :return: None
    """
    if message.author == client.user:
        return
    if len(message.content) > 0 and message.content[0] == "." and not is_enabled(message):
        return
    # if message.author.id != 169896955298709505:
    #     return
    # if message.author.id == 244573404059926529:
    #     return
    # log_chat("chatlogs", message)
    # if message.content.lower().startswith('hello') or message.content.lower().startswith("hey"):
    #     await message.channel.send('Hello {} !'.format(message.author.mention))
    #     return

    await client.process_commands(message)
    await react_to_msg(message, client)
    await copypasta_on_msg(message)
    await blacklistCheck(message)
    await translate(message)


@client.event
async def on_message_edit(before, after):
    if after.author == client.user or before.content == after.content:
        return

    if not SettingsController(after.guild).get_setting("logging", "on_edit"):
        return
    channel = SettingsController(after.guild).get_option("logging", "on_edit", "channel_to_post_in")
    embed = discord.Embed(title='@' + after.author.display_name,
                          description="Message edited in {}".format(after.channel.name),
                          color=0xf0f0f0)
    embed.add_field(name="Before", value=before.content, inline=False)
    embed.add_field(name="After", value=after.content, inline=False)
    embed.add_field(name='Edited at', value=after.edited_at, inline=False)
    embed.add_field(name="Jump to message", value=after.jump_url)
    await discord.utils.get(after.guild.channels, id=int(channel)).send(embed=embed)


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    if not SettingsController(message.guild).get_setting("logging", "on_edit"):
        return
    channel = SettingsController(message.guild).get_option("logging", "on_edit", "channel_to_post_in")
    embed = discord.Embed(title='@' + message.author.display_name,
                          description="Message deleted in {}".format(message.channel.name),
                          color=0xf0f0f0)
    embed.add_field(name="Message", value=message.content, inline=False)
    await discord.utils.get(message.guild.channels, id=int(channel)).send(embed=embed)


# LOAD COGS

client.load_extension("src.commands.BotMiscellaneous.cog")
client.load_extension("src.commands.Youtube.cog")
client.load_extension("src.commands.Reddit.cog")
client.load_extension("src.commands.Dictionary.cog")
client.load_extension("src.commands.Reactions.cog")
client.load_extension("src.commands.copypasta.cog")
client.load_extension("src.commands.DiscordVoice.cog")
client.load_extension("src.commands.RateGirl.cog")
client.load_extension("src.commands.Blacklist.cog")
client.load_extension("src.commands.Settings.cog")
client.run(bot_token)

# DONE Create the class for reactions triggered by keywords
# STUPIDTODO create the class for bot messages that start with
# TODO make bot save images
# TODO MAKE bot play music - bot can currently join/leave channels - postponed until bot is hosted
# TODO HOST BOT on a server
