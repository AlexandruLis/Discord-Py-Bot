from discord.ext import commands
import discord
from src.commands.RateGirl.rategirl import RateGirl
from PIL import Image, ImageDraw, ImageFont
from classified.globals import not_a_girl, spam_guild_id, spam_guild_channel as spam_channel_id


class DiscordRateGirl(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @staticmethod
    def draw_the_picture(xpoint, ypoint):
        img = Image.open('../assets/small_heart.png', 'r')
        im = Image.new('RGBA', (1200, 1200), (255, 255, 255, 255))
        font = ImageFont.truetype("../assets/ManhattanDarling-Regular.ttf", size=50)
        draw = ImageDraw.Draw(im)
        # draw the graph
        draw.line(xy=[(100, 700), (1100, 100)], fill=(0, 0, 0), width=3)  # Hot-crazy border line
        draw.line(xy=[(100, 700), (100, 100)], fill=(0, 0, 0), width=3)  # Crazy axis
        draw.line(xy=[(600, 700), (600, 100)], fill=(0, 0, 0), width=3)  # 5 hot line
        draw.line(xy=[(800, 1100), (800, 280)], fill=(0, 0, 0), width=3)  # 8 Hot line
        draw.line(xy=[(800, 400), (1100, 400)], fill=(0, 0, 0), width=3)  # Wife to date zone separator
        draw.line(xy=[(800, 600), (1100, 600)], fill=(0, 0, 0), width=3)  # Date to unicorn separator
        draw.line(xy=[(100, 700), (1100, 700)], fill=(0, 0, 0), width=3)  # Hot Axis
        # draw the text
        draw.text(xy=(40, 40), text="Crazy", fill=(255, 0, 0), font=font)
        draw.text(xy=(1120, 680), text="Hot", fill=(255, 0, 0), font=font)

        draw.text(xy=(250, 300), text="NO-GO", fill=(0, 0, 0), font=font)

        draw.text(xy=(700, 130), text="DANGER", fill=(0, 0, 0), font=font)
        draw.text(xy=(700, 170), text="ZONE", fill=(0, 0, 0), font=font)

        draw.text(xy=(670, 450), text="FUN", fill=(0, 0, 0), font=font)
        draw.text(xy=(670, 490), text="ZONE", fill=(0, 0, 0), font=font)

        draw.text(xy=(930, 250), text="DATE", fill=(0, 0, 0), font=font)
        draw.text(xy=(930, 290), text="ZONE", fill=(0, 0, 0), font=font)

        draw.text(xy=(930, 450), text="WIFE", fill=(0, 0, 0), font=font)
        draw.text(xy=(930, 490), text="ZONE", fill=(0, 0, 0), font=font)

        draw.text(xy=(900, 640), text="UNICORNS", fill=(0, 0, 0), font=font)

        draw.text(xy=(910, 760), text=not_a_girl.upper(), fill=(0, 0, 0), font=font)
        # get the heart
        im.paste(img, [xpoint, ypoint], mask=img)
        del draw

        # write to stdout
        im.save('../assets/rate_girl_result.png', "PNG")

    @commands.command(pass_context=True)
    async def rategirl(self, ctx):
        """
        Rates @User by 2 values, Hot and Crazy
        :param ctx: Context from message
        :return: None
        """

        user_id = float(
            "".join([s for s in ctx.message.content.split()[1] if s.isdigit()]))  # transform user id into a float
        try:
            hot_value, crazy_value, hot_position, crazy_position, result = RateGirl().rategirl(
                user_id)  # Call function for pseudo rng

            print(hot_value, crazy_value, hot_position, crazy_position, result)
            self.draw_the_picture(hot_position, crazy_position)
            from classified.bot_token.rategirl import rating_message
            embed = discord.Embed()
            embed.add_field(name='Hot', value=str(hot_value))
            embed.add_field(name='Crazy', value=str(crazy_value))
            embed.add_field(name='Status', value=result)
            embed.add_field(name='Advice', value=rating_message[result], inline=False)
            link = await self.generate_picture_link()
            embed.set_image(url=link)
            await ctx.channel.send(embed=embed)  # Send formatted message
        except ValueError or ZeroDivisionError:
            pass

    async def generate_picture_link(self):
        spam_channel = None
        embed_picture = None
        for guild in self.client.guilds:
            if guild.id == spam_guild_id:
                for channel in guild.channels:
                    if channel.id == spam_channel_id:
                        spam_channel = channel
        await spam_channel.send(file=discord.File('../assets/rate_girl_result.png'))
        async for message in spam_channel.history(limit=1):
            embed_picture = message.attachments[0].url
        return embed_picture


def setup(bot):
    bot.add_cog(DiscordRateGirl(bot))
