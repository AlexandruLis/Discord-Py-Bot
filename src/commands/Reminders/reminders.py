import multiprocessing
import time
import pickle


class RemindersThreaded:

    def __init__(self, pathToFile):
        self.file_path = pathToFile
        self.item_dict = {}
        self.key = None

    def save_dict_to_file(self):
        """
        Saves the dictionary to the file
        """
        file = open(self.file_path, "wb")
        pickle.dump(self.item_dict.copy(), file)
        file.close()

    def load_dict_from_file(self):
        """
        Loads the dictionary from the file
        """
        import pathlib
        print(pathlib.Path().absolute())

        try:
            file = open(self.file_path, "rb")
            dict_holder = pickle.load(file)
            file.close()
            return dict_holder
        except EOFError:  # Dictionary file exists but it's empty or a bunch of spaces
            return {}

        except FileNotFoundError:  # Dictionary file doesnt exist
            file = open(self.file_path, "wb")
            file.close()
            return {}

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
                for key in self.item_dict.keys():
                    # print(self.item_dict[key]['time'])
                    if len(self.item_dict) and self.item_dict[key]['time'] - time.time() < 60:
                        if self.item_dict[key]['repeatable']:
                            self.add(self.item_dict[key]['time'] + 86400, self.item_dict[key]['guild'],
                                     self.item_dict[key]['channel'], self.item_dict[key]['user'],
                                     self.item_dict[key]['message'], self.item_dict[key]['repeatable'], key)
                        self.key.value = key
                        break
            time.sleep(30)
            self.save_dict_to_file()
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

    def add(self, time, guild, channel, userId, message, repeatable=False, key=None):
        position = len(self.item_dict) + 1
        if repeatable and key != None:
            position = key
        self.item_dict[position] = {'guild': guild, 'channel': channel, 'user': userId,
                                    'message': message, 'time': time, 'repeatable': repeatable}
        print(self.item_dict.copy())
        self.save_dict_to_file()

    def remove(self, userId, msg_key):
        if len(self.item_dict):
            for item in self.item_dict.keys():
                print(item, userId, msg_key)
                if self.item_dict[item]['user'] == userId:
                    if self.item_dict[item]['message'].find(msg_key) != -1:
                        self.item_dict.pop(item)
                        self.save_dict_to_file()
                        print(self.item_dict)
                        return True
            return False
