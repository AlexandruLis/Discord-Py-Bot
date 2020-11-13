import pickle
from src.commands.BotMiscellaneous.cog import MiscellaneousCog

class Blacklist:
    """
    TODO
    """

    def __init__(self, path):
        """
        :param path: file name or true path
        """
        self.file_path = path  # Dictionary picke location
        self.pasta_dict = self.load_dict_from_file()
        if self.pasta_dict is None:  # No dict found, make an empty one
            self.pasta_dict = {}

    @staticmethod
    def get_the_pasta(string: str):
        """

        :param string: receives a message.context (a string) and formats the contents ass a pasta
        :return: keymark (key) to be added in dictionary containing pasta (message)
        """
        try:
            keymark = string.split()  # Split the message text received into a string of words
            keymark.pop(0)  # Remove the command (.addpasta, .eatpasta, etc)
            # Add the words together and make the key everything before char(")
            keymark = " ".join(keymark).split('"')[0]
            keymark = keymark[:-1]  # Remove space from the end
            pasta = string.split('"')[1]  # everything inside the " " gets selected as the pasta
            bits = int(string.split('"')[2])  # everything after (just 0 or 1) becomes the bit
        except IndexError:
            keymark = None
            pasta = None
            bits = None
        if bits is None:  # If no bits are specified at the end they're automatically set to 1
            bits = 1
        return keymark, pasta, bits

    def save_dict_to_file(self):
        """
        Saves the dictionary to the file
        """
        file = open(self.file_path, "wb")
        pickle.dump(self.pasta_dict, file)
        file.close()

    def load_dict_from_file(self):
        """
        Loads the dictionary from the file
        """
        try:
            file = open(self.file_path, "rb")
            dict_holder = pickle.load(file)
            file.close()
            return dict_holder
        except EOFError:  # Dictionary file exists but it's empty or a bunch of spaces
            self.pasta_dict = {}
        except FileNotFoundError:  # Dictionary file doesnt exist
            file = open(self.file_path, "wb")
            file.close()

    def exists(self, message: str, channel):
        try:
            if message in self.pasta_dict[channel]['message']:
                return True
            elif message in self.pasta_dict[channel]['word']:
                return True
            else:
                for word in self.pasta_dict[channel]['word']:
                    if message.find(word) != -1:
                        return True
                numberList = MiscellaneousCog.findAllNumbersInString(message)
                if numberList != -1:
                    for emoji in self.pasta_dict[channel]['emoji']:
                        if emoji in numberList:
                            return True
            return False
        except KeyError:
            pass

    def userExists(self, userID, channel):
        try:
            if userID in self.pasta_dict[channel]['user']:
                return True
            return False
        except Exception:
            return False

    def addBlacklist(self, blacklist: str, channel, blklistType: str):
        """

        :param blacklist: key
        :param channel: discord channel
        :param blklistType: a sentence, a word, an emoji, etc
        :return: goodend = 1, badend =0, exists = -1
        """
        if channel in self.pasta_dict:
            if blklistType in self.pasta_dict[channel]:
                if blacklist in self.pasta_dict[channel][blklistType]:
                    return -1  # already exists
                else:
                    self.pasta_dict[channel][blklistType].append(blacklist)
            else:
                self.pasta_dict[channel][blklistType] = []
                self.pasta_dict[channel][blklistType].append(blacklist)
        else:
            self.pasta_dict[channel] = {}  # Add it to dictionary
            keys = ['user', 'emoji', 'message', 'word']
            for key in keys:
                self.pasta_dict[channel][key] = []
            self.pasta_dict[channel][blklistType].append(blacklist)

    def removeBlacklist(self, blacklist: str, channel, blklistType: str):
        """
        TODO
        """
        try:
            self.pasta_dict[channel][blklistType].remove(blacklist)
            return 1
        except Exception:
            return 0

    @staticmethod
    def test_pasta_text(pasta):
        """
        Checks if the message contents are good
        :param pasta: the message that gets sent by typing a key
        :return: True or False
        """
        if len(pasta) > 200:
            return False
        elif len(pasta) < 3:
            return False
        return True
