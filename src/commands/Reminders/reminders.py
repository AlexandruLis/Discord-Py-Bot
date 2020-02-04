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

    def add(self, time, guild, channel, userId, message):
        self.item_dict[len(self.item_dict) + 1] = {'guild': guild, 'channel': channel, 'user': userId,
                                                   'message': message, 'time': time}
        print(self.item_dict.copy())
        self.save_dict_to_file()
