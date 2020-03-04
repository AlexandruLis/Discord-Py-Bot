import discord
from src.commands.BotMiscellaneous.cog import MiscellaneousCog
from textblob import TextBlob
from textblob.exceptions import NotTranslated
from polyglot.text import Text, Word
from src.commands.Settings.controller import SettingsController


# DetectorFactory.seed = 0


async def translate(message):
    message_content = MiscellaneousCog.removeEmojiAndPings(message.content)
    if len(message_content) < 2 or message.content == '' or message.content.startswith('.'):
        return

    if not SettingsController(message.guild).get_setting("google", "translate"):
        return

    languages = SettingsController(message.guild).get_option("google", "translate", "languages")
    # print(languages)
    text = Text(message_content)
    guess = text.language.code
    # print(guess)
    if guess != 'en' and guess in languages:  # and guess.confidence > 0.8:
        # print(translator.translate(message_content, src=guess.lang).text + "  source: =" + message_content)
        try:
            translation = str(TextBlob(message_content).translate())
        except NotTranslated:
            return
        if translation.lower() == message_content.lower():
            return
        embed = discord.Embed(title='@' + message.author.display_name + " said [{}]".format(guess),
                              description=translation,
                              color=0xf0f0f0)
        await message.channel.send(embed=embed)
