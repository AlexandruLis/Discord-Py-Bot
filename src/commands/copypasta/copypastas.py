import pickle


class Quotes:
    """
    A Class meant to store bot replies to certain words/ sentences TODO
    Eg:
    .addpasta abc "def" 1
    -User types: "abc"
    -Bot responds with: "def"
    -Number at the end is the bit that decides if the trigger message (abc) gets deleted
    """

    def __init__(self, path):
        """
        A file path where to store the dictionary of copypastas in a pickle format
        :param path: file name or true path
        """
        self.filePath = path  # Dictionary pickle location
        self.quotesDict = self.loadDict()
        if self.quotesDict is None:  # No dict found, make an empty one
            self.quotesDict = {}
            self.saveDict()

    def saveDict(self):
        """
        Saves the dictionary to the file
        """
        file = open(self.filePath, "wb")
        pickle.dump(self.quotesDict, file)
        file.close()

    def loadDict(self):
        """
        Loads the dictionary from the file
        """
        try:
            file = open(self.filePath, "rb")
            dictHolder = pickle.load(file)
            file.close()
            return dictHolder
        except EOFError:  # Dictionary file exists but it's empty or a bunch of spaces
            self.quotesDict = {}
        except FileNotFoundError:  # Dictionary file doesnt exist
            file = open(self.filePath, "wb")
            file.close()

    def addQuote(self, key: str, quote: str, bits):
        """
        Adds a copypasta
        :return: status of the action -1 for invalid input, 0 for already present and 1 for success
        """
        if key is None:
            return -1
        elif key in self.quotesDict:
            return 0
        if not self.testQuote(quote):
            return -1
        self.quotesDict[key] = [quote, bits]
        return 1

    def removeByQuote(self, key: str):
        for value in self.quotesDict:
            if self.quotesDict[value][0] == key:
                self.quotesDict.pop([value][0])
                return 1
        return -1

    def removeQuote(self, key: str):
        """
        Removes a copypasta
        :param key: the key of the message
        :return: status of the action, 0 for invalid input, -1 for not found, 1 for success
        """
        if key is None:
            return 0
        elif key not in self.quotesDict:
            return -1
        self.quotesDict.pop(key)
        return 1

    @staticmethod
    def testQuote(pasta):
        """
        Checks if the message contents are good
        :param pasta: the message that gets sent by typing a key
        :return: True or False
        """
        if len(pasta) > 100:
            return False
        elif len(pasta) < 3:
            return False
        return True

    def update_to_access_bits(self):
        """
        This function is only used if the dictionary isn't made from lists ( from the old version )
        to change it to a proper setup. Mainly ignore.
        :return:
        """
        for pasta in self.quotesDict:
            x = self.quotesDict[pasta]
            self.quotesDict[pasta] = [x, 1]
        self.saveDict()
        print(self.quotesDict)

    def setBits(self, key: str, bits):
        """
        Set the bit that decides if the keyword message gets deleted or not
        Command eg: .pastabits abc | 1
        - abc = key
        - | = delimiter
        - 1 bit gets set to
        :param msg: Message text
        :return: True/False
        """
        try:
            self.quotesDict[key][1] = bits
            self.saveDict()
            return True
        except KeyError:
            return False

    def import_guild_pastas(self, filename):
        """
        This is made in case you want to import pastas from another file
        :param filename: name of the file (must be a pickle)
        :return: None
        """
        file = open(filename, "rb")
        dict_holder = pickle.load(file)
        self.quotesDict = dict_holder
        self.save_dict_to_file()
