import multiprocessing
import time


class RemindersThreaded:

    def __init__(self):
        self.item_dict = {}
        self.key = None

    def startThread(self, dictionary, client, value):
        print("Starting reminders thread...")
        self.item_dict = dictionary
        self.key = value
        eventLoop = multiprocessing.Process(target=self.reminderEventLoop)
        eventLoop.start()  # No reason to join it...

    def reminderEventLoop(self):
        print("Started Reminders Thread!")
        while True:
            if len(self.item_dict):
                for unixTime in self.item_dict.keys():
                    if len(self.item_dict) and abs(unixTime - time.time()) < 310:
                        self.key.value = unixTime
                        break
            time.sleep(30)
            # print("FUCK")
            # print(self.item_dict)
            # print(self.key)

    async def executeReminder(self, key):
        # from discord.ext import commands
        from classified.bot_token.token import bot_token
        # client = commands.Bot(command_prefix=".")

        # await client.start(bot_token)
        # print(client)
        # await client.close()
        # await self.item_dict[key]['channel'].send(self.item_dict[key]['message'])

    def add(self, time, guild, channel, message):
        self.item_dict[time] = {'guild': guild, 'channel': channel, 'message': message}
        # self.save_dict_to_file()
