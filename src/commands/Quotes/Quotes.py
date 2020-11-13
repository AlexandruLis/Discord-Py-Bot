import pickle
from src.core.Interfaces.DefaultContainer import PickleDefaultContainer


class Quotes(PickleDefaultContainer):
    """
    A Class meant to store bot replies to certain words/ sentences TODO
    Eg:

    -User types: "abc"
    -Bot responds with: "def"
    -Number at the end is the bit that decides if the trigger message (abc) gets deleted
    """

    def addQuote(self, key: str, quote: str, bits):
        """
        :return: status of the action -1 for invalid input, 0 for already present and 1 for success
        """
        if key is None:
            return -1
        elif key in self.dict:
            return 0
        if not self.testQuote(quote):
            return -1
        self.dict[key] = [quote, bits]
        return 1

    def removeByQuote(self, key: str):
        for value in self.dict:
            if self.dict[value][0] == key:
                self.dict.pop([value][0])
                return 1
        return -1

    def removeQuote(self, key: str):
        """
        :param key: the key of the message
        :return: status of the action, 0 for invalid input, -1 for not found, 1 for success
        """
        if key is None:
            return 0
        elif key not in self.dict:
            return -1
        self.dict.pop(key)
        return 1

    @staticmethod
    def testQuote(quote):
        """
        Checks if the message contents are good
        :param quote: the message that gets sent by typing a key
        :return: True or False
        """
        if len(quote) > 100:
            return False
        elif len(quote) < 3:
            return False
        return True

    def setBits(self, key: str, bits):
        """
        Set the bit that decides if the keyword message gets deleted or not
        :return: True/False
        """
        try:
            self.dict[key][1] = bits
            self.saveDict()
            return True
        except KeyError:
            return False

    def import_guild_quotes(self, filename):
        """
        This is made in case you want to import quotes from another file
        :param filename: name of the file (must be a pickle)
        :return: None
        """
        file = open(filename, "rb")
        dict_holder = pickle.load(file)
        self.dict = dict_holder
        self.saveDict()
