from discord.ext import commands
import discord
import random
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import re
import urllib3
import urllib.request
import urllib.parse
import os
import argparse
import sys
import json
import time
import inspect
import datetime
import asyncio
import re

repeaters = []
counter = 0
votekick_on = 0


class MiscellaneousCog(commands.Cog):
    def __init__(self, bot):
        self.client = bot

    @commands.command()
    async def changelog(self, ctx):
        await ctx.message.channel.send(
            "This is a changelog"
        )

    @commands.command(pass_context=True)
    async def lb(self, ctx):
        """
        Turn lb into kg (imperial to metric)
        :param ctx: Discord.py context
        :return: None
        """
        lb = float(ctx.message.content.split()[1])
        await ctx.channel.send("That is {0:.2f} kg".format(lb * 0.453592))

    @commands.command(pass_context=True)
    async def kg(self, ctx):
        """
        Turn kg into lb (metric to imperial)
        :param ctx:
        :return: None
        """
        lb = float(ctx.message.content.split()[1])
        await ctx.channel.send("That is {0:.2f} lbs".format(lb * 2.20462))

    @commands.command(pass_context=True)
    async def ft(self, ctx):
        """
        Turns height ft.inch (Eg: 5.11) to cm (imperial to metric)
        :param ctx: Discord.py context
        :return: None
        """
        value = float(ctx.message.content.split()[1])
        lb = int(value)
        inch = (value - int(value)) * 10
        cm = lb * 30.48 + inch * 2.54
        print(lb, inch)
        await ctx.channel.send("That is {0:.2f} cm".format(cm))

    @commands.command(pass_context=True)
    async def cm(self, ctx):
        """
        Turns cm (height) to ft + inch (metric to imperial) by approximation
        :param ctx: Discord.py context
        :return: None
        """
        value = float(ctx.message.content.split()[1])
        ft = int(value * 0.0328084)
        inch = round((value * 0.0328084 - ft) * 12)
        await ctx.channel.send("That is {}ft {}inches".format(ft, inch))

    @commands.command(pass_context=True)
    async def dice(self, ctx):
        """
        Rolls 2 dice ( returns 2 values between 1-6)
        :param ctx: Discord.py context
        :return: None
        """
        await ctx.channel.send(str(random.randint(1, 6)) + " " + str(random.randint(1, 6)))

    @commands.command()
    async def killbot(self, ctx):
        """
        Turns the bot off (admin only)
        :param ctx: Context class from Discord.py
        :return:
        """
        message = ctx.message
        # await self.client.close()

    @commands.command()
    async def goodbot(self, ctx):
        """
        Filler command. Bot sends a message on call.
        :param ctx: Context class from Discord.py
        :return: None
        """
        pass

    @commands.command()
    async def badbot(self, ctx):
        """
        Same as goodbot
        """
        pass

    @staticmethod
    def verify_vote(vote_list, new_vote):
        if new_vote not in vote_list:
            return True
        return False

    @commands.command()
    async def votekick(self, ctx):
        """
        Starts a votekick for a certain user, needs 51% votes
        :param ctx: Context
        :return: None
        """
        global votekick_on
        if votekick_on == 1:
            await ctx.channel.send("A votekick is already open")
            return
        votekick_on = 1
        voted = []  # list of user ID's that voted
        message = ctx.message  # message string
        user = message.content.split()[1]  # user mention
        votes_needed = 9  # int(len(message.guild.members) / 2 + 1)
        current_votes = 0
        await ctx.message.channel.send(
            "Starting a votekick for user {}."
            " Type \"vote yes\" or \"vote no\" \n"
            "Votes needed:({}/{}) "
                .format(user, current_votes, votes_needed))
        bot_message = None
        async for message in ctx.channel.history(limit=50):
            if message.author.name == "Iku-nee":
                bot_message = message
                break
        timer = 60
        current_timer = 0
        while current_timer < timer:
            await asyncio.sleep(1)
            async for message in ctx.channel.history(limit=50):
                if message.content == "vote yes":
                    if MiscellaneousCog.verify_vote(voted, message.author.id):
                        current_votes += 1
                        voted.append(message.author.id)

                    await bot_message.edit(
                        content="Starting a votekick for user {}."
                                " Type \"vote yes\" or \"vote no\" \n"
                                "Votes needed:({}/{})"
                            .format(user, current_votes, votes_needed))
                    await message.delete()
                elif message.content == "vote no":
                    voted.append(message.author.id)
                    await message.delete()

            current_timer += 1
        if current_votes >= votes_needed:
            await ctx.channel.send("The senate decision is exile, begone {}!".format(user))
        else:
            await ctx.channel.send("The senate spares {}".format(user))
        votekick_on = 0

    @commands.command()
    async def erase(self, ctx):
        """
        Erase N messages (admin only)
        :param ctx: Discord.py Context
        :return: None
        """
        message = ctx.message
        if not message.author.top_role.permissions.administrator:
            return
        await message.delete()
        value = int(message.content.split()[1])
        await ctx.channel.purge(limit=value)

    @staticmethod
    def find_number_in_str(data: str):
        """
        Finds all the numbers in a string and returns them concatenated
        Should only be used for Discord ID parsing !! It doesn't have much benefit besides that!
        :param data: A string
        :return: Integer, the number created
        """
        number = ""
        for char in data:
            if '0' <= char <= '9':
                number += char
        try:
            return int(number)
        except ValueError:
            return -1

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(':ping_pong: {0}ms'.format(round(self.client.latency, 3) * 1000))

    @commands.command()
    async def al(self, ctx):
        character = ctx.message.content.split()[1:]
        character = [word.lower().capitalize() if word.lower() != 'of' else word.lower() for word in character]
        name = str('_'.join(character))
        print(name)
        try:
            r = requests.get(
                "https://azurlane.koumakan.jp/w/index.php?search=" + name)  # goes to link for word
            soup = BeautifulSoup(r.content, features="html.parser")  # sets up soup

            # setup color
            colors = {'Plum': 0xcc00cc, 'PaleGoldenrod': 0xffff00, 'background-image': 0xFF0000, 'PowderBlue': 0x3399FF,
                      'Gainsboro': 0xC0C0C0}
            # print(soup.select('table > tbody')[0].find_all('td')[1].attrs['style'])
            try:
                color = colors[soup.select('table > tbody')[0].find_all('td')[1].attrs['style'].split(':')[1]]
            except IndexError:
                return
            #

            # Grab the stats of the ship
            fields = []
            i = 0
            for table in soup.find_all("table", {'class': 'wikitable'}):
                if i == 0:
                    pass
                if i == 3:
                    for row in table.tbody:
                        if isinstance(row, NavigableString):
                            continue
                        else:
                            for dataCell in row:
                                if isinstance(dataCell, NavigableString):
                                    continue
                                elif dataCell.text.strip() != '':
                                    fields.append(dataCell.text.strip())
                    break
                i += 1

            for a in soup.find_all('img'):
                result = a['src']
                if type(result) is str:
                    if result.find(name + ".png") != -1:
                            # print(result)
                            embed = discord.Embed(title=name, description="Level 120 Stats", color=color)
                            embed.set_image(url="https://azurlane.koumakan.jp" + result)
                            embed.add_field(name="HP", value=fields[0], inline=True)
                            embed.add_field(name="Armor", value=fields[1], inline=True)
                            embed.add_field(name="Reload", value=fields[2], inline=True)
                            embed.add_field(name="Luck", value=fields[3], inline=True)
                            embed.add_field(name="FP", value=fields[4], inline=True)
                            embed.add_field(name="Torp", value=fields[5], inline=True)
                            embed.add_field(name="Eva", value=fields[6], inline=True)
                            embed.add_field(name="Speed", value=fields[8], inline=True)
                            embed.add_field(name="AA", value=fields[9], inline=True)
                            embed.add_field(name="Air", value=fields[10], inline=True)
                            embed.add_field(name="Oil", value=fields[11], inline=True)
                            embed.add_field(name="Acc", value=fields[12], inline=True)
                            embed.add_field(name="Sub", value=fields[13], inline=True)
                            await ctx.channel.send(embed=embed)
                            return
        except KeyError or IndexError:
            print("No results")

    @staticmethod
    def findAllNumbersInString(data: str):
        numberList = []
        number = ""
        for char in data:
            if '0' <= char <= '9':
                number += char
            elif number != "":
                numberList.append(int(number))
                number = ""
        if number != "":
            numberList.append(int(number))
            number = ""
        try:
            return numberList
        except ValueError:
            return -1

    @staticmethod
    def removeEmojiAndPings(message: str):
        numbers = MiscellaneousCog.findAllNumbersInString(message)
        for number in numbers:
            message = re.sub('[<][ A-Za-z:0-9@!\-_]+[>]', '', message)
        return message

    @commands.command()
    async def hide(self, ctx):
        """
        Removes the messages of a user from a channel
        :param ctx: Discord.py Context
        :return: None
        """
        channel = ctx.channel
        if not ctx.message.author.top_role.permissions.administrator:
            return
        user = ctx.message.content.split()[1]  # raw user string name or nickname

        try:
            user_if_id = MiscellaneousCog.find_number_in_str(user)  # user id if given by pinging
        except ValueError:
            user_if_id = -1
        value = int(ctx.message.content.split()[2])  # number of messages to be deleted
        counter = 0  # messages found
        async for message in channel.history(limit=500):
            if counter == value:
                return
            if message.author.name == user or message.author.id == user_if_id:
                await message.delete()
                counter += 1

    @commands.command()
    async def avm(self, ctx):
        """
        Print avatar of pinged User
        :param ctx: Discord.py Context
        :return: None
        """
        author_id = self.find_number_in_str(ctx.message.content)
        for author in ctx.guild.members:
            if author.id == author_id:
                await ctx.channel.send(author.avatar_url)

    @commands.command()
    async def gif(self, ctx):
        """
        Searcher for a random gif from google
        :param ctx:
        :return:
        """
        url = 'https://www.google.com/search?tbm=isch&q=' + "+".join(ctx.message.content.split()[1:] + ["+gif"])
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.130 Safari/537.36"}

        actualImages = []  # contains the link for Large original images, type of  image
        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
        string_of_soup = str(soup)
        x = re.findall('(https:)([a-z\-_0-9\/\:\.]*\.(gif))', string_of_soup)
        for link in x:
            actualLink = ''.join(link[:-1])
            if actualLink.find('gstatic') == -1 and actualLink.find('i.gif') == -1:
                actualImages.append(actualLink)
        try:
            # print(actualImages)
            print(actualImages[0])
            embed = discord.Embed(title='@' + ctx.message.author.display_name, description=url, color=0xf0f0f0)
            embed.set_image(url=actualImages[0])
            await ctx.channel.send(embed=embed)
        except IndexError:
            await ctx.channel.send("Something went wrong! Try again later.")

    @commands.command()
    async def img(self, ctx):
        url = 'https://www.google.com/search?tbm=isch&q=' + "+".join(ctx.message.content.split()[1:])
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/79.0.3945.130 Safari/537.36"}
        actualImages = []  # contains the link for Large original images, type of  image

        soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
        string_of_soup = str(soup)
        x = re.findall('(https:)([a-z\-_0-9\/\:\.]*\.(jpg|jpeg|png))', string_of_soup)
        for link in x:
            actualLink = ''.join(link[:-1])
            if actualLink.find('gstatic') == -1 and actualLink.find('www.png') == -1:
                actualImages.append(actualLink)
        try:
            # print(actualImages)
            print(actualImages[0])
            embed = discord.Embed(title='@' + ctx.message.author.display_name, description=url, color=0xf0f0f0)
            embed.set_image(url=actualImages[0])
            await ctx.channel.send(embed=embed)
        except IndexError:
            await ctx.channel.send("Something went wrong! Try again later.")


def setup(bot):
    """
    Required for the functionality of cog
    :param bot: commands.Bot
    :return: None
    """
    bot.add_cog(MiscellaneousCog(bot))
