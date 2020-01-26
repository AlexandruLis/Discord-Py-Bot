from discord.ext import commands
import time
from datetime import datetime
from dateutil import tz
from src.commands.Reminders.reminders import RemindersThreaded
from classified.globals import reminders_file_path

reminders = None


class RemindersCog(commands.Cog):
    @commands.command()
    async def remind(self, ctx):
        arguments = ctx.message.content.split()
        reminderTime = "".join(arguments[1]) + ' ' + "".join(arguments[2])

        unix_time = RemindersCog.convertToLocalTime(datetime.strptime(reminderTime, '%Y/%m/%d %H:%M')).timestamp()

        message = ' '.join(arguments[3:])

        reminders.add(int(unix_time),ctx.channel.guild.id, ctx.channel.id, message)

    @staticmethod
    def convertToLocalTime(localTime):
        from_zone = tz.tzutc()  # UTC TIME
        to_zone = tz.tzlocal()  # Machine code runs on TIME
        utc = localTime.replace(tzinfo=from_zone)  # TELL OBJECT IT'S IN UTC
        central = utc.astimezone(to_zone)  # CONVERT OBJECT TO MACHINE TIME
        return central

    @commands.command()
    async def cancel(self, ctx):
        return
        message_to_stop = int(ctx.message.content.split()[1])
        global repeaters
        global counter
        if message_to_stop in repeaters:
            repeaters.remove(message_to_stop)
            counter -= 1

    @commands.command()
    async def repeat(self, ctx):
        return
        global repeaters
        global counter
        arguments = ctx.message.content.split('"')
        interval = arguments[0].split()[1]
        message = arguments[1]
        # print(datetime.datetime.utcnow())
        if interval.find(":") != -1:
            pass
            # TO DO daily at a certain hour
        else:
            async_counter = counter + 1
            counter += 1
            repeaters.append(async_counter)
            interval = int(interval)
            await ctx.channel.send('Start execution with id "{}"'.format(async_counter))
            while True:
                if async_counter in repeaters:
                    await ctx.channel.send(message)
                    await asyncio.sleep(interval)
                else:
                    await ctx.channel.send('Finished execution of "{}"'.format(async_counter))
                    return

    #         interval = int(interval)
    #         next_message_time = time.time() + interval
    #         print(time.time())
    #         print(next_message_time)
    #         while True:
    #             async for ctx_message in ctx.channel.history(limit=30):
    #                 if ctx_message.content == ctx.message.content:
    #                     break
    #                 if ctx_message.content.find(".cancel") != -1:
    #                     await ctx.channel.send('Finished execution of "{}"'.format(message))
    #                     return
    #             if next_message_time < time.time():
    #                 await ctx.channel.send(message)
    #                 next_message_time = time.time() + interval
    #             await asyncio.sleep(6)


def setup(bot):
    bot.add_cog(RemindersCog(bot))
    global reminders
    reminders = RemindersThreaded()
