from discord.ext import commands
import discord
from classified.globals import imgflip_username, imgflip_password
import requests


class MemesCog(commands.Cog):
    """
    """

    def __init__(self, bot):
        self.client = bot
        self.memes = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']

    @commands.command(pass_context=True)
    async def mkmm(self, ctx, meme_format, *args):
        url = 'https://api.imgflip.com/caption_image'
        template_id = 0
        try:
            # Check if ID supplied
            template_id = int(meme_format)
        except ValueError:
            for meme in self.memes:
                if meme_format in meme['name'].casefold():
                    template_id = meme['id']
                    break
        params = dict(template_id=template_id, username=imgflip_username, password=imgflip_password)
        for i, text in enumerate(args):
            params["text" + str(i)] = text
        if len(args) == 0:
            params["text0"] = "  "

        res = requests.get(url, params=params)
        data = res.json()
        print(data)
        if not data['success']:
            await ctx.send('Meme not found, .memeinfo for more details')
            return
        embed = discord.Embed(title='@' + ctx.message.author.display_name,
                              description='https://imgflip.com/memetemplates', color=0xf0f0f0)
        embed.set_image(url=data['data']['url'])
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def memeinfo(self, ctx):
        await ctx.send('Go to https://imgflip.com/memetemplates . Click on the Template, then on Blank Template, then '
                       'provide Template ID')


def setup(bot):
    bot.add_cog(MemesCog(bot))
