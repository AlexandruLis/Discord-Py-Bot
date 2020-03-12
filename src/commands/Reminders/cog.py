from discord.ext import commands
import time
from datetime import datetime
from dateutil import tz
from src.commands.Reminders.reminders import RemindersThreaded
from classified.globals import reminders_file_path
from src.commands.BotMiscellaneous.cog import MiscellaneousCog

reminders = None


class RemindersCog(commands.Cog):
    @commands.command()
    async def remind(self, ctx, date, message, repeatable):
        if repeatable == 'True' or repeatable == '1':
            repeatable = True
        else:
            repeatable = False

        reminderTime = date
        unix_time = RemindersCog.convertToLocalTime(datetime.strptime(reminderTime, '%Y/%m/%d %H:%M')).timestamp()
        if int(unix_time) < time.time():
            await ctx.channel.send("Cannot add a reminder in the past!")
            return
        reminders.add(int(unix_time), ctx.channel.guild.id, ctx.channel.id, ctx.message.author.id, message, repeatable)
        await ctx.channel.send("Added at {} UST with an accuracy of -+ 5 minutes".format(reminderTime))

    @commands.command()
    async def remindme(self, ctx):
        arguments = ctx.message.content.split()
        reminderTime = "".join(arguments[1])

        unix_time = time.time() + int(reminderTime) * 60

        message = ' '.join(arguments[2:])
        if int(unix_time) < time.time():
            await ctx.channel.send("Cannot add a reminder in the past!")
            return
        reminders.add(int(unix_time), ctx.channel.guild.id, ctx.channel.id, ctx.message.author.id, message)
        await ctx.channel.send("Added in {} -+ 2 minutes from now".format(reminderTime))

    @staticmethod
    def convertToLocalTime(localTime):
        from_zone = tz.tzutc()  # UTC TIME
        to_zone = tz.tzlocal()  # Machine code runs on TIME
        utc = localTime.replace(tzinfo=from_zone)  # TELL OBJECT IT'S IN UTC
        central = utc.astimezone(to_zone)  # CONVERT OBJECT TO MACHINE TIME
        return central

    @commands.command()
    async def cancel(self, ctx, userId, message):
        id_int = MiscellaneousCog.find_number_in_str(userId)
        if id_int == -1:
            await ctx.channel.send("Unknown ID")
            return
        if reminders.remove(id_int, message):
            await ctx.channel.send("Successfully removed")
            return
        await ctx.channel.send("Oops! Looks like something went wrong. Cannot remove")


def setup(bot):
    bot.add_cog(RemindersCog(bot))
    global reminders
    reminders = RemindersThreaded(reminders_file_path)
